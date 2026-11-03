# Horní Domaslavice v datech

Neoficiální občanský web s veřejnými daty o obci Horní Domaslavice a srovnáním se sousedními obcemi.

## Sestavení

```
/usr/bin/python3 -I build.py
```

Vyžaduje `pandoc`. Texty stránek jsou v `obsah/*.md` (YAML hlavička `title`, `description`, `updated`), data v `data/`, obrázky v `img/`. Výstup jde do `docs/`. Hotový `docs/` se commituje; po pushi do `main` ho Cloudflare Pages samo nasadí (viz Provoz).

## Provoz

Od 3. 11. 2026. Do 2. 11. 2026 web běžel na GitHub Pages; ty jsou vypnuté, protože GitHub pro doménu nedokázal vydat HTTPS certifikát.

**Hosting – Cloudflare Pages**, projekt `hd-v-datech` (Workers & Pages):
- napojení na GitHub repo `dinkotom/hd-v-datech`, větev `main`, framework *None*, build příkaz prázdný, výstupní složka `docs`;
- náhled na https://hd-v-datech.pages.dev, vlastní domény `hd-v-datech.cz` a `www.hd-v-datech.cz` (Custom domains);
- Cloudflare přesměrovává `/stranka.html` na `/stranka` (308). Odkazy v buildu zůstávají s `.html`, funguje obojí.

**Soubory, které build generuje pro Cloudflare:**
- `docs/_headers` – HTTP hlavičky (CSP, HSTS, Referrer-Policy, nosniff, Permissions-Policy), funkce `build_headers()`. Hash jediného inline skriptu (`THEME_JS`) se do CSP počítá sám. Když stránka začne načítat cokoli z dalšího webu (skript, styl, obrázek, `fetch`), je nutné doplnit doménu do CSP, jinak to prohlížeč zablokuje.
- `docs/404.html` – bez ní by Cloudflare vracel na neexistující adresy úvodní stránku se stavem 200.
- `docs/sitemap.xml` a `docs/robots.txt` (odkaz na sitemap; Cloudflare před něj sám přidává své nastavení pro roboty). Každá stránka má kanonickou adresu bez `.html`, Open Graph (náhled při sdílení, obrázek `img/og.png` 1200 × 630) a ikonu `static/favicon.svg` + `img/apple-touch-icon.png`. Úvod nese strukturovaná data `WebSite`, stránka Data `Dataset` (Google Dataset Search).
- Vlastní `robots.txt` web nemá; Cloudflare ho generuje sám (volba *Bot Preference Sync*, všechny roboty včetně AI povoleny). Kdyby byl potřeba vlastní, je třeba sladit ho s nastavením v Cloudflare.

**Doména a DNS:**
- `hd-v-datech.cz` je registrovaná u WEDOS (expirace 31. 10. 2027, prodlužuje se tam). U WEDOS je nastaven jen NSSET s nameservery Cloudflare a KEYSET pro DNSSEC; DNS záznamy se u WEDOS needitují.
- DNS spravuje Cloudflare (nameservery `isla.ns.cloudflare.com`, `lennon.ns.cloudflare.com`). Záznamy:
  - `hd-v-datech.cz` a `www` – vytvořilo je Pages (Custom domains), přes proxy Cloudflare;
  - TXT `hd-v-datech.cz` `v=spf1 -all` a TXT `_dmarc` `v=DMARC1; p=reject; sp=reject; adkim=s; aspf=s` – doména neposílá ani nepřijímá e-mail (žádné MX), záznamy brání podvrhům odesílatele;
  - TXT `_github-pages-challenge-dinkotom` – ověření domény na GitHubu; ponechat, aby si doménu nemohl na GitHub Pages zabrat nikdo jiný.
