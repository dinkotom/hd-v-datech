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
    var wrap = el('div', { 'class': 'table-wrap' });
    var table = el('table', { 'class': 'usn-table' });
    table.innerHTML = '<thead><tr><th>Číslo</th><th>Datum</th><th>Usnesení</th><th>Téma</th><th>Výsledek</th></tr></thead>';
    var tbody = el('tbody');
    table.appendChild(tbody);
    wrap.appendChild(table);
    root.appendChild(wrap);
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
        var tr = el('tr');
        tr.appendChild(el('td', { 'class': 'nowrap' }, d.cislo));
        tr.appendChild(el('td', { 'class': 'nowrap' }, fmtDate(d.datum)));
        var td = el('td');
        td.appendChild(el('div', null, d.text));
        var meta = [d.typ, fmtKc(d.castka_kc), d.zdroj].filter(Boolean).join(' · ');
        td.appendChild(el('div', { 'class': 'usn-meta' }, meta));
        tr.appendChild(td);
        tr.appendChild(el('td', null, d.tema));
        var votes = (d.pro || d.proti || d.zdrzel) ? ' (' + [d.pro || '–', d.proti || '–', d.zdrzel || '–'].join(' : ') + ')' : '';
        tr.appendChild(el('td', { 'class': d.vysledek === 'nepřijato' ? 'usn-no' : '' }, d.vysledek + votes));
        tbody.appendChild(tr);
      });
      info.textContent = 'Nalezeno ' + current.length.toLocaleString('cs-CZ') + ' z ' + data.length.toLocaleString('cs-CZ') +
        ' usnesení. Hlasování je uvedeno jako pro : proti : zdržel se.';
      more.hidden = shown >= current.length;
    }
    more.addEventListener('click', function () { shown += PAGE; render(); });
    var t;
    q.addEventListener('input', function () { clearTimeout(t); t = setTimeout(apply, 150); });
    [sY, sT, sP, sR].forEach(function (s) { s.addEventListener('change', apply); });
    apply();
  }
})();
