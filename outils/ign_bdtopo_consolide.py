# -*- coding: utf-8 -*-
"""Consolide les comptages BD TOPO (IGN) relevés via le MCP Géoplateforme (WFS, result_type=hits)
en un tableau par département : nombre d'objets « Forêt fermée de feuillus », surface, densité.

Entrée  : tomes/01-le-chene/donnees/bdtopo_hits_raw.jsonl  (une ligne par appel WFS réussi, relevé le 9 novembre 2026)
          GEO_DIR/departements.geojson (IGN Admin Express via france-geojson) pour les surfaces
Sortie  : tomes/01-le-chene/donnees/bdtopo-petits-bois-departements.json

Méthode. Pour chaque département métropolitain, le nombre d'objets de la couche BDTOPO_V3:zone_de_vegetation
de nature « Forêt fermée de feuillus » dont la géométrie intersecte le département (ADMINEXPRESS-COG.LATEST).
Quand la géométrie du département est trop lourde pour le service (côtes découpées : 06, 13, 17, 22, 29, 30, 2A, 2B,
50, 56, 83, 85), le compte est la somme des arrondissements, ou des cantons, qui le composent : un bois à cheval
sur deux unités est alors compté deux fois (léger surcompte, de l'ordre du pour cent). Trois départements restent
incomplets parce que certains cantons côtiers n'ont pas pu être servis non plus : Finistère (Crozon, Douarnenez,
Saint-Renan manquent), Var (Hyères manque) ; la Corse-du-Sud, à qui il manque deux grands cantons (Sevi-Sorru-Cinarca,
Grand Sud), n'est pas cartographiée.

Ce que mesure ce compte : un nombre d'objets cartographiques (de bois distincts, en gros), pas une surface
ni une composition en essences. Il décrit le morcellement de la forêt feuillue — la France des petits bois —
et c'est à ce titre qu'il figure page 53.
"""
import json
import math
import os
from collections import defaultdict

from shapely.geometry import shape
from shapely.ops import transform

REPO = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
DON = os.path.join(REPO, "tomes", "01-le-chene", "donnees")
GEO = os.environ.get("GEO_DIR", "/tmp/geo")
RAW = os.path.join(DON, "bdtopo_hits_raw.jsonl")
OUT = os.path.join(DON, "bdtopo-petits-bois-departements.json")

INCOMPLETS = {  # code : unités manquantes (le service WFS n'a pas pu servir leur géométrie)
    "29": ["canton de Crozon", "canton de Douarnenez", "canton de Saint-Renan"],
    "83": ["canton d'Hyères"],
    "2A": ["canton de Sevi-Sorru-Cinarca", "canton Grand Sud"],
}
NON_CARTOGRAPHIES = {"2A"}
SURCOMPTE = {  # unités partagées comptées en entier (surcompte) ou parts non comptées (sous-compte)
    "22": "canton de Bégard (partagé avec l'arrondissement de Guingamp) compté deux fois en partie",
    "85": "parts des cantons de Challans et de Mareuil-sur-Lay situées dans l'arrondissement des Sables non comptées",
}

R = 6371.0088  # rayon moyen terrestre, km


def sinusoidal(lon, lat, lon0=2.5):
    """Projection sinusoïdale (équivalente) : les surfaces sont conservées."""
    lam = math.radians(lon - lon0)
    phi = math.radians(lat)
    return R * lam * math.cos(phi), R * phi


def area_km2(geom):
    return transform(lambda x, y, z=None: sinusoidal(x, y), geom).area


def main():
    rows = [json.loads(l) for l in open(RAW, encoding="utf-8") if l.strip()]
    deps = {}
    with open(os.path.join(GEO, "departements.geojson"), encoding="utf-8") as fh:
        for ft in json.load(fh)["features"]:
            p = ft["properties"]
            deps[p["code"]] = (p["nom"], shape(ft["geometry"]))
    feuil_dep = {r["code"]: r["hits"] for r in rows if r["nature"] == "feuil" and r["fid"].startswith("departement.")}
    conif_dep = {r["code"]: r["hits"] for r in rows if r["nature"] == "conif" and r["fid"].startswith("departement.")}
    sub = defaultdict(list)
    for r in rows:
        if r["nature"] == "feuil" and not r["fid"].startswith("departement."):
            sub[r["code"]].append(r)
    out = []
    for code, (nom, g) in sorted(deps.items()):
        if code.startswith("97"):
            continue
        a = area_km2(g)
        rec = dict(code=code, nom=nom, surface_km2=round(a, 1))
        if code in feuil_dep:
            rec.update(feuillus=feuil_dep[code], methode="département", unites=1)
        elif sub.get(code):
            units = sub[code]
            kinds = sorted({u["fid"].split(".")[0] for u in units})
            rec.update(feuillus=sum(u["hits"] for u in units), methode="somme des " + " et ".join(kinds) + "s",
                       unites=len(units))
        else:
            rec.update(feuillus=None, methode="non relevé", unites=0)
        if code in conif_dep:
            rec["coniferes"] = conif_dep[code]
        rec["complet"] = code not in INCOMPLETS
        if code in INCOMPLETS:
            rec["manque"] = INCOMPLETS[code]
        if code in SURCOMPTE:
            rec["remarque"] = SURCOMPTE[code]
        rec["cartographie"] = code not in NON_CARTOGRAPHIES and rec["feuillus"] is not None
        if rec["feuillus"] is not None:
            rec["densite_100km2"] = round(rec["feuillus"] / a * 100, 1)
        out.append(rec)
    meta = dict(
        source="IGN, BD TOPO v3, couche zone_de_vegetation (nature = « Forêt fermée de feuillus ») ; découpage ADMINEXPRESS-COG.LATEST",
        acces="MCP Géoplateforme (geocontext_ign), outil gpf_wfs_get_features, result_type = hits, spatial_operator = intersects_feature",
        date_releve="2026-11-09",
        mesure="nombre d'objets dont la géométrie intersecte l'unité administrative — compte d'objets, pas de surface",
        surfaces="calculées sur les contours Admin Express (france-geojson), projection sinusoïdale, rayon terrestre moyen",
        total_couche_objets=13868344,
        avertissement="les appels dont le service a rejeté la géométrie renvoient le total de la couche (13 868 344) : ces réponses ont été écartées",
    )
    json.dump(dict(meta=meta, departements=out), open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    done = [r for r in out if r["feuillus"] is not None]
    print("départements renseignés :", len(done), "/", len(out))
    for r in sorted(done, key=lambda r: -r["densite_100km2"])[:8]:
        print("  %s %-22s %6d objets  %7.0f km²  %5.1f /100 km²  %s" % (r["code"], r["nom"], r["feuillus"], r["surface_km2"], r["densite_100km2"], r["methode"]))
    print("  ...")
    for r in sorted(done, key=lambda r: r["densite_100km2"])[:8]:
        print("  %s %-22s %6d objets  %7.0f km²  %5.1f /100 km²  %s" % (r["code"], r["nom"], r["feuillus"], r["surface_km2"], r["densite_100km2"], r["methode"]))
    print("non renseignés :", [r["code"] for r in out if r["feuillus"] is None])
    print("incomplets :", [r["code"] for r in out if not r["complet"]])
    import statistics
    d = sorted(r["densite_100km2"] for r in done if r["cartographie"])
    print("quantiles densité :", [round(d[int(len(d) * q)], 1) for q in (0.2, 0.4, 0.6, 0.8)], "min", d[0], "max", d[-1])


if __name__ == "__main__":
    main()
