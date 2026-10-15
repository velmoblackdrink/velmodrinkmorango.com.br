"""Põe em todas as páginas .html da pasta: Google Tag Manager, GA4, imagem de compartilhamento
(og:image) e os botões de compartilhar (WhatsApp, Facebook, Instagram, copiar link).

Uso: python3 -I fonte/rastreio.py .
Os geradores (gerar_loja.py e gerar_blog.py) já chamam este script no fim. Pode rodar quantas vezes
quiser: tudo fica entre marcadores <!-- rastreio:inicio/fim -->, <!-- gtm-noscript:inicio/fim --> e
<!-- compartilhar:inicio/fim -->, que são trocados a cada rodada.
Onde houver <!-- compartilhar --> no HTML, entra uma barra de compartilhar; se a página não tiver
nenhum, entra uma antes do rodapé. Onde houver <!-- compartilhar:topo --> (abaixo da foto do topo),
entra uma versão compacta, entre <!-- compartilhar-topo:inicio/fim -->.
"""
import html
import os
import re
import sys
from urllib.parse import quote

SITE = "https://velmodrinkmorango.com.br"
GTM = "GTM-5RQXHCPW"
GA4 = "G-Z921CFD04J"
SEM_COMPARTILHAR = {"mapa-do-site.html"}

# Imagem de compartilhamento: 1200x630 em img/og/. A primeira regra que casar com o nome do arquivo vale.
IMAGENS = [
    (("clarize", "virilha", "axila", "niacinamida", "clarea", "clareador"), "clarize", "Clarize, clareador da Velmora, frasco de 60 ml"),
    (("gummy", "goma"), "creatina-gummy", "Creatina Gummy, gomas de creatina da Velmora"),
    (("creatina", "creagym"), "creagym", "CreaGym, creatina monohidratada sabor morango"),
]
IMAGEM_PADRAO = ("velmo-drink", "Velmo Black Drink sabores Morango e Tangerina")

ESTILO = (".compartilhar{margin:32px auto;max-width:720px;padding:20px;border-radius:12px;background:#f6f3f8;"
          "text-align:center;font-family:inherit}.compartilhar p{margin:0 0 12px;font-weight:600;color:#222}"
          ".compartilhar-botoes{display:flex;flex-wrap:wrap;gap:8px;justify-content:center}"
          ".compartilhar a,.compartilhar button{display:inline-flex;align-items:center;gap:6px;padding:10px 16px;"
          "border:0;border-radius:999px;font:inherit;font-size:15px;font-weight:600;color:#fff;cursor:pointer;"
          "text-decoration:none}.comp-whatsapp{background:#1f8f4e}.comp-facebook{background:#1663c7}"
          ".comp-instagram{background:#c13584}.comp-copiar{background:#555}"
          ".compartilhar-topo{margin:4px auto 20px;padding:0;background:none;display:flex;flex-wrap:wrap;"
          "align-items:center;justify-content:center;gap:8px}.compartilhar-topo p{margin:0;font-size:14px;"
          "font-weight:500;color:#4a5e59}.compartilhar-topo a,.compartilhar-topo button{padding:7px 13px;font-size:13px}")


def imagem_de(nome):
    for palavras, arquivo, alt in IMAGENS:
        if any(p in nome for p in palavras):
            return arquivo, alt
    return IMAGEM_PADRAO


def canonico(doc, nome):
    m = re.search(r'<link rel="canonical" href="([^"]+)"', doc)
    return m.group(1) if m else f"{SITE}/{nome}"


def titulo(doc):
    m = re.search(r'<meta property="og:title" content="([^"]*)"', doc) or re.search(r"<title>([^<]*)</title>", doc)
    return html.unescape(m.group(1)).strip() if m else "Velmo Drink"


def slug(nome):
    return "inicio" if nome == "index.html" else nome[:-5]


def bloco_head(doc, nome):
    arquivo, alt = imagem_de(nome)
    img = f"{SITE}/img/og/{arquivo}.jpg"
    linhas = [
        "<!-- rastreio:inicio (gerado por fonte/rastreio.py: não editar à mão) -->",
        "<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}"
        f"gtag('js',new Date());gtag('config','{GA4}');</script>",
        f'<script async src="https://www.googletagmanager.com/gtag/js?id={GA4}"></script>',
        "<script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':new Date().getTime(),event:'gtm.js'});"
        "var f=d.getElementsByTagName(s)[0],j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;"
        "j.src='https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);"
        f"}})(window,document,'script','dataLayer','{GTM}');</script>",
        f'<meta property="og:url" content="{canonico(doc, nome)}">',
        '<meta property="og:site_name" content="Velmo Drink">',
        '<meta property="og:locale" content="pt_BR">',
        f'<meta property="og:image" content="{img}">',
        '<meta property="og:image:type" content="image/jpeg">',
        '<meta property="og:image:width" content="1200">',
        '<meta property="og:image:height" content="630">',
        f'<meta property="og:image:alt" content="{html.escape(alt)}">',
        '<meta name="twitter:card" content="summary_large_image">',
        f'<meta name="twitter:image" content="{img}">',
        '<script src="js/rastreio.js" defer></script>',
        f"<style>{ESTILO}</style>",
        "<!-- rastreio:fim -->",
    ]
    if 'property="og:type"' not in doc:
        linhas.insert(4, '<meta property="og:type" content="website">')
    return "\n".join("  " + l for l in linhas) + "\n"


