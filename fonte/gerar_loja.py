import json, sys, os, html, subprocess, datetime, zoneinfo

sys.dont_write_bytecode = True  # sem __pycache__ dentro do repo
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import black_friday as BF
import vitrine as V

SITE = "https://velmodrinkmorango.com.br"
OUT = sys.argv[1]
# Data de hoje em Brasília (ou HOJE=AAAA-MM-DD para simular): liga e desliga a Black Friday.
HOJE = os.environ.get("HOJE") or datetime.datetime.now(zoneinfo.ZoneInfo("America/Sao_Paulo")).date().isoformat()
H = "https://pay.hest.com.br/"

def brl(v):
    s = f"{v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return "R$ " + s

def link(uuid, texto="Quero este kit"):
    return f'<a class="btn btn-primary" href="{H}{uuid}" target="_blank" rel="sponsored noopener">{texto}</a>'

AFILIADO = ("Este site é de um afiliado. A compra, a entrega e a garantia de 30 dias são da Velmora, pela Hest. "
            "Frete e prazo aparecem no checkout.")

PRODUTOS = {
  "clarize": {
    "img": ("img/clarize-clareador-intimo-60ml.webp", 221, 600, "Frasco do Clarize, clareador íntimo da Velmora, 60 ml"),
    "nome": "Clarize",
    "badge": "Clareador para virilha, axilas e joelhos",
    "title": "Clarize: clareador para virilha e axila, como usar e preços | Velmo Drink",
    "desc": "Clarize, clareador íntimo da Velmora para virilha, axilas e joelhos, com niacinamida e ácido hialurônico. Composição, modo de uso, prazo e preços de 1, 3 e 5 meses.",
    "h1": "Clarize: clareador para virilha, axilas e joelhos",
    "lead": "Cosmético de uso externo com niacinamida, ácido hialurônico, lithothamnium e óleo de girassol ozonizado, em frasco de 60 ml com válvula pump. Veja como usar, em quanto tempo aparecem os primeiros resultados e os preços de 1, 3 e 5 meses.",
    "linhas": [("1 Mês", 209.00, "8a088d7a-b2b5-46fa-a132-a818b7653a05"),
               ("3 Meses", 335.00, "7722b37f-57d7-4e26-a360-9d0e639d2930"),
               ("5 Meses", 461.00, "0db242fc-2d3e-449a-8d5a-08751fec8b5b")],
    "sobre": [
      "O Clarize é o clareador íntimo da Velmora: um cosmético de uso externo para uniformizar o tom da pele em áreas que costumam escurecer, como a virilha, as axilas e os joelhos. Vem em frasco de 60 ml com válvula pump. O rótulo destaca quatro ingredientes:",
    ],
    "itens": [
      "<strong>Niacinamida</strong>: forma da vitamina B3, o ingrediente mais estudado da fórmula para manchas. Ela atua na transferência de pigmento para a superfície da pele, e é usada em cosméticos de uniformidade do tom.",
      "<strong>Ácido hialurônico</strong>: ingrediente de hidratação, que ajuda a reter água na superfície da pele.",
      "<strong>Lithothamnium</strong>: alga marinha rica em minerais, usada em cosméticos de cuidado da pele.",
      "<strong>Óleo de girassol ozonizado</strong>: óleo vegetal usado em cosméticos de cuidado e conforto da pele.",
    ],
    "depois": [
      "O site do fabricante também cita óleo de rosa mosqueta e informa que o produto é vegano, livre de parabenos, dermatologicamente testado e sem ácidos agressivos. A lista completa de ingredientes está no rótulo.",
    ],
    "secoes": [
      ("Como usar o Clarize", [
        "O modo de uso informado pelo fabricante tem quatro passos:",
        "<ol><li><strong>Higienize</strong> a área com água e sabonete neutro.</li>"
        "<li><strong>Seque</strong> completamente.</li>"
        "<li><strong>Aplique</strong> uma pequena quantidade do produto.</li>"
        "<li><strong>Massageie</strong> até a pele absorver.</li></ol>",
        "Use só por fora, na pele da virilha, das axilas ou dos joelhos. Não aplique em mucosas (a parte interna da região íntima) nem logo depois de depilar, quando a pele está sensível.",
      ]),
      ("Em quanto tempo aparecem os resultados", [
        "Segundo o fabricante, os primeiros resultados aparecem entre 2 e 4 semanas de uso contínuo, e o recomendado é usar por 30 a 60 dias seguidos. Por isso existem os kits de 3 e 5 meses. Clarear a pele é um processo lento em qualquer produto, e o resultado varia de pessoa para pessoa.",
        "Se o atrito continuar (roupa apertada, lâmina, suor parado na dobra), a pele tende a escurecer de novo. Vale cuidar da causa junto com o produto.",
      ]),
      ("Por que a virilha e as axilas escurecem", [
        "As causas mais comuns são o atrito da pele com a roupa ou entre as coxas, a depilação com lâmina ou cera, que irrita a pele, o suor e o calor nas dobras, e mudanças hormonais, como na gravidez. A pele irritada produz mais melanina e escurece aos poucos.",
        "Nem toda mancha é só estética. Pele escura, grossa e com aspecto de veludo no pescoço, nas axilas ou na virilha pode ser <strong>acantose nigricans</strong>, que costuma estar ligada à resistência à insulina. Nesse caso, procure um médico: nenhum cosmético resolve a causa.",
      ]),
      ("Prazo de entrega", [
        "Segundo o fabricante, a entrega leva de 5 a 15 dias úteis depois da postagem, com código de rastreio. O prazo exato para o seu CEP aparece no checkout.",
      ]),
    ],
    "aviso": "Cosméticos não tratam doenças. Uso externo: não aplique em mucosas, sobre pele ferida ou irritada. Antes do primeiro uso, faça um teste em uma pequena área e suspenda se houver ardência ou vermelhidão. Manchas que aparecem de repente, com coceira ou mudança de textura, merecem avaliação de dermatologista ou ginecologista. Siga o modo de uso do rótulo.",
    "faq": [
      ("Onde posso usar o Clarize?", "Na pele da virilha, das axilas e dos joelhos, que são as áreas indicadas pelo fabricante. O uso é externo: não aplique em mucosas."),
      ("Como usar o Clarize?", "Lave a área com água e sabonete neutro, seque bem, aplique uma pequena quantidade e massageie até absorver, como indica o fabricante."),
      ("Em quanto tempo o Clarize faz efeito?", "Segundo o fabricante, os primeiros resultados aparecem entre 2 e 4 semanas de uso contínuo, e o recomendado é usar por 30 a 60 dias seguidos. O resultado varia de pessoa para pessoa."),
      ("O que vem no Clarize?", "O rótulo destaca niacinamida, ácido hialurônico, lithothamnium e óleo de girassol ozonizado. O fabricante também cita óleo de rosa mosqueta. A lista completa está no rótulo."),
      ("Quando procurar um médico em vez de usar clareador?", "Se a pele escureceu de repente, coça, dói ou ficou grossa e aveludada (como no pescoço e nas axilas), procure um médico. Pode ser acantose nigricans, ligada à resistência à insulina, ou outra condição que precisa de tratamento."),
      ("Qual a diferença entre os kits de 1, 3 e 5 meses?", "É a quantidade de produto. O preço por mês cai nos kits maiores: 1 mês sai por R$ 209,00, 3 meses por R$ 335,00 e 5 meses por R$ 461,00."),
      ("Tem garantia?", "Sim. A Velmora oferece garantia de 30 dias, pela Hest, a plataforma onde o pagamento é feito."),
      ("Quais as formas de pagamento?", "Cartão de crédito em até 12x, Pix e boleto, no checkout da Hest."),
    ],
  },
  "creagym": {
    "img": ("img/creagym-morango-e-tangerina-300g.webp", 760, 405, "Potes de CreaGym sabor Morango e sabor Tangerina, creatina monohidratada da Velmora, 300 g"),
    "kits": [("img/creagym-creatina-morango-300g.webp", 544, 600, "1 pote de CreaGym", "1 Mês: 1 pote"),
             ("img/creagym-kit-3-potes.webp", 600, 384, "Kit com 3 potes de CreaGym", "3 Meses: 3 potes"),
             ("img/creagym-kit-5-potes.webp", 600, 340, "Kit com 5 potes de CreaGym", "5 Meses: 5 potes")],
    "kits_nota": "Fotos do sabor Morango. Nos kits de Tangerina, os potes são de Tangerina.",
    "nome": "CreaGym",
    "badge": "Creatina + magnésio + coenzima Q10",
    "title": "CreaGym Morango e Tangerina: preços e onde comprar | Velmo Drink",
    "desc": "CreaGym, suplemento com creatina monohidratada, magnésio bisglicinato e coenzima Q10, nos sabores Morango e Tangerina. Preços de 1, 3 e 5 meses.",
    "h1": "CreaGym",
    "lead": "Suplemento em pó com creatina monohidratada, magnésio bisglicinato e coenzima Q10, nos sabores Morango e Tangerina. Veja os preços e compre com garantia de 30 dias.",
    "colunas": True,
    "linhas": [("1 Mês", 197.00, "bb220038-f89c-4611-a0f8-43d5935705ad", None),
               ("3 Meses", 417.00, "f33bd68a-46b5-4548-85bc-d05810400556", "815a83ed-8c16-11f1-b7d4-0affdf3a7b6b"),
               ("5 Meses", 529.00, "85f3495d-4fd4-4326-8d6e-8ff3871b9a21", "9388c4f4-8c16-11f1-b7d4-0affdf3a7b6b")],
    "nota_extra": "O kit de 1 mês existe só no sabor Morango. Os preços são iguais nos dois sabores.",
    "sobre": [
      "O CreaGym junta três ingredientes em um só suplemento:",
    ],
    "itens": [
      "<strong>Creatina monohidratada</strong>: a forma de creatina mais estudada, usada por quem treina com pesos ou faz esportes de esforço curto e intenso.",
      "<strong>Magnésio bisglicinato</strong>: forma de magnésio ligada ao aminoácido glicina.",
      "<strong>Coenzima Q10</strong>: substância presente nas células e usada em suplementos.",
    ],
    "depois": [
      "A quantidade de cada ingrediente por porção está no rótulo. Suplemento não substitui uma alimentação variada nem o treino.",
    ],
    "aviso": "Este produto não é medicamento. Creatina não é indicada para gestantes, lactantes e crianças. Pessoas com doença nos rins devem consultar um profissional de saúde antes de usar. Siga a porção indicada no rótulo.",
    "faq": [
      ("Quais sabores o CreaGym tem?", "Morango e Tangerina. O kit de 1 mês é só Morango; os kits de 3 e 5 meses existem nos dois sabores, com o mesmo preço."),
      ("O que tem no CreaGym?", "Creatina monohidratada, magnésio bisglicinato e coenzima Q10, segundo a descrição do produto. As quantidades estão no rótulo."),
      ("Tem garantia?", "Sim. A Velmora oferece garantia de 30 dias, pela Hest."),
      ("Quais as formas de pagamento?", "Cartão de crédito em até 12x, Pix e boleto, no checkout da Hest."),
    ],
  },
  "creatina-gummy": {
    "img": ("img/creatina-gummy-tutti-frutti-60-gomas.webp", 331, 600, "Frasco de Creatina Gummy sabor tutti-frutti da Velmora, 60 gomas"),
    "nome": "Creatina Gummy",
    "chamada": "Quero a minha Creatina Gummy",
    "badge": "Creatina em goma",
    "title": "Creatina Gummy: creatina em goma, preços e onde comprar | Velmo Drink",
    "desc": "Creatina Gummy, a creatina em goma da Velmora: 3 g de creatina por porção, sabor tutti-frutti, sem açúcar e sem glúten. Preços de 1, 3 e 5 meses.",
    "h1": "Creatina Gummy",
    "lead": "Creatina em goma: 3 g de creatina por porção de 2 gomas, sabor tutti-frutti, sem açúcar e sem glúten. Veja os preços de 1, 3 e 5 meses e compre com garantia de 30 dias.",
    "linhas": [("1 Mês", 197.00, "a427da49-539f-4bdc-81e1-bde5045d758a"),
               ("3 Meses", 459.00, "cdb8df1b-cf09-43eb-8743-be11c242a59e"),
               ("5 Meses", 630.00, "7e862ab8-9af8-4a1b-8831-d5ac8d6f71a5")],
    "sobre": [
      "A Creatina Gummy é a creatina em formato de goma de mastigar, para quem não quer misturar pó na água. Segundo a descrição do produto, cada porção tem 3 g de creatina, o sabor é tutti-frutti e as gomas não têm açúcar nem glúten.",
      "A creatina aumenta o desempenho físico durante exercícios repetidos de curta duração e alta intensidade. Para isso, a porção diária precisa ter pelo menos 3 g de creatina, junto com treino.",
    ],
    "itens": [],
    "depois": [
      "<strong>Como tomar:</strong> 2 gomas por dia, que somam 3 g de creatina. Cada frasco tem 30 porções (60 gomas), o suficiente para 1 mês. Indicado para maiores de 19 anos.",
      "<strong>Informação nutricional da porção (9 g, 2 gomas):</strong> 9 kcal, 4,2 g de carboidratos, 0 g de açúcares, 4 g de polióis (dos quais 1,5 g de eritritol) e 3.000 mg de creatina. Depois de aberto, consuma em até 90 dias e guarde em local fresco e seco, entre 15 e 30 °C.",
      "Suplemento não substitui uma alimentação variada.",
    ],
    "aviso": "Este produto não é medicamento. Não deve ser consumido por gestantes, lactantes e crianças; é indicado para maiores de 19 anos. Pessoas com doença nos rins devem consultar um profissional de saúde antes de usar creatina. Não ultrapasse 2 gomas por dia e mantenha fora do alcance de crianças.",
    "faq": [
      ("Creatina goma funciona?", "Funciona, desde que a porção diária tenha pelo menos 3 g de creatina, junto com treino. A creatina em goma entrega a mesma creatina do pó, só muda o formato: a Creatina Gummy tem 3 g em 2 gomas."),
      ("Quanto de creatina tem a Creatina Gummy?", "3 g (3.000 mg) de creatina por porção de 2 gomas, segundo o rótulo."),
      ("Quantas gomas por dia?", "2 gomas por dia. O frasco tem 60 gomas, ou 30 porções, para 1 mês de uso."),
      ("Tem açúcar ou glúten?", "Não tem açúcar: o rótulo informa 0 g de açúcares e adoçante eritritol. A descrição do produto informa que também não tem glúten."),
      ("Tem garantia?", "Sim. A Velmora oferece garantia de 30 dias, pela Hest."),
      ("Quais as formas de pagamento?", "Cartão de crédito em até 12x, Pix e boleto, no checkout da Hest."),
    ],
  },
}

