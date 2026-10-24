/* ============================================
   VELMO DRINK — cadastro.js
   Campo "Receba Ofertas Exclusivas" (form[data-cadastro]): manda o e-mail para /api/cadastro,
   que grava na aba "Cadastros" da planilha. Só envia com a caixa de consentimento marcada.
   ============================================ */
(function () {
  document.querySelectorAll('form[data-cadastro]').forEach(function (form) {
    var aviso = form.querySelector('.newsletter-success');
    var botao = form.querySelector('button[type="submit"]');

    function mostrar(msg, erro) {
      aviso.textContent = msg;
      aviso.classList.toggle('erro', !!erro);
      aviso.style.display = 'block';
    }

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var email = form.elements.email.value.trim();
      if (!form.elements.consentimento.checked) {
        mostrar('Marque a caixa de consentimento para receber as ofertas.', true);
        return;
      }
      botao.disabled = true;
      fetch('/api/cadastro', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          email: email,
          consentimento: true,
          site: form.elements.site.value,
          pagina: location.pathname.replace(/^\/+|\.html$/g, '') || 'inicio'
        })
      }).then(function (r) {
        return r.json().catch(function () { return {}; }).then(function (d) { return { ok: r.ok, d: d }; });
      }).then(function (res) {
        if (res.ok) {
          mostrar('✅ Pronto! Seu e-mail foi cadastrado. Para cancelar, é só pedir pelo WhatsApp.');
          form.reset();
          if (typeof window.gtag === 'function') window.gtag('event', 'sign_up', { method: 'newsletter' });
        } else if (res.d.erro === 'email') {
          mostrar('Confira o e-mail digitado.', true);
        } else {
          mostrar('Não deu para cadastrar agora. Tente de novo em alguns minutos.', true);
        }
      }).catch(function () {
        mostrar('Sem conexão. Tente de novo em alguns minutos.', true);
      }).then(function () { botao.disabled = false; });
    });
  });
})();
