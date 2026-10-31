// Searchable table of council resolutions, loaded from data/usneseni_zo_2022-2026.csv.
(function () {
  var root = document.getElementById('usneseni-app');
  if (!root) return;
  var SRC = 'data/usneseni_zo_2022-2026.csv';
  var PAGE = 50;

  function parseCSV(text) {
    var rows = [], row = [], field = '', q = false;
    for (var i = 0; i < text.length; i++) {
      var c = text[i];
      if (q) {
        if (c === '"') {
          if (text[i + 1] === '"') { field += '"'; i++; } else q = false;
        } else field += c;
      } else if (c === '"') q = true;
      else if (c === ',') { row.push(field); field = ''; }
      else if (c === '\n') { row.push(field); rows.push(row); row = []; field = ''; }
      else if (c !== '\r') field += c;
    }
    if (field || row.length) { row.push(field); rows.push(row); }
    var head = rows.shift();
    return rows.filter(function (r) { return r.length > 1; }).map(function (r) {
      var o = {};
      head.forEach(function (h, j) { o[h.trim()] = (r[j] || '').trim(); });
      return o;
    });
  }

  function el(tag, attrs, text) {
    var e = document.createElement(tag);
    for (var k in attrs || {}) e.setAttribute(k, attrs[k]);
    if (text != null) e.textContent = text;
    return e;
  }

  function fmtDate(d) {
    var m = /^(\d{4})-(\d{2})-(\d{2})$/.exec(d);
    return m ? (+m[3]) + '. ' + (+m[2]) + '. ' + m[1] : d;
  }

  function fmtKc(v) {
    if (!v) return '';
    var n = Number(v);
    return isNaN(n) ? v : n.toLocaleString('cs-CZ') + ' Kč';
  }

  function typeClass(t) {
    var m = { 'schvaluje': 'schvaluje', 'neschvaluje': 'neschvaluje', 'bere na vědomí': 'bere', 'volí': 'voli',
      'pověřuje': 'poveruje', 'ukládá': 'uklada', 'ruší': 'rusi' };
    return m[t] || 'jine';
  }

  function norm(s) {
    return (s || '').toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '');
  }

  root.textContent = 'Načítám usnesení…';
  fetch(SRC).then(function (r) {
    if (!r.ok) throw new Error(r.status);
    return r.text();
  }).then(function (txt) {
    var data = parseCSV(txt);
    data.forEach(function (d) { d._q = norm([d.cislo, d.text, d.tema, d.typ, d.zdroj].join(' ')); });
    build(data);
  }).catch(function () {
    root.textContent = 'Data usnesení se nepodařilo načíst. Stáhnout je lze na stránce Data ke stažení.';
  });

  function build(data) {
    root.textContent = '';
    root.className = 'usn';
    var years = Array.from(new Set(data.map(function (d) { return d.datum.slice(0, 4); }))).sort();
    var topics = Array.from(new Set([].concat.apply([], data.map(function (d) {
      return d.tema.split(';').map(function (t) { return t.trim(); });
    })).filter(Boolean))).sort(function (a, b) { return a.localeCompare(b, 'cs'); });
    var types = Array.from(new Set(data.map(function (d) { return d.typ; }).filter(Boolean))).sort();

    var nOk = data.filter(function (d) { return d.vysledek === 'přijato'; }).length;
    var nNo = data.filter(function (d) { return d.vysledek === 'nepřijato'; }).length;
    var nMeet = new Set(data.map(function (d) { return d.datum; })).size;
    var stats = el('div', { 'class': 'usn-stats' });
    [[data.length, 'usnesení celkem'], [nOk, 'přijato'], [nNo, 'nepřijato'], [nMeet, 'zasedání']].forEach(function (s) {
      var t = el('div', { 'class': 'tile' });
      t.appendChild(el('div', { 'class': 'v' }, s[0].toLocaleString('cs-CZ')));
      t.appendChild(el('div', { 'class': 'l' }, s[1]));
      stats.appendChild(t);
    });
    root.appendChild(stats);
    var bar = el('div', { 'class': 'usn-filters' });
    var q = el('input', { type: 'search', placeholder: 'Hledat v usneseních (např. chodník, MŠ, 872/2)…', 'aria-label': 'Hledat' });
    function select(label, opts) {
      var s = el('select', { 'aria-label': label });
      s.appendChild(el('option', { value: '' }, label));
      opts.forEach(function (o) { s.appendChild(el('option', { value: o }, o)); });
      return s;
    }
    var sY = select('Všechny roky', years);
    var sT = select('Všechna témata', topics);
    var sP = select('Všechny typy', types);
    var sR = select('Přijato i nepřijato', ['přijato', 'nepřijato', 'neuveden v zápisu']);
    [q, sY, sT, sP, sR].forEach(function (x) { bar.appendChild(x); });
    root.appendChild(bar);

    var info = el('p', { 'class': 'usn-info' });
    root.appendChild(info);
    var tbody = el('div', { 'class': 'usn-list' });
    root.appendChild(tbody);
    var more = el('button', { type: 'button', 'class': 'btn-ghost usn-more' }, 'Zobrazit další');
    root.appendChild(more);

    var shown = PAGE, current = [];
    function apply() {
      var terms = norm(q.value).split(/\s+/).filter(Boolean);
      current = data.filter(function (d) {
        if (sY.value && d.datum.slice(0, 4) !== sY.value) return false;
        if (sT.value && d.tema.split(';').map(function (t) { return t.trim(); }).indexOf(sT.value) < 0) return false;
        if (sP.value && d.typ !== sP.value) return false;
        if (sR.value && d.vysledek !== sR.value) return false;
        return terms.every(function (t) { return d._q.indexOf(t) >= 0; });
      }).sort(function (a, b) { return b.datum.localeCompare(a.datum); });
      shown = PAGE;
      render();
    }
    function render() {
      tbody.textContent = '';
      current.slice(0, shown).forEach(function (d) {
        var r = d.vysledek === 'přijato' ? 'ok' : d.vysledek === 'nepřijato' ? 'no' : 'na';
        var card = el('article', { 'class': 'usn-card r-' + r });
        var head = el('div', { 'class': 'usn-head' });
        head.appendChild(el('span', { 'class': 'badge b-' + r }, (r === 'ok' ? '✓ ' : r === 'no' ? '✗ ' : '? ') + d.vysledek));
        if (d.typ) head.appendChild(el('span', { 'class': 'chip chip-typ t-' + typeClass(d.typ) }, d.typ));
        head.appendChild(el('span', { 'class': 'usn-num' }, d.cislo));
        head.appendChild(el('span', { 'class': 'usn-date' }, fmtDate(d.datum)));
        if (d.castka_kc) head.appendChild(el('span', { 'class': 'usn-kc' }, fmtKc(d.castka_kc)));
        card.appendChild(head);
        card.appendChild(el('p', { 'class': 'usn-text' }, d.text));
        var foot = el('div', { 'class': 'usn-foot' });
        d.tema.split(';').map(function (s) { return s.trim(); }).filter(Boolean).forEach(function (s) {
          foot.appendChild(el('span', { 'class': 'chip' }, s));
        });
        if (d.pro || d.proti || d.zdrzel) {
          foot.appendChild(el('span', { 'class': 'usn-votes' },
            'hlasování: pro ' + (d.pro || '–') + ' · proti ' + (d.proti || '–') + ' · zdržel se ' + (d.zdrzel || '–')));
        }
        foot.appendChild(el('span', { 'class': 'usn-src' }, d.zdroj));
        card.appendChild(foot);
        tbody.appendChild(card);
      });
      info.textContent = 'Nalezeno ' + current.length.toLocaleString('cs-CZ') + ' z ' + data.length.toLocaleString('cs-CZ') +
        ' usnesení.';
      more.hidden = shown >= current.length;
    }
    more.addEventListener('click', function () { shown += PAGE; render(); });
    var t;
    q.addEventListener('input', function () { clearTimeout(t); t = setTimeout(apply, 150); });
    [sY, sT, sP, sR].forEach(function (s) { s.addEventListener('change', apply); });
    apply();
  }
})();