def mes(slug):
    k, v = PRODUTOS[slug]["linhas"][-1][0], PRODUTOS[slug]["linhas"][-1][1]
    n = int(k.split()[0])
    return f"ou {brl(v / n)} por mês no kit de {k.lower()}"

DRINK_MOR = ("img/velmo-black-drink-morango-150g.webp", 475, 465, "Pote de Velmo Black Drink sabor Morango, 150 g, 30 porções")
DRINK_TAN = ("img/velmo-black-drink-tangerina-150g.webp", 456, 465, "Pote de Velmo Black Drink sabor Tangerina, 150 g, 30 porções")

# (link da página ou None, nome, descrição, preço, uuid do checkout ou None, foto, linha extra, texto do botão)
SECOES = [
  ("velmo-black", "Velmo Black", "A linha principal da Velmora: o drink em pó, em dois sabores, e a versão em cápsulas.", None, [
    ("index.html", "Velmo Black Drink Morango", "Pó para preparo de bebida, sabor morango. Pote de 150 g com 30 porções.", 209.90, None, DRINK_MOR, "", "Ver detalhes e kits"),
    ("index.html", "Velmo Black Drink Tangerina", "Pó para preparo de bebida, sabor tangerina. Pote de 150 g com 30 porções.", 209.90, None, DRINK_TAN, "", "Ver detalhes e kits"),
    (None, "Velmo Black (cápsulas)", "A linha Velmo Black em cápsulas. Pote com 60 cápsulas; composição e modo de uso no rótulo.", 197.90, "d749bf05-25b1-4646-8139-35423bb2fb05",
     ("img/velmo-black-capsulas-1-pote.webp", 400, 810, "Pote de Velmo Black cápsulas, da Velmora, com 60 cápsulas"), "", "Quero o meu"),
  ]),
  ("creatina", "Creatina", "Creatina monohidratada em dois formatos: pó para misturar na água ou goma para mastigar.",
   ("creatina.html", "Creatina em pó ou em goma? Veja a comparação"), [
    ("creagym.html", "CreaGym", "Creatina monohidratada em pó com magnésio bisglicinato e coenzima Q10. Sabores Morango e Tangerina.", 197.00, None, PRODUTOS["creagym"]["img"], mes("creagym"), "Ver preços e detalhes"),
    ("creatina-gummy.html", "Creatina Gummy", "Gomas com 3 g de creatina por porção, sabor tutti-frutti, sem açúcar e sem glúten.", 197.00, None, PRODUTOS["creatina-gummy"]["img"], mes("creatina-gummy"), "Ver preços e detalhes"),
  ]),
  ("cuidados-intimos", "Cuidados com a pele", "Cosmético de uso externo para clarear áreas que escurecem com o atrito.", None, [
    ("clarize.html", "Clarize", "Clareador para virilha, axilas e joelhos, com niacinamida e ácido hialurônico. Frasco de 60 ml.", 209.00, None, PRODUTOS["clarize"]["img"], mes("clarize"), "Ver preços e detalhes"),
  ]),
]

