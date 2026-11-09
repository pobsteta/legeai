# -*- coding: utf-8 -*-
"""Le Jacques — détourage des vignettes et planche de présentation (maquette d'étude v0, 9 novembre 2026).

Usage (depuis la racine du dépôt) : python3 outils/jacques_planche.py

Entrées : collection/jacques/sources/*.png — copies 800 à 1 024 px, fond blanc, des générations Magnific retenues
          (planche modèle trois angles, feuille des huit têtes, douze attitudes J1 à J12).
Sorties : collection/jacques/vignettes/Jacques_Jnn_nom_v0.png — vignettes détourées (PNG, fond transparent) ;
          collection/jacques/Jacques_planche_v0.png / .pdf — planche de présentation : modèle, douze attitudes avec
          leur bulle d'exemple (police Patrick Hand), têtes, et le pied qui dit ce que c'est.

Détourage : remplissage depuis les bords sur les pixels presque blancs (le papier) ; les blancs enfermés dans le
dessin (gorge, croupion, tache de l'aile, œil) restent opaques puisqu'ils ne touchent pas le bord. Un léger flou
d'un pixel adoucit le contour. Pour l'édition définitive, préférer le détourage de Magnific (images_remove_background).

Les bulles sont dessinées ici en vectoriel pour la présentation ; dans le livre, elles sont posées à la maquette,
jamais générées dans l'image (fiche de personnage, section 6).
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np
from collections import deque
import glob, os, re

SRC = "collection/jacques/sources/"
OUT = "collection/jacques/"
VIG = OUT + "vignettes/"
F = "/usr/share/fonts/truetype/"
f_title = ImageFont.truetype(F + "google-fonts/Lora-Variable.ttf", 64)
f_sub = ImageFont.truetype(F + "google-fonts/Lora-Italic-Variable.ttf", 30)
f_lbl = ImageFont.truetype(F + "crosextra/Carlito-Bold.ttf", 30)
f_lbl2 = ImageFont.truetype(F + "crosextra/Carlito-Regular.ttf", 24)
f_foot = ImageFont.truetype(F + "crosextra/Caladea-Italic.ttf", 22)
f_bulle = ImageFont.truetype(OUT + "PatrickHand-Regular.ttf", 27)
INK = (43, 36, 24)
GREY = (110, 104, 92)
BLEU = (46, 98, 168)

POSES = [  # numéro, nom, fichier source (motif), bulle d'exemple (fiche de personnage, section 4), côté du bec (g/d)
    ("J1", "Le guetteur", "J01", "Moi, à cette date, j'ai déjà un nid et des œufs. Lui, pas une feuille. Chacun son rythme.", "d"),
    ("J2", "Le porteur", "J02", "Cent mille glands. Je ne peux pas tout prendre. Je fais ce que je peux.", "d"),
    ("J3", "Le planteur", "J03", "Je retrouve presque tout. Presque.", "g"),
    ("J4", "Le chercheur", "J04", "Je plante, ils mangent. On n'a pas la même idée d'une forêt.", "g"),
    ("J5", "En vol", "J05", "Le mulot plante à trente mètres. Moi, à trois cents. On ne joue pas dans la même cour.", "d"),
    ("J6", "Le vantard", "J06", "Un quart du bois de France. Devinez qui l'a planté.", "d"),
    ("J7", "Le vexé", "J07", "Il germe avant que j'aie fini de le cacher. C'est vexant, pour un planteur.", "d"),
    ("J8", "Le dubitatif", "J08", "Celui-là ? Jamais vu.", "d"),
    ("J9", "La sentinelle", "J09", "Criard, criard… Sentinelle, on dit.", "d"),
    ("J10", "Le gourmand", "J10", "Elles descendent au bout d'un fil quand on les dérange. Je n'ai qu'à ouvrir le bec.", "d"),
    ("J11", "Le patient", "J11", "Vingt minutes sans bouger ? J'ai essayé. J'ai tenu quarante secondes.", "d"),
    ("J12", "Le scribe", "J12", None, "d"),
]


def detourer(im, seuil=228):
    """Fond blanc → transparent par remplissage depuis les bords ; renvoie une image RGBA."""
    rgb = im.convert("RGB")
    a = np.asarray(rgb).astype(np.int16)
    clair = (a.min(axis=2) >= seuil)  # presque blanc sur les trois canaux
    h, w = clair.shape
    fond = np.zeros((h, w), dtype=bool)
    q = deque()
    for x in range(w):
        for y in (0, h - 1):
            if clair[y, x] and not fond[y, x]:
                fond[y, x] = True; q.append((y, x))
    for y in range(h):
        for x in (0, w - 1):
            if clair[y, x] and not fond[y, x]:
                fond[y, x] = True; q.append((y, x))
    while q:
        y, x = q.popleft()
        for ny, nx in ((y - 1, x), (y + 1, x), (y, x - 1), (y, x + 1)):
            if 0 <= ny < h and 0 <= nx < w and clair[ny, nx] and not fond[ny, nx]:
                fond[ny, nx] = True; q.append((ny, nx))
    alpha = Image.fromarray(np.where(fond, 0, 255).astype(np.uint8))
    alpha = alpha.filter(ImageFilter.GaussianBlur(0.7))
    out = rgb.copy(); out.putalpha(alpha)
    return out


def blanchir(rgb, seuil=232):
    """Le papier légèrement gris du générateur devient blanc pur ; les couleurs ne bougent pas."""
    a = np.asarray(rgb).astype(np.int16)
    clair = (a.min(axis=2) >= seuil)
    a[clair] = 255
    return Image.fromarray(a.astype(np.uint8))


def rogner(rgba, marge=12):
    bbox = rgba.getchannel("A").point(lambda v: 255 if v > 8 else 0).getbbox()
    if not bbox:
        return rgba
    l, t, r, b = bbox
    return rgba.crop((max(0, l - marge), max(0, t - marge), min(rgba.width, r + marge), min(rgba.height, b + marge)))


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


def bulle(d, texte, box, pointe):
    """Bulle ovale au trait fin, texte en Patrick Hand, appendice vers `pointe` (x, y)."""
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    # appendice : triangle du bord de l'ellipse vers la pointe
    import math
    ang = math.atan2(pointe[1] - cy, pointe[0] - cx)
    rx, ry = (x1 - x0) / 2, (y1 - y0) / 2
    bx, by = cx + rx * 0.92 * math.cos(ang), cy + ry * 0.92 * math.sin(ang)
    da = 0.22
    p1 = (cx + rx * 0.95 * math.cos(ang - da), cy + ry * 0.95 * math.sin(ang - da))
    p2 = (cx + rx * 0.95 * math.cos(ang + da), cy + ry * 0.95 * math.sin(ang + da))
    d.polygon([p1, p2, pointe], fill="white", outline=INK)
    d.ellipse(box, fill="white", outline=INK, width=2)
    d.polygon([p1, p2, pointe], fill="white")
    d.line([p1, pointe], fill=INK, width=2); d.line([p2, pointe], fill=INK, width=2)
    lines = wrap(d, texte, f_bulle, (x1 - x0) * 0.78)
    lh = 31
    ty = cy - lh * len(lines) / 2 + 4
    for ln in lines:
        d.text((cx, ty), ln, font=f_bulle, fill=INK, anchor="mt"); ty += lh


def main():
    os.makedirs(VIG, exist_ok=True)
    vignettes = {}
    for num, nom, motif, _, _ in POSES:
        src = glob.glob(SRC + "Jacques_%s_*.png" % motif)[0]
        ident = re.search(r"_([A-Za-z0-9]{10})\.png$", src).group(1)
        rgba = rogner(detourer(Image.open(src)))
        slug = re.sub(r"[^a-z-]", "", nom.lower().replace("é", "e").replace("è", "e").replace(" ", "-"))
        out = VIG + "Jacques_%s_%s_v0.png" % (motif, slug.replace("le-", "").replace("la-", "").replace("en-vol", "en-vol"))
        rgba.save(out)
        vignettes[num] = (rgba, out, ident)
        print(out, rgba.size, ident)

    # ---------------- planche de présentation ----------------
    W = 2400; M = 80
    modele = blanchir(Image.open(glob.glob(SRC + "Jacques_modele_*.png")[0]).convert("RGB"))
    tetes = blanchir(Image.open(glob.glob(SRC + "Jacques_tetes_*.png")[0]).convert("RGB"))
    CW = (W - 2 * M - 3 * 40) // 4  # 4 colonnes
    CH = 560; LBL = 60; BUL = 150
    rows = 3
    mod_h = int(modele.height * (W - 2 * M) * 0.62 / modele.width)
    tet_h = int(tetes.height * (W - 2 * M) * 0.62 / tetes.width)
    H = M + 150 + mod_h + 80 + rows * (LBL + CH + BUL + 30) + 60 + tet_h + 60 + 170 + M
    im = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(im)
    d.rectangle([M - 30, M - 30, W - M + 30, H - M + 30], outline=INK, width=3)
    d.rectangle([M - 22, M - 22, W - M + 22, H - M + 22], outline=INK, width=1)
    y = M
    d.text((W / 2, y), "LE JACQUES — PLANCHE MODÈLE v0", font=f_title, fill=INK, anchor="mt"); y += 78
    d.text((W / 2, y), "Le narrateur de la collection Le Geai — maquette d'étude, 9 novembre 2026", font=f_sub, fill=GREY, anchor="mt"); y += 72
    # modèle trois angles
    mw = int((W - 2 * M) * 0.62); mm = modele.resize((mw, mod_h), Image.LANCZOS)
    im.paste(mm, ((W - mw) // 2, y))
    d.text((M, y + 10), "A · Trois angles", font=f_lbl, fill=INK, anchor="lt")
    d.text((M, y + 48), "profil, trois-quarts, face —", font=f_lbl2, fill=GREY, anchor="lt")
    d.text((M, y + 76), "posture neutre, huppe mi-dressée", font=f_lbl2, fill=GREY, anchor="lt")
    d.text((W - M, y + 10), "Jacques_modele_v0", font=f_lbl2, fill=GREY, anchor="rt")
    y += mod_h + 40
    d.line([M, y, W - M, y], fill=INK, width=2); y += 40
    d.text((M, y), "B · Les douze attitudes", font=f_lbl, fill=INK, anchor="lt")
    d.text((W - M, y + 4), "bulles d'exemple en Patrick Hand (police proposée, licence OFL) — posées à la maquette, jamais générées", font=f_lbl2, fill=GREY, anchor="rt")
    y += 50
    for r in range(rows):
        for c in range(4):
            idx = r * 4 + c
            num, nom, motif, texte, cote = POSES[idx]
            rgba, _, ident = vignettes[num]
            x = M + c * (CW + 40)
            d.text((x, y), "%s · %s" % (num, nom), font=f_lbl, fill=INK, anchor="lt")
            d.text((x + CW, y + 6), ident, font=f_lbl2, fill=GREY, anchor="rt")
            cy0 = y + LBL
            # vignette ajustée dans CW × CH, posée en bas
            v = rgba.copy(); v.thumbnail((CW - 20, CH - 20), Image.LANCZOS)
            vx = x + (CW - v.width) // 2; vy = cy0 + CH - v.height - 10
            im.paste(v, (vx, vy), v)
            d.rectangle([x, cy0, x + CW, cy0 + CH], outline=(215, 210, 200), width=1)
            if texte:
                # bulle sous la vignette, pointe vers le haut (vers le bec), côté selon la pose
                bx0, by0, bx1, by1 = x + 10, cy0 + CH + 18, x + CW - 10, cy0 + CH + BUL - 6
                px = x + CW * (0.72 if cote == "d" else 0.28)
                bulle(d, texte, (bx0, by0, bx1, by1), (px, cy0 + CH - 30))
            else:
                d.text((x + CW / 2, cy0 + CH + 50), "(pas de bulle : il tient la plume", font=f_lbl2, fill=GREY, anchor="mm")
                d.text((x + CW / 2, cy0 + CH + 80), "sur la page de l'énigme et la lettre de fin)", font=f_lbl2, fill=GREY, anchor="mm")
        y += LBL + CH + BUL + 30
    d.line([M, y, W - M, y], fill=INK, width=2); y += 30
    d.text((M, y), "C · Huit têtes", font=f_lbl, fill=INK, anchor="lt")
    d.text((M, y + 38), "neutre · curieux · fier · vexé", font=f_lbl2, fill=GREY, anchor="lt")
    d.text((M, y + 66), "endormi · crieur · complice · surpris", font=f_lbl2, fill=GREY, anchor="lt")
    d.text((W - M, y + 4), "Jacques_tetes_v0", font=f_lbl2, fill=GREY, anchor="rt")
    tw = int((W - 2 * M) * 0.62); tt = tetes.resize((tw, tet_h), Image.LANCZOS)
    im.paste(tt, ((W - tw) // 2, y + 10))
    y += tet_h + 60
    foot = ("Maquette d'étude : le Jacques est ici généré avec Magnific (2 k) à partir de la seule description écrite de la fiche de personnage "
            "(sections 2 à 5) — aucune photographie ni dessin d'autrui n'a été donné au générateur ; la planche A sert d'image de référence "
            "aux passes B et C. La version définitive sera refaite à partir des photographies de geais de l'auteur (fiche de prises de vue, "
            "point E) et gelée sous le nom Jacques_modele_v1, puis déposée avec la marque. Contrôle (fiche, section 10) : calotte striée, "
            "moustache, gorge blanche, iris pâle, panneau bleu barré sur l'aile seule, croupion blanc, queue noire, rien d'humain — "
            "réserves notées dans collection/jacques/README.md.")
    for i, ln in enumerate(wrap(d, foot, f_foot, W - 2 * M - 40)):
        d.text((W / 2, y + i * 28), ln, font=f_foot, fill=GREY, anchor="mt")
    im.save(OUT + "Jacques_planche_v0.png", dpi=(200, 200))
    im.save(OUT + "Jacques_planche_v0.pdf", resolution=200.0)
    print("planche", im.size)


if __name__ == "__main__":
    main()
