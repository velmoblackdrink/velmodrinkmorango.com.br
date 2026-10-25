// Testes da Black Friday (fonte/black_friday.py): a oferta só aparece entre INICIO e FIM, com os preços do checkout.
// Rodar com: node --test tests/
import { test } from "node:test"
import assert from "node:assert/strict"
import { execFileSync } from "node:child_process"
import { cpSync, mkdtempSync, readFileSync } from "node:fs"
import { tmpdir } from "node:os"
import { join } from "node:path"
import { fileURLToPath } from "node:url"

const RAIZ = fileURLToPath(new URL("..", import.meta.url))
const PAGINAS = ["creagym.html", "creatina-gummy.html", "creatina.html", "loja.html", "clarize.html"]

function gerarEm(hoje) {
  const pasta = mkdtempSync(join(tmpdir(), "bf-"))
  for (const nome of ["sitemap.xml", "mapa-do-site.html", "creatina.html"]) cpSync(join(RAIZ, nome), join(pasta, nome))
  const env = { ...process.env, HOJE: hoje }
  execFileSync("python3", ["-I", join(RAIZ, "fonte/gerar_loja.py"), pasta], { env })
  execFileSync("python3", ["-I", join(RAIZ, "fonte/gerar_blog.py"), pasta], { env })
  return pasta
}
const ler = (pasta, nome) => readFileSync(join(pasta, nome), "utf8")

test("fora do período nenhuma página mostra Black Friday nem link de desconto", () => {
  for (const hoje of ["2026-11-19", "2026-12-01"]) {
    const pasta = gerarEm(hoje)
    for (const nome of PAGINAS) {
      const doc = ler(pasta, nome)
      assert.ok(!doc.includes("bf-letreiro") && !doc.includes('id="black-friday"'), `${hoje} ${nome}`)
      for (const uuid of ["e395fad4", "14f32758", "f3bb752f"]) assert.ok(!doc.includes(uuid), `${hoje} ${nome}: ${uuid}`)
    }
  }
})

test("no primeiro e no último dia a oferta aparece com os preços conferidos no checkout", () => {
  for (const hoje of ["2026-11-20", "2026-11-30"]) {
    const pasta = gerarEm(hoje)
    const cg = ler(pasta, "creagym.html")
    assert.ok(cg.includes("bf-letreiro") && cg.includes('id="black-friday"'), hoje)
    for (const [preco, uuid] of [["R$ 137,90", "c6dc3e80"], ["R$ 291,90", "1094666f"], ["R$ 370,30", "e395fad4"], ["R$ 370,30", "95fc0bba"]]) {
      assert.ok(cg.includes(preco), `${hoje} CreaGym ${preco}`)
      assert.ok(cg.includes(`pay.hest.com.br/${uuid}`), `${hoje} CreaGym ${uuid}`)
    }
    const gm = ler(pasta, "creatina-gummy.html")
    for (const preco of ["R$ 137,90", "R$ 321,30", "R$ 441,00"]) assert.ok(gm.includes(preco), `${hoje} Gummy ${preco}`)
    assert.ok(gm.includes("pay.hest.com.br/f3bb752f"), "leve junto: Clarize com 30%")
    assert.ok(gm.includes("R$ 146,30"), "Clarize com 30%")
    // frete à parte e prazo real: nada de "frete grátis" ou "incluso"
    for (const doc of [cg, gm, ler(pasta, "creatina.html")]) {
      assert.match(doc, /frete de R\$ 29,90 à parte/)
      assert.ok(!/frete (grátis|incluso)/i.test(doc))
    }
    assert.ok(ler(pasta, "loja.html").includes('href="creatina.html#black-friday"'))
    assert.ok(!ler(pasta, "clarize.html").includes("bf-letreiro"), "página do Clarize fica com o preço normal")
  }
})

test("o post da Black Friday avisa antes, mostra a oferta durante e diz que acabou depois", () => {
  const antes = ler(gerarEm("2026-11-03"), "creatina-black-friday.html")
  assert.match(antes, /aparecem nesta página/)
  assert.ok(!antes.includes("e395fad4"))
  const durante = ler(gerarEm("2026-11-25"), "creatina-black-friday.html")
  assert.ok(durante.includes('id="black-friday"') && durante.includes("e395fad4"))
  const depois = ler(gerarEm("2026-12-02"), "creatina-black-friday.html")
  assert.match(depois, /terminou/)
  assert.ok(!depois.includes("e395fad4"))
})

