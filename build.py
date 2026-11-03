"""Build the static site into docs/ (served by Cloudflare Pages).

Usage: /usr/bin/python3 -I build.py
Markdown pages live in obsah/, datasets in data/, images in img/.
"""
import base64
import csv
import hashlib
import html
import json
import os
import re
import shutil
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import charts  # noqa: E402
import slovnik  # noqa: E402

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, 'docs')
SITE = 'Horní Domaslavice v datech'
UPDATED = '3. 11. 2026'
REPO_URL = 'https://github.com/dinkotom/hd-v-datech'
DOMAIN = 'hd-v-datech.cz'
SITE_URL = f'https://{DOMAIN}/'
LICENSE_URL = 'https://creativecommons.org/licenses/by/4.0/'
AUTHOR = {'@type': 'Person', 'name': 'Tomáš Dinkov'}
LASTMOD = {}  # slug -> ISO date from front matter, for sitemap.xml

# Inline theme bootstrap (runs before CSS paint); its hash is allowed in the CSP.
THEME_JS = ("try{var t=localStorage.getItem('theme');if(t==='light'||t==='dark')"
            "document.documentElement.setAttribute('data-theme',t)}catch(e){}")

# Google Form for error reports. Fill in after creating the form (see README.md);
# while empty, reports open a prefilled GitHub issue instead.
REPORT_FORM = {
    'action': '',   # https://docs.google.com/forms/d/e/<ID>/formResponse
    'page': '',     # entry.NNNN – Stránka
    'quote': '',    # entry.NNNN – Citovaný text
    'text': '',     # entry.NNNN – Co je špatně
    'source': '',   # entry.NNNN – Správný údaj a zdroj
    'email': '',    # entry.NNNN – E-mail
}

NAV = [
    ('Obec v číslech', [
        ('hd-obyvatelstvo', 'Obyvatelstvo'),
        ('hd-prijmy', 'Příjmy ze sdílených daní'),
        ('hd-rozpocet-2026', 'Rozpočet 2026'),
        ('hd-vydaje', 'Výdaje, investice a opravy'),
        ('hd-ucty', 'Peníze na účtech'),
        ('hd-majetek', 'Majetek a účetnictví'),
        ('hd-dotace', 'Dotace'),
        ('hd-zakazky', 'Veřejné zakázky'),
        ('hd-registr-smluv', 'Registr smluv'),
        ('hd-vystavba', 'Výstavba a infrastruktura'),
        ('hd-skolstvi-socialni', 'Školství, sociální data, ovzduší'),
        ('hd-spolky', 'Spolky a subjekty'),
        ('hd-volby', 'Volby'),
        ('hd-usneseni', 'Usnesení zastupitelstva'),
        ('mapa', 'Mapa obce'),
    ]),
    ('Srovnání se sousedy', [
        ('srovnani-souhrn', 'Souhrn srovnání'),
        ('srovnani-finance', 'Finance'),
        ('srovnani-majetek-zakazky', 'Majetek, smlouvy, zakázky'),
        ('srovnani-obyvatelstvo-vystavba', 'Obyvatelstvo a výstavba'),
        ('srovnani-skolstvi-socialni', 'Školství a sociální data'),
        ('srovnani-volby-spolky', 'Volby a spolky'),
        ('srovnani-plochy', 'Rozloha a druhy pozemků'),
        ('srovnani-zastavba', 'Roztříštěnost zástavby'),
        ('srovnani-dan-nemovitosti', 'Daň z nemovitostí'),
        ('srovnani-vybavenost', 'Občanská vybavenost'),
    ]),
    ('Srovnání s podobnými obcemi', [
        ('srovnani-podobne-obce', 'Souhrn a výběr obcí'),
        ('podobne-finance', 'Finance'),
        ('podobne-majetek-zakazky', 'Majetek, smlouvy, zakázky'),
        ('podobne-obyvatelstvo-vystavba', 'Obyvatelstvo a výstavba'),
        ('podobne-skolstvi-socialni', 'Školství a sociální data'),
        ('podobne-volby-spolky', 'Volby a spolky'),
        ('podobne-plochy', 'Rozloha a druhy pozemků'),
        ('podobne-zastavba', 'Roztříštěnost zástavby'),
        ('podobne-dan-nemovitosti', 'Daň z nemovitostí'),
        ('podobne-vybavenost', 'Občanská vybavenost'),
    ]),
]

OBCE = [('HD', 'Horní Domaslavice'), ('PA', 'Pazderna'), ('DD', 'Dolní Domaslavice'), ('LU', 'Lučina'), ('VOJ', 'Vojkovice')]


# ---------- helpers ----------

def esc(s):
    return html.escape(str(s), quote=True)


def num(v, dec=0):
    s = f'{v:,.{dec}f}'.replace(',', ' ').replace('.', ',')
    return s


def read_csv(name):
    with open(os.path.join(ROOT, 'data', name), encoding='utf-8') as f:
        return list(csv.DictReader(f))


def front_matter(text):
    meta = {}
    if text.startswith('---'):
        end = text.find('\n---', 3)
        for line in text[3:end].strip().splitlines():
            if ':' in line:
                k, v = line.split(':', 1)
                meta[k.strip()] = v.strip().strip('"')
        text = text[end + 4:]
    return meta, text


def md_to_html(text):
    r = subprocess.run(['pandoc', '-f', 'gfm', '-t', 'html5', '--wrap=none'],
                       input=text, capture_output=True, text=True, check=True)
    return r.stdout


def nav_html(current):
    parts = ['<nav class="side" aria-label="Obsah webu">',
             f'<a class="top-link" href="index.html"{" aria-current=page" if current == "index" else ""}>Úvod</a>']
    for group, items in NAV:
        present = [(s, t) for s, t in items if os.path.exists(os.path.join(ROOT, 'obsah', s + '.md'))]
        if not present:
            continue
        is_open = current in [s for s, _ in present] or current == 'index'
        parts.append(f'<details{" open" if is_open else ""}><summary>{esc(group)}</summary><ul>')
        for s, t in present:
            cur = ' aria-current="page"' if s == current else ''
            parts.append(f'<li><a href="{s}.html"{cur}>{esc(t)}</a></li>')
        parts.append('</ul></details>')
    for s, t in [('zeptejte-se-ai', 'Zeptejte se AI'), ('data', 'Data ke stažení'), ('opravy', 'Opravy'), ('o-webu', 'O webu a metodika')]:
        cur = ' aria-current="page"' if s == current else ''
        parts.append(f'<a class="top-link" href="{s}.html"{cur}>{t}</a>')
    parts.append('</nav>')
    return '\n'.join(parts)


def body_attrs():
    a = f' data-repo="{esc(REPO_URL)}"'
    for k, v in REPORT_FORM.items():
        if v:
            a += f' data-form-{k}="{esc(v)}"'
    return a


def page_url(slug):
    # Cloudflare Pages serves /x.html as /x (308), so canonical URLs have no extension
    return SITE_URL if slug == 'index' else SITE_URL + slug


