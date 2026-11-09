# -*- coding: utf-8 -*-
"""Assemble les planches comparatives chêne pédonculé / chêne sessile à partir des dessins de elements/.

Usage (depuis la racine du dépôt) : python3 outils/compose_planches.py
Pour remplacer un dessin : déposer le nouveau fichier dans tomes/01-le-chene/planches/elements/ sous le même nom
(600 × 800 px ou plus, fond blanc ; le script normalise le point blanc et redimensionne). Le fichier enregistré dans
elements/ est le dessin normalisé, jamais zoomé ni recadré : le zoom et l'ancrage ne s'appliquent qu'à la case.

Échelle. Les dessins « au centimètre » (feuille, gland, bourgeon, écorce) reçoivent une pièce de 1 € (23,25 mm)
dessinée à l'échelle du sujet de la case ; les silhouettes gardent l'homme debout. L'échelle de chaque dessin
(ECHELLE, en pixels par centimètre dans le dessin de 600 × 800 avant zoom) est fixée d'après les dimensions typiques
des fiches CNPF/ONF (pétiole, gland, bourgeon, largeur des plaques d'écorce) — ce n'est pas une mesure sur photo :
pour l'édition définitive, la pièce sera dans le cadre des photographies de l'auteur et l'échelle en sera déduite.

Loupe. Les cases des bourgeons montrent le rameau (grossi trois fois) et, dans un cercle relié au bouquet terminal,
le bourgeon terminal grossi une dizaine de fois (LOUPE).
"""
from PIL import Image, ImageDraw, ImageFont, ImageOps
import math, os

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
f_note = ImageFont.truetype(F + "crosextra/Caladea-Italic.ttf", 24)
INK = (43, 36, 24)
GREY = (110, 104, 92)
PIECE_MM = 23.25  # diamètre de la pièce de 1 euro

ELEMENTS = {  # clé : (fichier, recadrage bas en fraction, nom de fichier de sortie)
    "feuille_ped": ("pedoncule_feuille.png", 0.0, "pedoncule_feuille.png"),
    "feuille_ses": ("sessile_feuille.png", 0.0, "sessile_feuille.png"),
    "gland_ped": ("pedoncule_glands.png", 0.0, "pedoncule_glands.png"),
    "gland_ses": ("sessile_glands.png", 0.0, "sessile_glands.png"),
    "bourgeon_ped": ("pedoncule_bourgeons.png", 0.0, "pedoncule_bourgeons.png"),
    "bourgeon_ses": ("sessile_bourgeons.png", 0.0, "sessile_bourgeons.png"),
    "ecorce_ped": ("pedoncule_ecorce.png", 0.0, "pedoncule_ecorce.png"),
    "ecorce_ses": ("sessile_ecorce.png", 0.0, "sessile_ecorce.png"),
    "port_ped": ("pedoncule_port.png", 0.0, "pedoncule_port.png"),
    "port_ses": ("sessile_port.png", 0.0, "sessile_port.png"),
}

# Zoom appliqué au dessin dans la case (jamais au fichier) : met les deux colonnes d'une ligne au même grossissement
# (bourgeon terminal : 6,5 mm pédonculé, 8,5 mm sessile) et laisse la place de la loupe.
ZOOM = {"bourgeon_ped": 0.80, "bourgeon_ses": 0.70}
# Ancrage du dessin zoomé dans la case : "centre" (défaut) ou "bas-gauche".
ANCRE = {"bourgeon_ped": "bas-gauche", "bourgeon_ses": "bas-gauche"}

