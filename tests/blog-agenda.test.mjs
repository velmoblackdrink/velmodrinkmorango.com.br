// Testes da fila do blog (fonte/gerar_blog.py): post com data futura não pode ir ao ar antes do dia.
// Rodar com: node --test tests/
import { test } from "node:test"
import assert from "node:assert/strict"
import { execFileSync } from "node:child_process"
import { cpSync, existsSync, mkdtempSync, readFileSync, readdirSync } from "node:fs"
import { tmpdir } from "node:os"
import { join } from "node:path"
import { fileURLToPath } from "node:url"

const RAIZ = fileURLToPath(new URL("..", import.meta.url))

function gerarEm(hoje) {
  const pasta = mkdtempSync(join(tmpdir(), "blog-"))
  for (const nome of ["sitemap.xml", "mapa-do-site.html", "creatina.html"]) cpSync(join(RAIZ, nome), join(pasta, nome))
  execFileSync("python3", ["-I", join(RAIZ, "fonte/gerar_blog.py"), pasta], { env: { ...process.env, HOJE: hoje } })
  return pasta
}

const ler = (pasta, nome) => readFileSync(join(pasta, nome), "utf8")

test("post com data futura fica fora do site, do sitemap e do mapa", () => {
  const pasta = gerarEm("2026-10-19")
  assert.ok(!existsSync(join(pasta, "para-que-serve-a-creatina.html")))
  for (const nome of ["blog.html", "sitemap.xml", "mapa-do-site.html", "creatina.html", "como-tomar-creatina.html"])
    assert.ok(!ler(pasta, nome).includes("para-que-serve-a-creatina"), nome)
})

test("no dia marcado o post entra no site, no sitemap, no mapa e na lista de guias", () => {
  const pasta = gerarEm("2026-10-20")
  assert.ok(existsSync(join(pasta, "para-que-serve-a-creatina.html")))
  for (const nome of ["blog.html", "sitemap.xml", "mapa-do-site.html", "creatina.html"])
    assert.ok(ler(pasta, nome).includes("para-que-serve-a-creatina.html"), nome)
  assert.match(ler(pasta, "sitemap.xml"), /blog\.html<\/loc>\s*<lastmod>2026-10-20</)
})

test("nenhum post publicado aponta para um post que ainda está na fila", () => {
  for (const hoje of ["2026-10-20", "2026-10-23", "2026-10-25", "2026-10-27", "2026-10-30", "2026-11-03", "2026-11-06", "2026-11-10", "2026-11-13", "2026-11-17", "2026-11-20", "2026-11-24", "2026-11-27", "2026-12-01", "2026-12-04", "2026-12-08", "2026-12-11"]) {
    const pasta = gerarEm(hoje)
    for (const arq of readdirSync(pasta).filter((n) => n.endsWith(".html"))) {
      for (const [, alvo] of ler(pasta, arq).matchAll(/href="([a-z0-9-]+\.html)"/g)) {
        assert.ok(existsSync(join(pasta, alvo)) || existsSync(join(RAIZ, alvo)), `${hoje} ${arq} -> ${alvo}`)
      }
    }
  }
})

test("rodar duas vezes no mesmo dia não muda nada (o robô só faz commit quando há post novo)", () => {
  const pasta = gerarEm("2026-10-23")
  const antes = ler(pasta, "sitemap.xml") + ler(pasta, "creatina.html") + ler(pasta, "mapa-do-site.html")
  execFileSync("python3", ["-I", join(RAIZ, "fonte/gerar_blog.py"), pasta], { env: { ...process.env, HOJE: "2026-10-23" } })
  assert.equal(ler(pasta, "sitemap.xml") + ler(pasta, "creatina.html") + ler(pasta, "mapa-do-site.html"), antes)
})

test("posts de emagrecimento: título curto, descrição, FAQ e sem promessa de resultado", () => {
  const pasta = gerarEm("2026-12-11")
  for (const slug of ["suplemento-para-emagrecer-funciona", "efeitos-colaterais-de-suplemento-para-emagrecer", "como-saber-se-suplemento-e-confiavel", "cha-ou-capsula-para-emagrecer"]) {
    const doc = ler(pasta, slug + ".html")
    const titulo = doc.match(/<title>([^<]+)<\/title>/)[1]
    assert.ok(titulo.length <= 75, `${slug}: título com ${titulo.length} caracteres`)
    const desc = doc.match(/<meta name="description" content="([^"]+)"/)[1]
    assert.ok(desc.length >= 120 && desc.length <= 170, `${slug}: descrição com ${desc.length}`)
    assert.ok(doc.includes('"@type": "FAQPage"') || doc.includes('"@type":"FAQPage"'), `${slug}: FAQPage`)
    assert.ok(doc.includes('href="index.html"'), `${slug}: CTA do Velmo Drink`)
    for (const f of ["secaps", "Secaps", "garantido</", "kg em 30 dias", "queima gordura localizada"]) assert.ok(!doc.includes(f), `${slug}: ${f}`)
  }
  assert.ok(!existsSync(join(gerarEm("2026-11-26"), "suplemento-para-emagrecer-funciona.html")))
})

test("todo post tem um CTA no meio da leitura, para uma página de produto que existe, além do CTA final", () => {
  const pasta = gerarEm("2027-12-31")
  const posts = readdirSync(pasta).filter((n) => n.endsWith(".html") && ler(pasta, n).includes('"@type": "BlogPosting"') && n !== "blog.html")
  assert.ok(posts.length >= 21, `só ${posts.length} posts`)
  for (const nome of posts) {
    const doc = ler(pasta, nome)
    const partes = doc.split('class="blog-cta-meio"')
    assert.equal(partes.length - 1, 1, `${nome}: um CTA no meio`)
    const pos = partes[0].length
    const h2s = [...doc.matchAll(/<h2>/g)].map((m) => m.index)
    assert.ok(h2s.length >= 3 && pos > h2s[0] && pos < h2s[h2s.length - 1], `${nome}: CTA entre a primeira e a última seção`)
    const href = partes[1].match(/href="([a-z0-9-]+\.html)(#[a-z-]+)?"/)[1]
    assert.ok(existsSync(join(RAIZ, href)), `${nome}: ${href} existe`)
    assert.ok(partes[1].slice(0, 600).includes('class="cta-meio-btn"'), `${nome}: link rastreável`)
  }
})

test("todo post publicado termina com a caixa grande de CTA antes do aviso", () => {
  const pasta = gerarEm("2027-12-31")
  for (const nome of readdirSync(pasta).filter((n) => n !== "blog.html" && n.endsWith(".html") && ler(pasta, n).includes('"@type": "BlogPosting"'))) {
    const doc = ler(pasta, nome)
    assert.equal(doc.split('<div class="blog-cta">').length - 1, 1, `${nome}: caixa final`)
    assert.ok(doc.indexOf('<div class="blog-cta">') < doc.indexOf('class="loja-aviso"'), `${nome}: CTA antes do aviso`)
  }
})
