# -*- coding: utf-8 -*-
"""Figures de données du tome 1 dessinées en vectoriel (matplotlib), au gabarit de la collection :
cartes schématiques, échelle des vies, chromosomes, graphique de l'inventaire. Ces figures ne sont pas
générées par Magnific : une carte ou un graphique doivent être exacts, pas plausibles.

Sorties (PNG 2 000 px de large + PDF vectoriel) dans tomes/01-le-chene/images/ :
    p06-07-carte-deux-chenes      — présence du pédonculé et du sessile par département (schéma indicatif)
    p36-echelle-des-vies          — longévité et première fructification des 25 espèces de la collection
    p46-europe-refuges            — refuges glaciaires et remontée post-glaciaire du chêne
    p47-france-trois-chenes       — aires indicatives des trois chênes et essais de migration assistée
    p50-carte-toponymes           — quelques noms de lieux du chêne (cassanos, robur, garric)
    p51-chromosomes               — les douze chromosomes du chêne pédonculé, schéma
    p52-graphique-ign             — mortalité et dépérissement d'après l'IGN

Données géographiques (non versionnées, ~10 Mo) : GEO_DIR (défaut /tmp/geo) doit contenir
ne_50m_admin_0_countries.geojson (Natural Earth) et departements.geojson, regions.geojson (france-geojson).
Les aires de présence par département sont une transcription indicative des cartes IGN/MFR, à vérifier
avant maquette finale ; les figures le disent en pied.
"""
import json
import math
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import Polygon as MplPolygon, FancyArrowPatch, Circle
from matplotlib.collections import PatchCollection
from shapely.geometry import shape, Polygon, MultiPolygon, box

REPO = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
OUT = os.path.join(REPO, "tomes", "01-le-chene", "images")
GEO = os.environ.get("GEO_DIR", "/tmp/geo")
os.makedirs(OUT, exist_ok=True)

# ---- polices et couleurs de la collection
FD = "/usr/share/fonts/truetype/crosextra/"
for f in ("Carlito-Regular.ttf", "Carlito-Bold.ttf", "Carlito-Italic.ttf", "Caladea-Regular.ttf", "Caladea-Italic.ttf"):
    if os.path.exists(FD + f):
        font_manager.fontManager.addfont(FD + f)
plt.rcParams["font.family"] = "Carlito"
GREEN, GREEN_L, OCHRE, OCHRE_L = "#2E5339", "#B9CDB4", "#8F6418", "#E6D3A8"
GREY, GREY_L, DARK, RED, BLUE, ICE = "#6A6A66", "#D9DBD4", "#222222", "#A3392B", "#3C6E9C", "#EAF2F7"
NOTE = dict(fontsize=8, color=GREY, style="italic")


