"""Cards de kit no formato de loja (foto dos potes junto com o preço, como no Mercado Livre).

Usado por gerar_loja.py (seção de preços do CreaGym e da Creatina Gummy) e por black_friday.py
(as mesmas vitrines com "de/por" durante a oferta).
"""
import html

H = "https://pay.hest.com.br/"
FRETE = 29.90

# Foto de cada kit: (arquivo, largura, altura, alt). Sem foto do kit, a foto de 1 unidade é empilhada n vezes.
FOTOS = {
    "creagym": {
        1: ("img/creagym-creatina-morango-300g.webp", 544, 600, "1 pote de CreaGym sabor Morango, 300 g"),
        3: ("img/creagym-kit-3-potes.webp", 600, 384, "Kit com 3 potes de CreaGym sabor Morango"),
        5: ("img/creagym-kit-5-potes.webp", 600, 340, "Kit com 5 potes de CreaGym sabor Morango"),
    },
    "creatina-gummy": {
        "unidade": ("img/creatina-gummy-tutti-frutti-60-gomas.webp", 331, 600, "Frasco de Creatina Gummy com 60 gomas"),
    },
}
UNIDADE = {"creagym": ("pote", "potes"), "creatina-gummy": ("frasco", "frascos")}

# Parcela em 12x no cartão (só o produto, sem o frete), como o checkout da Hest mostra.
# CONFERIDAS no checkout em 24/10/2026: 137,90 / 146,30 / 209,00 / 291,90 / 321,30 / 370,30 / 441,00.
# CALCULADAS pela mesma regra da Hest (parcela = 0,10211 x preço + 0,15, que bate com as 7 conferidas
# com menos de meio centavo de diferença): 197,00 / 417,00 / 459,00 / 529,00 / 630,00. Confira no checkout.
PARCELA_12X = {137.90: 14.23, 146.30: 15.09, 209.00: 21.49, 291.90: 29.96, 321.30: 32.96, 370.30: 37.96, 441.00: 45.18,
               197.00: 20.27, 417.00: 42.73, 459.00: 47.02, 529.00: 54.17, 630.00: 64.48}

# Clarize 1 mês, sugerido numa seção própria abaixo dos cards (a Hest tem um checkout por produto,
# então ele é uma compra separada). Preço com desconto só em campanha (black_friday.py).
CLARIZE = ("Clarize 1 mês", 209.00, "8a088d7a-b2b5-46fa-a132-a818b7653a05")
CLARIZE_FOTO = ("img/clarize-clareador-intimo-60ml.webp", 221, 600, "Frasco do Clarize, clareador íntimo da Velmora, 60 ml")


def brl(v):
    s = f"{v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return "R$ " + s


def meses(kit):
    return int(kit.split()[0])


def botao(uuid, texto):
    return f'<a class="btn btn-primary" href="{H}{uuid}" target="_blank" rel="sponsored noopener">{html.escape(texto)}</a>'


def foto(slug, n):
    fotos = FOTOS[slug]
    if n in fotos:
        a, w, h, alt = fotos[n]
        return f'<img src="{a}" width="{w}" height="{h}" alt="{html.escape(alt)}" loading="lazy">'
    a, w, h, alt = fotos["unidade"]
    um, varios = UNIDADE[slug]
    imgs = "".join(f'<img src="{a}" width="{w}" height="{h}" alt="" loading="lazy">' for _ in range(n))
    rotulo = alt if n == 1 else f"Kit com {n} {varios} de Creatina Gummy"
    return f'<div class="kit-pilha kit-pilha-{n}" role="img" aria-label="{html.escape(rotulo)}">{imgs}</div>'


def valor_grande(v):
    reais, cent = f"{v:,.2f}".replace(",", ".").rsplit(".", 1)
    return f'<span class="kit-rs">R$</span> {reais}<sup>{cent}</sup>'


def parcela(preco):
    return PARCELA_12X.get(round(preco, 2))


