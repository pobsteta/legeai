# -*- coding: utf-8 -*-
"""Carte « à la manière de Cassini » des plus belles forêts de chêne de France.

Données : contours des régions (gregoiredavid/france-geojson), pays voisins, rivières et
massifs (Natural Earth 10m). Projection de Cassini centrée sur le méridien de Paris.
Sortie : SVG (vectoriel, éditable), puis PNG/PDF via rsvg-convert.

Préparation (les données ne sont pas dans le dépôt, ~30 Mo) :
    mkdir -p geo && cd geo
    for f in ne_10m_rivers_lake_centerlines ne_10m_rivers_europe ne_10m_geography_regions_polys ne_10m_admin_0_countries; do
      curl -sSO https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/$f.geojson; done
    curl -sSO https://raw.githubusercontent.com/gregoiredavid/france-geojson/master/regions.geojson
    pip install shapely numpy
Puis, depuis le dossier qui contient geo/ :
    python3 outils/carte_cassini.py
    rsvg-convert -d 200 -p 200 -f png -o carte.png geo/carte-cassini-forets-de-chene.svg
    rsvg-convert -f pdf -o carte.pdf geo/carte-cassini-forets-de-chene.svg
Polices utilisées : Lora et Caladea (Google Fonts / crosextra), avec repli sur Liberation Serif.
La liste des forêts, des chênes remarquables, des villes et des étiquettes est en tête du script (FORETS, CHENES, VILLES…).
"""
import json, math, random
import shapely, shapely.prepared
from shapely.geometry import shape, Polygon, MultiPolygon, LineString, MultiLineString, box, Point
from shapely.ops import unary_union, linemerge

random.seed(20261108)
import os
G = os.environ.get("GEO_DIR", "geo/").rstrip("/") + "/"
OUT_SVG = G + "carte-cassini-forets-de-chene.svg"

# ---------------------------------------------------------------- projection
LON0 = 2.337229   # méridien de Paris
LAT0 = 48.8366    # Observatoire
R_KM = 6371.0
SCALE = 1 / 4_000_000  # 1:4 000 000  → 1 km = 0.25 mm
KM2MM = 1000 * 1000 * SCALE  # 0.25

def proj(lon, lat):
    lam = math.radians(lon - LON0); phi = math.radians(lat)
    x = R_KM * math.asin(math.cos(phi) * math.sin(lam))
    y = R_KM * (math.atan2(math.tan(phi), math.cos(lam)) - math.radians(LAT0))
    return x * KM2MM, -y * KM2MM  # y vers le bas

def tproj(geom):
    def f(coords):
        out = []
        for x, y in coords:
            out.append(proj(x, y))
        return out
    return shapely.transform(geom, lambda a: __import__("numpy").array(f(a)), include_z=False)

# fenêtre géographique
LON_W, LON_E, LAT_S, LAT_N = -5.95, 10.05, 41.05, 51.45
corners = [proj(LON_W, LAT_S), proj(LON_E, LAT_S), proj(LON_W, LAT_N), proj(LON_E, LAT_N), proj(LON0, LAT_N), proj(LON0, LAT_S)]
X0 = min(c[0] for c in corners); X1 = max(c[0] for c in corners)
Y0 = min(c[1] for c in corners); Y1 = max(c[1] for c in corners)
MARGIN = 9.0
W = (X1 - X0) + 2 * MARGIN; H = (Y1 - Y0) + 2 * MARGIN
def mm(x, y):  # projeté → coordonnées de page
    return x - X0 + MARGIN, y - Y0 + MARGIN
def P(lon, lat):
    return mm(*proj(lon, lat))

WINDOW = box(X0, Y0, X1, Y1)

# ---------------------------------------------------------------- données
def load(fn):
    return json.load(open(G + fn, encoding="utf-8"))

regions = load("regions.geojson")
france = unary_union([shape(f["geometry"]) for f in regions["features"]])
france = max([france] if isinstance(france, Polygon) else list(france.geoms), key=lambda g: g.area) if False else france
# ne garder que la métropole (fenêtre)
france = france.intersection(box(LON_W - 1, LAT_S - 1, LON_E + 1, LAT_N + 1))
france_p = tproj(france).simplify(0.12)

ne = load("ne_10m_admin_0_countries.geojson")
neigh_names = {"Spain", "Andorra", "Belgium", "Luxembourg", "Germany", "Switzerland", "Italy", "Monaco", "United Kingdom", "Jersey", "Guernsey", "Netherlands"}
neigh = [shape(f["geometry"]) for f in ne["features"] if f["properties"].get("NAME") in neigh_names or f["properties"].get("ADMIN") in neigh_names]
neigh = unary_union(neigh).intersection(box(LON_W - 1, LAT_S - 1, LON_E + 1, LAT_N + 1))
neigh_p = tproj(neigh).simplify(0.15)

regs = load("ne_10m_geography_regions_polys.geojson")
mtn = [shape(f["geometry"]) for f in regs["features"] if f["properties"].get("NAME") in {"Vosges", "Ardennes", "Jura", "Massif Central", "PYRENEES", "ALPS"}]
mtn = unary_union(mtn).intersection(france)
mtn_p = tproj(mtn).simplify(0.2)

riv1 = load("ne_10m_rivers_lake_centerlines.geojson")
riv2 = load("ne_10m_rivers_europe.geojson")
WANT = {"Loire", "Seine", "Rhône", "Garonne", "Dordogne", "Saône", "Marne", "Yonne", "Doubs", "Allier", "Cher", "Vienne", "Lot", "Tarn", "Sarthe", "Mayenne", "Vilaine", "Somme", "Charente", "Maas", "Mosel", "Rhin", "Adour", "Aude", "Durance", "Eure", "Aube", "Isère"}
rivers = {}
for src in (riv1, riv2):
    for f in src["features"]:
        n = f["properties"].get("name")
        if n in WANT:
            rivers.setdefault(n, []).append(shape(f["geometry"]))
