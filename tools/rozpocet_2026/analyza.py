import csv, os, sys, json
from collections import defaultdict

D = sys.argv[1]   # data_rozpocet_2026
A = sys.argv[2]   # data_monitor_mf
OUT = sys.argv[3] # output dir for csv

def num(s):
    s = s.strip().strip('"').strip()
    if not s:
        return 0.0
    neg = s.endswith('-')
    s = s.rstrip('-').strip()
    v = float(s)
    return -v if neg else v

def load(path, fmt):
    """returns dict (typ, par, pol) -> [SR, UR, SK]"""
    agg = defaultdict(lambda: [0.0, 0.0, 0.0])
    with open(path, encoding='utf-8', errors='replace') as f:
        lines = f.read().splitlines()
    for l in lines:
        if not l or l.startswith('"') or l.startswith('#') or l.startswith('ZC_'):
            continue
        p = l.split(';')
        if p[4] != '00536008':
            continue
        if fmt == 'new':
            typ, par, pol = p[7], p[8], p[9]
            vals = p[15], p[16], p[17]
        else:
            typ, par, pol = p[7], p[8], p[9]
            vals = p[10], p[11], p[12]
        a = agg[(typ, par, pol)]
        for i in range(3):
            a[i] += num(vals[i])
    return agg

data = {
    '2026_09': load(os.path.join(D, 'HD_FINM01_UJ_2026009.csv'), 'new'),
    '2025_09': load(os.path.join(D, 'HD_FINM201_2025009.csv'), 'old'),
    '2024_09': load(os.path.join(D, 'HD_FINM201_2024009.csv'), 'old'),
    '2023_09': load(os.path.join(D, 'HD_FINM201_2023009.csv'), 'old'),
    '2025_12': load(os.path.join(A, 'FINM201_HD_202512.csv'), 'old'),
    '2024_12': load(os.path.join(A, 'FINM201_HD_202412.csv'), 'old'),
    '2023_12': load(os.path.join(A, 'FINM201_HD_202312.csv'), 'old'),
}

def is_vydaj(par, pol):
    return pol[:1] in '56' and par != '0000' and pol not in ('6330', '6399') and par not in ('6330', '6399')

def is_prijem(par, pol):
    # bez 4134 (převody z vlastních fondů) a bez 1122 (daň z příjmů placená obcí sama sobě;
    # její protějšek § 6399 je mimo výdaje, proto se nepočítá ani do příjmů)
    return pol[:1] in '1234' and pol not in ('4134', '1122') and par not in ('6330',)

def is_rezerva(par, pol):
    return (par == '3639' and pol == '5169') or (par == '6409' and pol == '5901')

GROUPS = [
    ('Rezervy (§ 3639/5169, § 6409/5901)', lambda par, pol: is_rezerva(par, pol)),
    ('Správa obce (úřad, zastupitelstvo, volby)', lambda par, pol: par[:2] == '61' or par in ('6310', '6320')),
    ('Silnice, chodníky, doprava', lambda par, pol: par[:2] == '22'),
    ('Mateřská škola a školství', lambda par, pol: par[:2] == '31'),
    ('Sport a volný čas (vč. hřišť)', lambda par, pol: par[:2] == '34'),
    ('Kultura, památky, akce', lambda par, pol: par[:2] == '33'),
    ('Budovy (Obecní dům, byty)', lambda par, pol: par in ('3612', '3613')),
    ('Odpady', lambda par, pol: par[:3] == '372'),
    ('Zeleň a životní prostředí', lambda par, pol: par[:2] == '37'),
    ('Hasiči a krizové řízení', lambda par, pol: par[:2] in ('55', '52')),
    ('Veřejné osvětlení', lambda par, pol: par == '3631'),
    ('Hřbitov', lambda par, pol: par == '3632'),
    ('Územní plán a komunální služby', lambda par, pol: par in ('3635', '3636', '3639')),
    ('Sociální služby a zdraví', lambda par, pol: par[:1] == '4' or par[:2] == '35'),
    ('Ostatní', lambda par, pol: True),
]

def group_of(par, pol):
    for name, fn in GROUPS:
        if fn(par, pol):
            return name

def tot(agg, pred):
    r = [0.0, 0.0, 0.0]
    for (typ, par, pol), v in agg.items():
        if pred(par, pol):
            for i in range(3):
                r[i] += v[i]
    return r