def page(slug, title, body, description='', lede='', jsonld=None):
    desc = esc(description or lede or SITE)
    head_title = SITE if slug == 'index' else f'{title} – {SITE}'
    lede_html = f'<p class="lede">{esc(lede)}</p>' if lede else ''
    alt_md = f'<link rel="alternate" type="text/markdown" href="{slug}.md">\n' if os.path.exists(os.path.join(OUT, slug + '.md')) else ''
    if slug == '404':
        seo = '<meta name="robots" content="noindex">\n'
    else:
        url = page_url(slug)
        seo = f'''<link rel="canonical" href="{url}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{SITE}">
<meta property="og:locale" content="cs_CZ">
<meta property="og:title" content="{esc(head_title)}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE_URL}img/og.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
'''
    if jsonld:
        seo += f'<script type="application/ld+json">{json.dumps(jsonld, ensure_ascii=False)}</script>\n'
    return f'''<!doctype html>
<html lang="cs">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(head_title)}</title>
<meta name="description" content="{desc}">
{seo}<link rel="icon" href="static/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="img/apple-touch-icon.png">
<link rel="stylesheet" href="static/style.css">
{alt_md}<script>{THEME_JS}</script>
</head>
<body{body_attrs()}>
<header class="site-header"><div class="inner">
<a class="brand" href="index.html">{SITE} <span>· občanský přehled veřejných dat</span></a>
<button class="theme-toggle" type="button" aria-label="Přepnout světlý a tmavý režim">Světlý / tmavý</button>
</div></header>
<div class="layout">
{nav_html(slug)}
<main>
<h1>{esc(title)}</h1>
{lede_html}
{body}
</main>
</div>
<footer class="site-footer"><div class="inner">
Neoficiální občanský web. Nejde o stránky obce Horní Domaslavice; oficiální web obce je <a href="https://www.hornidomaslavice.cz/">hornidomaslavice.cz</a>.
Web je čistě informační: uvádí fakta z veřejných zdrojů a nepublikuje politická stanoviska (<a href="o-webu.html#nestrannost">závazek nestrannosti</a>).
Data z veřejných zdrojů (ČSÚ, Ministerstvo financí, ČÚZK, volby.cz a další), aktualizováno {UPDATED}. Obsah webu je pod licencí <a href="https://creativecommons.org/licenses/by/4.0/deed.cs">CC BY 4.0</a>.
Našli jste chybu? Použijte tlačítko „Nahlásit chybu“ na konci stránky. · <a href="opravy.html">Opravy</a> · <a href="o-webu.html">O webu a metodika</a>
</div></footer>
<script src="static/app.js"></script>
<script src="static/report.js"></script>
</body>
</html>
'''


# ---------- charts (inline SVG, colors via CSS classes) ----------

def round_bar(x, y, w, h, r=4):
    """Horizontal bar anchored at x, rounded only on the data end."""
    if w <= 0:
        return ''
    r = min(r, w, h / 2)
    return (f'M{x:.1f},{y:.1f} h{w - r:.1f} a{r},{r} 0 0 1 {r},{r} '
            f'v{h - 2 * r:.1f} a{r},{r} 0 0 1 -{r},{r} h-{w - r:.1f} z')


def round_col(x, base, w, h, r=4):
    """Vertical column anchored at baseline, rounded only on top."""
    if h <= 0:
        return ''
    r = min(r, h, w / 2)
    return (f'M{x:.1f},{base:.1f} v-{h - r:.1f} a{r},{r} 0 0 1 {r},-{r} '
            f'h{w - 2 * r:.1f} a{r},{r} 0 0 1 {r},{r} v{h - r:.1f} z')


def table_view(headers, rows):
    th = ''.join(f'<th>{esc(h)}</th>' for h in headers)
    trs = ''.join('<tr>' + ''.join(f'<td>{esc(c)}</td>' for c in r) + '</tr>' for r in rows)
    return f'<details><summary>Zobrazit jako tabulku</summary><table><thead><tr>{th}</tr></thead><tbody>{trs}</tbody></table></details>'