def head(title, desc, canon, ld):
    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{html.escape(title)}</title>
  <meta name="description" content="{html.escape(desc)}">
  <meta property="og:title" content="{html.escape(title)}">
  <meta property="og:description" content="{html.escape(desc)}">
  <meta property="og:type" content="website">
  <meta name="robots" content="index, follow">
  <link rel="canonical" href="{canon}">
  <link rel="stylesheet" href="css/style.css">
  <link rel="stylesheet" href="css/loja.css">
  <script type="application/ld+json">
{json.dumps(ld, ensure_ascii=False, indent=2)}
  </script>
</head>
<body>
  <script>
    window.skipInjection = ['hero', 'about', 'features'];
  </script>

  <div id="header-placeholder"></div>
"""

FOOT = """
  <a id="whatsapp-float" aria-label="Mais informações"></a>
  <div id="footer-placeholder"></div>
  <script src="js/main.js"></script>
</body>
</html>
"""

def crumbs(nome, slug):
    itens = [("Página Inicial", f"{SITE}/"), ("Loja", f"{SITE}/loja.html")]
    if slug:
        itens.append((nome, f"{SITE}/{slug}.html"))
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": u} for i, (n, u) in enumerate(itens)]}

def pagina_produto(slug, p):
    canon = f"{SITE}/{slug}.html"
    precos = [l[1] for l in p["linhas"]]
    ld = {"@context": "https://schema.org", "@graph": [
        crumbs(p["nome"], slug),
        {"@type": "Product", "name": p["nome"], "description": p["desc"],
         "brand": {"@type": "Brand", "name": "Velmora"},
         **({"image": f"{SITE}/{p['img'][0]}"} if p.get("img") else {}),
         "offers": {"@type": "AggregateOffer", "priceCurrency": "BRL",
                    "lowPrice": f"{min(precos):.2f}", "highPrice": f"{max(precos):.2f}",
                    "offerCount": str(len(precos)), "availability": "https://schema.org/InStock"}},
        {"@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in p["faq"]]},
    ]}
    if p.get("colunas"):
        cab = "<tr><th>Kit</th><th>Preço</th><th>Sabor</th><th></th></tr>"
        corpo = "\n".join(
            f"<tr><td>{k}</td><td class=\"preco\">{brl(v)}</td><td>{link(m, 'Morango')}</td>"
            f"<td>{link(t, 'Tangerina') if t else '—'}</td></tr>" for k, v, m, t in p["linhas"])
    else:
        cab = "<tr><th>Kit</th><th>Preço</th><th></th></tr>"
        corpo = "\n".join(f"<tr><td>{k}</td><td class=\"preco\">{brl(v)}</td><td>{link(u)}</td></tr>" for k, v, u in p["linhas"])
    vitrine = ""
    if slug in V.FOTOS:
        menor = min(p["linhas"], key=lambda l: l[1] / int(l[0].split()[0]))
        cards = []
        for l in p["linhas"]:
            links = ([("Quero Morango", l[2])] + ([("Quero Tangerina", l[3])] if l[3] else [])) if p.get("colunas") else [("Quero este kit", l[2])]
            cards.append(V.card(slug, p["nome"], l[0], l[1], links, destaque=l is menor))
        # Clarize sugerido abaixo dos cards; durante a Black Friday ele já aparece com desconto na seção da oferta.
        vitrine = V.grade(cards) + ("" if BF.ativa(HOJE) else "\n" + V.sugestao_clarize())
    else:
        vitrine = (f'      <div class="precos-wrap">\n        <table class="precos">\n          <thead>{cab}</thead>\n'
                   f'          <tbody>\n{corpo}\n          </tbody>\n        </table>\n      </div>')
    nota = "Frete de R$ 29,90, calculado no checkout junto com o prazo de entrega. Pagamento no cartão em até 12x, Pix ou boleto."
    if p.get("nota_extra"):
        nota = p["nota_extra"] + " " + nota
    sobre = "\n".join(f"        <p>{t}</p>" for t in p["sobre"])
    itens = ("        <ul>\n" + "\n".join(f"          <li>{t}</li>" for t in p["itens"]) + "\n        </ul>") if p["itens"] else ""
    depois = "\n".join(f"        <p>{t}</p>" for t in p["depois"])
    for titulo, blocos in p.get("secoes", []):
        depois += f"\n        <h3>{titulo}</h3>\n" + "\n".join(
            f"        {t}" if t.startswith("<ol") else f"        <p>{t}</p>" for t in blocos)
    faq = "\n".join(f"        <h3>{q}</h3>\n        <p>{a}</p>" for q, a in p["faq"])
    outros = "\n".join(
        f'          <li><a href="{s}.html">{PRODUTOS[s]["nome"]}</a></li>' for s in PRODUTOS if s != slug)
    principal = p["linhas"][0][2]
    im = p.get("img")
    comparar = ('        <p><a href="creatina.html">Creatina em pó ou em goma? Compare o CreaGym com a Creatina Gummy</a>.</p>\n'
                if slug in ("creagym", "creatina-gummy") else "")
    kits = ""
    if p.get("kits") and not vitrine:
        figs = "\n".join(
            f'        <figure><img src="{k[0]}" width="{k[1]}" height="{k[2]}" alt="{k[3]}" loading="lazy"><figcaption>{k[4]}</figcaption></figure>'
            for k in p["kits"])
        kits = f'      <div class="loja-kits">\n{figs}\n      </div>\n      <p class="loja-nota">{p["kits_nota"]}</p>\n'
    # Na Black Friday a oferta substitui a seção de preços normais (não repete os kits com preço cheio)
    # e os botões do topo e do fim levam para a oferta.
    em_oferta = BF.ativa(HOJE) and slug in BF.OFERTAS
    if em_oferta:
        secao_precos = ""
        botao_topo = '<a class="btn btn-primary" href="#black-friday">Ver ofertas com 30% OFF</a>'
        cta_final = (f'      <p class="section-desc">{BF.nome_campanha(HOJE)}: 30% OFF nos kits até {BF.FIM_TEXTO}, com garantia de 30 dias.</p>\n'
                     '      <a class="btn btn-primary" href="#black-friday">Ver as ofertas</a>')
    else:
        secao_precos = f"""  <section class="section section-alt" id="precos">
    <div class="container">
      <span class="section-subtitle">Preços</span>
      <h2 class="section-title">Kits do {p['nome']}</h2>
{vitrine}
      <p class="loja-nota">{nota}</p>
{kits}      <p class="loja-nota">{AFILIADO}</p>
      <!-- compartilhar -->
    </div>
  </section>
