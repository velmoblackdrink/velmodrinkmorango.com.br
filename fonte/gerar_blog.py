# Gera o blog. Só publica os posts com data <= hoje (horário de Brasília), então um post
# com data futura fica na fila e entra no ar sozinho no dia (ver .github/workflows/publicar-blog.yml).
# Uso, da raiz do repo: python3 -I fonte/gerar_blog.py .   (HOJE=AAAA-MM-DD força a data, para testar)
import datetime, html, json, os, subprocess, sys, zoneinfo

sys.dont_write_bytecode = True  # sem __pycache__ dentro do repo
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import black_friday as BF

SITE = "https://velmodrinkmorango.com.br"
OUT = sys.argv[1]
AUTOR = "Equipe Velmo Drink"
HOJE = os.environ.get("HOJE") or datetime.datetime.now(zoneinfo.ZoneInfo("America/Sao_Paulo")).date().isoformat()
MESES = ["janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho",
         "agosto", "setembro", "outubro", "novembro", "dezembro"]

def data_br(iso):
    a, m, d = iso.split("-")
    return f"{int(d)} de {MESES[int(m) - 1]} de {a}"

def head(title, desc, canon, ld, tipo="website"):
    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{html.escape(title)}</title>
  <meta name="description" content="{html.escape(desc)}">
  <meta property="og:title" content="{html.escape(title)}">
  <meta property="og:description" content="{html.escape(desc)}">
  <meta property="og:type" content="{tipo}">
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

def crumbs(*itens):
    base = [("Página Inicial", f"{SITE}/"), ("Blog", f"{SITE}/blog.html")]
    todos = base + list(itens)
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": u} for i, (n, u) in enumerate(todos)]}

# Cada post: slug, título (title tag), h1, descrição, categoria, data, resumo do card,
# corpo (HTML), faq [(pergunta, resposta)]
POSTS = []

CTA_CREATINA_CALISTENIA = """
<div class="blog-cta">
  <p class="blog-cta-titulo">Creatina para quem treina em casa</p>
  <p>A Velmora tem creatina em pó, o CreaGym, nos sabores Morango e Tangerina, e em goma, a Creatina Gummy, com 3 g por porção. Compare formato, ingredientes e preço por mês.</p>
  <a class="btn btn-primary" href="creatina.html">Ver a comparação</a>
</div>
"""

AVISO_CALISTENIA = """<div class="loja-aviso"><strong>Importante:</strong> Este texto é informativo e não substitui a orientação de um profissional de educação física ou de saúde. Creatina não é indicada para gestantes, lactantes e crianças, e pessoas com doença nos rins devem consultar um profissional antes de usar.</div>"""

POSTS.append(dict(
    slug="calistenia-para-iniciantes",
    curto="Calistenia para iniciantes",
    title="Calistenia para iniciantes: como começar em casa, sem equipamento | Velmo Drink",
    h1="Calistenia para iniciantes: como começar em casa",
    desc="Guia de calistenia para iniciantes: 6 exercícios com o peso do corpo, um treino de 4 semanas para fazer em casa, como progredir e os erros mais comuns.",
    categoria="Treino em casa",
    data="2026-10-15",
    resumo="Os 6 exercícios básicos com o peso do corpo, um plano de 4 semanas para fazer em casa e como evoluir sem se machucar.",
    corpo="""
<p>Calistenia é o treino feito com o peso do próprio corpo: agachamento, flexão, prancha, barra. Não precisa de academia nem de aparelhos, só de um pedaço de chão e, mais para frente, de uma barra fixa. Por isso é um dos jeitos mais simples de começar a treinar em casa.</p>
<p>Este guia é para quem está começando do zero. Você vai encontrar os seis exercícios básicos, um plano de quatro semanas e o que fazer para continuar evoluindo.</p>

<h2>O que a calistenia trabalha</h2>
<p>Com treino regular, a calistenia desenvolve força, resistência muscular, equilíbrio e controle do corpo. Como os exercícios usam vários músculos ao mesmo tempo, o treino também deixa o coração mais acelerado do que parece.</p>
<p>E o emagrecimento? Treinar gasta energia e ajuda, mas perder peso depende principalmente da alimentação e da constância ao longo de meses. Desconfie de qualquer programa que prometa um número de quilos em poucas semanas.</p>

<h2>Antes de começar</h2>
<ul>
  <li><strong>Converse com um médico</strong> se você tem problema no coração, pressão alta, dor nas articulações, está grávida ou está parado há muito tempo.</li>
  <li><strong>Aqueça por 5 minutos</strong>: marcha parada, giros de braço e de quadril, alguns agachamentos lentos.</li>
  <li><strong>Use roupa confortável e um tapete</strong> ou toalha dobrada para os exercícios no chão.</li>
  <li><strong>Dor aguda é sinal para parar.</strong> Músculo cansado e um pouco dolorido no dia seguinte é normal; dor forte ou na articulação, não.</li>
</ul>

<h2>Os 6 exercícios básicos</h2>

<h3>1. Agachamento</h3>
<p>Pés na largura dos ombros, desça o quadril para trás como se fosse sentar numa cadeira, com o peito aberto e os joelhos na direção dos pés. Suba empurrando o chão. <strong>Mais fácil:</strong> sente e levante de uma cadeira de verdade.</p>

<h3>2. Flexão de braço</h3>
<p>Mãos um pouco mais abertas que os ombros, corpo reto da cabeça aos pés. Desça o peito até perto do chão e empurre de volta. <strong>Mais fácil:</strong> comece com as mãos na parede, depois numa mesa firme, depois com os joelhos no chão.</p>

<h3>3. Afundo</h3>
<p>Dê um passo à frente e desça até os dois joelhos formarem um ângulo de mais ou menos 90 graus. Volte e troque de perna. <strong>Mais fácil:</strong> segure numa parede ou no encosto de uma cadeira para ter equilíbrio.</p>

<h3>4. Ponte de glúteo</h3>
<p>Deitado de costas, joelhos dobrados e pés no chão. Suba o quadril apertando o glúteo até o corpo formar uma linha dos ombros aos joelhos, segure um segundo e desça devagar.</p>

<h3>5. Prancha</h3>
<p>Apoie os antebraços e as pontas dos pés no chão, corpo reto, barriga firme. Não deixe o quadril cair nem subir demais. <strong>Mais fácil:</strong> joelhos no chão.</p>

<h3>6. Escalador</h3>
<p>Na posição de flexão com os braços esticados, traga um joelho de cada vez em direção ao peito, em ritmo constante. É o exercício que mais acelera o coração da lista. <strong>Mais fácil:</strong> faça devagar, alternando sem pressa.</p>

<h2>Plano de 4 semanas para iniciantes</h2>
<p>Treine <strong>3 vezes por semana</strong>, com um dia de descanso entre os treinos (por exemplo, segunda, quarta e sexta). Faça os exercícios em circuito: um depois do outro, descansando 30 a 60 segundos entre eles. Ao terminar os seis, descanse 2 minutos e repita.</p>
<div class="precos-wrap">
  <table class="precos treino">
    <thead><tr><th>Semana</th><th>Voltas</th><th>Repetições</th><th>Prancha</th></tr></thead>
    <tbody>
      <tr><td>1</td><td>2</td><td>6 a 8 de cada</td><td>15 a 20 s</td></tr>
      <tr><td>2</td><td>2</td><td>8 a 10 de cada</td><td>20 a 30 s</td></tr>
      <tr><td>3</td><td>3</td><td>8 a 10 de cada</td><td>30 s</td></tr>
      <tr><td>4</td><td>3</td><td>10 a 12 de cada</td><td>30 a 40 s</td></tr>
    </tbody>
  </table>
</div>
<p class="loja-nota">No afundo, as repetições são para cada perna. No escalador, conte cada joelho como uma repetição e faça o dobro do número da tabela.</p>
<p>Se uma semana ficou pesada demais, repita a semana em vez de avançar. Terminar bem é mais importante do que terminar rápido.</p>

<h2>Como continuar evoluindo</h2>
<p>Depois das quatro semanas, o corpo se acostuma e o treino precisa ficar um pouco mais difícil. Mude uma coisa de cada vez:</p>
<ul>
  <li><strong>Mais repetições</strong> ou mais uma volta no circuito.</li>
  <li><strong>Variações mais difíceis</strong>: flexão com os joelhos vira flexão completa; agachamento comum vira agachamento com salto.</li>
  <li><strong>Menos descanso</strong> entre os exercícios.</li>
  <li><strong>Uma barra fixa</strong> de porta abre caminho para a barra (pull-up) e a remada, que treinam as costas.</li>
</ul>

<h2>Erros comuns de quem está começando</h2>
<ul>
  <li><strong>Treinar todos os dias desde o início.</strong> O músculo se fortalece no descanso.</li>
  <li><strong>Pular o aquecimento.</strong> São só 5 minutos e reduzem o risco de lesão.</li>
  <li><strong>Sacrificar a postura para fazer mais repetições.</strong> Menos repetições bem feitas valem mais.</li>
  <li><strong>Desistir na segunda semana.</strong> Os primeiros resultados que você sente são de força e fôlego, e aparecem com constância.</li>
</ul>

<h2>Alimentação e suplementos</h2>
<p>O treino rende mais com o básico em dia: refeições com proteína (ovos, carnes, feijão, laticínios), frutas e verduras, e água ao longo do dia. Dormir bem também conta.</p>
<p>Suplemento é opcional e vem depois do básico. Para quem já treina com intensidade, a creatina é um dos mais estudados: com pelo menos 3 g por dia, ela ajuda no desempenho em exercícios repetidos de curta duração e alta intensidade. Ela existe em pó e em goma; <a href="creatina.html">veja a diferença entre os dois formatos</a>.</p>
""" + CTA_CREATINA_CALISTENIA + AVISO_CALISTENIA,
    faq=[
        ("Calistenia emagrece?",
         "O treino gasta energia e ajuda, mas o emagrecimento depende principalmente da alimentação e da constância ao longo de meses. A calistenia é uma boa forma de se manter ativo junto com uma alimentação equilibrada."),
        ("Quantas vezes por semana devo treinar no começo?",
         "Três vezes por semana, com um dia de descanso entre os treinos. Depois de algumas semanas, dá para passar para quatro."),
        ("Preciso de barra fixa para começar?",
         "Não. Os seis exercícios básicos deste guia não usam nenhum equipamento. A barra fixa entra depois, para treinar as costas."),
        ("Em quanto tempo vejo resultado?",
         "Força e fôlego costumam melhorar nas primeiras semanas de treino regular. Mudanças no corpo levam mais tempo e variam de pessoa para pessoa."),
        ("Posso fazer calistenia todos os dias?",
         "No começo, não é recomendado. Os músculos precisam de descanso para se recuperar e ficar mais fortes."),
    ],
))

CTA_CREATINA = """
<div class="blog-cta">
  <p class="blog-cta-titulo">Creatina em pó ou em goma?</p>
  <p>A Velmora tem as duas: o CreaGym, em pó, nos sabores Morango e Tangerina, e a Creatina Gummy, com 3 g de creatina por porção. Compare formato, ingredientes e preço por mês.</p>
  <a class="btn btn-primary" href="creatina.html">Ver a comparação</a>
</div>
"""

AVISO_CREATINA = """<div class="loja-aviso"><strong>Importante:</strong> Este texto é informativo e não substitui a orientação de um nutricionista ou médico. Creatina não é medicamento e não é indicada para gestantes, lactantes e crianças. Pessoas com doença nos rins devem consultar um profissional de saúde antes de usar. Siga sempre a porção indicada no rótulo.</div>"""

POSTS.append(dict(
    slug="como-tomar-creatina",
    curto="Como tomar creatina",
    title="Como tomar creatina: quantidade por dia, como misturar e por quanto tempo | Velmo Drink",
    h1="Como tomar creatina: quantidade, como misturar e por quanto tempo",
    desc="Como tomar creatina do jeito certo: quantos gramas por dia, com o que misturar, se precisa tomar nos dias sem treino, se precisa fazer pausa e quando aparecem os efeitos.",
    categoria="Creatina",
    data="2026-10-15",
    resumo="Quantos gramas por dia, com o que misturar, se precisa tomar nos dias sem treino e se precisa fazer pausa.",
    corpo="""
<p>Tomar creatina é simples: uma porção por dia, todos os dias. Mas algumas dúvidas aparecem sempre: quantos gramas, com o que misturar, se precisa tomar nos dias sem treino, se precisa fazer pausa. Este guia responde cada uma.</p>

<h2>Resumo rápido</h2>
<ul>
  <li><strong>Quantidade:</strong> a porção do rótulo. No Brasil, os rótulos costumam indicar 3 g por dia.</li>
  <li><strong>Frequência:</strong> todos os dias, inclusive nos dias sem treino.</li>
  <li><strong>Horário:</strong> o que você conseguir manter. A constância importa mais do que a hora.</li>
  <li><strong>Com o quê:</strong> água, suco, vitamina ou shake. Ou mastigando, se for em goma.</li>
  <li><strong>Pausa:</strong> não é necessária.</li>
</ul>

<h2>Quantos gramas de creatina por dia?</h2>
<p>A creatina funciona por acúmulo: o corpo guarda creatina nos músculos, e a porção diária vai enchendo esse estoque. Os estudos usam, em geral, de 3 a 5 g por dia para adultos.</p>
<p>No Brasil, a Anvisa reconhece que a creatina ajuda no desempenho físico em exercícios repetidos de curta duração e alta intensidade quando a porção diária tem <strong>pelo menos 3 g</strong>. Por isso a maioria dos rótulos indica 3 g. Siga a porção do rótulo do seu produto.</p>

<h3>E a fase de saturação?</h3>
<p>Alguns estudos usam uma "fase de saturação": cerca de 20 g por dia, divididos em várias doses, por 5 a 7 dias, para encher o estoque mais rápido. Ela não é obrigatória. Com a porção diária normal, o estoque também enche; só leva algumas semanas a mais. Para quem está começando, o caminho mais simples e seguro é tomar a porção do rótulo desde o primeiro dia.</p>

<h2>Precisa tomar nos dias sem treino?</h2>
<p>Sim. Como o efeito vem do estoque acumulado no músculo, parar nos dias de descanso faz esse estoque baixar. Tome a mesma porção todos os dias, treinando ou não.</p>

<h2>Com o que misturar a creatina em pó</h2>
<ul>
  <li><strong>Água</strong> é a opção mais simples. A creatina pura não tem sabor; a creatina com sabor fica parecida com um refresco.</li>
  <li><strong>Suco, vitamina ou shake</strong> também servem. Algumas pesquisas sugerem que tomar junto com uma refeição ajuda o músculo a absorver, mas isso não é obrigatório.</li>
  <li><strong>Prepare e tome na hora.</strong> Misturada em líquido, a creatina vai se degradando aos poucos; não deixe pronta de um dia para o outro.</li>
  <li><strong>Mexa bem.</strong> A creatina não se dissolve por completo, e é normal sobrar um pouco no fundo do copo. Coloque mais um pouco de líquido e tome o resto.</li>
</ul>
<p>Se você não quer misturar nada, existe creatina em goma, que é só mastigar. Explicamos as diferenças em <a href="creatina-com-sabor-e-em-goma.html">creatina com sabor e em goma funcionam?</a></p>

<h2>Qual o melhor horário?</h2>
<p>A diferença entre tomar antes ou depois do treino é pequena nos estudos. O mais importante é tomar todos os dias. Explicamos com detalhes em <a href="melhor-horario-para-tomar-creatina.html">qual o melhor horário para tomar creatina</a>.</p>

<h2>Precisa fazer pausa (ciclar)?</h2>
<p>Não há evidência de que pausas sejam necessárias. Pessoas saudáveis usam creatina de forma contínua por meses nos estudos. Se você parar, o estoque no músculo volta ao normal em algumas semanas.</p>

<h2>Em quanto tempo a creatina faz efeito?</h2>
<p>Com a porção diária normal, o estoque muscular costuma ficar cheio em cerca de 3 a 4 semanas. A partir daí, a diferença aparece no treino: mais repetições em exercícios intensos e curtos, como musculação, tiros de corrida e calistenia.</p>
<p>Creatina não faz efeito na hora, como cafeína, e não substitui treino nem alimentação.</p>

<h2>A creatina incha ou engorda?</h2>
<p>No começo, algumas pessoas ganham de 1 a 2 kg na balança. É água que a creatina leva para dentro do músculo, não gordura. A creatina não tem calorias relevantes na porção diária.</p>

<h2>Erros comuns</h2>
<ul>
  <li><strong>Tomar só nos dias de treino.</strong> O estoque baixa e o efeito diminui.</li>
  <li><strong>Tomar mais do que o rótulo</strong> achando que funciona mais rápido. O excesso é eliminado na urina.</li>
  <li><strong>Desistir na segunda semana</strong> antes do estoque encher.</li>
  <li><strong>Esquecer de beber água</strong> ao longo do dia, principalmente em dias de treino.</li>
</ul>
""" + CTA_CREATINA + AVISO_CREATINA,
    faq=[
        ("Quantos gramas de creatina devo tomar por dia?",
         "Siga a porção do rótulo. No Brasil, os rótulos costumam indicar 3 g por dia, que é a quantidade mínima para a alegação de desempenho reconhecida pela Anvisa."),
        ("Preciso tomar creatina nos dias sem treino?",
         "Sim. A creatina funciona pelo estoque acumulado no músculo, e esse estoque baixa se você parar nos dias de descanso."),
        ("Posso misturar creatina com whey?",
         "Pode. Creatina pode ser misturada com whey, suco, vitamina ou água. Prepare e tome na hora."),
        ("Precisa fazer pausa no uso de creatina?",
         "Não há evidência de que pausas sejam necessárias para pessoas saudáveis."),
        ("Em quanto tempo a creatina faz efeito?",
         "Com a porção diária normal, o estoque no músculo costuma encher em 3 a 4 semanas. O efeito aparece no desempenho em exercícios curtos e intensos."),
    ],
))

