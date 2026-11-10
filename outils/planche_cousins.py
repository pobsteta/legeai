# -*- coding: utf-8 -*-
"""Tome 1, p. 6-7 : la planche des feuilles des cousins, remise à l'échelle, numérotée, avec une pièce de 1 €.

Le dessin généré (eI767rRdqL) ne respecte pas les proportions entre espèces. On découpe chaque feuille,
on la redimensionne à une longueur typique (limbe + pétiole), on les aligne sur une même ligne de base,
puis on pose les numéros (vectoriels, jamais générés) et une pièce de 1 € (23,25 mm) à la même échelle.

Usage (depuis la racine du dépôt) : python3 outils/planche_cousins.py
"""
import sys
from PIL import Image, ImageDraw, ImageFont
import numpy as np
from scipy import ndimage

sys.path.insert(0, "outils")
from compose_planches import piece, INK, F, PIECE_MM  # noqa: E402

SRC = "tomes/01-le-chene/images/p06-07-feuilles-des-cousins_eI767rRdqL.jpg"
OUT = "tomes/01-le-chene/images/p06-07-feuilles-des-cousins-numerotees.png"

# Ordre de gauche à droite dans le dessin (prompt eI767rRdqL) et longueur typique limbe + pétiole, en cm.
# Valeurs moyennes des fourchettes courantes, À VÉRIFIER contre la Flore forestière française avant parution.
FEUILLES = [
    ("chêne pubescent", 9.0),
    ("chêne vert", 5.0),
    ("chêne-liège", 5.5),
    ("chêne kermès", 3.0),
    ("chêne tauzin", 14.0),
    ("chêne chevelu", 10.0),
    ("chêne rouge d'Amérique", 18.0),
]
PX_CM = 42          # échelle de la planche : pixels par centimètre
MARGE, ECART = 60, 46


def decouper(im):
    """Chaque feuille seule : découpée selon sa propre silhouette, papier ramené au blanc."""
    g = np.array(im.convert("L")).astype(float)
    masque = ndimage.binary_closing(g < 170, iterations=6)
    masque = ndimage.binary_fill_holes(masque)
    lab, _ = ndimage.label(masque)
    objets = [(s, k + 1) for k, s in enumerate(ndimage.find_objects(lab)) if s[0].stop - s[0].start > 80]
    objets.sort(key=lambda o: o[0][1].start)
    assert len(objets) == len(FEUILLES), len(objets)
    rgb = np.array(im).astype(float)
    # point blanc : le papier (≈ 235-250) devient 255, l'encre garde sa valeur
    blanc = np.clip((rgb - 0) * 255.0 / 232.0, 0, 255)
    out = []
    for (sy, sx), k in objets:
        p = 8
        y0, y1 = max(0, sy.start - p), min(im.height, sy.stop + p)
        x0, x1 = max(0, sx.start - p), min(im.width, sx.stop + p)
        m = ndimage.binary_dilation(lab[y0:y1, x0:x1] == k, iterations=5)
        crop = blanc[y0:y1, x0:x1].copy()
        crop[~m] = 255
        out.append(Image.fromarray(crop.astype(np.uint8)))
    return out


def main():
    src = Image.open(SRC).convert("RGB")
    feuilles = []
    for crop, (nom, cm) in zip(decouper(src), FEUILLES):
        h = int(cm * PX_CM)
        w = int(crop.width * h / crop.height)
        feuilles.append(crop.resize((w, h), Image.LANCZOS))
    R = int(PIECE_MM / 10 * PX_CM / 2)
    coin = piece(R)
    H_max = max(f.height for f in feuilles)
    f_num = ImageFont.truetype(F + "crosextra/Carlito-Bold.ttf", 34)
    larg = 2 * MARGE + sum(f.width for f in feuilles) + ECART * len(feuilles) + coin.width
    haut = MARGE + H_max + 70
    planche = Image.new("RGB", (larg, haut), "white")
    d = ImageDraw.Draw(planche)
    base = MARGE + H_max  # ligne de base : le bout des pétioles
    x = MARGE
    for i, f in enumerate(feuilles, 1):
        planche.paste(Image.fromarray(np.minimum(np.array(planche.crop((x, base - f.height, x + f.width, base))),
                                                 np.array(f))), (x, base - f.height))
        cx = x + f.width // 2
        d.ellipse([cx - 22, base + 14, cx + 22, base + 58], outline=INK, width=3)
        d.text((cx, base + 37), str(i), font=f_num, fill=INK, anchor="mm")
        x += f.width + ECART
    planche.paste(coin, (x, base - coin.height), coin)
    # recadrage serré sur le contenu
    planche = planche.crop((MARGE // 2, MARGE // 2, x + coin.width + MARGE // 2, haut))
    planche.save(OUT)
    print(OUT, planche.size)


if __name__ == "__main__":
    main()
