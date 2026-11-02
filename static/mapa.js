/* Mapa obce Horní Domaslavice. Data: window.HD_MAPA (static/mapa-data.js), záložně data/mapa_*.geojson. */
(function () {
  var el = document.getElementById('mapa');
  if (!el || !window.L) return;
  var root = document.documentElement;

  // ---------- barvy z CSS proměnných webu ----------
  function cssVar(name) { return getComputedStyle(root).getPropertyValue(name).trim(); }
  function hex(c) {
    c = c.replace('#', '');
    if (c.length === 3) c = c.split('').map(function (x) { return x + x; }).join('');
    return [parseInt(c.slice(0, 2), 16), parseInt(c.slice(2, 4), 16), parseInt(c.slice(4, 6), 16)];
  }
  function mix(a, b, t) {
    var A = hex(a), B = hex(b);
    return 'rgb(' + A.map(function (v, i) { return Math.round(v + (B[i] - v) * t); }).join(',') + ')';
  }
  var C = {};
  function readColors() {
    C.accent = cssVar('--accent') || '#2a78d6';
    C.card = cssVar('--card') || '#ffffff';
    C.ink = cssVar('--ink') || '#0b0b0b';
    C.axis = cssVar('--axis') || '#c3c2b7';
    C.muted = cssVar('--muted') || '#6f6d68';
    // jeden odstín: od barvy pozadí (nízké hodnoty) k plné barvě akcentu (vysoké hodnoty)
    C.ramp = [0.22, 0.4, 0.58, 0.78, 1].map(function (t) { return mix(C.card, C.accent, t); });
  }
  readColors();

  // ---------- škály ----------
  function fmt(v, d) { return v == null ? '–' : v.toFixed(d || 0).replace('.', ','); }
  var pctClasses = [
    { max: 20, label: '0–20 %' }, { max: 40, label: '20–40 %' }, { max: 60, label: '40–60 %' },
    { max: 80, label: '60–80 %' }, { max: 100.01, label: '80–100 %' }
  ];
  function pctIdx(v) { for (var i = 0; i < pctClasses.length; i++) if (v < pctClasses[i].max) return i; return 4; }
  var MODES = {
    domy: {
      title: 'Domy k bydlení ve čtverci',
      classes: ['méně než 5', '5', '6', '7', '8 a více'],
      value: function (p) { return p.domy == null ? 0 : Math.min(p.domy, 8) - 4; },
      all: true
    },
    vodovod: { title: 'Podíl domů s veřejným vodovodem', key: 'vodovod_pct' },
    plyn: { title: 'Podíl domů s plynem z veřejné sítě', key: 'plyn_pct' },
    kanalizace: { title: 'Podíl domů napojených na kanalizaci', key: 'kanalizace_pct',
      note: 'V obci není veřejná kanalizace; RÚIAN neuvádí žádný napojený dům.' },
    cov_zumpa: { title: 'Podíl domů s domovní ČOV nebo žumpou', key: 'cov_zumpa_pct' },
    rok: {
      title: 'Medián roku dokončení domů',
      classes: ['do 1949', '1950–1989', '1990–2009', '2010–2019', '2020 a později'],
      value: function (p) {
        var y = p.rok_median; if (y == null) return null;
        return y < 1950 ? 0 : y < 1990 ? 1 : y < 2010 ? 2 : y < 2020 ? 3 : 4;
      }
    }
  };
  ['vodovod', 'plyn', 'kanalizace', 'cov_zumpa'].forEach(function (k) {
    var m = MODES[k];
    m.classes = pctClasses.map(function (c) { return c.label; });
    m.value = function (p) { var v = p[m.key]; return v == null ? null : pctIdx(v); };
  });
  var mode = 'domy';

  // ---------- mapa ----------
  var map = L.map(el, {
    zoomSnap: 0.5, scrollWheelZoom: false, dragging: !L.Browser.mobile, tap: !L.Browser.mobile,
    attributionControl: true
  });
  map.attributionControl.setPrefix('<a href="https://leafletjs.com" target="_blank" rel="noopener">Leaflet</a>');
  el.addEventListener('click', function () { map.scrollWheelZoom.enable(); });
  el.addEventListener('mouseleave', function () { map.scrollWheelZoom.disable(); });

  var base = {
    osm: L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
      maxZoom: 19, className: 'mapa-tiles-osm',
      attribution: '&copy; <a href="https://www.openstreetmap.org/copyright" target="_blank" rel="noopener">přispěvatelé OpenStreetMap</a>'
    }),
    orto: L.tileLayer('https://ags.cuzk.gov.cz/arcgis1/rest/services/ORTOFOTO_WM/MapServer/tile/{z}/{y}/{x}', {
      maxZoom: 20, maxNativeZoom: 19,
      attribution: 'Ortofoto &copy; <a href="https://geoportal.cuzk.gov.cz/" target="_blank" rel="noopener">ČÚZK</a>'
    })
  };
  base.osm.addTo(map);

  function esc(s) {
    return String(s == null ? '' : s).replace(/[&<>"]/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c];
    });
  }

  function cellStyle(f) {
    var p = f.properties, m = MODES[mode];
    var i = m.value(p);
    if (i == null) {
      return { color: C.axis, weight: 1, dashArray: '3 3', fillColor: C.card, fillOpacity: 0.25, opacity: 0.9 };
    }
    return { color: C.card, weight: 0.8, fillColor: C.ramp[i], fillOpacity: 0.82, opacity: 0.9 };
  }

  function row(label, pct, n) {
    return '<tr><td>' + label + '</td><td class="n">' + (pct == null ? 'neuvedeno' : fmt(pct, 0) + ' %') +
      '</td><td class="n" style="color:var(--muted)">' + (n ? 'z ' + n : '') + '</td></tr>';
  }
  function cellPopup(p) {
    var h = '<h4>Čtverec 100 × 100 m</h4><p style="margin:0">Domy k bydlení: <b>' + esc(p.domy_text) + '</b></p>';
    var hasAttr = p.domy != null || p.skupina;
    if (!hasAttr) {
      return h + '<p class="src">Čtverec s méně než 5 domy a bez dost velkého okolí: podíly ani rok dokončení se kvůli ochraně soukromí neuvádějí.</p>';
    }
    if (p.domy == null) {
      h += '<p style="margin:4px 0 0">Údaje níže platí pro <b>' + esc(p.skupina_ctverce) + ' čtverců s méně než 5 domy</b> v bloku 300 × 300 m, dohromady ' +
        esc(p.skupina_domy) + ' domů.</p>';
    }
    h += '<table>' +
      row('Veřejný vodovod', p.vodovod_pct, p.vodovod_n) +
      row('Plyn z veřejné sítě', p.plyn_pct, p.plyn_n) +
      row('Kanalizace', p.kanalizace_pct, p.kanalizace_n) +
      row('Domovní ČOV nebo žumpa', p.cov_zumpa_pct, p.cov_zumpa_n) +
      '<tr><td>Medián roku dokončení</td><td class="n">' + (p.rok_median == null ? 'neuvedeno' : p.rok_median) +
      '</td><td class="n" style="color:var(--muted)">' + (p.rok_n ? 'z ' + p.rok_n : '') + '</td></tr></table>' +
      '<p class="src">Podíly z domů, u kterých RÚIAN údaj uvádí („z N“). Zdroj: RÚIAN, stav 30. 9. 2026.</p>';
    return h;
  }

  function poiIcon(cls, txt) {
    return L.divIcon({ className: '', html: '<span class="' + cls + '">' + (txt || '') + '</span>', iconSize: [18, 18], iconAnchor: [9, 9], popupAnchor: [0, -8] });
  }

  var layers = {};
  function build(D) {
    layers.hranice = L.geoJSON(D.hranice, {
      interactive: false,
      style: function () { return { color: C.ink, weight: 2.2, dashArray: '6 5', fill: false, opacity: 0.85 }; }
    });
    layers.ctverce = L.geoJSON(D.ctverce, {
      style: cellStyle,
      onEachFeature: function (f, l) { l.bindPopup(function () { return cellPopup(f.properties); }, { maxWidth: 300 }); }
    });
    layers.mista = L.geoJSON(D.mista, {
      pointToLayer: function (f, ll) { return L.marker(ll, { icon: poiIcon('mapa-poi'), title: f.properties.nazev, keyboard: true }); },
      onEachFeature: function (f, l) {
        var p = f.properties;
        l.bindPopup('<h4>' + esc(p.nazev) + '</h4><p style="margin:0">' + esc(p.popis) + '</p><p class="src">Poloha: ' + esc(p.zdroj_polohy) + '</p>', { maxWidth: 300 });
      }
    });
    layers.zastavky = L.geoJSON(D.zastavky, {
      pointToLayer: function (f, ll) { return L.marker(ll, { icon: poiIcon('mapa-bus', 'B'), title: f.properties.nazev, keyboard: true }); },
      onEachFeature: function (f, l) {
        var p = f.properties;
        l.bindPopup('<h4>' + esc(p.nazev) + '</h4><p style="margin:0"><b>' + esc(p.spoje_pracovni_den) +
          '</b> spojů v pracovní den (oba směry), linky ' + esc(p.linky.join(', ')) + '.</p><p class="src">Poloha: ' +
          esc(p.zdroj_polohy) + '. Spoje: ' + esc(p.zdroj_spoju) + '.</p>', { maxWidth: 300 });
      }
    });
    ['ctverce', 'hranice', 'mista', 'zastavky'].forEach(function (k) {
      var cb = document.querySelector('[data-mapa-layer="' + k + '"]');
      if (!cb || cb.checked) layers[k].addTo(map);
    });
    map.fitBounds(layers.hranice.getBounds(), { padding: [12, 12] });
    legend();
  }

  // ---------- legenda (HTML pod mapou) ----------
  function legend() {
    var box = document.getElementById('mapa-legenda');
    if (!box) return;
    var m = MODES[mode];
    var h = '<b>' + m.title + ':</b>';
    m.classes.forEach(function (c, i) {
      h += '<span class="sw"><i style="background:' + C.ramp[i] + '"></i>' + c + '</span>';
    });
    if (!m.all) h += '<span class="sw"><i class="none"></i>bez údaje (méně než 5 domů)</span>';
    h += '<span class="sw"><i class="line"></i>hranice obce</span>' +
      '<span class="sw"><span class="mapa-poi"></span>veřejné místo</span>' +
      '<span class="sw"><span class="mapa-bus">B</span>zastávka</span>';
    if (m.note) h += '<span class="note">' + m.note + '</span>';
    box.innerHTML = h;
  }

  function restyle() {
    readColors();
    if (layers.ctverce) layers.ctverce.setStyle(cellStyle);
    if (layers.hranice) layers.hranice.setStyle({ color: C.ink });
    legend();
  }

  // ---------- ovládání ----------
  document.querySelectorAll('[data-mapa-layer]').forEach(function (cb) {
    cb.addEventListener('change', function () {
      var l = layers[cb.getAttribute('data-mapa-layer')];
      if (!l) return;
      if (cb.checked) l.addTo(map); else map.removeLayer(l);
    });
  });
  var ctrl = document.querySelector('.mapa-ctrl');
  if (ctrl) ctrl.addEventListener('submit', function (e) { e.preventDefault(); });
  var sel = document.getElementById('mapa-barva');
  if (sel) sel.addEventListener('change', function () { mode = sel.value; restyle(); });
  document.querySelectorAll('input[name="mapa-podklad"]').forEach(function (r) {
    r.addEventListener('change', function () {
      if (!r.checked) return;
      Object.keys(base).forEach(function (k) { if (map.hasLayer(base[k])) map.removeLayer(base[k]); });
      base[r.value].addTo(map);
    });
  });

  new MutationObserver(restyle).observe(root, { attributes: true, attributeFilter: ['data-theme'] });
  if (window.matchMedia) {
    var mq = matchMedia('(prefers-color-scheme: dark)');
    if (mq.addEventListener) mq.addEventListener('change', restyle);
  }

  // ---------- načtení dat ----------
  if (window.HD_MAPA) {
    build(window.HD_MAPA);
  } else {
    var names = ['hranice', 'ctverce', 'mista', 'zastavky'], D = {};
    Promise.all(names.map(function (n) {
      return fetch('data/mapa_' + n + '.geojson').then(function (r) { return r.json(); }).then(function (j) { D[n] = j; });
    })).then(function () { build(D); }).catch(function () {
      el.innerHTML = '<p class="mapa-noscript">Data mapy se nepodařilo načíst.</p>';
    });
  }
})();