POSTS.append(dict(
    slug="melhor-horario-para-tomar-creatina",
    curto="Melhor horário para tomar creatina",
    title="Qual o melhor horário para tomar creatina? Antes, depois do treino ou à noite | Velmo Drink",
    h1="Qual o melhor horário para tomar creatina?",
    desc="Antes ou depois do treino? Pode tomar creatina à noite, antes de dormir? Veja o que os estudos dizem sobre o melhor horário e como não esquecer a dose.",
    categoria="Creatina",
    data="2026-10-15",
    resumo="Antes ou depois do treino, de manhã ou antes de dormir: o que os estudos dizem e o que realmente importa.",
    corpo="""
<p>Resposta curta: <strong>o melhor horário para tomar creatina é aquele em que você não esquece</strong>. A creatina funciona pelo estoque que se acumula no músculo ao longo das semanas, e não por um efeito na hora. Por isso, tomar todos os dias importa muito mais do que o horário.</p>
<p>Mesmo assim, há detalhes que ajudam a escolher.</p>

<h2>Antes ou depois do treino?</h2>
<p>Os estudos que compararam os dois momentos encontraram diferenças pequenas. Alguns sugerem uma leve vantagem em tomar <strong>perto do treino, principalmente depois</strong>, quando o músculo está mais receptivo a nutrientes. Outros não encontraram diferença.</p>
<p>Na prática:</p>
<ul>
  <li><strong>Se você treina sempre no mesmo horário</strong>, tome logo depois do treino, junto com a refeição ou o shake.</li>
  <li><strong>Se o seu horário de treino muda</strong>, escolha um horário fixo do dia, como o café da manhã.</li>
</ul>

<h2>Pode tomar creatina antes de dormir?</h2>
<p>Pode. A creatina não é estimulante, não tem cafeína e não costuma atrapalhar o sono. Se a noite é o momento em que você lembra, tome à noite.</p>
<p>A exceção são os pré-treinos que misturam creatina com cafeína. Esses, sim, podem tirar o sono; leia o rótulo.</p>

<h2>De manhã, em jejum?</h2>
<p>Também pode. Algumas pessoas sentem desconforto no estômago ao tomar em jejum; se for o seu caso, tome junto com uma refeição. Comer junto pode até ajudar o músculo a absorver a creatina.</p>

<h2>E nos dias sem treino?</h2>
<p>Tome a mesma porção, no horário que for mais fácil. O importante é não pular dias. Veja mais em <a href="como-tomar-creatina.html">como tomar creatina</a>.</p>

<h2>Como não esquecer a dose</h2>
<ul>
  <li><strong>Junte a creatina a algo que você já faz todo dia</strong>: café da manhã, almoço, o shake pós-treino.</li>
  <li><strong>Deixe o pote à vista</strong>, perto da cafeteira ou da garrafa de água.</li>
  <li><strong>Tenha uma opção para levar</strong>: a creatina em goma cabe na bolsa e não precisa de água nem de coqueteleira.</li>
</ul>

<h2>Tabela rápida</h2>
<div class="precos-wrap">
  <table class="precos">
    <thead><tr><th>Sua rotina</th><th>Melhor momento</th></tr></thead>
    <tbody>
      <tr><td>Treina sempre no mesmo horário</td><td>Logo depois do treino</td></tr>
      <tr><td>Horário de treino varia</td><td>Café da manhã ou almoço</td></tr>
      <tr><td>Esquece tudo de manhã</td><td>Jantar ou antes de dormir</td></tr>
      <tr><td>Passa o dia fora de casa</td><td>Creatina em goma, em qualquer refeição</td></tr>
    </tbody>
  </table>
</div>
""" + CTA_CREATINA + AVISO_CREATINA,
    faq=[
        ("Qual o melhor horário para tomar creatina?",
         "O horário em que você consegue tomar todos os dias. Os estudos mostram diferenças pequenas entre os horários, com leve vantagem para tomar perto do treino, principalmente depois."),
        ("Posso tomar creatina antes de dormir?",
         "Pode. A creatina não é estimulante e não costuma atrapalhar o sono. Só evite produtos que misturam creatina com cafeína."),
        ("Creatina antes ou depois do treino?",
         "Depois do treino tem leve vantagem em alguns estudos, mas a diferença é pequena. Se o seu horário de treino muda, escolha um horário fixo do dia."),
        ("Posso tomar creatina em jejum?",
         "Pode, mas algumas pessoas sentem desconforto no estômago. Nesse caso, tome junto com uma refeição."),
    ],
))

POSTS.append(dict(
    slug="creatina-com-sabor-e-em-goma",
    curto="Creatina com sabor e em goma",
    title="Creatina com sabor e creatina em goma funcionam? Diferenças e cuidados | Velmo Drink",
    h1="Creatina com sabor e creatina em goma funcionam?",
    desc="Creatina com sabor e em goma funcionam igual à creatina pura? Veja a diferença entre pó puro, pó com sabor, goma e cápsula, e o que conferir no rótulo antes de comprar.",
    categoria="Creatina",
    data="2026-10-15",
    resumo="Pó puro, pó com sabor, goma ou cápsula: o que muda, o que não muda e o que conferir no rótulo antes de comprar.",
    corpo="""
<p>A creatina mais estudada é a <strong>creatina monohidratada</strong>, normalmente vendida como pó sem sabor. Hoje ela também aparece com sabor, em goma e em cápsula. A pergunta é: funciona igual?</p>
<p>A resposta curta: <strong>sim, desde que cada porção entregue a quantidade de creatina indicada</strong>. O formato muda a praticidade e o preço, não o efeito da creatina.</p>

<h2>O que muda entre os formatos</h2>
<div class="precos-wrap">
  <table class="precos comparacao">
    <thead><tr><th></th><th>Como toma</th><th>Prós</th><th>Contras</th></tr></thead>
    <tbody>
      <tr><th scope="row">Pó sem sabor</th><td>Misturado em água ou shake</td><td>Mais barato por dose</td><td>Textura arenosa, precisa preparar</td></tr>
      <tr><th scope="row">Pó com sabor</th><td>Misturado em água, como refresco</td><td>Mais gostoso de tomar só com água</td><td>Porção maior por causa do aroma e do adoçante</td></tr>
      <tr><th scope="row">Goma</th><td>Mastigando</td><td>Não precisa de água, fácil de levar</td><td>Custa mais por dose</td></tr>
      <tr><th scope="row">Cápsula</th><td>Engolindo com água</td><td>Sem sabor, fácil de levar</td><td>Várias cápsulas para chegar a 3 g</td></tr>
    </tbody>
  </table>
</div>

<h2>Creatina com sabor funciona?</h2>
<p>Funciona. A creatina com sabor é a mesma creatina monohidratada, com aroma e adoçante para ficar parecida com um refresco. É uma boa opção para quem não gosta de misturar a creatina pura no shake e prefere tomar só com água.</p>
<p>O ponto de atenção é a porção: como o pó tem outros ingredientes, a colher é maior. Confira no rótulo <strong>quantos gramas de creatina</strong> há em cada porção, e não só o peso da colher.</p>

<h2>Creatina em goma funciona?</h2>
<p>Funciona, desde que a porção diária tenha a quantidade de creatina indicada, normalmente 3 g. A goma é o formato mais prático: basta mastigar, sem água nem coqueteleira, o que ajuda quem passa o dia fora de casa ou sempre esquece a dose.</p>
<p>Por outro lado, a goma é um formato mais difícil de fabricar do que o pó, e cada goma carrega pouca creatina. Por isso, vale ainda mais atenção ao rótulo:</p>
<ul>
  <li><strong>Gramas de creatina por porção</strong> e quantas gomas formam essa porção.</li>
  <li><strong>Tipo de creatina</strong>: monohidratada é a mais estudada.</li>
  <li><strong>Açúcar</strong>: há gomas com açúcar e gomas sem açúcar.</li>
  <li><strong>Marca conhecida e informações claras</strong> sobre fabricante e lote.</li>
</ul>

<h2>Então, qual escolher?</h2>
<ul>
  <li><strong>Quer gastar menos</strong> e não se importa em preparar: pó.</li>
  <li><strong>Não gosta do gosto da creatina pura</strong>: pó com sabor.</li>
  <li><strong>Quer praticidade</strong> ou vive esquecendo: goma.</li>
</ul>
<p>Qualquer que seja o formato, o que faz a creatina funcionar é tomar a porção certa todos os dias. Veja <a href="como-tomar-creatina.html">como tomar creatina</a> e <a href="melhor-horario-para-tomar-creatina.html">qual o melhor horário</a>.</p>
""" + CTA_CREATINA + AVISO_CREATINA,
    faq=[
        ("Creatina em goma funciona?",
         "Funciona, desde que a porção diária tenha a quantidade de creatina indicada, normalmente 3 g. Confira no rótulo quantos gramas de creatina há por porção e quantas gomas formam essa porção."),
        ("Creatina com sabor é pior que a pura?",
         "Não. É a mesma creatina monohidratada com aroma e adoçante. Só confira no rótulo quantos gramas de creatina há em cada porção."),
        ("Creatina em cápsula ou em pó: qual é melhor?",
         "As duas funcionam. O pó costuma sair mais barato por dose; a cápsula é mais prática, mas pode exigir várias unidades para chegar a 3 g."),
        ("Quantas gomas de creatina por dia?",
         "Depende da marca. Siga a porção do rótulo, que deve informar quantas gomas somam a quantidade diária de creatina."),
    ],
))

# ---- Fila: 2 posts por semana (terça e sexta). Um post só pode linkar posts com data igual ou anterior à dele.

POSTS.append(dict(
    slug="para-que-serve-a-creatina",
    curto="Para que serve a creatina",
    title="Para que serve a creatina? O que é e o que ela faz no corpo | Velmo Drink",
    h1="Para que serve a creatina? O que é e o que ela faz no corpo",
    desc="O que é creatina, de onde ela vem, o que faz no músculo e para quem ela é indicada. Veja o que a ciência confirma e o que é exagero.",
    categoria="Creatina",
    data="2026-10-20",
    resumo="O que é creatina, o que ela faz no músculo, para quem serve e o que é exagero.",
    corpo="""
<p>A creatina é um dos suplementos mais estudados do mundo. Mesmo assim, ainda há muita confusão: tem gente que acha que é hormônio, que é remédio, que emagrece ou que faz ganhar músculo sozinha. Nada disso. Veja o que ela é e para que serve de verdade.</p>

<h2>O que é creatina?</h2>
<p>Creatina é uma substância que o próprio corpo produz, a partir de três aminoácidos (arginina, glicina e metionina). O fígado, os rins e o pâncreas fabricam cerca de 1 g por dia. A alimentação traz mais um pouco: carnes e peixes são as principais fontes.</p>
<p>Quase toda a creatina do corpo, cerca de 95%, fica guardada nos músculos. Não é hormônio, não é anabolizante e não é medicamento. O suplemento é a mesma substância, produzida em fábrica, em pó ou em goma.</p>

<h2>O que a creatina faz no músculo?</h2>
<p>Em esforços curtos e fortes, como levantar um peso, subir uma escada correndo ou fazer uma série de flexões, o músculo gasta muito rápido a sua energia imediata (o ATP). A creatina, guardada no músculo como fosfocreatina, ajuda a repor essa energia em poucos segundos.</p>
<p>Com mais creatina guardada, o músculo aguenta um pouco mais nesses esforços. Na prática, isso aparece como uma ou duas repetições a mais por série, ou um tiro de corrida um pouco mais forte.</p>

<h2>Para que serve, então?</h2>
<p>No Brasil, a Anvisa reconhece uma alegação para a creatina: ela <strong>auxilia no desempenho físico em exercícios repetidos de curta duração e alta intensidade</strong>, quando a porção diária tem pelo menos 3 g. Isso vale para quem pratica musculação, calistenia, crossfit, futebol, lutas e tiros de corrida.</p>
<p>O ganho de músculo vem do treino. A creatina ajuda você a treinar um pouco melhor, e é esse treino, somado a alimentação e descanso, que traz o resultado ao longo dos meses.</p>

<h2>O que a creatina não faz</h2>
<ul>
  <li><strong>Não emagrece.</strong> Ela não queima gordura. No começo, a balança pode até subir 1 a 2 kg, por causa da água que vai para dentro do músculo.</li>
  <li><strong>Não faz ganhar músculo sem treino.</strong> Sem o estímulo do exercício, o estoque extra não tem onde ser usado.</li>
  <li><strong>Não dá energia na hora.</strong> Ela não é estimulante como a cafeína. O efeito vem do estoque acumulado em semanas.</li>
</ul>

<h2>Quem pode se beneficiar</h2>
<ul>
  <li>Quem faz treino de força: musculação ou <a href="calistenia-para-iniciantes.html">calistenia em casa</a>.</li>
  <li>Quem pratica esportes com arrancadas e pausas, como futebol, vôlei e lutas.</li>
  <li>Quem come pouca carne ou peixe, que costuma ter menos creatina guardada no músculo.</li>
</ul>
<p>Para quem só caminha ou faz exercícios leves e longos, o efeito tende a ser pequeno.</p>

<h2>Como começar</h2>
<p>Tome a porção do rótulo todos os dias, inclusive nos dias sem treino, no horário que for mais fácil lembrar. O passo a passo está em <a href="como-tomar-creatina.html">como tomar creatina</a>, e as dúvidas sobre horário em <a href="melhor-horario-para-tomar-creatina.html">qual o melhor horário para tomar creatina</a>.</p>
""" + CTA_CREATINA + AVISO_CREATINA,
    faq=[
        ("Creatina é hormônio ou anabolizante?",
         "Não. Creatina é uma substância que o próprio corpo produz a partir de aminoácidos e que também vem da carne e do peixe. Não é hormônio nem anabolizante."),
        ("Creatina emagrece?",
         "Não. A creatina não queima gordura. No começo, o peso pode até subir um pouco por causa da água que vai para dentro do músculo."),
        ("Creatina faz ganhar massa muscular sozinha?",
         "Não. Ela ajuda no desempenho em exercícios curtos e intensos. O ganho de músculo vem do treino, da alimentação e do descanso."),
        ("Quem não treina pode tomar creatina?",
         "Pode, mas o benefício reconhecido é no desempenho em exercícios de alta intensidade. Sem treino, o efeito é pequeno."),
    ],
))

POSTS.append(dict(
    slug="creatina-monohidratada-ou-creapure",
    curto="Creatina monohidratada ou Creapure",
    title="Creatina monohidratada ou Creapure: qual a diferença? | Velmo Drink",
    h1="Creatina monohidratada ou Creapure: qual a diferença?",
    desc="Creapure é creatina monohidratada? Vale pagar mais? Entenda a diferença entre os tipos de creatina (monohidratada, Creapure, HCl, alcalina) e qual escolher.",
    categoria="Creatina",
    data="2026-10-23",
    resumo="Creapure é creatina monohidratada? Vale pagar mais? E os outros tipos, como HCl e alcalina?",
    corpo="""
<p>Na hora de comprar creatina aparecem vários nomes no rótulo: monohidratada, Creapure, HCl, alcalina, micronizada. Parece que são produtos muito diferentes, mas a maioria é a mesma coisa com nomes diferentes. Veja como separar o que importa do que é marketing.</p>

<h2>O que é creatina monohidratada</h2>
<p>É a forma mais comum de creatina: uma molécula de creatina ligada a uma molécula de água. É também a forma <strong>usada na grande maioria dos estudos</strong>, inclusive os que levaram a Anvisa a reconhecer o efeito no desempenho físico. Quando alguém diz que "a creatina funciona", está falando da monohidratada.</p>

<h2>E a Creapure?</h2>
<p>Creapure não é outro tipo de creatina. É uma <strong>marca de creatina monohidratada</strong>, fabricada na Alemanha pela empresa AlzChem. O que a marca vende é o controle de qualidade: processo de fabricação próprio e testes de pureza.</p>
<p>Ou seja: toda Creapure é creatina monohidratada, mas nem toda creatina monohidratada é Creapure. Os produtos que usam essa matéria-prima costumam trazer o selo Creapure na embalagem.</p>

<h3>Vale pagar mais pela Creapure?</h3>
<p>No efeito, não há diferença: a molécula é a mesma. O que você paga a mais é a garantia de origem da matéria-prima. Uma creatina monohidratada de outro fabricante, de uma empresa séria e com porção correta, funciona do mesmo jeito. Se o preço extra pesa no bolso, a regularidade (tomar todo dia) vale mais do que o selo.</p>

<h2>E os outros tipos?</h2>
<ul>
  <li><strong>Micronizada:</strong> é monohidratada moída em partículas menores. Dissolve um pouco melhor na água. O efeito é o mesmo.</li>
  <li><strong>Creatina HCl (cloridrato):</strong> dissolve melhor e costuma ser vendida em porções menores. Não há estudos suficientes mostrando que seja melhor que a monohidratada.</li>
  <li><strong>Creatina alcalina (tamponada):</strong> prometia menos perda no estômago. Os estudos que compararam não encontraram vantagem sobre a monohidratada.</li>
  <li><strong>Etil éster:</strong> nos estudos, se mostrou pior que a monohidratada.</li>
</ul>

<h2>Então qual escolher?</h2>
<p>A creatina monohidratada continua sendo a escolha com mais evidência e, em geral, a de melhor preço por porção. Na embalagem, confira:</p>
<ol>
  <li>Se o ingrediente é <strong>creatina monohidratada</strong>.</li>
  <li>Se a porção diária tem <strong>pelo menos 3 g de creatina</strong>.</li>
  <li>O preço por porção, e não só o preço do pote.</li>
</ol>
<p>A forma de tomar também conta: tem gente que prefere pó com sabor e tem gente que prefere goma. Comparamos as duas em <a href="creatina-com-sabor-e-em-goma.html">creatina com sabor e em goma funcionam?</a> e o uso diário em <a href="como-tomar-creatina.html">como tomar creatina</a>.</p>
""" + CTA_CREATINA + AVISO_CREATINA,
    faq=[
        ("Creapure é creatina monohidratada?",
         "Sim. Creapure é uma marca de creatina monohidratada fabricada na Alemanha. Não é outro tipo de creatina."),
        ("Creapure funciona melhor que outra creatina monohidratada?",
         "Não há diferença no efeito, porque a molécula é a mesma. A diferença está na origem e no controle de qualidade da matéria-prima."),
        ("Creatina HCl é melhor que a monohidratada?",
         "Não há estudos suficientes mostrando isso. A monohidratada é a forma mais estudada."),
        ("O que é creatina micronizada?",
         "É creatina monohidratada moída em partículas menores, para dissolver melhor. O efeito é o mesmo."),
    ],
))

