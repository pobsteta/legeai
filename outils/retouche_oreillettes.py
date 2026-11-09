# -*- coding: utf-8 -*-
"""Retouche du 9 novembre 2026 : accentuer les oreillettes de la feuille de chêne pédonculé (maquette d'étude).

Le mode auto gratuit de Magnific n'a pas su dessiner une base auriculée (onze essais, voir
tomes/01-le-chene/planches/prompts-planches-comparatives.md). La base du dessin retenu (`ovPxVs5829`) est donc
déformée localement : les derniers millimètres du limbe, de part et d'autre du pétiole, sont étirés vers le bas selon
un profil gaussien (31 px au plus dans la case de 600 × 800, soit 5 mm environ à l'échelle de la planche) ; le pétiole
et le bout de rameau ne bougent pas. Rien n'est dessiné à la main : ce sont les hachures du dessin lui-même, étirées.

Usage (depuis la racine du dépôt) :
    python3 outils/retouche_oreillettes.py
Lit  tomes/01-le-chene/planches/elements/remplaces/pedoncule_feuille_ovPxVs5829_sans-oreillettes.png
Écrit tomes/01-le-chene/planches/elements/pedoncule_feuille.png
"""
from PIL import Image
import numpy as np, math

SRC = "tomes/01-le-chene/planches/elements/remplaces/pedoncule_feuille_ovPxVs5829_sans-oreillettes.png"
OUT = "tomes/01-le-chene/planches/elements/pedoncule_feuille.png"

PETIOLE = (293, 306)       # colonnes du pétiole, laissées intactes
Y0, YB = 540, 720          # bande déformée (au-dessus : identité ; au-dessous : identité)
D, W_G = 31, 26            # allongement maximal (px) et largeur du profil gaussien
XL, XR = 281, 318          # centres des deux oreillettes

src = Image.open(SRC).convert("L")
a = np.asarray(src); dark = a < 170
W, H = src.size


def bord(x):
    """Dernière ligne sombre du limbe dans la colonne x (sans le pétiole ni le rameau)."""
    col = np.where(dark[:660, x])[0]
    return col.max() if len(col) else None


def allongement(x):
    if x < PETIOLE[0]:
        return D * math.exp(-((x - XL) / W_G) ** 2)
    if x > PETIOLE[1]:
        return D * math.exp(-((x - XR) / W_G) ** 2)
    return 0.0


def facteur(x):
    e = bord(x)
    if e is None or e < Y0 + 10 or PETIOLE[0] <= x <= PETIOLE[1]:
        return 1.0
    return (e + allongement(x) - Y0) / (e - Y0)


mesh = []
for x0 in range(0, W, 2):
    x1 = min(W, x0 + 2)
    s0, s1 = facteur(x0), facteur(min(x1, W - 1))
    if PETIOLE[0] <= x0 <= PETIOLE[1] or PETIOLE[0] <= x1 - 1 <= PETIOLE[1]:
        s0 = s1 = 1.0
    mesh.append(((x0, 0, x1, Y0), (x0, 0, x0, Y0, x1, Y0, x1, 0)))
    mesh.append(((x0, Y0, x1, YB), (x0, Y0, x0, Y0 + (YB - Y0) / s0, x1, Y0 + (YB - Y0) / s1, x1, Y0)))
    mesh.append(((x0, YB, x1, H), (x0, YB, x0, H, x1, H, x1, YB)))
out = src.transform((W, H), Image.MESH, mesh, Image.BICUBIC, fillcolor=255)

# le petit bourgeon latéral du bout de rameau, déplacé par l'étirement, est effacé
arr = np.asarray(out).copy()
arr[695:721, 270:293] = 255
Image.fromarray(arr).save(OUT)
print("écrit", OUT)