clipper = france.buffer(0.03)
rivers_p = {}
for n, parts in rivers.items():
    g = unary_union(parts).intersection(clipper)
    if g.is_empty:
        continue
    g = linemerge(g) if isinstance(g, MultiLineString) else g
    rivers_p[n] = tproj(g).simplify(0.15)

# ---------------------------------------------------------------- contenu
FORETS = [  # nom, surface (ha), lat, lon, décalage étiquette (dx, dy) mm, ancre
    ("TRONÇAIS", 10600, 46.655, 2.72, (0, 9.0), "middle"),
    ("BERCÉ", 5400, 47.80, 0.43, (0, 7.5), "middle"),
    ("ORLÉANS", 22000, 48.00, 2.32, (0, 9.5), "middle"),
    ("FONTAINEBLEAU", 25000, 48.41, 2.66, (9.5, 4.5), "start"),
    ("COMPIÈGNE", 14400, 49.37, 2.92, (0, 8.5), "middle"),
    ("RAMBOUILLET", 14000, 48.64, 1.80, (0, 7.2), "middle"),
    ("BELLÊME", 2400, 48.37, 0.57, (-1.0, -4.5), "end"),
    ("RÉNO-VALDIEU", 1600, 48.50, 0.69, (-1.5, -5.8), "end"),
    ("CHAUX", 20500, 47.08, 5.66, (0, 10.0), "middle"),
    ("DARNEY", 8000, 48.06, 6.00, (0, 8.0), "middle"),
    ("HAYE", 11000, 48.70, 6.02, (1.5, 8.5), "middle"),
    ("LA REINE", 5000, 48.76, 5.80, (0, -5.5), "middle"),
    ("PAIMPONT", 7500, 48.02, -2.17, (0, 8.0), "middle"),
    ("BERTRANGES", 10000, 47.15, 3.36, (0, 9.0), "middle"),
    ("MOULIÈRE", 5000, 46.71, 0.61, (5.5, 2.0), "start"),
    ("LOCHES", 3600, 47.14, 1.05, (0, 6.8), "middle"),
    ("CHINON", 5000, 47.22, 0.28, (-5.0, 1.5), "end"),
    ("MORMAL", 9200, 50.21, 3.72, (7.5, 1.0), "start"),
    ("GRÉSIGNE", 3500, 44.04, 1.73, (6.5, 1.0), "start"),
    ("BOUCONNE", 2000, 43.65, 1.18, (-2.0, 7.0), "middle"),
    ("MERVENT", 5000, 46.53, -0.73, (0, -6.5), "middle"),
]
CHENES = [  # chênes remarquables isolés
    ("le Chêne-chapelle d'Allouville", 49.593, 0.671, (-1.0, -4.4), "end"),
    ("le Chêne de Guillotin", 48.084, -2.189, (-5.5, -4.0), "end"),
    ("le Chêne de l'Attaque", 49.52, 5.37, (6.0, -1.5), "start"),
]
VILLES = [  # nom, lat, lon, importance, (dx, dy), ancre
    ("PARIS", 48.857, 2.352, 2, (-4.0, -2.5), "end"),
    ("Orléans", 47.902, 1.909, 1, (-4.0, 1.0), "end"),
    ("Tours", 47.394, 0.689, 1, (4.0, 1.0), "start"),
    ("Le Mans", 48.006, 0.199, 1, (-4.0, 1.0), "end"),
    ("Rennes", 48.117, -1.678, 1, (4.0, 1.0), "start"),
    ("Nantes", 47.218, -1.554, 1, (0, -3.2), "middle"),
    ("Rouen", 49.443, 1.099, 1, (-4.0, 1.0), "end"),
    ("Lille", 50.629, 3.057, 1, (-4.0, 1.0), "end"),
    ("Reims", 49.258, 4.032, 1, (4.0, 1.0), "start"),
    ("Nancy", 48.692, 6.184, 1, (4.0, 1.0), "start"),
    ("Metz", 49.120, 6.177, 1, (4.0, -2.2), "start"),
    ("Strasbourg", 48.573, 7.752, 1, (-4.0, 1.0), "end"),
    ("Dijon", 47.322, 5.041, 1, (-4.0, 1.0), "end"),
    ("Besançon", 47.238, 6.024, 1, (4.0, -2.0), "start"),
    ("Lyon", 45.764, 4.836, 1, (4.0, 1.0), "start"),
    ("Clermont", 45.777, 3.087, 1, (4.0, 1.0), "start"),
    ("Moulins", 46.565, 3.333, 1, (4.0, 1.0), "start"),
    ("Bourges", 47.081, 2.399, 1, (4.0, 1.0), "start"),
    ("Poitiers", 46.580, 0.340, 1, (4.0, 1.0), "start"),
    ("Bordeaux", 44.838, -0.579, 1, (4.0, 1.0), "start"),
    ("Toulouse", 43.605, 1.444, 1, (4.0, 3.0), "start"),
    ("Montpellier", 43.611, 3.877, 1, (0, -4.0), "middle"),
    ("Marseille", 43.296, 5.370, 1, (4.0, 1.0), "start"),
    ("Caen", 49.183, -0.370, 1, (4.0, 1.0), "start"),
    ("Amiens", 49.895, 2.302, 1, (-4.0, 1.0), "end"),
    ("Limoges", 45.834, 1.262, 1, (4.0, 1.0), "start"),
    ("Grenoble", 45.188, 5.725, 1, (4.0, 1.0), "start"),
    ("Nice", 43.710, 7.262, 1, (4.0, 1.0), "start"),
    ("Bayonne", 43.493, -1.475, 1, (4.0, 1.0), "start"),
    ("Ajaccio", 41.927, 8.737, 1, (-4.0, 1.0), "end"),
    ("Épinal", 48.172, 6.449, 1, (4.0, 1.0), "start"),
    ("Alençon", 48.433, 0.092, 1, (0, 4.2), "middle"),
    ("Dole", 47.092, 5.49, 1, (-4.0, 1.0), "end"),
    ("Brest", 48.39, -4.49, 1, (0, -4.0), "middle"),
]
PAYS = [("ANGLETERRE", -1.3, 50.75, 0), ("PAYS-BAS AUTRICHIENS", 4.55, 50.85, 0), ("EMPIRE D'ALLEMAGNE", 8.85, 49.75, -90),
        ("SUISSE", 7.6, 46.85, 0), ("PIÉMONT", 7.9, 45.0, 0), ("ESPAGNE", -1.0, 42.55, 0)]