test("CreaGym e Creatina Gummy mostram os kits em cards, com a foto dos potes junto do preço", () => {
  const pasta = gerarEm("2026-10-24")
  const cg = ler(pasta, "creagym.html")
  assert.equal(cg.split('class="kit-card').length - 1, 3, "3 kits do CreaGym")
  for (const img of ["creagym-creatina-morango-300g", "creagym-kit-3-potes", "creagym-kit-5-potes"]) assert.ok(cg.includes(img), img)
  assert.ok(!cg.includes('class="loja-kits"'), "sem a fileira de fotos separada")
  assert.ok(!cg.includes('<table class="precos">'), "sem a tabela antiga")
  assert.equal(cg.split(">Menor preço por mês<").length - 1, 1, "um selo de menor preço por mês")
  const gm = ler(pasta, "creatina-gummy.html")
  assert.equal(gm.split('class="kit-card').length - 1, 3, "3 kits da Gummy")
  assert.ok(gm.includes("kit-pilha-3") && gm.includes("kit-pilha-5"), "frascos empilhados nos kits")
  assert.ok(ler(pasta, "clarize.html").includes('<table class="precos">'), "Clarize continua com a tabela")
  for (const doc of [cg, gm]) assert.ok(!doc.includes("OFF"), "sem desconto fora da Black Friday")
})

test("durante a oferta a vitrine mostra de/por com 30% OFF e o letreiro fica no topo", () => {
  const cg = ler(gerarEm("2026-11-20"), "creagym.html")
  assert.ok(cg.indexOf("bf-letreiro") < cg.indexOf('class="hero-badge"'), "letreiro antes do selo do topo")
  assert.match(cg, /<s>R\$ 529,00<\/s>/)
  assert.match(cg, /30% OFF/)
  assert.match(cg, /aria-label="12x de R\$ 37,96 no cartão">12x /, "parcela em destaque")
  assert.match(cg, /ou R\$ 370,30 à vista no Pix ou boleto · total no cartão R\$ 455,52/, "à vista e total no cartão")
  assert.equal(cg.split("pay.hest.com.br/f3bb752f").length - 1, 1, "Clarize com 30% numa seção só, abaixo dos cards")
  assert.match(cg, /Preço normal: <s>R\$ 209,00<\/s> <span class="kit-off">30% OFF/)
  assert.ok(!cg.includes("pay.hest.com.br/8a088d7a"), "na oferta, o Clarize aparece só com desconto")
})

test("o pó e a goma sugerem o Clarize abaixo dos cards, com foto e preço normal fora da oferta", () => {
  const pasta = gerarEm("2026-10-24")
  for (const nome of ["creagym.html", "creatina-gummy.html"]) {
    const doc = ler(pasta, nome)
    assert.equal(doc.split('class="sugestao"').length - 1, 1, `${nome}: uma seção do Clarize`)
    assert.ok(doc.indexOf('class="sugestao"') > doc.lastIndexOf('class="kit-card'), `${nome}: abaixo dos cards`)
    assert.ok(doc.includes("img/clarize-clareador-intimo-60ml.webp"), `${nome}: foto do Clarize`)
    assert.ok(doc.includes("pay.hest.com.br/8a088d7a"), `${nome}: Clarize a preço cheio fora da oferta`)
    assert.match(doc, /aria-label="12x de R\$ 21,49 no cartão"/, `${nome}: parcela do Clarize`)
    assert.ok(!doc.includes("f3bb752f") && !doc.includes("kit-bump"), `${nome}: sem desconto e sem caixa de marcar`)
    assert.match(doc, /aria-label="12x de R\$ 20,27 no cartão"/, `${nome}: parcela do kit de 1 mês`)
  }
  const gm = ler(pasta, "creatina-gummy.html")
  assert.match(gm, /<title>Creatina Gummy: creatina em goma, preços e onde comprar/)
  assert.ok(gm.includes("Creatina goma funciona?"))
})