POSTS.append(dict(
    slug="quem-nao-pode-tomar-creatina",
    curto="Quem não pode tomar creatina",
    title="Quem não pode tomar creatina? Rins, efeitos colaterais e cuidados | Velmo Drink",
    h1="Quem não pode tomar creatina? Rins, efeitos colaterais e cuidados",
    desc="Creatina faz mal para os rins? Dá câncer? Faz cair cabelo? Veja quem não deve tomar creatina, os efeitos colaterais mais comuns e quando falar com um médico.",
    categoria="Creatina",
    data="2026-11-03",
    resumo="Rins, câncer, queda de cabelo e efeitos colaterais: o que os estudos dizem e quem deve evitar.",
    corpo="""
<p>A creatina é considerada segura para adultos saudáveis na porção indicada no rótulo. Mas isso não quer dizer que ela sirva para todo mundo. Veja quem não deve tomar, quem precisa de orientação antes e o que é verdade sobre os efeitos colaterais mais falados.</p>

<h2>Quem não deve tomar creatina</h2>
<ul>
  <li><strong>Gestantes e lactantes.</strong> Os rótulos de creatina trazem esse aviso: não deve ser consumida durante a gravidez nem na amamentação.</li>
  <li><strong>Crianças.</strong> O suplemento é indicado para adultos. A Creatina Gummy, por exemplo, indica consumo para maiores de 19 anos.</li>
</ul>

<h2>Quem deve falar com um médico antes</h2>
<ul>
  <li>Pessoas com <strong>doença nos rins</strong> ou que já tiveram problema renal.</li>
  <li>Pessoas com <strong>diabetes ou pressão alta</strong>, condições que podem afetar os rins.</li>
  <li>Quem usa <strong>remédios de uso contínuo</strong>, principalmente os que agem nos rins.</li>
  <li>Quem <strong>tem ou teve câncer</strong> e está em tratamento ou acompanhamento.</li>
</ul>

<h2>Creatina faz mal para os rins?</h2>
<p>Em pessoas saudáveis, os estudos com uso por meses e até anos, na porção recomendada, não encontraram dano aos rins.</p>
<p>A confusão vem de um exame: a <strong>creatinina</strong>. Ela é um resíduo da creatina, e o médico usa a creatinina no sangue para avaliar os rins. Quem toma creatina pode ter a creatinina um pouco mais alta sem que os rins tenham problema. Por isso, <strong>avise o médico que você toma creatina</strong> antes de fazer exames de sangue.</p>
<p>Para quem já tem doença nos rins, a recomendação é outra: não tome sem orientação médica.</p>

<h2>Creatina dá câncer?</h2>
<p>Até hoje, os estudos em pessoas não mostraram que a creatina cause câncer. A dúvida surgiu de hipóteses de laboratório e de pesquisas que juntavam vários suplementos diferentes na mesma análise. Quem tem ou teve câncer deve decidir junto com o médico que acompanha o tratamento.</p>

<h2>Creatina faz cair cabelo?</h2>
<p>Essa ideia vem de um único estudo pequeno, de 2009, que mediu um aumento de um hormônio (DHT) em jogadores de rúgbi. O estudo não avaliou queda de cabelo, e pesquisas mais recentes não confirmaram o resultado. Não há evidência de que a creatina cause calvície.</p>

<h2>Efeitos colaterais mais comuns</h2>
<ul>
  <li><strong>Peso na balança:</strong> 1 a 2 kg nas primeiras semanas, por causa da água dentro do músculo. Não é gordura.</li>
  <li><strong>Desconforto no estômago:</strong> mais comum quando a pessoa toma doses grandes de uma vez. Na porção do rótulo, é raro.</li>
  <li><strong>Sede:</strong> beba água ao longo do dia, principalmente nos dias de treino.</li>
</ul>
<p>Se aparecer qualquer reação diferente, pare de tomar e procure um profissional de saúde.</p>

<h2>Como usar com segurança</h2>
<ol>
  <li>Tome só a porção indicada no rótulo. Mais do que isso não traz benefício.</li>
  <li>Prefira produtos de empresas identificadas, com rótulo completo e lote.</li>
  <li>Avise seu médico antes de exames de sangue.</li>
</ol>
<p>Para o uso no dia a dia, veja <a href="como-tomar-creatina.html">como tomar creatina</a> e <a href="para-que-serve-a-creatina.html">para que serve a creatina</a>.</p>
""" + CTA_CREATINA + AVISO_CREATINA,
    faq=[
        ("Creatina faz mal para os rins?",
         "Em pessoas saudáveis, os estudos com a porção recomendada não encontraram dano aos rins. Quem tem doença renal deve consultar um médico antes."),
        ("Por que a creatinina sobe quando tomo creatina?",
         "A creatinina é um resíduo da creatina. Ela pode subir um pouco no exame de sangue sem que haja problema nos rins. Avise o médico que você usa creatina."),
        ("Gestante pode tomar creatina?",
         "Não. Os rótulos de creatina indicam que ela não deve ser consumida por gestantes, lactantes e crianças."),
        ("Creatina faz cair cabelo?",
         "Não há evidência disso. A ideia vem de um estudo pequeno de 2009 que não avaliou queda de cabelo e não foi confirmado depois."),
        ("Creatina dá câncer?",
         "Os estudos em pessoas não mostraram que a creatina cause câncer. Quem tem ou teve câncer deve conversar com o médico antes de usar."),
    ],
))

POSTS.append(dict(
    slug="como-escolher-creatina",
    curto="Como escolher uma creatina",
    title="Como escolher uma creatina boa: o que olhar no rótulo | Velmo Drink",
    h1="Como escolher uma creatina boa: o que olhar no rótulo",
    desc="Qual a melhor creatina? Em vez de ranking de marcas, veja o que conferir no rótulo: tipo de creatina, porção, ingredientes, preço por dose e sinais de alerta.",
    categoria="Creatina",
    data="2026-11-06",
    resumo="Tipo de creatina, porção, ingredientes, preço por dose e sinais de alerta no rótulo.",
    corpo="""
<p>"Qual a melhor marca de creatina?" é uma das buscas mais comuns sobre o assunto. Aqui não vamos fazer ranking de marcas: preço e lote mudam o tempo todo, e o que vale para um pote pode não valer para o próximo. Em vez disso, mostramos <strong>o que olhar no rótulo</strong> para escolher qualquer creatina com segurança.</p>
<p><em>Transparência:</em> este site é de um afiliado e indica produtos da Velmora, que tem creatina em pó e em goma. Use o mesmo checklist para avaliar esses produtos e os de qualquer outra marca.</p>

<h2>1. O tipo de creatina</h2>
<p>Procure <strong>creatina monohidratada</strong> na lista de ingredientes. É a forma mais estudada e a que tem o efeito reconhecido. Outros tipos (HCl, alcalina) não mostraram vantagem nos estudos. Explicamos em <a href="creatina-monohidratada-ou-creapure.html">creatina monohidratada ou Creapure</a>.</p>

<h2>2. A quantidade por porção</h2>
<p>Confira na tabela nutricional quantos gramas de creatina há em cada porção. Para a alegação reconhecida pela Anvisa (desempenho em exercícios curtos e intensos), a porção diária precisa ter <strong>pelo menos 3 g de creatina</strong>.</p>
<p>Atenção nos produtos com sabor e nas gomas: a porção pesa mais que 3 g porque tem outros ingredientes. O que conta é a linha "creatina" da tabela, não o peso da porção.</p>

<h2>3. Os outros ingredientes</h2>
<ul>
  <li><strong>Creatina pura:</strong> só creatina. Sem sabor, mistura em qualquer bebida.</li>
  <li><strong>Com sabor:</strong> tem aroma, acidulante e adoçante. Veja quais adoçantes, se você evita algum.</li>
  <li><strong>Em goma:</strong> tem também gelificante e, às vezes, açúcar. Algumas usam polióis (como eritritol) no lugar do açúcar.</li>
</ul>

<h2>4. O preço por porção</h2>
<p>Compare o preço de cada dose, e não o do pote. A conta é simples: preço do pote dividido pelo número de porções. Um pote mais barato com poucas porções pode sair mais caro no mês.</p>

<h2>5. Quem fabrica</h2>
<p>O rótulo deve trazer o nome da empresa, CNPJ, endereço, lote, validade e um canal de atendimento. Desconfie de produtos sem essas informações.</p>

<h2>Sinais de alerta</h2>
<ul>
  <li>Promessas como <strong>"ganhe X kg de músculo"</strong>, "emagrece" ou "resultado sem treino". Creatina não faz isso, e essas frases não são permitidas pela Anvisa.</li>
  <li>Porção diária com <strong>menos de 3 g</strong> de creatina, ou sem dizer quanto tem.</li>
  <li>Preço muito abaixo do mercado, sem empresa identificada.</li>
  <li>Mistura de creatina com estimulantes sem informar a quantidade de cada ingrediente.</li>
</ul>

<h2>Resumo</h2>
<p>A melhor creatina para você é uma monohidratada, com pelo menos 3 g por porção, de uma empresa identificada, num formato que você consiga tomar todos os dias e com preço por porção que caiba no orçamento. Constância vale mais que marca. Veja também <a href="quem-nao-pode-tomar-creatina.html">quem não pode tomar creatina</a>.</p>
""" + CTA_CREATINA + AVISO_CREATINA,
    faq=[
        ("Qual a melhor marca de creatina?",
         "Não existe uma única resposta. Escolha uma creatina monohidratada, com pelo menos 3 g por porção, de uma empresa identificada no rótulo e com bom preço por porção."),
        ("Como calcular o preço por porção da creatina?",
         "Divida o preço do pote pelo número de porções informado no rótulo."),
        ("Creatina com sabor é pior que a pura?",
         "Não, se a porção tiver pelo menos 3 g de creatina. Ela só tem ingredientes a mais para dar sabor."),
        ("Desconfiar de creatina que promete ganho de massa?",
         "Sim. A alegação permitida é de desempenho em exercícios curtos e intensos. Promessas de quilos de músculo ou emagrecimento são sinal de alerta."),
    ],
))

POSTS.append(dict(
    slug="creatina-para-mulher",
    curto="Creatina para mulher",
    title="Creatina para mulher: funciona, engorda ou incha? | Velmo Drink",
    h1="Creatina para mulher: funciona, engorda ou incha?",
    desc="Mulher pode tomar creatina? Engorda, incha ou deixa o corpo masculino? Veja o que os estudos dizem, a dose e quem deve evitar.",
    categoria="Creatina",
    data="2026-11-10",
    resumo="Funciona do mesmo jeito? Engorda, incha ou deixa o corpo masculino? O que os estudos dizem.",
    corpo="""
<p>Muitas mulheres evitam a creatina com medo de inchar, engordar ou "ficar com corpo masculino". Esses medos fazem sentido para quem nunca ouviu uma explicação clara. Veja o que os estudos mostram.</p>

<h2>Creatina funciona para mulheres?</h2>
<p>Sim. A creatina age da mesma forma no músculo de homens e mulheres: aumenta o estoque de energia rápida usado em esforços curtos e fortes. Estudos com mulheres que fazem treino de força mostram o mesmo tipo de benefício no desempenho.</p>
<p>As mulheres costumam ter menos creatina guardada no músculo e consumir menos carne, por isso podem perceber diferença no treino até com mais facilidade.</p>

<h2>Creatina deixa o corpo masculino?</h2>
<p>Não. Creatina não é hormônio e não altera hormônios femininos. O que muda o formato do corpo é o treino, e o ganho de músculo nas mulheres é mais lento por causa dos próprios hormônios. A creatina só ajuda a treinar um pouco melhor.</p>

<h2>Creatina engorda?</h2>
<p>Não engorda no sentido de ganhar gordura: na porção diária, ela não tem calorias relevantes. O que pode acontecer é a balança subir de 1 a 2 kg nas primeiras semanas. Esse peso é água que vai para dentro do músculo.</p>

<h2>Creatina incha?</h2>
<p>A água fica <strong>dentro do músculo</strong>, e não embaixo da pele. Por isso, a maioria das pessoas não percebe inchaço no rosto ou nas pernas. Quem sente diferença costuma notar só nas primeiras semanas. Se o inchaço incomodar, fale com um profissional de saúde.</p>

<h2>Qual a dose para mulheres?</h2>
<p>A mesma: a porção do rótulo, que costuma ser de 3 g por dia, todos os dias. Não é preciso fase de saturação. Os detalhes estão em <a href="como-tomar-creatina.html">como tomar creatina</a>.</p>

<h2>Creatina durante a menstruação ou na menopausa?</h2>
<p>Não há motivo para parar durante a menstruação; o efeito depende de tomar todos os dias. Sobre a menopausa, há pesquisas em andamento sobre força muscular nessa fase, mas ainda não há conclusões firmes. Converse com seu médico ou nutricionista.</p>

<h2>Quem não deve tomar</h2>
<p><strong>Gestantes e lactantes não devem consumir creatina.</strong> Mulheres com doença nos rins devem consultar um médico antes. Veja a lista completa em <a href="quem-nao-pode-tomar-creatina.html">quem não pode tomar creatina</a>.</p>

<h2>Pó ou goma?</h2>
<p>O efeito é o mesmo se a porção tiver pelo menos 3 g de creatina. A escolha é de praticidade e gosto. Para escolher com segurança, veja <a href="como-escolher-creatina.html">como escolher uma creatina boa</a>.</p>
""" + CTA_CREATINA + AVISO_CREATINA,
    faq=[
        ("Mulher pode tomar creatina?",
         "Pode. A creatina funciona da mesma forma em homens e mulheres. Gestantes e lactantes não devem consumir."),
        ("Creatina engorda mulher?",
         "Não causa ganho de gordura. A balança pode subir de 1 a 2 kg nas primeiras semanas por causa da água dentro do músculo."),
        ("Creatina deixa a mulher com corpo masculino?",
         "Não. Creatina não é hormônio e não altera os hormônios femininos."),
        ("Qual a dose de creatina para mulher?",
         "A mesma porção do rótulo, geralmente 3 g por dia, todos os dias."),
    ],
))

CTA_CLARIZE = """
<div class="blog-cta">
  <p class="blog-cta-titulo">Clarize, o clareador da Velmora</p>
  <p>Cosmético de uso externo para virilha, axilas e joelhos, com niacinamida, ácido hialurônico, lithothamnium e óleo de girassol ozonizado. Veja como usar, o prazo indicado pelo fabricante e os preços.</p>
  <a class="btn btn-primary" href="clarize.html">Conhecer o Clarize</a>
</div>
"""

AVISO_PELE = """<div class="loja-aviso"><strong>Importante:</strong> Este texto é informativo e não substitui a consulta com dermatologista ou ginecologista. Cosméticos não tratam doenças. Manchas que aparecem de repente, coçam, doem ou mudam a textura da pele precisam de avaliação médica. Não aplique clareadores em mucosas nem sobre pele ferida ou irritada.</div>"""

POSTS.append(dict(
    slug="virilha-escura-causas-e-como-clarear",
    curto="Virilha escura: causas e como clarear",
    title="Virilha escura: causas e como clarear com segurança | Velmo Drink",
    h1="Virilha escura: o que causa e como clarear com segurança",
    desc="Por que a virilha escurece, o que ajuda a clarear, quanto tempo leva, o que evitar (limão, bicarbonato) e quando a mancha precisa de médico.",
    categoria="Cuidados com a pele",
    data="2026-11-13",
    resumo="Atrito, depilação, hormônios: por que a virilha escurece, o que ajuda a clarear e quando procurar um médico.",
    corpo="""
<p>A virilha escura é uma das queixas de pele mais comuns, em mulheres e em homens. Na maioria das vezes, não é sujeira nem falta de cuidado: é a pele reagindo a atrito e irritação. Entender a causa é o primeiro passo para clarear e, principalmente, para a mancha não voltar.</p>

<h2>Resumo rápido</h2>
<ul>
  <li><strong>Causa mais comum:</strong> atrito e irritação (roupa apertada, coxas, depilação).</li>
  <li><strong>O que ajuda:</strong> reduzir o atrito, depilar com cuidado, hidratar e usar um clareador cosmético de forma contínua.</li>
  <li><strong>Tempo:</strong> semanas a meses. Não existe clareamento em poucos dias.</li>
  <li><strong>Evite:</strong> limão, bicarbonato, água oxigenada e cremes com corticoide sem receita.</li>
  <li><strong>Procure médico</strong> se a pele ficou grossa e aveludada, coça, dói ou escureceu de repente.</li>
</ul>

<h2>Por que a virilha escurece</h2>
<p>A cor da pele vem da melanina. Quando a pele é irritada várias vezes, ela produz mais melanina naquele ponto e escurece aos poucos. Na virilha, os principais motivos são:</p>
<ul>
  <li><strong>Atrito:</strong> coxas que se encostam ao andar, calcinha ou cueca apertada, calça jeans justa, costura que roça na pele.</li>
  <li><strong>Depilação:</strong> a lâmina raspa a camada de cima da pele e a cera puxa; as duas irritam. Pelos encravados também deixam manchas.</li>
  <li><strong>Suor e calor:</strong> a dobra da virilha fica abafada, o que favorece irritação e micoses.</li>
  <li><strong>Hormônios:</strong> gravidez, anticoncepcional e outras mudanças hormonais podem escurecer áreas como virilha, mamilos e axilas.</li>
  <li><strong>Resistência à insulina:</strong> pode causar a acantose nigricans, explicada abaixo.</li>
</ul>

<h2>Quando a virilha escura precisa de médico</h2>
<p>A <strong>acantose nigricans</strong> deixa a pele escura, mais grossa e com aspecto de veludo, geralmente no pescoço, nas axilas e na virilha. Ela costuma estar ligada à resistência à insulina, que pode evoluir para diabetes. Nesse caso, o clareador não resolve: é preciso tratar a causa com um médico.</p>
<p>Procure também avaliação se a mancha coça, descama, dói, tem borda bem marcada (pode ser micose) ou apareceu de repente.</p>

<h2>Como clarear a virilha</h2>
<h3>1. Corte a causa</h3>
<p>Prefira roupas íntimas de algodão e menos apertadas. Em dias quentes ou de caminhada longa, um short por baixo da saia ou um creme de barreira reduz o atrito entre as coxas. Sem isso, qualquer produto perde efeito, porque a pele continua sendo irritada.</p>
<h3>2. Depile com mais cuidado</h3>
<p>Se usa lâmina, use lâmina nova, sabonete ou gel por baixo e passe no sentido do pelo. Depilação a laser costuma irritar menos a longo prazo. Não aplique clareador logo depois de depilar.</p>
<h3>3. Hidrate</h3>
<p>Pele hidratada fica menos sensível ao atrito. Ingredientes como ácido hialurônico ajudam a manter a água na superfície da pele.</p>
<h3>4. Use um clareador cosmético com constância</h3>
<p>Os cosméticos para virilha costumam ter ativos como niacinamida, ácido kójico, alfa-arbutina ou vitamina C. Eles agem devagar: os primeiros sinais costumam aparecer depois de algumas semanas de uso diário, e o resultado completo leva meses. Aplique só na pele externa, nunca em mucosas.</p>

<h2>O que não fazer</h2>
<ul>
  <li><strong>Limão:</strong> com sol, pode causar queimadura e manchas ainda mais escuras (fitofotodermatose).</li>
  <li><strong>Bicarbonato, água oxigenada, pasta de dente:</strong> irritam a pele e, com isso, tendem a escurecer mais.</li>
  <li><strong>Esfoliar com força:</strong> o atrito é justamente a causa do problema.</li>
  <li><strong>Pomadas com corticoide ou hidroquinona por conta própria:</strong> só com receita e acompanhamento médico.</li>
</ul>

<h2>Quanto tempo leva para clarear</h2>
<p>A pele renova a camada de cima em cerca de um mês. Por isso, qualquer clareamento leva semanas para começar a aparecer e alguns meses para ficar visível. Fotos no mesmo lugar e com a mesma luz, a cada 15 dias, ajudam a perceber a evolução.</p>
""" + CTA_CLARIZE + AVISO_PELE,
    faq=[
        ("Por que a virilha fica escura?",
         "Na maioria das vezes, por atrito e irritação: roupa apertada, coxas que se encostam e depilação. Hormônios e resistência à insulina também podem escurecer a virilha."),
        ("Como clarear a virilha rápido?",
         "Não existe clareamento rápido e seguro. Reduzir o atrito, depilar com cuidado e usar um clareador cosmético todos os dias costuma mostrar os primeiros sinais em algumas semanas."),
        ("Limão clareia a virilha?",
         "Não é recomendado. Limão com exposição ao sol pode queimar a pele e deixar manchas mais escuras."),
        ("Quando a virilha escura é sinal de doença?",
         "Quando a pele fica grossa e aveludada, o que pode ser acantose nigricans, ligada à resistência à insulina. Também quando coça, descama ou aparece de repente. Nesses casos, procure um médico."),
    ],
))

