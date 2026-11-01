"""Doplněk do slovnik.py: položky DATASETS pro data stránek srovnani-volby-spolky a podobne-volby-spolky.
Vložit do slovníku DATASETS (např. DATASETS.update(VOLBY_SPOLKY_DATASETS) za jeho definici)."""

_OBEC5 = 'Název obce: Horní Domaslavice, Pazderna, Dolní Domaslavice, Lučina nebo Vojkovice.'
_OBECP = 'Název obce: Horní Domaslavice, Písková Lhota, Rebešovice nebo Závišice.'
_KOD = 'Kód obce podle ČSÚ (HD 512192).'
_KOD_UZ = 'Kód území: kód obce ČSÚ, 8102 = okres Frýdek-Místek, CZ = Česká republika.'
_UZ = 'Název území (obec, okres nebo Česká republika).'

_KV = {
    'popis': 'Komunální volby 1994–2026 po obcích: voliči, účast, počet kandidátek a mandátů, rozdělení mandátů, typ kandidátek.',
    'radek': 'jedna obec × volby',
    'zdroj': 'volby.cz: výsledky za obec (kv1111) a seznamy zvolených (kv21111) 1994–2022, datové soubory kv2026 (vygenerováno 11. 10. 2026).',
    'pozor': ['Typ kandidátky je odvozený z navrhující strany zvolených kandidátů, u kandidátek bez mandátu a u roku 1994 z názvu.',
              'Pro rok 1994 volby.cz jména zvolených neuvádí, sloupce o zvolených jsou proto 0.'],
    'sloupce': {
        'kod_obce': _KOD, 'obec': None, 'rok': 'Rok voleb.',
        'pocet_clenu_zo': 'Počet členů zastupitelstva (mandátů).',
        'volici': 'Voliči v seznamu.', 'vydane_obalky': 'Vydané úřední obálky.', 'ucast_pct': 'Volební účast, %.',
        'platne_hlasy': 'Platné hlasy (v komunálních volbách má volič tolik hlasů, kolik je mandátů).',
        'pocet_kandidatek': 'Počet kandidátních listin.', 'pocet_kandidatu': 'Počet kandidátů na všech kandidátkách.',
        'kandidatek_s_mandatem': 'Počet kandidátek, které získaly aspoň jeden mandát.',
        'rozdeleni_mandatu': 'Mandáty jednotlivých kandidátek seřazené sestupně (např. „3 : 3 : 3 : 3 : 1“).',
        'nejsilnejsi_kandidatka_pct': 'Podíl hlasů nejsilnější kandidátky, %.',
        'kandidatek_typu_NK_SNK': 'Počet kandidátek zařazených jako nezávislí kandidáti nebo jejich sdružení.',
        'mandatu_kandidatkam_NK_SNK': 'Mandáty, které získaly kandidátky NK/SNK.',
        'zvolenych_celkem': 'Počet zvolených podle seznamu zvolených.',
        'zvolenych_navrh_NK': 'Zvolení, které navrhla „NK“ (bez navrhující strany).',
        'zvolenych_BEZPP': 'Zvolení bez politické příslušnosti.',
    },
}
_KAND = {
    'popis': 'Kandidátky v komunálních volbách 1994–2026: hlasy, mandáty a odvozený typ kandidátky.',
    'radek': 'jedna obec × volby × kandidátka',
    'zdroj': 'volby.cz (jako u souhrnu komunálních voleb).',
    'pozor': ['Kandidátky pojmenované jménem jednotlivého kandidáta jsou nahrazeny textem „kandidátka jednotlivce (NK)“; web neuvádí jména fyzických osob.'],
    'sloupce': {
        'kod_obce': _KOD, 'obec': None, 'rok': 'Rok voleb.', 'cislo': 'Číslo kandidátky (volební strany) podle volby.cz.',
        'kandidatka': 'Název kandidátky (zkrácený tak, jak ho uvádí volby.cz).', 'hlasy': 'Hlasy pro kandidátku.',
        'hlasy_pct': 'Podíl hlasů, %.', 'pocet_kandidatu': 'Počet kandidátů na kandidátce.', 'mandaty': 'Získané mandáty.',
        'typ_kandidatky': 'Odvozený typ: NK/SNK, strana/hnutí/koalice, strana/hnutí + NK; „(podle názvu)“ = odvozeno jen z názvu.',
        'kandidatu_navrh_NK_2026': 'Jen 2026: počet kandidátů navržených jako NK.',
        'kandidatu_celkem_2026': 'Jen 2026: počet kandidátů na kandidátce podle jmenného seznamu.',
    },
}
_KONT = {
    'popis': 'Kolik zastupitelů zvolených v daném roce bylo zvoleno už v předchozích volbách (bez jmen).',
    'radek': 'jedna obec × volby (od roku 2002)',
    'zdroj': 'Výpočet ze seznamů zvolených na volby.cz; porovnává se příjmení a jméno bez titulů.',
    'pozor': ['Změny příjmení se nezjišťovaly (u HD je známý jeden případ v roce 2026, není započten).',
              'Ve Vojkovicích byli v letech 2018 a 2022 zvoleni dva lidé se stejným jménem; rozlišeni jsou podle věku.'],
    'sloupce': {
        'kod_obce': _KOD, 'obec': None, 'rok': 'Rok voleb.', 'zvolenych_se_jmenem': 'Počet zvolených.',
        'zvoleni_i_v_minulych_volbach': 'Z nich zvolení i v bezprostředně předchozích volbách.',
        'pct_z_minulych': 'Podíl znovuzvolených z předchozích voleb, %.',
        'zvoleni_kdykoli_drive_od_1998': 'Z nich zvolení v kterýchkoli dřívějších volbách od roku 1998.',
        'pct_kdykoli_drive': 'Podíl zvolených kdykoli dříve, %.',
    },
}
_PSU = {
    'popis': 'Účast ve volbách do Poslanecké sněmovny 2013–2025.',
    'radek': 'jedno území × volby',
    'zdroj': 'volby.cz, appdata ps{rok}: výsledky za obec, okres a ČR.',
    'sloupce': {'kod': _KOD_UZ, 'uzemi': _UZ, 'rok': 'Rok voleb.', 'volici': 'Voliči v seznamu.',
                'vydane_obalky': 'Vydané obálky.', 'ucast_pct': 'Volební účast, %.', 'platne_hlasy': 'Platné hlasy.'},
}
_PSS = {
    'popis': 'Výsledky stran ve volbách do Poslanecké sněmovny 2013–2025.',
    'radek': 'jedno území × volby × strana',
    'zdroj': 'volby.cz, appdata ps{rok}.',
    'sloupce': {'kod': _KOD_UZ, 'uzemi': _UZ, 'rok': 'Rok voleb.', 'cislo': 'Číslo strany v daných volbách.',
                'strana': 'Název strany (zkrácený podle volby.cz).', 'hlasy': 'Hlasy.', 'pct': 'Podíl platných hlasů, %.'},
}
_PE = {
    'popis': 'Prezidentská volba 2023: účast v obou kolech a výsledek 2. kola (bez jmen kandidátů).',
    'radek': 'jedno území × kolo',
    'zdroj': 'volby.cz, pls/prez2023 (pe311, pe2).',
    'sloupce': {'kod': _KOD_UZ, 'uzemi': _UZ, 'kolo': '1. nebo 2. kolo.', 'volici': 'Voliči v seznamu.',
                'vydane_obalky': 'Vydané obálky.', 'ucast_pct': 'Volební účast, %.', 'platne_hlasy': 'Platné hlasy.',
                'k2_zvoleny_prezident_hlasy': 'Jen 2. kolo: hlasy pro kandidáta zvoleného prezidentem.',
                'k2_zvoleny_prezident_pct': 'Jen 2. kolo: jeho podíl, %.',
                'k2_protikandidat_hlasy': 'Jen 2. kolo: hlasy pro protikandidáta.', 'k2_protikandidat_pct': 'Jen 2. kolo: jeho podíl, %.'},
}
_ARS = {
    'popis': 'Ekonomické subjekty se sídlem v obci podle ARES, sloučené do skupin, i na 1 000 obyvatel.',
    'radek': 'jedna obec',
    'zdroj': 'ARES, vyhledání podle kódu obce sídla (POST /ekonomicke-subjekty-v-be/rest/ekonomicke-subjekty/vyhledat); HD, Pazderna, DD a Lučina stav k 30. 10. 2026, ostatní obce k 1. 11. 2026.',
    'pozor': ['Počítá se sídlo, ne místo působení. Podnikající FO jsou v ARES i tehdy, když aktivně nepodnikají.'],
    'sloupce': {'kod_obce': _KOD, 'obec': None, 'obyvatel_1_7_2025': 'Obyvatelé k 1. 7. 2025 (ČSÚ), základ přepočtu.',
                'subjektu_celkem': 'Subjekty celkem.', 'na_1000': 'Subjekty na 1 000 obyvatel.',
                'FO_podnikajici': 'Podnikající fyzické osoby (právní formy 101, 102, 105, 107, 424).', 'FO_na_1000': 'Na 1 000 obyvatel.',
                'obchodni_spolecnosti': 'Obchodní společnosti (111 v.o.s., 112 s.r.o., 121 a.s., 421 odštěpný závod).', 'OS_na_1000': 'Na 1 000 obyvatel.',
                'spolky_pobocne_ustavy': 'Spolky, pobočné spolky, ústavy, nadace, nadační fondy a o.p.s. (706, 736, 161, 117, 118, 141).',
                'spolky_na_1000': 'Na 1 000 obyvatel.', 'ostatni': 'Ostatní (obec, příspěvkové organizace, církevní osoby, SVJ, družstva aj.).'},
}
_ARP = {
    'popis': 'Ekonomické subjekty se sídlem v obci podle právní formy (ARES).',
    'radek': 'jedna obec × právní forma',
    'zdroj': 'ARES (jako souhrn subjektů); názvy právních forem z číselníku ARES PravniForma.',
    'sloupce': {'kod_obce': _KOD, 'obec': None, 'pravni_forma_kod': 'Kód právní formy.', 'pravni_forma': 'Název právní formy.',
                'pocet': 'Počet subjektů.', 'na_1000_obyv_2025': 'Na 1 000 obyvatel (k 1. 7. 2025).'},
}
_TR = {
    'popis': 'Transfery obcí neziskovým organizacím, církvím a fyzickým osobám po letech 2010–2025.',
    'radek': 'jedna obec × rok',
    'zdroj': 'Monitor státní pokladny MF, FIN 2-12 M za prosinec (skutečnost); obyvatelé ČSÚ k 1. 7.',
    'pozor': ['Hlavní ukazatel webu je `NNO_bez_par_6171_52xx_62xx` (položky 5221 + 5222 + 5229 bez § 6171 a § 52xx, 62xx).',
              'Výkaz neukazuje příjemce plateb.'],
    'sloupce': {'kod_obce': _KOD, 'obec': None, 'rok': 'Rozpočtový rok.', 'obyvatel_1_7': 'Obyvatelé k 1. 7.',
                'pol_5221': 'Položka 5221 – obecně prospěšným společnostem. Kč.', 'pol_5222': 'Položka 5222 – spolkům. Kč.',
                'pol_5223': 'Položka 5223 – církvím a náboženským společnostem. Kč.',
                'pol_5229': 'Položka 5229 – ostatním neziskovým a podobným organizacím. Kč.',
                'pol_5492': 'Položka 5492 – dary obyvatelstvu. Kč.', 'pol_5493': 'Položka 5493 – účelové neinvestiční transfery fyzickým osobám. Kč.',
                'pol_6322': 'Položka 6322 – investiční transfery spolkům. Kč.',
                'neinv_NNO_5221_5222_5229': 'Součet 5221 + 5222 + 5229 (neočištěno). Kč.', 'na_obyvatele': 'Předchozí sloupec na obyvatele. Kč.',
                'vcetne_cirkvi_5223': 'Součet 5221 + 5222 + 5229 + 5223. Kč.', 'vcetne_cirkvi_na_obyv': 'Předchozí sloupec na obyvatele. Kč.',
                'NNO_bez_par_6171_52xx_62xx': '5221 + 5222 + 5229 bez § 6171, § 52xx a § 62xx (očištěno). Kč.',
                'NNO_ocist_na_obyv': 'Očištěný součet na obyvatele. Kč.'},
}
_TRP = {
    'popis': 'Rozpis transferů z `transfery_NNO_*` podle paragrafu a položky.',
    'radek': 'jedna obec × rok × paragraf × položka',
    'zdroj': 'Monitor státní pokladny MF, FIN 2-12 M.',
    'sloupce': {'kod_obce': _KOD, 'obec': None, 'rok': 'Rozpočtový rok.', 'paragraf': 'Paragraf rozpočtové skladby.',
                'polozka': 'Položka (5221, 5222, 5223, 5229, 5492, 5493, 6322).', 'polozka_nazev': 'Název položky.',
                'schvaleny': 'Schválený rozpočet. Kč.', 'upraveny': 'Upravený rozpočet. Kč.', 'skutecnost': 'Skutečnost. Kč.'},
}


