import { createHash, timingSafeEqual } from "node:crypto"

// Recebe o webhook de vendas da Hest (pedido pago, reembolsado ou com chargeback).
// 1. Confere o X-Webhook-Token com o segredo guardado na Vercel (HEST_WEBHOOK_TOKEN).
// 2. Grava a venda na planilha SEM dados pessoais (LGPD): só pedido, produto, valores e comissão.
// 3. Se o pedido foi pago, manda o evento Purchase para a API de Conversões da Meta, com e-mail
//    e telefone em hash SHA-256 (a Meta exige assim). O id do pedido vira event_id, o que evita
//    contar a mesma venda duas vezes quando a Hest reenvia o webhook.
// Tokens e chaves ficam só nas variáveis de ambiente da Vercel, nunca no código.

const TAMANHO_MAXIMO = 64000 // bytes do corpo
const META_VERSAO = "v23.0"

const resposta = (status) => Response.json({ success: status === 200 }, { status })

const sha256 = (texto) => createHash("sha256").update(texto).digest("hex")

export function tokenValido(recebido, esperado) {
  if (!recebido || !esperado) return false
  // compara os hashes (mesmo tamanho) para não vazar nada pelo tempo de resposta
  return timingSafeEqual(Buffer.from(sha256(recebido)), Buffer.from(sha256(esperado)))
}

export function hashMeta(valor) {
  const normalizado = String(valor ?? "").trim().toLowerCase()
  return normalizado ? sha256(normalizado) : null
}

export function telefoneMeta(telefone) {
  let digitos = String(telefone ?? "").replace(/\D/g, "")
  if (digitos.length === 10 || digitos.length === 11) digitos = `55${digitos}`
  return digitos.length >= 12 && digitos.length <= 13 ? digitos : null
}

const reais = (centavos) => (Number.isFinite(Number(centavos)) ? Math.round(Number(centavos)) / 100 : null)

function linhaPlanilha(venda, evento) {
  const { order = {}, product = {}, freight = {}, commissions = [] } = venda
  const afiliado = commissions.find((c) => c?.type === "afiliado")
  const bumps = Array.isArray(venda.orderBumps) ? venda.orderBumps : []
  const centavosBumps = bumps.reduce((soma, b) => soma + (Number(b?.affiliateAmount) || 0), 0)
  return {
    dataHora: new Intl.DateTimeFormat("pt-BR", {
      timeZone: "America/Sao_Paulo",
      dateStyle: "short",
      timeStyle: "medium",
    }).format(new Date()),
    evento,
    pedido: String(order.id),
    produto: product.name ?? "",
    sku: product.sku ?? "",
    quantidade: product.total_quantity ?? product.quantity ?? null,
    valorPedido: reais(order.amount),
    frete: reais(freight.amount),
    comissaoAfiliado: reais(afiliado?.value),
    pagamento: order.payment_method ?? "",
    criadoEm: order.created_at ?? "",
    // order bump: oferta extra no checkout, com comissão própria da afiliada
    bumps: bumps.map((b) => b?.title ?? "").filter(Boolean).join("; "),
    comissaoBumps: reais(centavosBumps),
  }
}

function eventoMeta(venda) {
  const { order = {}, customer = {}, product = {} } = venda
  const userData = {}
  const email = hashMeta(customer.email)
  const telefone = telefoneMeta(customer.phone)
  if (email) userData.em = [email]
  if (telefone) userData.ph = [sha256(telefone)]
  userData.country = [sha256("br")]
  return {
    data: [
      {
        event_name: "Purchase",
        event_time: Math.floor(Date.now() / 1000),
        event_id: String(order.id),
        // a venda acontece no checkout da Hest, fora do site: por isso "other" e não "website"
        action_source: "other",
        user_data: userData,
        custom_data: {
          currency: order.currency || "BRL",
          value: reais(order.amount),
          content_ids: product.id ? [String(product.id)] : [],
          content_name: product.name ?? "",
          content_type: "product",
          num_items: product.total_quantity ?? product.quantity ?? 1,
        },
      },
    ],
  }
}

async function gravarPlanilha(linha, env, fetchFn) {
  const destino = env.PLANILHA_VENDAS_URL
  const chave = env.PLANILHA_VENDAS_CHAVE
  if (!destino || !chave) {
    console.log("venda (planilha não configurada)", JSON.stringify(linha))
    return
  }
  const r = await fetchFn(destino, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ ...linha, chave }),
  })
  // o script do Google responde 200 até quando falha (página de erro em HTML), então confere o "ok" do texto
  const retorno = (await r.text()).trim()
  if (!r.ok || retorno !== "ok") throw new Error(`planilha respondeu ${r.status}: ${retorno.slice(0, 200)}`)
}

async function enviarMeta(venda, env, fetchFn) {
  const pixel = env.META_PIXEL_ID
  const token = env.META_CAPI_TOKEN
  if (!pixel || !token) return
  const url = `https://graph.facebook.com/${META_VERSAO}/${encodeURIComponent(pixel)}/events?access_token=${encodeURIComponent(token)}`
  const r = await fetchFn(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(eventoMeta(venda)),
  })
  if (!r.ok) throw new Error(`Meta respondeu ${r.status}: ${(await r.text()).slice(0, 300)}`)
}

export async function tratarVenda(request, { env = process.env, fetch: fetchFn = fetch } = {}) {
  if (!env.HEST_WEBHOOK_TOKEN) {
    console.error("HEST_WEBHOOK_TOKEN não configurado")
    return resposta(503)
  }
  if (!tokenValido(request.headers.get("x-webhook-token"), env.HEST_WEBHOOK_TOKEN)) return resposta(401)

  const texto = await request.text()
  if (texto.length > TAMANHO_MAXIMO) return resposta(413)

  let venda
  try {
    venda = JSON.parse(texto)
  } catch {
    return resposta(400)
  }
  if (!venda || typeof venda !== "object" || !venda.order?.id) return resposta(400)

  // a Hest manda o tipo no status do pedido ("paid", "refunded", "chargedback"); aceita também "order.paid"
  const evento = String(venda.event ?? venda.order.status ?? "").replace(/^order\./, "").toLowerCase()

  // as mensagens de erro não levam URL, chave nem token; só quem mandou o token certo chega aqui e as vê
  const erros = []
  try {
    await gravarPlanilha(linhaPlanilha(venda, evento), env, fetchFn)
  } catch (erro) {
    console.error(erro)
    erros.push(erro.message)
  }
  if (evento === "paid") {
    try {
      await enviarMeta(venda, env, fetchFn)
    } catch (erro) {
      console.error(erro)
      erros.push(erro.message)
    }
  }
  if (erros.length) return Response.json({ success: false, erro: erros.join(" | ") }, { status: 502 })
  return resposta(200)
}