def botoes_compartilhar(doc, nome):
    url = canonico(doc, nome)
    utm = lambda rede: f"{url}?utm_source={rede}&utm_medium=social&utm_campaign=compartilhar&utm_content={slug(nome)}"
    texto = quote(f"{titulo(doc)} {utm('whatsapp')}", safe="")
    fb = quote(utm("facebook"), safe="")
    return f"""<div class="compartilhar-botoes">
      <a class="comp-whatsapp" data-rede="whatsapp" href="https://wa.me/?text={texto}" target="_blank" rel="nofollow noopener">Enviar pelo WhatsApp</a>
      <a class="comp-facebook" data-rede="facebook" href="https://www.facebook.com/sharer/sharer.php?u={fb}" target="_blank" rel="nofollow noopener">Facebook</a>
      <button type="button" class="comp-instagram" data-rede="instagram" data-url="{html.escape(utm('instagram'))}">Instagram</button>
      <button type="button" class="comp-copiar" data-rede="copiar" data-url="{html.escape(utm('copiar'))}">Copiar link</button>
    </div>"""


def bloco_compartilhar(doc, nome):
    return f"""<!-- compartilhar:inicio -->
  <div class="compartilhar">
    <p>Gostou? Envie para alguém:</p>
    {botoes_compartilhar(doc, nome)}
  </div>
  <!-- compartilhar:fim -->"""


def bloco_compartilhar_topo(doc, nome):
    return f"""<!-- compartilhar-topo:inicio -->
        <div class="compartilhar compartilhar-topo">
          <p>Compartilhe:</p>
          {botoes_compartilhar(doc, nome)}
        </div>
        <!-- compartilhar-topo:fim -->"""


def aplicar(doc, nome):
    # Limpa o que já existe: blocos de rodadas anteriores e metas que o bloco passa a controlar.
    doc = re.sub(r"[ \t]*<!-- rastreio:inicio.*?<!-- rastreio:fim -->\n", "", doc, flags=re.S)
    doc = re.sub(r"[ \t]*<!-- gtm-noscript:inicio -->.*?<!-- gtm-noscript:fim -->\n", "", doc, flags=re.S)
    doc = re.sub(r"<!-- compartilhar:inicio -->.*?<!-- compartilhar:fim -->", "<!-- compartilhar -->", doc, flags=re.S)
    doc = re.sub(r"<!-- compartilhar-topo:inicio -->.*?<!-- compartilhar-topo:fim -->", "<!-- compartilhar:topo -->", doc, flags=re.S)
    doc = re.sub(r'[ \t]*<meta (?:property="og:(?:url|site_name|locale|image[a-z:]*)"|name="twitter:[a-z:]+") content="[^"]*">\n', "", doc)

    vp = re.search(r"<meta name=\"viewport\"[^>]*>\n", doc)
    pos = vp.end() if vp else doc.index("<head>") + len("<head>\n")
    doc = doc[:pos] + bloco_head(doc, nome) + doc[pos:]

    body = re.search(r"<body[^>]*>\n?", doc)
    doc = (doc[:body.end()] + "  <!-- gtm-noscript:inicio -->\n"
           f'  <noscript><iframe src="https://www.googletagmanager.com/ns.html?id={GTM}" height="0" width="0" '
           'style="display:none;visibility:hidden"></iframe></noscript>\n  <!-- gtm-noscript:fim -->\n' + doc[body.end():])

    if nome in SEM_COMPARTILHAR:
        return doc.replace("<!-- compartilhar -->", "").replace("<!-- compartilhar:topo -->", "")
    doc = doc.replace("<!-- compartilhar:topo -->", bloco_compartilhar_topo(doc, nome))
    if "<!-- compartilhar -->" not in doc:
        rodape = re.search(r'[ \t]*<div id="footer-placeholder">|[ \t]*<footer[ >]', doc)
        doc = doc[:rodape.start()] + "  <!-- compartilhar -->\n\n" + doc[rodape.start():]
    return doc.replace("<!-- compartilhar -->", bloco_compartilhar(doc, nome))


def main(pasta):
    for nome in sorted(os.listdir(pasta)):
        if not nome.endswith(".html"):
            continue
        caminho = os.path.join(pasta, nome)
        with open(caminho, encoding="utf-8") as f:
            antes = f.read()
        depois = aplicar(antes, nome)
        if depois != antes:
            with open(caminho, "w", encoding="utf-8") as f:
                f.write(depois)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else ".")