MERS = [("LA MANCHE", -1.6, 49.78, -8), ("GOLFE DE GASCOGNE", -3.9, 43.95, 0), ("MER MÉDITERRANÉE", 5.3, 41.75, 0), ("OCÉAN", -5.55, 47.55, -90)]
RIVER_LABELS = {  # nom affiché, fraction de départ le long du tracé
    "Loire": ("la Loire", (-0.85, 47.37)), "Seine": ("la Seine", 0.30), "Rhône": ("le Rhône", (4.75, 44.55)), "Garonne": ("la Garonne", 0.55),
    "Dordogne": ("la Dordogne", 0.35), "Saône": ("la Saône", 0.45), "Maas": ("la Meuse", 0.62), "Mosel": ("la Moselle", 0.7),
    "Rhin": ("le Rhin", 0.4), "Marne": ("la Marne", 0.5), "Allier": ("l'Allier", (3.35, 46.25)), "Vienne": ("la Vienne", 0.5),
    "Lot": ("le Lot", 0.3), "Tarn": ("le Tarn", 0.5), "Charente": ("la Charente", 0.4), "Somme": ("la Somme", 0.4), "Durance": ("la Durance", 0.4),
}

# ---------------------------------------------------------------- helpers SVG
def fmt(v):
    return ("%.2f" % v).rstrip("0").rstrip(".")

def path_of(geom, close=True):
    """Chemin SVG d'une géométrie projetée (coordonnées page)."""
    parts = []
    def ring(coords):
        s = []
        for i, (x, y) in enumerate(coords):
            px, py = mm(x, y)
            s.append(("M" if i == 0 else "L") + fmt(px) + "," + fmt(py))
        if close:
            s.append("Z")
        return "".join(s)
    if geom.is_empty:
        return ""
    if isinstance(geom, Polygon):
        parts.append(ring(geom.exterior.coords))
        for r in geom.interiors:
            parts.append(ring(r.coords))
    elif isinstance(geom, MultiPolygon):
        for g in geom.geoms:
            parts.append(path_of(g, close))
    elif isinstance(geom, LineString):
        parts.append(ring(geom.coords) if not close else ring(geom.coords))
    elif isinstance(geom, MultiLineString):
        for g in geom.geoms:
            parts.append(path_of(g, close))
    elif hasattr(geom, "geoms"):
        for g in geom.geoms:
            parts.append(path_of(g, close))
    return " ".join(p for p in parts if p)

def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

svg = []
A = svg.append