def save(fig, name):
    for ext in ("png", "pdf"):
        fig.savefig(os.path.join(OUT, name + "." + ext), dpi=150 if ext == "png" else None,
                    bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("OK", name)


def geoms(path, keyname=None):
    with open(path, encoding="utf-8") as fh:
        gj = json.load(fh)
    out = {}
    for ft in gj["features"]:
        key = ft["properties"].get(keyname) if keyname else ft["properties"].get("ADMIN", ft["properties"].get("nom"))
        out[key] = shape(ft["geometry"])
    return out


def draw_geom(ax, geom, **kw):
    polys = geom.geoms if isinstance(geom, MultiPolygon) else [geom]
    for p in polys:
        ax.add_patch(MplPolygon(list(p.exterior.coords), closed=True, **kw))
        for ring in p.interiors:
            ax.add_patch(MplPolygon(list(ring.coords), closed=True, facecolor="white", edgecolor="none"))


def france_axes(ax):
    ax.set_xlim(-5.4, 9.8); ax.set_ylim(41.2, 51.4)
    ax.set_aspect(1 / math.cos(math.radians(46.5)))
    ax.axis("off")


# ---- présence par département (schéma indicatif, à vérifier sur les cartes IGN / fiches MFR)
MEDITERRANEE = {"06", "83", "13", "84", "30", "34", "11", "66", "2A", "2B"}
PEDONCULE_ABSENT = MEDITERRANEE | {"04", "05"}
SESSILE_ABSENT = MEDITERRANEE | {"04", "05", "29", "40", "64", "65"}
PUBESCENT_PRESENT = MEDITERRANEE | {"04", "05", "26", "07", "48", "12", "81", "82", "31", "32", "09", "65", "64", "47",
                                    "46", "24", "19", "15", "43", "42", "69", "01", "38", "73", "74", "39", "25", "21",
                                    "71", "58", "89", "10", "52", "70", "90", "68", "67", "54", "55", "57", "16", "17",
                                    "86", "36", "18", "03", "63", "87", "33", "40"}


def fig_carte_deux_chenes():
    deps = geoms(os.path.join(GEO, "departements.geojson"), "code")
    fig, ax = plt.subplots(figsize=(7.2, 7.2))
    france_axes(ax)
    for code, g in deps.items():
        if code.startswith("97"):
            continue
        ped = code not in PEDONCULE_ABSENT
        ses = code not in SESSILE_ABSENT
        if ped and ses:
            draw_geom(ax, g, facecolor=GREEN, edgecolor="white", linewidth=0.4, alpha=0.85)
        elif ped:
            draw_geom(ax, g, facecolor=GREEN_L, edgecolor="white", linewidth=0.4)
        elif ses:
            draw_geom(ax, g, facecolor=GREEN, edgecolor="white", linewidth=0.4, alpha=0.5)
        else:
            draw_geom(ax, g, facecolor="#F1F1EC", edgecolor="white", linewidth=0.4)
    ax.plot([6.2], [48.7], marker="o", ms=7, color=RED, mec="white", mew=1.2)
    ax.text(6.2, 48.35, "[lieu de l'individu suivi]", fontsize=8.5, color=RED, ha="center", va="top")
    ax.add_patch(plt.Rectangle((-5.1, 42.0), 0.45, 0.32, facecolor=GREEN_L)); ax.text(-4.5, 42.16, "pédonculé seul", fontsize=9, va="center")
    ax.add_patch(plt.Rectangle((-5.1, 41.55), 0.45, 0.32, facecolor=GREEN, alpha=0.85)); ax.text(-4.5, 41.71, "pédonculé et sessile", fontsize=9, va="center")
    ax.add_patch(plt.Rectangle((-1.9, 42.0), 0.45, 0.32, facecolor="#F1F1EC", edgecolor=GREY_L)); ax.text(-1.3, 42.16, "ni l'un ni l'autre (ou rares)", fontsize=9, va="center")
    ax.text(-5.3, 51.25, "Schéma indicatif par département, d'après les cartes de l'inventaire forestier — à vérifier avant maquette finale.", **NOTE)
    save(fig, "p06-07-carte-deux-chenes")


def fig_echelle_des_vies():
    rows = [  # (espèce, tome, première fructification min, longévité courante max, maximum connu ou None)
        ("Chêne pédonculé / sessile", 1, 20, 800, 1000), ("Sapin pectiné", 2, 30, 500, 600), ("Épicéa commun", 3, 30, 500, 600),
        ("Douglas", 4, 15, 1000, 1200), ("Pin sylvestre", 5, 15, 400, 600), ("Chêne pubescent", 6, 30, 500, None),
        ("Charme", 7, 20, 200, 300), ("Hêtre", 8, 40, 300, 500), ("Frêne", 9, 20, 250, 300),
        ("Châtaignier", 10, 20, 1000, 1500), ("Chêne vert", 11, 15, 500, 1000), ("Pin maritime", 12, 10, 300, None),
        ("Fusain", 13, 5, 100, None), ("Houx", 14, 10, 300, 500), ("Noisetier", 15, 5, 80, None),
        ("Cornouiller sanguin", 16, 5, 80, None), ("Buis", 17, 10, 600, None), ("Prunellier", 18, 5, 100, None),
        ("Genêt à balais", 19, 2, 15, 25), ("Aubépine monogyne", 20, 10, 500, 700), ("Troène", 21, 5, 100, None),
        ("Bourdaine", 22, 5, 60, None), ("Églantier", 23, 3, 100, None), ("Sureau noir", 24, 3, 80, 100), ("Lierre", 25, 10, 500, 1000),
    ]
    fig, ax = plt.subplots(figsize=(8.4, 8.6))
    ax.set_xscale("log"); ax.set_xlim(1, 2000)
    n = len(rows)
    for i, (nom, tome, f1, lc, mx) in enumerate(rows):
        y = n - i
        col = GREEN if tome == 1 else GREY_L
        ax.barh(y, lc - f1, left=f1, height=0.62, color=col, edgecolor="none")
        if mx:
            ax.plot([lc, mx], [y, y], color=GREEN if tome == 1 else GREY, lw=1.1, ls=(0, (1.5, 2.5)))
        ax.plot([f1], [y], marker="|", ms=11, color=DARK if tome == 1 else GREY, mew=1.4)
        ax.text(0.93, y, "%s  (t. %d)" % (nom, tome), ha="right", va="center", fontsize=9,
                color=DARK if tome == 1 else GREY, fontweight="bold" if tome == 1 else "normal")
    ax.set_ylim(0.3, n + 0.8); ax.set_yticks([])
    ax.set_xticks([1, 2, 5, 10, 20, 50, 100, 200, 500, 1000]); ax.set_xticklabels(["1", "2", "5", "10", "20", "50", "100", "200", "500", "1 000"], fontsize=8.5)
    ax.set_xlabel("années (échelle logarithmique)", fontsize=9, color=GREY)
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color(GREY)
    ax.grid(axis="x", color=GREY_L, lw=0.5)
    ax.set_axisbelow(True)
    ax.set_ylim(0.3, n + 1.6)
    ax.text(1.05, n + 1.1, "trait : première graine  ·  barre : vie courante  ·  pointillé : record connu ou revendiqué",
            fontsize=8.5, color=GREY, style="italic")
    fig.text(0.125, 0.01, "Valeurs indicatives (annexe A du chemin de fer), à confirmer espèce par espèce ; les records sont rarement mesurés. "
             "Le chêne en couleur du tome ; les autres se coloreront au fil des parutions.", **NOTE)
    save(fig, "p36-echelle-des-vies")


def fig_europe():
    countries = geoms(os.path.join(GEO, "ne_50m_admin_0_countries.geojson"))
    fig, ax = plt.subplots(figsize=(8.4, 7.4))
    ax.set_xlim(-12, 36); ax.set_ylim(34, 66); ax.set_aspect(1 / math.cos(math.radians(50))); ax.axis("off")
    win = box(-12, 34, 36, 66)
    land = None
    for g in countries.values():
        try:
            c = g.intersection(win)
        except Exception:
            continue
        if c.is_empty:
            continue
        land = c if land is None else land.union(c)
    # steppe froide : toute la terre émergée en ocre très pâle
    draw_geom(ax, land, facecolor="#F3EAD6", edgecolor="#B8AD93", linewidth=0.5)
    # calotte glaciaire du dernier maximum (tracé schématique)
    ice = Polygon([(-12, 51.5), (-5.5, 51.3), (0.5, 52.8), (8, 53.4), (13, 52.4), (20, 51.8), (28, 52.5), (36, 56), (36, 66), (-12, 66)])
    draw_geom(ax, ice.intersection(box(-12, 34, 36, 66)), facecolor=ICE, edgecolor=BLUE, linewidth=0.9, alpha=0.95)
    ax.text(10, 60, "glace", fontsize=11, color=BLUE, ha="center", style="italic")
    ax.text(2, 46.2, "steppe froide", fontsize=10, color="#8A7A55", ha="center", style="italic")
    # refuges
    for (x, y, lab, dx, ha) in [(-3.5, 37.3, "refuge ibérique", 2.2, "left"), (16.2, 39.6, "refuge italien", -2.2, "right"),
                                (21.5, 39.8, "refuge balkanique", 2.2, "left")]:
        ax.plot([x], [y], marker="o", ms=26, color=GREEN, alpha=0.9, mec="none")
        ax.text(x + dx, y, lab, fontsize=8.5, color=GREEN, ha=ha, va="center")
    # flèches de la remontée (deux temps)
    def arrow(p0, p1, rad, txt=None, tpos=None):
        a = FancyArrowPatch(p0, p1, connectionstyle="arc3,rad=%.2f" % rad, arrowstyle="-|>,head_length=6,head_width=3",
                            color=GREEN, lw=1.6)
        ax.add_patch(a)
        if txt:
            ax.text(tpos[0], tpos[1], txt, fontsize=8, color=GREEN, ha="center",
                    bbox=dict(boxstyle="round,pad=0.15", facecolor="white", edgecolor="none", alpha=0.8))
    arrow((-3.2, 39), (-1, 46), 0.25, "il y a 13 000 à 11 000 ans", (-6.5, 43.2))
    arrow((16, 41.2), (12, 47), -0.2)
    arrow((21.5, 41.4), (22, 47.5), 0.1)
    arrow((-1, 46.5), (0.5, 52), 0.15, "puis vers le nord,\n500 m par an en moyenne,\njusqu'à 1 000", (-8.5, 50.5))
    arrow((12, 47.5), (12.5, 52.8), -0.1)
    arrow((22, 48), (24, 52), 0.05, "il y a 6 000 ans :\naire actuelle atteinte", (29, 49))
    # le lieu
    ax.plot([6.2], [48.7], marker="o", ms=9, mfc="none", mec=RED, mew=2)
    ax.text(7.2, 48.4, "[lieu]", fontsize=9, color=RED)
    ax.text(-11.5, 65.2, "Schéma d'après Brewer et al. 2002 et Petit et al. 2002 (pollen fossile, ADN des chloroplastes) ; limite des glaces simplifiée.", **NOTE)
    save(fig, "p46-europe-refuges")


def fig_france_trois_chenes():
    deps = geoms(os.path.join(GEO, "departements.geojson"), "code")
    fig, axes = plt.subplots(1, 3, figsize=(12.6, 4.9))
    specs = [("Chêne pédonculé", lambda c: c not in PEDONCULE_ABSENT, GREEN_L),
             ("Chêne sessile", lambda c: c not in SESSILE_ABSENT, GREEN),
             ("Chêne pubescent", lambda c: c in PUBESCENT_PRESENT, OCHRE_L)]
    for ax, (titre, test, col) in zip(axes, specs):
        france_axes(ax)
        for code, g in deps.items():
            if code.startswith("97"):
                continue
            draw_geom(ax, g, facecolor=col if test(code) else "#F4F4F0", edgecolor="white", linewidth=0.35,
                      alpha=0.9 if test(code) else 1)
        ax.set_title(titre, fontsize=12, color=DARK, pad=4)
    # flèches du déplacement attendu (pubescent vers le nord ; pédonculé qui recule au sud-ouest)
    ax = axes[2]
    for x in (1.5, 4.0, 6.5):
        ax.add_patch(FancyArrowPatch((x, 45.2), (x, 48.3), arrowstyle="-|>,head_length=7,head_width=3.5", color=OCHRE, lw=1.8))
    ax.text(2.0, 49.3, "attendu plus au nord", fontsize=9, color=OCHRE, ha="center")
    for (x, y, lab) in [(5.38, 49.16, "Verdun"), (2.70, 46.65, "Tronçais")]:
        ax.plot([x], [y], marker="o", ms=6, color=GREEN, mec="white", mew=1)
        ax.text(x + 0.25, y, lab, fontsize=8.5, color=GREEN, va="center")
    ax.text(-5.2, 41.5, "points : essais de migration assistée (ONF)", fontsize=8.5, color=GREEN)
    ax = axes[0]
    ax.add_patch(FancyArrowPatch((0.5, 44.0), (-0.5, 46.5), arrowstyle="-|>,head_length=7,head_width=3.5", color=RED, lw=1.6))
    ax.text(-4.9, 43.0, "recul attendu\nau sud-ouest", fontsize=8.5, color=RED)
    fig.text(0.5, 0.02, "Aires de présence indicatives par département, transcrites des cartes de l'inventaire forestier et des fiches MFR — à vérifier avant maquette finale ; "
             "les flèches donnent le sens, pas la date.", ha="center", **NOTE)
    save(fig, "p47-france-trois-chenes")


def fig_toponymes():
    regs = geoms(os.path.join(GEO, "regions.geojson"), "code")
    fig, ax = plt.subplots(figsize=(7.2, 7.0))
    france_axes(ax)
    for code, g in regs.items():
        if code in ("01", "02", "03", "04", "06"):
            continue
        draw_geom(ax, g, facecolor="#F6F6F2", edgecolor="#C9CCC3", linewidth=0.5)
    villes = [  # nom, lon, lat, racine
        ("Le Chesnay", 2.12, 48.82, "cassanos"), ("Le Quesnoy", 3.64, 50.25, "cassanos"), ("Chassagne-Montrachet", 4.74, 46.93, "cassanos"),
        ("Cassagnes-Bégonhès", 2.65, 44.17, "cassanos"), ("Cassagnes", 2.67, 42.74, "cassanos"), ("Chenay", -0.46, 47.98, "cassanos"),
        ("Chênehutte", -0.15, 47.30, "cassanos"), ("Le Chesne", 4.77, 49.51, "cassanos"),
        ("Rouvray", 4.11, 47.43, "robur"), ("Rouvres-en-Plaine", 5.15, 47.26, "robur"), ("Rouvroy", 2.90, 50.39, "robur"),
        ("Rouvroy", 3.32, 49.83, "robur"), ("Saint-Étienne-du-Rouvray", 1.10, 49.38, "robur"), ("Rouvres", 1.45, 48.63, "robur"),
        ("la garrigue", 3.90, 43.75, "garric"), ("Garrigues", 2.30, 43.95, "garric"), ("Garrigues", 4.10, 43.95, "garric"),
    ]
    col = {"cassanos": GREEN, "robur": "#6B4A1E", "garric": OCHRE}
    for nom, x, y, r in villes:
        ax.plot([x], [y], marker="o", ms=6.5, color=col[r], mec="white", mew=0.8)
        ax.text(x + 0.14, y + 0.05, nom, fontsize=7.8, color=col[r])
    for i, (r, lab) in enumerate([("cassanos", "cassanos, le gaulois → chêne, chesne, casse"), ("robur", "robur, le latin → rouvre"), ("garric", "garric, le mot du Midi → garrigue")]):
        ax.plot([-5.0], [42.3 - 0.42 * i], marker="o", ms=7, color=col[r], mec="white")
        ax.text(-4.7, 42.3 - 0.42 * i, lab, fontsize=9, va="center", color=col[r])
    ax.text(6.0, 48.7, "[noms lorrains : à fournir]", fontsize=8.5, color=RED)
    ax.text(-5.3, 51.25, "Quelques exemples parmi des centaines (Dauzat & Rostaing ; Nègre) — carte d'illustration, à compléter avec les noms de la région.", **NOTE)
    save(fig, "p50-carte-toponymes")


def fig_chromosomes():
    # longueurs relatives indicatives des 12 chromosomes du chêne pédonculé (Plomion et al. 2018), ordre Qrob_Chr01..12
    L = [56, 116, 57, 44, 70, 57, 52, 71, 51, 52, 52, 38]
    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    import random
    random.seed(2018)
    for i, l in enumerate(L):
        x = i + 1
        ax.add_patch(plt.Rectangle((x - 0.22, 0), 0.44, l, facecolor=GREY_L, edgecolor=GREY, linewidth=0.8, joinstyle="round"))
        # mutations somatiques : positions indicatives
        for _ in range(random.choice([1, 1, 2, 2, 3])):
            y = random.uniform(3, l - 3)
            ax.plot([x - 0.22, x + 0.22], [y, y], color=RED, lw=1.6)
        if x in (3, 10):  # régions de résistance à l'oïdium (Bartholomé et al. 2020)
            y0 = l * (0.55 if x == 3 else 0.25)
            ax.add_patch(plt.Rectangle((x - 0.22, y0), 0.44, l * 0.16, facecolor=BLUE, edgecolor="none", alpha=0.9))
        ax.text(x, -4, str(x), ha="center", va="top", fontsize=9, color=GREY)
    ax.set_xlim(0.3, 12.7); ax.set_ylim(-14, 125); ax.axis("off")
    ax.plot([10.3, 10.7], [116, 116], color=RED, lw=1.6); ax.text(10.85, 116, "mutations apparues dans une branche d'un vieil arbre", fontsize=8.5, va="center", color=RED)
    ax.add_patch(plt.Rectangle((10.3, 104), 0.4, 5, facecolor=BLUE)); ax.text(10.85, 106.5, "régions liées à la résistance à l'oïdium", fontsize=8.5, va="center", color=BLUE)
    ax.text(0.3, -12, "Schéma redessiné d'après Plomion et al. 2018 et Bartholomé et al. 2020 : longueurs et positions indicatives, pas une carte génétique.", **NOTE)
    save(fig, "p51-chromosomes")


def fig_graphique_ign():
    fig, (ax, ins) = plt.subplots(1, 2, figsize=(10.5, 4.8), gridspec_kw=dict(width_ratios=[1.35, 1], wspace=0.45))
    periods = ["2005-2013", "2013-2021", "2015-2024"]
    vals = [7.4, 13.1, None]
    ax.bar([0, 1], vals[:2], width=0.58, color=GREEN, edgecolor="none")
    ax.bar([2], [7.4 * 2.25], width=0.58, color="white", edgecolor=GREEN, hatch="////", linewidth=1.2)
    for i, v in enumerate(vals[:2]):
        ax.text(i, v + 0.35, "%s millions de m³ par an" % str(v).replace(".", ","), ha="center", fontsize=9.5, color=DARK)
    ax.text(2, 7.4 * 2.25 + 0.35, "+ 125 % en dix ans\n(IGN, octobre 2025 ; hauteur indicative)", ha="center", fontsize=9, color=GREEN)
    ax.set_xticks([0, 1, 2]); ax.set_xticklabels(periods, fontsize=10)
    ax.set_ylim(0, 21); ax.set_yticks([]); ax.set_title("Volume d'arbres morts chaque année\nen forêt française", fontsize=12, color=DARK, loc="left")
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color(GREY)
    # second panneau : part d'arbres avec symptômes, campagne 2025
    ess = ["frêne", "châtaignier", "chêne pédonculé", "épicéa"]
    pc = [26, 21, 10, 10]
    cols = [GREY_L, GREY_L, GREEN, GREY_L]
    ins.barh(range(4)[::-1], pc, color=cols, height=0.6)
    for i, v in enumerate(pc):
        ins.text(v + 0.8, 3 - i, "%d %%" % v, va="center", fontsize=8.5, color=DARK)
    ins.set_yticks(range(4)[::-1]); ins.set_yticklabels(ess, fontsize=8.5); ins.set_xticks([]); ins.set_xlim(0, 34)
    for s in ("top", "right", "bottom"):
        ins.spines[s].set_visible(False)
    ins.set_title("Arbres avec symptômes\nde dépérissement, campagne 2025", fontsize=12, color=DARK, loc="left")
    fig.text(0.125, -0.04, "Chiffres IGN : Mémento 2023 (7,4 puis 13,1 Mm³/an) ; résultats 2025 (+ 125 % en dix ans ; 26 %, 21 %, 10 %, 10 %). Cités avec leur année.", **NOTE)
    save(fig, "p52-graphique-ign")


if __name__ == "__main__":
    fig_carte_deux_chenes()
    fig_echelle_des_vies()
    fig_europe()
    fig_france_trois_chenes()
    fig_toponymes()
    fig_chromosomes()
    fig_graphique_ign()
