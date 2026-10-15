# Gera o blog. Só publica os posts com data <= hoje (horário de Brasília), então um post
# com data futura fica na fila e entra no ar sozinho no dia (ver .github/workflows/publicar-blog.yml).
# Uso, da raiz do repo: python3 -I fonte/gerar_blog.py .   (HOJE=AAAA-MM-DD força a data, para testar)
import datetime, html, json, os, sys, zoneinfo

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
  <meta property="og:url" content="{canon}">
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
<div class="loja-aviso"><strong>Importante:</strong> Este texto é informativo e não substitui a orientação de um profissional de educação física ou de saúde. Creatina não é indicada para gestantes, lactantes e crianças, e pessoas com doença nos rins devem consultar um profissional antes de usar.</div>
""",
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
    data="2026-10-27",
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
    data="2026-10-30",
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
    data="2026-11-03",
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
print("publicados:", [p["slug"] for p in por_data])
print("na fila:", [(p["data"], p["slug"]) for p in FILA])
