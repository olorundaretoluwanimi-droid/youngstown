# Natural Earth (public domain) → assets/map.json: land, lakes and rail lines of the lower 48 window, Albers-projected and simplified,
# in a 0..1000 × 0..~620 space. No borders are drawn (DIRECTOR.md §13); rails are today's network, shown as a schematic.
import json, math, os
D = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); NE = os.path.join(D, 'research', 'ne')
P1, P2, L0, F0 = map(math.radians, (29.5, 45.5, -96, 37.5))
n = (math.sin(P1) + math.sin(P2)) / 2; Cc = math.cos(P1) ** 2 + 2 * n * math.sin(P1); r0 = math.sqrt(Cc - 2 * n * math.sin(F0)) / n
def alb(lon, lat):
    l, f = math.radians(lon), math.radians(lat); r = math.sqrt(Cc - 2 * n * math.sin(f)) / n; th = n * (l - L0)
    return r * math.sin(th), r0 - r * math.cos(th)
X0, Y0 = alb(-125, 49.5)[0], alb(-96, 50.5)[1]; X1 = alb(-66, 49.5)[0]; Y1 = alb(-98, 23.5)[1]
S = 1000 / (X1 - X0)
def pr(lon, lat): x, y = alb(lon, lat); return round((x - X0) * S, 1), round((Y0 - y) * S, 1)
H = round((Y0 - Y1) * S, 1)
def inwin(lon, lat): return -130 <= lon <= -60 and 20 <= lat <= 54
def simp(pts, tol):
    out = [pts[0]]
    for p in pts[1:]:
        if abs(p[0] - out[-1][0]) + abs(p[1] - out[-1][1]) >= tol: out.append(p)
    return out
def rings(geom):
    t, c = geom['type'], geom['coordinates']
    if t == 'Polygon': return c
    if t == 'MultiPolygon': return [r for poly in c for r in poly]
    if t == 'LineString': return [c]
    if t == 'MultiLineString': return c
    return []
def layer(fn, tol, keep=lambda p: True):
    out = []
    for f in json.load(open(os.path.join(NE, fn), encoding='utf-8'))['features']:
        if not keep(f['properties']): continue
        for r in rings(f['geometry']):
            if not any(inwin(*q[:2]) for q in r): continue
            pts = simp([pr(*q[:2]) for q in r], tol)
            if len(pts) >= 2: out.append(pts)
    return out
land = layer('ne_50m_land.geojson', 1.2); lakes = layer('ne_50m_lakes.geojson', 1.0)
rail = layer('ne_10m_railroads_north_america.geojson', 1.5)
towns = {'Rochester': (-77.61, 43.16), 'Parsons': (-95.26, 37.34), 'New York': (-74.0, 40.71), 'Los Angeles': (-118.24, 34.05), 'Chicago': (-87.63, 41.88),
         'Seattle': (-122.33, 47.61), 'Miami': (-80.19, 25.76), 'Boston': (-71.06, 42.36), 'Denver': (-104.99, 39.74), 'Dallas': (-96.8, 32.78),
         'Atlanta': (-84.39, 33.75), 'San Francisco': (-122.42, 37.77), 'Minneapolis': (-93.27, 44.98), 'Washington': (-77.04, 38.9), 'Phoenix': (-112.07, 33.45), 'Waterville': (-75.38, 42.93), 'Kansas City': (-94.58, 39.1), 'Detroit': (-83.05, 42.33), 'New Orleans': (-90.07, 29.95), 'Portland': (-122.68, 45.52), 'Salt Lake City': (-111.89, 40.76), 'Nashville': (-86.78, 36.16), 'Omaha': (-95.94, 41.26), 'Albuquerque': (-106.65, 35.08), 'Tuskegee': (-85.69, 32.42), 'Hampton': (-76.35, 37.03), 'Cambridge': (-71.11, 42.37), 'Santo Domingo': (-69.9, 18.5)}
json.dump({'W': 1000, 'H': H, 'land': land, 'lakes': lakes, 'rail': rail, 'towns': {k: pr(*v) for k, v in towns.items()}},
          open(os.path.join(D, 'assets', 'map.json'), 'w'), separators=(',', ':'))
print('H', H, 'land', len(land), 'lakes', len(lakes), 'rail', len(rail), sum(len(r) for r in rail), 'pts')
