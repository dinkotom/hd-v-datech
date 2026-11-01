"""Page charts inserted at <!--chart:KEY--> markers in obsah/*.md.

Each chart is an inline SVG styled by CSS classes from static/style.css, with
data-tip hover targets and a table view, matching the charts in build.py.
"""
import collections
import csv
import html
import math
import os

ROOT = os.path.dirname(os.path.abspath(__file__))
OBCE = ['Horní Domaslavice', 'Pazderna', 'Dolní Domaslavice', 'Lučina', 'Vojkovice']
SHORT = {'Horní Domaslavice': 'HD', 'Pazderna': 'Pazderna', 'Dolní Domaslavice': 'Dolní Dom.', 'Lučina': 'Lučina', 'Vojkovice': 'Vojkovice', 'Písková Lhota': 'Písk. Lhota', 'Rebešovice': 'Rebešovice', 'Závišice': 'Závišice'}


def esc(s):
    return html.escape(str(s), quote=True)


def num(v, dec=0):
    return f'{v:,.{dec}f}'.replace(',', ' ').replace('.', ',')


def read_csv(name):
    with open(os.path.join(ROOT, 'data', name), encoding='utf-8') as f:
        return list(csv.DictReader(f))


def nice_scale(lo, hi, max_ticks=5):
    span = hi - lo
    if span <= 0:
        return lo, hi + 1, 1
    mag = 10 ** math.floor(math.log10(span))
    for m in (0.1, 0.2, 0.25, 0.5, 1, 2, 2.5, 5, 10):
        step = m * mag
        a, b = math.floor(lo / step) * step, math.ceil(hi / step) * step
        if (b - a) / step <= max_ticks:
            return a, b, step
    return lo, hi, span


def table_view(headers, rows):
    th = ''.join(f'<th>{esc(h)}</th>' for h in headers)
    trs = ''.join('<tr>' + ''.join(f'<td>{esc(c)}</td>' for c in r) + '</tr>' for r in rows)
    return f'<details><summary>Zobrazit jako tabulku</summary><table><thead><tr>{th}</tr></thead><tbody>{trs}</tbody></table></details>'


def legend(items):
    """items: [(label, css class, shape)] shape: 'sq' | 'line'"""
    out = []
    for lab, cls, shape in items:
        sw = f'<i class="lg-{shape} {cls}"></i>'
        out.append(f'<span class="lg">{sw}{esc(lab)}</span>')
    return '<div class="legend">' + ''.join(out) + '</div>'


def figure(title, sub, svg, table, leg=''):
    return (f'<figure class="chart"><h3>{esc(title)}</h3><p class="sub">{esc(sub)}</p>'
            f'{leg}{svg}{table}</figure>')


# ---------- chart types ----------