POSTS.append(dict(
    slug="axilas-escuras-o-que-pode-ser",
    curto="Axilas escuras: o que pode ser e como clarear",
    title="Axilas escuras: o que pode ser e como clarear | Velmo Drink",
    h1="Axilas escuras: o que pode ser e como clarear",
    desc="Axilas escuras, o que pode ser: lâmina, desodorante, atrito ou acantose. Veja como clarear com segurança, quanto tempo leva e quando procurar médico.",
    categoria="Cuidados com a pele",
    data="2026-11-17",
    resumo="Depilação, desodorante e atrito: o que escurece as axilas e o que ajuda a clarear.",
    corpo="""
<p>A axila escura incomoda muita gente na hora de usar regata ou biquíni. A boa notícia é que, na maioria dos casos, a causa é a irritação do dia a dia, e dá para melhorar com mudanças simples e paciência.</p>

<h2>Por que as axilas escurecem</h2>
<ul>
  <li><strong>Lâmina:</strong> a depilação com lâmina raspa a pele e deixa a raiz do pelo escuro visível, o que dá aspecto acinzentado.</li>
  <li><strong>Pelos encravados e foliculite:</strong> cada inflamação deixa uma pequena mancha.</li>
  <li><strong>Desodorante ou antitranspirante:</strong> alguns causam irritação em peles sensíveis, principalmente os com álcool e perfume forte.</li>
  <li><strong>Atrito:</strong> roupa justa e movimento do braço.</li>
  <li><strong>Hormônios e resistência à insulina:</strong> como na virilha, a acantose nigricans também aparece nas axilas.</li>
</ul>
<p>Os mesmos mecanismos explicam a virilha escura. Se a sua dúvida também é essa região, veja <a href="virilha-escura-causas-e-como-clarear.html">virilha escura: o que causa e como clarear</a>.</p>

<h2>Como clarear as axilas</h2>
<h3>Troque ou pause a lâmina</h3>
<p>Se possível, prefira cera, depilador elétrico ou laser. Se continuar com lâmina, use lâmina nova, com gel ou sabonete, e no sentido do pelo.</p>
<h3>Revise o desodorante</h3>
<p>Se a axila arde ou fica vermelha depois de passar o desodorante, teste uma versão sem álcool e sem perfume. Não passe desodorante logo depois de depilar.</p>
<h3>Use um clareador cosmético todos os dias</h3>
<p>Aplique na pele limpa e seca, uma pequena quantidade, massageando até absorver. A niacinamida é um dos ativos com estudo publicado especificamente em axilas escuras.</p>
<h3>Hidrate e evite esfregar</h3>
<p>Esfoliar com bucha ou açúcar todos os dias irrita e pode escurecer mais. Esfoliação suave, no máximo uma vez por semana, é suficiente.</p>

<h2>O que evitar</h2>
<ul>
  <li>Limão, bicarbonato e água oxigenada.</li>
  <li>Pomadas com corticoide ou hidroquinona sem orientação médica.</li>
  <li>Aplicar clareador sobre pele ferida, com foliculite ou logo depois de depilar.</li>
</ul>

<h2>Em quanto tempo a axila clareia</h2>
<p>Os primeiros sinais costumam aparecer depois de 2 a 4 semanas de uso contínuo, e a melhora mais visível leva de 1 a 3 meses. Se a causa (lâmina, desodorante) continuar, a mancha volta.</p>

<h2>Quando procurar um médico</h2>
<p>Se a pele da axila ficou grossa, aveludada, com pequenas verrugas ao redor, ou se também há escurecimento no pescoço, procure um médico: pode ser acantose nigricans. Manchas que coçam ou descamam podem ser micose ou eritrasma, que têm tratamento específico.</p>
""" + CTA_CLARIZE + AVISO_PELE,
    faq=[
        ("Por que minha axila é escura?",
         "As causas mais comuns são a depilação com lâmina, pelos encravados, irritação pelo desodorante e atrito. Hormônios e resistência à insulina também podem escurecer as axilas."),
        ("Desodorante escurece a axila?",
         "Pode, em peles sensíveis. Desodorantes com álcool e perfume forte irritam, e a irritação repetida escurece a pele."),
        ("Em quanto tempo a axila clareia?",
         "Com cuidado diário, os primeiros sinais costumam aparecer em 2 a 4 semanas, e a melhora mais visível leva de 1 a 3 meses."),
        ("Bicarbonato clareia a axila?",
         "Não é recomendado. O bicarbonato irrita a pele, e a irritação tende a escurecer ainda mais."),
    ],
))

POSTS.append(dict(
    slug="niacinamida-clareia",
    curto="Niacinamida clareia?",
    title="Niacinamida clareia a pele? O que dizem os estudos | Velmo Drink",
    h1="Niacinamida clareia a pele? O que dizem os estudos",
    desc="O que é niacinamida, como ela age nas manchas, o estudo com niacinamida 4% nas axilas, em quanto tempo funciona e como usar na virilha e nas axilas.",
    categoria="Cuidados com a pele",
    data="2026-11-20",
    resumo="Como a vitamina B3 age nas manchas, o que o estudo com axilas mostrou e quanto tempo leva.",
    corpo="""
<p>A niacinamida aparece em séruns de rosto, cremes para manchas e clareadores de virilha e axila. Mas ela clareia mesmo? A resposta curta: ajuda a uniformizar o tom da pele, com efeito gradual, e tem estudos em pessoas.</p>

<h2>O que é niacinamida</h2>
<p>Niacinamida (ou nicotinamida) é uma forma da vitamina B3. Em cosméticos, ela é usada para manchas, oleosidade e para fortalecer a barreira da pele. É um ativo bem tolerado, que raramente irrita, por isso aparece em produtos para áreas sensíveis.</p>

<h2>Como ela age nas manchas</h2>
<p>A melanina é produzida por células chamadas melanócitos e depois é passada para as células da superfície da pele. A niacinamida <strong>reduz essa transferência</strong>. Ela não "descolore" a pele: faz com que menos pigmento chegue à superfície, e a mancha vai clareando conforme a pele se renova.</p>

<h2>O estudo com niacinamida nas axilas</h2>
<p>Um estudo publicado em 2013 na revista <em>Clinical, Cosmetic and Investigational Dermatology</em> testou um creme com niacinamida a 4% em pessoas com axilas escuras, comparando com um creme sem ativo (placebo) e com um corticoide leve. A niacinamida melhorou o escurecimento das axilas mais do que o placebo, sem efeitos colaterais importantes (<a href="https://pmc.ncbi.nlm.nih.gov/articles/PMC3552481/" target="_blank" rel="noopener">estudo completo, em inglês</a>).</p>
<p>Dois cuidados ao ler esse resultado: foi um estudo pequeno, e cada produto tem uma concentração diferente. Um cosmético com niacinamida não vai, necessariamente, ter o mesmo efeito do creme testado.</p>

<h2>Em quanto tempo funciona</h2>
<p>Como depende da renovação da pele, o efeito é lento. Os primeiros sinais costumam aparecer depois de 2 a 4 semanas de uso diário, e a melhora mais visível leva alguns meses. Parar no meio do caminho é o motivo mais comum de "não funcionou".</p>

<h2>Como usar na virilha e nas axilas</h2>
<ul>
  <li>Aplique na pele limpa e bem seca, em pequena quantidade.</li>
  <li>Use todos os dias, sempre na pele externa, nunca em mucosas.</li>
  <li>Não aplique logo depois de depilar.</li>
  <li>Corte a causa da mancha ao mesmo tempo: atrito, lâmina, desodorante irritante.</li>
</ul>
<p>Para entender as causas de cada região, veja <a href="virilha-escura-causas-e-como-clarear.html">virilha escura: causas e como clarear</a> e <a href="axilas-escuras-o-que-pode-ser.html">axilas escuras: o que pode ser</a>.</p>

<h2>Niacinamida tem efeito colateral?</h2>
<p>É um dos ativos mais suaves. Algumas pessoas sentem leve vermelhidão ou ardência no começo, principalmente em pele irritada. Se acontecer, suspenda e retome quando a pele acalmar. Faça sempre um teste em uma área pequena antes.</p>

<h2>Pode usar com outros ativos?</h2>
<p>Em geral, sim: a niacinamida combina bem com ácido hialurônico, que hidrata. Evite misturar vários clareadores fortes ao mesmo tempo na mesma área, porque isso aumenta a chance de irritação, e irritação escurece a pele.</p>
""" + CTA_CLARIZE + AVISO_PELE,
    faq=[
        ("Niacinamida clareia a virilha?",
         "Ajuda a uniformizar o tom da pele de forma gradual. Um estudo com niacinamida a 4% mostrou melhora do escurecimento nas axilas em comparação com placebo. Na virilha, o mecanismo é o mesmo."),
        ("Em quanto tempo a niacinamida faz efeito?",
         "Os primeiros sinais costumam aparecer em 2 a 4 semanas de uso diário, e a melhora mais visível leva alguns meses."),
        ("Niacinamida irrita a pele?",
         "Raramente. É um dos ativos mais bem tolerados, mas algumas pessoas sentem leve ardência no começo."),
        ("Posso usar niacinamida na região íntima?",
         "Só na pele externa, como virilha e axilas. Não aplique em mucosas."),
    ],
))

POSTS.append(dict(
    slug="clareamento-de-axilas-caseiro",
    curto="Clareamento de axilas caseiro",
    title="Clareamento de axilas caseiro: o que funciona e o que é mito | Velmo Drink",
    h1="Clareamento de axilas caseiro: o que funciona e o que é mito",
    desc="Leite de magnésia, bicarbonato, limão, açúcar, água oxigenada: veja quais receitas caseiras para clarear axilas e virilha são mito, quais irritam e o que funciona de verdade.",
    categoria="Cuidados com a pele",
    data="2026-11-24",
    resumo="Leite de magnésia, bicarbonato, limão: o que a receita caseira faz com a pele e o que funciona de verdade.",
    corpo="""
<p>Antes de comprar qualquer produto, muita gente procura uma receita caseira para clarear as axilas ou a virilha. Faz sentido: é barato e está na cozinha. O problema é que a maioria dessas receitas irrita a pele, e <strong>irritação é justamente o que escurece</strong> essas áreas. Veja receita por receita.</p>

<h2>Leite de magnésia clareia a axila?</h2>
<p>O leite de magnésia é usado por muita gente como desodorante, porque é alcalino e reduz as bactérias que causam o odor. Para clarear, <strong>não há estudo que mostre efeito</strong>. Se você usa como desodorante e a pele não arde, tudo bem. Se arder ou ficar vermelha, pare: a irritação repetida pode escurecer a axila.</p>

<h2>Bicarbonato de sódio</h2>
<p>É abrasivo e alcalino. Esfregado na axila, tira a camada de cima da pele e altera o pH. Pode até dar a impressão de pele mais clara no dia, mas a irritação tende a escurecer mais com o tempo. <strong>Não recomendado.</strong></p>

<h2>Limão</h2>
<p>É a receita mais arriscada. O suco de limão na pele, com exposição ao sol, pode causar queimadura e manchas escuras (fitofotodermatose). Na virilha e nas axilas, que já são sensíveis, o risco é maior. <strong>Não use.</strong></p>

<h2>Água oxigenada</h2>
<p>Descolore pelo, não pele. Na pele, irrita e resseca. <strong>Não recomendado.</strong></p>

<h2>Esfoliação com açúcar ou café</h2>
<p>Uma esfoliação suave, no máximo uma vez por semana, ajuda a tirar células mortas. Esfregar com força ou todos os dias é atrito, e atrito escurece. Se for fazer, use pouca pressão e nunca logo depois de depilar.</p>

<h2>Babosa (aloe vera)</h2>
<p>Acalma e hidrata. Não tem efeito clareador comprovado, mas não costuma irritar e pode ajudar a pele a se recuperar depois da depilação. Use o gel de produtos próprios para pele.</p>

<h2>O que funciona de verdade</h2>
<p>O caminho que funciona é menos "milagroso" e mais constante:</p>
<ul>
  <li><strong>Cortar a causa:</strong> trocar a lâmina, rever o desodorante, usar roupa menos apertada. As causas estão em <a href="axilas-escuras-o-que-pode-ser.html">axilas escuras: o que pode ser</a> e em <a href="virilha-escura-causas-e-como-clarear.html">virilha escura: causas e como clarear</a>.</li>
  <li><strong>Hidratar</strong> a pele todos os dias.</li>
  <li><strong>Usar um clareador cosmético</strong> com ativos estudados, como a niacinamida, por pelo menos 4 a 8 semanas. Explicamos o que os estudos dizem em <a href="niacinamida-clareia.html">niacinamida clareia a pele?</a></li>
</ul>
<p>Receita caseira parece mais segura por ser "natural", mas limão e bicarbonato irritam mais do que muitos cosméticos feitos para essas áreas.</p>
""" + CTA_CLARIZE + AVISO_PELE,
    faq=[
        ("Leite de magnésia clareia as axilas?",
         "Não há estudo que mostre efeito clareador. O leite de magnésia é usado como desodorante; se a pele arder ou ficar vermelha, suspenda."),
        ("Bicarbonato clareia a axila?",
         "Não é recomendado. O bicarbonato é abrasivo e alcalino, irrita a pele e a irritação tende a escurecer mais."),
        ("Qual a receita caseira mais segura para a axila escura?",
         "Nenhuma receita caseira tem efeito clareador comprovado. O mais seguro é hidratar, evitar atrito e usar um cosmético próprio para a área."),
        ("Limão clareia a virilha?",
         "Não use. Limão com sol pode queimar a pele e deixar manchas mais escuras."),
    ],
))

POSTS.append(dict(
    slug="clareamento-de-axilas-e-virilha-laser-peeling-ou-creme",
    curto="Clareamento de axilas e virilha: laser, peeling ou creme?",
    title="Clareamento de axilas e virilha: laser, peeling ou creme? | Velmo Drink",
    h1="Clareamento de axilas e virilha: laser, peeling ou creme?",
    desc="Compare laser, peeling e creme clareador para axilas e virilha: como funciona cada um, tempo, cuidados na pele negra e quando procurar um dermatologista.",
    categoria="Cuidados com a pele",
    data="2026-11-27",
    resumo="Como funciona cada opção, quanto tempo leva, cuidados na pele negra e por onde começar.",
    corpo="""
<p>Quem pesquisa clareamento de axilas e virilha encontra três caminhos: laser, peeling e creme. Eles não competem entre si: atendem situações diferentes. Veja como cada um funciona.</p>

<h2>Resumo da comparação</h2>
<div class="precos-wrap">
<table class="precos">
  <thead><tr><th></th><th>Creme clareador</th><th>Peeling</th><th>Laser</th></tr></thead>
  <tbody>
    <tr><td>Onde é feito</td><td>Em casa</td><td>Consultório</td><td>Clínica ou consultório</td></tr>
    <tr><td>Como age</td><td>Ativos diários, efeito gradual</td><td>Ácidos que renovam a pele</td><td>Luz que atinge o pigmento ou o pelo</td></tr>
    <tr><td>Tempo</td><td>Semanas a meses</td><td>Várias sessões</td><td>Várias sessões</td></tr>
    <tr><td>Risco de irritação</td><td>Baixo, com uso correto</td><td>Médio</td><td>Médio, maior na pele negra</td></tr>
    <tr><td>Precisa de profissional</td><td>Não</td><td>Sim</td><td>Sim</td></tr>
  </tbody>
</table>
</div>

<h2>Creme clareador</h2>
<p>É o ponto de partida para a maioria das pessoas: dá para usar em casa, todos os dias, e o risco é baixo quando se segue o rótulo. Os ativos mais comuns são niacinamida, ácido kójico, alfa-arbutina e vitamina C. O efeito é gradual: os primeiros sinais costumam aparecer em 2 a 4 semanas e a melhora mais visível em 1 a 3 meses. Entenda um desses ativos em <a href="niacinamida-clareia.html">niacinamida clareia a pele?</a></p>

<h2>Peeling</h2>
<p>O peeling químico usa ácidos (como glicólico, mandélico ou salicílico) em concentração maior que a dos cosméticos, para acelerar a renovação da pele. Deve ser feito por dermatologista, porque na virilha e nas axilas a pele é fina e a irritação pode gerar manchas novas. Costuma exigir várias sessões e cuidado em casa entre elas.</p>

<h2>Laser</h2>
<p>Há dois usos diferentes:</p>
<ul>
  <li><strong>Depilação a laser:</strong> não clareia diretamente, mas acaba com a lâmina e os pelos encravados, que são causas importantes do escurecimento. Com o tempo, a pele tende a melhorar.</li>
  <li><strong>Laser para pigmento:</strong> atinge a melanina da mancha. Exige avaliação médica e várias sessões.</li>
</ul>

<h2>Clareamento de axilas em pele negra</h2>
<p>Na pele negra, laser e peeling mal indicados podem causar <strong>hiperpigmentação pós-inflamatória</strong>: a pele escurece ainda mais depois do procedimento. Por isso é importante procurar profissional com experiência em pele negra, fazer teste antes e começar devagar. Cremes com ativos suaves e uso constante costumam ser a opção mais segura para começar.</p>

<h2>Por onde começar</h2>
<ol>
  <li>Descubra a causa: lâmina, desodorante, atrito ou algo que precise de médico. Veja <a href="axilas-escuras-o-que-pode-ser.html">axilas escuras: o que pode ser</a> e <a href="virilha-escura-causas-e-como-clarear.html">virilha escura: causas e como clarear</a>.</li>
  <li>Evite receitas que irritam (<a href="clareamento-de-axilas-caseiro.html">o que é mito no clareamento caseiro</a>).</li>
  <li>Use um creme clareador por 2 a 3 meses, com constância.</li>
  <li>Se não melhorar, ou se a mancha for grossa, aveludada ou coçar, procure um dermatologista. Ele pode indicar peeling, laser ou outro tratamento.</li>
</ol>
""" + CTA_CLARIZE + AVISO_PELE,
    faq=[
        ("Qual o melhor clareamento para axilas?",
         "Depende da causa e do tipo de pele. Para a maioria das pessoas, o começo é cortar a causa e usar um creme clareador por 2 a 3 meses. Peeling e laser são feitos por profissional, quando o creme não basta."),
        ("Clareamento de axilas a laser funciona?",
         "Pode funcionar, com várias sessões e avaliação médica. A depilação a laser também ajuda, porque acaba com a lâmina e os pelos encravados."),
        ("Pele negra pode fazer clareamento de axilas?",
         "Pode, com cuidado. Laser e peeling mal indicados podem escurecer a pele. Procure profissional com experiência em pele negra; cremes com ativos suaves costumam ser o começo mais seguro."),
        ("Peeling clareia virilha?",
         "O peeling químico acelera a renovação da pele e pode clarear, mas deve ser feito por dermatologista, porque a pele da virilha é fina e sensível."),
    ],
))

