"""Data dictionary entries for the school and social data (pages srovnani-skolstvi-socialni, podobne-skolstvi-socialni)."""

_OBCE = 'HD, sousední obce (Pazderna, Dolní Domaslavice, Lučina, Vojkovice) a podobné obce (Písková Lhota, Rebešovice, Závišice)'

SOCIALNI_DATASETS = {
    'skolstvi_socialni_exekuce_2026-10.csv': {
        'popis': f'Osoby v exekuci podle Exekutorské komory: {_OBCE}, jejich okresy, kraje a ČR.',
        'radek': 'jedno území (obec, okres, kraj, ČR)',
        'zdroj': 'Exekutorská komora ČR, mapa exekucí (obce.json, stav k 1. 10. 2026); obyvatelé 15+ ČSÚ.',
        'pozor': ['Podíl je počítán dvakrát: ze sčítání 2021 a z počtu obyvatel 15+ k 31. 12. 2024.'],
        'sloupce': {
            'kod_obce': 'Kód obce, okresu nebo kraje.', 'uzemi': 'Název území.', 'okres': 'Okres.', 'kraj': 'Kraj.',
            'osoby_v_exekuci': 'Počet osob v exekuci.', 'pocet_exekuci': 'Počet exekucí.', 'exekuci_na_osobu': 'Průměrný počet exekucí na osobu.',
            'obyv_15plus_SLDB2021': 'Obyvatelé 15+ podle sčítání 2021.', 'podil_SLDB2021_procent': 'Podíl osob v exekuci na obyvatelích 15+ (sčítání 2021), %.',
            'obyv_15plus_2024_12_31': 'Obyvatelé 15+ k 31. 12. 2024.', 'podil_2024_procent': 'Podíl osob v exekuci na obyvatelích 15+ (2024), %.',
            'stav_k': 'Datum stavu dat Exekutorské komory.',
        },
    },
    'skolstvi_socialni_nezamestnanost_MPSV_rocni.csv': {
        'popis': f'Podíl nezaměstnaných osob (PNO) podle MPSV, roční průměry: {_OBCE}, okresy a ČR.',
        'radek': 'jedno území × rok',
        'zdroj': 'MPSV, otevřená data evidence uchazečů (evid_pno_adresa_agr_frz_odata), data do 9/2026.',
        'pozor': ['Rok 2026 je průměr jen za dostupné měsíce (sloupec pocet_mesicu). U malých obcí kolísá podíl i o jednotlivce.'],
        'sloupce': {
            'uzemi': 'Obec, okres nebo ČR.', 'rok': 'Rok.', 'pocet_mesicu': 'Počet měsíců v průměru.',
            'pno_prumer_procent': 'Průměrný podíl nezaměstnaných osob (dosažitelní uchazeči 15–64 / obyvatelé 15–64), %.',
            'dosazitelni_min': 'Nejnižší měsíční počet dosažitelných uchazečů.', 'dosazitelni_max': 'Nejvyšší měsíční počet dosažitelných uchazečů.',
            'posledni_mesic': 'Poslední měsíc v datech.', 'pno_posledni_mesic': 'PNO v posledním měsíci, %.',
            'dosazitelni_posledni': 'Dosažitelní uchazeči v posledním měsíci.', 'obyv_15_64_posledni': 'Obyvatelé 15–64 použití pro poslední měsíc.',
        },
    },
    'skolstvi_socialni_kriminalita_2013-2026.csv': {
        'popis': f'Trestné činy, přestupky a dopravní nehody podle mapy kriminality Policie ČR: {_OBCE}.',
        'radek': 'jedna obec × rok',
        'zdroj': 'Policie ČR, mapa kriminality (API), 2013–2026; obyvatelé ČSÚ.',
        'pozor': ['Rok 2026 je neúplný (sloupec posledni_datum). Policie zveřejňuje jen vybrané druhy trestných činů. Na malých obcích jeden pachatel výrazně mění čísla.'],
        'sloupce': {
            'kod_obce': 'Kód obce ČSÚ.', 'obec': 'Obec.', 'rok': 'Rok.', 'obyvatele_31_12': 'Obyvatelé k 31. 12.',
            'delikty_celkem': 'Delikty celkem (trestné činy, přestupky, nehody).', 'prestupky': 'Přestupky.',
            'trestne_ciny_zverejnovane': 'Trestné činy (zveřejňované druhy).', 'dopravni_nehody': 'Dopravní nehody.',
            'delikty_na_1000': 'Delikty na 1 000 obyvatel.', 'tc_na_1000': 'Trestné činy na 1 000 obyvatel.',
            'prestupky_BESIP': 'Dopravní přestupky (BESIP).', 'prestupky_rychlost': 'Z toho překročení rychlosti.',
            'posledni_datum': 'Poslední datum v datech za daný rok.',
        },
    },
    'skolstvi_socialni_ovzdusi_CHMU.csv': {
        'popis': f'Pětileté průměry znečištění ovzduší (benzo(a)pyren, PM10, PM2,5, NO2) v čtvercích 1 × 1 km: {_OBCE}.',
        'radek': 'jedna obec × období × ukazatel',
        'zdroj': 'ČHMÚ, pětileté průměrné koncentrace ve čtvercové síti 1 km (sit1000_5lprum); hranice obcí RÚIAN/MSK.',
        'pozor': ['Jde o modelové hodnoty pro čtverce 1 km, ne o měření v obci. Limit benzo(a)pyrenu je 1 ng/m³.'],
        'sloupce': {
            'kod_obce': 'Kód obce ČSÚ.', 'obec': 'Obec.', 'obdobi': 'Pětileté období.', 'ukazatel': 'Znečišťující látka a ukazatel.',
            'vazeny_prumer': 'Průměr čtverců vážený plochou v obci.', 'min_ctverec': 'Nejnižší hodnota čtverce.', 'max_ctverec': 'Nejvyšší hodnota čtverce.',
            'pocet_ctvercu': 'Počet čtverců zasahujících do obce.', 'plocha_km2_v_obci': 'Plocha průniku čtverců s obcí, km².',
            'pole_v_datech': 'Název pole v datech ČHMÚ.', 'hranice_obce': 'Zdroj hranice obce.',
        },
    },
    'skolstvi_socialni_skoly_rejstrik_2026-11.csv': {
        'popis': f'Školy a školská zařízení v obcích podle rejstříku škol MŠMT: {_OBCE} (a ZŠ a MŠ Dobratice, kam patří MŠ ve Vojkovicích).',
        'radek': 'jedna součást školy (MŠ, ZŠ, družina, jídelna…)',
        'zdroj': 'MŠMT, rejstřík škol a školských zařízení (krajské výstupy JSON-LD, stav k 1. 11. 2026).',
        'sloupce': {
            'obec': 'Obec.', 'red_izo': 'Identifikátor ředitelství školy (RED_IZO).', 'ico': 'IČO právnické osoby.',
            'pravnicka_osoba': 'Název školy (právnické osoby).', 'zrizovatel': 'Zřizovatel.', 'izo': 'Identifikátor součásti (IZO).',
            'soucast': 'Druh součásti (MŠ, ZŠ, ŠD, ŠJ…).', 'druh_kod': 'Kód druhu podle rejstříku.', 'kapacita': 'Kapacita.',
            'jednotka': 'Jednotka kapacity (děti, žáci, stravovaní…).', 'mista_vyuky': 'Místa poskytování vzdělávání.',
            'datum_vystupu': 'Datum výstupu rejstříku.', 'zdroj': 'Soubor rejstříku.',
        },
    },
    'skolstvi_socialni_zdravotni_socialni_sluzby.csv': {
        'popis': f'Zdravotní a sociální služby s místem poskytování v obci: {_OBCE}.',
        'radek': 'jedno místo poskytování nebo souhrnný řádek obce',
        'zdroj': 'Národní registr poskytovatelů zdravotních služeb (NRPZS) a registr poskytovatelů sociálních služeb MPSV, stav 1. 11. 2026.',
        'pozor': ['Poskytovatelé, kteří jsou fyzickými osobami, jsou uvedeni jen jako „fyzická osoba“.'],
        'sloupce': {
            'obec': 'Obec.', 'registr': 'Registr (NRPZS, RPSS).', 'druh': 'Druh péče nebo služby.',
            'zarizeni_nebo_poskytovatel': 'Zařízení nebo poskytovatel (bez jmen fyzických osob).', 'misto_poskytovani': 'Místo poskytování.',
            'od': 'Od kdy (podle registru).', 'poznamka': 'Poznámka.',
        },
    },
}
