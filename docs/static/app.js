(function () {
  var root = document.documentElement;
  try {
    var saved = localStorage.getItem('theme');
    if (saved === 'light' || saved === 'dark') root.setAttribute('data-theme', saved);
  } catch (e) {}

  var btn = document.querySelector('.theme-toggle');
  if (btn) {
    btn.addEventListener('click', function () {
      var cur = root.getAttribute('data-theme') ||
        (matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
      var next = cur === 'dark' ? 'light' : 'dark';
      root.setAttribute('data-theme', next);
      try { localStorage.setItem('theme', next); } catch (e) {}
    });
  }

  // Wide tables scroll inside their own box instead of the page.
  document.querySelectorAll('main table').forEach(function (t) {
    if (t.parentElement.classList.contains('table-wrap')) return;
    var w = document.createElement('div');
    w.className = 'table-wrap';
    t.parentNode.insertBefore(w, t);
    w.appendChild(t);
  });

  // Hover tooltips for chart marks carrying data-tip.
  var tip = document.createElement('div');
  tip.className = 'tip';
  document.body.appendChild(tip);
  function show(e) {
    var el = e.target.closest('[data-tip]');
    if (!el) return;
    tip.textContent = el.getAttribute('data-tip');
    tip.classList.add('on');
    move(e);
  }
  function move(e) {
    var x = e.clientX + 14, y = e.clientY + 14;
    var r = tip.getBoundingClientRect();
    if (x + r.width > innerWidth - 8) x = e.clientX - r.width - 14;
    if (y + r.height > innerHeight - 8) y = e.clientY - r.height - 14;
    tip.style.left = x + 'px';
    tip.style.top = y + 'px';
  }
  function hide(e) {
    if (e.target.closest('[data-tip]')) tip.classList.remove('on');
  }
  document.addEventListener('pointerover', show);
  document.addEventListener('pointermove', function (e) {
    if (tip.classList.contains('on')) move(e);
  });
  document.addEventListener('pointerout', hide);
})();