# ---------------------------------------------------------------- en-tête
A('<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="%smm" height="%smm" viewBox="0 0 %s %s">' % (fmt(W), fmt(H), fmt(W), fmt(H)))
A('''<defs>
<style>
  .enc{font-family:"Lora","Caladea","Liberation Serif",serif}
  .lbl{font-family:"Caladea","Lora","Liberation Serif",serif}
  .foret{font-family:"Lora","Caladea",serif;font-weight:600;font-size:3.1px;letter-spacing:0.55px;fill:#2e3a24}
  .ville{font-family:"Caladea","Lora",serif;font-size:2.7px;fill:#2b2418}
  .ville2{font-family:"Lora","Caladea",serif;font-weight:700;font-size:3.6px;letter-spacing:0.5px;fill:#2b2418}
  .riv{font-family:"Lora","Caladea",serif;font-style:italic;font-size:2.6px;fill:#3f5468;letter-spacing:0.25px}
  .pays{font-family:"Lora","Caladea",serif;font-size:4.4px;letter-spacing:1.6px;fill:#5a4d3a}
  .mer{font-family:"Lora","Caladea",serif;font-style:italic;font-size:4.6px;letter-spacing:2.2px;fill:#4f6476}
  .chene{font-family:"Lora","Caladea",serif;font-style:italic;font-size:2.7px;fill:#3a2e1c}
  .titre{font-family:"Lora","Caladea",serif;font-weight:700;fill:#2b2418}
  .cart{font-family:"Lora","Caladea",serif;fill:#2b2418}
  .carti{font-family:"Lora","Caladea",serif;font-style:italic;fill:#2b2418}
  .leg{font-family:"Caladea","Lora",serif;font-size:2.8px;fill:#2b2418}
</style>
<filter id="papier" x="0" y="0" width="100%" height="100%">
  <feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="3" seed="7" result="n"/>
  <feColorMatrix in="n" type="matrix" values="0 0 0 0 0.93  0 0 0 0 0.88  0 0 0 0 0.76  0 0 0 0.18 0" result="g"/>
  <feBlend in="SourceGraphic" in2="g" mode="multiply"/>
</filter>
<symbol id="arbre" viewBox="-5 -6 10 12" overflow="visible">
  <path d="M0,-5.2 C1.6,-5.4 2.9,-4.4 3.1,-3 C4.4,-2.6 4.8,-0.9 3.9,0.3 C4.5,1.7 3.3,3.1 1.9,2.8 C1.3,3.9 -1.3,3.9 -1.9,2.8 C-3.3,3.1 -4.5,1.7 -3.9,0.3 C-4.8,-0.9 -4.4,-2.6 -3.1,-3 C-2.9,-4.4 -1.6,-5.4 0,-5.2 Z" fill="#b7c49d" stroke="#3e4a30" stroke-width="0.55" stroke-linejoin="round"/>
  <path d="M1.2,-4.6 C2.8,-3.6 3.6,-1.6 3.2,0.6 C2.9,1.9 2.2,2.6 1.5,2.9" fill="none" stroke="#5c6a48" stroke-width="0.5" stroke-linecap="round"/>
  <path d="M2.1,-2.4 l0.9,0.4 M2.5,-1.2 l0.9,0.3 M2.6,0 l0.9,0.2 M2.3,1.2 l0.8,0.3" stroke="#5c6a48" stroke-width="0.4" fill="none" stroke-linecap="round"/>
  <path d="M0,3 L0,5.6" stroke="#3e4a30" stroke-width="0.8" stroke-linecap="round"/>
  <path d="M-1.4,5.8 L1.4,5.8" stroke="#3e4a30" stroke-width="0.5" stroke-linecap="round"/>
</symbol>
<symbol id="gros-chene" viewBox="-6 -7 12 14" overflow="visible">
  <path d="M0,-6 C2.2,-6.2 4,-4.9 4.1,-3.2 C5.6,-2.7 6,-0.6 4.9,0.7 C5.5,2.3 4,3.8 2.3,3.4 C1.6,4.6 -1.6,4.6 -2.3,3.4 C-4,3.8 -5.5,2.3 -4.9,0.7 C-6,-0.6 -5.6,-2.7 -4.1,-3.2 C-4,-4.9 -2.2,-6.2 0,-6 Z" fill="#a9b98c" stroke="#2f3a24" stroke-width="0.6" stroke-linejoin="round"/>
  <path d="M1.5,-5.3 C3.6,-4.1 4.6,-1.8 4.2,0.9 C3.8,2.3 3,3.1 2,3.4" fill="none" stroke="#4e5c3c" stroke-width="0.55"/>
  <path d="M2.3,-3 l1,0.5 M2.9,-1.6 l1,0.4 M3.1,-0.2 l1,0.3 M2.8,1.2 l0.9,0.4" stroke="#4e5c3c" stroke-width="0.45" fill="none" stroke-linecap="round"/>
  <path d="M-0.6,3.6 L-0.4,6.6 M0.6,3.6 L0.4,6.6" stroke="#2f3a24" stroke-width="0.7" stroke-linecap="round"/>
  <path d="M-2.4,6.8 L2.4,6.8" stroke="#2f3a24" stroke-width="0.55" stroke-linecap="round"/>
</symbol>
<pattern id="collines" width="7" height="5.2" patternUnits="userSpaceOnUse">
  <g fill="none" stroke="#7a6a52" stroke-width="0.22" stroke-linecap="round" opacity="0.85">
    <path d="M0.2,2.2 Q1.4,-0.4 2.9,2.2"/>
    <path d="M1.9,0.9 l0.3,0.6 M2.2,1.25 l0.3,0.55 M2.5,1.65 l0.25,0.45 M1.55,0.72 l0.3,0.6"/>
    <path d="M3.6,4.9 Q4.9,2.3 6.5,4.9"/>
    <path d="M5.4,3.55 l0.3,0.6 M5.75,3.95 l0.3,0.55 M6.05,4.35 l0.25,0.45 M5.05,3.4 l0.3,0.6"/>
  </g>
</pattern>
</defs>''')

# ---------------------------------------------------------------- papier
A('<rect x="0" y="0" width="%s" height="%s" fill="#efe3c6"/>' % (fmt(W), fmt(H)))
A('<rect x="0" y="0" width="%s" height="%s" fill="#efe3c6" filter="url(#papier)"/>' % (fmt(W), fmt(H)))

# zone de carte (clip)
CX0, CY0, CX1, CY1 = MARGIN, MARGIN, W - MARGIN, H - MARGIN
A('<clipPath id="carte"><rect x="%s" y="%s" width="%s" height="%s"/></clipPath>' % (fmt(CX0), fmt(CY0), fmt(CX1 - CX0), fmt(CY1 - CY0)))
A('<g clip-path="url(#carte)">')

# hachures de rivage (côté mer) : décalages successifs du contour de la France, coupés le long des frontières terrestres
neigh_cut = neigh_p.buffer(1.2)
for i, d in enumerate([0.55, 1.25, 2.05, 2.95, 3.95]):
    ring = france_p.buffer(d, join_style="round").boundary.difference(neigh_cut)
    op = 0.55 - i * 0.09
    A('<path d="%s" fill="none" stroke="#5f7486" stroke-width="%s" opacity="%.2f"/>' % (path_of(ring, close=False), fmt(0.26 - i * 0.03), op))

# pays voisins (contour léger) et France
A('<path d="%s" fill="#ebdfc0" stroke="#8d8068" stroke-width="0.28" stroke-dasharray="1.1 0.7" opacity="0.9"/>' % path_of(neigh_p))
A('<path d="%s" fill="#f1e6c9" stroke="#2b2418" stroke-width="0.42"/>' % path_of(france_p))

