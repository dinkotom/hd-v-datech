"""Vrstvy pro stránku „Mapa obce“ (obsah/mapa.md) -> data/mapa_*.geojson.

Použití (z kořene repozitáře):
  /usr/bin/python3 -I tools/mapa_data.py --vfr <20260930_OB_512192_UKSH.xml> \
      --osm <osm_hd.json z tools/mapa_osm.py> --jdf <subset.json s JDF jízdními řády> \
      [--datum 2026-11-03] [--diag]

Vstupy:
  --vfr  výměnný formát RÚIAN, obec 512192, úplná data se standardní hranicí (OB_UKSH);
         https://vdp.cuzk.gov.cz/vymenny_format/soucasna/20260930_OB_512192_UKSH.xml.zip
  --osm  výstup tools/mapa_osm.py (Overpass API, OpenStreetMap, licence ODbL)
  --jdf  jízdní řády linek ve formátu JDF převedené do JSON {soubor: {tabulka: [řádky]}}
         (CIS JŘ, stejná data jako obec_dokumenty/srovnani_obci/data_vybavenost/doprava_JDF_*.csv)

Výstupy (WGS84, 6 desetinných míst):
  data/mapa_hranice.geojson   hranice obce a katastrálního území
  data/mapa_ctverce.geojson   zástavba ve čtvercích 100 × 100 m sítě S-JTSK
  data/mapa_mista.geojson     veřejné budovy a místa (body)
  data/mapa_zastavky.geojson  autobusové zastávky s počtem spojů v pracovní den
  data/mapa_souhrn.json       čísla za obec pro tabulku pod mapou a kontrolu převodu

Ochrana soukromí: jednotlivé domy se nevypisují. Čtverec s 1–2 domy dostane jen údaj
„méně než 3“ bez dalších atributů.
"""
import argparse
import datetime
import json
import math
import os
import re
import statistics
import sys
import xml.etree.ElementTree as ET
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from krovak import sjtsk_to_wgs84, distance_m  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NS = {
    'vf': 'urn:cz:isvs:ruian:schemas:VymennyFormatTypy:v1',
    'obi': 'urn:cz:isvs:ruian:schemas:ObecIntTypy:v1',
    'kui': 'urn:cz:isvs:ruian:schemas:KatUzIntTypy:v1',
    'soi': 'urn:cz:isvs:ruian:schemas:StavObjIntTypy:v1',
    'ami': 'urn:cz:isvs:ruian:schemas:AdrMistoIntTypy:v1',
    'pai': 'urn:cz:isvs:ruian:schemas:ParcelaIntTypy:v1',
    'com': 'urn:cz:isvs:ruian:schemas:CommonTypy:v1',
    'gml': 'http://www.opengis.net/gml/3.2',
}
# uzel OSM „Horní Domaslavice“ (place=village), převzatý z ÚIR-ZSJ; stav OSM 31. 10. 2026
PLACE_NODE = {'lat': 49.6956992, 'lon': 18.4592603}
CELL = 100          # velikost čtverce v metrech
K_MIN = 5           # minimální počet domů pro zveřejnění atributů čtverce
DEC = 6


def rnd(v):
    return round(v, DEC)


def ll(x, y):
    lat, lon = sjtsk_to_wgs84(x, y)
    return [rnd(lon), rnd(lat)]


def text(el, path):
    e = el.find(path, NS)
    return e.text.strip() if e is not None and e.text else ''


def pos(el, path):
    e = el.find(path, NS)
    if e is None:
        return None
    x, y = map(float, e.text.split()[:2])
    return x, y


def ring(poslist):
    v = list(map(float, poslist.split()))
    return [(v[i], v[i + 1]) for i in range(0, len(v), 2)]


def multisurface(el):
    """gml:MultiSurface -> list polygonů [vnější, díry...] v S-JTSK."""
    polys = []
    for poly in el.iter('{%s}Polygon' % NS['gml']):
        rings = [ring(poly.find('gml:exterior/gml:LinearRing/gml:posList', NS).text)]
        for i in poly.findall('gml:interior/gml:LinearRing/gml:posList', NS):
            rings.append(ring(i.text))
        polys.append(rings)
    return polys


