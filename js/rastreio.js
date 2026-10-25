/* ============================================
   VELMO DRINK — rastreio.js
   Eventos de clique no GA4/GTM, UTMs da visita levadas ao checkout,
   botões de compartilhar (Compartilhar e Copiar link) e aviso de cookies (LGPD).
   Carregado em todas as páginas pelo bloco de fonte/rastreio.py.
   ============================================ */
(function () {
  var CHAVES = ['utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 'utm_content'];
  var GUARDA = 'velmo_origem';

  // Nome curto da página: "clarize", "como-tomar-creatina", "inicio".
  function paginaDe(caminho) {
    return caminho.replace(/^\/+/, '').replace(/\.html$/, '').replace(/\/+$/, '') || 'inicio';
  }

  // De onde veio a visita: UTMs do link; sem UTMs, o site que mandou a pessoa; sem nada, direto.
  function origemDaVisita(busca, referencia, dominio) {
    var q = new URLSearchParams(busca);
    var utm = {};
    CHAVES.forEach(function (k) { if (q.get(k)) utm[k] = q.get(k).slice(0, 100); });
    if (utm.utm_source) return utm;
    var host = '';
    try { host = referencia ? new URL(referencia).hostname.replace(/^www\./, '') : ''; } catch (e) {}
    if (!host || host === dominio) return { utm_source: '(direto)', utm_medium: '(nenhum)' };
    var busca = host.match(/(?:^|\.)(google|bing|yahoo|duckduckgo|ecosia)\./);
    if (busca) return { utm_source: busca[1], utm_medium: 'organico' };
    if (/(^|\.)instagram\.com$/.test(host)) return { utm_source: 'instagram', utm_medium: 'social' };
    if (/(^|\.)(facebook\.com|fb\.me)$/.test(host)) return { utm_source: 'facebook', utm_medium: 'social' };
    return { utm_source: host, utm_medium: 'referencia' };
  }

  // Link do checkout com a origem da visita e a página do clique (utm_content).
  // A UTM que já estiver no link fica como está.
  function decorarCheckout(href, origem, pagina) {
    var u = new URL(href);
    var dados = {
      utm_source: origem.utm_source, utm_medium: origem.utm_medium, utm_campaign: origem.utm_campaign || 'site',
      utm_term: origem.utm_content || origem.utm_term, utm_content: pagina
    };
    CHAVES.forEach(function (k) { if (dados[k] && !u.searchParams.get(k)) u.searchParams.set(k, dados[k]); });
    return u.toString();
  }

  // Exposto para os testes (tests/rastreio.test.mjs).
  window.VelmoRastreio = { paginaDe: paginaDe, origemDaVisita: origemDaVisita, decorarCheckout: decorarCheckout };
  if (!window.document || !document.addEventListener) return;

  function ler() { try { return JSON.parse(sessionStorage.getItem(GUARDA)); } catch (e) { return null; } }
  function guardar(o) { try { sessionStorage.setItem(GUARDA, JSON.stringify(o)); } catch (e) {} }

  // A origem é a da primeira página da visita; uma UTM nova no meio da visita substitui.
  var nova = origemDaVisita(location.search, document.referrer, location.hostname.replace(/^www\./, ''));
  var origem = ler();
  if (!origem || new URLSearchParams(location.search).get('utm_source')) { origem = nova; guardar(origem); }
  var pagina = paginaDe(location.pathname);

  /* ─── AVISO DE COOKIES ───
     O bloco do <head> (fonte/rastreio.py) já leu a escolha em window.velmoCookies e só carrega o GTM
     (Clarity) com "aceito". Sem escolha, mostra o aviso; "Preferências de cookies" no rodapé reabre. */
  var COOKIES = 'velmo_cookies';
  var aviso = null;

  function apagarCookiesDeMedicao() {
    var dominios = ['', location.hostname, '.' + location.hostname.replace(/^www\./, '')];
    document.cookie.split(';').forEach(function (c) {
      var nome = c.split('=')[0].trim();
      if (!/^(_ga|_gid|_gat|_clck|_clsk|CLID|_fbp)/.test(nome)) return;
      dominios.forEach(function (d) {
        document.cookie = nome + '=; expires=Thu, 01 Jan 1970 00:00:00 GMT; path=/' + (d ? '; domain=' + d : '');
      });
    });
  }

  function escolher(escolha) {
    try { localStorage.setItem(COOKIES, JSON.stringify({ escolha: escolha, em: Date.now() })); } catch (e) {}
    window.velmoCookies = escolha;
    var v = escolha === 'aceito' ? 'granted' : 'denied';
    if (typeof window.gtag === 'function')
      window.gtag('consent', 'update', { analytics_storage: v, ad_storage: v, ad_user_data: v, ad_personalization: v });
    if (escolha === 'aceito') { if (window.velmoGTM) window.velmoGTM(); }
    else apagarCookiesDeMedicao();
    if (aviso) { aviso.remove(); aviso = null; }
  }

  function mostrarAviso() {
    if (aviso) return;
    aviso = document.createElement('div');
    aviso.className = 'cookies';
    aviso.setAttribute('role', 'region');
    aviso.setAttribute('aria-label', 'Aviso de cookies');
    aviso.innerHTML = '<p>Usamos cookies do Google Analytics e do Microsoft Clarity para saber quais páginas ajudam ' +
      'e melhorar o site. Eles só entram se você aceitar. ' +
      '<a href="politica-de-privacidade.html">Política de Privacidade</a></p>' +
      '<div class="cookies-botoes"><button type="button" data-cookies="recusado">Recusar</button>' +
      '<button type="button" data-cookies="aceito">Aceitar</button></div>';
    document.body.appendChild(aviso);
  }

  if (window.velmoCookies !== 'aceito' && window.velmoCookies !== 'recusado') {
    if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', mostrarAviso);
    else mostrarAviso();
  }

  function enviar(nome, dados) {
    dados.pagina = pagina;
    if (typeof window.gtag === 'function') window.gtag('event', nome, dados);
    var camada = (window.dataLayer = window.dataLayer || []);
    var copia = { event: nome };
    for (var k in dados) copia[k] = dados[k];
    camada.push(copia);
  }

  function texto(el) { return (el && el.textContent || '').replace(/\s+/g, ' ').trim().slice(0, 100); }

  // Nome do kit/produto mais perto do botão: linha da tabela de preços, card ou bloco do botão.
  function itemDe(a) {
    var linha = a.closest('tr');
    if (linha) return texto(linha.querySelector('td, th'));
    var card = a.closest('.loja-card, [class*="card"], [class*="plan"], [class*="kit"]');
    if (card) return texto(card.querySelector('h3, h4, [class*="title"], [class*="titulo"]'));
    return '';
  }

  function avisar(botao, msg) {
    var antes = botao.getAttribute('data-texto') || botao.textContent;
    botao.setAttribute('data-texto', antes);
    botao.textContent = msg;
    setTimeout(function () { botao.textContent = antes; }, 2500);
  }

  function copiar(url, botao, msg) {
    var ok = function () { avisar(botao, msg); };
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(url).then(ok, function () { window.prompt('Copie o link:', url); });
    } else {
      window.prompt('Copie o link:', url);
    }
  }

  document.addEventListener('click', function (e) {
    var el = e.target.closest && e.target.closest('a, button');
    if (!el) return;
    var escolha = el.getAttribute('data-cookies');
    if (escolha) { escolher(escolha); return; }
    if (el.hasAttribute('data-abrir-cookies')) { e.preventDefault(); mostrarAviso(); return; }

    var href = el.getAttribute('href') || '';
    var rede = el.getAttribute('data-rede');

    if (rede) {
      enviar('share', { method: rede, content_type: 'pagina', item_id: pagina, posicao: el.closest('.compartilhar-topo') ? 'topo' : 'rodape' });
      var url = el.getAttribute('data-url');
      if (rede === 'compartilhar') {
        // No celular abre a lista de apps (WhatsApp, Instagram, Facebook...); no computador, copia o link.
        if (navigator.share) navigator.share({ title: document.title, url: url }).catch(function () {});
        else copiar(url, el, 'Link copiado! Cole onde quiser');
      } else if (rede === 'copiar') {
        copiar(url, el, 'Link copiado!');
      }
      return;
    }

    if (/^https:\/\/pay\.hest\.com\.br\//.test(href)) {
      // DESLIGADO em 25/10/2026: com as UTMs no link, o checkout da Hest abriu vazio ("Vendedor:" em branco, R$ 0,00).
      // O link vai como está no HTML. Para religar, confirmar antes com a Hest que o checkout aceita UTMs.
      // el.setAttribute('href', decorarCheckout(href, origem, pagina));
      enviar('clique_comprar', {
        produto: texto(document.querySelector('h1')), item: itemDe(el), texto_botao: texto(el),
        checkout: href.split('?')[0].split('/').pop(), origem: origem.utm_source, midia: origem.utm_medium
      });
      return;
    }

    if (/^https:\/\/(wa\.me|api\.whatsapp\.com)\//.test(href)) {
      enviar('clique_whatsapp', { texto_botao: texto(el) });
      return;
    }

    if (el.tagName === 'BUTTON' || /(^|\s|-)btn(\s|-|$)/.test(el.className || '')) {
      enviar('clique_botao', { texto_botao: texto(el), destino: href.slice(0, 100) });
    }
  }, true);

})();
