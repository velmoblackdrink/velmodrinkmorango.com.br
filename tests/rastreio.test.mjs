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

test("toda página tem GTM, GA4 e noscript do GTM uma vez só", () => {
  for (const nome of PAGINAS) {
    const doc = ler(nome)
    assert.equal(conta(doc, "gtm.js?id="), 1, `${nome}: GTM`)
    assert.equal(conta(doc, "gtag/js?id=G-Z921CFD04J"), 1, `${nome}: GA4`)
    assert.equal(conta(doc, "gtag('config'"), 1, `${nome}: config do GA4`)
    assert.equal(conta(doc, "ns.html?id=GTM-5RQXHCPW"), 1, `${nome}: noscript`)
    assert.ok(doc.indexOf("ns.html?id=") > doc.indexOf("<body"), `${nome}: noscript dentro do body`)
    assert.equal(conta(doc, 'src="js/rastreio.js"'), 1, `${nome}: rastreio.js`)
  }
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

test("botões de compartilhar levam UTM e não aparecem no mapa do site", () => {
  const doc = ler("clarize.html")
  assert.equal(conta(doc, 'class="compartilhar"'), 1)
  assert.ok(doc.includes("https://wa.me/?text=") && doc.includes("utm_source%3Dwhatsapp%26utm_medium%3Dsocial%26utm_campaign%3Dcompartilhar%26utm_content%3Dclarize"))
  assert.ok(doc.includes("facebook.com/sharer/sharer.php?u=https%3A%2F%2Fvelmodrinkmorango.com.br%2Fclarize.html%3Futm_source%3Dfacebook"))
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
    assert.ok(doc.slice(topo, selo).includes("utm_content%3D" + nome.slice(0, -5)), `${nome}: UTM da página`)
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