"""
        botao_topo = '<a class="btn btn-primary" href="#precos">Ver preços</a>'
        cta_final = (f"      <p class=\"section-desc\">Kit de 1 mês por {brl(p['linhas'][0][1])}, com garantia de 30 dias.</p>\n"
                     f"      {link(principal, 'Quero o kit de 1 mês')}")
    foto = (f'<div class="loja-hero-foto"><img src="{im[0]}" width="{im[1]}" height="{im[2]}" alt="{im[3]}" fetchpriority="high"></div>' if im else "")
    return head(p["title"], p["desc"], canon, ld) + f"""
  <section class="hero loja-hero">
    {BF.faixa(HOJE) if slug in BF.OFERTAS else ""}
    <div class="container{' loja-hero-grid' if im else ''}">
      <div class="hero-content">
        <div class="hero-badge">{p['badge']}</div>
        <h1>{p['h1']}</h1>
        <p class="hero-desc">{p['lead']}</p>
        <div class="hero-actions">
          {botao_topo}
          <a class="btn btn-outline" href="loja.html">Voltar para a Loja</a>
        </div>
      </div>
      {foto}
    </div>
  </section>

  {BF.bloco_produto(slug, HOJE)}
{secao_precos}
  <section class="seo-section">
    <div class="seo-inner">
      <h2>O que é o {p['nome']}</h2>
      <div class="conteudo-seo">
{sobre}
{itens}
{depois}
        <div class="loja-aviso"><strong>Cuidados:</strong> {p['aviso']}</div>
        <h2 style="margin-top:48px;">Perguntas frequentes</h2>
{faq}
{comparar}        <h3>Outros produtos da Loja</h3>
        <ul>
{outros}
          <li><a href="loja.html">Todos os produtos</a></li>
        </ul>
        <p class="loja-assinatura">Texto da Equipe Velmo Drink, com base na descrição do produto e no rótulo. Atualizado em outubro de 2026.</p>
      </div>
    </div>
  </section>

  <div class="cta-section">
    <div class="container">
      <h2 class="section-title">{p.get('chamada', 'Quero o meu ' + p['nome'])}</h2>
{cta_final}
    </div>
  </div>
