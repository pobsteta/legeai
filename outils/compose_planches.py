# -*- coding: utf-8 -*-
"""Assemble les planches comparatives chêne pédonculé / chêne sessile à partir des dessins de elements/.

Usage (depuis la racine du dépôt) : python3 outils/compose_planches.py
Pour remplacer un dessin : déposer le nouveau fichier dans tomes/01-le-chene/planches/elements/ sous le même nom
(600 × 800 px ou plus, fond blanc ; le script normalise le point blanc et redimensionne).
"""
from PIL import Image, ImageDraw, ImageFont, ImageOps
import textwrap, os

SRC = "tomes/01-le-chene/planches/elements/"  # dessins déjà préparés (600 × 800, fond blanc)
OUT = "tomes/01-le-chene/planches/"
F = "/usr/share/fonts/truetype/"
f_title = ImageFont.truetype(F + "google-fonts/Lora-Variable.ttf", 54)
f_sub = ImageFont.truetype(F + "google-fonts/Lora-Italic-Variable.ttf", 30)
f_col = ImageFont.truetype(F + "crosextra/Carlito-Bold.ttf", 36)
f_lat = ImageFont.truetype(F + "google-fonts/Lora-Italic-Variable.ttf", 28)
f_row = ImageFont.truetype(F + "crosextra/Carlito-Bold.ttf", 30)
f_cap = ImageFont.truetype(F + "crosextra/Caladea-Regular.ttf", 26)
f_foot = ImageFont.truetype(F + "crosextra/Caladea-Italic.ttf", 22)
INK = (43, 36, 24)
GREY = (110, 104, 92)

ELEMENTS = {  # clé : (fichier, recadrage bas en fraction, nom de fichier de sortie)
    "feuille_ped": ("pedoncule_feuille.png", 0.0, "pedoncule_feuille.png"),
    "feuille_ses": ("sessile_feuille.png", 0.0, "sessile_feuille.png"),
    "gland_ped": ("pedoncule_glands.png", 0.0, "pedoncule_glands.png"),
    "gland_ses": ("sessile_glands.png", 0.0, "sessile_glands.png"),
    "bourgeon_ped": ("pedoncule_bourgeons.png", 0.0, "pedoncule_bourgeons.png"),
    "bourgeon_ses": ("sessile_bourgeons.png", 0.0, "sessile_bourgeons.png"),
    "ecorce_ped": ("pedoncule_ecorce.png", 0.0, "pedoncule_ecorce.png"),
    "ecorce_ses": ("sessile_ecorce.png", 0.0, "sessile_ecorce.png"),
}

def prep(key, w=600, h=800):
    fn, crop_bottom, out = ELEMENTS[key]
    im = Image.open(SRC + fn).convert("L")
    if crop_bottom:
        im = im.crop((0, 0, im.width, int(im.height * (1 - crop_bottom))))
    # point blanc adaptatif : la teinte du papier (valeur médiane) devient blanc, les traits restent
    hist = im.histogram(); total = sum(hist); acc = 0; med = 255
    for v, n in enumerate(hist):
        acc += n
        if acc >= total * 0.5:
            med = v; break
    white = max(200, med - 4)
    lut = [min(255, max(0, int((v - 18) * 255 / (white - 18)))) for v in range(256)]
    im = im.point(lut)
    im = ImageOps.pad(im, (w, h), color=255, method=Image.LANCZOS)
    os.makedirs(OUT + "elements", exist_ok=True)
    im.save(OUT + "elements/" + out)
    return im.convert("RGB")

def wrap(draw, text, font, width):
    words = text.split(); lines = []; cur = ""
    for wd in words:
        t = (cur + " " + wd).strip()
        if draw.textlength(t, font=font) <= width:
            cur = t
        else:
            lines.append(cur); cur = wd
    if cur:
        lines.append(cur)
    return lines

