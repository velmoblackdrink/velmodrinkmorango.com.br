// Testes do cadastro de e-mail (api/cadastro.mjs).
// Rodar com: node --test tests/
import { test } from "node:test"
import assert from "node:assert/strict"
import { tratarCadastro, emailValido, TEXTO_CONSENTIMENTO } from "../api/_lib/cadastro.mjs"

const ENV = { CADASTRO_PLANILHA_URL: "https://script.google.com/teste", CADASTRO_PLANILHA_CHAVE: "chave-teste" }

function pedido(corpo, origem = "https://velmodrinkmorango.com.br") {
  const headers = { "content-type": "application/json" }
  if (origem) headers.origin = origem
  return new Request("https://velmodrinkmorango.com.br/api/cadastro", {
    method: "POST", headers, body: typeof corpo === "string" ? corpo : JSON.stringify(corpo),
  })
}

function fetchFalso(retorno = "ok") {
  const chamadas = []
  const fn = async (url, opcoes) => {
    chamadas.push({ url: String(url), corpo: JSON.parse(opcoes.body) })
    return new Response(retorno, { status: 200 })
  }
  return { fn, chamadas }
}

const valido = { email: " Fulana@Exemplo.com ", consentimento: true, pagina: "inicio" }

test("grava e-mail com consentimento, texto aceito e versão da política", async () => {
  const f = fetchFalso()
  const r = await tratarCadastro(pedido(valido), { env: ENV, fetch: f.fn })
  assert.equal(r.status, 200)
  assert.equal(f.chamadas.length, 1)
  const c = f.chamadas[0].corpo
  assert.equal(c.tipo, "cadastro")
  assert.equal(c.chave, "chave-teste")
  assert.equal(c.email, "fulana@exemplo.com")
  assert.equal(c.consentimento, TEXTO_CONSENTIMENTO)
  assert.match(c.versaoPolitica, /^\d{4}-\d{2}-\d{2}$/)
  assert.equal(c.pagina, "inicio")
})

test("sem a caixa marcada não grava", async () => {
  for (const consentimento of [false, "true", undefined]) {
    const f = fetchFalso()
    const r = await tratarCadastro(pedido({ ...valido, consentimento }), { env: ENV, fetch: f.fn })
    assert.equal(r.status, 400)
    assert.equal(f.chamadas.length, 0)
  }
})

test("pedido de fora do site é recusado", async () => {
  for (const origem of ["https://golpe.com", null, "https://velmodrinkmorango.com.br.golpe.com"]) {
    const f = fetchFalso()
    const r = await tratarCadastro(pedido(valido, origem), { env: ENV, fetch: f.fn })
    assert.equal(r.status, 403, String(origem))
    assert.equal(f.chamadas.length, 0)
  }
  const f = fetchFalso()
  assert.equal((await tratarCadastro(pedido(valido, "https://www.velmodrinkmorango.com.br"), { env: ENV, fetch: f.fn })).status, 200)
})

test("robô que preenche o campo escondido recebe ok e nada é gravado", async () => {
  const f = fetchFalso()
  const r = await tratarCadastro(pedido({ ...valido, site: "http://spam" }), { env: ENV, fetch: f.fn })
  assert.equal(r.status, 200)
  assert.equal(f.chamadas.length, 0)
})

test("e-mail inválido ou que viraria fórmula na planilha é recusado", () => {
  for (const e of ["", "sem-arroba", "a@b", "=SOMA(A1)@x.com", "+1@x.com", "-x@x.com", "a b@x.com", `${"a".repeat(250)}@x.com`])
    assert.equal(emailValido(e), null, e)
  assert.equal(emailValido("Ana.Paula+ofertas@Gmail.com"), "ana.paula+ofertas@gmail.com")
})

test("corpo grande, JSON quebrado e planilha fora do ar", async () => {
  const f = fetchFalso()
  assert.equal((await tratarCadastro(pedido("x".repeat(3000)), { env: ENV, fetch: f.fn })).status, 413)
  assert.equal((await tratarCadastro(pedido("{quebrado"), { env: ENV, fetch: f.fn })).status, 400)
  assert.equal((await tratarCadastro(pedido(valido), { env: {}, fetch: f.fn })).status, 503)
  assert.equal(f.chamadas.length, 0)
  const negado = fetchFalso("negado")
  assert.equal((await tratarCadastro(pedido(valido), { env: ENV, fetch: negado.fn })).status, 502)
})