def card(slug, nome, kit, preco, links, cheio=None, destaque=False):
    """links: [(texto do botão, uuid)]. cheio: preço "de" (só na oferta)."""
    n = meses(kit)
    um, varios = UNIDADE[slug]
    qtd = f"{n} {um if n == 1 else varios}"
    pct = round((1 - preco / cheio) * 100) if cheio else 0
    tag = '<span class="kit-tag">Menor preço por mês</span>' if destaque else ""
    de = f'<p class="kit-de"><s>{brl(cheio)}</s> <span class="kit-off">{pct}% OFF</span></p>' if cheio else ""
    p12 = parcela(preco)
    if p12:
        grande = f'<p class="kit-preco" aria-label="12x de {brl(p12)} no cartão">12x {valor_grande(p12)}</p>'
        avista = (f'<p class="kit-avista">ou {brl(preco)} à vista no Pix ou boleto'
                  f' · total no cartão {brl(p12 * 12)}</p>')
    else:
        grande = f'<p class="kit-preco" aria-label="{brl(preco)}">{valor_grande(preco)}</p>'
        avista = '<p class="kit-avista">em até 12x no cartão, Pix ou boleto</p>'
    por_mes = f'<p class="kit-mes">{brl(preco / n)} por mês{f" · {brl(preco / (30 * n))} por dia" if destaque else ""}</p>' if n > 1 else ""
    botoes = " ".join(botao(u, t) for t, u in links)
    return f"""        <div class="kit-card{' kit-destaque' if destaque else ''}">
          <div class="kit-foto">{foto(slug, n)}</div>
          <div class="kit-info">
            {tag}
            <p class="kit-nome">{html.escape(nome)} · Kit {kit.lower()} ({qtd})</p>
            {de}
            {grande}
            {avista}
            {por_mes}
            <p class="kit-frete">Frete {brl(FRETE)} · garantia de 30 dias</p>
            <div class="kit-botoes">{botoes}</div>
          </div>
        </div>"""


def sugestao_clarize(preco=None, uuid=None, cheio=None):
    """Seção "leve também o Clarize" abaixo dos cards. Sem argumentos: preço normal.
    Na campanha: preco com desconto, uuid do link de desconto e cheio = preço normal."""
    nome, normal, link_normal = CLARIZE
    preco, uuid = (preco or normal), (uuid or link_normal)
    a, w, h, alt = CLARIZE_FOTO
    p12 = parcela(preco)
    if cheio:
        pct = round((1 - preco / cheio) * 100)
        precos = (f'<p class="kit-de">Preço normal: <s>{brl(cheio)}</s> <span class="kit-off">{pct}% OFF</span></p>'
                  f'<p class="kit-preco" aria-label="12x de {brl(p12)} no cartão">12x {valor_grande(p12)}</p>'
                  f'<p class="kit-avista">ou {brl(preco)} à vista no Pix ou boleto · total no cartão {brl(p12 * 12)}</p>')
        botao_txt = f"Comprar o Clarize com {pct}% OFF"
    else:
        precos = (f'<p class="kit-preco" aria-label="12x de {brl(p12)} no cartão">12x {valor_grande(p12)}</p>'
                  f'<p class="kit-avista">ou {brl(preco)} à vista no Pix ou boleto · total no cartão {brl(p12 * 12)}</p>')
        botao_txt = "Comprar o Clarize"
    return f"""      <div class="sugestao">
        <div class="sugestao-foto"><img src="{a}" width="{w}" height="{h}" alt="{html.escape(alt)}" loading="lazy"></div>
        <div class="sugestao-info">
          <span class="kit-tag">Sugestão para você</span>
          <h3>Leve também o Clarize</h3>
          <p class="sugestao-desc">Clareador íntimo com niacinamida para virilha, axilas e joelhos. Frasco de 60 ml, para 1 mês de uso.</p>
          {precos}
          <p class="kit-frete">É uma compra separada da creatina, com frete próprio de {brl(FRETE)} · garantia de 30 dias</p>
          <div class="kit-botoes">{botao(uuid, botao_txt)} <a class="btn btn-outline" href="clarize.html">Saiba mais</a></div>
        </div>
      </div>"""


def grade(cards):
    return '      <div class="kit-grade">\n' + "\n".join(cards) + "\n      </div>"