# Échelle de chaque dessin en pixels par centimètre (avant zoom) et mode de pose de la pièce :
# "libre" = posée sur le papier, dans un coin libre ; "sur" = posée sur l'écorce, en bas à droite.
ECHELLE = {
    "feuille_ped": (66, "libre"),   # feuille de 10 cm environ, pétiole compris
    "feuille_ses": (66, "libre"),   # feuille de 11 cm environ, long pétiole compris
    "gland_ped": (56, "libre"),     # gland de 2,5 cm, pédoncule de 8 cm
    "gland_ses": (56, "libre"),     # gland de 2 cm
    "bourgeon_ped": (108, "libre"), # bourgeon terminal de 6,5 mm, rameau grossi trois fois
    "bourgeon_ses": (125, "libre"), # bourgeon terminal de 8,5 mm ; ramené à 108 × 0,8 par le zoom
    "ecorce_ped": (30, "sur"),      # plaques de 4 cm de large environ, cadre de 20 cm
    "ecorce_ses": (30, "sur"),      # lanières de 1,5 cm de large environ
}

# Loupe : (fichier du gros plan, centre du bouquet terminal sur le dessin du rameau en coordonnées source 600 × 800,
#          rayon du cercle de visée autour du bouquet, centre et rayon du cercle de la loupe dans la case).
LOUPE = {
    "bourgeon_ped": ("pedoncule_bourgeon_loupe.png", (437, 179), 62, (452, 158), 132),
    "bourgeon_ses": ("sessile_bourgeon_loupe.png", (464, 150), 52, (452, 158), 132),
}


def normaliser(im):
    """Point blanc adaptatif (première passe) puis grain du papier effacé ; idempotent."""
    hist = im.histogram(); total = sum(hist); acc = 0; med = 255
    for v, n in enumerate(hist):
        acc += n
        if acc >= total * 0.5:
            med = v; break
    if med < 250:  # première passe seulement : le papier (médiane) devient blanc
        white = max(200, med - 4)
        im = im.point([min(255, int(v * 255 / white)) for v in range(256)])
    return im.point([255 if v >= 240 else v for v in range(256)])


def prep(key, w=600, h=800):
    """Charge, normalise et enregistre le dessin ; renvoie la case (zoom et ancrage appliqués) et sa transformation."""
    fn, crop_bottom, out = ELEMENTS[key]
    im = Image.open(SRC + fn).convert("L")
    if crop_bottom:
        im = im.crop((0, 0, im.width, int(im.height * (1 - crop_bottom))))
    im = normaliser(im)
    im = ImageOps.pad(im, (w, h), color=255, method=Image.LANCZOS)
    os.makedirs(OUT + "elements", exist_ok=True)
    im.save(OUT + "elements/" + out)
    z = ZOOM.get(key, 1.0)
    dx = dy = 0.0
    if z != 1.0 or ANCRE.get(key):
        bbox = ImageOps.invert(im).getbbox()
        content = im.crop(bbox)
        content = content.resize((max(1, int(content.width * z)), max(1, int(content.height * z))), Image.LANCZOS)
        if ANCRE.get(key) == "bas-gauche":
            px, py = 24, h - content.height - 24
        else:
            px, py = (w - content.width) // 2, (h - content.height) // 2
        canvas = Image.new("L", (w, h), 255)
        canvas.paste(content, (px, py))
        im = canvas
        dx, dy = px - bbox[0] * z, py - bbox[1] * z  # x_case = x_source * z + dx
    return im.convert("RGB"), (z, dx, dy)