def _ds(base, obec, popis_navic=''):
    d = {k: (dict(v) if isinstance(v, dict) else v) for k, v in base.items()}
    d['sloupce'] = {k: (obec if v is None else v) for k, v in base['sloupce'].items()}
    if popis_navic:
        d['popis'] = d['popis'] + popis_navic
    return d


VOLBY_SPOLKY_DATASETS = {}
for _n, _b in [('volby_komunalni_{}1994-2026.csv', _KV), ('volby_komunalni_kandidatky_{}1994-2026.csv', _KAND),
               ('volby_komunalni_kontinuita_{}2002-2026.csv', _KONT), ('volby_snemovni_ucast_{}2013-2025.csv', _PSU),
               ('volby_snemovni_strany_{}2013-2025.csv', _PSS), ('transfery_NNO_{}2010-2025.csv', _TR),
               ('transfery_NNO_paragrafy_{}2010-2025.csv', _TRP)]:
    VOLBY_SPOLKY_DATASETS[_n.format('sousede_')] = _ds(_b, _OBEC5, ' HD a sousední obce.')
    VOLBY_SPOLKY_DATASETS['podobne_obce_' + _n.format('')] = _ds(_b, _OBECP, ' HD a podobné obce.')
VOLBY_SPOLKY_DATASETS['volby_prezidentska_2023_sousede.csv'] = _ds(_PE, _OBEC5, ' HD, sousední obce, okres FM a ČR.')
VOLBY_SPOLKY_DATASETS['podobne_obce_volby_prezidentska_2023.csv'] = _ds(_PE, _OBECP, ' HD, podobné obce a ČR.')
VOLBY_SPOLKY_DATASETS['subjekty_ARES_souhrn_sousede.csv'] = _ds(_ARS, _OBEC5, ' HD a sousední obce.')
VOLBY_SPOLKY_DATASETS['podobne_obce_subjekty_ARES_souhrn.csv'] = _ds(_ARS, _OBECP, ' HD a podobné obce.')
VOLBY_SPOLKY_DATASETS['subjekty_ARES_pravni_forma_sousede.csv'] = _ds(_ARP, _OBEC5, ' HD a sousední obce.')
VOLBY_SPOLKY_DATASETS['podobne_obce_subjekty_ARES_pravni_forma.csv'] = _ds(_ARP, _OBECP, ' HD a podobné obce.')