POSTS.append(dict(
    slug="creme-clareador-para-axilas-e-virilha-como-escolher",
    curto="Creme clareador para axilas e virilha: como escolher",
    title="Creme clareador para axilas e virilha: como escolher | Velmo Drink",
    h1="Creme clareador para axilas e virilha: como escolher",
    desc="Como escolher um creme ou produto para clareamento de axilas e virilha: ativos, o que conferir no rótulo, sinais de alerta, como usar e quanto tempo esperar.",
    categoria="Cuidados com a pele",
    data="2026-12-01",
    resumo="Ativos, rótulo, sinais de alerta e como usar para ver resultado.",
    corpo="""
<p>Há dezenas de cremes, séruns e "pomadas" para clarear axilas e virilha, de farmácia e de internet. Este guia mostra o que conferir antes de comprar, para escolher com segurança, seja qual for a marca.</p>

<h2>1. Veja os ativos</h2>
<p>Os ativos mais usados em cosméticos clareadores são:</p>
<ul>
  <li><strong>Niacinamida (vitamina B3):</strong> reduz a passagem do pigmento para a superfície da pele e é bem tolerada. Tem estudo em axilas; veja <a href="niacinamida-clareia.html">niacinamida clareia a pele?</a></li>
  <li><strong>Alfa-arbutina e ácido kójico:</strong> reduzem a produção de melanina.</li>
  <li><strong>Vitamina C:</strong> antioxidante, ajuda na uniformidade do tom.</li>
  <li><strong>Hidratantes</strong>, como ácido hialurônico: não clareiam, mas deixam a pele menos sensível ao atrito.</li>
</ul>
<p><strong>Hidroquinona e corticoides</strong> são medicamentos: só com receita e acompanhamento médico. Desconfie de produto que tenha esses ativos sem receita.</p>

<h2>2. Confira o rótulo</h2>
<ul>
  <li>Indicação de <strong>uso externo</strong> e das áreas (virilha, axilas, joelhos).</li>
  <li>Lista completa de ingredientes.</li>
  <li>Empresa responsável, com CNPJ, e número de notificação ou registro na Anvisa.</li>
  <li>Modo de uso e advertências.</li>
</ul>

<h2>3. Fuja das promessas exageradas</h2>
<p>Clarear a pele leva semanas. Desconfie de "clareia em 7 dias", "resultado permanente" ou "serve para qualquer pele, sem nenhum risco". Cosméticos não tratam doenças, e a mancha pode voltar se a causa continuar.</p>

<h2>4. Pense no uso diário</h2>
<p>O resultado depende de usar todos os dias por pelo menos 4 a 8 semanas. Por isso pesa na escolha:</p>
<ul>
  <li><strong>Textura</strong> que absorve rápido e não mancha a roupa.</li>
  <li><strong>Embalagem</strong> prática, como pump, que evita contaminar o produto com os dedos.</li>
  <li><strong>Preço por mês</strong>, já que o uso é contínuo. Kits de vários meses costumam sair mais baratos por mês.</li>
  <li><strong>Garantia</strong> para testar com tranquilidade.</li>
</ul>

<h2>5. Use do jeito certo</h2>
<ol>
  <li>Lave com água e sabonete neutro.</li>
  <li>Seque completamente.</li>
  <li>Aplique uma pequena quantidade.</li>
  <li>Massageie até absorver.</li>
</ol>
<p>Antes do primeiro uso, teste numa área pequena. Não aplique em mucosas, em pele ferida ou logo depois de depilar. Junto com o creme, corte a causa: veja <a href="axilas-escuras-o-que-pode-ser.html">axilas escuras: o que pode ser</a> e <a href="virilha-escura-causas-e-como-clarear.html">virilha escura: causas e como clarear</a>. Se estiver em dúvida entre creme e procedimento, veja <a href="clareamento-de-axilas-e-virilha-laser-peeling-ou-creme.html">laser, peeling ou creme</a>.</p>
""" + CTA_CLARIZE + AVISO_PELE,
    faq=[
        ("Qual o melhor creme para clareamento de axilas?",
         "O que tem ativos estudados, como niacinamida, alfa-arbutina ou vitamina C, rótulo completo com notificação na Anvisa, e que você consegue usar todos os dias por pelo menos 4 a 8 semanas."),
        ("Pomada para clarear axila precisa de receita?",
         "Pomadas com hidroquinona ou corticoide são medicamentos e precisam de receita. Cosméticos clareadores com niacinamida, por exemplo, não precisam."),
        ("Em quanto tempo um creme clareador faz efeito?",
         "Os primeiros sinais costumam aparecer em 2 a 4 semanas de uso diário, e a melhora mais visível em 1 a 3 meses."),
        ("Posso usar o mesmo creme na axila e na virilha?",
         "Se o rótulo indicar as duas áreas, sim, sempre na pele externa e nunca em mucosas."),
    ],
))

CTA_VELMO = """
<div class="blog-cta">
  <p class="blog-cta-titulo">Velmo Black Drink, da Velmora</p>
  <p>Drink em pó nos sabores morango e tangerina, pote de 150 g com 30 porções. Não emagrece sozinho: é um apoio prático para quem está organizando a alimentação. Veja a composição, o modo de uso e os preços.</p>
  <a class="btn btn-primary" href="index.html">Conhecer o Velmo Drink</a>
</div>
"""

AVISO_EMAGRECER = """<div class="loja-aviso"><strong>Importante:</strong> Este texto é informativo e não substitui a orientação de médico ou nutricionista. Nenhum suplemento emagrece sozinho, e os resultados variam de pessoa para pessoa. Gestantes, lactantes, menores de 18 anos, pessoas com doença no coração, pressão alta, problemas de tireoide, ansiedade ou que usam remédios devem consultar um médico antes de usar qualquer produto para emagrecer.</div>"""

POSTS.append(dict(
    slug="suplemento-para-emagrecer-funciona",
    curto="Suplemento para emagrecer funciona?",
    title="Suplemento para emagrecer funciona? Quantos quilos dá para perder",
    h1="Suplemento para emagrecer funciona? Quantos quilos dá para perder",
    desc="Suplemento para emagrecer funciona mesmo? Veja o que dizem os estudos, quantos quilos dá para perder com segurança, em quanto tempo e por que desconfiar de promessas.",
    categoria="Emagrecimento",
    data="2026-12-04",
    resumo="O que os estudos mostram, o ritmo seguro de perda de peso e as promessas que são sinal de alerta.",
    corpo="""
<p>"Emagrece mesmo?" e "quantos quilos dá para perder?" estão entre as perguntas mais buscadas sobre qualquer suplemento para emagrecer. A resposta honesta é menos empolgante do que os anúncios, mas ajuda você a gastar melhor o seu dinheiro.</p>

<h2>Resposta curta</h2>
<p>Suplemento para emagrecer, sozinho, faz pouca diferença. O que emagrece é gastar mais energia do que você consome (o chamado déficit calórico), mantido por semanas e meses. Um suplemento pode, no máximo, <strong>ajudar você a manter a rotina</strong>: dar praticidade a um lanche, ajudar a evitar o "beliscar", lembrar você do compromisso todos os dias.</p>

<h2>O que os estudos mostram</h2>
<p>Revisões de estudos sobre os ingredientes mais comuns em produtos para emagrecer, como cafeína, chá verde, fibras (glucomanana, psyllium), picolinato de cromo e vinagre de maçã, encontram em geral diferenças <strong>pequenas</strong> em relação ao placebo. Muitas vezes a diferença fica em poucos quilos ou menos, e boa parte dos estudos é curta, pequena ou de baixa qualidade.</p>
<p>Ou seja: quando alguém perde muito peso "tomando um produto", quase sempre mudou também a alimentação e a rotina. O mérito é principalmente dessas mudanças.</p>

<h2>Quantos quilos dá para perder com segurança</h2>
<p>O ritmo considerado saudável pela maioria dos especialistas é de <strong>0,5 a 1 kg por semana</strong>, o que dá cerca de 2 a 4 kg por mês. Na primeira semana a balança pode cair mais, porque o corpo perde água junto com o glicogênio (a reserva de açúcar dos músculos). Isso não é gordura e não se repete nas semanas seguintes.</p>
<p>Uma conta aproximada: 1 kg de gordura corresponde a cerca de 7.700 kcal. Para perder 0,5 kg por semana, é preciso um déficit de cerca de 500 kcal por dia, somando o que se come a menos e o que se gasta a mais. Perder 10 kg em um mês exigiria um déficit que nenhuma pessoa consegue manter com segurança.</p>

<h2>Em quanto tempo aparecem os resultados</h2>
<p>Com alimentação ajustada e alguma atividade física, é comum notar diferença nas roupas e nas medidas em 4 a 8 semanas. Mas não existe prazo garantido: ponto de partida, sono, estresse, remédios e hormônios mudam muito o ritmo de cada pessoa. Acompanhe pela fita métrica e por fotos, não só pela balança.</p>

<h2>Promessas que são sinal de alerta</h2>
<ul>
  <li>"Perca X kg em Y dias" ou "emagreça sem dieta e sem exercício".</li>
  <li>"Queima gordura da barriga": não existe perda de gordura localizada com suplemento.</li>
  <li>"Resultado garantido", "100% natural, sem nenhum efeito colateral".</li>
  <li>Fotos de antes e depois e depoimentos que você não consegue conferir.</li>
  <li>Produto que só se compra por um "site oficial" com contador regressivo e desconto que nunca acaba.</li>
</ul>
<p>Para saber o que conferir antes de comprar, veja também o nosso guia sobre <a href="qual-melhor-suplemento-para-emagrecer-sao-paulo-sp.html">como escolher um suplemento para emagrecer</a>.</p>

<h2>Então vale a pena usar?</h2>
<p>Vale se você enxergar o suplemento como <strong>apoio</strong>, e não como solução. Escolha um produto com rótulo claro e empresa identificada, siga o modo de uso, e invista a maior parte da energia em três coisas: refeições com proteína e fibras, movimento diário e sono.</p>
""" + CTA_VELMO + AVISO_EMAGRECER,
    faq=[
        ("Suplemento para emagrecer funciona?",
         "Sozinho, faz pouca diferença. Os estudos com os ingredientes mais comuns mostram efeitos pequenos. Ele pode ser um apoio para manter a rotina, mas quem emagrece é a combinação de alimentação e atividade física."),
        ("Quantos quilos dá para perder com suplemento?",
         "Não existe um número garantido. O ritmo seguro de perda de peso é de 0,5 a 1 kg por semana, com ou sem suplemento, e depende principalmente da alimentação."),
        ("Em quanto tempo o suplemento para emagrecer faz efeito?",
         "Com alimentação ajustada e atividade física, a diferença nas medidas costuma aparecer em 4 a 8 semanas. O prazo varia de pessoa para pessoa."),
        ("Dá para emagrecer tomando só o suplemento, sem dieta?",
         "Não. Sem déficit calórico não há perda de gordura. Desconfie de produtos que prometem emagrecer sem dieta e sem exercício."),
        ("Por que a balança cai rápido na primeira semana?",
         "Porque o corpo perde água junto com o glicogênio quando você reduz carboidratos. Essa queda não é gordura e não se repete nas semanas seguintes."),
    ],
))

POSTS.append(dict(
    slug="efeitos-colaterais-de-suplemento-para-emagrecer",
    curto="Efeitos colaterais de suplementos para emagrecer",
    title="Efeitos colaterais de suplementos para emagrecer: o que observar",
    h1="Efeitos colaterais de suplementos para emagrecer: o que observar",
    desc="Efeitos colaterais de suplementos para emagrecer: cafeína e termogênicos, fibras, chás laxantes e produtos adulterados. Quem deve evitar e quando procurar um médico.",
    categoria="Emagrecimento",
    data="2026-12-08",
    resumo="Termogênicos, fibras, chás laxantes e produtos adulterados: os efeitos mais comuns, quem deve evitar e os sinais para parar.",
    corpo="""
<p>"Tem efeito colateral?" é uma das primeiras perguntas de quem pensa em comprar um produto para emagrecer, e a pergunta certa a fazer. Nenhum produto é "seguro para todo mundo": o risco depende dos ingredientes, da dose e de quem está tomando.</p>

<h2>Cafeína e termogênicos</h2>
<p>Muitos produtos para emagrecer têm cafeína, guaraná, chá verde, café verde ou outras fontes de estimulantes. Os efeitos colaterais mais comuns são:</p>
<ul>
  <li>Insônia e sono leve, principalmente se tomados à tarde ou à noite.</li>
  <li>Coração acelerado, palpitação e tremor.</li>
  <li>Ansiedade, irritação e dor de cabeça.</li>
  <li>Aumento da pressão arterial.</li>
  <li>Azia e desconforto no estômago.</li>
</ul>
<p>Para adultos saudáveis, a referência mais usada é não passar de cerca de <strong>400 mg de cafeína por dia</strong>, somando tudo: café, refrigerante, energético e suplemento. Uma xícara de café coado tem, em média, 80 a 100 mg. Gestantes devem ficar bem abaixo disso e conversar com o médico.</p>
<p>Extratos concentrados de chá verde em doses altas já foram associados a casos de lesão no fígado. Por isso, siga a porção do rótulo e não junte vários produtos com o mesmo tipo de ingrediente.</p>

<h2>Fibras (glucomanana, psyllium, goma guar)</h2>
<p>As fibras aumentam a saciedade porque absorvem água e ocupam espaço no estômago. Os efeitos mais comuns são gases, inchaço e mudança no ritmo do intestino. Tomadas com pouca água, podem engasgar ou travar o intestino. Elas também podem atrapalhar a absorção de remédios: tome com intervalo de algumas horas e beba bastante água.</p>

<h2>Chás e produtos laxantes ou diuréticos</h2>
<p>Alguns "chás para emagrecer" têm sene, cáscara sagrada ou outras plantas laxantes e diuréticas. Eles fazem a balança cair porque eliminam água e conteúdo do intestino, não gordura. O uso frequente pode causar cólica, diarreia, desidratação, perda de potássio e dependência do intestino. Leia mais sobre isso no guia <a href="suplemento-para-emagrecer-funciona.html">suplemento para emagrecer funciona?</a></p>

<h2>O maior risco: produto adulterado</h2>
<p>A Anvisa e a polícia apreendem com frequência "emagrecedores naturais" que, na verdade, têm remédios escondidos, como sibutramina, antidepressivos ou diuréticos. Esses produtos podem causar arritmia, pressão alta e outros problemas graves, justamente porque a pessoa não sabe o que está tomando. Desconfie de produto sem rótulo completo, sem empresa identificada ou com efeito "forte demais".</p>

<h2>Quem deve evitar ou consultar o médico antes</h2>
<ul>
  <li>Gestantes, lactantes e menores de 18 anos.</li>
  <li>Pessoas com pressão alta, arritmia ou doença no coração.</li>
  <li>Quem tem problemas de tireoide, fígado, rins ou ansiedade.</li>
  <li>Quem usa remédios contínuos, como antidepressivos, anticoagulantes ou remédios para pressão e diabetes.</li>
</ul>

<h2>Sinais para parar e procurar atendimento</h2>
<ul>
  <li>Dor no peito, falta de ar, palpitação forte ou desmaio.</li>
  <li>Pele ou olhos amarelados, urina escura ou dor do lado direito da barriga.</li>
  <li>Diarreia ou vômitos que não passam.</li>
  <li>Alergia: coceira forte, inchaço no rosto ou na garganta.</li>
</ul>
<p>Se acontecer, pare o produto e procure um serviço de saúde levando a embalagem.</p>
""" + CTA_VELMO + AVISO_EMAGRECER,
    faq=[
        ("Quais os efeitos colaterais mais comuns de suplementos para emagrecer?",
         "Nos produtos com cafeína ou termogênicos: insônia, coração acelerado, ansiedade, dor de cabeça e aumento da pressão. Nos de fibras: gases e inchaço. Nos chás laxantes: cólica, diarreia e desidratação."),
        ("Suplemento natural para emagrecer pode fazer mal?",
         "Pode. Natural não quer dizer seguro: plantas e extratos têm efeitos no corpo, e doses altas ou combinações erradas podem causar problemas. Siga o rótulo e consulte um médico se tiver alguma condição de saúde."),
        ("Quanto de cafeína por dia é seguro?",
         "Para adultos saudáveis, a referência mais usada é até cerca de 400 mg por dia, somando café, refrigerante, energético e suplementos. Gestantes devem consumir bem menos e conversar com o médico."),
        ("Quem tem pressão alta pode tomar suplemento para emagrecer?",
         "Só com orientação médica. Produtos com cafeína e outros estimulantes podem aumentar a pressão e acelerar o coração."),
        ("Como saber se o produto tem remédio escondido?",
         "Pelo rótulo não dá para ter certeza. Desconfie de produto sem empresa identificada, sem lista completa de ingredientes ou com efeito forte demais, e prefira marcas regularizadas."),
    ],
))