def piece(R):
    """Dessin d'une pièce de 1 € de rayon R pixels, au trait, sur fond transparent (RGBA)."""
    S = 4  # suréchantillonnage pour des traits propres
    r = R * S
    size = int(2 * r + 8 * S)
    c = size / 2
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    lw = max(1, int(round(r / 34)))
    d.ellipse([c - r + 0.05 * r, c - r + 0.08 * r, c + r + 0.05 * r, c + r + 0.08 * r], fill=(120, 112, 100, 255))
    d.ellipse([c - r, c - r, c + r, c + r], fill=(255, 255, 255, 255), outline=INK + (255,), width=lw)
    r_in = 0.76 * r
    hatch = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    hd = ImageDraw.Draw(hatch)
    step = max(2 * S, int(r / 11))
    for k in range(-size, 2 * size, step):
        hd.line([k, 0, k + size, size], fill=(95, 88, 76, 255), width=max(1, lw // 2))
    mask = Image.new("L", (size, size), 0)
    md = ImageDraw.Draw(mask)
    md.ellipse([c - r + lw, c - r + lw, c + r - lw, c + r - lw], fill=255)
    md.ellipse([c - r_in, c - r_in, c + r_in, c + r_in], fill=0)
    im.paste(hatch, (0, 0), mask)
    d.ellipse([c - r_in, c - r_in, c + r_in, c + r_in], outline=INK + (255,), width=lw)
    if R >= 45:
        for i in range(12):
            a0 = -math.pi / 2 + i * math.pi / 6
            cx, cy = c + 0.88 * r * math.cos(a0), c + 0.88 * r * math.sin(a0)
            pts = []
            for j in range(10):
                rr = 0.075 * r if j % 2 == 0 else 0.032 * r
                a = a0 + j * math.pi / 5
                pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
            d.polygon(pts, fill=(255, 255, 255, 255), outline=INK + (255,))
    f1 = ImageFont.truetype(F + "crosextra/Caladea-Bold.ttf", int(1.15 * r))
    d.text((c - 0.14 * r, c + 0.02 * r), "1", font=f1, fill=INK + (255,), anchor="mm")
    fe = ImageFont.truetype(F + "crosextra/Carlito-Bold.ttf", int(0.24 * r))
    tw = int(fe.getlength("EURO")) + 4 * S
    th = int(0.3 * r) + 4 * S
    t = Image.new("RGBA", (tw, th), (0, 0, 0, 0))
    ImageDraw.Draw(t).text((tw / 2, th / 2), "EURO", font=fe, fill=INK + (255,), anchor="mm")
    t = t.rotate(90, expand=True)
    im.paste(t, (int(c + 0.36 * r - t.width / 2), int(c - t.height / 2)), t)
    return im.resize((size // S, size // S), Image.LANCZOS)


def zone_libre(cell, cx, cy, rr):
    g = cell.convert("L").load()
    w, h = cell.size
    for yy in range(max(0, cy - rr), min(h, cy + rr), 3):
        for xx in range(max(0, cx - rr), min(w, cx + rr), 3):
            if (xx - cx) ** 2 + (yy - cy) ** 2 <= rr * rr and g[xx, yy] < 200:
                return False
    return True


def poser_piece(cell, key, transfo):
    """Pose la pièce à l'échelle de la case : dans un coin libre du papier, ou sur l'écorce."""
    if key not in ECHELLE:
        return False
    ppcm, mode = ECHELLE[key]
    z = transfo[0]
    R = int(round(PIECE_MM / 10 * ppcm * z / 2))
    w, h = cell.size
    marge = 14
    if mode == "sur":
        cx, cy = w - R - 60, h - R - 110
    else:
        cands = []
        for cy in range(h - R - marge, R + marge, -8):
            for cx in range(w - R - marge, R + marge, -8):
                cands.append((((w - R - marge) - cx) ** 2 + ((h - R - marge) - cy) ** 2, cx, cy))
        cands.sort()
        cx, cy = None, None
        for _, x, y in cands:
            if zone_libre(cell, x, y, R + 10):
                cx, cy = x, y; break
        if cx is None:
            cx, cy = w - R - marge, h - R - marge
    p = piece(R)
    cell.paste(p, (int(cx - p.width / 2), int(cy - p.height / 2)), p)
    return True


def poser_loupe(cell, key, transfo):
    """Cercle de visée sur le bouquet terminal du rameau, deux traits, et la loupe avec le gros plan."""
    if key not in LOUPE:
        return
    fn, (sx, sy), r_vise, (lx, ly), r_loupe = LOUPE[key]
    z, dx, dy = transfo
    vx, vy = sx * z + dx, sy * z + dy  # bouquet terminal dans la case
    d = ImageDraw.Draw(cell)
    # gros plan, normalisé, ajusté dans le cercle
    gp = normaliser(Image.open(SRC + fn).convert("L"))
    bbox = ImageOps.invert(gp).getbbox()
    gp = gp.crop(bbox)
    gp = gp.crop((0, 0, gp.width, int(gp.height * 0.78)))  # le bourgeon et sa base, moins de rameau
    side = int(2 * r_loupe * 0.88)
    gp = ImageOps.contain(gp, (side, side), method=Image.LANCZOS)
    disque = Image.new("L", (2 * r_loupe, 2 * r_loupe), 255)
    disque.paste(gp, ((2 * r_loupe - gp.width) // 2, (2 * r_loupe - gp.height) // 2))
    mask = Image.new("L", (2 * r_loupe, 2 * r_loupe), 0)
    ImageDraw.Draw(mask).ellipse([0, 0, 2 * r_loupe - 1, 2 * r_loupe - 1], fill=255)
    cell.paste(disque.convert("RGB"), (int(lx - r_loupe), int(ly - r_loupe)), mask)
    # traits de liaison : tangentes approchées entre le cercle de visée et la loupe
    ang = math.atan2(ly - vy, lx - vx)
    for s in (-1, 1):
        a1 = ang + s * math.pi / 2
        x1, y1 = vx + r_vise * math.cos(a1), vy + r_vise * math.sin(a1)
        x2, y2 = lx + r_loupe * math.cos(a1), ly + r_loupe * math.sin(a1)
        d.line([x1, y1, x2, y2], fill=GREY, width=1)
    d.ellipse([vx - r_vise, vy - r_vise, vx + r_vise, vy + r_vise], outline=INK, width=2)
    d.ellipse([lx - r_loupe, ly - r_loupe, lx + r_loupe, ly + r_loupe], outline=INK, width=3)
    d.ellipse([lx - r_loupe + 6, ly - r_loupe + 6, lx + r_loupe - 6, ly + r_loupe - 6], outline=GREY, width=1)


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


def pied(avec_piece, avec_loupe):
    foot = ("Dessins générés par IA (Magnific) à partir des seuls critères écrits des fiches CNPF, de la formation ONF 2008 "
            "(F. Lebourgeois) et de la planche du CDAF-Chimay, puis contrôlés contre ces documents et la Flore forestière française ; "
            "aucune photographie ni planche d'autrui n'a été fournie au générateur. ")
    if avec_piece:
        foot += "La pièce de 1 € (23 mm) est dessinée à l'échelle du sujet de chaque case"
        foot += " ; la loupe montre le bourgeon terminal grossi une dizaine de fois. " if avec_loupe else ". "
    return foot + "Maquette d'étude pour Le Geai, tome 1, pages 4-5 — 8 et 9 novembre 2026."


def planche(num, titre, rows, out_name, note=None):
    W = 1400; M = 60; G = 80; CW = 600
    IH = 800; CAP_H = 150; ROW_LBL = 70
    cles = [k for _, l, r in rows for k, _ in (l, r) if k]
    avec_piece = any(k in ECHELLE for k in cles)
    avec_loupe = any(k in LOUPE for k in cles)
    n_foot = len(wrap(ImageDraw.Draw(Image.new("RGB", (W, 10))), pied(avec_piece, avec_loupe), f_foot, W - 2 * M - 40))
    FOOT_H = 40 + n_foot * 28
    H = 330 + len(rows) * (ROW_LBL + IH + CAP_H) + FOOT_H + 40 + (40 if note else 0)
    im = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(im)
    d.rectangle([M - 24, M - 24, W - M + 24, H - M + 24], outline=INK, width=3)
    d.rectangle([M - 16, M - 16, W - M + 16, H - M + 16], outline=INK, width=1)
    y = M + 20
    d.text((W / 2, y), "LE CHÊNE — PLANCHE COMPARATIVE %s" % num, font=f_title, fill=INK, anchor="mt")
    y += 70
    d.text((W / 2, y), titre, font=f_sub, fill=GREY, anchor="mt")
    y += 60
    cols = [("CHÊNE PÉDONCULÉ", "Quercus robur L.", M), ("CHÊNE SESSILE", "Quercus petraea (Matt.) Liebl.", M + CW + G)]
    for name, lat, x in cols:
        d.text((x + CW / 2, y), name, font=f_col, fill=INK, anchor="mt")
        d.text((x + CW / 2, y + 42), lat, font=f_lat, fill=GREY, anchor="mt")
    y += 95
    d.line([M, y, W - M, y], fill=INK, width=2)
    y += 20
    for label, left, right in rows:
        d.text((W / 2, y + 8), label.upper(), font=f_row, fill=INK, anchor="mt")
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
            cell, transfo = prep(key, CW, IH)
            poser_loupe(cell, key, transfo)
            poser_piece(cell, key, transfo)
            im.paste(cell, (x, y))
            d.rectangle([x, y, x + CW, y + IH], outline=(200, 196, 186), width=1)
            for i, ln in enumerate(wrap(d, cap, f_cap, CW - 10)):
                d.text((x + CW / 2, y + IH + 16 + i * 32), ln, font=f_cap, fill=INK, anchor="mt")
        y += IH + CAP_H
    if note:
        for i, ln in enumerate(wrap(d, note, f_note, W - 2 * M - 40)):
            d.text((W / 2, y - 30 + i * 30), ln, font=f_note, fill=INK, anchor="mt")
    for i, ln in enumerate(wrap(d, pied(avec_piece, avec_loupe), f_foot, W - 2 * M - 40)):
        d.text((W / 2, H - M - FOOT_H + 20 + i * 28), ln, font=f_foot, fill=GREY, anchor="mt")
    im.save(OUT + out_name + ".png", dpi=(200, 200))
    im.save(OUT + out_name + ".pdf", resolution=200.0)
    print(out_name, im.size)


if __name__ == "__main__":
    planche("I", "Feuille et gland — les deux critères les plus sûrs",
            [("La feuille",
              ("feuille_ped", "Pétiole très court (4 à 8 mm) · deux oreillettes arrondies et inégales à la base · lobes inégaux et irréguliers · plus grande largeur au tiers supérieur · nervures intercalaires nombreuses · limbe mat"),
              ("feuille_ses", "Pétiole long (13 à 17 mm) · base en coin, sans oreillettes · lobes courts et réguliers · plus grande largeur à mi-hauteur · pas ou peu de nervures intercalaires · limbe luisant, poils étoilés dessous")),
             ("Le gland",
              ("gland_ped", "Glands allongés, cylindriques, par un à trois, nettement séparés, au bout d'un long pédoncule grêle de 3 à 8 cm"),
              ("gland_ses", "Glands trapus, ovoïdes, plus larges à la base, serrés en bouquet, assis directement sur le rameau"))],
            "planche-I-feuille-gland")

    planche("II", "Bourgeon et écorce — quand il n'y a ni feuilles ni glands",
            [("Le bourgeon",
              ("bourgeon_ped", "Bourgeons ovoïdes globuleux, courts et arrondis, groupés en bouquet au bout du rameau anguleux (rameau grossi trois fois ; bourgeon terminal dans la loupe)"),
              ("bourgeon_ses", "Bourgeons ovoïdes pointus, allongés et effilés, groupés eux aussi en bouquet terminal (même grossissement, même loupe)")),
             ("L'écorce",
              ("ecorce_ped", "Grossière, rugueuse : rhytidome épais, crevasses profondes longitudinales et transversales, découpé en plaquettes trapézoïdales anguleuses rangées en colonnes"),
              ("ecorce_ses", "Plus lisse, moins rugueuse : rhytidome mince et gris clair, fines lanières longitudinales coupées en petites plaquettes carrées, fissures peu profondes"))],
            "planche-II-bourgeon-ecorce")

    planche("III", "Le port — l'arbre entier, en hiver",
            [("Le port",
              ("port_ped", "Tronc court et massif, divisé bas en grosses branches maîtresses tortueuses partant en coude · ramification désordonnée · houppier large et irrégulier, plus large que haut (arbre de haie ou de pré)"),
              ("port_ses", "Fût droit, long et cylindrique, sans branche basse · branches fines et régulières dressées en éventail · houppier régulier, plus haut que large (arbre de futaie)"))],
            "planche-III-port")