def chart_hbar(title, sub, rows, unit, dec=0):
    """rows: [(label, value, highlight)]"""
    W, lw, rh, gap = 640, 170, 28, 10
    vmax = max(v for _, v, _ in rows) or 1
    plot = W - lw - 90
    H = len(rows) * (rh + gap) + 6
    out = [f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="{esc(title)}">']
    for i, (lab, v, hl) in enumerate(rows):
        y = i * (rh + gap) + 3
        w = plot * v / vmax
        tip = f'{lab}: {num(v, dec)} {unit}'
        out.append(f'<text x="{lw - 10}" y="{y + rh / 2 + 4}" text-anchor="end">{esc(lab)}</text>')
        if w > 0:
            out.append(f'<path class="{"s1" if hl else "so"}" d="{round_bar(lw, y, w, rh)}"/>')
        out.append(f'<text class="val" x="{lw + w + 6}" y="{y + rh / 2 + 4}">{num(v, dec)}</text>')
        out.append(f'<rect class="hit" x="0" y="{y - 4}" width="{W}" height="{rh + 8}" data-tip="{esc(tip)}"/>')
    out.append(f'<line class="axis" x1="{lw}" y1="0" x2="{lw}" y2="{H}"/>')
    out.append('</svg>')
    tv = table_view(['Obec', unit], [(l, num(v, dec)) for l, v, _ in rows])
    return f'<figure class="chart"><h3>{esc(title)}</h3><p class="sub">{esc(sub)}</p>{"".join(out)}{tv}</figure>'


def nice_scale(v, max_ticks=5):
    """Round axis maximum up to a nice step; returns (vmax, step)."""
    import math
    mag = 10 ** math.floor(math.log10(v)) if v > 0 else 1
    for m in (0.1, 0.2, 0.25, 0.5, 1, 2, 2.5, 5, 10):
        step = m * mag
        if math.ceil(v / step) <= max_ticks:
            return math.ceil(v / step) * step, step
    return v, v


def ticks(vmax, step):
    n = round(vmax / step)
    return [step * i for i in range(n + 1)]


def chart_columns(title, sub, xs, ys, unit, dec=1, label_every=1):
    W, H, l, b, t = 640, 230, 46, 26, 10
    vmax, step = nice_scale(max(ys))
    pw, ph = W - l - 8, H - b - t
    n = len(xs)
    slot = pw / n
    cw = max(4, slot - 4)
    out = [f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="{esc(title)}">']
    for tv in ticks(vmax, step):
        y = t + ph - ph * tv / vmax
        out.append(f'<line class="grid" x1="{l}" y1="{y:.1f}" x2="{W - 8}" y2="{y:.1f}"/>')
        out.append(f'<text x="{l - 6}" y="{y + 4:.1f}" text-anchor="end">{num(tv, 0)}</text>')
    base = t + ph
    for i, (x, v) in enumerate(zip(xs, ys)):
        cx = l + i * slot + (slot - cw) / 2
        h = ph * v / vmax
        out.append(f'<path class="s1" d="{round_col(cx, base, cw, h)}"/>')
        out.append(f'<rect class="hit" x="{l + i * slot:.1f}" y="{t}" width="{slot:.1f}" height="{ph}" data-tip="{esc(f"{x}: {num(v, dec)} {unit}")}"/>')
        if i % label_every == 0 or i == n - 1:
            out.append(f'<text x="{cx + cw / 2:.1f}" y="{H - 8}" text-anchor="middle">{esc(x)}</text>')
    out.append(f'<line class="axis" x1="{l}" y1="{base}" x2="{W - 8}" y2="{base}"/>')
    out.append('</svg>')
    tv = table_view(['Rok', unit], [(x, num(v, dec)) for x, v in zip(xs, ys)])
    return f'<figure class="chart"><h3>{esc(title)}</h3><p class="sub">{esc(sub)}</p>{"".join(out)}{tv}</figure>'


def chart_line(title, sub, xs, ys, unit, dec=0, label_every=5):
    W, H, l, b, t = 640, 230, 46, 26, 12
    vmax, step = nice_scale(max(ys))
    pw, ph = W - l - 14, H - b - t
    n = len(xs)
    px = lambda i: l + pw * i / (n - 1)
    py = lambda v: t + ph - ph * v / vmax
    out = [f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="{esc(title)}">']
    for tv in ticks(vmax, step):
        y = py(tv)
        out.append(f'<line class="grid" x1="{l}" y1="{y:.1f}" x2="{W - 14}" y2="{y:.1f}"/>')
        out.append(f'<text x="{l - 6}" y="{y + 4:.1f}" text-anchor="end">{num(tv, 0)}</text>')
    pts = ' '.join(f'{px(i):.1f},{py(v):.1f}' for i, v in enumerate(ys))
    out.append(f'<polyline class="line" points="{pts}"/>')
    out.append(f'<circle class="s1" cx="{px(n - 1):.1f}" cy="{py(ys[-1]):.1f}" r="4"/>')
    out.append(f'<text class="val" x="{px(n - 1) - 6:.1f}" y="{py(ys[-1]) - 9:.1f}" text-anchor="end">{num(ys[-1], dec)}</text>')
    for i, (x, v) in enumerate(zip(xs, ys)):
        if i % label_every == 0 or i == n - 1:
            out.append(f'<text x="{px(i):.1f}" y="{H - 8}" text-anchor="middle">{esc(x)}</text>')
        sw = pw / (n - 1)
        out.append(f'<rect class="hit" x="{px(i) - sw / 2:.1f}" y="{t}" width="{sw:.1f}" height="{ph}" data-tip="{esc(f"{x}: {num(v, dec)} {unit}")}"/>')
    out.append(f'<line class="axis" x1="{l}" y1="{t + ph}" x2="{W - 14}" y2="{t + ph}"/>')
    out.append('</svg>')
    tv = table_view(['Rok', unit], [(x, num(v, dec)) for x, v in zip(xs, ys)])
    return f'<figure class="chart"><h3>{esc(title)}</h3><p class="sub">{esc(sub)}</p>{"".join(out)}{tv}</figure>'


# ---------- pages ----------

def build_index():
    per = {}
    for r in read_csv('souhrn_po_obdobich_sousede.csv'):
        if r['roky'] == '2023–2025':
            per[(r['obec'], r['ukazatel'])] = float(r['kc_na_obyv_a_rok'] or 0)
    names = [n for _, n in OBCE]
    hd = read_csv('finance_HD_2010-2025.csv')
    years = [r['rok'] for r in hd]
    cash = [float(r['penize_231_244_245']) / 1e6 for r in hd]
    io = [float(r['io']) / 1e6 for r in hd]
    pop = [r for r in read_csv('souhrn_obyvatel_rocne_2000-2025_sousede_okres_CR.csv') if r['uzemi'] == 'HD']
    r26 = [r for r in read_csv('rozpocet_2026_investice_opravy.csv') if r['paragraf'].isdigit()]
    io26 = sum(float(r['investice_skutecnost_9_2026_kc'] or 0) + float(r['opravy_5171_skutecnost_9_2026_kc'] or 0) for r in r26) / 1e6
    io26_plan = sum(float(r['investice_upraveny_kc'] or 0) + float(r['opravy_5171_upraveny_kc'] or 0) for r in r26) / 1e6

    tiles = f'''<div class="tiles">
<div class="tile"><div class="v">{num(int(pop[-1]["obyvatel_31_12"]))}</div><div class="l">obyvatel ke konci roku 2025, téměř dvakrát víc než v roce 2000 ({pop[0]["obyvatel_31_12"]})</div></div>
<div class="tile"><div class="v">{num(cash[-1], 1)} mil. Kč</div><div class="l">na účtech obce ke konci roku 2025</div></div>
<div class="tile"><div class="v">{num(per[("Horní Domaslavice", "io")])} Kč</div><div class="l">na investice a opravy na obyvatele a rok (2023–2025); sousední obce 12–31 tis. Kč</div></div>
<div class="tile"><div class="v">0 Kč</div><div class="l">investičních dotací přišlo na účet v letech 2023–2025; v prosinci 2025 obec uzavřela smlouvu s krajem na dotaci až 2,7 mil. Kč</div></div>
<div class="tile"><div class="v">{num(io26, 1)} mil. Kč</div><div class="l">zaplatila obec na investice a opravy v roce 2026 do 30. 9., tedy {num(io26 / io26_plan * 100)} % z plánovaných {num(io26_plan, 1)} mil. Kč</div></div>
</div>'''

    c_io = chart_hbar('Investice a opravy na obyvatele a rok, 2023–2025',
                      'Kč na obyvatele a rok; investice (třída 6) + opravy (položka 5171). Zdroj: Monitor státní pokladny MF.',
                      [(n, per[(n, 'io')], n == names[0]) for n in names], 'Kč na obyvatele a rok')
    c_tax = chart_hbar('Daňové příjmy na obyvatele a rok, 2023–2025',
                       'Kč na obyvatele a rok; třída 1 rozpočtu bez daně z příjmů placené obcí sama sobě (položka 1122). Zdroj: Monitor státní pokladny MF.',
                       [(n, per[(n, 'trida1')], n == names[0]) for n in names], 'Kč na obyvatele a rok')
    c_cash = chart_line('Peníze na účtech obce Horní Domaslavice',
                        'Mil. Kč ke 31. 12. (účty 231, 244, 245). Zdroj: Monitor státní pokladny MF.',
                        years, cash, 'mil. Kč', dec=1, label_every=3)
    c_io_hd = chart_columns('Investice a opravy obce Horní Domaslavice po letech',
                            'Mil. Kč ročně. Zdroj: Monitor státní pokladny MF.',
                            years, io, 'mil. Kč', dec=1, label_every=3)
    c_pop = chart_line('Počet obyvatel Horních Domaslavic',
                       'Stav ke 31. 12. Zdroj: ČSÚ.',
                       [r['rok'] for r in pop], [float(r['obyvatel_31_12']) for r in pop], 'obyvatel', label_every=5)

    def cards(group):
        items = [it for g, its in NAV if g == group for it in its]
        out = []
        for s, t in items:
            p = os.path.join(ROOT, 'obsah', s + '.md')
            if not os.path.exists(p):
                continue
            meta, _ = front_matter(open(p, encoding='utf-8').read())
            out.append(f'<a class="card" href="{s}.html"><b>{esc(t)}</b><span>{esc(meta.get("description", ""))}</span></a>')
        return '<div class="cards">' + ''.join(out) + '</div>'

    body = f'''{tiles}
<div class="note">Tento web je soukromá občanská iniciativa. Shromažďuje veřejně dostupná data o obci Horní Domaslavice
a srovnává je se sousedními obcemi Pazderna, Dolní Domaslavice, Lučina a Vojkovice i s podobnými obcemi odjinud. Nehodnotí osoby, ukazuje čísla a jejich zdroje.
Všechna data lze stáhnout a ověřit. Na data se můžete <a href="zeptejte-se-ai.html">zeptat i svého AI asistenta</a>.</div>
<h2>Hlavní zjištění</h2>
<p>Horní Domaslavice jsou ze sousedních obcí nejrychleji rostoucí. Daňové příjmy na obyvatele mají srovnatelné se sousedy,
do investic a oprav ale v letech 2023–2025 dávaly na obyvatele dvakrát až pětkrát méně a mají nejvíc peněz na účtech.
Na rok 2026 obec naplánovala investice a opravy za {num(io26_plan, 1)} mil. Kč, do 30. 9. z toho zaplatila {num(io26, 1)} mil. Kč (<a href="hd-rozpocet-2026.html">Rozpočet 2026</a>).
Podrobnosti a výhrady ke srovnatelnosti jsou v <a href="srovnani-souhrn.html">souhrnu srovnání</a>.</p>
{c_io}
{c_tax}
{c_io_hd}
{c_cash}
{c_pop}
<h2>Obec v číslech</h2>
{cards("Obec v číslech")}
<h2>Srovnání se sousedy</h2>
{cards("Srovnání se sousedy")}
<h2>Srovnání s podobnými obcemi</h2>
{cards("Srovnání s podobnými obcemi")}
'''
    return page('index', SITE, body, lede='Veřejná data o obci na jednom místě: lidé, peníze, majetek, výstavba a srovnání se sousedními obcemi.',
                description='Občanský přehled veřejných dat o obci Horní Domaslavice: obyvatelé, rozpočet a výdaje, majetek, výstavba, volby a srovnání se sousedními obcemi.',
                jsonld={'@context': 'https://schema.org', '@type': 'WebSite', 'name': SITE, 'url': SITE_URL, 'inLanguage': 'cs',
                        'description': 'Neoficiální občanský přehled veřejných dat o obci Horní Domaslavice.', 'author': AUTHOR, 'license': LICENSE_URL})


DATA_DESC = {
    'finance_HD_2010-2025.csv': 'Horní Domaslavice: příjmy, výdaje, investice, opravy, dotace, peníze a úvěry po letech 2010–2025 (Monitor MF).',
    'finance_PAZ_2010-2025.csv': 'Pazderna: totéž.',
    'finance_DD_2010-2025.csv': 'Dolní Domaslavice: totéž.',
    'finance_LUC_2010-2025.csv': 'Lučina: totéž.',
    'souhrn_po_obdobich_sousede.csv': 'Souhrny ukazatelů za volební období, celkem a na obyvatele a rok (HD a sousední obce).',
    'ukazatele_sousede_2010-2025.csv': 'Ukazatele po letech v dlouhém formátu (HD a sousední obce).',
    'investice_opravy_podle_paragrafu_sousede.csv': 'Investice a opravy podle účelu výdaje (paragrafu rozpočtové skladby).',
    'ukazatele_rozvaha_vzz_sousede.csv': 'Rozvaha a výkaz zisku a ztráty: majetek, peníze, úvěry, odpisy (HD a sousední obce, 2010–2025).',
    'souhrn_obyvatel_rocne_2000-2025_sousede_okres_CR.csv': 'Počet obyvatel a věkové skupiny 2000–2025, pohyb obyvatel 2002–2025 (HD a sousední obce, okres, ČR; ČSÚ).',
    'RUIAN_souhrn_sousede_stav_20260930.csv': 'Budovy, byty a napojení na vodovod, kanalizaci a plyn podle RÚIAN (stav 30. 9. 2026).',
    'CUZK_UHDP_druhy_pozemku_sousede_2004_2014_2026.csv': 'Výměry druhů pozemků po katastrálních územích, 2004, 2014 a 2026 (ČÚZK).',
    'roztrisenost_sousede.csv': 'Ukazatele roztříštěnosti zástavby (skupiny domů, vzdálenosti, délka propojení).',
    'usneseni_zo_2022-2026.csv': 'Usnesení zastupitelstva 2022–2026 (a dojezd 2018–2022): číslo, datum, znění bez jmen osob, typ, výsledek, hlasy, téma, částka.',
    'rozpocet_2026_srovnani_k_30_9.csv': 'Rozpočet 2026: plnění příjmů a čerpání výdajů k 30. 9. proti stejnému období 2023–2025.',
    'rozpocet_2026_vydaje_podle_ucelu.csv': 'Rozpočet 2026: výdaje podle účelu – schváleno, upraveno, skutečnost k 30. 9.',
    'rozpocet_2026_investice_opravy.csv': 'Rozpočet 2026: plánované a zaplacené investice a opravy podle akcí.',
    'rozpocet_2026_odhad_prijmu.csv': 'Rozpočtované a skutečné příjmy 2023–2026.',
    'rozpocet_2026_rozpoctova_opatreni.csv': 'Rozpočtová opatření 2026.',
    'rozpocet_2026_stav_uctu.csv': 'Peníze na účtech obce po čtvrtletích 2023–2026.',
    'rozpocet_2026_strednedoby_vyhled.csv': 'Střednědobý výhled rozpočtu 2025–2028.',
    'finance_VOJ_2010-2025.csv': 'Vojkovice (okres Frýdek-Místek, sousední obec): hospodaření po letech 2010–2025, stejné sloupce jako u HD.',
    'finance_PL_2010-2025.csv': 'Písková Lhota (okres Mladá Boleslav): hospodaření po letech 2010–2025, stejné sloupce jako u HD.',
    'finance_REB_2010-2025.csv': 'Rebešovice (okres Brno-venkov): hospodaření po letech 2010–2025, stejné sloupce jako u HD.',
    'finance_ZAV_2010-2025.csv': 'Závišice (okres Nový Jičín): hospodaření po letech 2010–2025, stejné sloupce jako u HD.',
    'podobne_obce_vyber.csv': 'Výběr podobných obcí: 232 obcí ČR s parametry obyvatel, rozlohy a zástavby, skóre a pořadím výběru a indexem odlišnosti zástavby od HD.',
    'podobne_obce_souhrn_po_obdobich.csv': 'Souhrny ukazatelů po volebních obdobích pro HD, Pískovou Lhotu, Rebešovice a Závišice.',
    'podobne_obce_investice_podle_ucelu_2016-2025.csv': 'Investice a opravy 2016–2025 podle účelu: HD, Písková Lhota, Rebešovice, Závišice.',
    'podobne_obce_investice_podle_paragrafu.csv': 'Investice a opravy HD, Pískové Lhoty, Rebešovic a Závišic podle paragrafu a roku.',
    'podobne_obce_CUZK_UHDP_2004_2014_2026.csv': 'Výměry druhů pozemků HD a podobných obcí, 2004, 2014 a 2026 (ČÚZK).',
    'podobne_obce_roztrisenost.csv': 'Ukazatele roztříštěnosti zástavby HD a podobných obcí.',
    'podobne_obce_obyvatel_rocne_2000-2025.csv': 'Počet obyvatel a věkové skupiny 2000–2025, pohyb obyvatel 2002–2025 (HD, podobné obce, ČR; ČSÚ).',
    'podobne_obce_RUIAN_souhrn_stav_20260930.csv': 'Budovy, byty a napojení na sítě podle RÚIAN, HD a podobné obce (stav 30. 9. 2026).',
    'podobne_obce_ukazatele_rozvaha_vzz.csv': 'Rozvaha a výkaz zisku a ztráty HD a podobných obcí, 2010–2025.',
    'podobne_obce_vydaje_kategorie_2010-2025.csv': 'Výdaje HD, Pískové Lhoty, Rebešovic a Závišic podle účelu a druhu, 2010–2025.',
    'podobne_obce_obyvatele_2000-2025.csv': 'Počet obyvatel HD, Pískové Lhoty, Rebešovic a Závišic 2000–2025.',
}


def build_data_page():
    rows = []
    for f in sorted(os.listdir(os.path.join(ROOT, 'data'))):
        if f.endswith('.csv'):
            size = os.path.getsize(os.path.join(ROOT, 'data', f)) / 1024
            rows.append(f'<tr><td><a href="data/{esc(f)}">{esc(f)}</a></td><td>{esc(DATA_DESC.get(f, ""))}</td><td style="text-align:right">{num(size, 0)} kB</td></tr>')
    body = f'''<p>Data, ze kterých stránky vycházejí, jsou ke stažení ve formátu CSV (UTF-8, oddělovač čárka, desetinná tečka).
Co znamená který sloupec, popisuje <a href="slovnik-dat.html">slovník dat</a>. Jsou to výřezy a výpočty z veřejných zdrojů. Při dalším použití uveďte původní zdroj: Ministerstvo financí (Monitor státní pokladny),
Český statistický úřad, ČÚZK (RÚIAN, katastr nemovitostí).</p>
<table><thead><tr><th>Soubor</th><th>Obsah</th><th>Velikost</th></tr></thead><tbody>{"".join(rows)}</tbody></table>
<p>Původní zdroje:</p>
<ul>
<li><a href="https://monitor.statnipokladna.gov.cz/">Monitor státní pokladny</a> – rozpočty a účetnictví obcí</li>
<li><a href="https://csu.gov.cz/">Český statistický úřad</a> – obyvatelstvo, sčítání 2021, bytová výstavba</li>
<li><a href="https://vdp.cuzk.gov.cz/">RÚIAN</a> a <a href="https://services.cuzk.cz/sestavy/UHDP/">ČÚZK – úhrnné hodnoty druhů pozemků</a></li>
<li><a href="https://www.volby.cz/">volby.cz</a> – výsledky voleb</li>
<li><a href="https://smlouvy.gov.cz/">Registr smluv</a>, profily zadavatelů, ARES a další rejstříky</li>
</ul>'''
    dataset = {'@context': 'https://schema.org', '@type': 'Dataset', 'name': f'{SITE} – data ke stažení',
               'description': 'Výřezy a výpočty z veřejných zdrojů (Ministerstvo financí, ČSÚ, ČÚZK, volby.cz a další) o obci Horní Domaslavice '
                              'a srovnávaných obcích: rozpočty a účetnictví, obyvatelstvo, výstavba, plochy, volby, usnesení zastupitelstva.',
               'url': page_url('data'), 'inLanguage': 'cs', 'license': LICENSE_URL, 'isAccessibleForFree': True,
               'creator': AUTHOR, 'spatialCoverage': {'@type': 'Place', 'name': 'Horní Domaslavice, okres Frýdek-Místek'},
               'distribution': [{'@type': 'DataDownload', 'encodingFormat': 'text/csv', 'contentUrl': f'{SITE_URL}data/{f}', 'name': f}
                                for f in sorted(os.listdir(os.path.join(ROOT, 'data'))) if f.endswith('.csv')]}
    return page('data', 'Data ke stažení', body, lede='Všechna čísla na webu lze ověřit ve zdrojových datech.',
                description='Data o obci Horní Domaslavice ke stažení v CSV: finance, obyvatelstvo, výstavba, volby, usnesení a srovnání se sousedními obcemi.',
                jsonld=dataset)


def build_about():
    if REPORT_FORM['action']:
        REPORT_PRIVACY = '''<p>Hlášení odeslaná formulářem „Nahlásit chybu“ se ukládají do Google Formuláře autora webu. Obsahují stránku, citovaný text a váš popis.
E-mail je nepovinný a použije se jen k odpovědi na hlášení.</p>'''
    else:
        REPORT_PRIVACY = f'''<p>Tlačítko „Nahlásit chybu“ otevře předvyplněné hlášení (issue) v <a href="{REPO_URL}/issues">repozitáři webu na GitHubu</a>.
Hlášení je veřejné a je u něj vidět uživatelské jméno na GitHubu; nepište do něj osobní údaje. Web žádná hlášení sám neukládá.</p>'''
    body = f'''<h2>Co je tento web</h2>
<p>Soukromá, nadstranická občanská iniciativa. Cílem je, aby měl každý občan Horních Domaslavic po ruce veřejná data o své obci
v srozumitelné podobě a mohl je porovnat se sousedními obcemi. Web není stránkou obce a nevyjadřuje stanovisko žádné politické strany, hnutí ani kandidátky.</p>
<h2 id="nestrannost">Závazek nestrannosti</h2>
<p>Tento web je a i do budoucna zůstane čistě informační. Platí pro něj:</p>
<ul>
<li>Zveřejňuje jen fakta a data z veřejně dostupných zdrojů, vždy s odkazem na zdroj.</li>
<li>Neobsahuje politická prohlášení, hodnocení ani doporučení, koho volit. Nepodporuje ani nekritizuje žádnou stranu, hnutí, kandidátku ani osobu.</li>
<li>Texty popisují, co data ukazují a jaké k nim platí výhrady. Závěry nechávají na čtenáři.</li>
<li>Autor web nevyužívá ve volebních kampaních a web nenese reklamu. Data může díky licenci CC BY použít kdokoli, i v kampani. Za takové použití web neodpovídá.</li>
<li>Všechny opravy se veřejně zapisují na stránku <a href="opravy.html">Opravy</a>.</li>
</ul>
<p>Pokud narazíte na text, který tomuto závazku neodpovídá, nahlaste ho prosím stejně jako chybu.</p>
<h2>Zásady</h2>
<ul>
<li>Jen veřejně dostupné zdroje. U každé stránky je uvedeno, odkud data jsou.</li>
<li>Hodnotí se čísla, ne lidé. Stránky nejmenují zastupitele ani jiné osoby.</li>
<li>Výhrady k datům a ke srovnatelnosti obcí jsou uvedeny u každé stránky v části „Pozor“.</li>
<li>Chyby opravujeme. Na konci každé stránky je tlačítko „Nahlásit chybu“; chybu lze nahlásit i přímo v označeném textu.
Provedené opravy jsou zveřejněné na stránce <a href="opravy.html">Opravy</a>.</li>
</ul>
<h2>Metodika v kostce</h2>
<ul>
<li><b>Finance</b> vycházejí z výkazu FIN 2-12 M a účetních výkazů obcí v Monitoru státní pokladny, roky 2010–2025.
Výdaje bez převodů mezi vlastními účty (§ 6330), příjmy bez převodů z vlastních fondů (413x). Daň z příjmů, kterou obec platí sama sobě (položka 1122), je odečtena z příjmů i výdajů.
„Investice a opravy“ = investiční výdaje (třída 6) + opravy a udržování (položka 5171).</li>
<li><b>Na obyvatele</b>: toky (příjmy, výdaje) se dělí počtem obyvatel k 1. 7., stavy (peníze na účtech, úvěry) počtem k 31. 12. daného roku (ČSÚ).</li>
<li><b>Částky</b> nejsou očištěné o inflaci. Roční data končí rokem 2025; za rok 2026 je jen průběžný stav k 30. 9. (stránka Rozpočet 2026).</li>
<li><b>Srovnávané obce</b> nejsou zcela srovnatelné (např. Dolní Domaslavice a Lučina zřizují základní školu,
Lučina má výdaje spojené s nádrží Žermanice). Výhrady jsou uvedeny u jednotlivých stránek.</li>
</ul>
<h2>Hlášení chyb a osobní údaje</h2>
{REPORT_PRIVACY}
<p>Web nepoužívá cookies. Hostuje ho služba Cloudflare Pages; Cloudflare jako provozovatel hostingu při doručování stránek zpracovává technické údaje o přístupu, včetně IP adresy.
Návštěvnost měříme službou Cloudflare Web Analytics. Ta nepoužívá cookies ani jiné ukládání do prohlížeče a návštěvníky nesleduje mezi dny ani mezi weby;
vidíme jen souhrnné údaje: kolikrát byla která stránka zobrazena, odkud návštěvníci přišli, typ zařízení, země a rychlost načítání.
Stránka Mapa načítá mapové podklady z OpenStreetMap a ČÚZK a knihovnu Leaflet z unpkg.com; jejich provozovatelé při tom také vidí IP adresu návštěvníka.</p>
<h2>Licence</h2>
<p>Texty, grafy a zpracovaná data tohoto webu můžete volně používat, upravovat a šířit, i komerčně, pokud uvedete zdroj („Horní Domaslavice v datech, hd-v-datech.cz“).
Platí licence <a href="https://creativecommons.org/licenses/by/4.0/deed.cs">Creative Commons Uveďte původ 4.0 Mezinárodní (CC BY 4.0)</a>.
Původní data se řídí podmínkami svých zdrojů (ČSÚ, Ministerstvo financí, ČÚZK a další), mapové podklady podmínkami OpenStreetMap a ČÚZK.</p>
<h2>Autor</h2>
<p>Tomáš Dinkov</p>
<p>Poslední aktualizace: {UPDATED}.</p>'''
    return page('o-webu', 'O webu a metodika', body, lede='Kdo web dělá, z čeho vychází a jak se počítají čísla.',
                description='Kdo web Horní Domaslavice v datech dělá, z jakých veřejných zdrojů vychází a jak se počítají čísla.')


def build_md_pages():
    built = []
    for f in sorted(os.listdir(os.path.join(ROOT, 'obsah'))):
        if not f.endswith('.md'):
            continue
        slug = f[:-3]
        meta, text = front_matter(open(os.path.join(ROOT, 'obsah', f), encoding='utf-8').read())
        text = re.sub(r'^#\s+.*\n', '', text.lstrip(), count=1)  # H1 comes from the template
        body = md_to_html(text)
        body = re.sub(r'<!--\s*chart:([\w-]+)\s*-->', lambda m: charts.CHARTS[m.group(1)](), body)
        if 'id="usneseni-app"' in body:
            body += '<script src="static/usneseni.js" defer></script>'
        if meta.get('updated'):
            d = meta['updated']
            LASTMOD[slug] = d
            m = re.match(r'(\d{4})-(\d{2})-(\d{2})$', d)
            if m:
                d = f'{int(m.group(3))}. {int(m.group(2))}. {m.group(1)}'
            body = f'<p class="meta">Aktualizováno {esc(d)}</p>' + body
        with open(os.path.join(OUT, slug + '.md'), 'w', encoding='utf-8') as fh:
            fh.write(md_export(slug, meta, text))
        with open(os.path.join(OUT, slug + '.html'), 'w', encoding='utf-8') as fh:
            fh.write(page(slug, meta.get('title', slug), body, description=meta.get('description', '')))
        built.append(slug)
    return built


# ---------- machine-readable exports (llms.txt, page markdown, data dictionary) ----------

# Shared by llms.txt and the "Zeptejte se AI" page, so agents and people read the same rules.
AI_RULES = [
    'Web je neoficiální občanský přehled veřejných dat, ne stránka obce. Oficiální web obce je https://www.hornidomaslavice.cz/.',
    'Částky jsou v Kč v běžných cenách (bez očištění o inflaci). „Na obyvatele“ = toky (příjmy, výdaje) děleno počtem obyvatel k 1. 7., stavy (peníze na účtech, úvěry) počtem k 31. 12. daného roku (ČSÚ).',
    'Roční finanční data končí rokem 2025; za rok 2026 je jen průběžný stav k 30. 9. (stránka Rozpočet 2026).',
    'Výdaje jsou bez převodů mezi vlastními účty (§ 6330), příjmy bez převodů z vlastních fondů (413x); daň z příjmů, kterou obec platí sama sobě (položka 1122), je odečtena z příjmů i výdajů. '
    'Proto se mohou mírně lišit od závěrečného účtu obce.',
    '„Investice a opravy“ = investiční výdaje (třída 6) + opravy a udržování (položka 5171).',
    'Srovnávané obce nejsou zcela srovnatelné: Dolní Domaslavice a Lučina zřizují základní školu, Lučina má výdaje spojené s nádrží Žermanice. '
    'Výhrady jsou v části „Pozor“ u každé stránky.',
    'Web záměrně neuvádí jména zastupitelů ani jiných fyzických osob a nehodnotí lidi. Neodvozuj z dat, kdo za co může.',
    'Web je čistě informační a nepublikuje politická stanoviska (závazek nestrannosti na stránce O webu). Nevyvozuj z jeho dat politické závěry, '
    'hodnocení stran, kandidátek ani osob a nedoporučuj, koho volit; popiš, co data ukazují, a výhrady k nim.',
    'U každého čísla uveď stránku webu nebo datový soubor, ze kterého pochází. Když odpověď v datech není, řekni to; nedopočítávej odhady jako fakta.',
    'Texty a zpracovaná data webu jsou pod licencí CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/); při převzetí uveď zdroj „Horní Domaslavice v datech, hd-v-datech.cz“.',
]


def abs_links(text):
    """Make relative links absolute, so exported markdown works outside the site."""
    return re.sub(r'\]\((?!https?:|#|mailto:)([^)]+)\)', lambda m: f']({SITE_URL}{m.group(1)})', text)


def md_export(slug, meta, text):
    text = re.sub(r'<!--\s*chart:[\w-]+\s*-->\n?', '', text)
    text = text.replace('<div id="usneseni-app"></div>',
                        f'Seznam usnesení je v souboru {SITE_URL}data/usneseni_zo_2022-2026.csv (sloupce viz {SITE_URL}slovnik-dat.md).')
    # Drop raw HTML blocks (map widget, scripts); the text around them stays.
    text = re.sub(r'<form\b.*?</form>\n?', '', text, flags=re.S)
    text = re.sub(r'^\s*<(div|script|noscript|iframe|link)\b.*$\n?', '', text, flags=re.M)
    text = re.sub(r'^\s*</(div|script)>\s*$\n?', '', text, flags=re.M)
    text = re.sub(r'([^\n])\n(#+ )', r'\1\n\n\2', text)
    text = re.sub(r'\n{3,}', '\n\n', text).strip()
    head = [f'# {meta.get("title", slug)}', '',
            f'Zdroj: {SITE_URL}{slug}.html' + (f' (aktualizováno {meta["updated"]})' if meta.get('updated') else ''), '']
    if meta.get('description'):
        head += [f'> {meta["description"]}', '']
    return '\n'.join(head) + '\n' + abs_links(text) + '\n'


def slovnik_md():
    lines = ['# Slovník dat', '',
             f'Popis datových souborů webu {SITE} ({SITE_URL}). Všechny soubory jsou CSV v UTF-8, oddělovač čárka, '
             'desetinná tečka, data ve tvaru RRRR-MM-DD. Částky jsou v Kč, běžné ceny.', '']
    warnings = []
    for f in sorted(os.listdir(os.path.join(ROOT, 'data'))):
        if not f.endswith('.csv'):
            continue
        d = slovnik.DATASETS.get(f)
        if not d:
            warnings.append(f'{f}: chybí ve slovníku')
            continue
        with open(os.path.join(ROOT, 'data', f), encoding='utf-8') as fh:
            rd = csv.reader(fh)
            header = next(rd)
            n = sum(1 for _ in rd)
        base = slovnik.DATASETS.get(d.get('stejne_jako'), d)
        lines += [f'## {f}', '', d['popis'], '',
                  f'- Odkaz: [data/{f}]({SITE_URL}data/{f})',
                  f'- Řádků: {n}; jeden řádek = {base["radek"]}',
                  f'- Zdroj: {base["zdroj"]}']
        lines += [f'- Pozor: {p}' for p in base.get('pozor', [])]
        lines.append('')
        if 'stejne_jako' in d:
            lines += [f'Sloupce jsou stejné jako v `{d["stejne_jako"]}`.', '']
            for c in header:
                if slovnik.describe(f, c) is None:
                    warnings.append(f'{f}: sloupec {c} bez popisu')
            continue
        lines += ['| Sloupec | Význam |', '|---|---|']
        per_capita = []
        for c in header:
            desc = slovnik.describe(f, c)
            if desc is None:
                warnings.append(f'{f}: sloupec {c} bez popisu')
                desc = ''
            if c.endswith('_na_obyv') and c not in slovnik.columns(f):
                per_capita.append(c)
                continue
            lines.append(f'| `{c}` | {desc.replace("|", "/")} |')
        if per_capita:
            lines.append(f'| `*_na_obyv` ({len(per_capita)} sloupců) | Stejnojmenný sloupec bez přípony na obyvatele: toky děleno `obyv_1_7`, stavy k 31. 12. (účty, peníze, úvěry, závazky) děleno `obyv_31_12`. Kč. |')
        lines.append('')
    return '\n'.join(lines), warnings


def build_slovnik():
    md, warnings = slovnik_md()
    with open(os.path.join(OUT, 'slovnik-dat.md'), 'w', encoding='utf-8') as fh:
        fh.write(md + '\n')
    body = md_to_html(re.sub(r'^# .*\n', '', md, count=1))
    body = body.replace(f'href="{SITE_URL}', 'href="')
    html_ = page('slovnik-dat', 'Slovník dat', body, lede='Co znamená který sloupec v datech ke stažení.',
                 description='Slovník dat webu Horní Domaslavice v datech: co znamená který sloupec v souborech ke stažení.')
    return html_, warnings


def page_list(slugs):
    titles = {s: t for _, items in NAV for s, t in items}
    out = []
    for group, items in NAV:
        out.append((group, [(s, t) for s, t in items if s in slugs]))
    return out


def build_llms(slugs):
    desc = {}
    for s in slugs:
        meta, _ = front_matter(open(os.path.join(ROOT, 'obsah', s + '.md'), encoding='utf-8').read())
        desc[s] = meta.get('description', '')
    lines = [f'# {SITE}', '',
             '> Neoficiální občanský přehled veřejných dat o obci Horní Domaslavice (okres Frýdek-Místek) a srovnání se sousedními '
             'obcemi Pazderna, Dolní Domaslavice, Lučina a Vojkovice a s podobnými obcemi jinde v ČR: obyvatelstvo, rozpočet a hospodaření 2010–2026, investice, dotace, '
             'majetek, zakázky, usnesení zastupitelstva, výstavba, pozemky a občanská vybavenost. Zdroje: Ministerstvo financí '
             '(Monitor státní pokladny), ČSÚ, ČÚZK, volby.cz, registr smluv, dokumenty obce.', '',
             f'Autor: Tomáš Dinkov. Aktualizováno {UPDATED}. Chyby lze hlásit na {REPO_URL}/issues.', '',
             '## Jak data číst a citovat', '']
    lines += [f'- {r}' for r in AI_RULES]
    lines.append('')
    for group, items in page_list(slugs):
        if not items:
            continue
        lines += [f'## {group}', '']
        lines += [f'- [{t}]({SITE_URL}{s}.md): {desc.get(s, "")}' for s, t in items]
        lines.append('')
    lines += ['## Data', '',
              f'- [Slovník dat]({SITE_URL}slovnik-dat.md): popis všech CSV souborů a jejich sloupců',
              f'- [Data ke stažení]({SITE_URL}data.html): seznam souborů']
    for f in sorted(os.listdir(os.path.join(ROOT, 'data'))):
        if f.endswith('.csv'):
            lines.append(f'- [{f}]({SITE_URL}data/{f}): {slovnik.DATASETS.get(f, {}).get("popis", "")}')
    lines += ['', '## Optional', '',
              f'- [Celý web v jednom souboru]({SITE_URL}llms-full.txt): texty všech stránek a slovník dat',
              f'- [O webu a metodika]({SITE_URL}o-webu.html)',
              f'- [Opravy]({SITE_URL}opravy.md): seznam opravených chyb', '']
    llms = '\n'.join(lines)
    full = [llms, '']
    for _, items in page_list(slugs):
        for s, _ in items:
            full += ['\n---\n', open(os.path.join(OUT, s + '.md'), encoding='utf-8').read()]
    full += ['\n---\n', open(os.path.join(OUT, 'slovnik-dat.md'), encoding='utf-8').read()]
    with open(os.path.join(OUT, 'llms.txt'), 'w', encoding='utf-8') as fh:
        fh.write(llms)
    with open(os.path.join(OUT, 'llms-full.txt'), 'w', encoding='utf-8') as fh:
        fh.write('\n'.join(full))


def build_ai_page():
    size = os.path.getsize(os.path.join(OUT, 'llms-full.txt')) / 1024
    prompt = (f'Přečti si rozcestník webu o obci Horní Domaslavice {SITE_URL}llms.txt, podle mé otázky otevři odkazované stránky '
              'a odpovídej jen podle nich. U každého čísla uveď stránku webu, ze které pochází. Když odpověď v datech není, řekni to.\n\n'
              'Moje otázka: ')
    questions = [
        'Kolik obec investovala do silnic a chodníků v posledních čtyřech letech a jak to vypadá u sousedních obcí?',
        'Proč má obec na účtech tolik peněz? Jak se stav vyvíjel od roku 2014?',
        'Která usnesení zastupitelstva se týkala mateřské školy a jak dopadla?',
        'Jak se změnil počet obyvatel od roku 2000 a odkud přibývají – narozením, nebo stěhováním?',
        'Kolik domů v obci nemá přípojku vodovodu a kanalizace?',
        'Jaké dotace obec získala a ve kterých letech?',
        'Jak si stojí rozpočet 2026 k 30. září proti předchozím rokům?',
    ]
    qs = ''.join(f'<li>{esc(q)}</li>' for q in questions)
    rules = ''.join(f'<li>{esc(r)}</li>' for r in AI_RULES)
    body = f'''<p>Na data z tohoto webu se můžete zeptat svého AI asistenta (ChatGPT, Claude, Gemini, Copilot a podobně) běžnou češtinou.
Web pro ně má rozcestník, texty všech stránek v jednoduchém formátu a popis dat, takže asistent odpovídá z čísel na webu a může citovat konkrétní stránku.</p>
<h2>Jak na to</h2>
<ol class="ai-steps">
<li><b>Zkopírujte úvodní zprávu</b> a vložte ji do svého asistenta. Za „Moje otázka:“ dopište, co vás zajímá.
<div class="copy-box"><pre id="ai-prompt">{esc(prompt)}</pre><button type="button" class="btn-ghost" data-copy="#ai-prompt">Zkopírovat zprávu</button></div></li>
<li><b>Pokud asistent odkaz neotevře</b> (některé verze neumí číst web), stáhněte si
<a href="llms-full.txt" download>soubor s celým webem</a> ({num(size, 0)} kB, prostý text) a vložte ho do konverzace jako přílohu.
V úvodní zprávě pak místo odkazu napište „Přečti si přiložený soubor“.</li>
<li><b>Ověřte si důležitá čísla</b> na stránce, kterou asistent uvede. AI se může splést nebo si něco domyslet; rozhodující je text na webu a původní zdroj.</li>
</ol>
<h2>Na co se zeptat</h2>
<ul>{qs}</ul>
<h2>Co asistent dostane jako pravidla</h2>
<p>Na začátku souboru jsou pokyny, jak data číst. Platí i pro lidi:</p>
<ul>{rules}</ul>
<h2>Soukromí</h2>
<p>Otázky píšete do služby svého asistenta, ne na tento web. Web nic z konverzace nevidí a neukládá. Co poskytovatel asistenta s konverzací dělá, se řídí jeho podmínkami.</p>
<h2>Pro pokročilé</h2>
<ul>
<li><a href="llms.txt">llms.txt</a> – rozcestník pro AI agenty podle standardu llmstxt.org: pravidla, odkazy na stránky v Markdownu a na data.</li>
<li>Každá stránka je k dispozici i jako Markdown: stačí v adrese nahradit <code>.html</code> za <code>.md</code> (například <a href="hd-vydaje.md">hd-vydaje.md</a>).</li>
<li><a href="slovnik-dat.html">Slovník dat</a> a <a href="data.html">CSV soubory</a> pro vlastní výpočty, třeba v Excelu nebo v Pythonu.</li>
</ul>'''
    return page('zeptejte-se-ai', 'Zeptejte se AI', body,
                lede='Ptejte se na data o obci vlastními slovy a nechte si odpověď vysvětlit.',
                description='Jak se na data o obci Horní Domaslavice zeptat AI asistenta vlastními slovy a nechat si odpověď vysvětlit.')


def check_links(slugs):
    known = set(slugs) | {'index', 'data', 'o-webu', 'opravy', 'zeptejte-se-ai', 'slovnik-dat'}
    bad = []
    for f in os.listdir(OUT):
        if not f.endswith('.html'):
            continue
        t = open(os.path.join(OUT, f), encoding='utf-8').read()
        for href in re.findall(r'href="([^"#:]+?)\.html', t):
            if href not in known:
                bad.append((f, href))
        for src in re.findall(r'(?:src|href)="((?:img|data)/[^"]+)"', t):
            if not os.path.exists(os.path.join(OUT, src)):
                bad.append((f, src))
    return bad


def build_404():
    body = '''<p>Stránka na této adrese neexistuje. Mohla být přejmenována, nebo je v adrese překlep.</p>
<p>Pokračujte na <a href="index.html">úvodní stránku</a> nebo do <a href="data.html">přehledu dat ke stažení</a>.</p>'''
    # served for any missing path, so make relative links root-relative
    return re.sub(r'(href|src)="(?![a-z]+:|/|#)', r'\1="/', page('404', 'Stránka nenalezena', body))


def build_seo_files(slugs):
    m = re.match(r'(\d+)\. (\d+)\. (\d{4})$', UPDATED)
    site_date = f'{m.group(3)}-{int(m.group(2)):02d}-{int(m.group(1)):02d}'
    urls = []
    for slug in ['index', 'data', 'o-webu', 'slovnik-dat', 'zeptejte-se-ai'] + list(slugs):
        urls.append(f'<url><loc>{page_url(slug)}</loc><lastmod>{LASTMOD.get(slug, site_date)}</lastmod></url>')
    with open(os.path.join(OUT, 'sitemap.xml'), 'w', encoding='utf-8') as fh:
        fh.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
                 + '\n'.join(urls) + '\n</urlset>\n')
    # Cloudflare prepends its bot preferences (content signals) to this file
    with open(os.path.join(OUT, 'robots.txt'), 'w', encoding='utf-8') as fh:
        fh.write(f'User-agent: *\nAllow: /\n\nSitemap: {SITE_URL}sitemap.xml\n')


def build_headers():
    theme = base64.b64encode(hashlib.sha256(THEME_JS.encode()).digest()).decode()
    csp = '; '.join([
        "default-src 'self'",
        f"script-src 'self' 'sha256-{theme}' https://unpkg.com https://static.cloudflareinsights.com",
        "style-src 'self' 'unsafe-inline' https://unpkg.com",
        "img-src 'self' data: https://unpkg.com https://tile.openstreetmap.org https://ags.cuzk.gov.cz",
        "connect-src 'self' https://docs.google.com https://cloudflareinsights.com",
        "object-src 'none'", "base-uri 'self'", "form-action 'self'", "frame-ancestors 'none'",
    ])
    return f"""/*
  Content-Security-Policy: {csp}
  Referrer-Policy: strict-origin-when-cross-origin
  Strict-Transport-Security: max-age=31536000
  X-Content-Type-Options: nosniff
  Permissions-Policy: camera=(), microphone=(), geolocation=(), interest-cohort=()
"""


def main():
    if os.path.exists(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT)
    for d in ('static', 'img', 'data'):
        shutil.copytree(os.path.join(ROOT, d), os.path.join(OUT, d))
    with open(os.path.join(OUT, '_headers'), 'w') as fh:  # HTTP headers for Cloudflare Pages
        fh.write(build_headers())
    slugs = build_md_pages()
    slovnik_html, warnings = build_slovnik()
    build_llms(slugs)
    for name, html_ in (('index', build_index()), ('data', build_data_page()), ('o-webu', build_about()),
                        ('slovnik-dat', slovnik_html), ('zeptejte-se-ai', build_ai_page())):
        with open(os.path.join(OUT, name + '.html'), 'w', encoding='utf-8') as fh:
            fh.write(html_)
    bad = check_links(slugs)
    build_seo_files(slugs)
    with open(os.path.join(OUT, '404.html'), 'w', encoding='utf-8') as fh:  # after check_links: root-relative links
        fh.write(build_404())
    print(f'{len(slugs)} stránek z obsah/, výstup v docs/')
    for f, h in bad:
        print(f'  ROZBITÝ ODKAZ: {f} -> {h}')
    for w in warnings:
        print(f'  SLOVNÍK: {w}')
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main())