- **DNSSEC:** podepisuje Cloudflare (DNS → Settings → DNSSEC). Do registru .cz se nezadává DS, ale veřejný klíč: u WEDOS *Nastavení DNSSEC → vytvořit a použít vlastní KEYSET*, Flag KSK, algoritmus 13, klíč z Cloudflare (*Public Key*, key tag 2371). Kontrola: `dig +short DS hd-v-datech.cz @a.ns.nic.cz` a `dig +dnssec hd-v-datech.cz @1.1.1.1` (příznak `ad`).
- **Při změně DNS nebo vypnutí DNSSEC v Cloudflare** je nutné nejdřív u WEDOS zrušit KEYSET a počkat, až DS zmizí z registru (TTL 1 h), jinak doména přestane fungovat. WEDOS nedovolí měnit nameservery, dokud nemá vyřízený požadavek na DNSSEC (trvá i několik hodin).

**Repozitář na GitHubu:** veřejný, zapnuté jen Issues (hlášení chyb). Wiki, Projects a GitHub Actions jsou vypnuté. Nasazení na Cloudflare Actions nepotřebuje, používá aplikaci Cloudflare s přístupem jen k tomuto repu. Kdo může do `main` pushovat, může změnit web, proto je na účtu nutné dvoufázové přihlášení (2FA).

**Vyhledávače** (registrováno 3. 11. 2026):
- Google Search Console – vlastnost typu Doména `hd-v-datech.cz` (ověření přes DNS v Cloudflare), odeslána sitemap `https://hd-v-datech.cz/sitemap.xml`;
- Seznam Webmaster – `https://hd-v-datech.cz/`, ověření meta tagem `seznam-wmt` na úvodní stránce (`SITE_VERIFICATION` v `build.py`; tag neodstraňovat ani negenerovat nový), sitemap si Seznam bere z `robots.txt`;
- Bing Webmaster Tools – import z Google Search Console, sitemap odeslána ručně.

**Pravidla v Cloudflare:**
- Rules → Redirect Rules: `https://www.*` → `https://${1}`, 301, se zachováním parametrů – `www` přesměrovává na doménu bez `www`;
- SSL/TLS: certifikát vydává Cloudflare automaticky, http přesměrovává na https.
- Caching → Crawler Hints zapnuto: Cloudflare po změnách obsahu sám ohlašuje vyhledávačům (IndexNow).
- Návštěvnost: Pages projekt → Metrics → Web Analytics (Cloudflare skript `beacon.min.js` vkládá do stránek sám, bez cookies). V CSP jsou proto povoleny `static.cloudflareinsights.com` (skript) a `cloudflareinsights.com` (odesílání). Hrubé serverové statistiky jsou u domény v Analytics & Logs → HTTP Traffic.

## Hlášení chyb (Google Formulář)

Dokud není formulář nastavený, tlačítko „Nahlásit chybu“ otevře předvyplněný issue na GitHubu.

Nastavení formuláře:

1. Na forms.google.com založte formulář „Hlášení chyby – HD v datech“ s pěti otázkami typu *Krátká odpověď* nebo *Odstavec*:
   - Stránka
   - Citovaný text
   - Co je špatně
   - Správný údaj a zdroj
   - E-mail
2. V Nastavení vypněte sběr e-mailů a přihlášení. Formulář musí být otevřený i pro lidi bez účtu Google.
3. Klikněte na ⋮ → *Získat předvyplněný odkaz*, vyplňte do každého pole cokoli a zkopírujte odkaz. Obsahuje `entry.NNNN=` pro každé pole.
4. Do `REPORT_FORM` v `build.py` doplňte:
   - `action`: adresa formuláře, kde `/viewform` nahradíte `/formResponse`;
   - čísla `entry.NNNN` pro jednotlivá pole.
5. V odpovědích formuláře zapněte *Dostávat e-mailová oznámení o nových odpovědích* a případně propojte s tabulkou.

Opravy se zapisují do `obsah/opravy.md`.

## Licence

Texty, grafy a zpracovaná data (`obsah/`, `data/`, `docs/`) jsou pod licencí [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/deed.cs). Uveďte zdroj „Horní Domaslavice v datech, hd-v-datech.cz“. Původní data se řídí podmínkami svých zdrojů (ČSÚ, MF, ČÚZK a další).