""" + FOOT

def card(c, h="h3", lazy=True):
    s, n, d, v, u, im, extra, btxt = c
    foto = (f'<img class="loja-foto" src="{im[0]}" width="{im[1]}" height="{im[2]}" alt="{im[3]}"{" loading=\"lazy\"" if lazy else ""}>' if im else "")
    botao = (f'<a class="btn btn-primary" href="{s}">{btxt}</a>' if s else link(u, btxt))
    extra = f'\n          <div class="loja-mes">{extra}</div>' if extra else ""
    return f"""        <div class="loja-card">
          {foto}
          <{h}>{n}</{h}>
          <p>{d}</p>
          <div class="loja-preco">a partir de <strong>{brl(v)}</strong></div>{extra}
          {botao}
        </div>"""

def pagina_loja():
    canon = f"{SITE}/loja.html"
    todos = [c for sec in SECOES for c in sec[4]]
    ld = {"@context": "https://schema.org", "@graph": [
        crumbs("Loja", None),
        {"@type": "ItemList", "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": c[1],
             "url": f"{SITE}/{c[0]}" if c[0] else f"{H}{c[4]}"} for i, c in enumerate(todos)]},
    ]}
    nav = " · ".join(f'<a href="#{sid}">{t}</a>' for sid, t, _, _, _ in SECOES)
    blocos = []
    for k, (sid, titulo, texto, extra, cards) in enumerate(SECOES):
        ex = f' <a href="{extra[0]}">{extra[1]}</a>' if extra else ""
        blocos.append(f"""  <section class="section{' section-alt' if k % 2 == 0 else ''}" id="{sid}">
    <div class="container">
      <span class="section-subtitle">Loja</span>
      <h2 class="section-title">{titulo}</h2>
      <p class="loja-secao-desc">{texto}{ex}</p>
      <div class="loja-grid">
{chr(10).join(card(c, lazy=k > 0) for c in cards)}
      </div>
    </div>
  </section>
