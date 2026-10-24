// Recebe o e-mail do campo "Receba Ofertas Exclusivas" (rodapé da página inicial).
// 1. Só aceita pedidos vindos do próprio site (cabeçalho Origin).
// 2. Só grava com a caixa de consentimento marcada (LGPD): guarda junto o texto aceito e a versão da política.
// 3. Grava na aba "Cadastros" da planilha de vendas, pelo mesmo script do Google (PLANILHA_VENDAS_URL/CHAVE).
// A chave fica só na Vercel; o navegador nunca a vê.

const TAMANHO_MAXIMO = 2000 // bytes do corpo
export const VERSAO_POLITICA = "2026-10-24"
export const TEXTO_CONSENTIMENTO =
  "Aceito receber ofertas e novidades do Velmo Drink por e-mail. Li a Política de Privacidade e sei que posso cancelar quando quiser."

const ORIGENS = [/^https:\/\/(www\.)?velmodrinkmorango\.com\.br$/, /^https:\/\/[a-z0-9-]+\.vercel\.app$/, /^http:\/\/localhost(:\d+)?$/]

const resposta = (status, extra = {}) => Response.json({ success: status === 200, ...extra }, { status })

export function origemPermitida(origem) {
  return !!origem && ORIGENS.some((r) => r.test(origem))
}

// Começa com letra ou número: um e-mail como "=SOMA(...)@x.com" viraria fórmula na planilha.
export function emailValido(valor) {
  const email = String(valor ?? "").trim().toLowerCase()
  return email.length <= 254 && /^[a-z0-9][a-z0-9._%+-]*@[a-z0-9-]+(\.[a-z0-9-]+)*\.[a-z]{2,}$/.test(email) ? email : null
}

const paginaLimpa = (valor) => String(valor ?? "").toLowerCase().replace(/[^a-z0-9-]/g, "").slice(0, 80) || "inicio"

export async function tratarCadastro(request, { env = process.env, fetch: fetchFn = fetch } = {}) {
  if (!origemPermitida(request.headers.get("origin"))) return resposta(403)

  const texto = await request.text()
  if (texto.length > TAMANHO_MAXIMO) return resposta(413)
  let dados
  try {
    dados = JSON.parse(texto)
  } catch {
    return resposta(400)
  }
  if (!dados || typeof dados !== "object") return resposta(400)

  // campo escondido: gente não vê nem preenche; robô preenche. Finge que deu certo e não grava.
  if (dados.site) return resposta(200)

  const email = emailValido(dados.email)
  if (!email) return resposta(400, { erro: "email" })
  if (dados.consentimento !== true) return resposta(400, { erro: "consentimento" })

  const destino = env.PLANILHA_VENDAS_URL
  const chave = (env.PLANILHA_VENDAS_CHAVE || "").trim()
  if (!destino || !chave) {
    console.error("cadastro: planilha não configurada")
    return resposta(503)
  }

  const linha = {
    tipo: "cadastro",
    chave,
    dataHora: new Intl.DateTimeFormat("pt-BR", { timeZone: "America/Sao_Paulo", dateStyle: "short", timeStyle: "medium" }).format(new Date()),
    email,
    pagina: paginaLimpa(dados.pagina),
    consentimento: TEXTO_CONSENTIMENTO,
    versaoPolitica: VERSAO_POLITICA,
  }
  try {
    const r = await fetchFn(destino, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(linha) })
    const retorno = (await r.text()).trim()
    if (!r.ok || retorno !== "ok") throw new Error(`planilha respondeu ${r.status}: ${retorno.slice(0, 120)}`)
  } catch (erro) {
    console.error("cadastro:", erro.message)
    return resposta(502)
  }
  return resposta(200)
}