def point_in_polys(pt, polys):
    def inside(p, r):
        x, y = p
        c = False
        for (x1, y1), (x2, y2) in zip(r, r[1:] + r[:1]):
            if (y1 > y) != (y2 > y) and x < (x2 - x1) * (y - y1) / (y2 - y1) + x1:
                c = not c
        return c
    return any(inside(pt, p[0]) and not any(inside(pt, h) for h in p[1:]) for p in polys)


def polys_to_geojson(polys):
    out = []
    for p in polys:
        rings = []
        for r in p:
            c = [ll(x, y) for x, y in r]
            if c[0] != c[-1]:
                c.append(c[0])
            rings.append(c)
        out.append(rings)
    return {'type': 'MultiPolygon', 'coordinates': out}


def feature(geom, props):
    return {'type': 'Feature', 'geometry': geom, 'properties': props}


BUNDLE = {}   # stejná data pro static/mapa-data.js (stránka otevřená z file:// nesmí použít fetch)


def write_geojson(name, feats, meta=None):
    fc = {'type': 'FeatureCollection', 'features': feats}
    if meta:
        fc['metadata'] = meta
    BUNDLE[name[len('mapa_'):-len('.geojson')]] = fc
    path = os.path.join(ROOT, 'data', name)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(fc, f, ensure_ascii=False, separators=(',', ':'))
        f.write('\n')
    print(f'{name}: {len(feats)} prvků, {os.path.getsize(path) / 1024:.0f} kB')


# ---------- RÚIAN ----------

def load_vfr(path):
    root = ET.parse(path).getroot()
    data = root.find('vf:Data', NS)
    obec = data.find('vf:Obce/vf:Obec', NS)
    ku = data.find('vf:KatastralniUzemi/vf:KatastralniUzemi', NS)
    res = {
        'obec': {'kod': text(obec, 'obi:Kod'), 'nazev': text(obec, 'obi:Nazev'),
                 'db': pos(obec, 'obi:Geometrie/obi:DefinicniBod//gml:pos'),
                 'polys': multisurface(obec.find('obi:Geometrie/obi:OriginalniHranice', NS))},
        'ku': {'kod': text(ku, 'kui:Kod'), 'nazev': text(ku, 'kui:Nazev'),
               'polys': multisurface(ku.find('kui:Geometrie/kui:OriginalniHranice', NS))},
        'datum': text(root, 'vf:Hlavicka/vf:PlatnostDatK/com:ISUI')[:10],
    }
    so = {}
    for e in data.iter('{%s}StavebniObjekt' % NS['vf']):
        kod = text(e, 'soi:Kod')
        so[kod] = {
            'kod': kod,
            'typ': text(e, 'soi:TypStavebnihoObjektuKod'),
            'vyuziti': text(e, 'soi:ZpusobVyuzitiKod'),
            'cisla': [c.text for c in e.findall('soi:CislaDomovni/com:CisloDomovni', NS)],
            'byty': int(text(e, 'soi:PocetBytu') or 0),
            'rok': int(text(e, 'soi:Dokonceni')[:4]) if text(e, 'soi:Dokonceni') else None,
            'voda': text(e, 'soi:PripojeniVodovodKod'),
            'plyn': text(e, 'soi:PripojeniPlynKod'),
            'kanal': text(e, 'soi:PripojeniKanalizaceKod'),
            'db': pos(e, 'soi:Geometrie/soi:DefinicniBod//gml:pos'),
        }
    am = []
    for e in data.iter('{%s}AdresniMisto' % NS['vf']):
        am.append({'kod': text(e, 'ami:Kod'), 'cislo': text(e, 'ami:CisloDomovni'),
                   'so': text(e, 'ami:StavebniObjekt/soi:Kod'),
                   'bod': pos(e, 'ami:Geometrie/ami:DefinicniBod//gml:pos')})
    par = []
    for e in data.iter('{%s}Parcela' % NS['vf']):
        par.append({'id': text(e, 'pai:Id'), 'kmen': text(e, 'pai:KmenoveCislo'),
                    'pod': text(e, 'pai:PododdeleniCisla'), 'druh_cisl': text(e, 'pai:DruhCislovaniKod'),
                    'db': pos(e, 'pai:Geometrie/pai:DefinicniBod//gml:pos')})
    res['so'], res['am'], res['par'] = so, am, par
    return res