def planche(num, titre, rows, out_name, note_rows=None):
    W = 1400; M = 60; G = 80; CW = 600
    IH = 800; CAP_H = 150; ROW_LBL = 70
    H = 330 + len(rows) * (ROW_LBL + IH + CAP_H) + 150
    im = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(im)
    # cadre
    d.rectangle([M - 24, M - 24, W - M + 24, H - M + 24], outline=INK, width=3)
    d.rectangle([M - 16, M - 16, W - M + 16, H - M + 16], outline=INK, width=1)
    y = M + 20
    d.text((W / 2, y), "LE CHÊNE — PLANCHE COMPARATIVE %s" % num, font=f_title, fill=INK, anchor="mt")
    y += 70
    d.text((W / 2, y), titre, font=f_sub, fill=GREY, anchor="mt")
    y += 60
    # en-têtes de colonnes
    cols = [("CHÊNE PÉDONCULÉ", "Quercus robur L.", M), ("CHÊNE SESSILE", "Quercus petraea (Matt.) Liebl.", M + CW + G)]
    for name, lat, x in cols:
        d.text((x + CW / 2, y), name, font=f_col, fill=INK, anchor="mt")
        d.text((x + CW / 2, y + 42), lat, font=f_lat, fill=GREY, anchor="mt")
    y += 95
    d.line([M, y, W - M, y], fill=INK, width=2)
    y += 20
    for label, left, right in rows:
        d.text((W / 2, y + 8), label.upper(), font=f_row, fill=INK, anchor="mt")
        # petits filets de part et d'autre
        tw = d.textlength(label.upper(), font=f_row)
        d.line([M, y + 26, W / 2 - tw / 2 - 20, y + 26], fill=GREY, width=1)
        d.line([W / 2 + tw / 2 + 20, y + 26, W - M, y + 26], fill=GREY, width=1)
        y += ROW_LBL
        for (key, cap), x in zip((left, right), (M, M + CW + G)):
            if key is None:
                d.rectangle([x, y, x + CW, y + IH], outline=GREY, width=1)
                for i, ln in enumerate(wrap(d, cap, f_cap, CW - 60)):
                    d.text((x + CW / 2, y + IH / 2 - 40 + i * 34), ln, font=f_cap, fill=GREY, anchor="mt")
                continue
            cell = prep(key, CW, IH)
            im.paste(cell, (x, y))
            d.rectangle([x, y, x + CW, y + IH], outline=(200, 196, 186), width=1)
            for i, ln in enumerate(wrap(d, cap, f_cap, CW - 10)):
                d.text((x + CW / 2, y + IH + 16 + i * 32), ln, font=f_cap, fill=INK, anchor="mt")
        y += IH + CAP_H
    # pied
    foot = ("Dessins générés par IA (Magnific, mode auto) à partir des seuls critères écrits des fiches CNPF et de la formation ONF 2008 "
            "(F. Lebourgeois), puis contrôlés contre ces fiches et la Flore forestière française ; aucune photographie d'autrui n'a été fournie "
            "au générateur. Maquette d'étude pour Le Geai, tome 1, pages 4-5 — 8 novembre 2026.")
    for i, ln in enumerate(wrap(d, foot, f_foot, W - 2 * M - 40)):
        d.text((W / 2, H - M - 70 + i * 28), ln, font=f_foot, fill=GREY, anchor="mt")
    im.save(OUT + out_name + ".png", dpi=(200, 200))
    im.save(OUT + out_name + ".pdf", resolution=200.0)
    print(out_name, im.size)

planche("I", "Feuille et gland — les deux critères les plus sûrs",
        [("La feuille",
          ("feuille_ped", "Pétiole très court (4 à 8 mm) · base du limbe à deux oreillettes · lobes profonds, inégaux et irréguliers · plus grande largeur au tiers supérieur · nervures intercalaires nombreuses (3 et plus) · limbe mat"),
          ("feuille_ses", "Pétiole long (13 à 17 mm) · base du limbe en coin, sans oreillettes · lobes courts et réguliers · plus grande largeur à mi-hauteur · pas ou peu de nervures intercalaires · limbe luisant, poils étoilés dessous")),
         ("Le gland",
          ("gland_ped", "Glands allongés, cylindriques, par un à trois, nettement séparés, au bout d'un long pédoncule grêle de 3 à 8 cm"),
          ("gland_ses", "Glands trapus, ovoïdes, plus larges à la base, serrés en bouquet, assis directement sur le rameau"))],
        "planche-I-feuille-gland")

planche("II", "Bourgeon et écorce — quand il n'y a ni feuilles ni glands",
        [("Le bourgeon",
          ("bourgeon_ped", "Bourgeons ovoïdes globuleux, courts et arrondis, groupés en bouquet au bout du rameau anguleux"),
          ("bourgeon_ses", "Bourgeons ovoïdes pointus, allongés et effilés, groupés eux aussi en bouquet terminal")),
         ("L'écorce",
          ("ecorce_ped", "Rhytidome épais, profondément crevassé, découpé en plaques trapézoïdales larges et bombées, sillons profonds"),
          ("ecorce_ses", "Rhytidome mince et grisâtre, fissuré en long, en fines lanières verticales étroites et peu profondes"))],
        "planche-II-bourgeon-ecorce")

planche("III", "Le port — à compléter (dessins à générer)",
        [("Le port",
          (None, "Chêne pédonculé : tronc court et massif, grosses branches tortueuses partant en coude, ramification désordonnée, houppier large et irrégulier. Dessin à générer (quota du jour atteint)."),
          (None, "Chêne sessile : fût droit, long et conique, branches régulières et fines dressées en éventail, houppier régulier plus haut que large. Dessin à générer (quota du jour atteint)."))],
        "planche-III-port")