res = {}
for k, agg in data.items():
    res[k] = {
        'prijmy': tot(agg, is_prijem),
        'vydaje': tot(agg, is_vydaj),
        'vydaje_bez_rez': tot(agg, lambda a, b: is_vydaj(a, b) and not is_rezerva(a, b)),
        'rezerva': tot(agg, lambda a, b: is_vydaj(a, b) and is_rezerva(a, b)),
        'investice': tot(agg, lambda a, b: is_vydaj(a, b) and b[:1] == '6'),
        'opravy': tot(agg, lambda a, b: is_vydaj(a, b) and b == '5171'),
        'bezne_bez_rez': tot(agg, lambda a, b: is_vydaj(a, b) and b[:1] == '5' and not is_rezerva(a, b)),
        'financovani_8115': tot(agg, lambda a, b: b == '8115'),
        't1': tot(agg, lambda a, b: b[:1] == '1' and b != '1122'),
        't2': tot(agg, lambda a, b: b[:1] == '2'),
        't3': tot(agg, lambda a, b: b[:1] == '3'),
        't4': tot(agg, lambda a, b: b[:1] == '4' and b != '4134'),
        't5': tot(agg, lambda a, b: is_vydaj(a, b) and b[:1] == '5'),
        't6': tot(agg, lambda a, b: is_vydaj(a, b) and b[:1] == '6'),
        'sdilene': tot(agg, lambda a, b: b in ('1111', '1112', '1113', '1119', '1121', '1211')),
        'dpo_obec': tot(agg, lambda a, b: b == '1122'),
        'dzn': tot(agg, lambda a, b: b == '1511'),
        'poplatky': tot(agg, lambda a, b: b[:2] in ('13',) and b[:3] != '138'),
        'hazard': tot(agg, lambda a, b: b[:3] == '138'),
        'nedanove': tot(agg, lambda a, b: b[:1] == '2'),
        'transfery': tot(agg, lambda a, b: b[:1] == '4' and b != '4134'),
        'p6330_vyd': tot(agg, lambda a, b: a == '6330' and b[:1] in '56'),
        'p4134': tot(agg, lambda a, b: b == '4134'),
    }

def m(x):
    return round(x / 1e6, 2)

print('== souhrn (mil. Kč) SR / UR / SK')
for k in sorted(res):
    print(k)
    for key, v in res[k].items():
        pct = (v[2] / v[1] * 100) if v[1] else float('nan')
        print(f'   {key:18s} {m(v[0]):8.2f} {m(v[1]):8.2f} {m(v[2]):8.2f}  {pct:5.0f} %')

# groups 2026
def groups(agg):
    g = defaultdict(lambda: [0.0, 0.0, 0.0])
    for (typ, par, pol), v in agg.items():
        if is_vydaj(par, pol):
            n = group_of(par, pol)
            for i in range(3):
                g[n][i] += v[i]
    return g

g26 = groups(data['2026_09'])
g25 = groups(data['2025_09']); g24 = groups(data['2024_09']); g23 = groups(data['2023_09'])
g25y = groups(data['2025_12'])
print('== skupiny 2026')
rows = []
for name, _ in GROUPS:
    v = g26.get(name, [0, 0, 0])
    if not any(v) and not any(g25.get(name, [0, 0, 0])):
        continue
    rows.append(name)
    pct = v[2] / v[1] * 100 if v[1] else 0
    print(f'{name:45s} {m(v[0]):7.2f} {m(v[1]):7.2f} {m(v[2]):7.2f} {pct:4.0f}% | 9/25 {m(g25[name][2]):6.2f} 9/24 {m(g24[name][2]):6.2f} 9/23 {m(g23[name][2]):6.2f} | 2025 rok {m(g25y[name][2]):6.2f}')

os.makedirs(OUT, exist_ok=True)
with open(os.path.join(OUT, 'rozpocet_2026_vydaje_podle_ucelu.csv'), 'w', encoding='utf-8', newline='') as f:
    w = csv.writer(f)
    w.writerow(['kategorie', 'schvaleny_2026_kc', 'upraveny_2026_kc', 'skutecnost_9_2026_kc', 'cerpani_upraveneho_pct',
                'skutecnost_9_2025_kc', 'skutecnost_9_2024_kc', 'skutecnost_9_2023_kc', 'skutecnost_cely_rok_2025_kc'])
    for name in rows:
        v = g26.get(name, [0, 0, 0])
        w.writerow([name, round(v[0], 2), round(v[1], 2), round(v[2], 2), round(v[2] / v[1] * 100, 1) if v[1] else '',
                    round(g25[name][2], 2), round(g24[name][2], 2), round(g23[name][2], 2), round(g25y[name][2], 2)])
    v = res['2026_09']['vydaje']
    w.writerow(['CELKEM', round(v[0], 2), round(v[1], 2), round(v[2], 2), round(v[2] / v[1] * 100, 1),
                round(res['2025_09']['vydaje'][2], 2), round(res['2024_09']['vydaje'][2], 2), round(res['2023_09']['vydaje'][2], 2), round(res['2025_12']['vydaje'][2], 2)])

# investice + opravy podle paragrafu 2026
print('== investice (tr. 6) a opravy (5171) podle paragrafu 2026 ')
io = defaultdict(lambda: [0.0] * 6)
for (typ, par, pol), v in data['2026_09'].items():
    if is_vydaj(par, pol) and (pol[:1] == '6' or pol == '5171'):
        k = 0 if pol[:1] == '6' else 3
        for i in range(3):
            io[(par)][k + i] += v[i]
