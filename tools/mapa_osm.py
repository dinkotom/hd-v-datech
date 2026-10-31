"""Stažení podkladů z OpenStreetMap (Overpass API) pro mapu obce.

Použití:
  /usr/bin/python3 -I tools/mapa_osm.py <výstupní_složka> [jih západ sever východ]

Výchozí obdélník pokrývá katastr Horních Domaslavic s okrajem asi 300 m.
Stahuje: autobusové zastávky, kostely a kaple, hřbitovy, dětská hřiště, sportoviště,
hasičské zbrojnice, obecní úřad, MŠ a adresní body převzaté z RÚIAN (ref:ruian:addr),
které slouží ke kontrole převodu souřadnic. Výstup: <složka>/osm_hd.json.
"""
import json
import os
import subprocess
import sys
import urllib.parse
import urllib.request

SERVERS = ['https://overpass-api.de/api/interpreter',
           'https://overpass.kumi.systems/api/interpreter']
BBOX = (49.675, 18.432, 49.709, 18.494)


def query(bbox):
    b = '(%.4f,%.4f,%.4f,%.4f)' % bbox
    return f'''[out:json][timeout:90];
(
  node["highway"="bus_stop"]{b};
  node["public_transport"="platform"]["bus"="yes"]{b};
  nwr["amenity"~"^(place_of_worship|townhall|kindergarten|fire_station|grave_yard|community_centre)$"]{b};
  nwr["landuse"="cemetery"]{b};
  nwr["leisure"~"^(playground|pitch|sports_centre)$"]{b};
  nwr["building"~"^(church|chapel)$"]{b};
  nwr["ref:ruian:addr"]{b};
);
out center tags;'''


def main():
    out = sys.argv[1]
    bbox = tuple(map(float, sys.argv[2:6])) if len(sys.argv) >= 6 else BBOX
    os.makedirs(out, exist_ok=True)
    data = urllib.parse.urlencode({'data': query(bbox)}).encode()
    ua = 'hd-v-datech/1.0 (obcansky web, mapa obce)'
    last = None
    for url in SERVERS:
        try:
            try:
                req = urllib.request.Request(url, data=data, headers={'User-Agent': ua, 'Accept': 'application/json'})
                with urllib.request.urlopen(req, timeout=180) as r:
                    body = r.read()
            except Exception as e:
                # systémový Python na macOS (LibreSSL) neprojde TLS na některých serverech -> curl
                print(f'{url}: urllib selhal ({e}), zkouším curl', file=sys.stderr)
                body = subprocess.run(['curl', '-sS', '-m', '180', '-A', ua, '-H', 'Accept: application/json',
                                       '--data-binary', '@-', url], input=data, capture_output=True, check=True).stdout
            js = json.loads(body)
            js['_source'] = url
            with open(os.path.join(out, 'osm_hd.json'), 'w', encoding='utf-8') as f:
                json.dump(js, f, ensure_ascii=False)
            print(f'{url}: {len(js.get("elements", []))} prvků -> {out}/osm_hd.json')
            return 0
        except Exception as e:  # zkusíme další server
            last = e
            print(f'{url}: {e}', file=sys.stderr)
    print(f'Overpass nedostupný: {last}', file=sys.stderr)
    return 1


if __name__ == '__main__':
    sys.exit(main())
