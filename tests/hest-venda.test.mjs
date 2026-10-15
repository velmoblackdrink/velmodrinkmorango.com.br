// Testes da rota que recebe as vendas da Hest (api/hest/venda.mjs).
// Rodar com: node --test tests/
import { test } from "node:test"
import assert from "node:assert/strict"
import { createHash } from "node:crypto"
import { tratarVenda, hashMeta, telefoneMeta } from "../api/_lib/hest.mjs"

const TOKEN = "token-de-teste"
const ENV = {
  HEST_WEBHOOK_TOKEN: TOKEN,
  PLANILHA_VENDAS_URL: "https://script.google.com/teste",
  PLANILHA_VENDAS_CHAVE: "chave-teste",
  META_PIXEL_ID: "123",
  META_CAPI_TOKEN: "meta-teste",
}

function exemplo(status = "paid") {
  return {
    value: 4590,
    order: { id: "ped-1", status, payment_method: "pix", amount: 23980, currency: "BRL", created_at: "2026-10-15T12:00:00Z" },
    customer: {
      name: "Fulana de Tal", email: " Fulana@Exemplo.com ", document: "12345678900", phone: "(11) 98765-4321",
      address: { street: "Rua A", number: "1", city: "São Paulo", state: "SP", zipcode: "01000000" },
    },
    product: { id: "prod-9", name: "Velmo Black Drink - Morango", price: 20990, quantity: 1, total_quantity: 1, sku: "VBD-M" },
    freight: { amount: 2990, method: "PAC" },
    commissions: [
      { id: "c1", type: "produtor", name: "Produtor", email: "p@x.com", value: 15000 },
      { id: "c2", type: "afiliado", name: "Afiliada", email: "a@x.com", value: 4590 },
    ],
    orderBumps: [],
  }
}

function pedido(corpo, token = TOKEN) {
  const headers = { "content-type": "application/json" }
  if (token !== null) headers["x-webhook-token"] = token
  return new Request("https://velmodrinkmorango.com.br/api/hest/venda", {
    method: "POST", headers, body: typeof corpo === "string" ? corpo : JSON.stringify(corpo),
  })
}

// fetch falso: guarda as chamadas e responde como a planilha ("ok") e a Meta (JSON)
function fetchFalso() {
  const chamadas = []
  const fn = async (url, opcoes) => {
    chamadas.push({ url: String(url), corpo: JSON.parse(opcoes.body) })
    if (String(url).includes("graph.facebook.com")) return new Response('{"events_received":1}', { status: 200 })
    return new Response("ok", { status: 200 })
  }
  return { fn, chamadas }
}

const sha = (texto) => createHash("sha256").update(texto).digest("hex")

test("sem HEST_WEBHOOK_TOKEN configurado responde 503 e não chama nada", async () => {
  const f = fetchFalso()
  const resposta = await tratarVenda(pedido(exemplo()), { env: {}, fetch: f.fn })
  assert.equal(resposta.status, 503)
  assert.equal(f.chamadas.length, 0)
})

test("token errado ou ausente responde 401 e não chama nada", async () => {
  const f = fetchFalso()
  assert.equal((await tratarVenda(pedido(exemplo(), "errado"), { env: ENV, fetch: f.fn })).status, 401)
  assert.equal((await tratarVenda(pedido(exemplo(), null), { env: ENV, fetch: f.fn })).status, 401)
  assert.equal(f.chamadas.length, 0)
})

test("corpo grande demais responde 413", async () => {
  const f = fetchFalso()
  const resposta = await tratarVenda(pedido("x".repeat(70000)), { env: ENV, fetch: f.fn })
  assert.equal(resposta.status, 413)
})

test("JSON inválido ou sem id do pedido responde 400", async () => {
  const f = fetchFalso()
  assert.equal((await tratarVenda(pedido("{nao e json"), { env: ENV, fetch: f.fn })).status, 400)
  assert.equal((await tratarVenda(pedido({ order: {} }), { env: ENV, fetch: f.fn })).status, 400)
  assert.equal(f.chamadas.length, 0)
})