""")
    return head("Loja: Velmo Black, CreaGym, Creatina Gummy e Clarize | Velmo Drink",
                "Produtos da Velmora: Velmo Black Drink e cápsulas, creatina CreaGym e Creatina Gummy, e Clarize. Preços, garantia de 30 dias e pagamento em até 12x.",
                canon, ld) + f"""
  <section class="hero loja-hero">
    {BF.faixa(HOJE, "creatina.html#black-friday")}
    <div class="container loja-hero-grid">
      <div class="hero-content">
        <div class="hero-badge">Loja</div>
        <h1>Produtos da Velmora</h1>
        <p class="hero-desc">O Velmo Black Drink e os outros produtos da Velmora: suplementos para quem treina e cosmético. Todos têm garantia de 30 dias e pagamento no cartão em até 12x, Pix ou boleto.</p>
        <p class="loja-atalhos">{nav}</p>
      </div>
      <div class="loja-hero-foto"><a href="index.html"><img src="img/velmo-black-drink-morango-e-tangerina.webp" width="700" height="315" alt="Potes de Velmo Black Drink sabor Morango e sabor Tangerina, da Velmora" fetchpriority="high"></a></div>
    </div>
  </section>

{"".join(blocos)}
  <section class="section">
    <div class="container">
      <p class="loja-nota">{AFILIADO}</p>
    </div>
  </section>
