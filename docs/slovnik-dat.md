# Slovník dat

Popis datových souborů webu Horní Domaslavice v datech (https://hd-v-datech.cz/). Všechny soubory jsou CSV v UTF-8, oddělovač čárka, desetinná tečka, data ve tvaru RRRR-MM-DD. Částky jsou v Kč, běžné ceny.

## CUZK_UHDP_druhy_pozemku_4obce_2004_2014_2026.csv

Výměry druhů pozemků po katastrálních územích (orná půda, louky, lesy, zastavěné plochy…).

- Odkaz: [data/CUZK_UHDP_druhy_pozemku_4obce_2004_2014_2026.csv](https://hd-v-datech.cz/data/CUZK_UHDP_druhy_pozemku_4obce_2004_2014_2026.csv)
- Řádků: 18; jeden řádek = jeden rok × katastrální území
- Zdroj: ČÚZK, úhrnné hodnoty druhů pozemků (UHDP).
- Pozor: Dolní Domaslavice mají dvě katastrální území (Dolní Domaslavice a Volovec), Lučina také (Lučina a Kocurovice). Za obec je třeba řádky sečíst podle sloupce `obec`.

| Sloupec | Význam |
|---|---|
| `rok` | Rok stavu (2004, 2014, 2026). |
| `obec` | Zkratka obce: HD, PA, DD, LU. |
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

## RUIAN_souhrn_4obce_stav_20260930.csv

Budovy, byty a technické vybavení podle Registru územní identifikace (RÚIAN), stav 30. 9. 2026.

- Odkaz: [data/RUIAN_souhrn_4obce_stav_20260930.csv](https://hd-v-datech.cz/data/RUIAN_souhrn_4obce_stav_20260930.csv)
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

## finance_DD_2010-2025.csv

Hospodaření obce Dolní Domaslavice po letech 2010–2025 (stejné sloupce jako `finance_HD_2010-2025.csv`; obec zřizuje základní školu).

- Odkaz: [data/finance_DD_2010-2025.csv](https://hd-v-datech.cz/data/finance_DD_2010-2025.csv)
- Řádků: 16; jeden řádek = jeden rozpočtový rok
- Zdroj: Monitor státní pokladny MF: výkaz FIN 2-12 M za prosinec (plnění rozpočtu) a rozvaha k 31. 12.
- Pozor: Částky v Kč, běžné ceny. Rok 2026 zatím chybí (MF zveřejní roční data na jaře 2027).
- Pozor: Každý sloupec `X_na_obyv` = `X` / `obyv_1_7` (Kč na obyvatele).

Sloupce jsou stejné jako v `finance_HD_2010-2025.csv`.

## finance_HD_2010-2025.csv

Hospodaření obce Horní Domaslavice po letech 2010–2025: příjmy, výdaje, investice, opravy, dotace, rezervy, peníze a úvěry.

- Odkaz: [data/finance_HD_2010-2025.csv](https://hd-v-datech.cz/data/finance_HD_2010-2025.csv)
- Řádků: 16; jeden řádek = jeden rozpočtový rok
- Zdroj: Monitor státní pokladny MF: výkaz FIN 2-12 M za prosinec (plnění rozpočtu) a rozvaha k 31. 12.
- Pozor: Částky v Kč, běžné ceny. Rok 2026 zatím chybí (MF zveřejní roční data na jaře 2027).
- Pozor: Každý sloupec `X_na_obyv` = `X` / `obyv_1_7` (Kč na obyvatele).

| Sloupec | Význam |
|---|---|
| `rok` | Rozpočtový rok. |
| `obyv_1_7` | Počet obyvatel k 1. 7. daného roku (ČSÚ). Tímto číslem se dělí všechny sloupce `*_na_obyv`. |
| `obyv_31_12` | Počet obyvatel k 31. 12. daného roku (ČSÚ). |
| `prijmy` | Příjmy celkem = třídy 1–4 rozpočtové skladby bez převodů z vlastních fondů (položky 413x). Kč. |
| `trida1` | Daňové příjmy (třída 1): sdílené daně, daň z nemovitých věcí, místní poplatky aj. Kč. |
| `rud` | Sdílené daně (rozpočtové určení daní: DPH, daně z příjmů fyzických a právnických osob). Kč. |
| `dan_nemovitosti` | Daň z nemovitých věcí (položka 1511). Kč. |
| `dppo_obec` | Daň z příjmů právnických osob za obec (položka 1122). Obec ji platí sama sobě, proto je stejná částka i ve `vyd_6399`. Kč. |
| `trida2` | Nedaňové příjmy (třída 2): pronájmy, prodej služeb, úroky aj. Kč. |
| `trida3` | Kapitálové příjmy (třída 3): prodej majetku. Kč. |
| `trida4` | Přijaté transfery (třída 4) bez převodů z vlastních fondů = `dotace_neinv` + `dotace_inv`. Kč. |
| `dotace_neinv` | Neinvestiční přijaté transfery (včetně souhrnného dotačního vztahu na výkon státní správy). Kč. |
| `dotace_inv` | Investiční přijaté dotace. Kč. |
| `vydaje` | Výdaje celkem = třídy 5 a 6, bez převodů mezi vlastními účty (§ 6330) a bez daně z příjmů za obec (§ 6399). Kč. |
| `vydaje_sch` | Schválený rozpočet výdajů (stejné vymezení jako `vydaje`). Kč. |
| `vydaje_upr` | Upravený rozpočet výdajů ke konci roku (po rozpočtových opatřeních). Kč. |
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
| `vyd_6399` | Ostatní finanční operace (§ 6399), hlavně daň z příjmů za obec; do `vydaje` se nepočítají. Kč. |
| `*_na_obyv` (40 sloupců) | Stejnojmenný sloupec bez přípony vydělený `obyv_1_7`. Kč na obyvatele. |

## finance_LUC_2010-2025.csv

Hospodaření obce Lučina po letech 2010–2025 (stejné sloupce jako `finance_HD_2010-2025.csv`; obec zřizuje základní školu a má výdaje spojené s nádrží Žermanice).

- Odkaz: [data/finance_LUC_2010-2025.csv](https://hd-v-datech.cz/data/finance_LUC_2010-2025.csv)
- Řádků: 16; jeden řádek = jeden rozpočtový rok
- Zdroj: Monitor státní pokladny MF: výkaz FIN 2-12 M za prosinec (plnění rozpočtu) a rozvaha k 31. 12.
- Pozor: Částky v Kč, běžné ceny. Rok 2026 zatím chybí (MF zveřejní roční data na jaře 2027).
- Pozor: Každý sloupec `X_na_obyv` = `X` / `obyv_1_7` (Kč na obyvatele).

Sloupce jsou stejné jako v `finance_HD_2010-2025.csv`.

## finance_PAZ_2010-2025.csv

Hospodaření obce Pazderna po letech 2010–2025 (stejné sloupce jako `finance_HD_2010-2025.csv`).

- Odkaz: [data/finance_PAZ_2010-2025.csv](https://hd-v-datech.cz/data/finance_PAZ_2010-2025.csv)
- Řádků: 16; jeden řádek = jeden rozpočtový rok
- Zdroj: Monitor státní pokladny MF: výkaz FIN 2-12 M za prosinec (plnění rozpočtu) a rozvaha k 31. 12.
- Pozor: Částky v Kč, běžné ceny. Rok 2026 zatím chybí (MF zveřejní roční data na jaře 2027).
- Pozor: Každý sloupec `X_na_obyv` = `X` / `obyv_1_7` (Kč na obyvatele).

Sloupce jsou stejné jako v `finance_HD_2010-2025.csv`.

## investice_opravy_podle_paragrafu_4obce.csv

Investice a opravy 4 obcí podle paragrafu rozpočtové skladby (na co šly).

- Odkaz: [data/investice_opravy_podle_paragrafu_4obce.csv](https://hd-v-datech.cz/data/investice_opravy_podle_paragrafu_4obce.csv)
- Řádků: 629; jeden řádek = jedna obec × rok × paragraf (jen nenulové)
- Zdroj: Monitor státní pokladny MF, FIN 2-12 M.

| Sloupec | Význam |
|---|---|
| `obec` | Název obce: Horní Domaslavice, Pazderna, Dolní Domaslavice nebo Lučina. |
| `rok` | Rozpočtový rok. |
| `paragraf` | Paragraf rozpočtové skladby (např. 2212 silnice, 2219 chodníky a ostatní komunikace, 3111 mateřská škola, 3412 sportovní zařízení, 3613 nebytové hospodářství, 3631 veřejné osvětlení, 5512 hasiči). |
| `investice_plus_opravy_kc` | Třída 6 + položka 5171 v daném paragrafu. Kč. |

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

## roztrisenost_4obce.csv

Ukazatele roztříštěnosti zástavby: jak daleko od sebe a od středu obce jsou domy a kolik tvoří skupin.

- Odkaz: [data/roztrisenost_4obce.csv](https://hd-v-datech.cz/data/roztrisenost_4obce.csv)
- Řádků: 4; jeden řádek = jedna obec
- Zdroj: Výpočet z polohy budov v RÚIAN (stav 30. 9. 2026).
- Pozor: „Shluk N m“ = skupina domů, kde každý dům má souseda ve skupině blíž než N metrů.

| Sloupec | Význam |
|---|---|
| `obec` | Zkratka obce: HD, PA, DD, LU. |
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

## souhrn_obyvatel_rocne_2000-2025_4obce_okres_CR.csv

Počet obyvatel, věková struktura a pohyb obyvatel 2000–2025 pro 4 obce, okres Frýdek-Místek a Českou republiku.

- Odkaz: [data/souhrn_obyvatel_rocne_2000-2025_4obce_okres_CR.csv](https://hd-v-datech.cz/data/souhrn_obyvatel_rocne_2000-2025_4obce_okres_CR.csv)
- Řádků: 154; jeden řádek = jedno území × rok
- Zdroj: Český statistický úřad (sloupec `zdroj` uvádí kód datové sady).
- Pozor: Pohyb obyvatel (narození … vystěhovalí) je u některých let a území prázdný.

| Sloupec | Význam |
|---|---|
| `uzemi` | HD, Pazderna, DD, Lucina, okres (Frýdek-Místek), CR (Česká republika). |
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

## souhrn_po_obdobich_4obce.csv

Součty ukazatelů za volební období a průměr na obyvatele a rok.

- Odkaz: [data/souhrn_po_obdobich_4obce.csv](https://hd-v-datech.cz/data/souhrn_po_obdobich_4obce.csv)
- Řádků: 256; jeden řádek = jedna obec × volební období × ukazatel
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

## ukazatele_4obce_2010-2025.csv

Stejné ukazatele jako `finance_*` pro všechny 4 obce v dlouhém formátu (vhodné pro filtrování a grafy).

- Odkaz: [data/ukazatele_4obce_2010-2025.csv](https://hd-v-datech.cz/data/ukazatele_4obce_2010-2025.csv)
- Řádků: 2560; jeden řádek = jedna obec × rok × ukazatel
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
| `kc_na_obyv` | `kc` / `obyv_1_7`. |

## ukazatele_rozvaha_vzz_4_obce.csv

Rozvaha a výkaz zisku a ztráty 4 obcí: majetek, peníze, závazky, náklady, výnosy, odpisy.

- Odkaz: [data/ukazatele_rozvaha_vzz_4_obce.csv](https://hd-v-datech.cz/data/ukazatele_rozvaha_vzz_4_obce.csv)
- Řádků: 64; jeden řádek = jedna obec × rok (stav k 31. 12.)
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

## vydaje_kategorie_4obce_2010-2025.csv

Výdaje 4 obcí rozdělené podle účelu (sloučené paragrafy) a podle druhu (sloučené položky).

- Odkaz: [data/vydaje_kategorie_4obce_2010-2025.csv](https://hd-v-datech.cz/data/vydaje_kategorie_4obce_2010-2025.csv)
- Řádků: 1408; jeden řádek = jedna obec × rok × členění × kategorie
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

