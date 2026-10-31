// Error reporting: page button + "report selected text", sent to a Google Form
// (config in <body data-form-*>) or, when no form is configured, to a prefilled GitHub issue.
(function () {
  var body = document.body;
  var cfg = {
    action: body.getAttribute('data-form-action') || '',
    fPage: body.getAttribute('data-form-page') || '',
    fQuote: body.getAttribute('data-form-quote') || '',
    fText: body.getAttribute('data-form-text') || '',
    fSource: body.getAttribute('data-form-source') || '',
    fEmail: body.getAttribute('data-form-email') || '',
    repo: body.getAttribute('data-repo') || ''
  };
  var main = document.querySelector('main');
  if (!main) return;

  function sectionOf(node) {
    var el = node && node.nodeType === 1 ? node : node && node.parentElement;
    while (el && el !== main) {
      var h = el;
      while (h) {
        if (/^H[23]$/.test(h.tagName)) return h.textContent.trim();
        h = h.previousElementSibling;
      }
      el = el.parentElement;
    }
    return '';
  }

  // ---- dialog ----
  var dlg = document.createElement('dialog');
  dlg.className = 'report';
  dlg.innerHTML =
    '<form method="dialog" class="report-form">' +
    '<h2>Nahlásit chybu</h2>' +
    '<p class="report-where"></p>' +
    '<blockquote class="report-quote" hidden></blockquote>' +
    '<label><span>Co je špatně? <span class="req">*</span></span><textarea name="text" rows="4" required></textarea></label>' +
    '<label>Správný údaj a zdroj (nepovinné)<input name="source" type="text" placeholder="např. odkaz na usnesení, výkaz, web"></label>' +
    '<label>E-mail pro odpověď (nepovinné)<input name="email" type="email" autocomplete="email"></label>' +
    '<p class="report-privacy"></p>' +
    '<div class="report-actions"><button type="button" class="btn-ghost" value="cancel">Zrušit</button>' +
    '<button type="submit" class="btn-primary">Odeslat</button></div>' +
    '<p class="report-done" hidden>Děkujeme, hlášení jsme přijali. Opravené chyby zveřejňujeme na stránce <a href="opravy.html">Opravy</a>.</p>' +
    '</form>';
  body.appendChild(dlg);
  var form = dlg.querySelector('form');
  var state = { page: '', quote: '' };

  dlg.querySelector('.report-privacy').textContent = cfg.action
    ? 'Hlášení se uloží do Google Formuláře autora webu. E-mail použijeme jen pro odpověď.'
    : 'Otevře se předvyplněné hlášení na GitHubu (vyžaduje účet GitHub).';
  dlg.querySelector('.btn-ghost').addEventListener('click', function () { dlg.close(); });

  function open(quote, anchorNode) {
    var sec = quote ? sectionOf(anchorNode) : '';
    state.page = document.title.split(' – ')[0] + (sec ? ' › ' + sec : '') + ' (' + location.pathname.split('/').pop() + ')';
    state.quote = quote || '';
    form.reset();
    form.querySelector('.report-done').hidden = true;
    form.querySelectorAll('label, .report-actions, .report-privacy').forEach(function (e) { e.hidden = false; });
    dlg.querySelector('.report-where').textContent = 'Stránka: ' + state.page;
    var q = dlg.querySelector('.report-quote');
    q.hidden = !state.quote;
    q.textContent = state.quote;
    if (dlg.showModal) dlg.showModal(); else dlg.setAttribute('open', '');
    form.querySelector('textarea').focus();
  }

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    var text = form.text.value.trim();
    if (!text) return;
    var source = form.source.value.trim(), email = form.email.value.trim();
    if (cfg.action) {
      var fd = new FormData();
      fd.append(cfg.fPage, state.page);
      if (cfg.fQuote) fd.append(cfg.fQuote, state.quote);
      fd.append(cfg.fText, text);
      if (cfg.fSource) fd.append(cfg.fSource, source);
      if (cfg.fEmail) fd.append(cfg.fEmail, email);
      fetch(cfg.action, { method: 'POST', mode: 'no-cors', body: fd }).catch(function () {});
      form.querySelectorAll('label, .report-actions, .report-privacy').forEach(function (e) { e.hidden = true; });
      form.querySelector('.report-done').hidden = false;
    } else {
      var md = '**Stránka:** ' + state.page + '\n\n' +
        (state.quote ? '**Text:**\n> ' + state.quote.replace(/\n/g, '\n> ') + '\n\n' : '') +
        '**Co je špatně:**\n' + text + '\n\n' + (source ? '**Správný údaj / zdroj:** ' + source + '\n' : '');
      var url = cfg.repo + '/issues/new?labels=chyba&title=' + encodeURIComponent('Chyba: ' + state.page) +
        '&body=' + encodeURIComponent(md);
      window.open(url, '_blank', 'noopener');
      dlg.close();
    }
  });

  // ---- page button ----
  var box = document.createElement('div');
  box.className = 'report-box';
  box.innerHTML = '<span>Našli jste na této stránce chybu nebo nepřesnost?</span>' +
    '<button type="button" class="btn-primary">Nahlásit chybu</button>' +
    '<span class="hint">Tip: označte text myší a nahlaste chybu přímo v něm.</span>';
  main.appendChild(box);
  box.querySelector('button').addEventListener('click', function () { open('', null); });

  // ---- selection button ----
  var fab = document.createElement('button');
  fab.type = 'button';
  fab.className = 'report-fab';
  fab.textContent = 'Nahlásit chybu v označeném textu';
  fab.hidden = true;
  body.appendChild(fab);
  var selNode = null, selText = '';

  function onSel() {
    var s = window.getSelection();
    var t = s && s.rangeCount ? s.toString().trim() : '';
    if (!t || t.length < 3 || dlg.open || !main.contains(s.anchorNode)) { fab.hidden = true; return; }
    selText = t.slice(0, 600);
    selNode = s.anchorNode;
    var r = s.getRangeAt(0).getBoundingClientRect();
    fab.hidden = false;
    var x = Math.min(Math.max(8, r.left + r.width / 2 - fab.offsetWidth / 2), innerWidth - fab.offsetWidth - 8);
    var y = r.bottom + 8;
    if (y + fab.offsetHeight > innerHeight - 8) y = r.top - fab.offsetHeight - 8;
    fab.style.left = x + 'px';
    fab.style.top = y + 'px';
  }
  document.addEventListener('mouseup', function () { setTimeout(onSel, 0); });
  document.addEventListener('touchend', function () { setTimeout(onSel, 350); });
  document.addEventListener('keyup', function (e) { if (e.shiftKey) onSel(); });
  document.addEventListener('selectionchange', function () {
    if (!window.getSelection().toString().trim()) fab.hidden = true;
  });
  window.addEventListener('scroll', function () { fab.hidden = true; }, { passive: true });
  fab.addEventListener('mousedown', function (e) { e.preventDefault(); });
  fab.addEventListener('click', function () {
    fab.hidden = true;
    open(selText, selNode);
  });
})();
