// Testes do rastreio: GTM/GA4/og:image em todas as páginas (fonte/rastreio.py) e as regras de UTM do js/rastreio.js.
// Rodar com: node --test tests/
import { test } from "node:test"
import assert from "node:assert/strict"
import { execFileSync } from "node:child_process"
import { cpSync, existsSync, mkdtempSync, readFileSync, readdirSync } from "node:fs"
import { tmpdir } from "node:os"
import { join } from "node:path"
import { fileURLToPath } from "node:url"
import vm from "node:vm"

const RAIZ = fileURLToPath(new URL("..", import.meta.url))
const PAGINAS = readdirSync(RAIZ).filter((n) => n.endsWith(".html"))
const ler = (nome, pasta = RAIZ) => readFileSync(join(pasta, nome), "utf8")
const conta = (texto, trecho) => texto.split(trecho).length - 1

test("toda página tem GTM e GA4 uma vez só, com consentimento negado antes do config e sem noscript do GTM", () => {
  for (const nome of PAGINAS) {
    const doc = ler(nome)
    assert.equal(conta(doc, "gtm.js?id="), 1, `${nome}: GTM`)
    assert.equal(conta(doc, "gtag/js?id=G-Z921CFD04J"), 1, `${nome}: GA4`)
    assert.equal(conta(doc, "gtag('config'"), 1, `${nome}: config do GA4`)
    assert.equal(conta(doc, "gtag('consent','default'"), 1, `${nome}: consentimento padrão`)
    assert.ok(doc.indexOf("gtag('consent','default'") < doc.indexOf("gtag('config'"), `${nome}: consentimento antes do config`)
    assert.equal(conta(doc, "ns.html?id="), 0, `${nome}: noscript carregaria o GTM sem aceite`)
    assert.equal(conta(doc, 'src="js/rastreio.js"'), 1, `${nome}: rastreio.js`)
  }
})

// Roda o bloco do <head> como o navegador, com a escolha guardada, e diz se o GTM carregou e o consentimento dado.
function rodarHead(guardado) {
  const doc = ler("clarize.html")
  const codigo = doc.match(/<script>(window\.dataLayer=[\s\S]*?)<\/script>/)[1]
  const inseridos = []
  const elemento = { parentNode: { insertBefore: (j) => inseridos.push(j.src) } }
  const janela = {}
  const contexto = {
    window: janela, Date,
    localStorage: { getItem: () => (guardado === undefined ? null : JSON.stringify(guardado)) },
    document: { getElementsByTagName: () => [elemento], createElement: () => ({}) },
  }
  contexto.window = contexto
  vm.runInNewContext(codigo, contexto)
  const padrao = contexto.dataLayer.find((a) => a[0] === "consent" && a[1] === "default")
  return { gtm: inseridos.some((s) => s.includes("gtm.js")), analytics: padrao[2].analytics_storage, escolha: contexto.velmoCookies }
}

test("GTM (Clarity) só carrega com aceite guardado há menos de 12 meses", () => {
  assert.deepEqual(rodarHead(undefined), { gtm: false, analytics: "denied", escolha: null })
  assert.deepEqual(rodarHead({ escolha: "recusado", em: Date.now() }), { gtm: false, analytics: "denied", escolha: "recusado" })
  assert.deepEqual(rodarHead({ escolha: "aceito", em: Date.now() }), { gtm: true, analytics: "granted", escolha: "aceito" })
  const velho = Date.now() - 400 * 24 * 3600 * 1000
  assert.deepEqual(rodarHead({ escolha: "aceito", em: velho }), { gtm: false, analytics: "denied", escolha: null })
})

test("política de privacidade existe, está no rodapé, no mapa do site e no formulário da home", () => {
  const politica = ler("politica-de-privacidade.html")
  assert.match(politica, /Atendimento Velmo Black/)
  assert.match(politica, /id="cookies"/)
  assert.match(ler("js/main.js"), /href="politica-de-privacidade\.html"/)
  assert.match(ler("js/main.js"), /data-abrir-cookies/)
  assert.match(ler("mapa-do-site.html"), /href="politica-de-privacidade\.html"/)
  const home = ler("index.html")
  assert.ok(!home.includes("offondigital.github.io/velmo-black-drink/privacidade"), "link antigo da política")
  const form = home.match(/<form[^>]*data-cadastro[\s\S]*?<\/form>/)[0]
  assert.match(form, /name="email"/)
  assert.match(form, /type="checkbox" name="consentimento" required/)
  assert.match(form, /href="politica-de-privacidade\.html"/)
  assert.match(home, /src="js\/cadastro\.js"/)
})