POSTS.append(dict(
    slug="como-saber-se-suplemento-e-confiavel",
    curto="Como saber se um suplemento é confiável",
    title="Como saber se um suplemento é confiável: Anvisa, rótulo e Reclame Aqui",
    h1="Como saber se um suplemento é confiável",
    desc="Como saber se um suplemento para emagrecer é confiável e original: o que conferir na Anvisa, no rótulo, no Reclame Aqui e no site de compra antes de pagar.",
    categoria="Emagrecimento",
    data="2026-12-11",
    resumo="Um checklist de 6 passos: empresa, Anvisa, rótulo, Reclame Aqui, site de compra e promessas.",
    corpo="""
<p>"É confiável?", "é original?", "tem no Reclame Aqui?". Antes de comprar qualquer suplemento, principalmente os vendidos pela internet, vale gastar dez minutos com este checklist. Ele serve para qualquer marca, inclusive a que vendemos aqui.</p>

<h2>1. Descubra quem é a empresa</h2>
<p>O rótulo precisa trazer o nome da empresa responsável, o CNPJ e o endereço. Pesquise o CNPJ: veja se a empresa está ativa e se o ramo dela tem a ver com alimentos ou suplementos. Desconfie de produto que só mostra uma marca bonita e um número de WhatsApp.</p>

<h2>2. Confira a situação na Anvisa</h2>
<p>No Brasil, nem todo suplemento alimentar tem "número de registro": muitos são dispensados de registro, mas a empresa continua obrigada a seguir as regras da Anvisa de ingredientes, quantidades e rótulo. Por isso:</p>
<ul>
  <li>Se o rótulo traz um número de registro, consulte no site de consultas da Anvisa.</li>
  <li>Se não traz, confira se a empresa está regularizada e se os ingredientes e quantidades seguem as regras de suplementos.</li>
  <li>Pesquise o nome do produto junto com "Anvisa" para ver se há alerta, recolhimento ou proibição.</li>
</ul>
<p>Desconfie de selo "aprovado pela Anvisa" usado como argumento de venda, e de qualquer promessa de tratar ou curar doença: suplemento não é remédio.</p>

<h2>3. Leia o rótulo inteiro</h2>
<ul>
  <li>Lista completa de ingredientes e a quantidade de cada ativo por porção.</li>
  <li>Porção diária recomendada e modo de uso.</li>
  <li>Advertências (por exemplo, "não indicado para gestantes").</li>
  <li>Lote e validade.</li>
</ul>
<p>"Fórmula secreta" ou "blend exclusivo" sem as quantidades não é bom sinal.</p>

<h2>4. Pesquise no Reclame Aqui</h2>
<p>Olhe além da nota. Leia as reclamações mais recentes e veja <strong>do que</strong> as pessoas reclamam: atraso na entrega, dificuldade para cancelar assinatura, cobrança que não foi autorizada, reembolso negado. Veja também se a empresa responde e resolve. Muitas reclamações de cobrança recorrente indicam venda com assinatura escondida.</p>

<h2>5. Confira onde você está comprando</h2>
<ul>
  <li>O endereço do site é o que aparece no rótulo ou nas redes oficiais da marca?</li>
  <li>O pagamento é feito em uma plataforma conhecida, com página segura (cadeado)?</li>
  <li>Há política de troca, prazo de garantia e dados de contato?</li>
  <li>O preço é muito abaixo do normal? Produto falsificado costuma aparecer em marketplaces com preço "bom demais".</li>
</ul>
<p>Muitos produtos são vendidos por afiliados (como este site). Isso é permitido: o importante é que a compra seja feita na plataforma oficial do produtor e que o afiliado deixe isso claro.</p>

<h2>6. Desconfie das promessas</h2>
<p>Quanto maior a promessa, maior a chance de problema. "perca X kg em Y dias", "sem efeito colateral" e "resultado garantido" são sinais de alerta. Veja os detalhes em <a href="suplemento-para-emagrecer-funciona.html">suplemento para emagrecer funciona?</a> e em <a href="efeitos-colaterais-de-suplemento-para-emagrecer.html">efeitos colaterais de suplementos para emagrecer</a>.</p>
""" + CTA_VELMO + AVISO_EMAGRECER,
    faq=[
        ("Como saber se um suplemento é original?",
         "Compre pelo site ou pela plataforma oficial do produtor, confira se o rótulo traz empresa, CNPJ, lote e validade, e desconfie de preço muito abaixo do normal em marketplaces."),
        ("Todo suplemento precisa de registro na Anvisa?",
         "Não. Muitos suplementos alimentares são dispensados de registro, mas precisam seguir as regras da Anvisa de ingredientes, quantidades e rótulo. Produtos com promessa de tratar doença não podem ser vendidos como suplemento."),
        ("Como consultar um produto na Anvisa?",
         "Se o rótulo trouxer número de registro, use o site de consultas da Anvisa. Vale também pesquisar o nome do produto com a palavra Anvisa para ver alertas e recolhimentos."),
        ("O que olhar no Reclame Aqui antes de comprar?",
         "Além da nota, leia as reclamações recentes e veja o tipo de problema, como entrega, cobrança recorrente ou reembolso, e se a empresa responde e resolve."),
        ("Comprar de afiliado é seguro?",
         "Pode ser, desde que o pagamento seja feito na plataforma oficial do produtor e o afiliado informe que recebe comissão."),
    ],
))

POSTS.append(dict(
    slug="cha-ou-capsula-para-emagrecer",
    curto="Chá, cápsula ou pó para emagrecer",
    title="Chá, cápsula ou pó para emagrecer: o que olhar no rótulo",
    h1="Chá, cápsula ou pó para emagrecer: qual escolher e o que olhar no rótulo",
    desc="Chá, cápsula ou pó para emagrecer: diferenças entre os formatos, o que conferir na composição e no rótulo, como tomar e os cuidados com chás laxantes.",
    categoria="Emagrecimento",
    data="2026-12-15",
    resumo="Diferenças entre os formatos, como ler a composição e como tomar sem errar.",
    corpo="""
<p>Os produtos para emagrecer aparecem em três formatos principais: chá, cápsula (ou comprimido) e pó para preparar bebida. Muita gente escolhe pelo formato, mas o que importa de verdade é o que está dentro, e se você consegue usar todos os dias.</p>

<h2>Chá</h2>
<p><strong>Prós:</strong> ritual agradável, ajuda na hidratação, costuma ser barato.<br>
<strong>Contras:</strong> a quantidade de ativo varia com o tempo de infusão, e alguns "chás para emagrecer" têm plantas laxantes ou diuréticas, como sene e cáscara sagrada. Eles fazem a balança cair por perda de água, não de gordura, e não são para uso contínuo.</p>
<p><strong>Confira:</strong> a lista de plantas, as advertências e se há sene, cáscara sagrada ou "ruibarbo" entre os ingredientes.</p>

<h2>Cápsula ou comprimido</h2>
<p><strong>Prós:</strong> prático de levar, dose fixa, sem sabor.<br>
<strong>Contras:</strong> é fácil tomar mais do que o indicado ou somar vários produtos com cafeína. Também é o formato mais usado em produtos falsificados ou adulterados.</p>
<p><strong>Confira:</strong> a quantidade de cada ativo por cápsula, quantas cápsulas formam a porção diária e o total de cafeína, se houver.</p>

<h2>Pó para preparar bebida (drink)</h2>
<p><strong>Prós:</strong> pode substituir um lanche ou um refrigerante, tem sabor, e o preparo diário ajuda a criar o hábito.<br>
<strong>Contras:</strong> precisa de preparo, e é preciso olhar açúcar e calorias por porção.</p>
<p><strong>Confira:</strong> calorias e açúcares por porção, ingredientes, adoçantes e quantas porções vêm no pote.</p>

<h2>O que olhar na composição, em qualquer formato</h2>
<ul>
  <li><strong>Ingredientes e quantidades por porção:</strong> fuja de "blend exclusivo" sem números.</li>
  <li><strong>Estimulantes:</strong> cafeína, guaraná, chá verde e café verde somam. Veja os limites no guia de <a href="efeitos-colaterais-de-suplemento-para-emagrecer.html">efeitos colaterais</a>.</li>
  <li><strong>Laxantes e diuréticos:</strong> não são para uso diário.</li>
  <li><strong>Empresa, CNPJ, lote e validade:</strong> veja o checklist completo em <a href="como-saber-se-suplemento-e-confiavel.html">como saber se um suplemento é confiável</a>.</li>
  <li><strong>Promessas no rótulo:</strong> suplemento não pode prometer tratar doença nem "queimar gordura localizada".</li>
</ul>

<h2>Como tomar</h2>
<ol>
  <li>Siga a porção e o horário indicados no rótulo, sem dobrar a dose.</li>
  <li>Produtos com cafeína: evite tomar depois do meio da tarde.</li>
  <li>Fibras: tome com bastante água e longe dos remédios.</li>
  <li>Não combine vários produtos para emagrecer ao mesmo tempo.</li>
  <li>Junte com refeições com proteína e fibras, água e movimento: é isso que faz a diferença. Leia <a href="suplemento-para-emagrecer-funciona.html">suplemento para emagrecer funciona?</a></li>
</ol>

<h2>Qual formato escolher?</h2>
<p>O melhor formato é o que tem composição clara e que você consegue usar todos os dias sem esforço. Se você gosta de um momento de pausa, chá ou drink combinam mais. Se quer praticidade fora de casa, cápsula. Em todos os casos, leia o rótulo antes do preço.</p>
""" + CTA_VELMO + AVISO_EMAGRECER,
    faq=[
        ("Chá ou cápsula para emagrecer: qual é melhor?",
         "Nenhum formato é melhor por si só. O que importa é a composição, a quantidade de cada ativo e se você consegue usar todos os dias seguindo o rótulo."),
        ("Chá para emagrecer funciona?",
         "Chás podem ajudar na hidratação e na rotina, mas não queimam gordura. Os que têm plantas laxantes ou diuréticas só fazem perder água e não devem ser usados todos os dias."),
        ("O que olhar na composição de um produto para emagrecer?",
         "A quantidade de cada ingrediente por porção, o total de cafeína, a presença de laxantes ou diuréticos, as advertências e os dados da empresa responsável."),
        ("Qual o melhor horário para tomar?",
         "Siga o rótulo. Produtos com cafeína devem ser tomados de manhã ou no início da tarde para não atrapalhar o sono."),
        ("Posso tomar chá e cápsula para emagrecer juntos?",
         "Não é recomendado combinar produtos para emagrecer, porque os estimulantes e os efeitos colaterais se somam. Se quiser combinar, converse com um médico ou nutricionista."),
    ],
))


CTA_LOJA = """
<div class="blog-cta">
  <p class="blog-cta-titulo">Já sabe o seu objetivo?</p>
  <p>Na Loja estão os produtos da Velmora separados por uso: o Velmo Drink para quem organiza a alimentação, o CreaGym e a Creatina Gummy para quem treina. Cada página mostra a composição, o modo de uso e os cuidados.</p>
  <a class="btn btn-primary" href="loja.html">Ver a Loja</a>
</div>
"""

AVISO_SUPLEMENTOS = """<div class="loja-aviso"><strong>Importante:</strong> Este texto é informativo e não substitui a orientação de médico ou nutricionista. Suplemento não é remédio e não trata doença. Gestantes, lactantes, menores de 18 anos, pessoas com doença crônica e quem usa remédios todos os dias devem falar com um profissional de saúde antes de começar qualquer suplemento. Siga sempre a porção indicada no rótulo.</div>"""

POSTS.append(dict(
    slug="nao-sei-qual-suplemento-tomar",
    curto="Não sei qual suplemento tomar",
    title="Não sei qual suplemento tomar: como escolher pelo objetivo",
    h1="Não sei qual suplemento tomar: como escolher pelo seu objetivo",
    desc="Não sabe qual suplemento tomar? Guia para mulheres de 30 a 50 anos: como escolher pelo objetivo, o que olhar no rótulo e quando falar com um profissional.",
    categoria="Suplementos",
    data="2026-10-25",
    resumo="Para mulheres de 30 a 50 anos: comece pelo objetivo, não pela prateleira, e escolha sem gastar à toa.",
    corpo="""
<p>Você entra na farmácia (ou abre o Instagram) e aparecem colágeno, creatina, whey, termogênico, multivitamínico, ômega 3, "fórmula para mulheres 40+". Cada um com alguém jurando que mudou a vida. Dá vontade de levar tudo, e é exatamente aí que muita mulher gasta dinheiro à toa.</p>
<p>Entre os 30 e os 50 anos, o corpo muda de verdade: a massa muscular começa a cair devagar, a menstruação pode pesar no ferro, e lá pelos 40 a perimenopausa mexe com sono, humor e peso. Isso não quer dizer que você precisa de uma sacola de potes. Quer dizer que vale escolher com mais critério.</p>
<p>A escolha fica bem mais simples quando você inverte a pergunta. Em vez de "qual suplemento tomar?", pergunte "o que eu quero melhorar, e a comida já não resolve isso?".</p>

<h2>Resposta curta</h2>
<p>Escolha pelo objetivo, um suplemento de cada vez. Para quem treina com intensidade, a creatina é o que tem mais estudo. Para quem não come proteína suficiente, um pó de proteína ajuda. Para emagrecer, nenhum produto faz o trabalho sozinho. E vitaminas e minerais, só com exame ou orientação, porque excesso também faz mal.</p>

<h2>Antes de tudo: talvez você nem precise</h2>
<p>Suplemento serve para <strong>completar</strong> a alimentação, não para substituir. Se você come comida de verdade na maior parte das refeições, dorme razoavelmente e se movimenta, muitas vezes não falta nada. Nesse caso, o suplemento vira gasto extra sem retorno.</p>
<p>Três sinais de que vale a pena considerar um:</p>
<ul>
  <li>você tem um objetivo claro (ganhar força, comer mais proteína, ter um lanche prático);</li>
  <li>já tentou resolver pela alimentação e não conseguiu manter;</li>
  <li>um exame ou um profissional apontou uma falta específica.</li>
</ul>

<h2>Escolha pelo objetivo</h2>
<h3>Treino, força e desempenho</h3>
<p>Aqui a creatina é a primeira da fila. É um dos suplementos mais estudados do mundo: com pelo menos 3 g por dia, junto com treino, ela ajuda no desempenho em exercícios repetidos de curta duração e alta intensidade, como musculação e tiros de corrida. Não é estimulante, não precisa de "ciclo" e funciona do mesmo jeito em mulheres. E o treino de força fica cada vez mais importante depois dos 30, justamente porque o músculo começa a diminuir se não for usado. Para entender melhor, leia <a href="para-que-serve-a-creatina.html">para que serve a creatina</a> e <a href="como-tomar-creatina.html">como tomar creatina</a>.</p>

<h3>Comer mais proteína</h3>
<p>Adultos precisam, em média, de 0,8 g de proteína por quilo de peso por dia. Quem treina força costuma precisar de mais, algo entre 1,2 e 2 g por quilo, e depois dos 40 a proteína ajuda a preservar o músculo. Na correria, é comum o café da manhã ser só café e o almoço ser "qualquer coisa". Se você não chega lá com carne, ovo, frango, peixe, feijão e laticínios, um pó de proteína (whey ou vegetal) resolve de forma prática. Se chega, não precisa.</p>

<h3>Emagrecer</h3>
<p>Sem rodeios: nenhum suplemento emagrece sozinho. Se o peso começou a mudar perto dos 40 mesmo sem você mudar nada, a perimenopausa pode ter parte nisso, e vale conversar com a ginecologista. O que emagrece é comer um pouco menos do que você gasta, por semanas e meses. Um produto pode ajudar a manter a rotina, por exemplo como um lanche prático no lugar do refrigerante ou do biscoito. Fuja de qualquer coisa que prometa "X quilos em Y dias" ou que tenha muita cafeína misturada com outros estimulantes (o limite costuma ser 400 mg de cafeína por dia para adultos saudáveis, somando café e tudo mais).</p>
<p>Se esse é o seu caso, vale ler o guia sobre <a href="qual-melhor-suplemento-para-emagrecer-sao-paulo-sp.html">como escolher um suplemento para emagrecer</a>.</p>

<h3>Cansaço e "falta de energia"</h3>
<p>Esse é o objetivo em que mais gente erra. Cansaço tem muitas causas: sono ruim, estresse, anemia (muito comum em quem tem menstruação intensa), tireoide, perimenopausa, alimentação bagunçada. Tomar um "energético" ou um multivitamínico por conta própria pode esconder o problema em vez de resolver. Aqui o primeiro passo é conversar com um médico e, se for o caso, fazer exames.</p>

<h3>Vitaminas e minerais</h3>
<p>Vitamina D, ferro e B12 estão entre as faltas mais comuns, e são justamente as que não convém tomar no escuro. Menstruação intensa é uma das causas mais frequentes de falta de ferro em mulheres, mas ferro em excesso também faz mal. Perto da menopausa, vitamina D e cálcio ganham atenção por causa dos ossos. Quem é vegana ou vegetariana costuma precisar de B12. Em todos os casos, a dose certa vem de um exame e de um profissional, não da prateleira.</p>

<h2>Um de cada vez</h2>
<p>Começar três suplementos na mesma semana é o jeito mais rápido de não saber o que funcionou (e o que deu dor de estômago). Escolha um, use do jeito que o rótulo indica por algumas semanas e observe. Só depois pense no próximo, se ainda fizer sentido.</p>

<h2>O que conferir no rótulo</h2>
<ul>
  <li><strong>Quantidade de cada ingrediente por porção.</strong> Desconfie de "blend exclusivo" sem números.</li>
  <li><strong>Porção diária e quantas porções vêm na embalagem.</strong> É isso que mostra o preço real por mês.</li>
  <li><strong>Advertências.</strong> Todo suplemento sério informa para quem não é indicado.</li>
  <li><strong>Empresa responsável, CNPJ, lote e validade.</strong> Sem isso, não compre.</li>
  <li><strong>Promessas.</strong> Suplemento não pode dizer que trata, cura ou previne doença.</li>
</ul>

<h2>Quando falar com um profissional antes</h2>
<p>Procure um médico ou nutricionista antes de começar se você está grávida ou amamentando, tem menos de 18 anos, tem doença nos rins, no fígado ou no coração, pressão alta, diabetes, ou usa algum remédio todos os dias. Nesses casos, até um suplemento comum pode não ser indicado ou pode interferir no tratamento.</p>
""" + CTA_LOJA + AVISO_SUPLEMENTOS,
    faq=[
        ("Não sei qual suplemento tomar. Por onde começo?",
         "Comece pelo objetivo: força e treino, mais proteína, praticidade na alimentação. Depois veja se a comida já não resolve. Se não resolver, escolha um suplemento só e use por algumas semanas antes de pensar em outro."),
        ("Qual o suplemento mais seguro para começar?",
         "Para quem treina, a creatina é um dos suplementos mais estudados e com bom perfil de segurança em adultos saudáveis, na porção de 3 a 5 g por dia. Pessoas com doença nos rins devem consultar um médico antes."),
        ("Preciso tomar suplemento para ter saúde?",
         "Não necessariamente. Com alimentação variada, sono e atividade física, muitas pessoas não precisam de nenhum suplemento. Ele serve para completar o que falta, não para substituir a comida."),
        ("Posso tomar vários suplementos ao mesmo tempo?",
         "Não é o ideal começar vários juntos, porque você não sabe qual funcionou nem qual causou algum incômodo, e estimulantes se somam. Comece por um e acrescente outros com calma, de preferência com orientação."),
        ("Suplemento para emagrecer funciona?",
         "Nenhum suplemento emagrece sozinho. O que faz diferença é a alimentação e a rotina. Um produto pode ajudar a manter o hábito, mas desconfie de promessas de quilos em poucos dias."),
        ("Mulher de 40 anos precisa tomar suplemento?",
         "Não automaticamente. Com a idade, vale olhar com mais atenção para proteína, treino de força, ferro e vitamina D. Mas o que tomar, e se precisa, depende da alimentação e dos exames de cada uma."),
    ],
))


