# Horní Domaslavice v datech

Neoficiální občanský web s veřejnými daty o obci Horní Domaslavice a srovnáním se sousedními obcemi.

## Sestavení

```
/usr/bin/python3 -I build.py
```

Vyžaduje `pandoc`. Texty stránek jsou v `obsah/*.md` (YAML hlavička `title`, `description`, `updated`), data v `data/`, obrázky v `img/`. Výstup jde do `docs/`, který zveřejňuje GitHub Pages (Settings → Pages → branch `main`, složka `/docs`).

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
