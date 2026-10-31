import sys, zipfile, io, os
# usage: extract.py zip outdir ico prefix [member_substring]
zp, out, ico, pref = sys.argv[1:5]
sub = sys.argv[5] if len(sys.argv) > 5 else ''
with zipfile.ZipFile(zp) as z:
    for n in z.namelist():
        if sub not in n: continue
        with z.open(n) as f:
            t = io.TextIOWrapper(f, encoding='utf-8', errors='replace')
            header = t.readline()
            rows = []
            for l in t:
                if ico in l:
                    p = l.split(';')
                    if len(p) > 4 and p[4].strip('"') == ico:
                        rows.append(l)
        if not rows: print(n, 0); continue
        on = os.path.join(out, pref + os.path.basename(n))
        with open(on, 'w', encoding='utf-8') as g:
            g.write(header); g.writelines(rows)
        print(n, len(rows))