CTA_ROTINA = """
<div class="blog-cta">
  <p class="blog-cta-titulo">Uma rotina que cuida de você</p>
  <p>Comer melhor e se mexer mais ajudam o sono a longo prazo. Na Loja da Velmora estão o Velmo Drink, para quem está organizando a alimentação, e o CreaGym e a Creatina Gummy, para quem treina. Nenhum deles é para dormir ou para ansiedade: são apoio para a rotina.</p>
  <a class="btn btn-primary" href="loja.html">Ver a Loja</a>
</div>
"""

AVISO_SONO = """<div class="loja-aviso"><strong>Importante:</strong> Este texto é informativo e não substitui consulta com médico, ginecologista, psicólogo ou psiquiatra. Insônia e ansiedade são condições de saúde e têm tratamento. Não misture chás, suplementos ou remédios para dormir sem orientação. Se você está pensando em se machucar, ligue 188 (CVV, gratuito, 24 horas) ou procure uma UPA ou o SAMU (192).</div>"""

POSTS.append(dict(
    slug="durmo-mal-e-vivo-ansiosa",
    curto="Durmo mal e vivo ansiosa",
    title="Durmo mal e vivo ansiosa: o que pode ser e o que ajuda",
    h1="Durmo mal e vivo ansiosa: o que pode estar por trás e o que ajuda",
    desc="Dorme mal e vive ansiosa? Para mulheres de 30 a 50 anos: por que sono e ansiedade se alimentam, o papel da perimenopausa, o que ajuda e quando procurar ajuda.",
    categoria="Bem-estar",
    data="2026-10-27",
    resumo="Para mulheres de 30 a 50 anos: por que um puxa o outro, o que pesa nessa fase e o que dá para fazer hoje.",
    corpo="""
<p>São três da manhã e a cabeça liga sozinha: a reunião de amanhã, a conta que vence, o filho, a mãe, aquela mensagem que você não respondeu. Você vira para o lado, olha o celular, faz a conta de quantas horas ainda dá para dormir. E no dia seguinte, cansada, tudo parece mais pesado e a ansiedade vem mais fácil.</p>
<p>Se isso descreve a sua semana, saiba que é muito comum. Entre os 30 e os 50 anos, sono ruim e ansiedade estão entre as queixas mais comuns das mulheres, e as duas coisas costumam andar juntas.</p>

<h2>Resposta curta</h2>
<p>Ansiedade atrapalha o sono, e sono ruim deixa você mais ansiosa no dia seguinte. Para sair desse ciclo, ajudam horário fixo para acordar, menos cafeína à tarde, um tempo para desacelerar antes de deitar e atividade física. Nessa fase da vida, a perimenopausa também pode estar por trás. Se o problema dura semanas e atrapalha a sua vida, procure ajuda: tem tratamento, e funciona.</p>

<h2>Por que um puxa o outro</h2>
<p>Quando você está ansiosa, o corpo fica em modo de alerta: coração mais rápido, músculos tensos, pensamento acelerado. É o contrário do que ele precisa para dormir. E depois de uma noite ruim, a parte do cérebro que segura as emoções trabalha pior, então o estresse do dia pesa mais. Uma noite mal dormida já basta para você acordar com menos paciência. Várias seguidas viram um ciclo.</p>

<h2>O que costuma pesar entre os 30 e os 50</h2>
<h3>Carga mental</h3>
<p>Trabalho, casa, filhos, pais envelhecendo, a agenda de todo mundo na sua cabeça. Muita mulher só tem silêncio na hora de deitar, e é aí que os pensamentos aparecem todos de uma vez.</p>

<h3>Perimenopausa</h3>
<p>É a fase de transição antes da menopausa, que costuma começar por volta dos 40 (às vezes antes) e pode durar alguns anos. Os hormônios oscilam, e isso pode trazer calor e suor à noite, despertares de madrugada, irritabilidade, ansiedade e ciclos menstruais irregulares. Muita mulher passa anos achando que "é só estresse" sem saber que existe tratamento. Se você se reconheceu aqui, vale falar com a ginecologista.</p>

<h3>Ciclo menstrual</h3>
<p>Nos dias antes da menstruação, muitas mulheres dormem pior e ficam mais ansiosas. Anotar no calendário ajuda a ver se o seu padrão é esse.</p>

<h3>Cafeína, álcool e tela</h3>
<p>A cafeína fica horas no corpo: o café das quatro da tarde ainda está agindo às dez da noite. O vinho pode dar sono no começo, mas deixa o sono mais leve e picado na segunda metade da noite. E o celular na cama mantém a cabeça ligada, seja pela luz, seja pelo conteúdo.</p>

<h3>Saúde</h3>
<p>Tireoide, anemia, apneia do sono (aquele ronco com pausas) e alguns remédios também atrapalham o sono e podem dar sensação de ansiedade. Por isso o exame de rotina importa.</p>

<h2>O que ajuda a partir de hoje</h2>
<ul>
  <li><strong>Acorde no mesmo horário todo dia</strong>, inclusive no fim de semana. Isso ajusta o relógio do corpo mais do que o horário de deitar.</li>
  <li><strong>Pegue luz de manhã</strong>, nem que sejam dez minutos na janela ou na rua.</li>
  <li><strong>Café só até o início da tarde.</strong> Lembre que chá preto, chá mate, refrigerante de cola e alguns pré-treinos também têm cafeína.</li>
  <li><strong>Tire meia hora para desacelerar</strong> antes de deitar: luz mais baixa, banho morno, leitura em papel, sem notícia e sem trabalho.</li>
  <li><strong>Escreva as preocupações</strong> num papel antes de dormir, com o próximo passo de cada uma. Tirar da cabeça e pôr no papel acalma mais do que parece.</li>
  <li><strong>Não brigue com a cama.</strong> Se passou uns 20 minutos e o sono não veio, levante, faça algo calmo com pouca luz e volte quando bater o sono.</li>
  <li><strong>Mexa o corpo</strong> na maior parte dos dias. Caminhada já conta. Treino intenso, de preferência longe da hora de dormir.</li>
  <li><strong>Quarto fresco e escuro</strong>, o que ajuda bastante quem sente calor à noite.</li>
  <li><strong>Respire devagar</strong> quando a ansiedade apertar: solte o ar mais devagar do que puxa, por alguns minutos.</li>
</ul>
<p>Nada disso resolve em uma noite. Costuma levar algumas semanas, fazendo todo dia do mesmo jeito, para o sono começar a mudar.</p>

<h2>E os chás e suplementos?</h2>
<p>Camomila, melissa e maracujá aparecem em muitas receitas para dormir. Os estudos são pequenos e o efeito, quando existe, é leve. Como ritual de desacelerar, podem ajudar. Se você usa remédios, converse com o médico antes, porque algumas plantas interagem com eles.</p>
<p>A melatonina é permitida no Brasil como suplemento, para maiores de 19 anos, com no máximo 0,21 mg por dia. Ela não é calmante e não trata ansiedade, e não é indicada para gestantes e lactantes. O magnésio é muito divulgado para sono, mas a evidência é fraca para quem não tem falta dele.</p>
<p>Desconfie de "calmante natural" que promete acabar com a ansiedade ou fazer dormir a noite toda. E nunca misture suplemento para dormir com remédio para dormir ou para ansiedade sem orientação.</p>

<h2>Quando procurar ajuda</h2>
<p>Procure um profissional se:</p>
<ul>
  <li>você dorme mal três ou mais noites por semana há mais de um mês;</li>
  <li>a ansiedade atrapalha o trabalho, as relações ou as tarefas do dia;</li>
  <li>tem crises com coração disparado, falta de ar ou medo intenso;</li>
  <li>a tristeza ou a falta de vontade não passam;</li>
  <li>tem calor à noite, ciclos irregulares ou outros sinais de perimenopausa.</li>
</ul>
<p>Pode começar pela clínica geral, pela ginecologista ou pela Unidade Básica de Saúde, que encaminha se precisar. Para a insônia, a terapia cognitivo-comportamental é o tratamento de primeira escolha e funciona para muita gente sem remédio. Para a ansiedade, psicoterapia e, em alguns casos, medicação ajudam bastante. Quanto antes você pede ajuda, mais rápido sai do ciclo.</p>
<p>Se em algum momento você pensar em se machucar, ligue 188. O CVV atende de graça, 24 horas por dia.</p>
""" + CTA_ROTINA + AVISO_SONO,
    faq=[
        ("Por que eu durmo mal quando estou ansiosa?",
         "Porque a ansiedade deixa o corpo em alerta, com coração acelerado, músculos tensos e pensamento rápido, o contrário do que ele precisa para dormir. E dormir mal deixa a ansiedade mais forte no dia seguinte."),
        ("Perimenopausa causa insônia e ansiedade?",
         "Pode causar. Na perimenopausa, que costuma começar por volta dos 40, a oscilação dos hormônios pode trazer calor à noite, despertares, irritabilidade e ansiedade. A ginecologista consegue avaliar e indicar tratamento."),
        ("Chá de camomila ajuda a dormir?",
         "Pode ajudar como parte de um ritual para desacelerar, mas os estudos mostram efeito leve. Se você usa remédios, confirme com o médico, porque algumas plantas interagem com eles."),
        ("Melatonina ajuda na ansiedade?",
         "Não. A melatonina ajuda a regular o relógio do sono e não é calmante. No Brasil, como suplemento, é permitida para maiores de 19 anos com no máximo 0,21 mg por dia."),
        ("Quando devo procurar um médico por causa do sono?",
         "Se você dorme mal três ou mais noites por semana há mais de um mês, ou se o cansaço e a ansiedade atrapalham o trabalho e as relações. Insônia e ansiedade têm tratamento."),
    ],
))


CTA_BICARBONATO = """
<div class="blog-cta">
  <p class="blog-cta-titulo">Em vez da receita caseira, o produto certo para cada objetivo</p>
  <p>Para clarear virilha e axilas, o Clarize, clareador com niacinamida feito para essas regiões. Para organizar a alimentação, o Velmo Drink. Para o treino, o CreaGym e a Creatina Gummy. Na Loja você compara composição, modo de uso e preço.</p>
  <a class="btn btn-primary" href="loja.html">Ver a Loja</a>
</div>
"""

AVISO_BICARBONATO = """<div class="loja-aviso"><strong>Importante:</strong> Este texto é informativo e não substitui a orientação de médico, nutricionista ou dermatologista. Bicarbonato de sódio tem muito sódio e não deve ser usado por conta própria por quem tem pressão alta, doença nos rins ou no coração, está grávida ou amamentando. Não use bicarbonato em pele ferida, irritada ou em mucosas.</div>"""

POSTS.append(dict(
    slug="bicarbonato-como-suplemento",
    curto="Bicarbonato como suplemento",
    title="Bicarbonato como suplemento: emagrece, clareia ou ajuda no treino?",
    h1="Bicarbonato de sódio como suplemento: emagrece, clareia ou melhora o treino?",
    desc="Bicarbonato como suplemento funciona? O que é verdade sobre bicarbonato para emagrecer, clarear axila e virilha e melhorar o treino, e quem deve evitar.",
    categoria="Suplementos",
    data="2026-10-30",
    resumo="Três usos famosos do bicarbonato, o que tem estudo, o que é mito e quem deve evitar.",
    corpo="""
<p>Ele está na despensa de quase toda casa e aparece em receita para tudo: bicarbonato com limão em jejum para emagrecer, pasta de bicarbonato para clarear axila e virilha, cápsula de bicarbonato antes do treino. Barato, natural, "da vó". Mas funciona?</p>
<p>A resposta muda bastante de um uso para o outro, e em dois deles o bicarbonato pode atrapalhar mais do que ajudar.</p>

<h2>Resposta curta</h2>
<p>Para emagrecer, não funciona. Para clarear a pele, pode irritar e até escurecer mais. Para o treino, existe estudo mostrando ganho em esforços intensos e curtos, mas a dose é alta, costuma dar desconforto no estômago e traz muito sódio. Para a maioria das mulheres, há opções mais simples e seguras para cada objetivo.</p>

<h2>O que é o bicarbonato de sódio</h2>
<p>É um sal alcalino, ou seja, o contrário de ácido. Na cozinha, faz o bolo crescer. Na farmácia, é vendido como antiácido, para aliviar azia de vez em quando. Cada grama tem cerca de 270 mg de sódio, o mesmo mineral do sal de cozinha, e esse detalhe pesa em todos os usos abaixo.</p>

<h2>Bicarbonato emagrece?</h2>
<p>Não. Não há estudo mostrando que bicarbonato, puro ou com limão, queima gordura ou acelera o metabolismo. A mistura com limão faz espuma porque um neutraliza o outro: o que sobra é água, gás e um sal de sódio. A sensação de barriga menos estufada, quando aparece, é passageira.</p>
<p>Tomar todo dia ainda tem custo: mais sódio (ruim para a pressão e para o inchaço), possível efeito rebote de acidez no estômago e, em excesso, alteração no equilíbrio do sangue. O que emagrece continua sendo a soma de alimentação, movimento e sono, mantida por semanas. Se você está nessa busca, veja o guia sobre <a href="qual-melhor-suplemento-para-emagrecer-sao-paulo-sp.html">como escolher um suplemento para emagrecer</a>.</p>

<h2>Bicarbonato clareia axila e virilha?</h2>
<p>Essa é uma das receitas caseiras mais compartilhadas, e uma das piores para a pele dessas regiões. A pele tem pH levemente ácido, perto de 5. O bicarbonato é alcalino e granulado: esfregado na pele fina da axila e da virilha, tira a camada de proteção e pode causar ardência, vermelhidão e coceira.</p>
<p>O problema é que pele irritada tende a escurecer. Esse escurecimento depois da inflamação é mais comum justamente em peles morenas e negras. Ou seja, a receita pode deixar a região mais escura do que estava. A aparência "mais clara" logo depois de esfregar costuma ser só a pele esfoliada e avermelhada.</p>
<p>Para clarear essas áreas, o caminho mais seguro é diminuir o atrito (roupa e depilação), hidratar e usar um produto feito para a região, com ativos estudados como a niacinamida, sempre testando antes num pedaço pequeno de pele.</p>

<h2>Bicarbonato melhora o treino?</h2>
<p>Aqui existe ciência de verdade. Durante um esforço muito intenso, o músculo acumula ácido, e é isso que dá aquela queimação que obriga a parar. O bicarbonato ajuda o corpo a neutralizar esse ácido. Os estudos mostram ganho pequeno em esforços máximos de cerca de 30 segundos a alguns minutos, como tiros de corrida, remo, natação e algumas provas de luta.</p>
<p>Só que a dose usada nos estudos é alta: cerca de 0,3 g por quilo, algo como 18 a 20 g para uma mulher de 65 kg, uma a três horas antes do treino. Isso traz mais de 5 g de sódio de uma vez, mais do que o dobro do limite diário recomendado. E muita gente tem enjoo, gases e diarreia, que acabam com o treino que era para melhorar.</p>
<p>Para quem faz musculação ou treino funcional algumas vezes por semana, a <a href="para-que-serve-a-creatina.html">creatina</a> costuma ser a escolha mais simples: é estudada há décadas, a dose é pequena (3 a 5 g por dia), não precisa de hora marcada e não tem sódio. Veja também <a href="como-tomar-creatina.html">como tomar creatina</a>.</p>

<h2>Quem deve evitar bicarbonato</h2>
<ul>
  <li>Quem tem pressão alta, doença nos rins ou no coração.</li>
  <li>Grávidas e mulheres amamentando.</li>
  <li>Quem segue dieta com pouco sal ou tem inchaço frequente.</li>
  <li>Quem usa remédios todos os dias: o bicarbonato muda a acidez do estômago e pode interferir na absorção de alguns deles.</li>
  <li>Na pele: quem tem pele sensível, ferida, irritada ou acabou de depilar.</li>
</ul>

<h2>Então, para que serve?</h2>
<p>Na cozinha e na limpeza, para muita coisa. Na saúde, como antiácido ocasional, com orientação. Como suplemento, só faz sentido para quem treina em alta intensidade, com acompanhamento, e aguenta bem o estômago. Para emagrecer e para clarear a pele, vale deixar o bicarbonato na despensa.</p>
""" + CTA_BICARBONATO + AVISO_BICARBONATO,
    faq=[
        ("Bicarbonato como suplemento funciona?",
         "Para treinos muito intensos e curtos, há estudos mostrando ganho pequeno, mas a dose é alta, tem muito sódio e costuma causar desconforto no estômago. Para emagrecer ou clarear a pele, não funciona."),
        ("Bicarbonato com limão em jejum emagrece?",
         "Não. Não há estudo mostrando que a mistura queima gordura. Ela ainda traz sódio e, tomada todo dia, pode causar efeito rebote de acidez no estômago."),
        ("Bicarbonato clareia a virilha e as axilas?",
         "Não é recomendado. O bicarbonato é alcalino e abrasivo, pode irritar a pele fina dessas regiões e a irritação pode escurecer ainda mais a área, principalmente em peles morenas e negras."),
        ("Qual a dose de bicarbonato para o treino?",
         "Os estudos usam cerca de 0,3 g por quilo de peso, uma a três horas antes do exercício. É uma dose alta, com muito sódio, e só deve ser usada com orientação profissional."),
        ("Bicarbonato ou creatina para treinar?",
         "Para musculação e treino funcional, a creatina costuma ser mais prática: dose pequena, sem sódio, sem hora marcada e com muitos estudos. O bicarbonato é mais específico para esforços máximos de poucos minutos."),
    ],
))