with open(os.path.join(OUT, 'rozpocet_2026_investice_opravy.csv'), 'w', encoding='utf-8', newline='') as f:
    w = csv.writer(f)
    w.writerow(['paragraf', 'investice_schvaleny_kc', 'investice_upraveny_kc', 'investice_skutecnost_9_2026_kc',
                'opravy_5171_schvaleny_kc', 'opravy_5171_upraveny_kc', 'opravy_5171_skutecnost_9_2026_kc'])
    for par in sorted(io):
        v = io[par]
        print(par, [m(x) for x in v])
        w.writerow([par] + [round(x, 2) for x in v])

# detail rows print for key paragraphs
print('== detail 2026 (par, pol, SR, UR, SK) pro třídy 5,6 s UR>=100k nebo SK>=100k')
for (typ, par, pol), v in sorted(data['2026_09'].items(), key=lambda x: (x[0][1], x[0][2])):
    if is_vydaj(par, pol) and (abs(v[1]) >= 100000 or abs(v[2]) >= 100000 or abs(v[0]) >= 100000):
        print(par, pol, m(v[0]), m(v[1]), m(v[2]))
print('== příjmy detail 2026')
for (typ, par, pol), v in sorted(data['2026_09'].items(), key=lambda x: (x[0][2], x[0][1])):
    if is_prijem(par, pol) or pol in ('8115', '4134', '8124', '8117', '8118'):
        print(par, pol, round(v[0]), round(v[1]), round(v[2]))

# souhrn srovnani
with open(os.path.join(OUT, 'rozpocet_2026_srovnani_k_30_9.csv'), 'w', encoding='utf-8', newline='') as f:
    w = csv.writer(f)
    w.writerow(['ukazatel', 'rok', 'schvaleny_kc', 'upraveny_kc', 'skutecnost_k_30_9_kc', 'plneni_upraveneho_pct', 'skutecnost_cely_rok_kc'])
    for key, label in [('prijmy', 'Příjmy (třídy 1–4 bez 4134 a 1122)'), ('t1', 'Daňové příjmy (třída 1 bez 1122)'),
                       ('t2', 'Nedaňové příjmy (třída 2)'), ('t3', 'Kapitálové příjmy (třída 3)'), ('t4', 'Přijaté transfery (třída 4 bez 4134)'),
                       ('vydaje', 'Výdaje celkem (třídy 5–6)'), ('rezerva', 'z toho rezervy'), ('vydaje_bez_rez', 'Výdaje bez rezerv'),
                       ('t5', 'Běžné výdaje (třída 5, vč. rezervy)'), ('t6', 'Kapitálové výdaje (třída 6)'), ('opravy', 'Opravy (5171)')]:
        for y in ('2023', '2024', '2025', '2026'):
            v = res[f'{y}_09'][key]
            full = res.get(f'{y}_12', {}).get(key)
            w.writerow([label, y, round(v[0], 2), round(v[1], 2), round(v[2], 2), round(v[2] / v[1] * 100, 1) if v[1] else '',
                        round(full[2], 2) if full else ''])

# odhad příjmů: schválený vs skutečnost celý rok
print('== přesnost odhadu příjmů (celý rok): SR, UR, SK, SK/SR')
with open(os.path.join(OUT, 'rozpocet_2026_odhad_prijmu.csv'), 'w', encoding='utf-8', newline='') as f:
    w = csv.writer(f)
    w.writerow(['rok', 'ukazatel', 'schvaleny_kc', 'upraveny_kc', 'skutecnost_kc', 'skutecnost_k_30_9_kc', 'podil_k_30_9_z_celeho_roku_pct', 'skutecnost_vs_schvaleny_pct'])
    for y in ('2023', '2024', '2025', '2026'):
        for key, label in [('prijmy', 'Příjmy celkem'), ('sdilene', 'Sdílené daně (DPH, DPFO, DPPO)'), ('dzn', 'Daň z nemovitých věcí'),
                           ('poplatky', 'Poplatky (odpady, psi, správní aj.)'), ('nedanove', 'Nedaňové příjmy'), ('transfery', 'Přijaté transfery')]:
            v9 = res[f'{y}_09'][key]
            v12 = res.get(f'{y}_12', {}).get(key)
            if v12:
                print(y, label, m(v12[0]), m(v12[1]), m(v12[2]), f'{v12[2]/v12[0]*100 if v12[0] else 0:.0f}%', '| 9:', m(v9[2]), f'{v9[2]/v12[2]*100 if v12[2] else 0:.0f}% roku')
                w.writerow([y, label, round(v12[0], 2), round(v12[1], 2), round(v12[2], 2), round(v9[2], 2),
                            round(v9[2] / v12[2] * 100, 1) if v12[2] else '', round(v12[2] / v12[0] * 100, 1) if v12[0] else ''])
            else:
                print(y, label, m(v9[0]), m(v9[1]), '9:', m(v9[2]))
                w.writerow([y, label, round(v9[0], 2), round(v9[1], 2), '', round(v9[2], 2), '', ''])
json.dump({k: v for k, v in res.items()}, open(os.path.join(sys.argv[4]), 'w'), ensure_ascii=False, indent=1)