# montagnes
# montagnes en taupinières : collines semées dans les massifs
def hills(geom, seed=3):
    rnd = random.Random(seed)
    out = []
    minx, miny, maxx, maxy = geom.bounds
    prepared = shapely.prepared.prep(geom)
    step = 3.1
    y = miny; row = 0
    while y <= maxy:
        x = minx + (step / 2 if row % 2 else 0)
        while x <= maxx:
            jx, jy = x + rnd.uniform(-0.9, 0.9), y + rnd.uniform(-0.7, 0.7)
            if prepared.contains(Point(jx, jy)):
                w = rnd.uniform(2.2, 3.6); h = w * rnd.uniform(0.42, 0.6)
                px, py = mm(jx, jy)
                out.append((py, px, w, h))
            x += step
        y += step * 0.8; row += 1
    out.sort()
    parts = []
    for py, px, w, h in out:
        # dos de colline, ombre hachurée à droite
        d = 'M%s,%s q%s,%s %s,0' % (fmt(px - w / 2), fmt(py), fmt(w / 2), fmt(-2 * h), fmt(w))
        hach = []
        for k in range(3):
            t = 0.55 + k * 0.14
            hx = px - w / 2 + t * w
            hy = py - 2 * h * t * (1 - t) * 1.0
            hach.append('M%s,%s l%s,%s' % (fmt(hx), fmt(hy + 0.1), fmt(0.25), fmt(py - hy - 0.15)))
        parts.append('<path d="%s" fill="#eee2c5" stroke="#6e5f49" stroke-width="0.22"/><path d="%s" stroke="#6e5f49" stroke-width="0.18" fill="none"/>' % (d, " ".join(hach)))
    return "\n".join(parts)

A('<g id="montagnes" opacity="0.8">')
A(hills(mtn_p))
A('</g>')

# rivières
A('<g fill="none" stroke="#4e6378" stroke-linecap="round" stroke-linejoin="round">')
for n, g in rivers_p.items():
    big = n in {"Loire", "Seine", "Rhône", "Garonne", "Rhin"}
    A('<path d="%s" stroke-width="%s"/>' % (path_of(g, close=False), "0.5" if big else "0.32"))
A('</g>')

# étiquettes de rivières : posées sur le tracé, tournées selon la tangente locale
A('<g class="riv">')
for n, (label, frac) in RIVER_LABELS.items():
    if n not in rivers_p:
        continue
    g = rivers_p[n]
    if isinstance(frac, tuple) and hasattr(g, "geoms"):
        pt = Point(*proj(*frac))
        line = min(g.geoms, key=lambda l: l.distance(pt))
    else:
        line = max(g.geoms, key=lambda l: l.length) if hasattr(g, "geoms") else g
    L = line.length
    if isinstance(frac, tuple):
        d0 = line.project(Point(*proj(*frac)))
    else:
        d0 = frac * L
    pA = line.interpolate(max(0, d0 - 5)); pB = line.interpolate(min(L, d0 + 5)); pm = line.interpolate(d0)
    ax, ay = mm(pA.x, pA.y); bx, by = mm(pB.x, pB.y); cx, cy = mm(pm.x, pm.y)
    ang = math.degrees(math.atan2(by - ay, bx - ax))
    if ang > 90: ang -= 180
    if ang < -90: ang += 180
    # décalage perpendiculaire (au-dessus de la rivière)
    nx, ny = -math.sin(math.radians(ang)), math.cos(math.radians(ang))
    tx, ty = cx - nx * 1.1, cy - ny * 1.1
    A('<text x="%s" y="%s" text-anchor="middle" transform="rotate(%s %s %s)">%s</text>' % (fmt(tx), fmt(ty), fmt(ang), fmt(tx), fmt(ty), esc(label)))
A('</g>')

# forêts : taches d'arbres
def patch(cx, cy, ha, seed):
    rnd = random.Random(seed)
    r = min(9.6, 2.3 + 1.15 * math.sqrt(ha / 1000.0))
    ax, ay = r * rnd.uniform(0.85, 1.2), r * rnd.uniform(0.75, 1.0)
    rot = rnd.uniform(0, math.pi)
    out = ['<ellipse cx="%s" cy="%s" rx="%s" ry="%s" transform="rotate(%s %s %s)" fill="#f1e6c9" stroke="#8a9a6d" stroke-width="0.25" stroke-dasharray="0.6 0.5"/>'
           % (fmt(cx), fmt(cy), fmt(ax + 0.9), fmt(ay + 0.9), fmt(math.degrees(rot)), fmt(cx), fmt(cy))]
    trees = []
    step = 1.55
    y = -ay - step
    row = 0
    while y <= ay + step:
        x = -ax - step + (step / 2 if row % 2 else 0)
        while x <= ax + step:
            jx, jy = x + rnd.uniform(-0.35, 0.35), y + rnd.uniform(-0.3, 0.3)
            # dans l'ellipse (après rotation inverse)
            ux = jx * math.cos(-rot) - jy * math.sin(-rot)
            uy = jx * math.sin(-rot) + jy * math.cos(-rot)
            if (ux / ax) ** 2 + (uy / ay) ** 2 <= 1.0:
                s = rnd.uniform(1.35, 1.75)
                trees.append((cx + jx, cy + jy, s))
            x += step
        y += step * 0.86
        row += 1
    trees.sort(key=lambda t: t[1])
    for tx, ty, s in trees:
        out.append('<use xlink:href="#arbre" x="%s" y="%s" width="%s" height="%s"/>' % (fmt(tx - s * 0.5), fmt(ty - s * 0.6), fmt(s), fmt(s * 1.2)))
    return "\n".join(out)