POSTS.append(dict(
    slug="creatina-black-friday",
    curto="Creatina na Black Friday",
    title="Creatina na Black Friday: como achar desconto de verdade",
    h1="Creatina na Black Friday: como achar desconto de verdade e não cair em golpe",
    desc="Creatina na Black Friday: como saber se o desconto é real, a conta do preço por mês, o que olhar no rótulo, sites falsos e quando vale levar o kit maior.",
    categoria="Creatina",
    data="2026-10-26",
    resumo="Como saber se o desconto é real, a conta que importa e os golpes mais comuns de novembro.",
    corpo="""
<p>Novembro está chegando, e a creatina já aparece em todo canto com "até 70% OFF", contador regressivo e "últimas unidades". Para quem já usa ou quer começar, é mesmo uma boa hora para comprar, porque a creatina é de uso diário e um kit maior com desconto faz diferença no bolso. Mas é também o mês em que mais aparece desconto de mentira e site falso.</p>
<p>Este guia mostra como separar uma coisa da outra em poucos minutos.</p>

<h2>Resposta curta</h2>
<p>Desconto bom é aquele que baixa o <strong>preço por mês</strong> em relação ao que a loja cobrava antes, não o que tem a maior porcentagem escrita. Confira o preço com antecedência, faça a conta por dose ou por mês, leia o rótulo (creatina monohidratada, quantidade por porção, empresa identificada) e compre só em site que você consegue verificar.</p>
""" + BF.aviso_post(HOJE) + BF.bloco_comparacao(HOJE) + """
<h2>O truque do preço inflado</h2>
<p>O golpe mais comum da Black Friday nem é ilegal de cara: a loja aumenta o preço em outubro para "dar" 50% em novembro. No fim, você paga o mesmo de sempre, ou mais.</p>
<p>Como se proteger:</p>
<ul>
  <li>Anote hoje o preço dos produtos que você está de olho, ou tire um print.</li>
  <li>Compare o preço "de" da oferta com o que a loja cobrava semanas antes. Pela lei, o preço anterior anunciado precisa ser real.</li>
  <li>Use sites que mostram o histórico de preço quando a compra for em grandes lojas.</li>
</ul>

<h2>Faça a conta do preço por mês</h2>
<p>Porcentagem engana; preço por mês não. Divida o valor do kit pelo número de meses de uso (ou pelo número de doses). Um exemplo com números redondos: um kit de 5 potes por R$ 400 dá R$ 80 por mês, enquanto um pote avulso "com 40% OFF" por R$ 120 dá R$ 120 por mês. O segundo parece uma oferta maior, mas o primeiro sai bem mais barato.</p>
<p>Lembre também do frete: em alguns lugares ele vem à parte e muda a conta, principalmente no kit pequeno.</p>

<h2>O que olhar no rótulo antes de comprar</h2>
<ul>
  <li><strong>Tipo de creatina:</strong> a monohidratada é a mais estudada. Creapure é uma marca de creatina monohidratada, não outro tipo. Veja a diferença em <a href="creatina-monohidratada-ou-creapure.html">creatina monohidratada ou Creapure</a>.</li>
  <li><strong>Quantidade por porção:</strong> o que funciona nos estudos é pelo menos 3 g de creatina por dia, junto com treino. Desconfie de "blend" sem números.</li>
  <li><strong>Empresa, CNPJ, lote e validade:</strong> sem isso, não compre, por mais barato que esteja.</li>
  <li><strong>Formato:</strong> pó sai mais barato por dose; goma é mais prática para quem não quer misturar. As duas funcionam se a porção tiver creatina suficiente.</li>
</ul>

<h2>Golpes comuns na Black Friday</h2>
<ul>
  <li><strong>Site clonado:</strong> parece a loja oficial, mas o endereço tem uma letra a mais ou termina diferente. Digite o endereço em vez de clicar em anúncio.</li>
  <li><strong>Pix para pessoa física:</strong> loja de verdade recebe em nome da empresa.</li>
  <li><strong>Perfil falso no Instagram</strong> com preço muito abaixo de todo mundo e pagamento só por Pix.</li>
  <li><strong>Pressa artificial:</strong> contador que reinicia quando você atualiza a página e estoque "acabando" o tempo todo.</li>
</ul>
<p>Antes de pagar, procure a loja no Reclame Aqui e confira se o checkout mostra o nome da empresa vendedora.</p>

<h2>Vale a pena levar o kit maior?</h2>
<p>Se você já usa creatina e sabe que vai continuar, sim: ela é de uso diário e contínuo, e o kit de vários meses quase sempre tem o menor preço por mês. Confira só a validade, que costuma ser longa.</p>
<p>Se você nunca tomou, também dá para começar pelo kit maior, mas pense antes no formato que você vai conseguir manter todo dia, pó ou goma. Ficou em dúvida se creatina é para você? Leia <a href="para-que-serve-a-creatina.html">para que serve a creatina</a> e <a href="como-tomar-creatina.html">como tomar creatina</a>.</p>
""" + CTA_CREATINA + AVISO_CREATINA,
    faq=[
        ("Vale a pena comprar creatina na Black Friday?",
         "Vale, se o desconto for real. Como a creatina é de uso diário, um kit de vários meses com desconto costuma ter o menor preço por mês do ano. Compare com o preço cobrado antes de novembro."),
        ("Como saber se o desconto da Black Friday é real?",
         "Anote o preço antes de novembro e compare com o preço 'de' da oferta. Faça também a conta do preço por mês ou por dose: ela mostra se a oferta é boa de verdade."),
        ("Qual creatina comprar na Black Friday?",
         "Uma creatina monohidratada com quantidade por porção clara no rótulo, de pelo menos 3 g por dia, de empresa identificada com CNPJ, lote e validade. O formato, pó ou goma, é questão de preferência."),
        ("Creatina em pó ou em goma: qual compensa mais?",
         "O pó costuma sair mais barato por dose. A goma é mais prática, porque não precisa de água nem de coqueteleira. As duas funcionam se tiverem creatina suficiente por porção."),
        ("Como evitar golpe na Black Friday?",
         "Digite o endereço da loja em vez de clicar em anúncios, desconfie de Pix para pessoa física e de preço muito abaixo do mercado, e confira a loja no Reclame Aqui antes de pagar."),
    ],
))


# CTA leve no meio da leitura: caixa de uma linha antes da seção indicada (o CTA grande continua no fim).
# slug: (h2 antes do qual entra, texto, link, texto do link)
CTA_MEIO = {
    "calistenia-para-iniciantes": ("Plano de 4 semanas para iniciantes",
        "Treina com intensidade e pensa em creatina? A Velmora tem em pó e em goma.", "creatina.html", "Compare os dois formatos"),
    "como-tomar-creatina": ("Qual o melhor horário?",
        "Prefere creatina com sabor para misturar na água?", "creagym.html", "Conheça o CreaGym, sabores Morango e Tangerina"),
    "melhor-horario-para-tomar-creatina": ("E nos dias sem treino?",
        "Esquece a dose? A creatina em goma é fácil de levar na bolsa.", "creatina-gummy.html", "Veja a Creatina Gummy, 3 g por porção"),
    "creatina-com-sabor-e-em-goma": ("Então, qual escolher?",
        "Quer ver os dois formatos lado a lado, com ingredientes e preço por mês?", "creatina.html", "Compare o CreaGym e a Creatina Gummy"),
    "para-que-serve-a-creatina": ("Quem pode se beneficiar",
        "Pensando em começar?", "creatina.html", "Veja as opções de creatina da Velmora, em pó e em goma"),
    "creatina-monohidratada-ou-creapure": ("Então qual escolher?",
        "Na hora de comparar, olhe a quantidade de creatina por porção.", "creatina.html", "Veja a comparação do CreaGym e da Creatina Gummy"),
    "quem-nao-pode-tomar-creatina": ("Como usar com segurança",
        "Se a creatina é para você, compare formato e porção antes de comprar.", "creatina.html", "CreaGym ou Creatina Gummy?"),
    "como-escolher-creatina": ("4. O preço por porção",
        "Quer aplicar este checklist em um produto real?", "creatina.html", "Veja ingredientes e preço por mês do CreaGym e da Creatina Gummy"),
    "creatina-para-mulher": ("Qual a dose para mulheres?",
        "Prefere creatina com sabor ou em goma?", "creatina.html", "Compare as opções da Velmora"),
    "virilha-escura-causas-e-como-clarear": ("O que não fazer",
        "Procura um clareador feito para a região?", "clarize.html", "Conheça o Clarize, com niacinamida, para virilha e axilas"),
    "axilas-escuras-o-que-pode-ser": ("O que evitar",
        "Procura um clareador de uso externo para as axilas?", "clarize.html", "Conheça o Clarize"),
    "niacinamida-clareia": ("Como usar na virilha e nas axilas",
        "O Clarize tem niacinamida entre os seus 4 ativos.", "clarize.html", "Veja a composição e o modo de uso"),
    "clareamento-de-axilas-caseiro": ("Água oxigenada",
        "Em vez de receitas caseiras, prefira um produto feito para a pele da região.", "clarize.html", "Conheça o Clarize"),
    "clareamento-de-axilas-e-virilha-laser-peeling-ou-creme": ("Peeling",
        "Quer começar pelo creme?", "clarize.html", "Veja o Clarize: ativos, modo de uso e prazo indicado pelo fabricante"),
    "creme-clareador-para-axilas-e-virilha-como-escolher": ("3. Fuja das promessas exageradas",
        "Quer ver esses itens em um rótulo real?", "clarize.html", "Confira a composição do Clarize"),
    "suplemento-para-emagrecer-funciona": ("Em quanto tempo aparecem os resultados",
        "Procura um apoio prático para a rotina? O Velmo Drink é um drink em pó, sabores morango e tangerina.", "index.html", "Conheça o Velmo Drink"),
    "efeitos-colaterais-de-suplemento-para-emagrecer": ("Fibras (glucomanana, psyllium, goma guar)",
        "Gosta de conferir a composição antes de comprar?", "index.html", "Veja os ingredientes e o modo de uso do Velmo Drink"),
    "como-saber-se-suplemento-e-confiavel": ("4. Pesquise no Reclame Aqui",
        "Quer praticar com um produto real?", "index.html", "Confira o rótulo e o modo de uso do Velmo Drink"),
    "cha-ou-capsula-para-emagrecer": ("O que olhar na composição, em qualquer formato",
        "Um exemplo de drink em pó: o Velmo Drink, sabores morango e tangerina, 30 porções por pote.", "index.html", "Conheça o Velmo Drink"),
    "nao-sei-qual-suplemento-tomar": ("Um de cada vez",
        "Já sabe qual é o seu objetivo?", "loja.html", "Veja os produtos da Velmora separados por uso na Loja"),
    "creatina-black-friday": ("Golpes comuns na Black Friday",
        "Quer fazer a conta com produtos reais?", "creatina.html", "Veja o preço por mês do CreaGym e da Creatina Gummy"),
    "bicarbonato-como-suplemento": ("Bicarbonato melhora o treino?",
        "Procura clarear virilha e axilas sem receita caseira?", "clarize.html", "Conheça o Clarize, clareador com niacinamida para essas regiões"),
    "durmo-mal-e-vivo-ansiosa": ("E os chás e suplementos?",
        "Mexer o corpo ajuda muito o sono. Está montando uma rotina de treino ou de alimentação?", "loja.html", "Veja os produtos da Velmora na Loja"),
}

for _p in POSTS:
    _antes, _texto, _href, _rotulo = CTA_MEIO[_p["slug"]]
    _alvo = f"<h2>{_antes}</h2>"
    assert _p["corpo"].count(_alvo) == 1, (_p["slug"], _antes)
    _p["corpo"] = _p["corpo"].replace(_alvo,
        f'<aside class="blog-cta-meio"><p>{_texto} <a class="cta-meio-btn" href="{_href}">{_rotulo} &rarr;</a></p></aside>\n\n{_alvo}', 1)


def pagina_post(p):
    url = f"{SITE}/{p['slug']}.html"
    ld = {"@context": "https://schema.org", "@graph": [
        crumbs((p["h1"], url)),
        {"@type": "BlogPosting", "headline": p["h1"], "description": p["desc"],
         "datePublished": p["data"], "dateModified": p["data"], "inLanguage": "pt-BR",
         "mainEntityOfPage": url, "articleSection": p["categoria"],
         "author": {"@type": "Organization", "name": AUTOR, "url": f"{SITE}/"},
         "publisher": {"@type": "Organization", "name": "Velmo Drink", "url": f"{SITE}/"}},
        {"@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in p["faq"]]},
    ]}
    faq = "\n".join(f"<h3>{html.escape(q)}</h3>\n<p>{html.escape(a)}</p>" for q, a in p["faq"])
    outros = sorted((o for o in POSTS if o["slug"] != p["slug"]),
                    key=lambda o: o["categoria"] != p["categoria"])[:4]
    leia = ""
    if outros:
        leia = "<h2 style=\"margin-top:48px;\">Leia também</h2>\n<ul>\n" + "\n".join(
            f'  <li><a href="{o["slug"]}.html">{html.escape(o["h1"])}</a></li>' for o in outros) + "\n</ul>"
    return head(p["title"], p["desc"], url, ld, "article") + f"""
  <section class="hero loja-hero blog-hero">
    <div class="container">
      <div class="hero-content">
        <p class="blog-trilha"><a href="index.html">Início</a> / <a href="blog.html">Blog</a> / {html.escape(p['categoria'])}</p>
        <h1>{html.escape(p['h1'])}</h1>
        <p class="hero-desc">{html.escape(p['resumo'])}</p>
        <p class="blog-meta">Por {AUTOR} · <time datetime="{p['data']}">{data_br(p['data'])}</time></p>
      </div>
    </div>
  </section>

  <section class="seo-section blog-corpo">
    <article class="seo-inner blog-post">
{p['corpo']}
<h2 style="margin-top:48px;">Perguntas frequentes</h2>
{faq}
<!-- compartilhar -->
{leia}
<p class="loja-assinatura">Texto da {AUTOR}. Publicado em {data_br(p['data'])}. Este site é de um afiliado: alguns links levam a produtos à venda, e a compra é feita no site do vendedor. <a href="blog.html">Ver todos os posts do blog</a>.</p>
    </article>
  </section>
""" + FOOT


def pagina_blog():
    url = f"{SITE}/blog.html"
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Página Inicial", "item": f"{SITE}/"},
            {"@type": "ListItem", "position": 2, "name": "Blog", "item": url}]},
        {"@type": "Blog", "name": "Blog Velmo Drink", "url": url, "inLanguage": "pt-BR",
         "blogPost": [{"@type": "BlogPosting", "headline": p["h1"], "url": f"{SITE}/{p['slug']}.html",
                       "datePublished": p["data"]} for p in POSTS]},
    ]}
    cards = "\n".join(f"""        <div class="loja-card">
          <span class="blog-cat">{html.escape(p['categoria'])}</span>
          <h2 class="blog-card-titulo"><a href="{p['slug']}.html">{html.escape(p['h1'])}</a></h2>
          <p>{html.escape(p['resumo'])}</p>
          <p class="blog-meta"><time datetime="{p['data']}">{data_br(p['data'])}</time></p>
          <a class="btn btn-outline" href="{p['slug']}.html">Ler o post</a>
        </div>""" for p in sorted(POSTS, key=lambda p: p["data"], reverse=True))
    return head("Blog Velmo Drink: treino em casa, creatina e suplementos",
                "Guias práticos sobre treino em casa, calistenia, creatina e suplementos, escritos sem promessas milagrosas.",
                url, ld) + f"""
  <section class="hero loja-hero">
    <div class="container">
      <div class="hero-content">
        <div class="hero-badge">Blog</div>
        <h1>Blog Velmo Drink</h1>
        <p class="hero-desc">Guias práticos sobre treino em casa, creatina e suplementos. Sem promessas milagrosas: o que funciona, para quem e como usar.</p>
      </div>
    </div>
  </section>

  <section class="section section-alt">
    <div class="container">
      <div class="loja-grid">
{cards}
      </div>
    </div>
  </section>
""" + FOOT


FILA = sorted((p for p in POSTS if p["data"] > HOJE), key=lambda p: p["data"])
POSTS = [p for p in POSTS if p["data"] <= HOJE]


def trocar_bloco(nome, inicio, fim, conteudo):
    caminho = os.path.join(OUT, nome)
    texto = open(caminho, encoding="utf-8").read()
    antes, resto = texto.split(inicio, 1)
    _, depois = resto.split(fim, 1)
    novo = antes + inicio + conteudo + fim + depois
    if novo != texto:
        with open(caminho, "w", encoding="utf-8") as f:
            f.write(novo)


def url_sitemap(slug, data, freq, prio):
    return (f"  <url>\n    <loc>{SITE}/{slug}.html</loc>\n    <lastmod>{data}</lastmod>\n"
            f"    <changefreq>{freq}</changefreq>\n    <priority>{prio}</priority>\n  </url>\n")


por_data = sorted(POSTS, key=lambda p: p["data"])
for p in POSTS:
    with open(os.path.join(OUT, p["slug"] + ".html"), "w", encoding="utf-8") as f:
        f.write(pagina_post(p))
with open(os.path.join(OUT, "blog.html"), "w", encoding="utf-8") as f:
    f.write(pagina_blog())
# No sitemap, no mapa do site e na lista de guias de creatina.html entram só os posts publicados.
trocar_bloco("sitemap.xml", "  <!-- blog:inicio -->\n", "  <!-- blog:fim -->\n",
             url_sitemap("blog", max(p["data"] for p in POSTS), "weekly", "0.7")
             + "".join(url_sitemap(p["slug"], p["data"], "monthly", "0.6") for p in por_data))
trocar_bloco("mapa-do-site.html", "<!-- blog:inicio -->\n", "<!-- blog:fim -->\n",
             '        <div class="link-item"><a href="blog.html">Blog</a></div>\n'
             + "".join(f'        <div class="link-item"><a href="{p["slug"]}.html">{html.escape(p["curto"])}</a></div>\n'
                       for p in por_data))
trocar_bloco("creatina.html", "<!-- guias:inicio -->", "<!-- guias:fim -->",
             "\n".join(f'          <li><a href="{p["slug"]}.html">{html.escape(p["h1"])}</a></li>'
                       for p in por_data if p["categoria"] == "Creatina") + "\n")
# GTM, GA4, imagem de compartilhamento e botões de compartilhar em todas as páginas.
subprocess.run([sys.executable, "-I", os.path.join(os.path.dirname(os.path.abspath(__file__)), "rastreio.py"), OUT], check=True)
print("publicados:", [p["slug"] for p in por_data])
print("na fila:", [(p["data"], p["slug"]) for p in FILA])