test("venda paga grava na planilha SEM dados pessoais", async () => {
  const f = fetchFalso()
  const resposta = await tratarVenda(pedido(exemplo()), { env: ENV, fetch: f.fn })
  assert.equal(resposta.status, 200)
  const planilha = f.chamadas.find((c) => c.url === ENV.PLANILHA_VENDAS_URL)
  assert.ok(planilha, "não chamou a planilha")
  assert.deepEqual(
    { ...planilha.corpo, dataHora: "x" },
    {
      dataHora: "x", evento: "paid", pedido: "ped-1", produto: "Velmo Black Drink - Morango", sku: "VBD-M",
      quantidade: 1, valorPedido: 239.8, frete: 29.9, comissaoAfiliado: 45.9, pagamento: "pix",
      criadoEm: "2026-10-15T12:00:00Z", bumps: "", comissaoBumps: 0, chave: "chave-teste",
    },
  )
  const texto = JSON.stringify(planilha.corpo)
  for (const pessoal of ["Fulana", "12345678900", "98765", "Rua A", "01000000", "a@x.com"]) {
    assert.ok(!texto.includes(pessoal), `planilha recebeu dado pessoal: ${pessoal}`)
  }
})

test("venda paga manda Purchase para a Meta com e-mail e telefone em hash", async () => {
  const f = fetchFalso()
  await tratarVenda(pedido(exemplo()), { env: ENV, fetch: f.fn })
  const meta = f.chamadas.find((c) => c.url.includes("graph.facebook.com"))
  assert.ok(meta, "não chamou a Meta")
  assert.match(meta.url, /\/123\/events\?access_token=meta-teste$/)
  const [evento] = meta.corpo.data
  assert.equal(evento.event_name, "Purchase")
  assert.equal(evento.event_id, "ped-1")
  assert.deepEqual(evento.user_data.em, [sha("fulana@exemplo.com")])
  assert.deepEqual(evento.user_data.ph, [sha("5511987654321")])
  assert.equal(evento.custom_data.value, 239.8)
  assert.equal(evento.custom_data.currency, "BRL")
  const texto = JSON.stringify(meta.corpo)
  for (const pessoal of ["Fulana", "fulana@", "12345678900", "98765-4321", "Rua A"]) {
    assert.ok(!texto.includes(pessoal), `Meta recebeu dado pessoal sem hash: ${pessoal}`)
  }
})

test("reembolso e chargeback gravam na planilha mas não mandam Purchase", async () => {
  for (const status of ["refunded", "chargedback"]) {
    const f = fetchFalso()
    const resposta = await tratarVenda(pedido(exemplo(status)), { env: ENV, fetch: f.fn })
    assert.equal(resposta.status, 200)
    assert.equal(f.chamadas.length, 1)
    assert.equal(f.chamadas[0].corpo.evento, status)
  }
})

test("sem planilha e sem Meta configuradas ainda responde 200 (só registra no log)", async () => {
  const f = fetchFalso()
  const resposta = await tratarVenda(pedido(exemplo()), { env: { HEST_WEBHOOK_TOKEN: TOKEN }, fetch: f.fn })
  assert.equal(resposta.status, 200)
  assert.equal(f.chamadas.length, 0)
})

test("planilha com erro responde 502 para a Hest tentar de novo", async () => {
  const fn = async (url) =>
    String(url).includes("graph.facebook.com") ? new Response("{}") : new Response("<html>erro</html>", { status: 200 })
  const resposta = await tratarVenda(pedido(exemplo()), { env: ENV, fetch: fn })
  assert.equal(resposta.status, 502)
  // quem tem o token vê o motivo (sem segredo nenhum), para dar para diagnosticar sem abrir os Logs
  const corpo = await resposta.json()
  assert.match(corpo.erro, /^planilha respondeu 200: <html>erro/)
  assert.ok(!JSON.stringify(corpo).includes(ENV.PLANILHA_VENDAS_URL))
  assert.ok(!JSON.stringify(corpo).includes(ENV.PLANILHA_VENDAS_CHAVE))
})

test("order bumps entram na planilha com a comissão da afiliada", async () => {
  const f = fetchFalso()
  const venda = exemplo()
  venda.orderBumps = [
    { bumpKey: "12", title: "Oferta especial", amount: 2990, producerAmount: 2392, affiliateAmount: 598 },
    { bumpKey: "13", title: "Outra oferta", amount: 1000, affiliateAmount: 200 },
  ]
  await tratarVenda(pedido(venda), { env: ENV, fetch: f.fn })
  const planilha = f.chamadas.find((c) => c.url === ENV.PLANILHA_VENDAS_URL)
  assert.equal(planilha.corpo.bumps, "Oferta especial; Outra oferta")
  assert.equal(planilha.corpo.comissaoBumps, 7.98)
})

test("hashMeta normaliza antes do hash; telefoneMeta põe o 55 do Brasil", () => {
  assert.equal(hashMeta("  A@B.com "), sha("a@b.com"))
  assert.equal(hashMeta(""), null)
  assert.equal(telefoneMeta("(11) 98765-4321"), "5511987654321")
  assert.equal(telefoneMeta("+55 11 98765-4321"), "5511987654321")
  assert.equal(telefoneMeta("123"), null)
})