def is_house(s):
    """Dům k bydlení: rodinný nebo bytový dům, případně jiná budova s č. p. a s byty."""
    return s['vyuziti'] in ('6', '7') or (s['typ'] == '1' and s['byty'] > 0)


def share(vals, ok):
    known = [v for v in vals if v not in ('', '8', '9')]
    if not known:
        return None, 0
    return round(100 * sum(1 for v in known if v in ok) / len(known), 1), len(known)


ATTRS = (('vodovod', 'voda', ('1',)), ('plyn', 'plyn', ('1',)),
         ('kanalizace', 'kanal', ('1',)), ('cov_zumpa', 'kanal', ('2', '3')))


def attrs(hs):
    """Podíly napojení a medián roku dokončení; údaj s méně než K_MIN zjištěnými hodnotami se nezveřejní."""
    p = {}
    for key, attr, ok in ATTRS:
        s, k = share([h[attr] for h in hs], ok)
        p[f'{key}_pct'] = s if k >= K_MIN else None
        p[f'{key}_n'] = k
    roky = sorted(h['rok'] for h in hs if h['rok'])
    p['rok_median'] = int(round(statistics.median(roky))) if len(roky) >= K_MIN else None
    p['rok_n'] = len(roky)
    return p


def build_cells(houses):
    """Čtverce 100 m; čtverce s 1–2 domy se pro atributy slučují v bloku 300 × 300 m.

    Atributy čtverce se zveřejní, jen když má aspoň K_MIN domů. Zbylé (malé) čtverce téhož bloku
    300 × 300 m se sloučí do skupiny a dostanou společné atributy, pokud má skupina aspoň K_MIN domů.
    Skupina obsahuje jen domy z malých čtverců, takže ji nelze „odečíst“ od zveřejněných čtverců.
    """
    cells = defaultdict(list)
    for h in houses:
        x, y = h['db']
        cells[(math.floor(x / CELL), math.floor(y / CELL))].append(h)
    groups = defaultdict(list)
    for (i, j), hs in cells.items():
        if len(hs) < K_MIN:
            groups[(math.floor(i / 3), math.floor(j / 3))].append((i, j))
    gattrs = {}
    for g, members in groups.items():
        hs = [h for c in members for h in cells[c]]
        if len(hs) >= K_MIN:
            gattrs[g] = dict(skupina=f'{g[0]}_{g[1]}', skupina_domy=len(hs), skupina_ctverce=len(members), **attrs(hs))
    feats = []
    for (i, j), hs in sorted(cells.items()):
        x0, y0 = i * CELL, j * CELL
        corners = [(x0, y0), (x0 + CELL, y0), (x0 + CELL, y0 + CELL), (x0, y0 + CELL), (x0, y0)]
        geom = {'type': 'Polygon', 'coordinates': [[ll(x, y) for x, y in corners]]}
        n = len(hs)
        p = {'id': f'{i}_{j}'}
        if n < K_MIN:
            p['domy'] = None
            p['domy_text'] = f'méně než {K_MIN}'
            g = (math.floor(i / 3), math.floor(j / 3))
            if g in gattrs:
                p.update(gattrs[g])
        else:
            p['domy'] = n
            p['domy_text'] = str(n)
            p.update(attrs(hs))
        feats.append(feature(geom, p))
    return feats, cells, groups, gattrs


def totals(houses):
    t = {'domy': len(houses)}
    for key, attr, ok in (('vodovod', 'voda', ('1',)), ('plyn', 'plyn', ('1',)),
                          ('kanalizace', 'kanal', ('1',)), ('cov_zumpa', 'kanal', ('2', '3'))):
        s, k = share([h[attr] for h in houses], ok)
        t[f'{key}_pct'], t[f'{key}_n'] = s, k
    roky = sorted(h['rok'] for h in houses if h['rok'])
    t['rok_median'] = int(round(statistics.median(roky)))
    t['rok_n'] = len(roky)
    t['dokonceno_od_2010'] = sum(1 for r in roky if r >= 2010)
    return t


# ---------- OSM ----------

def load_osm(path):
    with open(path, encoding='utf-8') as f:
        js = json.load(f)
    out = {}
    for e in js['elements']:
        c = e.get('center', e)
        out[f"{e['type']}/{e['id']}"] = {'lat': c.get('lat'), 'lon': c.get('lon'), 'tags': e.get('tags', {})}
    return out, js.get('osm3s', {}).get('timestamp_osm_base', '')