A('<g id="forets">')
for i, (name, ha, lat, lon, (dx, dy), anchor) in enumerate(FORETS):
    cx, cy = P(lon, lat)
    A(patch(cx, cy, ha, i + 1))
A('</g>')

# chênes remarquables
A('<g id="chenes">')
for name, lat, lon, (dx, dy), anchor in CHENES:
    cx, cy = P(lon, lat)
    A('<use xlink:href="#gros-chene" x="%s" y="%s" width="4.6" height="5.4"/>' % (fmt(cx - 2.3), fmt(cy - 3.6)))
A('</g>')

# villes
A('<g id="villes">')
for name, lat, lon, imp, (dx, dy), anchor in VILLES:
    cx, cy = P(lon, lat)
    if imp == 2:
        A('<circle cx="%s" cy="%s" r="1.1" fill="#efe3c6" stroke="#2b2418" stroke-width="0.4"/><circle cx="%s" cy="%s" r="0.4" fill="#2b2418"/>' % (fmt(cx), fmt(cy), fmt(cx), fmt(cy)))
    else:
        A('<circle cx="%s" cy="%s" r="0.75" fill="#efe3c6" stroke="#2b2418" stroke-width="0.35"/><circle cx="%s" cy="%s" r="0.25" fill="#2b2418"/>' % (fmt(cx), fmt(cy), fmt(cx), fmt(cy)))
A('</g>')

A('</g>')  # fin clip

# ---------------------------------------------------------------- étiquettes (hors clip, pour dépasser si besoin)
A('<g id="etiquettes">')
for name, lat, lon, imp, (dx, dy), anchor in VILLES:
    cx, cy = P(lon, lat)
    A('<text class="%s" x="%s" y="%s" text-anchor="%s">%s</text>' % ("ville2" if imp == 2 else "ville", fmt(cx + dx), fmt(cy + dy), anchor, esc(name)))
for name, ha, lat, lon, (dx, dy), anchor in FORETS:
    cx, cy = P(lon, lat)
    A('<text class="foret" x="%s" y="%s" text-anchor="%s">FORÊT DE %s</text>' % (fmt(cx + dx), fmt(cy + dy), anchor, esc(name)) if name != "LA REINE" else
      '<text class="foret" x="%s" y="%s" text-anchor="%s">FORÊT DE LA REINE</text>' % (fmt(cx + dx), fmt(cy + dy), anchor))
for name, lat, lon, (dx, dy), anchor in CHENES:
    cx, cy = P(lon, lat)
    A('<text class="chene" x="%s" y="%s" text-anchor="%s">%s</text>' % (fmt(cx + dx), fmt(cy + dy), anchor, esc(name)))
for name, lon, lat, rot in PAYS:
    cx, cy = P(lon, lat)
    A('<text class="pays" x="%s" y="%s" text-anchor="middle" transform="rotate(%s %s %s)">%s</text>' % (fmt(cx), fmt(cy), rot, fmt(cx), fmt(cy), esc(name)))
for name, lon, lat, rot in MERS:
    cx, cy = P(lon, lat)
    A('<text class="mer" x="%s" y="%s" text-anchor="middle" transform="rotate(%s %s %s)">%s</text>' % (fmt(cx), fmt(cy), rot, fmt(cx), fmt(cy), esc(name)))
A('</g>')

# ---------------------------------------------------------------- cartouche (golfe de Gascogne)
cw, ch = 76, 72
x0 = MARGIN + 6
cy = P(-4.0, 45.4)[1]
y0 = cy - ch / 2
cx = x0 + cw / 2
A('<g id="cartouche">')
A('<rect x="%s" y="%s" width="%s" height="%s" fill="#f3e9cf" stroke="#2b2418" stroke-width="0.55"/>' % (fmt(x0), fmt(y0), cw, ch))
A('<rect x="%s" y="%s" width="%s" height="%s" fill="none" stroke="#2b2418" stroke-width="0.25"/>' % (fmt(x0 + 1.4), fmt(y0 + 1.4), cw - 2.8, ch - 2.8))
# volutes d'angle
for sx, sy in [(x0, y0), (x0 + cw, y0), (x0, y0 + ch), (x0 + cw, y0 + ch)]:
    fx = 1 if sx == x0 else -1; fy = 1 if sy == y0 else -1
    A('<path d="M%s,%s c%s,%s %s,%s %s,%s c%s,%s %s,%s %s,%s" fill="none" stroke="#2b2418" stroke-width="0.45" stroke-linecap="round"/>'
      % (fmt(sx + fx * 1.4), fmt(sy + fy * 7.5), fmt(fx * 0.0), fmt(fy * -3.6), fmt(fx * 3.4), fmt(fy * -4.8), fmt(fx * 6.2), fmt(fy * -4.4),
         fmt(fx * 1.6), fmt(fy * 0.3), fmt(fx * 2.4), fmt(fy * 1.9), fmt(fx * 1.4), fmt(fy * 3.2)))
    A('<circle cx="%s" cy="%s" r="0.9" fill="none" stroke="#2b2418" stroke-width="0.35"/>' % (fmt(sx + fx * 4.2), fmt(sy + fy * 4.2)))