""" + FOOT

def guias_atuais():
    # A lista de guias é preenchida por fonte/gerar_blog.py (só posts já publicados);
    # aqui ela é mantida como está no creatina.html atual.
    try:
        atual = open(os.path.join(OUT, "creatina.html"), encoding="utf-8").read()
        return atual.split("<!-- guias:inicio -->", 1)[1].split("<!-- guias:fim -->", 1)[0]
    except (OSError, IndexError):
        return ""


def pagina_creatina():
    canon = f"{SITE}/creatina.html"
    cg, gm = PRODUTOS["creagym"], PRODUTOS["creatina-gummy"]
    faq = [
      ("Creatina em pó ou em goma: qual é melhor?", "As duas entregam creatina monohidratada. A diferença está no formato e no preço. O pó (CreaGym) sai mais barato por mês nos kits maiores e traz magnésio e coenzima Q10 na fórmula. A goma (Creatina Gummy) é mais prática: não precisa de água nem de coqueteleira."),
      ("Quanto de creatina por dia?", "A quantidade estudada para melhorar o desempenho é de pelo menos 3 g por dia, junto com treino. A Creatina Gummy tem 3 g em 2 gomas. No CreaGym, a quantidade por porção está no rótulo."),
      ("Precisa tomar creatina todos os dias?", "Sim. A creatina funciona pelo acúmulo nos músculos com o uso diário, inclusive nos dias sem treino. Siga a porção indicada no rótulo."),
      ("Quem não deve tomar creatina?", "Gestantes, lactantes e crianças não devem tomar. Pessoas com doença nos rins devem consultar um profissional de saúde antes de usar."),
    ]
    def pm(p, i):
        k, v = p["linhas"][i][0], p["linhas"][i][1]
        return brl(v / int(k.split()[0]))
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Página Inicial", "item": f"{SITE}/"},
            {"@type": "ListItem", "position": 2, "name": "Loja", "item": f"{SITE}/loja.html"},
            {"@type": "ListItem", "position": 3, "name": "Creatina", "item": canon}]},
        {"@type": "ItemList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "CreaGym", "url": f"{SITE}/creagym.html"},
            {"@type": "ListItem", "position": 2, "name": "Creatina Gummy", "url": f"{SITE}/creatina-gummy.html"}]},
        {"@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]},
    ]}
    cards = [c for c in SECOES[1][4]]
    linhas = [
      ("Formato", "Pó para misturar na água", "Goma para mastigar"),
      ("Creatina", "Monohidratada (quantidade por porção no rótulo)", "Monohidratada, 3 g em 2 gomas"),
      ("Outros ingredientes", "Magnésio bisglicinato e coenzima Q10", "Sem açúcar e sem glúten"),
      ("Sabores", "Morango e Tangerina", "Tutti-frutti"),
      ("Embalagem", "Pote de 300 g", "Pote com 60 gomas (30 porções)"),
      ("Kit de 1 mês", brl(cg["linhas"][0][1]), brl(gm["linhas"][0][1])),
      ("Kit de 3 meses", f"{brl(cg['linhas'][1][1])} ({pm(cg, 1)}/mês)", f"{brl(gm['linhas'][1][1])} ({pm(gm, 1)}/mês)"),
      ("Kit de 5 meses", f"{brl(cg['linhas'][2][1])} ({pm(cg, 2)}/mês)", f"{brl(gm['linhas'][2][1])} ({pm(gm, 2)}/mês)"),
    ]
    tabela = "\n".join(f"            <tr><th scope=\"row\">{a}</th><td>{b}</td><td>{c}</td></tr>" for a, b, c in linhas)
    faqh = "\n".join(f"        <h3>{q}</h3>\n        <p>{a}</p>" for q, a in faq)
    return head("Creatina em pó ou em goma: CreaGym x Creatina Gummy | Velmo Drink",
                "Compare a creatina em pó CreaGym com a Creatina Gummy, em goma: formato, ingredientes, sabores e preço por mês de cada kit. Garantia de 30 dias.",
                canon, ld) + f"""
  <section class="hero loja-hero">
    {BF.faixa(HOJE)}
    <div class="container loja-hero-grid">
      <div class="hero-content">
        <div class="hero-badge">Creatina</div>
        <h1>Creatina em pó ou em goma: qual escolher</h1>
        <p class="hero-desc">A Velmora vende creatina monohidratada em dois formatos: o CreaGym, em pó, e a Creatina Gummy, em gomas. Veja a diferença entre os dois e o preço por mês de cada kit.</p>
        <div class="hero-actions">
          <a class="btn btn-primary" href="#comparacao">Ver a comparação</a>
          <a class="btn btn-outline" href="loja.html">Voltar para a Loja</a>
        </div>
      </div>
      <div class="loja-hero-foto"><img src="{cg['img'][0]}" width="{cg['img'][1]}" height="{cg['img'][2]}" alt="{cg['img'][3]}" fetchpriority="high"></div>
    </div>
  </section>

  {BF.bloco_comparacao(HOJE)}
  <section class="section section-alt" id="comparacao">
    <div class="container">
      <span class="section-subtitle">Comparação</span>
      <h2 class="section-title">CreaGym x Creatina Gummy</h2>
      <div class="precos-wrap">
        <table class="precos comparacao">
          <thead><tr><th></th><th>CreaGym (pó)</th><th>Creatina Gummy (goma)</th></tr></thead>
          <tbody>
{tabela}
          </tbody>
        </table>
      </div>
      <p class="loja-nota">Informações da descrição de cada produto. Confira sempre o rótulo. {AFILIADO}</p>
      <div class="loja-grid">
{chr(10).join(card(c) for c in cards)}
      </div>
    </div>
  </section>

  <section class="seo-section">
    <div class="seo-inner">
      <h2>Para quem é cada formato</h2>
      <div class="conteudo-seo">
        <p><strong>CreaGym, em pó</strong>, combina com quem já prepara bebidas para o treino e quer gastar menos por mês: no kit de 5 meses, sai por {pm(cg, 2)} por mês. A fórmula também traz magnésio bisglicinato e coenzima Q10.</p>
        <p><strong>Creatina Gummy, em goma</strong>, combina com quem não gosta de misturar pó ou passa o dia fora de casa: basta mastigar 2 gomas por dia. Cada porção tem 3 g de creatina, sem açúcar e sem glúten.</p>
        <p>Nos dois casos, a creatina aumenta o desempenho físico em exercícios repetidos de curta duração e alta intensidade quando a porção diária tem pelo menos 3 g, junto com treino. Suplemento não substitui uma alimentação variada.</p>
        <div class="loja-aviso"><strong>Cuidados:</strong> {cg['aviso']}</div>
        <h2 style="margin-top:48px;">Perguntas frequentes</h2>
{faqh}
        <h3>Páginas dos produtos</h3>
        <ul>
          <li><a href="creagym.html">CreaGym: preços dos kits Morango e Tangerina</a></li>
          <li><a href="creatina-gummy.html">Creatina Gummy: preços dos kits</a></li>
          <li><a href="loja.html">Todos os produtos da Loja</a></li>
        </ul>
        <h3>Guias sobre creatina</h3>
        <ul>
<!-- guias:inicio -->{guias_atuais()}<!-- guias:fim -->
        </ul>
        <p class="loja-assinatura">Texto da Equipe Velmo Drink, com base na descrição dos produtos e nos rótulos. Atualizado em outubro de 2026.</p>
      </div>
    </div>
  </section>
""" + FOOT

for slug, p in PRODUTOS.items():
    open(os.path.join(OUT, f"{slug}.html"), "w").write(pagina_produto(slug, p))
open(os.path.join(OUT, "loja.html"), "w").write(pagina_loja())
pagina = pagina_creatina()  # antes de abrir o arquivo, que zera o conteúdo
open(os.path.join(OUT, "creatina.html"), "w").write(pagina)
# GTM, GA4, imagem de compartilhamento e botões de compartilhar em todas as páginas.
subprocess.run([sys.executable, "-I", os.path.join(os.path.dirname(os.path.abspath(__file__)), "rastreio.py"), OUT], check=True)
print("ok")
