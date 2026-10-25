"""Black Friday da Velmora: 30% OFF nos kits do CreaGym e da Creatina Gummy, com o Clarize de 1 mês
com 30% sugerido abaixo dos cards (compra separada).

A oferta entra e sai sozinha pela data (INICIO a FIM, horário de Brasília): gerar_loja.py e gerar_blog.py
chamam este módulo, e a ação diária (.github/workflows/publicar-blog.yml) regera o site às 07:00.
Fora do período, nenhuma página mostra desconto (regra: preço com desconto só em campanha).

Preços conferidos no checkout da Hest em 24/10/2026: 30% sobre o preço do produto, frete de R$ 29,90 à parte.
O "de" é o preço cheio que o site mostra o ano todo (regra do Procon: preço anterior real).
Para a Black Friday do ano que vem: troque INICIO, FIM, ANO e confira os links e preços no checkout.
"""
import html

import vitrine as V

INICIO = "2026-10-26"  # antecipada a pedido em 25/10/2026 (era 20/11)
FIM = "2026-11-30"
# De INICIO até a véspera de DIA_BLACK a oferta se chama "Esquenta Black Friday"; de DIA_BLACK a FIM, "Black Friday".
DIA_BLACK = "2026-11-20"
ANO = "2026"
PERIODO = "de 26 de outubro a 30 de novembro"
FIM_TEXTO = "30/11 às 23h59"
DESCONTO = 0.30
FRETE = 29.90
H = "https://pay.hest.com.br/"

# kit, preço cheio, link 30% (Morango ou único), link 30% Tangerina
OFERTAS = {
    "creagym": ("CreaGym", [
        ("1 Mês", 197.00, "c6dc3e80-b0de-4748-8143-06ec913f627c", "94c55e0f-8c16-11f1-b7d4-0affdf3a7b6b"),
        ("3 Meses", 417.00, "1094666f-dcc9-4548-b3f1-4794838fd456", "9561173f-8c16-11f1-b7d4-0affdf3a7b6b"),
        ("5 Meses", 529.00, "e395fad4-94d9-4730-9486-d1e623a52d16", "95fc0bba-8c16-11f1-b7d4-0affdf3a7b6b"),
    ]),
    "creatina-gummy": ("Creatina Gummy", [
        ("1 Mês", 197.00, "a5626e35-a2ec-40a6-87c6-760ec0a241e9", None),
        ("3 Meses", 459.00, "33f2d6a2-5582-4411-9f2c-7f7289070e2e", None),
        ("5 Meses", 630.00, "14f32758-32f0-4838-a1d0-55a601d75f36", None),
    ]),
}
CLARIZE = ("Clarize 1 Mês", 209.00, "f3bb752f-57a0-403b-9c80-981393e29fc0")


def ativa(hoje):
    return INICIO <= hoje <= FIM


def nome_campanha(hoje):
    """Nome da campanha no dia: 'Esquenta Black Friday Velmora' antes de DIA_BLACK, depois 'Black Friday Velmora'."""
    return "Esquenta Black Friday Velmora" if hoje < DIA_BLACK else "Black Friday Velmora"


def brl(v):
    s = f"{v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return "R$ " + s


def por(v):
    return round(v * (1 - DESCONTO), 2)


def meses(kit):
    return int(kit.split()[0])


def botao(uuid, texto):
    return f'<a class="btn btn-primary" href="{H}{uuid}" target="_blank" rel="sponsored noopener">{html.escape(texto)}</a>'


def faixa(hoje, alvo="#black-friday"):
    """Letreiro que passa na largura toda do topo da página (formato slide), só durante a oferta.
    O texto aparece duas vezes seguidas para o movimento não ter emenda; quem pede menos movimento
    no aparelho vê o letreiro parado (css/loja.css)."""
    if not ativa(hoje):
        return ""
    frase = (f'<span><strong>{nome_campanha(hoje).upper()}</strong> · 30% OFF nos kits de creatina até {FIM_TEXTO} · '
             f'Ver ofertas &rarr;</span>')
    return (f'<a class="bf-letreiro" href="{alvo}" aria-label="{nome_campanha(hoje)}: 30% OFF nos kits de creatina até '
            f'{FIM_TEXTO}. Ver ofertas"><div class="bf-trilho" aria-hidden="true">{frase * 4}{frase * 4}</div></a>\n    ')