def stacked_columns(title, sub, xs, series, unit, dec=1, label_every=1, total_label=True):
    """series: [(name, values, css class)] stacked bottom-up; values may be negative (drawn below 0)."""
    W, H, l, b, t = 640, 250, 50, 26, 14
    pos = [sum(max(0, s[1][i]) for s in series) for i in range(len(xs))]
    neg = [sum(min(0, s[1][i]) for s in series) for i in range(len(xs))]
    lo, hi, step = nice_scale(min(0, min(neg)), max(pos))
    pw, ph = W - l - 8, H - b - t
    py = lambda v: t + ph - ph * (v - lo) / (hi - lo)
    slot = pw / len(xs)
    cw = max(4, slot * 0.72)
    out = [f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="{esc(title)}">']
    v = lo
    while v <= hi + 1e-9:
        out.append(f'<line class="grid" x1="{l}" y1="{py(v):.1f}" x2="{W - 8}" y2="{py(v):.1f}"/>')
        out.append(f'<text x="{l - 6}" y="{py(v) + 4:.1f}" text-anchor="end">{num(v, 0 if step >= 1 else 1)}</text>')
        v += step
    for i, x in enumerate(xs):
        cx = l + i * slot + (slot - cw) / 2
        up, down = 0.0, 0.0
        tip = [f'{x}']
        for name, vals, cls in series:
            val = vals[i]
            tip.append(f'{name}: {num(val, dec)} {unit}')
            if val >= 0:
                y0, y1 = py(up), py(up + val)
                up += val
            else:
                y0, y1 = py(down + val), py(down)
                down += val
            h = abs(y0 - y1)
            if h > 0.5:
                out.append(f'<rect class="{cls}" x="{cx:.1f}" y="{min(y0, y1):.1f}" width="{cw:.1f}" height="{max(0, h - 1.5):.1f}" rx="2"/>')
        if total_label and len(xs) <= 16 and up > 0:
            out.append(f'<text class="val small" x="{cx + cw / 2:.1f}" y="{py(up) - 4:.1f}" text-anchor="middle">{num(up, dec)}</text>')
        out.append(f'<rect class="hit" x="{l + i * slot:.1f}" y="{t}" width="{slot:.1f}" height="{ph}" data-tip="{esc(" · ".join(tip))}"/>')
        if i % label_every == 0 or i == len(xs) - 1:
            out.append(f'<text x="{cx + cw / 2:.1f}" y="{H - 8}" text-anchor="middle">{esc(x)}</text>')
    out.append(f'<line class="axis" x1="{l}" y1="{py(0):.1f}" x2="{W - 8}" y2="{py(0):.1f}"/>')
    out.append('</svg>')
    tv = table_view(['Rok'] + [s[0] for s in series], [[x] + [num(s[1][i], dec) for s in series] for i, x in enumerate(xs)])
    leg = legend([(s[0], s[2], 'sq') for s in series]) if len(series) > 1 else ''
    return figure(title, sub, ''.join(out), tv, leg)


def lines_highlight(title, sub, xs, series, unit, dec=0, label_every=5, hl='Horní Domaslavice', index_note=''):
    """series: {name: [values]}; the highlighted municipality in accent, the others recessive."""
    W, H, l, b, t, r = 640, 270, 50, 26, 14, 128
    allv = [v for vals in series.values() for v in vals if v is not None]
    lo, hi, step = nice_scale(min(0, min(allv)), max(allv))
    pw, ph = W - l - r, H - b - t
    px = lambda i: l + pw * i / (len(xs) - 1)
    py = lambda v: t + ph - ph * (v - lo) / (hi - lo)
    out = [f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="{esc(title)}">']
    v = lo
    while v <= hi + 1e-9:
        out.append(f'<line class="grid" x1="{l}" y1="{py(v):.1f}" x2="{l + pw}" y2="{py(v):.1f}"/>')
        out.append(f'<text x="{l - 6}" y="{py(v) + 4:.1f}" text-anchor="end">{num(v, 0)}</text>')
        v += step
    order = [n for n in series if n != hl] + [hl]
    ends = []
    for n in order:
        vals = series[n]
        pts = ' '.join(f'{px(i):.1f},{py(val):.1f}' for i, val in enumerate(vals) if val is not None)
        cls = 'line' if n == hl else 'line-other'
        out.append(f'<polyline class="{cls}" points="{pts}"/>')
        last = max(i for i, val in enumerate(vals) if val is not None)
        ends.append([py(vals[last]), n, vals[last], px(last)])
    # direct labels at line ends, nudged apart
    ends.sort()
    for k in range(1, len(ends)):
        if ends[k][0] - ends[k - 1][0] < 14:
            ends[k][0] = ends[k - 1][0] + 14
    for y, n, val, x in ends:
        cls = 'val' if n == hl else ''
        out.append(f'<text class="{cls}" x="{x + 6:.1f}" y="{y + 4:.1f}">{esc(SHORT.get(n, n))} {num(val, dec)}</text>')
    out.append(f'<circle class="s1" cx="{ends[[e[1] for e in ends].index(hl)][3]:.1f}" cy="{py(series[hl][-1]):.1f}" r="4"/>' if series[hl][-1] is not None else '')
    for i, x in enumerate(xs):
        if i % label_every == 0 or i == len(xs) - 1:
            out.append(f'<text x="{px(i):.1f}" y="{H - 8}" text-anchor="middle">{esc(x)}</text>')
        sw = pw / (len(xs) - 1)
        tip = f'{x}: ' + ' · '.join(f'{SHORT.get(n, n)} {num(series[n][i], dec)}' for n in series if series[n][i] is not None)
        out.append(f'<rect class="hit" x="{px(i) - sw / 2:.1f}" y="{t}" width="{sw:.1f}" height="{ph}" data-tip="{esc(tip + " " + unit)}"/>')
    out.append(f'<line class="axis" x1="{l}" y1="{py(lo):.1f}" x2="{l + pw}" y2="{py(lo):.1f}"/>')
    out.append('</svg>')
    tv = table_view(['Rok'] + list(series), [[x] + [num(series[n][i], dec) if series[n][i] is not None else '' for n in series] for i, x in enumerate(xs)])
    leg = legend([(hl, 's1', 'line'), ('ostatní obce', 'so', 'line')])
    return figure(title, sub, ''.join(out), tv, leg)


def stacked100(title, sub, rows, cats):
    """rows: [(label, [values])]; cats: [(name, css class)]"""
    W, lw, rh, gap = 640, 150, 30, 12
    H = len(rows) * (rh + gap) + 4
    out = [f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="{esc(title)}">']
    pw = W - lw - 8
    for i, (lab, vals) in enumerate(rows):
        y = i * (rh + gap) + 2
        tot = sum(vals) or 1
        x = lw
        out.append(f'<text x="{lw - 10}" y="{y + rh / 2 + 4}" text-anchor="end">{esc(lab)}</text>')
        for (name, cls), v in zip(cats, vals):
            w = pw * v / tot
            if w <= 0:
                continue
            pct = 100 * v / tot
            out.append(f'<rect class="{cls}" x="{x:.1f}" y="{y}" width="{max(0, w - 2):.1f}" height="{rh}" rx="2" data-tip="{esc(f"{lab} · {name}: {num(v, 1)} ha ({num(pct, 0)} %)")}"/>')
            if pct >= 9:
                out.append(f'<text class="in{" dark" if cls == "c4" else ""}" x="{x + w / 2 - 1:.1f}" y="{y + rh / 2 + 4}" text-anchor="middle">{num(pct, 0)} %</text>')
            x += w
    out.append('</svg>')
    tv = table_view(['Obec'] + [c[0] for c in cats], [[lab] + [num(v, 1) for v in vals] for lab, vals in rows])
    return figure(title, sub, ''.join(out), tv, legend([(c[0], c[1], 'sq') for c in cats]))


def bullet(title, sub, rows, unit='mil. Kč', dec=2):
    """rows: [(label, plan, actual)] – plan as a light track, actual as the accent bar."""
    W, lw, rh, gap = 640, 210, 20, 16
    vmax = max(max(p, a) for _, p, a in rows) or 1
    pw = W - lw - 120
    H = len(rows) * (rh + gap) + 4
    out = [f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="{esc(title)}">']
    for i, (lab, plan, act) in enumerate(rows):
        y = i * (rh + gap) + 2
        wp, wa = pw * plan / vmax, pw * act / vmax
        pct = 100 * act / plan if plan else 0
        out.append(f'<text x="{lw - 10}" y="{y + rh / 2 + 4}" text-anchor="end">{esc(lab)}</text>')
        out.append(f'<rect class="track" x="{lw}" y="{y}" width="{max(wp, 1):.1f}" height="{rh}" rx="3"/>')
        if wa > 0:
            out.append(f'<rect class="s1" x="{lw}" y="{y + 4}" width="{wa:.1f}" height="{rh - 8}" rx="2"/>')
        out.append(f'<text class="val" x="{lw + max(wp, wa) + 6:.1f}" y="{y + rh / 2 + 4}">{num(act, dec)} z {num(plan, dec)} ({num(pct, 0)} %)</text>')
        out.append(f'<rect class="hit" x="0" y="{y - 4}" width="{W}" height="{rh + 8}" data-tip="{esc(f"{lab}: zaplaceno {num(act, dec)} z {num(plan, dec)} {unit} ({num(pct, 0)} %)")}"/>')
    out.append(f'<line class="axis" x1="{lw}" y1="0" x2="{lw}" y2="{H}"/>')
    out.append('</svg>')
    tv = table_view(['Položka', f'Rozpočet ({unit})', f'Skutečnost ({unit})', 'Plnění'],
                    [[l, num(p, dec), num(a, dec), f'{num(100 * a / p if p else 0, 0)} %'] for l, p, a in rows])
    leg = legend([('rozpočet po změnách', 'track', 'sq'), ('zaplaceno k 30. 9. 2026', 's1', 'sq')])
    return figure(title, sub, ''.join(out), tv, leg)


def hbar(title, sub, rows, unit, dec=0, hl=None):
    W, lw, rh, gap = 640, 210, 22, 8
    vmax = max(v for _, v in rows) or 1
    pw = W - lw - 70
    H = len(rows) * (rh + gap) + 4
    out = [f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="{esc(title)}">']
    for i, (lab, v) in enumerate(rows):
        y = i * (rh + gap) + 2
        w = pw * v / vmax
        cls = 's1' if (hl is None or lab == hl) else 'so'
        out.append(f'<text x="{lw - 10}" y="{y + rh / 2 + 4}" text-anchor="end">{esc(lab)}</text>')
        if w > 0:
            out.append(f'<rect class="{cls}" x="{lw}" y="{y}" width="{w:.1f}" height="{rh}" rx="3"/>')
        out.append(f'<text class="val" x="{lw + w + 6:.1f}" y="{y + rh / 2 + 4}">{num(v, dec)}</text>')
        out.append(f'<rect class="hit" x="0" y="{y - 3}" width="{W}" height="{rh + 6}" data-tip="{esc(f"{lab}: {num(v, dec)} {unit}")}"/>')
    out.append(f'<line class="axis" x1="{lw}" y1="0" x2="{lw}" y2="{H}"/>')
    out.append('</svg>')
    return figure(title, sub, ''.join(out), table_view(['Položka', unit], [[l, num(v, dec)] for l, v in rows]))


# ---------- data-bound charts ----------

def _fin(obec_file):
    return read_csv(obec_file)


FIN_FILES = {'Horní Domaslavice': 'finance_HD_2010-2025.csv', 'Pazderna': 'finance_PAZ_2010-2025.csv',
             'Dolní Domaslavice': 'finance_DD_2010-2025.csv', 'Lučina': 'finance_LUC_2010-2025.csv',
             'Vojkovice': 'finance_VOJ_2010-2025.csv'}
MF = 'Zdroj: Monitor státní pokladny MF.'


def c_hd_io_roky():
    r = _fin(FIN_FILES['Horní Domaslavice'])
    xs = [x['rok'] for x in r]
    return stacked_columns('Investice a opravy obce po letech', 'Mil. Kč; investice (třída 6) a opravy (položka 5171). ' + MF, xs,
                           [('Investice', [float(x['investice']) / 1e6 for x in r], 'c1'),
                            ('Opravy', [float(x['opravy']) / 1e6 for x in r], 'c2')], 'mil. Kč', label_every=3)


def c_hd_dotace_roky():
    r = _fin(FIN_FILES['Horní Domaslavice'])
    xs = [x['rok'] for x in r]
    return stacked_columns('Přijaté dotace po letech', 'Mil. Kč; investiční a neinvestiční transfery (bez souhrnné dotace na výkon státní správy a školství). ' + MF, xs,
                           [('Investiční dotace', [float(x['dotace_inv']) / 1e6 for x in r], 'c1'),
                            ('Neinvestiční dotace', [float(x['dotace_neinv']) / 1e6 for x in r], 'c3')], 'mil. Kč', label_every=3)


def c_hd_prijmy_roky():
    r = _fin(FIN_FILES['Horní Domaslavice'])
    xs = [x['rok'] for x in r]
    rud = [float(x['rud']) / 1e6 for x in r]
    dzn = [float(x['dan_nemovitosti']) / 1e6 for x in r]
    ost = [float(x['trida1']) / 1e6 - a - b for x, a, b in zip(r, rud, dzn)]
    return stacked_columns('Daňové příjmy obce po letech', 'Mil. Kč; sdílené daně (RUD), daň z nemovitých věcí a ostatní daně a poplatky. ' + MF, xs,
                           [('Sdílené daně (RUD)', rud, 'c1'), ('Daň z nemovitých věcí', dzn, 'c2'),
                            ('Ostatní daně a poplatky', ost, 'c3')], 'mil. Kč', label_every=3)


def c_hd_ucty():
    r = _fin(FIN_FILES['Horní Domaslavice'])
    xs = [x['rok'] for x in r]
    return stacked_columns('Peníze na účtech obce ke konci roku', 'Mil. Kč k 31. 12. (účty 231, 244, 245). ' + MF, xs,
                           [('Peníze na účtech', [float(x['penize_231_244_245']) / 1e6 for x in r], 'c1')], 'mil. Kč', label_every=3)


def c_hd_vydaje_ucel():
    agg = collections.Counter()
    for x in read_csv('vydaje_kategorie_sousede_2010-2025.csv'):
        if x['obec'] == 'Horní Domaslavice' and x['cleneni'] == 'ucel' and 2022 <= int(x['rok']) <= 2025:
            agg[x['kategorie']] += float(x['kc']) / 1e6
    rows = [(k, v) for k, v in agg.most_common() if v >= 0.05]
    return hbar('Na co obec utratila peníze v letech 2022–2025', 'Mil. Kč za čtyři roky podle účelu výdaje. ' + MF, rows, 'mil. Kč', dec=1)


def c_hd_obyvatele():
    r = [x for x in read_csv('souhrn_obyvatel_rocne_2000-2025_sousede_okres_CR.csv') if x['uzemi'] == 'HD']
    xs = [x['rok'] for x in r]
    nat, mig = [], []
    for x in r:
        try:
            nat.append(float(x['narozeni']) - float(x['zemreli']))
            mig.append(float(x['pristehovali']) - float(x['vystehovali']))
        except ValueError:
            nat.append(0.0)
            mig.append(0.0)
    keep = [i for i, x in enumerate(r) if x['narozeni']]
    return stacked_columns('Odkud přibývají obyvatelé', 'Roční přírůstek: saldo stěhování a přirozený přírůstek (narození − zemřelí). Zdroj: ČSÚ.',
                           [xs[i] for i in keep],
                           [('Saldo stěhování', [mig[i] for i in keep], 'c1'), ('Přirozený přírůstek', [nat[i] for i in keep], 'c2')],
                           'osob', dec=0, label_every=4, total_label=False)


def _per_capita_series(key):
    out = {}
    for n in OBCE:
        r = _fin(FIN_FILES[n])
        out[n] = [float(x[key]) / float(x['obyv_31_12']) for x in r]
    return [x['rok'] for x in _fin(FIN_FILES[OBCE[0]])], out


def c_srov_io():
    xs, s = _per_capita_series('io')
    return lines_highlight('Investice a opravy na obyvatele po letech', 'Kč na obyvatele a rok. ' + MF, xs, s, 'Kč', label_every=3)


def c_srov_penize():
    xs, s = _per_capita_series('penize_231_244_245')
    return lines_highlight('Peníze na účtech na obyvatele', 'Kč na obyvatele k 31. 12. ' + MF, xs, s, 'Kč', label_every=3)


def c_srov_dane():
    xs, s = _per_capita_series('trida1')
    return lines_highlight('Daňové příjmy na obyvatele', 'Kč na obyvatele a rok (třída 1). ' + MF, xs, s, 'Kč', label_every=3)


def c_srov_obyv():
    key = {'HD': 'Horní Domaslavice', 'Pazderna': 'Pazderna', 'DD': 'Dolní Domaslavice', 'Lucina': 'Lučina', 'Vojkovice': 'Vojkovice'}
    rows = read_csv('souhrn_obyvatel_rocne_2000-2025_sousede_okres_CR.csv')
    xs = sorted({x['rok'] for x in rows})
    s = {}
    for code, n in key.items():
        vals = {x['rok']: float(x['obyvatel_31_12']) for x in rows if x['uzemi'] == code}
        if not vals:
            continue
        base = vals[xs[0]]
        s[n] = [100 * vals[y] / base if y in vals else None for y in xs]
    s = {n: s[n] for n in OBCE if n in s}
    return lines_highlight('Růst počtu obyvatel (rok 2000 = 100)', 'Počet obyvatel ke 31. 12. jako index proti roku 2000. Zdroj: ČSÚ.', xs, s, '(index)', label_every=5)


def c_srov_plochy():
    agg = collections.defaultdict(lambda: collections.Counter())
    nm = {'HD': 'Horní Domaslavice', 'PA': 'Pazderna', 'DD': 'Dolní Domaslavice', 'LU': 'Lučina', 'VOJ': 'Vojkovice'}
    for x in read_csv('CUZK_UHDP_druhy_pozemku_sousede_2004_2014_2026.csv'):
        if x['rok'] == '2026':
            a = agg[nm[x['obec']]]
            a['orna'] += float(x['orna_ha'])
            a['travni'] += float(x['ttp_ha'])
            a['zahrady'] += float(x['zahrada_ha']) + float(x['sad_ha'])
            a['les'] += float(x['les_ha'])
            a['voda'] += float(x['voda_ha'])
            a['zast'] += float(x['zastavena_ha']) + float(x['ostatni_ha'])
    # colour order validated as adjacent pairs (validate_palette.js, light + dark)
    cats = [('Orná půda', 'c2', 'orna'), ('Louky a pastviny', 'c3', 'travni'), ('Zahrady a sady', 'c4', 'zahrady'),
            ('Les', 'c6', 'les'), ('Vodní plocha', 'c1', 'voda'), ('Zastavěné a ostatní plochy', 'c5', 'zast')]
    rows = [(n, [agg[n][c[2]] for c in cats]) for n in OBCE]
    return stacked100('Z čeho se skládá území obcí (2026)', 'Podíl druhů pozemků z rozlohy obce. Zdroj: ČÚZK, úhrnné hodnoty druhů pozemků k 1. 10. 2026.',
                      rows, [(c[0], c[1]) for c in cats])


def c_srov_dotace():
    rows = []
    for n in OBCE:
        r = _fin(FIN_FILES[n])
        rows.append((n, sum(float(x['dotace_inv']) for x in r if 2011 <= int(x['rok']) <= 2025) / 1e6))
    return hbar('Investiční dotace 2011–2025 celkem', 'Mil. Kč. ' + MF, rows, 'mil. Kč', dec=1, hl='Horní Domaslavice')


def c_rozp_ucel():
    rows = []
    for x in read_csv('rozpocet_2026_vydaje_podle_ucelu.csv'):
        plan, act = float(x['upraveny_2026_kc']) / 1e6, float(x['skutecnost_9_2026_kc']) / 1e6
        if plan >= 0.2 and not x['kategorie'].upper().startswith('CELKEM'):
            rows.append((x['kategorie'].split(' (')[0], plan, act))
    rows.sort(key=lambda r: -r[1])
    return bullet('Výdaje 2026 podle účelu: rozpočet a skutečnost k 30. 9.', 'Mil. Kč; rozpočet po změnách a zaplacené výdaje do konce září. ' + MF, rows)


def c_rozp_ucty():
    r = read_csv('rozpocet_2026_stav_uctu.csv')
    keys = list(r[0].keys())
    xs = [x[keys[0]][:7] for x in r]
    vals = [float(x[keys[-2]]) / 1e6 for x in r]
    return stacked_columns('Peníze na účtech obce po čtvrtletích', 'Mil. Kč na konci čtvrtletí. ' + MF, xs,
                           [('Peníze na účtech', vals, 'c1')], 'mil. Kč', label_every=2)


def c_usn_roky():
    r = read_csv('usneseni_zo_2022-2026.csv')
    years = sorted({x['datum'][:4] for x in r})
    cnt = collections.Counter((x['datum'][:4], x['vysledek']) for x in r)
    return stacked_columns('Usnesení podle roku a výsledku', 'Počet usnesení; zahrnuje i usnesení „bere na vědomí“. Zdroj: zápisy ze zasedání zastupitelstva.', years,
                           [('přijato', [cnt[(y, 'přijato')] for y in years], 'ok'),
                            ('nepřijato', [cnt[(y, 'nepřijato')] for y in years], 'no'),
                            ('neuvedeno', [cnt[(y, 'neuveden v zápisu')] for y in years], 'so')], 'usnesení', dec=0)


def c_usn_temata():
    r = read_csv('usneseni_zo_2022-2026.csv')
    cnt = collections.Counter()
    for x in r:
        for t in x['tema'].split(';'):
            if t.strip():
                cnt[t.strip()] += 1
    return hbar('Usnesení podle tématu', 'Počet usnesení; jedno usnesení může mít dvě témata. Zdroj: zápisy ze zasedání zastupitelstva.',
                cnt.most_common(), 'usnesení')


PODOBNE = ['Horní Domaslavice', 'Písková Lhota', 'Rebešovice', 'Závišice']
POD_FILES = {'Horní Domaslavice': 'finance_HD_2010-2025.csv', 'Písková Lhota': 'finance_PL_2010-2025.csv',
             'Rebešovice': 'finance_REB_2010-2025.csv', 'Závišice': 'finance_ZAV_2010-2025.csv'}


def _pod_series(key, per):
    out = {}
    for n in PODOBNE:
        r = _fin(POD_FILES[n])
        out[n] = [float(x[key]) / float(x[per]) for x in r]
    return [x['rok'] for x in _fin(POD_FILES[PODOBNE[0]])], out


def c_pod_obyv():
    rows = read_csv('podobne_obce_obyvatele_2000-2025.csv')
    xs = sorted({x['rok'] for x in rows})
    s = {n: [float(x['obyvatel_31_12']) for x in rows if x['obec'] == n] for n in PODOBNE}
    return lines_highlight('Počet obyvatel 2000–2025', 'Stav ke 31. 12. Zdroj: ČSÚ.', xs, s, 'obyvatel', label_every=5)


def c_pod_io():
    xs, s = _pod_series('io', 'obyv_1_7')
    return lines_highlight('Investice a opravy na obyvatele po letech', 'Kč na obyvatele a rok. ' + MF, xs, s, 'Kč', label_every=3)


def c_pod_penize():
    xs, s = _pod_series('penize_231_244_245', 'obyv_31_12')
    return lines_highlight('Peníze na účtech na obyvatele', 'Kč na obyvatele k 31. 12. ' + MF, xs, s, 'Kč', label_every=3)


def c_pod_obdobi():
    v = {(x['obec'], x['ukazatel']): float(x['kc_na_obyv_a_rok']) for x in read_csv('podobne_obce_souhrn_po_obdobich.csv')
         if x['obdobi'] == '2022–2026' and x['kc_na_obyv_a_rok']}
    return hbar('Investice a opravy na obyvatele a rok, 2023–2025',
                'Kč na obyvatele a rok; investice (třída 6) + opravy (položka 5171). ' + MF,
                [(n, v[(n, 'io')]) for n in PODOBNE], 'Kč na obyvatele a rok', hl='Horní Domaslavice')


CHARTS = {
    'pod-obyv': c_pod_obyv, 'pod-io': c_pod_io, 'pod-penize': c_pod_penize, 'pod-obdobi': c_pod_obdobi,
    'hd-io-roky': c_hd_io_roky, 'hd-dotace-roky': c_hd_dotace_roky, 'hd-prijmy-roky': c_hd_prijmy_roky,
    'hd-ucty': c_hd_ucty, 'hd-vydaje-ucel': c_hd_vydaje_ucel, 'hd-obyvatele-pohyb': c_hd_obyvatele,
    'srov-io': c_srov_io, 'srov-penize': c_srov_penize, 'srov-dane': c_srov_dane, 'srov-obyv': c_srov_obyv,
    'srov-plochy': c_srov_plochy, 'srov-dotace': c_srov_dotace,
    'rozp-ucel': c_rozp_ucel, 'rozp-ucty': c_rozp_ucty,
    'usn-roky': c_usn_roky, 'usn-temata': c_usn_temata,
}
