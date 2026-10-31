"""Převod S-JTSK (EPSG:5514, Křovák East North) na WGS84 v čistém Pythonu.

Postup:
1. inverzní Křovákovo zobrazení (EPSG metoda 9819, parametry EPSG:5514) -> zeměpisné
   souřadnice na Besselově elipsoidu (datum S-JTSK, poledník Greenwich);
2. převod na geocentrické X, Y, Z (Bessel 1841, h = 0);
3. sedmiprvková Helmertova transformace S-JTSK -> WGS84, konvence Position Vector
   (EPSG:1623: tx 570,8 m, ty 85,7 m, tz 462,8 m, rx 4,998″, ry 1,587″, rz 5,261″, ds 3,56 ppm);
4. geocentrické -> zeměpisné na elipsoidu WGS84 (iterace).

Nominální přesnost transformace EPSG:1623 je asi 1 m. Ověření je popsáno v obsah/mapa.md.

Použití:  from krovak import sjtsk_to_wgs84;  lat, lon = sjtsk_to_wgs84(x, y)
kde x, y jsou souřadnice EPSG:5514 tak, jak je uvádí RÚIAN (obě záporné, x = východ, y = sever).
"""
import math

# Bessel 1841
A_B = 6377397.155
F_B = 1 / 299.1528128
E2_B = 2 * F_B - F_B ** 2
E_B = math.sqrt(E2_B)

# WGS84
A_W = 6378137.0
F_W = 1 / 298.257223563
E2_W = 2 * F_W - F_W ** 2

# Křovák (EPSG:5514)
LAT_C = math.radians(49.5)                       # latitude of projection centre
LON_0 = math.radians(24 + 50 / 60)               # 24°50' východně od Greenwiche (= 42°30' od Ferra)
ALPHA_C = math.radians(30 + 17 / 60 + 17.30311 / 3600)  # azimut osy
LAT_P = math.radians(78.5)                       # pseudo standard parallel
K_P = 0.9999

# Helmert S-JTSK -> WGS84 (EPSG:1623, Position Vector)
TX, TY, TZ = 570.8, 85.7, 462.8
SEC = math.pi / (180 * 3600)
RX, RY, RZ = 4.998 * SEC, 1.587 * SEC, 5.261 * SEC
DS = 3.56e-6

# odvozené konstanty Křováka (EPSG Guidance Note 7-2)
_A = A_B * math.sqrt(1 - E2_B) / (1 - E2_B * math.sin(LAT_C) ** 2)
_B = math.sqrt(1 + E2_B * math.cos(LAT_C) ** 4 / (1 - E2_B))
_G0 = math.asin(math.sin(LAT_C) / _B)
_T0 = (math.tan(math.pi / 4 + _G0 / 2)
       * ((1 + E_B * math.sin(LAT_C)) / (1 - E_B * math.sin(LAT_C))) ** (E_B * _B / 2)
       / math.tan(math.pi / 4 + LAT_C / 2) ** _B)
_N = math.sin(LAT_P)
_R0 = K_P * _A / math.tan(LAT_P)


def krovak_inverse(x, y):
    """EPSG:5514 (x = východ, y = sever, záporné) -> (lat, lon) v radiánech na Besselu."""
    # EPSG:5514 je „East North“ varianta: southing = -y, westing = -x
    Xp = -y
    Yp = -x
    r = math.hypot(Xp, Yp)
    theta = math.atan2(Yp, Xp)
    D = theta / math.sin(LAT_P)
    T = 2 * (math.atan((_R0 / r) ** (1 / _N) * math.tan(math.pi / 4 + LAT_P / 2)) - math.pi / 4)
    U = math.asin(math.cos(ALPHA_C) * math.sin(T) - math.sin(ALPHA_C) * math.cos(T) * math.cos(D))
    V = math.asin(math.cos(T) * math.sin(D) / math.cos(U))
    lat = U
    for _ in range(20):
        s = math.sin(lat)
        nxt = 2 * (math.atan(
            _T0 ** (-1 / _B) * math.tan(U / 2 + math.pi / 4) ** (1 / _B)
            * ((1 + E_B * s) / (1 - E_B * s)) ** (E_B / 2)) - math.pi / 4)
        if abs(nxt - lat) < 1e-13:
            lat = nxt
            break
        lat = nxt
    lon = LON_0 - V / _B
    return lat, lon


def geodetic_to_ecef(lat, lon, a, e2, h=0.0):
    n = a / math.sqrt(1 - e2 * math.sin(lat) ** 2)
    return ((n + h) * math.cos(lat) * math.cos(lon),
            (n + h) * math.cos(lat) * math.sin(lon),
            (n * (1 - e2) + h) * math.sin(lat))


def ecef_to_geodetic(X, Y, Z, a, e2):
    lon = math.atan2(Y, X)
    p = math.hypot(X, Y)
    lat = math.atan2(Z, p * (1 - e2))
    for _ in range(20):
        n = a / math.sqrt(1 - e2 * math.sin(lat) ** 2)
        h = p / math.cos(lat) - n
        nxt = math.atan2(Z, p * (1 - e2 * n / (n + h)))
        if abs(nxt - lat) < 1e-13:
            lat = nxt
            break
        lat = nxt
    return lat, lon


def helmert_pv(X, Y, Z):
    """Position Vector transformation (EPSG metoda 1033 / 9606)."""
    m = 1 + DS
    return (TX + m * (X - RZ * Y + RY * Z),
            TY + m * (RZ * X + Y - RX * Z),
            TZ + m * (-RY * X + RX * Y + Z))


def sjtsk_to_wgs84(x, y):
    """EPSG:5514 -> (lat, lon) ve stupních WGS84."""
    lat_b, lon_b = krovak_inverse(x, y)
    X, Y, Z = geodetic_to_ecef(lat_b, lon_b, A_B, E2_B)
    X, Y, Z = helmert_pv(X, Y, Z)
    lat, lon = ecef_to_geodetic(X, Y, Z, A_W, E2_W)
    return math.degrees(lat), math.degrees(lon)


def distance_m(lat1, lon1, lat2, lon2):
    """Vzdálenost dvou bodů WGS84 (haversine, poloměr 6 371 km); stačí pro kontrolu v řádu metrů."""
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp, dl = p2 - p1, math.radians(lon2 - lon1)
    h = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * 6371008.8 * math.asin(math.sqrt(h))


if __name__ == '__main__':
    # Testovací bod z EPSG Guidance Note 7-2 (Křovák, Bessel, bez transformace data):
    # lat 50°12'32.442"N, lon 16°50'59.179"E (Greenwich) <-> southing 1050538.643, westing 568991.000
    lat, lon = krovak_inverse(-568991.000, -1050538.643)
    exp_lat = 50 + 12 / 60 + 32.442 / 3600
    exp_lon = 16 + 50 / 60 + 59.179 / 3600
    d = distance_m(math.degrees(lat), math.degrees(lon), exp_lat, exp_lon)
    print(f'EPSG GN7-2 test (Bessel): {math.degrees(lat):.7f} {math.degrees(lon):.7f}, odchylka {d:.3f} m')
    print('Definiční bod obce HD:', sjtsk_to_wgs84(-459231.00, -1118136.00))