tx = cx
lines = [
    ("titre", 5.6, 11.0, "CARTE"),
    ("titre", 3.7, 6.2, "DES PLUS BELLES FORÊTS DE CHÊNE"),
    ("titre", 3.7, 5.4, "DU ROYAUME DE FRANCE"),
    ("carti", 2.9, 7.0, "Dressée à la manière de la Carte de Cassini"),
    ("cart", 2.6, 4.8, "pour la Collection LE GEAI, Arbres & Arbustes de France,"),
    ("cart", 2.6, 3.9, "par les soins du Jacques, Geai des chênes, l'an MMXXVI."),
    ("carti", 2.5, 6.4, "Où l'on voit les futaies de Colbert, les chênes de Lorraine"),
    ("carti", 2.5, 3.6, "et les vieux arbres que l'on visite encore."),
    ("carti", 2.3, 5.8, "Les forêts y sont figurées au-delà de leur étendue véritable,"),
    ("carti", 2.3, 3.4, "pour l'agrément de l'œil ; le lecteur voudra bien les y chercher"),
    ("carti", 2.3, 3.4, "à pied, ce qui est la seule manière de les voir."),
]
yy = y0 + 4.5
for cls, size, gap, text in lines:
    yy += gap
    A('<text class="%s" font-size="%s" x="%s" y="%s" text-anchor="middle">%s</text>' % (cls, size, fmt(tx), fmt(yy), esc(text)))
# filet
A('<path d="M%s,%s L%s,%s" stroke="#2b2418" stroke-width="0.3"/>' % (fmt(tx - 16), fmt(y0 + 29.8), fmt(tx + 16), fmt(y0 + 29.8)))
A('</g>')

# ---------------------------------------------------------------- légende et échelle (Méditerranée)
lx, ly = P(5.55, 41.93)
lw, lh = 104, 42
x0, y0 = lx - lw / 2, ly - lh / 2
A('<g id="legende">')
A('<rect x="%s" y="%s" width="%s" height="%s" fill="#f3e9cf" stroke="#2b2418" stroke-width="0.5"/>' % (fmt(x0), fmt(y0), lw, lh))
A('<rect x="%s" y="%s" width="%s" height="%s" fill="none" stroke="#2b2418" stroke-width="0.22"/>' % (fmt(x0 + 1.2), fmt(y0 + 1.2), lw - 2.4, lh - 2.4))
A('<text class="titre" font-size="3.4" x="%s" y="%s" text-anchor="middle" letter-spacing="0.8">EXPLICATION DES SIGNES</text>' % (fmt(lx), fmt(y0 + 6.2)))
# colonne gauche
gx = x0 + 6; gy = y0 + 11
A(patch(gx + 3, gy + 1.5, 1500, 99))
A('<text class="leg" x="%s" y="%s">Forêt de chêne (sélection de l\'auteur)</text>' % (fmt(gx + 10), fmt(gy + 2.5)))
A('<use xlink:href="#gros-chene" x="%s" y="%s" width="4.6" height="5.4"/>' % (fmt(gx + 0.7), fmt(gy + 6.5)))
A('<text class="leg" x="%s" y="%s">Chêne remarquable que l\'on visite</text>' % (fmt(gx + 10), fmt(gy + 10.3)))
A('<circle cx="%s" cy="%s" r="0.75" fill="#efe3c6" stroke="#2b2418" stroke-width="0.35"/><circle cx="%s" cy="%s" r="0.25" fill="#2b2418"/>' % (fmt(gx + 3), fmt(gy + 16.3), fmt(gx + 3), fmt(gy + 16.3)))
A('<text class="leg" x="%s" y="%s">Ville</text>' % (fmt(gx + 10), fmt(gy + 17.2)))
# colonne droite
rx = x0 + 64; ry = y0 + 11
A('<path d="M%s,%s c3,-1.5 5,1.5 8,0" fill="none" stroke="#4e6378" stroke-width="0.45"/>' % (fmt(rx), fmt(ry + 1.8)))
A('<text class="leg" x="%s" y="%s">Rivière</text>' % (fmt(rx + 11), fmt(ry + 2.5)))
A('<rect x="%s" y="%s" width="8" height="5" fill="url(#collines)" stroke="none"/>' % (fmt(rx), fmt(ry + 5.4)))
A('<text class="leg" x="%s" y="%s">Montagnes</text>' % (fmt(rx + 11), fmt(ry + 9)))
# échelle : 50 lieues de poste de 2000 toises (3,898 km) = 194,9 km
L = 50 * 3.898 * KM2MM
sx, sy = x0 + 8, y0 + 35.0
A('<text class="leg" font-style="italic" x="%s" y="%s">Échelle de cinquante lieues de poste, de deux mille toises chacune</text>' % (fmt(sx), fmt(sy - 1.6)))
A('<rect x="%s" y="%s" width="%s" height="1.3" fill="none" stroke="#2b2418" stroke-width="0.3"/>' % (fmt(sx), fmt(sy), fmt(L)))
for k in range(5):
    if k % 2 == 0:
        A('<rect x="%s" y="%s" width="%s" height="1.3" fill="#2b2418"/>' % (fmt(sx + k * L / 5), fmt(sy), fmt(L / 5)))
    A('<text class="leg" font-size="2.2" x="%s" y="%s" text-anchor="middle">%d</text>' % (fmt(sx + k * L / 5), fmt(sy + 4.0), k * 10))
A('<text class="leg" font-size="2.2" x="%s" y="%s" text-anchor="middle">50</text>' % (fmt(sx + L), fmt(sy + 4.0)))
A('<text class="leg" font-size="2.1" font-style="italic" x="%s" y="%s">soit environ 195 kilomètres</text>' % (fmt(sx + L + 5), fmt(sy + 1.2)))
A('</g>')

