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
  for (const hoje of ["2026-10-20", "2026-10-23", "2026-10-27", "2026-10-30", "2026-11-03", "2026-11-06", "2026-11-10", "2026-11-13", "2026-11-17", "2026-11-20", "2026-11-24"]) {
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