# ---------- JDF ----------

def stop_counts(path, date, obec='Horní Domaslavice'):
    """Počet spojů, které v daný den zastaví na jednotlivých zastávkách obce (oba směry)."""
    with open(path, encoding='utf-8') as f:
        d = json.load(f)
    D = datetime.date(*map(int, date.split('-')))
    WD = D.isoweekday()

    def pd(s):
        return datetime.date(int(s[4:8]), int(s[2:4]), int(s[0:2])) if s else None

    best = {}
    for k, v in d.items():
        L = v['Linky.txt'][0]
        if not re.match(r'^(86|91)', L[0]):
            continue
        od, do = pd(L[13]), pd(L[14])
        rozl = int(L[15] or 0)
        if not (od <= D <= do):
            continue
        if L[0] not in best or (od, rozl) > (best[L[0]][1], best[L[0]][2]):
            best[L[0]] = (k, od, rozl)
    counts = defaultdict(int)
    lines = defaultdict(set)
    spoje = set()
    for line, (k, _, _) in sorted(best.items()):
        v = d[k]
        pk = {r[0]: r[1] for r in v['Pevnykod.txt']}
        zast = {r[0]: r for r in v['Zastavky.txt']}
        cas = defaultdict(list)
        for r in v['Caskody.txt']:
            cas[r[1]].append(r)
        zs = defaultdict(list)
        for r in v['Zasspoje.txt']:
            zs[r[1]].append(r)
        for s in v['Spoje.txt']:
            sp = s[1]
            codes = [pk.get(c, '') for c in s[2:12] if c]
            days = [c for c in codes if c in ('X', '1', '2', '3', '4', '5', '6', '7', '+')]
            run = (('X' in days and WD <= 5) or (str(WD) in days) or ('+' in days and WD == 7)) if days else True
            cc = cas.get(sp, [])

            def inr(r):
                return pd(r[5]) <= D <= (pd(r[6]) or pd(r[5]))
            t3 = [r for r in cc if r[4] == '3']
            if t3:
                run = any(inr(r) for r in t3)
            else:
                t1 = [r for r in cc if r[4] == '1']
                if t1 and not any(inr(r) for r in t1):
                    run = False
                if any(inr(r) for r in cc if r[4] == '2'):
                    run = True
            if any(inr(r) for r in cc if r[4] == '4'):
                run = False
            if not run:
                continue
            seen = set()
            for r in zs[sp]:
                if r[11] in ('', '<', '|') and r[10] in ('', '<', '|'):
                    continue   # spoj zastávkou neprojíždí nebo nezastavuje
                z = zast[r[3]]
                if z[1].split(' [')[0] != obec:
                    continue
                name = z[3] or z[2]
                if name not in seen:
                    seen.add(name)
                    counts[name] += 1
                    lines[name].add(line)
                    spoje.add((line, sp))
    return dict(counts), {k: sorted(v) for k, v in lines.items()}, len(spoje)


