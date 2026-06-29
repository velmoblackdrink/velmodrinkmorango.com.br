/* ============================================
   VELMO DRINK — main.js
   Controla header, footer, whatsapp, schema
   ============================================ */

document.addEventListener('DOMContentLoaded', () => {

  /* ─── HEADER ─── */
  const headerHTML = `
    <header id="site-header">
      <div class="header-inner">
        <a class="logo" href="index.html">Velmo <span>Drink</span></a>
        <nav>
          <a href="index.html#beneficios">Benefícios</a>
          <a href="index.html#sobre">Sobre</a>
          <a href="index.html#depoimentos">Depoimentos</a>
        </nav>
        <a class="btn btn-primary header-cta" href="https://velmodrinkmorango.com.br" target="_blank" rel="nofollow noopener">Saiba Mais</a>
      </div>
    </header>`;

  const headerTarget = document.getElementById('header-placeholder');
  if (headerTarget) headerTarget.outerHTML = headerHTML;

  /* ─── FOOTER ─── */
  const footerHTML = `
    <!-- Footer -->
    <footer id="site-footer">
      <div class="container">
        <div class="footer-grid">
          <div class="footer-brand">
            <a class="logo" href="index.html">Velmo <span>Drink</span></a>
            <p>Suplemento natural para emagrecimento desenvolvido para auxiliar no controle do peso, da fome e da ansiedade alimentar. Atendimento 24 Horas, 7 Dias por Semana.</p>
          </div>
          <div class="footer-col">
            <h4>Links Rápidos</h4>
            <ul>
              <li><a href="index.html">Página Inicial</a></li>
              <li><a href="mapa-do-site.html">Mapa do Site</a></li>
            </ul>
          </div>
          <div class="footer-col">
            <h4>Contato</h4>
            <ul>
              <li><span>(45) 99966-3199</span></li>
              <li><span>Atendimento 24h / 7 dias</span></li>
              <li><a href="https://velmodrinkmorango.com.br" target="_blank" rel="nofollow noopener">Mais Informações</a></li>
            </ul>
          </div>
        </div>
        <div class="footer-disclaimer">
          <strong>⚠️ Aviso Importante:</strong> As informações contidas neste site são de caráter informativo e educacional. O Velmo Drink não substitui tratamentos médicos. Consulte um profissional de saúde antes de iniciar qualquer suplementação. Resultados podem variar. Produto à base de ingredientes naturais. Leia atentamente o rótulo antes de consumir.
        </div>
        <div class="footer-bottom">
          <p>© 2024 Velmo Drink. Todos os direitos reservados.</p>
          <p>velmodrinkmorango.com.br</p>
        </div>
      </div>
    </footer>`;

  const footerTarget = document.getElementById('footer-placeholder');
  if (footerTarget) footerTarget.outerHTML = footerHTML;

  /* ─── WHATSAPP FLOAT ─── */
  const waLink = document.getElementById('whatsapp-float');
  if (waLink) {
    waLink.href = 'https://velmodrinkmorango.com.br';
    waLink.setAttribute('target', '_blank');
    waLink.setAttribute('rel', 'nofollow noopener');
    waLink.innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="white" width="30" height="30">
      <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/>
    </svg>`;
  }

  /* ─── SCHEMA.ORG ─── */
  const schema = {
    "@context": "https://schema.org",
    "@type": "Product",
    "name": "Velmo Drink",
    "description": "Suplemento natural para emagrecimento desenvolvido para auxiliar no controle do peso, da fome e da ansiedade alimentar.",
    "brand": { "@type": "Brand", "name": "Velmo Drink" },
    "offers": {
      "@type": "Offer",
      "priceCurrency": "BRL",
      "availability": "https://schema.org/InStock"
    },
    "contactPoint": {
      "@type": "ContactPoint",
      "telephone": "+55-45-99966-3199",
      "contactType": "customer service",
      "availableLanguage": "Portuguese"
    }
  };
  const schemaTag = document.createElement('script');
  schemaTag.type = 'application/ld+json';
  schemaTag.textContent = JSON.stringify(schema);
  document.head.appendChild(schemaTag);

  /* ─── SKIP INJECTION (páginas estáticas) ─── */
  const skip = window.skipInjection || [];

  if (!skip.includes('hero')) {
    // hero já está estático em cada página
  }

});
