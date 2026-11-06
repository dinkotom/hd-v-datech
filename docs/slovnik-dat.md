# Slovník dat

Popis datových souborů webu Horní Domaslavice v datech (https://hd-v-datech.cz/). Všechny soubory jsou CSV v UTF-8, oddělovač čárka, desetinná tečka, data ve tvaru RRRR-MM-DD. Částky jsou v Kč, běžné ceny.

## CUZK_UHDP_druhy_pozemku_sousede_2004_2014_2026.csv

Výměry druhů pozemků po katastrálních územích HD a sousedních obcí (orná půda, louky, lesy, zastavěné plochy…).

- Odkaz: [data/CUZK_UHDP_druhy_pozemku_sousede_2004_2014_2026.csv](https://hd-v-datech.cz/data/CUZK_UHDP_druhy_pozemku_sousede_2004_2014_2026.csv)
- Řádků: 21; jeden řádek = jeden rok × katastrální území
- Zdroj: ČÚZK, úhrnné hodnoty druhů pozemků (UHDP).
- Pozor: Dolní Domaslavice mají dvě katastrální území (Dolní Domaslavice a Volovec), Lučina také (Lučina a Kocurovice). Za obec je třeba řádky sečíst podle sloupce `obec`.

| Sloupec | Význam |
|---|---|
| `rok` | Rok stavu (1. 1. 2004, 1. 1. 2014, 1. 10. 2026). |
| `obec` | Zkratka obce: HD, PA (Pazderna), DD, LU (Lučina), VOJ (Vojkovice); v souboru podobných obcí PL, REB, ZAV. |
| `ku_kod` | Kód katastrálního území. |
| `ku` | Název katastrálního území. |
| `celkem_ha` | Výměra celkem, ha. |
| `orna_ha` | Orná půda, ha. |
| `zahrada_ha` | Zahrady, ha. |
| `sad_ha` | Ovocné sady, ha. |
| `ttp_ha` | Trvalé travní porosty (louky, pastviny), ha. |
| `les_ha` | Lesní pozemky, ha. |
| `voda_ha` | Vodní plochy, ha. |
| `zastavena_ha` | Zastavěné plochy a nádvoří, ha. |
| `ostatni_ha` | Ostatní plochy (cesty, zeleň, manipulační plochy…), ha. |

## RUIAN_souhrn_sousede_stav_20260930.csv

Budovy, byty a technické vybavení podle Registru územní identifikace (RÚIAN), stav 30. 9. 2026.

- Odkaz: [data/RUIAN_souhrn_sousede_stav_20260930.csv](https://hd-v-datech.cz/data/RUIAN_souhrn_sousede_stav_20260930.csv)
- Řádků: 20; jeden řádek = jeden ukazatel; sloupce jsou obce
- Zdroj: RÚIAN (ČÚZK), výměnný formát VFR.
- Pozor: Údaje o vodovodu, kanalizaci a plynu jsou v RÚIAN neúplné a často zastaralé (viz `kanal_nezjist`). Spolehlivější je sčítání 2021 na stránce Obyvatelstvo a výstavba.

| Sloupec | Význam |
|---|---|
| `ukazatel` | Kód ukazatele (počet stavebních objektů, není-li uvedeno jinak): `RD_s_cp` rodinné domy s číslem popisným; `RD_vse` všechny rodinné domy; `SO_celkem` stavební objekty celkem; `adresni_mista` adresní místa; `bez_cp_ce` objekty bez čísla popisného i evidenčního; `bytovy_dum` bytové domy; `byty_RUIAN` počet bytů; `kanal_COV` domácí čistírna odpadních vod; `kanal_zumpa` žumpa nebo septik; `kanal_sit` veřejná kanalizace; `kanal_nic` bez odkanalizování; `kanal_nezjist` neuvedeno; `max_cp` nejvyšší přidělené číslo popisné; `plyn_verejny` přípojka plynu; `rekreace` stavby pro rodinnou rekreaci; `rekreace_s_ce` z toho s číslem evidenčním; `s_ce` objekty s číslem evidenčním; `s_cp` objekty s číslem popisným; `vodovod_s` s přípojkou vodovodu; `vodovod_bez` bez vodovodu. |
| `HD` | Horní Domaslavice. |
| `Pazderna` | Pazderna. |
| `DD` | Dolní Domaslavice. |
| `Lucina` | Lučina. |
| `Vojkovice` | Vojkovice. |
| `Nosovice` | Nošovice. |
| `DTosanovice` | Dolní Tošanovice. |

## finance_DD_2010-2025.csv

Hospodaření obce Dolní Domaslavice po letech 2010–2025 (stejné sloupce jako `finance_HD_2010-2025.csv`; obec zřizuje základní školu).

- Odkaz: [data/finance_DD_2010-2025.csv](https://hd-v-datech.cz/data/finance_DD_2010-2025.csv)
- Řádků: 16; jeden řádek = jeden rozpočtový rok
- Zdroj: Monitor státní pokladny MF: výkaz FIN 2-12 M za prosinec (plnění rozpočtu) a rozvaha k 31. 12.
- Pozor: Částky v Kč, běžné ceny. Rok 2026 zatím chybí (MF zveřejní roční data na jaře 2027).
- Pozor: Sloupec `X_na_obyv` = `X` na obyvatele: toky děleno `obyv_1_7`, stavy k 31. 12. (účty, peníze, úvěry, závazky) děleno `obyv_31_12`.

Sloupce jsou stejné jako v `finance_HD_2010-2025.csv`.

## finance_DTO_2010-2025.csv

Hospodaření obce Dolní Tošanovice (okres Frýdek-Místek, IČO 00576875), sousední obce HD, po letech 2010–2025 (stejné sloupce jako `finance_HD_2010-2025.csv`).

- Odkaz: [data/finance_DTO_2010-2025.csv](https://hd-v-datech.cz/data/finance_DTO_2010-2025.csv)
- Řádků: 16; jeden řádek = jeden rozpočtový rok
- Zdroj: Monitor státní pokladny MF: výkaz FIN 2-12 M za prosinec (plnění rozpočtu) a rozvaha k 31. 12.
- Pozor: Částky v Kč, běžné ceny. Rok 2026 zatím chybí (MF zveřejní roční data na jaře 2027).
- Pozor: Sloupec `X_na_obyv` = `X` na obyvatele: toky děleno `obyv_1_7`, stavy k 31. 12. (účty, peníze, úvěry, závazky) děleno `obyv_31_12`.

Sloupce jsou stejné jako v `finance_HD_2010-2025.csv`.

## finance_HD_2010-2025.csv

Hospodaření obce Horní Domaslavice po letech 2010–2025: příjmy, výdaje, investice, opravy, dotace, rezervy, peníze a úvěry.

- Odkaz: [data/finance_HD_2010-2025.csv](https://hd-v-datech.cz/data/finance_HD_2010-2025.csv)
- Řádků: 16; jeden řádek = jeden rozpočtový rok
- Zdroj: Monitor státní pokladny MF: výkaz FIN 2-12 M za prosinec (plnění rozpočtu) a rozvaha k 31. 12.
- Pozor: Částky v Kč, běžné ceny. Rok 2026 zatím chybí (MF zveřejní roční data na jaře 2027).
- Pozor: Sloupec `X_na_obyv` = `X` na obyvatele: toky děleno `obyv_1_7`, stavy k 31. 12. (účty, peníze, úvěry, závazky) děleno `obyv_31_12`.

| Sloupec | Význam |
|---|---|
| `rok` | Rozpočtový rok. |
| `obyv_1_7` | Počet obyvatel k 1. 7. daného roku (ČSÚ). Tímto číslem se dělí toky (příjmy, výdaje…) ve sloupcích `*_na_obyv`. |
| `obyv_31_12` | Počet obyvatel k 31. 12. daného roku (ČSÚ). Tímto číslem se dělí stavy (`ucet_*`, `penize_*`, úvěry a závazky) ve sloupcích `*_na_obyv`. |
| `prijmy` | Příjmy celkem = třídy 1–4 rozpočtové skladby bez převodů z vlastních fondů (položky 413x) a bez daně z příjmů, kterou obec platí sama sobě (položka 1122, viz `dppo_obec`). Kč. |
| `trida1` | Daňové příjmy (třída 1): sdílené daně, daň z nemovitých věcí, místní poplatky aj.; bez položky 1122 (daň placená obcí sama sobě). Kč. |
| `rud` | Sdílené daně (rozpočtové určení daní: DPH, daně z příjmů fyzických a právnických osob). Kč. |
| `dan_nemovitosti` | Daň z nemovitých věcí (položka 1511). Kč. |
| `dppo_obec` | Daň z příjmů právnických osob za obec (položka 1122). Obec ji platí sama sobě; částka je odečtena z `prijmy`, `trida1` i `vydaje` (protějšek ve výdajích bývá v § 6399, u některých obcí a let v § 6171). Kč. |
| `trida2` | Nedaňové příjmy (třída 2): pronájmy, prodej služeb, úroky aj. Kč. |
| `trida3` | Kapitálové příjmy (třída 3): prodej majetku. Kč. |
| `trida4` | Přijaté transfery (třída 4) bez převodů z vlastních fondů = `dotace_neinv` + `dotace_inv`. Kč. |
| `dotace_neinv` | Neinvestiční přijaté transfery (včetně souhrnného dotačního vztahu na výkon státní správy). Kč. |
| `dotace_inv` | Investiční přijaté dotace. Kč. |
| `vydaje` | Výdaje celkem = třídy 5 a 6 bez převodů mezi vlastními účty (§ 6330), minus daň z příjmů placená obcí sama sobě (částka `dppo_obec`). Ostatní platby v § 6399 (např. odvody DPH) se počítají. Kč. |
| `vydaje_sch` | Schválený rozpočet výdajů (stejné vymezení jako `vydaje`). Kč. |
| `vydaje_upr` | Upravený rozpočet výdajů ke konci roku (po rozpočtových opatřeních), stejné vymezení jako `vydaje`. Kč. |
| `investice` | Investiční (kapitálové) výdaje, třída 6. Kč. |
| `opravy` | Opravy a udržování, položka 5171. Kč. |
| `io` | Investice a opravy = `investice` + `opravy`. Hlavní ukazatel webu pro „kolik obec dává do majetku“. Kč. |
| `io_vlastni` | Investice a opravy z vlastních zdrojů = `io` − `dotace_inv`. Kč. |
| `vodovod_kanalizace` | Výdaje na vodovod a kanalizaci (§ 2310 a 2321), běžné i investiční. Kč. |
| `rez3639_upr` | Rezerva v upraveném rozpočtu na řádku § 3639 / položka 5169. Obec HD sem od roku 2017 ukládá zapojený zůstatek z minulých let; prakticky se z ní nečerpá. Kč. |
| `rez3639_sk` | Skutečné čerpání z řádku § 3639 / položka 5169. Kč. |
| `rez5901_upr` | Nespecifikované rezervy (položka 5901) v upraveném rozpočtu. Kč. |
| `rez5901_sk` | Skutečné čerpání položky 5901 (bývá 0, rezerva se přesouvá rozpočtovým opatřením). Kč. |
| `saldo` | Saldo = `prijmy` − `vydaje` (kladné = přebytek). Kč. |
| `ucet_231` | Základní běžný účet obce (účet 231) k 31. 12. podle rozvahy. Kč. |
| `ucet_236` | Běžné účty fondů obce (účet 236) k 31. 12. Kč. |
| `ucet_244` | Termínované vklady krátkodobé (účet 244) k 31. 12. Kč. |
| `ucet_245` | Jiné běžné účty (účet 245) k 31. 12. Kč. |
| `penize_231_244_245` | Peníze obce k 31. 12. = účty 231 + 244 + 245. Kč. |
| `penize_vc_236` | Peníze obce k 31. 12. včetně fondů = 231 + 244 + 245 + 236. Kč. |
| `kratkodobe_uvery_281` | Krátkodobé úvěry (účet 281) k 31. 12. Kč. |
| `dlouhodobe_uvery_451` | Dlouhodobé úvěry (účet 451) k 31. 12. Kč. |
| `uvery_281_451` | Úvěry celkem = 281 + 451. Kč. |
| `rezerva_upr` | Rezervy v upraveném rozpočtu celkem = `rez3639_upr` + `rez5901_upr`. Kč. |
| `rezerva_sk` | Čerpání rezerv celkem = `rez3639_sk` + `rez5901_sk`. Kč. |
| `necerpano` | Nevyčerpaná část upraveného rozpočtu výdajů = `vydaje_upr` − `vydaje`. Kč. |
| `dlouhodobe_zavazky_459` | Ostatní dlouhodobé závazky (účet 459) k 31. 12.; věřitele výkazy neuvádějí. Kč. |
| `pr_4134` | Převody z rozpočtových účtů (položka 4134); do `prijmy` se nepočítají. Kč. |
| `pr_413x_ostatni` | Ostatní převody z vlastních fondů (413x kromě 4134); do `prijmy` se nepočítají. Kč. |
| `vyd_6330` | Převody mezi vlastními účty (§ 6330); do `vydaje` se nepočítají. Kč. |
| `vyd_6399` | Ostatní finanční operace (§ 6399): hlavně daň z příjmů za obec, u některých obcí i odvody DPH. Do `vydaje` se počítají, odečte se jen částka `dppo_obec`. Kč. |
| `*_na_obyv` (40 sloupců) | Stejnojmenný sloupec bez přípony na obyvatele: toky děleno `obyv_1_7`, stavy k 31. 12. (účty, peníze, úvěry, závazky) děleno `obyv_31_12`. Kč. |

## finance_LUC_2010-2025.csv

Hospodaření obce Lučina po letech 2010–2025 (stejné sloupce jako `finance_HD_2010-2025.csv`; obec zřizuje základní školu a má výdaje spojené s nádrží Žermanice).

- Odkaz: [data/finance_LUC_2010-2025.csv](https://hd-v-datech.cz/data/finance_LUC_2010-2025.csv)
- Řádků: 16; jeden řádek = jeden rozpočtový rok
- Zdroj: Monitor státní pokladny MF: výkaz FIN 2-12 M za prosinec (plnění rozpočtu) a rozvaha k 31. 12.
- Pozor: Částky v Kč, běžné ceny. Rok 2026 zatím chybí (MF zveřejní roční data na jaře 2027).
- Pozor: Sloupec `X_na_obyv` = `X` na obyvatele: toky děleno `obyv_1_7`, stavy k 31. 12. (účty, peníze, úvěry, závazky) děleno `obyv_31_12`.

Sloupce jsou stejné jako v `finance_HD_2010-2025.csv`.

## finance_NOS_2010-2025.csv

Hospodaření obce Nošovice (okres Frýdek-Místek, IČO 00577049), sousední obce HD, po letech 2010–2025 (stejné sloupce jako `finance_HD_2010-2025.csv`).

- Odkaz: [data/finance_NOS_2010-2025.csv](https://hd-v-datech.cz/data/finance_NOS_2010-2025.csv)
- Řádků: 16; jeden řádek = jeden rozpočtový rok
- Zdroj: Monitor státní pokladny MF: výkaz FIN 2-12 M za prosinec (plnění rozpočtu) a rozvaha k 31. 12.
- Pozor: Částky v Kč, běžné ceny. Rok 2026 zatím chybí (MF zveřejní roční data na jaře 2027).
- Pozor: Sloupec `X_na_obyv` = `X` na obyvatele: toky děleno `obyv_1_7`, stavy k 31. 12. (účty, peníze, úvěry, závazky) děleno `obyv_31_12`.

Sloupce jsou stejné jako v `finance_HD_2010-2025.csv`.

## finance_PAZ_2010-2025.csv

Hospodaření obce Pazderna po letech 2010–2025 (stejné sloupce jako `finance_HD_2010-2025.csv`).

- Odkaz: [data/finance_PAZ_2010-2025.csv](https://hd-v-datech.cz/data/finance_PAZ_2010-2025.csv)
- Řádků: 16; jeden řádek = jeden rozpočtový rok
- Zdroj: Monitor státní pokladny MF: výkaz FIN 2-12 M za prosinec (plnění rozpočtu) a rozvaha k 31. 12.
- Pozor: Částky v Kč, běžné ceny. Rok 2026 zatím chybí (MF zveřejní roční data na jaře 2027).
- Pozor: Sloupec `X_na_obyv` = `X` na obyvatele: toky děleno `obyv_1_7`, stavy k 31. 12. (účty, peníze, úvěry, závazky) děleno `obyv_31_12`.

Sloupce jsou stejné jako v `finance_HD_2010-2025.csv`.

## finance_PL_2010-2025.csv

Hospodaření obce Písková Lhota (okres Mladá Boleslav, IČO 00509230) po letech 2010–2025 (stejné sloupce jako `finance_HD_2010-2025.csv`). Podobná obec pro srovnání.

- Odkaz: [data/finance_PL_2010-2025.csv](https://hd-v-datech.cz/data/finance_PL_2010-2025.csv)
- Řádků: 16; jeden řádek = jeden rozpočtový rok
- Zdroj: Monitor státní pokladny MF: výkaz FIN 2-12 M za prosinec (plnění rozpočtu) a rozvaha k 31. 12.
- Pozor: Částky v Kč, běžné ceny. Rok 2026 zatím chybí (MF zveřejní roční data na jaře 2027).
- Pozor: Sloupec `X_na_obyv` = `X` na obyvatele: toky děleno `obyv_1_7`, stavy k 31. 12. (účty, peníze, úvěry, závazky) děleno `obyv_31_12`.

Sloupce jsou stejné jako v `finance_HD_2010-2025.csv`.

## finance_REB_2010-2025.csv

Hospodaření obce Rebešovice (okres Brno-venkov, IČO 00488089) po letech 2010–2025 (stejné sloupce jako `finance_HD_2010-2025.csv`). Podobná obec pro srovnání.

- Odkaz: [data/finance_REB_2010-2025.csv](https://hd-v-datech.cz/data/finance_REB_2010-2025.csv)
- Řádků: 16; jeden řádek = jeden rozpočtový rok
- Zdroj: Monitor státní pokladny MF: výkaz FIN 2-12 M za prosinec (plnění rozpočtu) a rozvaha k 31. 12.
- Pozor: Částky v Kč, běžné ceny. Rok 2026 zatím chybí (MF zveřejní roční data na jaře 2027).
- Pozor: Sloupec `X_na_obyv` = `X` na obyvatele: toky děleno `obyv_1_7`, stavy k 31. 12. (účty, peníze, úvěry, závazky) děleno `obyv_31_12`.

Sloupce jsou stejné jako v `finance_HD_2010-2025.csv`.

## finance_VOJ_2010-2025.csv

Hospodaření obce Vojkovice (okres Frýdek-Místek, IČO 00577081), sousední obce HD, po letech 2010–2025 (stejné sloupce jako `finance_HD_2010-2025.csv`).

- Odkaz: [data/finance_VOJ_2010-2025.csv](https://hd-v-datech.cz/data/finance_VOJ_2010-2025.csv)
- Řádků: 16; jeden řádek = jeden rozpočtový rok
- Zdroj: Monitor státní pokladny MF: výkaz FIN 2-12 M za prosinec (plnění rozpočtu) a rozvaha k 31. 12.
- Pozor: Částky v Kč, běžné ceny. Rok 2026 zatím chybí (MF zveřejní roční data na jaře 2027).
- Pozor: Sloupec `X_na_obyv` = `X` na obyvatele: toky děleno `obyv_1_7`, stavy k 31. 12. (účty, peníze, úvěry, závazky) děleno `obyv_31_12`.

Sloupce jsou stejné jako v `finance_HD_2010-2025.csv`.

## finance_ZAV_2010-2025.csv

Hospodaření obce Závišice (okres Nový Jičín, IČO 00600709) po letech 2010–2025 (stejné sloupce jako `finance_HD_2010-2025.csv`). Podobná obec pro srovnání.

- Odkaz: [data/finance_ZAV_2010-2025.csv](https://hd-v-datech.cz/data/finance_ZAV_2010-2025.csv)
- Řádků: 16; jeden řádek = jeden rozpočtový rok
- Zdroj: Monitor státní pokladny MF: výkaz FIN 2-12 M za prosinec (plnění rozpočtu) a rozvaha k 31. 12.
- Pozor: Částky v Kč, běžné ceny. Rok 2026 zatím chybí (MF zveřejní roční data na jaře 2027).
- Pozor: Sloupec `X_na_obyv` = `X` na obyvatele: toky děleno `obyv_1_7`, stavy k 31. 12. (účty, peníze, úvěry, závazky) děleno `obyv_31_12`.

Sloupce jsou stejné jako v `finance_HD_2010-2025.csv`.

## investice_opravy_podle_paragrafu_sousede.csv

Investice a opravy HD a sousedních obcí podle paragrafu rozpočtové skladby (na co šly).

- Odkaz: [data/investice_opravy_podle_paragrafu_sousede.csv](https://hd-v-datech.cz/data/investice_opravy_podle_paragrafu_sousede.csv)
- Řádků: 1094; jeden řádek = jedna obec × rok × paragraf (jen nenulové)
- Zdroj: Monitor státní pokladny MF, FIN 2-12 M.

| Sloupec | Význam |
|---|---|
| `obec` | Název obce: Horní Domaslavice, Pazderna, Dolní Domaslavice nebo Lučina. |
| `rok` | Rozpočtový rok. |
| `paragraf` | Paragraf rozpočtové skladby (např. 2212 silnice, 2219 chodníky a ostatní komunikace, 3111 mateřská škola, 3412 sportovní zařízení, 3613 nebytové hospodářství, 3631 veřejné osvětlení, 5512 hasiči). |
| `investice_plus_opravy_kc` | Třída 6 + položka 5171 v daném paragrafu. Kč. |

## podobne_obce_CUZK_UHDP_2004_2014_2026.csv

Výměry druhů pozemků HD, Pískové Lhoty (PL), Rebešovic (REB) a Závišic (ZAV) v letech 2004, 2014 a 2026 (stejné sloupce jako `CUZK_UHDP_druhy_pozemku_sousede_2004_2014_2026.csv`).

- Odkaz: [data/podobne_obce_CUZK_UHDP_2004_2014_2026.csv](https://hd-v-datech.cz/data/podobne_obce_CUZK_UHDP_2004_2014_2026.csv)
- Řádků: 12; jeden řádek = jeden rok × katastrální území
- Zdroj: ČÚZK, úhrnné hodnoty druhů pozemků (UHDP).
- Pozor: Dolní Domaslavice mají dvě katastrální území (Dolní Domaslavice a Volovec), Lučina také (Lučina a Kocurovice). Za obec je třeba řádky sečíst podle sloupce `obec`.

Sloupce jsou stejné jako v `CUZK_UHDP_druhy_pozemku_sousede_2004_2014_2026.csv`.

## podobne_obce_RUIAN_souhrn_stav_20260930.csv

Budovy, byty a technické vybavení podle RÚIAN (stav 30. 9. 2026) pro HD, Pískovou Lhotu, Rebešovice a Závišice (stejné řádky jako `RUIAN_souhrn_sousede_stav_20260930.csv`).

- Odkaz: [data/podobne_obce_RUIAN_souhrn_stav_20260930.csv](https://hd-v-datech.cz/data/podobne_obce_RUIAN_souhrn_stav_20260930.csv)
- Řádků: 20; jeden řádek = jeden ukazatel; sloupce jsou obce
- Zdroj: RÚIAN (ČÚZK), výměnný formát VFR.
- Pozor: Údaje o vodovodu, kanalizaci a plynu jsou v RÚIAN neúplné a často zastaralé (viz `kanal_nezjist`). Spolehlivější je sčítání 2021 na stránce Obyvatelstvo a výstavba.

Sloupce jsou stejné jako v `RUIAN_souhrn_sousede_stav_20260930.csv`.

## podobne_obce_investice_podle_paragrafu.csv

Investice a opravy HD, Pískové Lhoty, Rebešovic a Závišic podle paragrafu rozpočtové skladby (stejné sloupce jako `investice_opravy_podle_paragrafu_sousede.csv`).

- Odkaz: [data/podobne_obce_investice_podle_paragrafu.csv](https://hd-v-datech.cz/data/podobne_obce_investice_podle_paragrafu.csv)
- Řádků: 679; jeden řádek = jedna obec × rok × paragraf (jen nenulové)
- Zdroj: Monitor státní pokladny MF, FIN 2-12 M.

Sloupce jsou stejné jako v `investice_opravy_podle_paragrafu_sousede.csv`.

## podobne_obce_investice_podle_ucelu_2016-2025.csv

Investice a opravy za roky 2016–2025 sečtené podle účelu (sloučené paragrafy) pro HD, Pískovou Lhotu, Rebešovice a Závišice.

- Odkaz: [data/podobne_obce_investice_podle_ucelu_2016-2025.csv](https://hd-v-datech.cz/data/podobne_obce_investice_podle_ucelu_2016-2025.csv)
- Řádků: 48; jeden řádek = jedna obec × kategorie účelu
- Zdroj: Výpočet z výkazu FIN 2-12 M (Monitor státní pokladny MF).

| Sloupec | Význam |
|---|---|
| `obec` | Název obce. |
| `kategorie` | Účel (sloučené paragrafy; stejné členění jako `vydaje_kategorie_sousede_2010-2025.csv`). |
| `kc_2016_2025` | Investice (třída 6) + opravy (položka 5171) celkem za 2016–2025. Kč. |
| `kc_na_obyv_a_rok` | Totéž na obyvatele a rok (součet děleno součtem obyvatel k 1. 7.). Kč. |

## podobne_obce_obyvatel_rocne_2000-2025.csv

Počet obyvatel, věková struktura a pohyb obyvatel 2000–2025 (pohyb od roku 2002, dřívější roky ČSÚ po obcích nevydává) pro HD, Pískovou Lhotu, Rebešovice, Závišice a ČR (stejné sloupce jako `souhrn_obyvatel_rocne_2000-2025_sousede_okres_CR.csv`).

- Odkaz: [data/podobne_obce_obyvatel_rocne_2000-2025.csv](https://hd-v-datech.cz/data/podobne_obce_obyvatel_rocne_2000-2025.csv)
- Řádků: 129; jeden řádek = jedno území × rok
- Zdroj: Český statistický úřad (sloupec `zdroj` uvádí kód datové sady).
- Pozor: Pohyb obyvatel (narození … vystěhovalí) je u některých let a území prázdný.

Sloupce jsou stejné jako v `souhrn_obyvatel_rocne_2000-2025_sousede_okres_CR.csv`.

## podobne_obce_obyvatele_2000-2025.csv

Počet obyvatel HD, Pískové Lhoty, Rebešovic a Závišic 2000–2025.

- Odkaz: [data/podobne_obce_obyvatele_2000-2025.csv](https://hd-v-datech.cz/data/podobne_obce_obyvatele_2000-2025.csv)
- Řádků: 104; jeden řádek = jedna obec × rok
- Zdroj: ČSÚ, datová sada OBY01B01.

| Sloupec | Význam |
|---|---|
| `obec` | Název obce. |
| `rok` | Rok. |
| `obyvatel_31_12` | Obyvatelé k 31. 12. |

## podobne_obce_roztrisenost.csv

Ukazatele roztříštěnosti zástavby HD, Pískové Lhoty (PL), Rebešovic (REB) a Závišic (ZAV) (stejné sloupce jako `roztrisenost_sousede.csv`).

- Odkaz: [data/podobne_obce_roztrisenost.csv](https://hd-v-datech.cz/data/podobne_obce_roztrisenost.csv)
- Řádků: 4; jeden řádek = jedna obec
- Zdroj: Výpočet z polohy budov v RÚIAN (stav 30. 9. 2026).
- Pozor: „Shluk N m“ = skupina domů, kde každý dům má souseda ve skupině blíž než N metrů.

Sloupce jsou stejné jako v `roztrisenost_sousede.csv`.

## podobne_obce_souhrn_po_obdobich.csv

Součty ukazatelů za volební období pro HD, Pískovou Lhotu, Rebešovice a Závišice (stejné sloupce jako `souhrn_po_obdobich_sousede.csv`).

- Odkaz: [data/podobne_obce_souhrn_po_obdobich.csv](https://hd-v-datech.cz/data/podobne_obce_souhrn_po_obdobich.csv)
- Řádků: 256; jeden řádek = jedna obec × volební období × ukazatel
- Zdroj: Výpočet z `finance_*`.
- Pozor: Za období se počítají rozpočtové roky, za které odpovídá dané zastupitelstvo (sloupec `roky`); období 2022–2026 zatím jen 2023–2025.
- Pozor: Hodnoty sloupce `ukazatel` mají stejný význam jako stejnojmenné sloupce v souborech `finance_*_2010-2025.csv` (viz výše).

Sloupce jsou stejné jako v `souhrn_po_obdobich_sousede.csv`.

## podobne_obce_subjekty_ARES_pravni_forma.csv

Ekonomické subjekty se sídlem v obci podle právní formy (ARES). HD a podobné obce.

- Odkaz: [data/podobne_obce_subjekty_ARES_pravni_forma.csv](https://hd-v-datech.cz/data/podobne_obce_subjekty_ARES_pravni_forma.csv)
- Řádků: 46; jeden řádek = jedna obec × právní forma
- Zdroj: ARES (jako souhrn subjektů); názvy právních forem z číselníku ARES PravniForma.

| Sloupec | Význam |
|---|---|
| `kod_obce` | Kód obce podle ČSÚ (HD 512192). |
| `obec` | Název obce: Horní Domaslavice, Písková Lhota, Rebešovice nebo Závišice. |
| `pravni_forma_kod` | Kód právní formy. |
| `pravni_forma` | Název právní formy. |
| `pocet` | Počet subjektů. |
| `na_1000_obyv_2025` | Na 1 000 obyvatel (k 1. 7. 2025). |

## podobne_obce_subjekty_ARES_souhrn.csv

Ekonomické subjekty se sídlem v obci podle ARES, sloučené do skupin, i na 1 000 obyvatel. HD a podobné obce.

- Odkaz: [data/podobne_obce_subjekty_ARES_souhrn.csv](https://hd-v-datech.cz/data/podobne_obce_subjekty_ARES_souhrn.csv)
- Řádků: 4; jeden řádek = jedna obec
- Zdroj: ARES, vyhledání podle kódu obce sídla (POST /ekonomicke-subjekty-v-be/rest/ekonomicke-subjekty/vyhledat); HD, Pazderna, DD a Lučina stav k 30. 10. 2026, ostatní obce k 1. 11. 2026.
- Pozor: Počítá se sídlo, ne místo působení. Podnikající FO jsou v ARES i tehdy, když aktivně nepodnikají.

| Sloupec | Význam |
|---|---|
| `kod_obce` | Kód obce podle ČSÚ (HD 512192). |
| `obec` | Název obce: Horní Domaslavice, Písková Lhota, Rebešovice nebo Závišice. |
| `obyvatel_1_7_2025` | Obyvatelé k 1. 7. 2025 (ČSÚ), základ přepočtu. |
| `subjektu_celkem` | Subjekty celkem. |
| `na_1000` | Subjekty na 1 000 obyvatel. |
| `FO_podnikajici` | Podnikající fyzické osoby (právní formy 101, 102, 105, 107, 424). |
| `FO_na_1000` | Na 1 000 obyvatel. |
| `obchodni_spolecnosti` | Obchodní společnosti (111 v.o.s., 112 s.r.o., 121 a.s., 421 odštěpný závod). |
| `OS_na_1000` | Na 1 000 obyvatel. |
| `spolky_pobocne_ustavy` | Spolky, pobočné spolky, ústavy, nadace, nadační fondy a o.p.s. (706, 736, 161, 117, 118, 141). |
| `spolky_na_1000` | Na 1 000 obyvatel. |
| `ostatni` | Ostatní (obec, příspěvkové organizace, církevní osoby, SVJ, družstva aj.). |

## podobne_obce_transfery_NNO_2010-2025.csv

Transfery obcí neziskovým organizacím, církvím a fyzickým osobám po letech 2010–2025. HD a podobné obce.

- Odkaz: [data/podobne_obce_transfery_NNO_2010-2025.csv](https://hd-v-datech.cz/data/podobne_obce_transfery_NNO_2010-2025.csv)
- Řádků: 64; jeden řádek = jedna obec × rok
- Zdroj: Monitor státní pokladny MF, FIN 2-12 M za prosinec (skutečnost); obyvatelé ČSÚ k 1. 7.
- Pozor: Hlavní ukazatel webu je `NNO_bez_par_6171_52xx_62xx` (položky 5221 + 5222 + 5229 bez § 6171 a § 52xx, 62xx).
- Pozor: Výkaz neukazuje příjemce plateb.

| Sloupec | Význam |
|---|---|
| `kod_obce` | Kód obce podle ČSÚ (HD 512192). |
| `obec` | Název obce: Horní Domaslavice, Písková Lhota, Rebešovice nebo Závišice. |
| `rok` | Rozpočtový rok. |
| `obyvatel_1_7` | Obyvatelé k 1. 7. |
| `pol_5221` | Položka 5221 – obecně prospěšným společnostem. Kč. |
| `pol_5222` | Položka 5222 – spolkům. Kč. |
| `pol_5223` | Položka 5223 – církvím a náboženským společnostem. Kč. |
| `pol_5229` | Položka 5229 – ostatním neziskovým a podobným organizacím. Kč. |
| `pol_5492` | Položka 5492 – dary obyvatelstvu. Kč. |
| `pol_5493` | Položka 5493 – účelové neinvestiční transfery fyzickým osobám. Kč. |
| `pol_6322` | Položka 6322 – investiční transfery spolkům. Kč. |
| `neinv_NNO_5221_5222_5229` | Součet 5221 + 5222 + 5229 (neočištěno). Kč. |
| `na_obyvatele` | Předchozí sloupec na obyvatele. Kč. |
| `vcetne_cirkvi_5223` | Součet 5221 + 5222 + 5229 + 5223. Kč. |
| `vcetne_cirkvi_na_obyv` | Předchozí sloupec na obyvatele. Kč. |
| `NNO_bez_par_6171_52xx_62xx` | 5221 + 5222 + 5229 bez § 6171, § 52xx a § 62xx (očištěno). Kč. |
| `NNO_ocist_na_obyv` | Očištěný součet na obyvatele. Kč. |

## podobne_obce_transfery_NNO_paragrafy_2010-2025.csv

Rozpis transferů z `transfery_NNO_*` podle paragrafu a položky. HD a podobné obce.

- Odkaz: [data/podobne_obce_transfery_NNO_paragrafy_2010-2025.csv](https://hd-v-datech.cz/data/podobne_obce_transfery_NNO_paragrafy_2010-2025.csv)
- Řádků: 364; jeden řádek = jedna obec × rok × paragraf × položka
- Zdroj: Monitor státní pokladny MF, FIN 2-12 M.

| Sloupec | Význam |
|---|---|
| `kod_obce` | Kód obce podle ČSÚ (HD 512192). |
| `obec` | Název obce: Horní Domaslavice, Písková Lhota, Rebešovice nebo Závišice. |
| `rok` | Rozpočtový rok. |
| `paragraf` | Paragraf rozpočtové skladby. |
| `polozka` | Položka (5221, 5222, 5223, 5229, 5492, 5493, 6322). |
| `polozka_nazev` | Název položky. |
| `schvaleny` | Schválený rozpočet. Kč. |
| `upraveny` | Upravený rozpočet. Kč. |
| `skutecnost` | Skutečnost. Kč. |

## podobne_obce_ukazatele_rozvaha_vzz.csv

Rozvaha a výkaz zisku a ztráty HD, Pískové Lhoty, Rebešovic a Závišic (stejné sloupce jako `ukazatele_rozvaha_vzz_sousede.csv`).

- Odkaz: [data/podobne_obce_ukazatele_rozvaha_vzz.csv](https://hd-v-datech.cz/data/podobne_obce_ukazatele_rozvaha_vzz.csv)
- Řádků: 64; jeden řádek = jedna obec × rok (stav k 31. 12.)
- Zdroj: Monitor státní pokladny MF: rozvaha a výkaz zisku a ztráty.
- Pozor: Účetní hodnoty, ne tržní ceny. Stavby se účetně odepisují od roku 2012.

Sloupce jsou stejné jako v `ukazatele_rozvaha_vzz_sousede.csv`.

## podobne_obce_volby_komunalni_1994-2026.csv

Komunální volby 1994–2026 po obcích: voliči, účast, počet kandidátek a mandátů, rozdělení mandátů, typ kandidátek. HD a podobné obce.

- Odkaz: [data/podobne_obce_volby_komunalni_1994-2026.csv](https://hd-v-datech.cz/data/podobne_obce_volby_komunalni_1994-2026.csv)
- Řádků: 36; jeden řádek = jedna obec × volby
- Zdroj: volby.cz: výsledky za obec (kv1111) a seznamy zvolených (kv21111) 1994–2022, datové soubory kv2026 (vygenerováno 11. 10. 2026).
- Pozor: Typ kandidátky je odvozený z navrhující strany zvolených kandidátů, u kandidátek bez mandátu a u roku 1994 z názvu.
- Pozor: Pro rok 1994 volby.cz jména zvolených neuvádí, sloupce o zvolených jsou proto 0.

| Sloupec | Význam |
|---|---|
| `kod_obce` | Kód obce podle ČSÚ (HD 512192). |
| `obec` | Název obce: Horní Domaslavice, Písková Lhota, Rebešovice nebo Závišice. |
| `rok` | Rok voleb. |
| `pocet_clenu_zo` | Počet členů zastupitelstva (mandátů). |
| `volici` | Voliči v seznamu. |
| `vydane_obalky` | Vydané úřední obálky. |
| `ucast_pct` | Volební účast, %. |
| `platne_hlasy` | Platné hlasy (v komunálních volbách má volič tolik hlasů, kolik je mandátů). |
| `pocet_kandidatek` | Počet kandidátních listin. |
| `pocet_kandidatu` | Počet kandidátů na všech kandidátkách. |
| `kandidatek_s_mandatem` | Počet kandidátek, které získaly aspoň jeden mandát. |
| `rozdeleni_mandatu` | Mandáty jednotlivých kandidátek seřazené sestupně (např. „3 : 3 : 3 : 3 : 1“). |
| `nejsilnejsi_kandidatka_pct` | Podíl hlasů nejsilnější kandidátky, %. |
| `kandidatek_typu_NK_SNK` | Počet kandidátek zařazených jako nezávislí kandidáti nebo jejich sdružení. |
| `mandatu_kandidatkam_NK_SNK` | Mandáty, které získaly kandidátky NK/SNK. |
| `zvolenych_celkem` | Počet zvolených podle seznamu zvolených. |
| `zvolenych_navrh_NK` | Zvolení, které navrhla „NK“ (bez navrhující strany). |
| `zvolenych_BEZPP` | Zvolení bez politické příslušnosti. |

## podobne_obce_volby_komunalni_kandidatky_1994-2026.csv

Kandidátky v komunálních volbách 1994–2026: hlasy, mandáty a odvozený typ kandidátky. HD a podobné obce.

- Odkaz: [data/podobne_obce_volby_komunalni_kandidatky_1994-2026.csv](https://hd-v-datech.cz/data/podobne_obce_volby_komunalni_kandidatky_1994-2026.csv)
- Řádků: 124; jeden řádek = jedna obec × volby × kandidátka
- Zdroj: volby.cz (jako u souhrnu komunálních voleb).
- Pozor: Kandidátky pojmenované jménem jednotlivého kandidáta jsou nahrazeny textem „kandidátka jednotlivce (NK)“; web neuvádí jména fyzických osob.

| Sloupec | Význam |
|---|---|
| `kod_obce` | Kód obce podle ČSÚ (HD 512192). |
| `obec` | Název obce: Horní Domaslavice, Písková Lhota, Rebešovice nebo Závišice. |
| `rok` | Rok voleb. |
| `cislo` | Číslo kandidátky (volební strany) podle volby.cz. |
| `kandidatka` | Název kandidátky (zkrácený tak, jak ho uvádí volby.cz). |
| `hlasy` | Hlasy pro kandidátku. |
| `hlasy_pct` | Podíl hlasů, %. |
| `pocet_kandidatu` | Počet kandidátů na kandidátce. |
| `mandaty` | Získané mandáty. |
| `typ_kandidatky` | Odvozený typ: NK/SNK, strana/hnutí/koalice, strana/hnutí + NK; „(podle názvu)“ = odvozeno jen z názvu. |
| `kandidatu_navrh_NK_2026` | Jen 2026: počet kandidátů navržených jako NK. |
| `kandidatu_celkem_2026` | Jen 2026: počet kandidátů na kandidátce podle jmenného seznamu. |

## podobne_obce_volby_komunalni_kontinuita_2002-2026.csv

Kolik zastupitelů zvolených v daném roce bylo zvoleno už v předchozích volbách (bez jmen). HD a podobné obce.

- Odkaz: [data/podobne_obce_volby_komunalni_kontinuita_2002-2026.csv](https://hd-v-datech.cz/data/podobne_obce_volby_komunalni_kontinuita_2002-2026.csv)
- Řádků: 28; jeden řádek = jedna obec × volby (od roku 2002)
- Zdroj: Výpočet ze seznamů zvolených na volby.cz; porovnává se příjmení a jméno bez titulů.
- Pozor: Změny příjmení se nezjišťovaly (u HD je známý jeden případ v roce 2026, není započten).
- Pozor: Ve Vojkovicích byli v letech 2018 a 2022 zvoleni dva lidé se stejným jménem; rozlišeni jsou podle věku.

| Sloupec | Význam |
|---|---|
| `kod_obce` | Kód obce podle ČSÚ (HD 512192). |
| `obec` | Název obce: Horní Domaslavice, Písková Lhota, Rebešovice nebo Závišice. |
| `rok` | Rok voleb. |
| `zvolenych_se_jmenem` | Počet zvolených. |
| `zvoleni_i_v_minulych_volbach` | Z nich zvolení i v bezprostředně předchozích volbách. |
| `pct_z_minulych` | Podíl znovuzvolených z předchozích voleb, %. |
| `zvoleni_kdykoli_drive_od_1998` | Z nich zvolení v kterýchkoli dřívějších volbách od roku 1998. |
| `pct_kdykoli_drive` | Podíl zvolených kdykoli dříve, %. |

## podobne_obce_volby_prezidentska_2023.csv

Prezidentská volba 2023: účast v obou kolech a výsledek 2. kola (bez jmen kandidátů). HD, podobné obce a ČR.

- Odkaz: [data/podobne_obce_volby_prezidentska_2023.csv](https://hd-v-datech.cz/data/podobne_obce_volby_prezidentska_2023.csv)
- Řádků: 10; jeden řádek = jedno území × kolo
- Zdroj: volby.cz, pls/prez2023 (pe311, pe2).

| Sloupec | Význam |
|---|---|
| `kod` | Kód území: kód obce ČSÚ, 8102 = okres Frýdek-Místek, CZ = Česká republika. |
| `uzemi` | Název území (obec, okres nebo Česká republika). |
| `kolo` | 1. nebo 2. kolo. |
| `volici` | Voliči v seznamu. |
| `vydane_obalky` | Vydané obálky. |
| `ucast_pct` | Volební účast, %. |
| `platne_hlasy` | Platné hlasy. |
| `k2_zvoleny_prezident_hlasy` | Jen 2. kolo: hlasy pro kandidáta zvoleného prezidentem. |
| `k2_zvoleny_prezident_pct` | Jen 2. kolo: jeho podíl, %. |
| `k2_protikandidat_hlasy` | Jen 2. kolo: hlasy pro protikandidáta. |
| `k2_protikandidat_pct` | Jen 2. kolo: jeho podíl, %. |

## podobne_obce_volby_snemovni_strany_2013-2025.csv

Výsledky stran ve volbách do Poslanecké sněmovny 2013–2025. HD a podobné obce.

- Odkaz: [data/podobne_obce_volby_snemovni_strany_2013-2025.csv](https://hd-v-datech.cz/data/podobne_obce_volby_snemovni_strany_2013-2025.csv)
- Řádků: 445; jeden řádek = jedno území × volby × strana
- Zdroj: volby.cz, appdata ps{rok}.

| Sloupec | Význam |
|---|---|
| `kod` | Kód území: kód obce ČSÚ, 8102 = okres Frýdek-Místek, CZ = Česká republika. |
| `uzemi` | Název území (obec, okres nebo Česká republika). |
| `rok` | Rok voleb. |
| `cislo` | Číslo strany v daných volbách. |
| `strana` | Název strany (zkrácený podle volby.cz). |
| `hlasy` | Hlasy. |
| `pct` | Podíl platných hlasů, %. |

## podobne_obce_volby_snemovni_ucast_2013-2025.csv

Účast ve volbách do Poslanecké sněmovny 2013–2025. HD a podobné obce.

- Odkaz: [data/podobne_obce_volby_snemovni_ucast_2013-2025.csv](https://hd-v-datech.cz/data/podobne_obce_volby_snemovni_ucast_2013-2025.csv)
- Řádků: 20; jeden řádek = jedno území × volby
- Zdroj: volby.cz, appdata ps{rok}: výsledky za obec, okres a ČR.

| Sloupec | Význam |
|---|---|
| `kod` | Kód území: kód obce ČSÚ, 8102 = okres Frýdek-Místek, CZ = Česká republika. |
| `uzemi` | Název území (obec, okres nebo Česká republika). |
| `rok` | Rok voleb. |
| `volici` | Voliči v seznamu. |
| `vydane_obalky` | Vydané obálky. |
| `ucast_pct` | Volební účast, %. |
| `platne_hlasy` | Platné hlasy. |

## podobne_obce_vyber.csv

Podklady k výběru podobných obcí: 231 obcí ČR s 650–1 800 obyvateli (2025), růstem od roku 2000 alespoň 35 % a rozlohou 3–11 km², a pro srovnání HD. Pro 93 z nich, které splňují užší filtr výběru (750–1 600 obyvatel, růst alespoň 55 %, rozloha 3–8,5 km²), je uvedeno i skóre a pořadí, podle kterého se vybíraly tři podobné obce.

- Odkaz: [data/podobne_obce_vyber.csv](https://hd-v-datech.cz/data/podobne_obce_vyber.csv)
- Řádků: 232; jeden řádek = jedna obec; seřazeno podle indexu odlišnosti zástavby (sloupec poradi), ne podle pořadí výběru
- Zdroj: ČSÚ (obyvatelé), ČÚZK (úhrnné hodnoty druhů pozemků k 1. 1. 2026), RÚIAN (budovy, stav 30. 9. 2026). Výpočet autora webu.
- Pozor: Tři podobné obce se vybíraly podle skóre výběru (sloupce skore_vyberu a poradi_vyberu), ne podle indexu odlišnosti. Písková Lhota je v pořadí výběru 1., Rebešovice 11. a Závišice 19.; obce v zázemí Prahy a několik dalších obcí s podobným skóre byly při výběru přeskočeny ručně.
- Pozor: Index odlišnosti je výpočet autora webu podle šesti ukazatelů (obyvatelé, růst, rozloha, největší část obce, vzdálenost od středu, propojení na dům); slouží k posouzení, jak běžná je zástavba podobná HD. Jiné váhy by daly jiné pořadí.
- Pozor: Napojení na kanalizaci a plyn je z RÚIAN, údaje jsou neúplné.

| Sloupec | Význam |
|---|---|
| `poradi` | Pořadí podle indexu odlišnosti (0 = HD). |
| `kod_obce` | Kód obce ČSÚ. |
| `obec` | Název obce. |
| `okres` | Okres. |
| `obyvatel_2000` | Obyvatelé k 31. 12. 2000. |
| `obyvatel_2025` | Obyvatelé k 31. 12. 2025. |
| `rust_2000_2025_pct` | Růst počtu obyvatel 2000–2025, %. |
| `rozloha_km2` | Rozloha obce, km². |
| `hustota_obyv_km2` | Obyvatelé na km² (2025). |
| `orna_pct` | Podíl orné půdy na rozloze, %. |
| `les_pct` | Podíl lesa na rozloze, %. |
| `domy_bydleni` | Počet budov pro bydlení podle RÚIAN. |
| `podil_nejvetsi_casti_150m_pct` | Podíl domů v největší souvislé části obce (domy do 150 m od sebe), %. |
| `casti_150m_min5domu` | Počet takových částí s alespoň 5 domy. |
| `vzd_od_stredu_median_m` | Medián vzdálenosti domu od středu zástavby, m. |
| `mst_m_na_dum` | Délka nejkratšího propojení všech domů na jeden dům, m. |
| `kanalizace_verejna_pct` | Podíl domů se zjištěným údajem, které jsou napojené na veřejnou kanalizaci, %. |
| `plyn_pct` | Podíl domů se zjištěným údajem napojených na plyn z veřejné sítě, %. |
| `domy_po_2000_pct` | Podíl domů dokončených po roce 2000, %. |
| `katastralni_uzemi` | Počet katastrálních území obce. |
| `index_odlisnosti_od_HD` | Index odlišnosti od HD (0 = HD; čím menší, tím podobnější). Odmocnina součtu čtverců: ln poměru obyvatel / 0,3, ln poměru (100 + růst %) / 0,2, ln poměru rozlohy / 0,35, rozdíl podílu největší části / 15 p. b., ln poměru vzdálenosti od středu / 0,35 a ln poměru propojení na dům / 0,3. |
| `skore_vyberu` | Skóre výběru podobných obcí (0 = HD; čím menší, tím podobnější). Odmocnina součtu čtverců: ln poměru obyvatel 2025 / 0,25, ln poměru (100 + růst %) / 0,15, ln poměru rozlohy / 0,3, rozdíl podílu orné půdy / 20 p. b. a rozdíl podílu lesa / 15 p. b. Zástavbu nezohledňuje. |
| `poradi_vyberu` | Pořadí podle skóre výběru mezi 93 obcemi, které splňují filtr výběru (750–1 600 obyvatel v roce 2025, růst od roku 2000 alespoň 55 %, rozloha 3–8,5 km²); prázdné u obcí, které filtr nesplňují. |

## podobne_obce_vydaje_kategorie_2010-2025.csv

Výdaje HD, Pískové Lhoty, Rebešovic a Závišic podle účelu a druhu (stejné sloupce jako `vydaje_kategorie_sousede_2010-2025.csv`).

- Odkaz: [data/podobne_obce_vydaje_kategorie_2010-2025.csv](https://hd-v-datech.cz/data/podobne_obce_vydaje_kategorie_2010-2025.csv)
- Řádků: 1408; jeden řádek = jedna obec × rok × členění × kategorie
- Zdroj: Monitor státní pokladny MF, FIN 2-12 M.
- Pozor: Obě členění (`ucel`, `druh`) dávají v součtu stejné celkové výdaje; nesčítat je dohromady.

Sloupce jsou stejné jako v `vydaje_kategorie_sousede_2010-2025.csv`.

## rozpocet_2026_investice_opravy.csv

Rozpočet 2026: plánované a zaplacené investice a opravy podle paragrafu.

- Odkaz: [data/rozpocet_2026_investice_opravy.csv](https://hd-v-datech.cz/data/rozpocet_2026_investice_opravy.csv)
- Řádků: 15; jeden řádek = jeden paragraf
- Zdroj: Monitor státní pokladny MF, FIN 2-12 M za září 2026.

| Sloupec | Význam |
|---|---|
| `paragraf` | Paragraf rozpočtové skladby. |
| `investice_schvaleny_kc` | Investice (třída 6), schválený rozpočet. Kč. |
| `investice_upraveny_kc` | Investice, upravený rozpočet. Kč. |
| `investice_skutecnost_9_2026_kc` | Investice, skutečnost k 30. 9. 2026. Kč. |
| `opravy_5171_schvaleny_kc` | Opravy (položka 5171), schválený rozpočet. Kč. |
| `opravy_5171_upraveny_kc` | Opravy, upravený rozpočet. Kč. |
| `opravy_5171_skutecnost_9_2026_kc` | Opravy, skutečnost k 30. 9. 2026. Kč. |

## rozpocet_2026_odhad_prijmu.csv

Rozpočtované a skutečné příjmy 2023–2026 a jaký podíl ročních příjmů obvykle přichází do konce září.

- Odkaz: [data/rozpocet_2026_odhad_prijmu.csv](https://hd-v-datech.cz/data/rozpocet_2026_odhad_prijmu.csv)
- Řádků: 24; jeden řádek = jeden rok × druh příjmu
- Zdroj: Monitor státní pokladny MF.

| Sloupec | Význam |
|---|---|
| `rok` | Rok. |
| `ukazatel` | Druh příjmu. |
| `schvaleny_kc` | Schválený rozpočet. Kč. |
| `upraveny_kc` | Upravený rozpočet ke konci roku. Kč. |
| `skutecnost_kc` | Skutečnost za celý rok (u 2026 prázdné). Kč. |
| `skutecnost_k_30_9_kc` | Skutečnost k 30. 9. Kč. |
| `podil_k_30_9_z_celeho_roku_pct` | Kolik % ročních příjmů přišlo do 30. 9. |
| `skutecnost_vs_schvaleny_pct` | Skutečnost / schválený rozpočet, %. |

## rozpocet_2026_rozpoctova_opatreni.csv

Rozpočtová opatření (změny rozpočtu) 2026.

- Odkaz: [data/rozpocet_2026_rozpoctova_opatreni.csv](https://hd-v-datech.cz/data/rozpocet_2026_rozpoctova_opatreni.csv)
- Řádků: 8; jeden řádek = jedno rozpočtové opatření nebo jeho část
- Zdroj: Rozpočtová opatření a zápisy zveřejněné obcí (sloupec `zdroj`).

| Sloupec | Význam |
|---|---|
| `cislo` | Číslo rozpočtového opatření v roce. |
| `datum` | Datum (RRRR-MM-DD). |
| `paragraf` | Dotčený paragraf (případně / položka). |
| `popis` | Účel změny. |
| `zmena_vydaju_kc` | Změna celkových výdajů. Kč. |
| `zmena_prijmu_a_financovani_kc` | Změna příjmů a financování. Kč. |
| `zmena_rezervy_3639_kc` | Změna rezervy § 3639 (záporné = peníze z rezervy přesunuty na uvedený účel). Kč. |
| `zdroj` | Dokument, ze kterého údaj pochází. |

## rozpocet_2026_srovnani_k_30_9.csv

Rozpočet 2026: plnění příjmů a čerpání výdajů k 30. 9. proti stejnému období 2023–2025.

- Odkaz: [data/rozpocet_2026_srovnani_k_30_9.csv](https://hd-v-datech.cz/data/rozpocet_2026_srovnani_k_30_9.csv)
- Řádků: 44; jeden řádek = jeden ukazatel × rok
- Zdroj: Monitor státní pokladny MF, FIN 2-12 M za září.

| Sloupec | Význam |
|---|---|
| `ukazatel` | Ukazatel (příjmy, výdaje, investice…), vymezení v názvu. |
| `rok` | Rok. |
| `schvaleny_kc` | Schválený rozpočet. Kč. |
| `upraveny_kc` | Upravený rozpočet k 30. 9. Kč. |
| `skutecnost_k_30_9_kc` | Skutečnost k 30. 9. Kč. |
| `plneni_upraveneho_pct` | Skutečnost k 30. 9. / upravený rozpočet, %. |
| `skutecnost_cely_rok_kc` | Skutečnost za celý rok (u 2026 prázdné). Kč. |

## rozpocet_2026_stav_uctu.csv

Peníze na účtech obce Horní Domaslavice po čtvrtletích 2023–2026.

- Odkaz: [data/rozpocet_2026_stav_uctu.csv](https://hd-v-datech.cz/data/rozpocet_2026_stav_uctu.csv)
- Řádků: 9; jeden řádek = jedno datum (konec čtvrtletí)
- Zdroj: Rozvaha obce, Monitor státní pokladny MF.

| Sloupec | Význam |
|---|---|
| `datum` | Datum stavu (RRRR-MM-DD). |
| `bezny_ucet_231_kc` | Základní běžný účet (231). Kč. |
| `terminovany_vklad_244_kc` | Termínované vklady (244). Kč. |
| `celkem_kc` | Celkem. Kč. |
| `zdroj` | Výkaz, ze kterého údaj pochází. |

## rozpocet_2026_strednedoby_vyhled.csv

Střednědobý výhled rozpočtu obce Horní Domaslavice na roky 2025–2028.

- Odkaz: [data/rozpocet_2026_strednedoby_vyhled.csv](https://hd-v-datech.cz/data/rozpocet_2026_strednedoby_vyhled.csv)
- Řádků: 20; jeden řádek = jeden ukazatel; sloupce jsou roky
- Zdroj: Střednědobý výhled rozpočtu zveřejněný obcí.
- Pozor: Výhled je plán obce, ne skutečnost.

| Sloupec | Význam |
|---|---|
| `ukazatel` | Ukazatel výhledu. |
| `2025_kc` | Rok 2025. Kč. |
| `2026_kc` | Rok 2026. Kč. |
| `2027_kc` | Rok 2027. Kč. |
| `2028_kc` | Rok 2028. Kč. |

## rozpocet_2026_vydaje_podle_ucelu.csv

Rozpočet 2026: výdaje podle účelu – schváleno, upraveno, skutečnost k 30. 9. a srovnání s minulými lety.

- Odkaz: [data/rozpocet_2026_vydaje_podle_ucelu.csv](https://hd-v-datech.cz/data/rozpocet_2026_vydaje_podle_ucelu.csv)
- Řádků: 16; jeden řádek = jedna kategorie výdajů (poslední řádek CELKEM)
- Zdroj: Monitor státní pokladny MF, FIN 2-12 M.

| Sloupec | Význam |
|---|---|
| `kategorie` | Účel výdajů (sloučené paragrafy). |
| `schvaleny_2026_kc` | Schválený rozpočet 2026. Kč. |
| `upraveny_2026_kc` | Upravený rozpočet 2026 k 30. 9. Kč. |
| `skutecnost_9_2026_kc` | Skutečnost k 30. 9. 2026. Kč. |
| `cerpani_upraveneho_pct` | Čerpání upraveného rozpočtu, %. |
| `skutecnost_9_2025_kc` | Skutečnost k 30. 9. 2025. Kč. |
| `skutecnost_9_2024_kc` | Skutečnost k 30. 9. 2024. Kč. |
| `skutecnost_9_2023_kc` | Skutečnost k 30. 9. 2023. Kč. |
| `skutecnost_cely_rok_2025_kc` | Skutečnost za celý rok 2025. Kč. |

## roztrisenost_sousede.csv

Ukazatele roztříštěnosti zástavby: jak daleko od sebe a od středu obce jsou domy a kolik tvoří skupin.

- Odkaz: [data/roztrisenost_sousede.csv](https://hd-v-datech.cz/data/roztrisenost_sousede.csv)
- Řádků: 5; jeden řádek = jedna obec
- Zdroj: Výpočet z polohy budov v RÚIAN (stav 30. 9. 2026).
- Pozor: „Shluk N m“ = skupina domů, kde každý dům má souseda ve skupině blíž než N metrů.

| Sloupec | Význam |
|---|---|
| `obec` | Zkratka obce: HD, PA (Pazderna), DD, LU (Lučina), VOJ (Vojkovice); v souboru podobných obcí PL (Písková Lhota), REB (Rebešovice), ZAV (Závišice). |
| `domy_bydleni` | Počet budov pro bydlení. |
| `rekreacni_objekty` | Počet rekreačních objektů (do výpočtu nezahrnuty). |
| `mst_m_na_dum` | Délka nejkratší sítě spojující všechny domy (minimální kostra) na jeden dům, m. Hrubý odhad délky sítí na dům. |
| `mst_km` | Délka minimální kostry celkem, km. |
| `nn_median_m` | Medián vzdálenosti k nejbližšímu sousednímu domu, m. |
| `nn_prumer_m` | Průměr vzdálenosti k nejbližšímu sousedovi, m. |
| `domy_nn_nad_100m` | Počet domů, jejichž nejbližší soused je dál než 100 m. |
| `vzd_od_stredu_median_m` | Medián vzdálenosti domu od středu zástavby (medián souřadnic domů, ne náves ani úřad), m. |
| `vzd_od_stredu_p90_m` | 90. percentil vzdálenosti od středu zástavby, m. |
| `plocha_obalky_50m_ha` | Plocha území do 50 m od domů, ha. |
| `domy_na_ha_obalky` | Domy na hektar této plochy (hustota). |
| `shluky_75m` | Počet shluků při vzdálenosti 75 m (včetně samot). |
| `shluky_75m_min5domu` | Počet shluků s alespoň 5 domy. |
| `podil_nejvetsi_75m_pct` | Podíl domů v největším shluku, %. |
| `samoty_75m` | Počet samot (dům bez souseda do 75 m). |
| `nejvetsi_shluky_75m` | Velikosti největších shluků oddělené mezerou. |
| `shluky_100m` | Totéž pro 100 m. |
| `shluky_100m_min5domu` | Totéž pro 100 m. |
| `podil_nejvetsi_100m_pct` | Totéž pro 100 m. |
| `samoty_100m` | Totéž pro 100 m. |
| `nejvetsi_shluky_100m` | Totéž pro 100 m. |
| `shluky_150m` | Totéž pro 150 m. |
| `shluky_150m_min5domu` | Totéž pro 150 m. |
| `podil_nejvetsi_150m_pct` | Totéž pro 150 m. |
| `samoty_150m` | Totéž pro 150 m. |
| `nejvetsi_shluky_150m` | Totéž pro 150 m. |

## skolstvi_socialni_exekuce_2026-10.csv

Osoby v exekuci podle Exekutorské komory: HD, sousední obce (Pazderna, Dolní Domaslavice, Lučina, Vojkovice) a podobné obce (Písková Lhota, Rebešovice, Závišice), jejich okresy, kraje a ČR.

- Odkaz: [data/skolstvi_socialni_exekuce_2026-10.csv](https://hd-v-datech.cz/data/skolstvi_socialni_exekuce_2026-10.csv)
- Řádků: 16; jeden řádek = jedno území (obec, okres, kraj, ČR)
- Zdroj: Exekutorská komora ČR, mapa exekucí (obce.json, stav k 1. 10. 2026); obyvatelé 15+ ČSÚ.
- Pozor: Podíl je počítán dvakrát: ze sčítání 2021 a z počtu obyvatel 15+ k 31. 12. 2024.

| Sloupec | Význam |
|---|---|
| `kod_obce` | Kód obce, okresu nebo kraje. |
| `uzemi` | Název území. |
| `okres` | Okres. |
| `kraj` | Kraj. |
| `osoby_v_exekuci` | Počet osob v exekuci. |
| `pocet_exekuci` | Počet exekucí. |
| `exekuci_na_osobu` | Průměrný počet exekucí na osobu. |
| `obyv_15plus_SLDB2021` | Obyvatelé 15+ podle sčítání 2021. |
| `podil_SLDB2021_procent` | Podíl osob v exekuci na obyvatelích 15+ (sčítání 2021), %. |
| `obyv_15plus_2024_12_31` | Obyvatelé 15+ k 31. 12. 2024. |
| `podil_2024_procent` | Podíl osob v exekuci na obyvatelích 15+ (2024), %. |
| `stav_k` | Datum stavu dat Exekutorské komory. |

## skolstvi_socialni_kriminalita_2013-2026.csv

Trestné činy, přestupky a dopravní nehody podle mapy kriminality Policie ČR: HD, sousední obce (Pazderna, Dolní Domaslavice, Lučina, Vojkovice) a podobné obce (Písková Lhota, Rebešovice, Závišice).

- Odkaz: [data/skolstvi_socialni_kriminalita_2013-2026.csv](https://hd-v-datech.cz/data/skolstvi_socialni_kriminalita_2013-2026.csv)
- Řádků: 112; jeden řádek = jedna obec × rok
- Zdroj: Policie ČR, mapa kriminality (API), 2013–2026; obyvatelé ČSÚ.
- Pozor: Rok 2026 je neúplný (sloupec posledni_datum). Policie zveřejňuje jen vybrané druhy trestných činů. Na malých obcích jeden pachatel výrazně mění čísla.

| Sloupec | Význam |
|---|---|
| `kod_obce` | Kód obce ČSÚ. |
| `obec` | Obec. |
| `rok` | Rok. |
| `obyvatele_31_12` | Obyvatelé k 31. 12. |
| `delikty_celkem` | Delikty celkem (trestné činy, přestupky, nehody). |
| `prestupky` | Přestupky. |
| `trestne_ciny_zverejnovane` | Trestné činy (zveřejňované druhy). |
| `dopravni_nehody` | Dopravní nehody. |
| `delikty_na_1000` | Delikty na 1 000 obyvatel. |
| `tc_na_1000` | Trestné činy na 1 000 obyvatel. |
| `prestupky_BESIP` | Dopravní přestupky (BESIP). |
| `prestupky_rychlost` | Z toho překročení rychlosti. |
| `posledni_datum` | Poslední datum v datech za daný rok. |

## skolstvi_socialni_nezamestnanost_MPSV_rocni.csv

Podíl nezaměstnaných osob (PNO) podle MPSV, roční průměry: HD, sousední obce (Pazderna, Dolní Domaslavice, Lučina, Vojkovice) a podobné obce (Písková Lhota, Rebešovice, Závišice), okresy a ČR.

- Odkaz: [data/skolstvi_socialni_nezamestnanost_MPSV_rocni.csv](https://hd-v-datech.cz/data/skolstvi_socialni_nezamestnanost_MPSV_rocni.csv)
- Řádků: 26; jeden řádek = jedno území × rok
- Zdroj: MPSV, otevřená data evidence uchazečů (evid_pno_adresa_agr_frz_odata), data do 9/2026.
- Pozor: Rok 2026 je průměr jen za dostupné měsíce (sloupec pocet_mesicu). U malých obcí kolísá podíl i o jednotlivce.

| Sloupec | Význam |
|---|---|
| `uzemi` | Obec, okres nebo ČR. |
| `rok` | Rok. |
| `pocet_mesicu` | Počet měsíců v průměru. |
| `pno_prumer_procent` | Průměrný podíl nezaměstnaných osob (dosažitelní uchazeči 15–64 / obyvatelé 15–64), %. |
| `dosazitelni_min` | Nejnižší měsíční počet dosažitelných uchazečů. |
| `dosazitelni_max` | Nejvyšší měsíční počet dosažitelných uchazečů. |
| `posledni_mesic` | Poslední měsíc v datech. |
| `pno_posledni_mesic` | PNO v posledním měsíci, %. |
| `dosazitelni_posledni` | Dosažitelní uchazeči v posledním měsíci. |
| `obyv_15_64_posledni` | Obyvatelé 15–64 použití pro poslední měsíc. |

## skolstvi_socialni_ovzdusi_CHMU.csv

Pětileté průměry znečištění ovzduší (benzo(a)pyren, PM10, PM2,5, NO2) v čtvercích 1 × 1 km: HD, sousední obce (Pazderna, Dolní Domaslavice, Lučina, Vojkovice) a podobné obce (Písková Lhota, Rebešovice, Závišice).

- Odkaz: [data/skolstvi_socialni_ovzdusi_CHMU.csv](https://hd-v-datech.cz/data/skolstvi_socialni_ovzdusi_CHMU.csv)
- Řádků: 240; jeden řádek = jedna obec × období × ukazatel
- Zdroj: ČHMÚ, pětileté průměrné koncentrace ve čtvercové síti 1 km (sit1000_5lprum); hranice obcí RÚIAN/MSK.
- Pozor: Jde o modelové hodnoty pro čtverce 1 km, ne o měření v obci. Limit benzo(a)pyrenu je 1 ng/m³.

| Sloupec | Význam |
|---|---|
| `kod_obce` | Kód obce ČSÚ. |
| `obec` | Obec. |
| `obdobi` | Pětileté období. |
| `ukazatel` | Znečišťující látka a ukazatel. |
| `vazeny_prumer` | Průměr čtverců vážený plochou v obci. |
| `min_ctverec` | Nejnižší hodnota čtverce. |
| `max_ctverec` | Nejvyšší hodnota čtverce. |
| `pocet_ctvercu` | Počet čtverců zasahujících do obce. |
| `plocha_km2_v_obci` | Plocha průniku čtverců s obcí, km². |
| `pole_v_datech` | Název pole v datech ČHMÚ. |
| `hranice_obce` | Zdroj hranice obce. |

## skolstvi_socialni_skoly_rejstrik_2026-11.csv

Školy a školská zařízení v obcích podle rejstříku škol MŠMT: HD, sousední obce (Pazderna, Dolní Domaslavice, Lučina, Vojkovice) a podobné obce (Písková Lhota, Rebešovice, Závišice) (a ZŠ a MŠ Dobratice, kam patří MŠ ve Vojkovicích).

- Odkaz: [data/skolstvi_socialni_skoly_rejstrik_2026-11.csv](https://hd-v-datech.cz/data/skolstvi_socialni_skoly_rejstrik_2026-11.csv)
- Řádků: 28; jeden řádek = jedna součást školy (MŠ, ZŠ, družina, jídelna…)
- Zdroj: MŠMT, rejstřík škol a školských zařízení (krajské výstupy JSON-LD, stav k 1. 11. 2026).

| Sloupec | Význam |
|---|---|
| `obec` | Obec. |
| `red_izo` | Identifikátor ředitelství školy (RED_IZO). |
| `ico` | IČO právnické osoby. |
| `pravnicka_osoba` | Název školy (právnické osoby). |
| `zrizovatel` | Zřizovatel. |
| `izo` | Identifikátor součásti (IZO). |
| `soucast` | Druh součásti (MŠ, ZŠ, ŠD, ŠJ…). |
| `druh_kod` | Kód druhu podle rejstříku. |
| `kapacita` | Kapacita. |
| `jednotka` | Jednotka kapacity (děti, žáci, stravovaní…). |
| `mista_vyuky` | Místa poskytování vzdělávání. |
| `datum_vystupu` | Datum výstupu rejstříku. |
| `zdroj` | Soubor rejstříku. |

## skolstvi_socialni_zdravotni_socialni_sluzby.csv

Zdravotní a sociální služby s místem poskytování v obci: HD, sousední obce (Pazderna, Dolní Domaslavice, Lučina, Vojkovice) a podobné obce (Písková Lhota, Rebešovice, Závišice).

- Odkaz: [data/skolstvi_socialni_zdravotni_socialni_sluzby.csv](https://hd-v-datech.cz/data/skolstvi_socialni_zdravotni_socialni_sluzby.csv)
- Řádků: 12; jeden řádek = jedno místo poskytování nebo souhrnný řádek obce
- Zdroj: Národní registr poskytovatelů zdravotních služeb (NRPZS) a registr poskytovatelů sociálních služeb MPSV, stav 1. 11. 2026.
- Pozor: Poskytovatelé, kteří jsou fyzickými osobami, jsou uvedeni jen jako „fyzická osoba“.

| Sloupec | Význam |
|---|---|
| `obec` | Obec. |
| `registr` | Registr (NRPZS, RPSS). |
| `druh` | Druh péče nebo služby. |
| `zarizeni_nebo_poskytovatel` | Zařízení nebo poskytovatel (bez jmen fyzických osob). |
| `misto_poskytovani` | Místo poskytování. |
| `od` | Od kdy (podle registru). |
| `poznamka` | Poznámka. |

## souhrn_obyvatel_rocne_2000-2025_sousede_okres_CR.csv

Počet obyvatel, věková struktura a pohyb obyvatel 2000–2025 (pohyb od roku 2002, dřívější roky ČSÚ po obcích nevydává) pro HD, sousední obce, okres Frýdek-Místek a Českou republiku.

- Odkaz: [data/souhrn_obyvatel_rocne_2000-2025_sousede_okres_CR.csv](https://hd-v-datech.cz/data/souhrn_obyvatel_rocne_2000-2025_sousede_okres_CR.csv)
- Řádků: 232; jeden řádek = jedno území × rok
- Zdroj: Český statistický úřad (sloupec `zdroj` uvádí kód datové sady).
- Pozor: Pohyb obyvatel (narození … vystěhovalí) je u některých let a území prázdný.

| Sloupec | Význam |
|---|---|
| `uzemi` | HD, Pazderna, DD, Lucina, Vojkovice, Nosovice (Nošovice), DTosanovice (Dolní Tošanovice), okres (Frýdek-Místek), CR (Česká republika). |
| `rok` | Rok. |
| `obyvatel_31_12` | Obyvatelé k 31. 12. |
| `vek_0_14` | Obyvatelé ve věku 0–14 let. |
| `vek_15_64` | Obyvatelé ve věku 15–64 let. |
| `vek_65plus` | Obyvatelé ve věku 65 a více let. |
| `index_stari` | Index stáří = počet 65+ na 100 dětí 0–14. |
| `narozeni` | Živě narození za rok. |
| `zemreli` | Zemřelí za rok. |
| `pristehovali` | Přistěhovalí za rok. |
| `vystehovali` | Vystěhovalí za rok. |
| `zdroj` | Datová sada ČSÚ. |

## souhrn_po_obdobich_sousede.csv

Součty ukazatelů za volební období a průměr na obyvatele a rok.

- Odkaz: [data/souhrn_po_obdobich_sousede.csv](https://hd-v-datech.cz/data/souhrn_po_obdobich_sousede.csv)
- Řádků: 448; jeden řádek = jedna obec × volební období × ukazatel
- Zdroj: Výpočet z `finance_*`.
- Pozor: Za období se počítají rozpočtové roky, za které odpovídá dané zastupitelstvo (sloupec `roky`); období 2022–2026 zatím jen 2023–2025.
- Pozor: Hodnoty sloupce `ukazatel` mají stejný význam jako stejnojmenné sloupce v souborech `finance_*_2010-2025.csv` (viz výše).

| Sloupec | Význam |
|---|---|
| `obec` | Název obce: Horní Domaslavice, Pazderna, Dolní Domaslavice nebo Lučina. |
| `obdobi` | Volební období (2010–2014 … 2022–2026). |
| `roky` | Rozpočtové roky zahrnuté do součtu. |
| `ukazatel` | Kód ukazatele. Navíc: `penize_konec_obdobi`, `uvery_konec_obdobi` (stav na konci posledního roku) a `podil_vlastni_io_na_danovych` (podíl `io_vlastni` na `trida1`, desetinné číslo 0–1). |
| `kc_celkem` | Součet za roky v období. U `*_konec_obdobi` stav na konci období, u `podil_*` podíl (0–1). Kč. |
| `kc_na_obyv_a_rok` | Průměr na obyvatele a rok; u `*_konec_obdobi` stav na obyvatele; u podílů prázdné. Kč. |

## subjekty_ARES_pravni_forma_sousede.csv

Ekonomické subjekty se sídlem v obci podle právní formy (ARES). HD a sousední obce.

- Odkaz: [data/subjekty_ARES_pravni_forma_sousede.csv](https://hd-v-datech.cz/data/subjekty_ARES_pravni_forma_sousede.csv)
- Řádků: 55; jeden řádek = jedna obec × právní forma
- Zdroj: ARES (jako souhrn subjektů); názvy právních forem z číselníku ARES PravniForma.

| Sloupec | Význam |
|---|---|
| `kod_obce` | Kód obce podle ČSÚ (HD 512192). |
| `obec` | Název obce: Horní Domaslavice, Pazderna, Dolní Domaslavice, Lučina nebo Vojkovice. |
| `pravni_forma_kod` | Kód právní formy. |
| `pravni_forma` | Název právní formy. |
| `pocet` | Počet subjektů. |
| `na_1000_obyv_2025` | Na 1 000 obyvatel (k 1. 7. 2025). |

## subjekty_ARES_souhrn_sousede.csv

Ekonomické subjekty se sídlem v obci podle ARES, sloučené do skupin, i na 1 000 obyvatel. HD a sousední obce.

- Odkaz: [data/subjekty_ARES_souhrn_sousede.csv](https://hd-v-datech.cz/data/subjekty_ARES_souhrn_sousede.csv)
- Řádků: 5; jeden řádek = jedna obec
- Zdroj: ARES, vyhledání podle kódu obce sídla (POST /ekonomicke-subjekty-v-be/rest/ekonomicke-subjekty/vyhledat); HD, Pazderna, DD a Lučina stav k 30. 10. 2026, ostatní obce k 1. 11. 2026.
- Pozor: Počítá se sídlo, ne místo působení. Podnikající FO jsou v ARES i tehdy, když aktivně nepodnikají.

| Sloupec | Význam |
|---|---|
| `kod_obce` | Kód obce podle ČSÚ (HD 512192). |
| `obec` | Název obce: Horní Domaslavice, Pazderna, Dolní Domaslavice, Lučina nebo Vojkovice. |
| `obyvatel_1_7_2025` | Obyvatelé k 1. 7. 2025 (ČSÚ), základ přepočtu. |
| `subjektu_celkem` | Subjekty celkem. |
| `na_1000` | Subjekty na 1 000 obyvatel. |
| `FO_podnikajici` | Podnikající fyzické osoby (právní formy 101, 102, 105, 107, 424). |
| `FO_na_1000` | Na 1 000 obyvatel. |
| `obchodni_spolecnosti` | Obchodní společnosti (111 v.o.s., 112 s.r.o., 121 a.s., 421 odštěpný závod). |
| `OS_na_1000` | Na 1 000 obyvatel. |
| `spolky_pobocne_ustavy` | Spolky, pobočné spolky, ústavy, nadace, nadační fondy a o.p.s. (706, 736, 161, 117, 118, 141). |
| `spolky_na_1000` | Na 1 000 obyvatel. |
| `ostatni` | Ostatní (obec, příspěvkové organizace, církevní osoby, SVJ, družstva aj.). |

## transfery_NNO_paragrafy_sousede_2010-2025.csv

Rozpis transferů z `transfery_NNO_*` podle paragrafu a položky. HD a sousední obce.

- Odkaz: [data/transfery_NNO_paragrafy_sousede_2010-2025.csv](https://hd-v-datech.cz/data/transfery_NNO_paragrafy_sousede_2010-2025.csv)
- Řádků: 495; jeden řádek = jedna obec × rok × paragraf × položka
- Zdroj: Monitor státní pokladny MF, FIN 2-12 M.

| Sloupec | Význam |
|---|---|
| `kod_obce` | Kód obce podle ČSÚ (HD 512192). |
| `obec` | Název obce: Horní Domaslavice, Pazderna, Dolní Domaslavice, Lučina nebo Vojkovice. |
| `rok` | Rozpočtový rok. |
| `paragraf` | Paragraf rozpočtové skladby. |
| `polozka` | Položka (5221, 5222, 5223, 5229, 5492, 5493, 6322). |
| `polozka_nazev` | Název položky. |
| `schvaleny` | Schválený rozpočet. Kč. |
| `upraveny` | Upravený rozpočet. Kč. |
| `skutecnost` | Skutečnost. Kč. |

## transfery_NNO_sousede_2010-2025.csv

Transfery obcí neziskovým organizacím, církvím a fyzickým osobám po letech 2010–2025. HD a sousední obce.

- Odkaz: [data/transfery_NNO_sousede_2010-2025.csv](https://hd-v-datech.cz/data/transfery_NNO_sousede_2010-2025.csv)
- Řádků: 80; jeden řádek = jedna obec × rok
- Zdroj: Monitor státní pokladny MF, FIN 2-12 M za prosinec (skutečnost); obyvatelé ČSÚ k 1. 7.
- Pozor: Hlavní ukazatel webu je `NNO_bez_par_6171_52xx_62xx` (položky 5221 + 5222 + 5229 bez § 6171 a § 52xx, 62xx).
- Pozor: Výkaz neukazuje příjemce plateb.

| Sloupec | Význam |
|---|---|
| `kod_obce` | Kód obce podle ČSÚ (HD 512192). |
| `obec` | Název obce: Horní Domaslavice, Pazderna, Dolní Domaslavice, Lučina nebo Vojkovice. |
| `rok` | Rozpočtový rok. |
| `obyvatel_1_7` | Obyvatelé k 1. 7. |
| `pol_5221` | Položka 5221 – obecně prospěšným společnostem. Kč. |
| `pol_5222` | Položka 5222 – spolkům. Kč. |
| `pol_5223` | Položka 5223 – církvím a náboženským společnostem. Kč. |
| `pol_5229` | Položka 5229 – ostatním neziskovým a podobným organizacím. Kč. |
| `pol_5492` | Položka 5492 – dary obyvatelstvu. Kč. |
| `pol_5493` | Položka 5493 – účelové neinvestiční transfery fyzickým osobám. Kč. |
| `pol_6322` | Položka 6322 – investiční transfery spolkům. Kč. |
| `neinv_NNO_5221_5222_5229` | Součet 5221 + 5222 + 5229 (neočištěno). Kč. |
| `na_obyvatele` | Předchozí sloupec na obyvatele. Kč. |
| `vcetne_cirkvi_5223` | Součet 5221 + 5222 + 5229 + 5223. Kč. |
| `vcetne_cirkvi_na_obyv` | Předchozí sloupec na obyvatele. Kč. |
| `NNO_bez_par_6171_52xx_62xx` | 5221 + 5222 + 5229 bez § 6171, § 52xx a § 62xx (očištěno). Kč. |
| `NNO_ocist_na_obyv` | Očištěný součet na obyvatele. Kč. |

## ukazatele_rozvaha_vzz_sousede.csv

Rozvaha a výkaz zisku a ztráty HD a sousedních obcí (včetně Vojkovic): majetek, peníze, závazky, náklady, výnosy, odpisy.

- Odkaz: [data/ukazatele_rozvaha_vzz_sousede.csv](https://hd-v-datech.cz/data/ukazatele_rozvaha_vzz_sousede.csv)
- Řádků: 80; jeden řádek = jedna obec × rok (stav k 31. 12.)
- Zdroj: Monitor státní pokladny MF: rozvaha a výkaz zisku a ztráty.
- Pozor: Účetní hodnoty, ne tržní ceny. Stavby se účetně odepisují od roku 2012.

| Sloupec | Význam |
|---|---|
| `obec` | Zkratka obce: HD, PA (Pazderna), DD, LU (Lučina). |
| `nazev` | Název obce. |
| `kod_obce` | Kód obce ČSÚ. |
| `rok` | Rok (stav k 31. 12.). |
| `obyvatel_31_12` | Obyvatelé k 31. 12. |
| `aktiva_netto` | Aktiva celkem po odečtení oprávek. Kč. |
| `pasiva` | Pasiva celkem. Kč. |
| `stavby_brutto` | Stavby (účet 021) v pořizovací ceně. Kč. |
| `stavby_opravky` | Oprávky ke stavbám (účet 081). Kč. |
| `stavby_netto` | Stavby po odečtení oprávek. Kč. |
| `pozemky_031` | Pozemky (účet 031). Kč. |
| `nedok_invest_042` | Nedokončený dlouhodobý hmotný majetek (účet 042), tj. rozestavěné investice. Kč. |
| `zalohy_dm_052` | Poskytnuté zálohy na dlouhodobý hmotný majetek (účet 052). Kč. |
| `ucet_231` | Základní běžný účet (231). Kč. |
| `ucet_241` | Běžný účet (241). Kč. |
| `ucet_244` | Termínované vklady krátkodobé (244). Kč. |
| `ucet_245` | Jiné běžné účty (245). Kč. |
| `ucet_236` | Běžné účty fondů (236). Kč. |
| `penize_231_244_245` | Peníze = 231 + 244 + 245. Kč. |
| `kratk_fin_majetek_celkem` | Krátkodobý finanční majetek celkem. Kč. |
| `uvery_dlouhodobe_451` | Dlouhodobé úvěry (451). Kč. |
| `ost_dlouhodobe_zavazky_459` | Ostatní dlouhodobé závazky (459). Kč. |
| `navratne_vypomoci_452` | Přijaté návratné finanční výpomoci dlouhodobé (452). Kč. |
| `dlouhodobe_zalohy_transfery_472` | Dlouhodobé přijaté zálohy na transfery (472). Kč. |
| `dlouhodobe_zavazky_celkem` | Dlouhodobé závazky celkem. Kč. |
| `uvery_kratkodobe_281` | Krátkodobé úvěry (281). Kč. |
| `kratk_zavazky_celkem` | Krátkodobé závazky celkem. Kč. |
| `vlastni_kapital` | Vlastní kapitál. Kč. |
| `transfery_403` | Transfery na pořízení dlouhodobého majetku (403), tj. dotace zachycené v kapitálu. Kč. |
| `vh_rozvaha_493` | Výsledek hospodaření běžného účetního období v rozvaze (493). Kč. |
| `naklady` | Náklady celkem (výkaz zisku a ztráty). Kč. |
| `vynosy` | Výnosy celkem. Kč. |
| `odpisy_551` | Odpisy dlouhodobého majetku (551). Kč. |
| `opravy_511` | Opravy a udržování (511). Kč. |
| `vh_vzz` | Výsledek hospodaření podle výkazu zisku a ztráty = výnosy − náklady. Kč. |

## ukazatele_sousede_2010-2025.csv

Stejné ukazatele jako `finance_*` pro HD a všech šest sousedních obcí v dlouhém formátu (vhodné pro filtrování a grafy).

- Odkaz: [data/ukazatele_sousede_2010-2025.csv](https://hd-v-datech.cz/data/ukazatele_sousede_2010-2025.csv)
- Řádků: 4480; jeden řádek = jedna obec × rok × ukazatel
- Zdroj: Monitor státní pokladny MF; obyvatelé ČSÚ.
- Pozor: Hodnoty sloupce `ukazatel` mají stejný význam jako stejnojmenné sloupce v souborech `finance_*_2010-2025.csv` (viz výše).

| Sloupec | Význam |
|---|---|
| `obec` | Název obce: Horní Domaslavice, Pazderna, Dolní Domaslavice nebo Lučina. |
| `kod_obce` | Kód obce podle ČSÚ (HD 512192). |
| `rok` | Rozpočtový rok. |
| `ukazatel` | Kód ukazatele (např. `prijmy`, `io`, `penize_231_244_245`). |
| `kc` | Hodnota v Kč. |
| `obyv_1_7` | Obyvatelé k 1. 7. |
| `obyv_31_12` | Obyvatelé k 31. 12. |
| `kc_na_obyv` | `kc` na obyvatele: toky děleno `obyv_1_7`, stavy k 31. 12. děleno `obyv_31_12`. |

## usneseni_zo_2022-2026.csv

Usnesení zastupitelstva obce Horní Domaslavice 2022–2026 (a konec období 2018–2022).

- Odkaz: [data/usneseni_zo_2022-2026.csv](https://hd-v-datech.cz/data/usneseni_zo_2022-2026.csv)
- Řádků: 547; jeden řádek = jedno usnesení
- Zdroj: Zápisy ze zasedání zastupitelstva zveřejněné obcí (sloupec `zdroj`).
- Pozor: Text je přepsaný ze zápisů; jména fyzických osob jsou vynechaná. Závazné je znění zápisu na webu obce.
- Pozor: Témata a typ přiřadil autor webu podle textu, mohou být nepřesná.

| Sloupec | Význam |
|---|---|
| `cislo` | Číslo usnesení ve tvaru pořadí/zasedání/rok. |
| `zasedani` | Pořadové číslo zasedání. |
| `datum` | Datum zasedání (RRRR-MM-DD). |
| `obdobi` | Volební období. |
| `text` | Znění usnesení. |
| `typ` | Druh rozhodnutí: schvaluje, neschvaluje, bere na vědomí, volí, pověřuje, ukládá, ruší, jiné. |
| `vysledek` | přijato / nepřijato / neuveden v zápisu. |
| `pro` | Počet hlasů pro. |
| `proti` | Počet hlasů proti. |
| `zdrzel` | Počet zdržených. |
| `tema` | Témata oddělená středníkem. |
| `castka_kc` | Částka uvedená v usnesení, pokud nějaká je. Kč. |
| `zdroj` | Zápis, ze kterého usnesení pochází. |

## volby_komunalni_kandidatky_sousede_1994-2026.csv

Kandidátky v komunálních volbách 1994–2026: hlasy, mandáty a odvozený typ kandidátky. HD a sousední obce.

- Odkaz: [data/volby_komunalni_kandidatky_sousede_1994-2026.csv](https://hd-v-datech.cz/data/volby_komunalni_kandidatky_sousede_1994-2026.csv)
- Řádků: 144; jeden řádek = jedna obec × volby × kandidátka
- Zdroj: volby.cz (jako u souhrnu komunálních voleb).
- Pozor: Kandidátky pojmenované jménem jednotlivého kandidáta jsou nahrazeny textem „kandidátka jednotlivce (NK)“; web neuvádí jména fyzických osob.

| Sloupec | Význam |
|---|---|
| `kod_obce` | Kód obce podle ČSÚ (HD 512192). |
| `obec` | Název obce: Horní Domaslavice, Pazderna, Dolní Domaslavice, Lučina nebo Vojkovice. |
| `rok` | Rok voleb. |
| `cislo` | Číslo kandidátky (volební strany) podle volby.cz. |
| `kandidatka` | Název kandidátky (zkrácený tak, jak ho uvádí volby.cz). |
| `hlasy` | Hlasy pro kandidátku. |
| `hlasy_pct` | Podíl hlasů, %. |
| `pocet_kandidatu` | Počet kandidátů na kandidátce. |
| `mandaty` | Získané mandáty. |
| `typ_kandidatky` | Odvozený typ: NK/SNK, strana/hnutí/koalice, strana/hnutí + NK; „(podle názvu)“ = odvozeno jen z názvu. |
| `kandidatu_navrh_NK_2026` | Jen 2026: počet kandidátů navržených jako NK. |
| `kandidatu_celkem_2026` | Jen 2026: počet kandidátů na kandidátce podle jmenného seznamu. |

## volby_komunalni_kontinuita_sousede_2002-2026.csv

Kolik zastupitelů zvolených v daném roce bylo zvoleno už v předchozích volbách (bez jmen). HD a sousední obce.

- Odkaz: [data/volby_komunalni_kontinuita_sousede_2002-2026.csv](https://hd-v-datech.cz/data/volby_komunalni_kontinuita_sousede_2002-2026.csv)
- Řádků: 35; jeden řádek = jedna obec × volby (od roku 2002)
- Zdroj: Výpočet ze seznamů zvolených na volby.cz; porovnává se příjmení a jméno bez titulů.
- Pozor: Změny příjmení se nezjišťovaly (u HD je známý jeden případ v roce 2026, není započten).
- Pozor: Ve Vojkovicích byli v letech 2018 a 2022 zvoleni dva lidé se stejným jménem; rozlišeni jsou podle věku.

| Sloupec | Význam |
|---|---|
| `kod_obce` | Kód obce podle ČSÚ (HD 512192). |
| `obec` | Název obce: Horní Domaslavice, Pazderna, Dolní Domaslavice, Lučina nebo Vojkovice. |
| `rok` | Rok voleb. |
| `zvolenych_se_jmenem` | Počet zvolených. |
| `zvoleni_i_v_minulych_volbach` | Z nich zvolení i v bezprostředně předchozích volbách. |
| `pct_z_minulych` | Podíl znovuzvolených z předchozích voleb, %. |
| `zvoleni_kdykoli_drive_od_1998` | Z nich zvolení v kterýchkoli dřívějších volbách od roku 1998. |
| `pct_kdykoli_drive` | Podíl zvolených kdykoli dříve, %. |

## volby_komunalni_sousede_1994-2026.csv

Komunální volby 1994–2026 po obcích: voliči, účast, počet kandidátek a mandátů, rozdělení mandátů, typ kandidátek. HD a sousední obce.

- Odkaz: [data/volby_komunalni_sousede_1994-2026.csv](https://hd-v-datech.cz/data/volby_komunalni_sousede_1994-2026.csv)
- Řádků: 45; jeden řádek = jedna obec × volby
- Zdroj: volby.cz: výsledky za obec (kv1111) a seznamy zvolených (kv21111) 1994–2022, datové soubory kv2026 (vygenerováno 11. 10. 2026).
- Pozor: Typ kandidátky je odvozený z navrhující strany zvolených kandidátů, u kandidátek bez mandátu a u roku 1994 z názvu.
- Pozor: Pro rok 1994 volby.cz jména zvolených neuvádí, sloupce o zvolených jsou proto 0.

| Sloupec | Význam |
|---|---|
| `kod_obce` | Kód obce podle ČSÚ (HD 512192). |
| `obec` | Název obce: Horní Domaslavice, Pazderna, Dolní Domaslavice, Lučina nebo Vojkovice. |
| `rok` | Rok voleb. |
| `pocet_clenu_zo` | Počet členů zastupitelstva (mandátů). |
| `volici` | Voliči v seznamu. |
| `vydane_obalky` | Vydané úřední obálky. |
| `ucast_pct` | Volební účast, %. |
| `platne_hlasy` | Platné hlasy (v komunálních volbách má volič tolik hlasů, kolik je mandátů). |
| `pocet_kandidatek` | Počet kandidátních listin. |
| `pocet_kandidatu` | Počet kandidátů na všech kandidátkách. |
| `kandidatek_s_mandatem` | Počet kandidátek, které získaly aspoň jeden mandát. |
| `rozdeleni_mandatu` | Mandáty jednotlivých kandidátek seřazené sestupně (např. „3 : 3 : 3 : 3 : 1“). |
| `nejsilnejsi_kandidatka_pct` | Podíl hlasů nejsilnější kandidátky, %. |
| `kandidatek_typu_NK_SNK` | Počet kandidátek zařazených jako nezávislí kandidáti nebo jejich sdružení. |
| `mandatu_kandidatkam_NK_SNK` | Mandáty, které získaly kandidátky NK/SNK. |
| `zvolenych_celkem` | Počet zvolených podle seznamu zvolených. |
| `zvolenych_navrh_NK` | Zvolení, které navrhla „NK“ (bez navrhující strany). |
| `zvolenych_BEZPP` | Zvolení bez politické příslušnosti. |

## volby_prezidentska_2023_sousede.csv

Prezidentská volba 2023: účast v obou kolech a výsledek 2. kola (bez jmen kandidátů). HD, sousední obce, okres FM a ČR.

- Odkaz: [data/volby_prezidentska_2023_sousede.csv](https://hd-v-datech.cz/data/volby_prezidentska_2023_sousede.csv)
- Řádků: 14; jeden řádek = jedno území × kolo
- Zdroj: volby.cz, pls/prez2023 (pe311, pe2).

| Sloupec | Význam |
|---|---|
| `kod` | Kód území: kód obce ČSÚ, 8102 = okres Frýdek-Místek, CZ = Česká republika. |
| `uzemi` | Název území (obec, okres nebo Česká republika). |
| `kolo` | 1. nebo 2. kolo. |
| `volici` | Voliči v seznamu. |
| `vydane_obalky` | Vydané obálky. |
| `ucast_pct` | Volební účast, %. |
| `platne_hlasy` | Platné hlasy. |
| `k2_zvoleny_prezident_hlasy` | Jen 2. kolo: hlasy pro kandidáta zvoleného prezidentem. |
| `k2_zvoleny_prezident_pct` | Jen 2. kolo: jeho podíl, %. |
| `k2_protikandidat_hlasy` | Jen 2. kolo: hlasy pro protikandidáta. |
| `k2_protikandidat_pct` | Jen 2. kolo: jeho podíl, %. |

## volby_snemovni_strany_sousede_2013-2025.csv

Výsledky stran ve volbách do Poslanecké sněmovny 2013–2025. HD a sousední obce.

- Odkaz: [data/volby_snemovni_strany_sousede_2013-2025.csv](https://hd-v-datech.cz/data/volby_snemovni_strany_sousede_2013-2025.csv)
- Řádků: 612; jeden řádek = jedno území × volby × strana
- Zdroj: volby.cz, appdata ps{rok}.

| Sloupec | Význam |
|---|---|
| `kod` | Kód území: kód obce ČSÚ, 8102 = okres Frýdek-Místek, CZ = Česká republika. |
| `uzemi` | Název území (obec, okres nebo Česká republika). |
| `rok` | Rok voleb. |
| `cislo` | Číslo strany v daných volbách. |
| `strana` | Název strany (zkrácený podle volby.cz). |
| `hlasy` | Hlasy. |
| `pct` | Podíl platných hlasů, %. |

## volby_snemovni_ucast_sousede_2013-2025.csv

Účast ve volbách do Poslanecké sněmovny 2013–2025. HD a sousední obce.

- Odkaz: [data/volby_snemovni_ucast_sousede_2013-2025.csv](https://hd-v-datech.cz/data/volby_snemovni_ucast_sousede_2013-2025.csv)
- Řádků: 28; jeden řádek = jedno území × volby
- Zdroj: volby.cz, appdata ps{rok}: výsledky za obec, okres a ČR.

| Sloupec | Význam |
|---|---|
| `kod` | Kód území: kód obce ČSÚ, 8102 = okres Frýdek-Místek, CZ = Česká republika. |
| `uzemi` | Název území (obec, okres nebo Česká republika). |
| `rok` | Rok voleb. |
| `volici` | Voliči v seznamu. |
| `vydane_obalky` | Vydané obálky. |
| `ucast_pct` | Volební účast, %. |
| `platne_hlasy` | Platné hlasy. |

## vydaje_kategorie_sousede_2010-2025.csv

Výdaje HD a sousedních obcí rozdělené podle účelu (sloučené paragrafy) a podle druhu (sloučené položky).

- Odkaz: [data/vydaje_kategorie_sousede_2010-2025.csv](https://hd-v-datech.cz/data/vydaje_kategorie_sousede_2010-2025.csv)
- Řádků: 2464; jeden řádek = jedna obec × rok × členění × kategorie
- Zdroj: Monitor státní pokladny MF, FIN 2-12 M.
- Pozor: Obě členění (`ucel`, `druh`) dávají v součtu stejné celkové výdaje; nesčítat je dohromady.

| Sloupec | Význam |
|---|---|
| `obec` | Název obce: Horní Domaslavice, Pazderna, Dolní Domaslavice nebo Lučina. |
| `rok` | Rozpočtový rok. |
| `cleneni` | `ucel` = podle paragrafů (na co), `druh` = podle položek (jaký výdaj). |
| `kategorie` | Název kategorie; v závorce bývají zahrnuté paragrafy nebo položky. |
| `kc` | Výdaje v Kč. |
| `kc_na_obyv` | Kč na obyvatele (obyvatelé k 1. 7.). |