# ---------- main ----------

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--vfr', required=True)
    ap.add_argument('--osm', required=True)
    ap.add_argument('--jdf', required=True)
    ap.add_argument('--datum', default='2026-11-03')
    ap.add_argument('--diag', action='store_true')
    a = ap.parse_args()

    v = load_vfr(a.vfr)
    osm, osm_ts = load_osm(a.osm)
    polys = v['obec']['polys']

    # --- kontrola převodu: definiční bod obce a adresní body převzaté do OSM z RÚIAN ---
    am_by_kod = {m['kod']: m for m in v['am']}
    diffs = []
    for o in osm.values():
        k = o['tags'].get('ref:ruian:addr')
        if k in am_by_kod and o['tags'].get('source:addr', 'cuzk:ruian').startswith('cuzk') and o['lat']:
            x, y = am_by_kod[k]['bod']
            lat, lon = sjtsk_to_wgs84(x, y)
            diffs.append(distance_m(lat, lon, o['lat'], o['lon']))
    diffs.sort()
    dlat, dlon = sjtsk_to_wgs84(*v['obec']['db'])
    place = osm.get('node/1601416118') or PLACE_NODE
    check = {
        'adresni_body_porovnano': len(diffs),
        'odchylka_median_m': round(statistics.median(diffs), 2) if diffs else None,
        'odchylka_p95_m': round(diffs[int(0.95 * (len(diffs) - 1))], 2) if diffs else None,
        'odchylka_max_m': round(diffs[-1], 2) if diffs else None,
        'podil_do_0_1_m_pct': round(100 * sum(1 for d in diffs if d <= 0.1) / len(diffs), 1) if diffs else None,
        'podil_do_1_m_pct': round(100 * sum(1 for d in diffs if d <= 1) / len(diffs), 1) if diffs else None,
        'definicni_bod_obce_wgs84': [rnd(dlat), rnd(dlon)],
    }
    if place:
        check['definicni_bod_vs_osm_place_m'] = round(distance_m(dlat, dlon, place['lat'], place['lon']), 2)

    # --- 1. hranice ---
    # stejné hranice se mohou lišit jen počátečním vrcholem prstence -> porovnáváme množiny vrcholů
    vert = lambda ps: (len(ps), sorted(len(r) for p in ps for r in p), set(pt for p in ps for r in p for pt in r))
    same = vert(v['obec']['polys']) == vert(v['ku']['polys'])
    hran = [feature(polys_to_geojson(v['obec']['polys']),
                    {'druh': 'obec a katastrální území' if same else 'obec', 'nazev': v['obec']['nazev'],
                     'kod_obce': v['obec']['kod'], 'kod_ku': v['ku']['kod'], 'shodna_s_ku': same})]
    if not same:
        hran.append(feature(polys_to_geojson(v['ku']['polys']),
                            {'druh': 'katastrální území', 'nazev': v['ku']['nazev'], 'kod': v['ku']['kod']}))
    write_geojson('mapa_hranice.geojson', hran, {
        'zdroj': f"RÚIAN, výměnný formát OB_{v['obec']['kod']}_UKSH, stav {v['datum']}",
        'pozn': ('Hranice obce a katastrálního území ' + v['ku']['nazev'] + f" (kód {v['ku']['kod']}) "
                 + ('jsou totožné.' if same else 'se liší.'))})

    # --- 2. čtverce ---
    houses = [s for s in v['so'].values() if is_house(s)]
    cells_f, cells, groups, gattrs = build_cells(houses)
    write_geojson('mapa_ctverce.geojson', cells_f, {
        'zdroj': f"RÚIAN, definiční body stavebních objektů, stav {v['datum']}",
        'sit': 'čtverce 100 × 100 m v souřadnicích S-JTSK (EPSG:5514), převedené do WGS84',
        'dum': 'rodinný nebo bytový dům (způsob využití 6, 7) nebo jiná budova s č. p. a s byty',
        'ochrana': (f'čtverce s méně než {K_MIN} domy nemají vlastní atributy; malé čtverce téhož bloku 300 × 300 m '
                    f'se slučují do skupiny (skupina_*), pokud má aspoň {K_MIN} domy; jinak bez atributů'),
        'podily': 'v % z domů se zjištěným údajem (bez kódů 8 nedefinováno a 9 nezjištěno)'})
    t = totals(houses)
    n_small = sum(1 for hs in cells.values() if len(hs) < K_MIN)
    t.update({'ctverce': len(cells), 'ctverce_male': n_small,
              'domy_v_malych_ctvercich': sum(len(hs) for hs in cells.values() if len(hs) < K_MIN),
              'max_domu_ve_ctverci': max(len(hs) for hs in cells.values()),
              'skupiny': len(gattrs),
              'domy_ve_skupinach': sum(a['skupina_domy'] for a in gattrs.values()),
              'domy_bez_atributu': sum(len(cells[c]) for g, m in groups.items() if g not in gattrs for c in m)})

    # --- 3. veřejná místa ---
    def am_point(cislo, typ):
        for m in v['am']:
            s = v['so'].get(m['so'])
            if m['cislo'] == cislo and s and s['typ'] == typ:
                return m, s
        return None, None

    def parcel_point(kmen, pod, druh='2'):
        for p in v['par']:
            if p['kmen'] == kmen and p['pod'] == pod and p['druh_cisl'] == druh:
                return p
        return None

    mista = []

    def add(nazev, druh, xy, zdroj, popis, wgs=False):
        """xy: (x, y) v S-JTSK, nebo (lat, lon) ve WGS84 při wgs=True."""
        lat, lon = xy if wgs else sjtsk_to_wgs84(*xy)
        mista.append(feature({'type': 'Point', 'coordinates': [rnd(lon), rnd(lat)]},
                             {'nazev': nazev, 'druh': druh, 'zdroj_polohy': zdroj, 'popis': popis}))

    for cislo, nazev, druh, popis in (
            ('212', 'Obecní úřad', 'úřad', 'Sídlo obce, č. p. 212. V budově je pobočka Místní knihovny Dobrá.'),
            ('232', 'Obecní dům', 'kultura', 'Sál, extrovna a hospoda, klubovna Klubu žen; volební místnost. Rekonstrukce 2025–2026.'),
            ('78', 'Mateřská škola', 'škola', 'MŠ Horní Domaslavice, příspěvková organizace (sídlo č. p. 78). U MŠ je veřejně přístupné dětské hřiště (dotace MMR 2021).')):
        m, s = am_point(cislo, '1')
        if m:
            add(nazev, druh, m['bod'], f'RÚIAN, adresní místo č. p. {cislo} (kód {m["kod"]})', popis)
    m, s = am_point('346', '2')
    if m:
        add('Hasičská klubovna', 'hasiči', m['bod'], f'RÚIAN, adresní místo č. ev. 346 (kód {m["kod"]})',
            'Klubovna SDH, stavba č. ev. 346 (zápis ZO č. 32 a 27/2026).')

    # kostel: budova RÚIAN, kterou OSM označuje jako kostel sv. Jakuba
    for key, o in osm.items():
        tg = o['tags']
        if tg.get('building') == 'church' and 'Jakuba' in tg.get('name', ''):
            s = v['so'].get(tg.get('ref:ruian:building', ''))
            if s:
                add('Kostel sv. Jakuba Staršího', 'církev', s['db'],
                    f"RÚIAN, definiční bod stavebního objektu {s['kod']}; určení budovy podle OpenStreetMap ({key})",
                    'Kulturní památka (ÚSKP 49841/8-3986), farnost Domaslavice.')
            else:
                add('Kostel sv. Jakuba Staršího', 'církev', (o['lat'], o['lon']),
                    f'OpenStreetMap ({key}), budova převzatá z RÚIAN', 'Kulturní památka, farnost Domaslavice.', wgs=True)

    # hřbitov: plochy v OSM (zdroj geometrie cuzk:ruian); bod = těžiště plochy
    for key, nazev, popis in (
            ('way/304710748', 'Hřbitov u kostela',
             'Hřbitov kolem kostela sv. Jakuba; obec vydává hřbitovní řád. Oplocení 2018, chodníky uvnitř hřbitova 2019.'),
            ('way/304710902', 'Hřbitov (druhá plocha)',
             'Druhá hřbitovní plocha východně od kostela. Obě plochy spojuje „chodník mezi hřbitovy“ podél MK 6 (2018).')):
        o = osm.get(key)
        if o:
            add(nazev, 'hřbitov', (o['lat'], o['lon']),
                f'OpenStreetMap ({key}), těžiště plochy převzaté z katastru (source=cuzk:ruian)', popis, wgs=True)

    # dětské hřiště za Obecním domem
    o = osm.get('way/1568511595')
    if o:
        add('Dětské hřiště', 'hřiště', (o['lat'], o['lon']), 'OpenStreetMap (way/1568511595), těžiště plochy leisure=playground',
            'Dětské hřiště za Obecním domem (dotace MMR 2017).', wgs=True)

    # staveniště víceúčelového hřiště: pozemek parc. č. 249/3
    p = parcel_point('249', '3')
    if p:
        add('Víceúčelové hřiště (staveniště)', 'hřiště', p['db'],
            'RÚIAN, definiční bod parcely 249/3 (parcelní číslo podle zprávy o uplatňování ÚP)',
            'Ve výstavbě, dokončení plánováno na 11/2026 (36 × 18 m).')

    # hasičská zbrojnice: OSM bod z databáze ZABAGED; kontrola: pozemky 1010/44 a 1010/80, které zápis ZO
    # 2/2025 popisuje jako „pozemky u hasičské zbrojnice“, musí ležet do 50 m
    o = osm.get('node/13992958592')
    near = []
    for kmen, pod in (('1010', '44'), ('1010', '80')):
        p = parcel_point(kmen, pod)
        if p and o:
            near.append(round(distance_m(o['lat'], o['lon'], *sjtsk_to_wgs84(*p['db'])), 1))
    check['zbrojnice_osm_vs_parcely_1010_44_80_m'] = near
    if o and len(near) == 2 and max(near) < 50:
        add('Hasičská zbrojnice', 'hasiči', (o['lat'], o['lon']),
            'OpenStreetMap (node/13992958592, amenity=fire_station, převzato ze ZABAGED); kontrola: definiční body '
            f'parcel 1010/44 a 1010/80 „u hasičské zbrojnice“ (zápis ZO 2/2025) leží {near[0]:.0f} a {near[1]:.0f} m od bodu',
            'Zbrojnice JSDH, rekonstrukce 2018 (dotace MSK).', wgs=True)

    # příznak, zda bod leží uvnitř hranice obce (test v WGS84)
    wgs_polys = [[[tuple(c) for c in r] for r in p] for p in polys_to_geojson(polys)['coordinates']]
    for f in mista:
        lon, lat = f['geometry']['coordinates']
        f['properties']['v_obci'] = point_in_polys((lon, lat), [[r[:-1] for r in p] for p in wgs_polys])
    write_geojson('mapa_mista.geojson', mista, {'zdroj': 'RÚIAN (stav ' + v['datum'] + '), OpenStreetMap (' + osm_ts + ')'})

    # --- 4. zastávky ---
    counts, lines, n_spoje = stop_counts(a.jdf, a.datum)
    jdf_names = sorted(counts)
    zast = []
    found = set()
    for key, o in sorted(osm.items()):
        tg = o['tags']
        nm = tg.get('name', '')
        if not nm.startswith('Horní Domaslavice, ') or tg.get('public_transport') != 'platform':
            continue
        sub = nm.split(', ', 1)[1]
        match = [j for j in jdf_names if j.lower() == sub.lower()]
        if not match or match[0] in found:
            continue
        found.add(match[0])
        zast.append(feature({'type': 'Point', 'coordinates': [rnd(o['lon']), rnd(o['lat'])]},
                            {'nazev': 'Horní Domaslavice, ' + match[0], 'spoje_pracovni_den': counts[match[0]],
                             'linky': lines[match[0]], 'zdroj_polohy': f'OpenStreetMap ({key})',
                             'zdroj_spoju': f'JDF jízdní řády, {a.datum} (úterý)'}))
    write_geojson('mapa_zastavky.geojson', zast, {'datum_jr': a.datum})
    chybi = [j for j in jdf_names if j not in found]

    souhrn = {'obec': v['obec']['nazev'], 'kod_obce': v['obec']['kod'], 'kod_ku': v['ku']['kod'],
              'stav_ruian': v['datum'], 'osm_stav': osm_ts, 'zastavba': t, 'prevod': check,
              'zastavky_jdf': {j: counts[j] for j in jdf_names}, 'zastavky_bez_polohy': chybi,
              'spoje_v_obci_celkem': n_spoje, 'hranice_obce_a_ku_shodne': same}
    with open(os.path.join(ROOT, 'data', 'mapa_souhrn.json'), 'w', encoding='utf-8') as f:
        json.dump(souhrn, f, ensure_ascii=False, indent=1)
        f.write('\n')
    print(json.dumps(souhrn, ensure_ascii=False, indent=1))
    js = os.path.join(ROOT, 'static', 'mapa-data.js')
    with open(js, 'w', encoding='utf-8') as f:
        f.write('/* Generováno tools/mapa_data.py – neupravovat ručně. Totéž co data/mapa_*.geojson. */\n')
        f.write('window.HD_MAPA = ' + json.dumps(BUNDLE, ensure_ascii=False, separators=(',', ':')) + ';\n')
    print(f'static/mapa-data.js: {os.path.getsize(js) / 1024:.0f} kB')

    if a.diag:
        from collections import Counter
        print('rozdělení počtu domů ve čtvercích:', sorted(Counter(len(h) for h in cells.values()).items()))
        for f in mista:
            print(f['properties']['nazev'], f['geometry']['coordinates'], f['properties']['v_obci'])
        for s in v['so'].values():
            if s['vyuziti'] == '15':
                print('SO 15', s['kod'], s['cisla'], sjtsk_to_wgs84(*s['db']))


if __name__ == '__main__':
    main()
