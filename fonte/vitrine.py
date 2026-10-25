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

# Parcela em 12x no cartão (só o produto, sem o frete), conferida no checkout da Hest em 24/10/2026.
# Preço sem parcela conferida mostra só "em até 12x no cartão".
PARCELA_12X = {137.90: 14.23, 291.90: 29.96, 370.30: 37.96, 321.30: 32.96, 441.00: 45.18, 146.30: 15.09}


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


def preco_grande(v):
    reais, cent = f"{v:,.2f}".replace(",", ".").rsplit(".", 1)
    return f'<span class="kit-rs">R$</span> {reais}<sup>{cent}</sup>'


def card(slug, nome, kit, preco, links, cheio=None, destaque=False):
    """links: [(texto do botão, uuid)]. cheio: preço "de" (só na oferta)."""
    n = meses(kit)
    um, varios = UNIDADE[slug]
    qtd = f"{n} {um if n == 1 else varios}"
    tag = '<span class="kit-tag">Menor preço por mês</span>' if destaque else ""
    de = f'<p class="kit-de"><s>{brl(cheio)}</s></p>' if cheio else ""
    off = f' <span class="kit-off">{round((1 - preco / cheio) * 100)}% OFF</span>' if cheio else ""
    parcela = (f"ou 12x de {brl(PARCELA_12X[round(preco, 2)])} no cartão" if round(preco, 2) in PARCELA_12X
               else "em até 12x no cartão, Pix ou boleto")
    por_mes = f'<p class="kit-mes">{brl(preco / n)} por mês{f" · {brl(preco / (30 * n))} por dia" if destaque else ""}</p>' if n > 1 else ""
    botoes = " ".join(botao(u, t) for t, u in links)
    return f"""        <div class="kit-card{' kit-destaque' if destaque else ''}">
          <div class="kit-foto">{foto(slug, n)}</div>
          <div class="kit-info">
            {tag}
            <p class="kit-nome">{html.escape(nome)} · Kit {kit.lower()} ({qtd})</p>
            {de}
            <p class="kit-preco" aria-label="{brl(preco)}{f" com {round((1 - preco / cheio) * 100)}% de desconto" if cheio else ""}">{preco_grande(preco)}{off}</p>
            <p class="kit-parcela">{parcela}</p>
            {por_mes}
            <p class="kit-frete">Frete {brl(FRETE)} · garantia de 30 dias</p>
            <div class="kit-botoes">{botoes}</div>
          </div>
        </div>"""


def grade(cards):
    return '      <div class="kit-grade">\n' + "\n".join(cards) + "\n      </div>"