# ---------------------------------------------------------------- rose des vents (Manche, au large de la Bretagne)
rx, ry = P(-4.7, 50.35)
R = 14
A('<g id="rose" transform="translate(%s %s)">' % (fmt(rx), fmt(ry)))
A('<circle r="%s" fill="none" stroke="#2b2418" stroke-width="0.3"/><circle r="%s" fill="none" stroke="#2b2418" stroke-width="0.2"/>' % (R, R - 1.6))
pts = []
for k in range(32):
    ang = k * math.pi / 16
    rr = R - 2.2 if k % 8 == 0 else (R * 0.68 if k % 4 == 0 else (R * 0.42 if k % 2 == 0 else R * 0.22))
    pts.append((rr * math.sin(ang), -rr * math.cos(ang)))
A('<path d="%s Z" fill="#f3e9cf" stroke="#2b2418" stroke-width="0.3"/>' % " ".join(("M" if i == 0 else "L") + fmt(x) + "," + fmt(y) for i, (x, y) in enumerate(pts)))
# moitiés ombrées des quatre pointes principales
for k in range(4):
    ang = k * math.pi / 2
    tip = ((R - 2.2) * math.sin(ang), -(R - 2.2) * math.cos(ang))
    side = (R * 0.22 * math.sin(ang + math.pi / 16), -R * 0.22 * math.cos(ang + math.pi / 16))
    A('<path d="M0,0 L%s,%s L%s,%s Z" fill="#2b2418"/>' % (fmt(tip[0]), fmt(tip[1]), fmt(side[0]), fmt(side[1])))
# fleur de lis au nord
A('<g transform="translate(0 %s) scale(0.42)"><path d="M0,-9 C-1.5,-5 -1.5,-2 0,1 C1.5,-2 1.5,-5 0,-9 Z M-5,-2 C-7,0 -5,3 -2,2 C-3,0 -2,-1 -5,-2 Z M5,-2 C7,0 5,3 2,2 C3,0 2,-1 5,-2 Z M-3,3 L3,3 L2.4,5 L-2.4,5 Z M-1,5 L1,5 L1.4,8 L-1.4,8 Z" fill="#2b2418"/></g>' % fmt(-R - 1.0))
A('</g>')

# ---------------------------------------------------------------- cadre
A('<rect x="%s" y="%s" width="%s" height="%s" fill="none" stroke="#2b2418" stroke-width="1.1"/>' % (fmt(MARGIN - 2.2), fmt(MARGIN - 2.2), fmt(W - 2 * MARGIN + 4.4), fmt(H - 2 * MARGIN + 4.4)))
A('<rect x="%s" y="%s" width="%s" height="%s" fill="none" stroke="#2b2418" stroke-width="0.35"/>' % (fmt(MARGIN), fmt(MARGIN), fmt(W - 2 * MARGIN), fmt(H - 2 * MARGIN)))
# graduations de latitude et de longitude (tous les degrés) sur le cadre
for lat in range(42, 52):
    for lon_edge in (LON_W, LON_E):
        x, y = P(lon_edge, lat)
        xe = MARGIN if lon_edge == LON_W else W - MARGIN
        A('<path d="M%s,%s L%s,%s" stroke="#2b2418" stroke-width="0.3"/>' % (fmt(xe - (1.4 if lon_edge == LON_W else 0)), fmt(y), fmt(xe + (0 if lon_edge == LON_W else 1.4)), fmt(y)))
        A('<text class="lbl" font-size="2.2" x="%s" y="%s" text-anchor="%s" fill="#2b2418">%d°</text>' % (fmt(xe - 2.2 if lon_edge == LON_W else xe + 2.2), fmt(y + 0.8), "end" if lon_edge == LON_W else "start", lat))
for lon in range(-5, 11):
    for lat_edge in (LAT_S, LAT_N):
        x, y = P(lon, lat_edge)
        ye = H - MARGIN if lat_edge == LAT_S else MARGIN
        A('<path d="M%s,%s L%s,%s" stroke="#2b2418" stroke-width="0.3"/>' % (fmt(x), fmt(ye), fmt(x), fmt(ye + (1.4 if lat_edge == LAT_S else -1.4))))
        label = "%d°" % lon if lon != 0 else "0° (Greenwich)"
        A('<text class="lbl" font-size="2.2" x="%s" y="%s" text-anchor="middle" fill="#2b2418">%s</text>' % (fmt(x), fmt(ye + 4.0 if lat_edge == LAT_S else ye - 2.4), label))
# méridien de Paris
xp0 = P(LON0, LAT_N); xp1 = P(LON0, LAT_S)
A('<path d="M%s,%s L%s,%s" stroke="#2b2418" stroke-width="0.25" stroke-dasharray="2 1.2" opacity="0.6"/>' % (fmt(xp0[0]), fmt(xp0[1]), fmt(xp1[0]), fmt(xp1[1])))
A('<text class="carti" font-size="2.3" x="%s" y="%s" text-anchor="middle" transform="rotate(-90 %s %s)">Méridien de Paris</text>' % (fmt(xp1[0] - 1.6), fmt(xp1[1] - 22), fmt(xp1[0] - 1.6), fmt(xp1[1] - 22)))
# mention en pied
A('<text class="carti" font-size="2.2" x="%s" y="%s" text-anchor="end">Projection de Cassini sur le méridien de Paris · 1 : 4 000 000 · tracés d\'après IGN-Admin Express et Natural Earth · dessinée pour Le Geai, 2026</text>' % (fmt(W - MARGIN + 2.2), fmt(H - 2.6)))

A('</svg>')
open(OUT_SVG, "w", encoding="utf-8").write("\n".join(svg))
print("OK", OUT_SVG, "page %.0f x %.0f mm" % (W, H), "forêts", len(FORETS), "rivières", sorted(rivers_p))