def _cards(slug):
    nome, kits = OFERTAS[slug]
    menor = min(kits, key=lambda k: por(k[1]) / meses(k[0]))
    out = []
    for kit, cheio, uuid, tang in kits:
        links = [("Quero Morango", uuid), ("Quero Tangerina", tang)] if tang else [("Quero agora com 30%", uuid)]
        out.append(V.card(slug, nome, kit, por(cheio), links, cheio=cheio, destaque=kit == menor[0]))
    return V.grade(out)


def regras():
    return (f'<p class="bf-regras">Oferta válida {PERIODO} de {ANO}, até {FIM_TEXTO}, ou enquanto a Velmora mantiver os preços '
            f'no checkout da Hest. 30% de desconto sobre o preço do produto; frete de {brl(FRETE)} à parte. '
            f'Pagamento no cartão em até 12x, Pix ou boleto. Este site é de um afiliado: a compra, a entrega e a garantia '
            f'de 30 dias são da Velmora, pela Hest.</p>')


def bloco_produto(slug, hoje):
    """Seção da oferta na página do produto (creagym, creatina-gummy). Vazia fora do período."""
    if not ativa(hoje) or slug not in OFERTAS:
        return ""
    nome = OFERTAS[slug][0]
    return f"""<!-- black-friday:inicio -->
  <section class="bf" id="black-friday">
    <div class="container">
      <p class="bf-selo">{nome_campanha(hoje)} · até {FIM_TEXTO}</p>
      <h2>30% OFF nos kits do {nome}</h2>
      <p class="bf-sub">O desconto já vem no link: é só escolher o kit e pagar no checkout da Hest.</p>
{_cards(slug)}
{V.sugestao_clarize(por(CLARIZE[1]), CLARIZE[2], CLARIZE[1])}
      {regras()}
    </div>
  </section>
  <!-- black-friday:fim -->
"""


def bloco_comparacao(hoje):
    """Seção da oferta em creatina.html e no post da Black Friday: os dois produtos lado a lado."""
    if not ativa(hoje):
        return ""
    partes = []
    for slug in OFERTAS:
        nome = OFERTAS[slug][0]
        partes.append(f"""      <h3 class="bf-produto">{nome} <a href="{slug}.html">ver detalhes</a></h3>
{_cards(slug)}""")
    return f"""<!-- black-friday:inicio -->
  <section class="bf" id="black-friday">
    <div class="container">
      <p class="bf-selo">{nome_campanha(hoje)} · até {FIM_TEXTO}</p>
      <h2>30% OFF na creatina: em pó ou em goma</h2>
      <p class="bf-sub">O desconto já vem no link: é só escolher o kit e pagar no checkout da Hest.</p>
{chr(10).join(partes)}
{V.sugestao_clarize(por(CLARIZE[1]), CLARIZE[2], CLARIZE[1])}
      {regras()}
    </div>
  </section>
  <!-- black-friday:fim -->
"""


def aviso_post(hoje):
    """Parágrafo do post 'creatina-black-friday' antes e depois da oferta."""
    if ativa(hoje):
        return ""
    if hoje < INICIO:
        return (f'<div class="bf-aviso"><p><strong>Black Friday Velmora {ANO}:</strong> {PERIODO}, '
                f'com 30% OFF nos kits do CreaGym e da Creatina Gummy. Os preços com desconto aparecem nesta página '
                f'quando a oferta começar. Até lá, veja os <a href="creatina.html">preços atuais e a comparação</a>.</p></div>')
    return (f'<div class="bf-aviso"><p>A oferta de Black Friday de {ANO} terminou. Veja os '
            f'<a href="creatina.html">preços atuais do CreaGym e da Creatina Gummy</a>.</p></div>')