test("toda página tem og:image absoluta de 1200x630 que existe, e um og:url igual ao canonical", () => {
  for (const nome of PAGINAS) {
    const doc = ler(nome)
    const imgs = [...doc.matchAll(/<meta property="og:image" content="https:\/\/velmodrinkmorango\.com\.br\/(img\/og\/[a-z-]+\.jpg)">/g)]
    assert.equal(imgs.length, 1, `${nome}: og:image`)
    assert.ok(existsSync(join(RAIZ, imgs[0][1])), `${nome}: ${imgs[0][1]} existe`)
    assert.match(doc, /<meta name="twitter:card" content="summary_large_image">/, nome)
    const urls = [...doc.matchAll(/<meta property="og:url" content="([^"]+)">/g)].map((m) => m[1])
    const canon = doc.match(/<link rel="canonical" href="([^"]+)"/)
    assert.deepEqual(urls, [canon[1]], `${nome}: og:url`)
  }
})

test("página de produto e post usam a foto do produto certo", () => {
  const img = (nome) => ler(nome).match(/og:image" content="[^"]*\/og\/([a-z-]+)\.jpg"/)[1]
  assert.equal(img("clarize.html"), "clarize")
  assert.equal(img("creagym.html"), "creagym")
  assert.equal(img("creatina-gummy.html"), "creatina-gummy")
  assert.equal(img("como-tomar-creatina.html"), "creagym")
  assert.equal(img("index.html"), "velmo-drink")
})

test("só dois botões de compartilhar (Compartilhar e Copiar link), com UTM, fora do mapa do site", () => {
  const doc = ler("clarize.html")
  assert.equal(conta(doc, 'class="compartilhar"'), 1)
  assert.ok(doc.includes('data-rede="compartilhar" data-url="https://velmodrinkmorango.com.br/clarize.html?utm_source=compartilhar&amp;utm_medium=social&amp;utm_campaign=compartilhar&amp;utm_content=clarize"'))
  assert.ok(doc.includes('data-rede="copiar" data-url="https://velmodrinkmorango.com.br/clarize.html?utm_source=copiar&amp;'))
  for (const velho of ["wa.me/?text=", "facebook.com/sharer", 'data-rede="instagram"', "comp-whatsapp"])
    assert.ok(!doc.includes(velho), `ainda tem ${velho}`)
  assert.ok(doc.indexOf('class="compartilhar"') < doc.indexOf('id="footer-placeholder"'))
  assert.ok(!ler("mapa-do-site.html").includes('class="compartilhar"'))
  assert.equal(conta(ler("index.html"), 'class="compartilhar"'), 1)
})

test("rodar o rastreio.py de novo não muda nenhuma página", () => {
  const pasta = mkdtempSync(join(tmpdir(), "rastreio-"))
  for (const nome of PAGINAS) cpSync(join(RAIZ, nome), join(pasta, nome))
  execFileSync("python3", ["-I", join(RAIZ, "fonte/rastreio.py"), pasta])
  for (const nome of PAGINAS) assert.equal(ler(nome, pasta), ler(nome), nome)
})

function carregarJs() {
  const janela = {}
  vm.runInNewContext(ler("js/rastreio.js"), { window: janela, URL, URLSearchParams })
  return janela.VelmoRastreio
}

test("origem da visita: UTM do link, busca do Google, rede social, direto", () => {
  const { origemDaVisita } = carregarJs()
  const d = "velmodrinkmorango.com.br"
  assert.deepEqual({ ...origemDaVisita("?utm_source=whatsapp&utm_medium=social&utm_campaign=compartilhar", "", d) },
    { utm_source: "whatsapp", utm_medium: "social", utm_campaign: "compartilhar" })
  assert.deepEqual({ ...origemDaVisita("", "https://www.google.com.br/", d) }, { utm_source: "google", utm_medium: "organico" })
  assert.deepEqual({ ...origemDaVisita("", "https://l.instagram.com/", d) }, { utm_source: "instagram", utm_medium: "social" })
  assert.deepEqual({ ...origemDaVisita("", "https://m.facebook.com/", d) }, { utm_source: "facebook", utm_medium: "social" })
  assert.deepEqual({ ...origemDaVisita("", "https://velmodrinkmorango.com.br/loja.html", d) }, { utm_source: "(direto)", utm_medium: "(nenhum)" })
  assert.deepEqual({ ...origemDaVisita("", "", d) }, { utm_source: "(direto)", utm_medium: "(nenhum)" })
})

test("link do checkout ganha a origem e a página do clique, sem apagar UTM que já existia", () => {
  const { decorarCheckout, paginaDe } = carregarJs()
  const u = new URL(decorarCheckout("https://pay.hest.com.br/abc", { utm_source: "google", utm_medium: "organico" }, paginaDe("/clarize.html")))
  assert.equal(u.searchParams.get("utm_source"), "google")
  assert.equal(u.searchParams.get("utm_medium"), "organico")
  assert.equal(u.searchParams.get("utm_campaign"), "site")
  assert.equal(u.searchParams.get("utm_content"), "clarize")
  const v = new URL(decorarCheckout("https://pay.hest.com.br/abc?utm_source=x", { utm_source: "google", utm_medium: "organico" }, "inicio"))
  assert.equal(v.searchParams.get("utm_source"), "x")
  assert.equal(paginaDe("/"), "inicio")
})

test("páginas de emagrecimento: foto do produto, depois compartilhar, depois o selo e o H1", () => {
  const sp = PAGINAS.filter((n) => n.endsWith("-sao-paulo-sp.html"))
  assert.equal(sp.length, 27)
  for (const nome of sp) {
    const doc = ler(nome)
    const foto = doc.indexOf('class="hero-foto"')
    const topo = doc.indexOf('class="compartilhar compartilhar-topo"')
    const selo = doc.indexOf('class="hero-badge"')
    const h1 = doc.indexOf("<h1")
    assert.ok(foto > 0 && foto < topo && topo < selo && selo < h1, `${nome}: ordem foto > compartilhar > selo > h1`)
    assert.equal(conta(doc, 'class="compartilhar compartilhar-topo"'), 1, `${nome}: um compartilhar no topo`)
    assert.ok(doc.slice(topo, selo).includes("utm_content=" + nome.slice(0, -5) + '"'), `${nome}: UTM da página`)
  }
})

test("menu sanduíche: botão com aria no cabeçalho do main.js", () => {
  const js = ler("js/main.js")
  assert.match(js, /<button[^>]*class="menu-toggle"[^>]*aria-controls="site-nav"[^>]*aria-expanded="false"/)
  assert.match(js, /<nav id="site-nav"/)
  assert.match(ler("css/style.css"), /\.menu-toggle/)
})

test("páginas de emagrecimento: FAQ e seções de texto em fundo claro, sem texto dourado ou cinza-claro", () => {
  for (const nome of PAGINAS.filter((n) => n.endsWith("-sao-paulo-sp.html"))) {
    const doc = ler(nome)
    for (const escuro of ["background:#111", "background:#0d0d0d", "background:#1a1a1a", "color:#ccc", "color:#D4AF37", "solid #2a2a2a"])
      assert.ok(!doc.includes(escuro), `${nome}: ainda tem ${escuro}`)
  }
})

test("menu: link da Loja com coroa dourada no cabeçalho", () => {
  const js = ler("js/main.js")
  assert.match(js, /<nav id="site-nav">[\s\S]*<a href="loja\.html"[^>]*><svg class="icone-coroa"[^>]*aria-hidden="true"[\s\S]*?<\/svg>Loja<\/a>[\s\S]*<\/nav>/)
  assert.match(ler("css/style.css"), /\.icone-coroa\s*\{/)
})

test("cabeçalho sem o botão Saiba Mais ao lado do menu", () => {
  const js = ler("js/main.js")
  assert.ok(!js.includes("header-cta") && !js.includes("Saiba Mais"))
})

test("páginas de emagrecimento: sem promessas de resultado, depoimentos ou estados errados", () => {
  const proibidas = ["transformaram seu corpo", "O Velmo Drink acelera", "100%</strong><span>Natural", "Natural para Emagrecimento",
    "Minas Gerais", "Sergipe", "Tocantins", "Florianópolis", "relatam", "adia a transformação", "sem efeitos colaterais",
    "eficácia comprovada", "versão premium", "4 a 6 kg", "3 e 6 kg", "5 a 9 kg", "perfil de segurança", "O Velmo Drink resolve esse problema"]
  for (const nome of PAGINAS.filter((n) => n.endsWith("-sao-paulo-sp.html"))) {
    const doc = ler(nome)
    for (const f of proibidas) assert.ok(!doc.includes(f), `${nome}: ainda tem "${f}"`)
  }
})
