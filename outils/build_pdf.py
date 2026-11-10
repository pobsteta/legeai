# -*- coding: utf-8 -*-
"""Construit le PDF de relecture d'une livraison de texte (manuscrit de travail) à partir du markdown.

Usage :
    python3 outils/build_pdf.py SRC.md OUT.pdf [--tome "Tome 1"] [--titre "Le Chêne"]
        [--sous-titre "La vie secrète du roi de nos forêts"]
        [--livraison "Texte, livraison 1 — pages 1 à 27"]
        [--contenu "Ouverture · Reconnaître · ..."] [--date "8 novembre 2026"]

Conventions attendues dans le markdown : voir collection/02-charte-de-style.md et
tomes/01-le-chene/texte/livraison-1-p01-27.md (## Page N — titre, **[Regard]**, **[Bulle]**,
**[Parole du Jacques]**, **[Légende]**, **[Encadré — titre]**, **(n)** notes).
Un encadré long s'ouvre par **[Encadré — titre]** seul sur sa ligne : les paragraphes qui
suivent lui appartiennent jusqu'au prochain marqueur, note, titre ou séparateur ---.
"""
import re
import argparse
from reportlab import rl_config
rl_config.useA85 = 0  # pas d'encodage ASCII85 des images : PDF un quart plus léger
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER
from reportlab.platypus import (KeepInFrame, BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer,
                                PageBreak, Table, TableStyle, KeepTogether, ListFlowable,
                                ListItem, HRFlowable)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

ap = argparse.ArgumentParser(description="PDF de relecture d'une livraison Le Geai")
ap.add_argument("src", help="fichier markdown de la livraison")
ap.add_argument("out", help="fichier PDF à produire")
ap.add_argument("--tome", default="Tome 1")
ap.add_argument("--titre", default="Le Chêne")
ap.add_argument("--sous-titre", dest="sous_titre", default="La vie secrète du roi de nos forêts")
ap.add_argument("--livraison", default="Texte, livraison 1 — pages 1 à 27")
ap.add_argument("--contenu", default="Ouverture · Reconnaître · Qui êtes-vous ? · L'année (printemps, été, automne, hiver)")
ap.add_argument("--date", default="8 novembre 2026")
# --- Maquette illustrée ---
ap.add_argument("--illustre", action="store_true",
                help="maquette illustrée : images existantes en place, cadres « image à produire », le Jacques à chaque bulle")
ap.add_argument("--images", default=None, help="JSON page → images existantes (défaut : tomes/01-le-chene/maquette/images.json)")
ap.add_argument("--poses", default=None, help="JSON page → attitude du Jacques (défaut : tomes/01-le-chene/maquette/poses.json)")
ap.add_argument("--entete", default=None, help="mention d'en-tête (défaut : « Manuscrit de travail », ou « Maquette de relecture illustrée » avec --illustre)")
ap.add_argument("--sans-couverture", dest="sans_couverture", action="store_true", help="ne pas produire la page de couverture")
ap.add_argument("--premiere-page", dest="premiere_page", type=int, default=1, help="numéro de la première page du PDF (pour assembler plusieurs livraisons)")
ap.add_argument("--kdp", action="store_true",
                help="format du livre imprimé (KDP) : 7 × 10 pouces, marges miroir, corps 11 pt, sans en-tête de relecture, sans annexes ni notes d'image provisoire")
ap.add_argument("--format", default="7x10", choices=["7x10", "8x10", "8.25x11", "8.5x11"],
                help="format KDP en pouces (largeur x hauteur), avec --kdp")
ap.add_argument("--double", action="store_true",
                help="avec --kdp : chaque page du chemin de fer devient une double page et commence sur une page paire (gauche)")
ap.add_argument("--notes-fin", dest="notes_fin", default=None,
                help="avec --kdp : JSON des notes des livraisons précédentes ; ajoute la section « Notes » en fin de volume")
ap.add_argument("--note-couverture", dest="note_couverture", default=None, help="paragraphe ajouté au cadre de conventions de la couverture")
ARGS = ap.parse_args()
SRC, OUT, DATE = ARGS.src, ARGS.out, ARGS.date

import os, json, tempfile
REPO = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
ENTETE = ARGS.entete or ("Maquette de relecture illustrée" if ARGS.illustre else "Manuscrit de travail")


def _load_json(path, default_rel):
    p = path or os.path.join(REPO, default_rel)
    if not os.path.exists(p):
        return {}
    with open(p, encoding="utf-8") as f:
        d = json.load(f)
    d.pop("_doc", None)
    return d


IMAGES = _load_json(ARGS.images, "tomes/01-le-chene/maquette/images.json") if ARGS.illustre else {}
POSES = _load_json(ARGS.poses, "tomes/01-le-chene/maquette/poses.json") if ARGS.illustre else {}

# Les douze attitudes du Jacques (planche modèle v0) : identifiant → (fichier détouré, côté du bec g/d)
JACQUES_DIR = os.path.join(REPO, "collection", "jacques", "vignettes")
JACQUES_POSES = {
    "J1": ("Jacques_J01_guetteur_v0.png", "d"), "J2": ("Jacques_J02_porteur_v0.png", "d"),
    "J3": ("Jacques_J03_planteur_v0.png", "g"), "J4": ("Jacques_J04_chercheur_v0.png", "g"),
    "J5": ("Jacques_J05_en-vol_v0.png", "d"), "J6": ("Jacques_J06_vantard_v0.png", "d"),
    "J7": ("Jacques_J07_vexe_v0.png", "d"), "J8": ("Jacques_J08_dubitatif_v0.png", "d"),
    "J9": ("Jacques_J09_sentinelle_v0.png", "d"), "J10": ("Jacques_J10_gourmand_v0.png", "d"),
    "J11": ("Jacques_J11_patient_v0.png", "d"), "J12": ("Jacques_J12_scribe_v0.png", "d"),
}
POSE_CYCLE = ["J1", "J8", "J6", "J2", "J7", "J11", "J9", "J4", "J3", "J5", "J10", "J12"]

# ---------- Polices ----------
FD = "/usr/share/fonts/truetype/crosextra/"
pdfmetrics.registerFont(TTFont("Caladea", FD + "Caladea-Regular.ttf"))
pdfmetrics.registerFont(TTFont("Caladea-Italic", FD + "Caladea-Italic.ttf"))
pdfmetrics.registerFont(TTFont("Caladea-Bold", FD + "Caladea-Bold.ttf"))
pdfmetrics.registerFont(TTFont("Caladea-BoldItalic", FD + "Caladea-BoldItalic.ttf"))
pdfmetrics.registerFontFamily("Caladea", normal="Caladea", bold="Caladea-Bold",
                              italic="Caladea-Italic", boldItalic="Caladea-BoldItalic")
pdfmetrics.registerFont(TTFont("Carlito", FD + "Carlito-Regular.ttf"))
pdfmetrics.registerFont(TTFont("Carlito-Italic", FD + "Carlito-Italic.ttf"))
pdfmetrics.registerFont(TTFont("Carlito-Bold", FD + "Carlito-Bold.ttf"))
pdfmetrics.registerFont(TTFont("Carlito-BoldItalic", FD + "Carlito-BoldItalic.ttf"))
pdfmetrics.registerFontFamily("Carlito", normal="Carlito", bold="Carlito-Bold",
                              italic="Carlito-Italic", boldItalic="Carlito-BoldItalic")
# Patrick Hand (OFL) : la police des bulles du Jacques, choisie dans la charte
_PH = os.path.join(REPO, "collection", "jacques", "PatrickHand-Regular.ttf")
HAS_PATRICK = os.path.exists(_PH)
if HAS_PATRICK:
    pdfmetrics.registerFont(TTFont("PatrickHand", _PH))
    pdfmetrics.registerFontFamily("PatrickHand", normal="PatrickHand", bold="PatrickHand",
                                  italic="PatrickHand", boldItalic="PatrickHand")

# ---------- Couleurs ----------
GREEN = colors.HexColor("#2E5339")
OCHRE = colors.HexColor("#8F6418")
JACQUES_BG = colors.HexColor("#FBF3DF")
REGARD_BG = colors.HexColor("#EEF1EA")
PLACE_BG = colors.HexColor("#F7F7F4")
GREY = colors.HexColor("#6A6A66")
DARK = colors.HexColor("#222222")
RULE = colors.HexColor("#B9BDB2")
FLAG = colors.HexColor("#A3392B")

# ---------- Styles ----------
body = ParagraphStyle("body", fontName="Caladea", fontSize=10.5, leading=15,
                      alignment=TA_JUSTIFY, spaceAfter=5, textColor=DARK)
body_center = ParagraphStyle("body_center", parent=body, alignment=TA_CENTER, spaceAfter=3)
regard = ParagraphStyle("regard", parent=body, fontName="Caladea-Italic", textColor=colors.HexColor("#2F3A31"),
                        spaceAfter=0)
jacques = ParagraphStyle("jacques", fontName="Carlito", fontSize=10, leading=13.5,
                         alignment=TA_LEFT, textColor=DARK, spaceAfter=0)
legende = ParagraphStyle("legende", fontName="Carlito-Italic", fontSize=9, leading=12,
                         alignment=TA_LEFT, textColor=GREY, spaceAfter=0)
encadre = ParagraphStyle("encadre", parent=body, fontSize=10, leading=13.5, spaceAfter=0)
note = ParagraphStyle("note", fontName="Caladea", fontSize=8.5, leading=11, alignment=TA_LEFT,
                      textColor=colors.HexColor("#333333"), leftIndent=16, firstLineIndent=-16, spaceAfter=2)
if ARGS.kdp:  # charte : texte courant 11 pt minimum, notes 9 pt
    body.fontSize, body.leading = 11, 14.6
    note.fontSize, note.leading = 9, 11.4
    encadre.fontSize, encadre.leading = 10.5, 14
label = ParagraphStyle("label", fontName="Carlito-Bold", fontSize=7.5, leading=9, textColor=GREY, spaceAfter=2)
label_ochre = ParagraphStyle("label_ochre", parent=label, textColor=OCHRE)
label_green = ParagraphStyle("label_green", parent=label, textColor=GREEN)
h_pagenum = ParagraphStyle("h_pagenum", fontName="Carlito", fontSize=9, leading=11, textColor=GREY, spaceAfter=1)
h_page = ParagraphStyle("h_page", fontName="Carlito-Bold", fontSize=16, leading=19, textColor=GREEN, spaceAfter=8)
h_sub = ParagraphStyle("h_sub", fontName="Caladea-Bold", fontSize=12, leading=15, textColor=DARK,
                       spaceBefore=8, spaceAfter=4)
season = ParagraphStyle("season", fontName="Carlito-Bold", fontSize=9.5, leading=12, textColor=colors.white)
cover_small = ParagraphStyle("cover_small", fontName="Carlito-Bold", fontSize=11, leading=14, textColor=OCHRE,
                             alignment=TA_CENTER)
cover_title = ParagraphStyle("cover_title", fontName="Caladea-Bold", fontSize=34, leading=40, textColor=GREEN,
                             alignment=TA_CENTER, spaceBefore=6)
cover_sub = ParagraphStyle("cover_sub", fontName="Caladea-Italic", fontSize=14, leading=18, textColor=DARK,
                           alignment=TA_CENTER, spaceBefore=4)
cover_meta = ParagraphStyle("cover_meta", fontName="Carlito", fontSize=10.5, leading=14, textColor=GREY,
                            alignment=TA_CENTER, spaceBefore=2)
cover_body = ParagraphStyle("cover_body", parent=body, fontSize=10, leading=14)


# ---------- Mise en forme en ligne ----------
def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def french_spaces(s):
    s = re.sub(r" ([:;!?»])", " \\1", s)
    s = s.replace("« ", "« ")
    return s


def inline(s, flag_brackets=True, superscript_refs=True):
    s = esc(s)
    s = french_spaces(s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s)
    s = re.sub(r"\*(.+?)\*", r"<i>\1</i>", s)
    if flag_brackets:
        s = re.sub(r"\[([^\]]*)\]", r'<font color="#A3392B">[\1]</font>', s)
    if superscript_refs:
        s = re.sub(r" ?\((\d)\)", r'<super><font size="7">\1</font></super>', s)
    return s


# ---------- Encadrés ----------
def box(flowables, bg=None, left_bar=None, border=None, pad=7, width=None):
    t = Table([[flowables]], colWidths=[width] if width else None)
    st = [("VALIGN", (0, 0), (-1, -1), "TOP"),
          ("LEFTPADDING", (0, 0), (-1, -1), pad + (4 if left_bar else 0)),
          ("RIGHTPADDING", (0, 0), (-1, -1), pad),
          ("TOPPADDING", (0, 0), (-1, -1), pad - 1),
          ("BOTTOMPADDING", (0, 0), (-1, -1), pad)]
    if bg is not None:
        st.append(("BACKGROUND", (0, 0), (-1, -1), bg))
    if left_bar is not None:
        st.append(("LINEBEFORE", (0, 0), (0, -1), 2.2, left_bar))
    if border is not None:
        st.append(("BOX", (0, 0), (-1, -1), 0.6, border))
    t.setStyle(TableStyle(st))
    return t


def regard_box(text, W):
    return [box([Paragraph("REGARD", label_green), Paragraph(inline(text), regard)],
                bg=REGARD_BG, left_bar=GREEN, width=W), Spacer(1, 7)]


def jacques_box(text, W, kind="Bulle"):
    lab = "LE JACQUES — BULLE" if kind == "Bulle" else "PAROLE DU JACQUES"
    return [KeepTogether(box([Paragraph(lab, label_ochre), Paragraph(inline(text), jacques)],
                             bg=JACQUES_BG, width=W)), Spacer(1, 6)]


def legende_box(text, W):
    return [KeepTogether(box([Paragraph("LÉGENDE", label), Paragraph(inline(text), legende)],
                             left_bar=RULE, pad=5, width=W)), Spacer(1, 6)]


def encadre_box(title, text, W):
    """text : une chaîne (un paragraphe) ou une liste de paragraphes (encadré long,
    ouvert par un marqueur **[Encadré — titre]** sans texte sur la même ligne)."""
    inner = [Paragraph("ENCADRÉ", label)]
    if title:
        inner.append(Paragraph(inline(title), ParagraphStyle("et", parent=encadre, fontName="Caladea-Bold", spaceAfter=2)))
    paras = text if isinstance(text, list) else [text]
    for i, t in enumerate(paras):
        inner.append(Paragraph(inline(t), ParagraphStyle("ep%d" % i, parent=encadre, spaceAfter=3 if i < len(paras) - 1 else 0)))
    return [KeepTogether(box(inner, border=RULE, width=W)), Spacer(1, 7)]


def placeholder_box(kind, text, W):
    return [KeepTogether(box([Paragraph(kind.upper(), label), Paragraph(inline(text), legende)],
                             bg=PLACE_BG, border=RULE, pad=5, width=W)), Spacer(1, 6)]


# ---------- Maquette illustrée ----------
from reportlab.platypus import Flowable, Image as RLImage
from reportlab.lib.utils import ImageReader

bulle_style = ParagraphStyle("bulle", fontName="PatrickHand" if HAS_PATRICK else "Carlito",
                             fontSize=12.5, leading=15.5, textColor=DARK, alignment=TA_LEFT)
parole_style = ParagraphStyle("parole", parent=bulle_style, fontSize=11.5, leading=14.5)
note_image = ParagraphStyle("note_image", parent=legende, textColor=OCHRE, fontName="Carlito")


_VIGNETTES = {}


def vignette_reader(pose, max_h_px=420):
    """Un seul ImageReader par attitude (copie réduite, PNG à transparence), réutilisé pour toutes les bulles :
    une image dans le PDF par attitude au lieu d'une par bulle."""
    if pose not in _VIGNETTES:
        fichier, _ = JACQUES_POSES[pose]
        src = os.path.join(JACQUES_DIR, fichier)
        try:
            from PIL import Image as PILImage
            os.makedirs(_CACHE, exist_ok=True)
            out = os.path.join(_CACHE, fichier[:-4] + "_%dpx.png" % max_h_px)
            if not os.path.exists(out):
                im = PILImage.open(src).convert("RGBA")
                im.thumbnail((max_h_px * 2, max_h_px), PILImage.LANCZOS)
                im.save(out, "PNG", optimize=True)
            _VIGNETTES[pose] = ImageReader(out)
        except Exception:
            _VIGNETTES[pose] = ImageReader(src)
    return _VIGNETTES[pose]


class JacquesBulle(Flowable):
    """Le Jacques détouré et sa bulle vectorielle (Patrick Hand), côte à côte sur la largeur du texte.
    La bulle n'est jamais générée dans l'image : elle est dessinée ici, à la mise en page."""

    def __init__(self, text, pose, W, kind="Bulle"):
        Flowable.__init__(self)
        fichier, cote = JACQUES_POSES[pose]
        self.img = vignette_reader(pose)
        self.cote = cote  # bec à droite ('d') : oiseau à gauche, bulle à droite ; 'g' : l'inverse
        self.W = W
        self.kind = kind
        self.vh = (30 if kind == "Bulle" else 38) * mm
        iw, ih = self.img.getSize()
        self.vw = self.vh * iw / ih
        self.gap, self.tail, self.pad = 4 * mm, 6 * mm, 4 * mm
        txt = text.strip()
        txt = re.sub(r"^«\s*", "", txt); txt = re.sub(r"\s*»$", "", txt)
        self.para = Paragraph(inline(txt), bulle_style if kind == "Bulle" else parole_style)
        self.bw = self.W - self.vw - self.gap - self.tail
        _, ph = self.para.wrap(self.bw - 2 * self.pad, 10000)
        self.bh = ph + 2 * self.pad
        self.height = max(self.vh, self.bh) + 2 * mm

    def wrap(self, aw, ah):
        return (self.W, self.height)

    def draw(self):
        c = self.canv
        if self.cote == "d":
            xv, xb = 0, self.vw + self.gap + self.tail
        else:
            xb, xv = 0, self.bw + self.tail + self.gap
        yv = 0
        yb = max(0, (self.vh - self.bh) / 2) if self.bh < self.vh else 0
        c.drawImage(self.img, xv, yv, self.vw, self.vh, mask="auto", preserveAspectRatio=True)
        c.setFillColor(JACQUES_BG); c.setStrokeColor(OCHRE); c.setLineWidth(0.9)
        c.roundRect(xb, yb, self.bw, self.bh, 3 * mm, stroke=1, fill=1)
        # la queue de la bulle vise la tête de l'oiseau (vers 72 % de sa hauteur)
        yh = yv + 0.72 * self.vh
        y1 = min(max(yh - 4 * mm, yb + 3 * mm), yb + self.bh - 9 * mm)
        y2 = y1 + 6 * mm
        p = c.beginPath()
        if self.cote == "d":
            p.moveTo(xb, y1); p.lineTo(xb - self.tail, yh); p.lineTo(xb, y2)
            c.drawPath(p, stroke=1, fill=1)
            c.setStrokeColor(JACQUES_BG); c.setLineWidth(1.6); c.line(xb, y1 + 0.6, xb, y2 - 0.6)
        else:
            xr = xb + self.bw
            p.moveTo(xr, y1); p.lineTo(xr + self.tail, yh); p.lineTo(xr, y2)
            c.drawPath(p, stroke=1, fill=1)
            c.setStrokeColor(JACQUES_BG); c.setLineWidth(1.6); c.line(xr, y1 + 0.6, xr, y2 - 0.6)
        self.para.drawOn(c, xb + self.pad, yb + self.pad)


def jacques_illustre(text, W, kind, page_key, counter):
    """Choisit l'attitude (poses.json, sinon cycle) et renvoie le flowable composite."""
    spec = POSES.get(page_key)
    pose = None
    if isinstance(spec, dict):
        pose = spec.get("P" if kind == "Parole" else "B")
    elif isinstance(spec, str):
        pose = spec
    if pose not in JACQUES_POSES:
        pose = POSE_CYCLE[counter % len(POSE_CYCLE)]
    lab = Paragraph("PAROLE DU JACQUES", label_ochre) if kind == "Parole" else None
    out = [lab] if lab else []
    out += [JacquesBulle(text, pose, W, kind), Spacer(1, 7)]
    return [KeepTogether(out)]


_CACHE = os.path.join(tempfile.gettempdir(), "legeai_maquette_cache")


def _leger(f, max_px=1600):
    """Copie JPEG allégée d'un PNG opaque (planches, figures) pour la maquette de relecture ; les PNG à transparence
    et les JPEG sont pris tels quels. Le fichier d'origine n'est jamais modifié."""
    if not f.lower().endswith(".png"):
        return f
    try:
        from PIL import Image as PILImage
        im = PILImage.open(f)
        if im.mode in ("RGBA", "LA") or "transparency" in im.info:
            return f
        os.makedirs(_CACHE, exist_ok=True)
        out = os.path.join(_CACHE, os.path.basename(f)[:-4] + "_%d.jpg" % os.path.getmtime(f))
        if not os.path.exists(out):
            im = im.convert("RGB")
            if max(im.size) > max_px:
                im.thumbnail((max_px, max_px), PILImage.LANCZOS)
            im.save(out, "JPEG", quality=88, optimize=True)
        return out
    except Exception:
        return f


def _fit(f, max_w, max_h):
    f = _leger(f)
    iw, ih = ImageReader(f).getSize()
    w, h = max_w, max_w * ih / iw
    if h > max_h:
        w, h = max_h * iw / ih, max_h
    return RLImage(f, width=w, height=h)


def image_zone(page_key, legende_text, W, max_h=None, zone=0, pleine=False):
    if max_h is None:
        max_h = (100 * KDP_ECHELLE if ARGS.kdp else 118) * mm
    """Image(s) existante(s) de la page + légende ; sinon cadre gris « image à produire » portant la légende (le brief).
    images.json : liste de fichiers, ou objet {fichiers, note, hauteur_mm, empiler, une_par_page}, ou {zones: [...]}
    quand la page a plusieurs emplacements d'image (zone = rang de l'emplacement dans la page)."""
    spec = IMAGES.get(page_key)
    if isinstance(spec, dict) and "zones" in spec:
        zones = spec["zones"]
        spec = zones[zone] if zone < len(zones) else None
    note = None
    files = []
    empiler = une_par_page = False
    if isinstance(spec, dict):
        files, note = spec.get("fichiers", []), spec.get("note")
        empiler, une_par_page = bool(spec.get("empiler")), bool(spec.get("une_par_page"))
        if pleine:
            empiler, une_par_page = len(spec.get("fichiers", [])) > 1, False
        elif spec.get("hauteur_mm"):
            max_h = float(spec["hauteur_mm"]) * mm * (0.82 * KDP_ECHELLE if ARGS.kdp else 1)
    elif isinstance(spec, list):
        files = spec
        empiler = pleine and len(files) > 1
    files = [os.path.join(REPO, f) for f in files if os.path.exists(os.path.join(REPO, f))]
    out = []
    leg = box([Paragraph("LÉGENDE", label), Paragraph(inline(legende_text), legende)], left_bar=RULE, pad=5, width=W)
    if files and une_par_page:
        # chaque image sur sa propre page, pleine hauteur ; la légende sous la dernière
        flow = []
        for i, f in enumerate(files):
            flow.append(PageBreak())
            img = _fit(f, W, ((186 * KDP_ECHELLE if i == len(files) - 1 else 205 * KDP_ECHELLE) if ARGS.kdp else (228 if i == len(files) - 1 else 252)) * mm)
            img.hAlign = "CENTER"
            flow.append(img)
        if note:
            if not ARGS.kdp:
                flow += [Spacer(1, 3), Paragraph("<b>Image provisoire —</b> " + inline(note), note_image)]
        flow += [Spacer(1, 4), leg, Spacer(1, 7)]
        return flow
    if files:
        n = len(files)
        gap = 5 * mm
        if empiler:
            for f in files:
                img = _fit(f, W, (max_h - 4 * (len(files) - 1)) / len(files) if pleine else max_h); img.hAlign = "CENTER"
                out += [img, Spacer(1, 4)]
        else:
            cw = (W - gap * (n - 1)) / n
            cells = [_fit(f, cw, max_h) for f in files]
            t = Table([cells], colWidths=[cw] * n, hAlign="CENTER")
            t.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "BOTTOM"), ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                                   ("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                                   ("TOPPADDING", (0, 0), (-1, -1), 0), ("BOTTOMPADDING", (0, 0), (-1, -1), 3)]))
            out.append(t)
        if note:
            if not ARGS.kdp:
                out.append(Paragraph("<b>Image provisoire —</b> " + inline(note), note_image))
            out.append(Spacer(1, 2))
        out.append(leg)
    else:
        inner = [Paragraph("IMAGE À PRODUIRE — PAGE %s" % page_key, label_ochre),
                 Spacer(1, 16 * mm),
                 Paragraph("<i>Brief :</i> " + inline(legende_text), legende),
                 Spacer(1, 12 * mm)]
        out.append(box(inner, bg=PLACE_BG, border=RULE, pad=8, width=W))
    return [KeepTogether(out), Spacer(1, 7)]


def season_banner(name, W):
    t = Table([[Paragraph(name, season)]], colWidths=[W])
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), GREEN),
                           ("LEFTPADDING", (0, 0), (-1, -1), 8), ("TOPPADDING", (0, 0), (-1, -1), 3),
                           ("BOTTOMPADDING", (0, 0), (-1, -1), 4)]))
    return [t, Spacer(1, 8)]


def notes_block(notes):
    out = [Spacer(1, 4), HRFlowable(width="30%", thickness=0.5, color=RULE, hAlign="LEFT"), Spacer(1, 3)]
    for n in notes:
        m = re.match(r"^\*\*\((\d+)\)\*\*\s*(.*)$", n)
        num, txt = m.group(1), m.group(2)
        out.append(Paragraph("<b>(%s)</b> %s" % (num, inline(txt, superscript_refs=False)), note))
    out.append(Spacer(1, 6))
    return [KeepTogether(out)]


# ---------- Analyse du markdown ----------
def parse(md):
    """Retourne une liste de blocs (type, data)."""
    blocks = []
    para = []
    lst = None  # (kind, items)
    pending_regard = False
    title_mode = False
    open_enc = None  # liste des paragraphes d'un encadré long en cours

    def flush_para():
        nonlocal para, pending_regard
        if para:
            text = " ".join(para).strip()
            if pending_regard:
                blocks.append(("regard", text))
                pending_regard = False
            elif open_enc is not None:
                open_enc.append(text)
            else:
                blocks.append(("para", text))
            para = []

    def flush_list():
        nonlocal lst
        if lst:
            blocks.append(("list", lst))
            lst = None

    for raw in md.splitlines():
        line = raw.rstrip()
        if not line.strip():
            flush_para(); flush_list(); continue
        if line.strip() == "---":
            flush_para(); flush_list(); open_enc = None; continue
        if line.startswith("# "):
            flush_para(); flush_list(); open_enc = None; blocks.append(("doctitle", line[2:].strip())); continue
        if line.startswith("## ") or line.startswith("### "):
            flush_para(); flush_list(); open_enc = None
            text = line.lstrip("#").strip()
            if re.match(r"^Pages? [\d\-]+ — ", text):
                blocks.append(("page", text))
                title_mode = text.startswith("Page 1 —")
            elif text.startswith("Annexe"):
                blocks.append(("page", text)); title_mode = False
            elif line.startswith("## "):
                blocks.append(("season", text)); title_mode = False
            else:
                blocks.append(("sub", text))
            continue
        m = re.match(r"^\*\*\[([^\]]+)\]\*\*\s*(.*)$", line)
        if m:
            flush_para(); flush_list(); open_enc = None
            kind, rest = m.group(1), m.group(2)
            if kind == "Regard":
                pending_regard = True
                if rest:
                    para.append(rest)
            elif kind.startswith("Encadré") and not rest:
                open_enc = []
                blocks.append(("marker", (kind, open_enc)))
            else:
                blocks.append(("marker", (kind, rest)))
            continue
        if re.match(r"^\*\*\(\d+\)\*\*", line):
            flush_para(); flush_list(); open_enc = None
            if blocks and blocks[-1][0] == "notes":
                blocks[-1][1].append(line)
            else:
                blocks.append(("notes", [line]))
            continue
        m = re.match(r"^(\d+)\. (.*)$", line)
        if m:
            flush_para()
            if lst is None or lst[0] != "num":
                flush_list(); lst = ("num", [])
            lst[1].append(m.group(2)); continue
        if line.startswith("- "):
            flush_para()
            if lst is None or lst[0] != "bul":
                flush_list(); lst = ("bul", [])
            lst[1].append(line[2:]); continue
        # ligne de texte ordinaire
        flush_list()
        if title_mode:
            blocks.append(("titleline", line.strip()))
        else:
            para.append(line.strip())
    flush_para(); flush_list()
    return blocks


# ---------- Calibrage KDP ----------
from reportlab.platypus.flowables import Flowable, DocIf
KDP_L, KDP_H = (float(x) for x in ARGS.format.split("x"))
KDP_ECHELLE = float(os.environ.get("KDP_ECHELLE_IMAGES", KDP_H / 10))  # hauteur des images (référence 7 × 10 = 1)
NOTES_FIN = []  # (clé de page, lignes de notes) — renvoyées en fin de volume en KDP
CALIBRAGE = []  # (clé de page du livre, page physique où elle commence)


class MarquePage(Flowable):
    """Repère invisible : note la page physique où commence une page du livre."""
    def __init__(self, cle):
        super().__init__(); self.cle = cle; self.width = self.height = 0

    def wrap(self, aw, ah):
        return 0, 0

    def draw(self):
        CALIBRAGE.append((self.cle, self.canv.getPageNumber() + ARGS.premiere_page - 1))


# ---------- Construction ----------
def build():
    md = open(SRC, encoding="utf-8").read()
    blocks = parse(md)

    if ARGS.kdp:
        # KDP, 7 × 10 pouces (17,78 × 25,4 cm), sans fond perdu ; marges miroir au-delà des minimums KDP
        # (intérieur ≥ 0,375 po soit 9,5 mm pour 24 à 150 pages ; extérieur ≥ 0,25 po soit 6,4 mm)
        PAGE_W, PAGE_H = KDP_L * 72, KDP_H * 72
        IN_M, OUT_M = 17 * mm, 13 * mm
        TM, BM = 14 * mm, 16 * mm
        LM, RM = IN_M, OUT_M
    else:
        PAGE_W, PAGE_H = A4
        LM = RM = 22 * mm
        TM, BM = 20 * mm, 17 * mm
    W = PAGE_W - LM - RM

    def on_page(canv, doc):
        canv.saveState()
        if ARGS.kdp:
            n = doc.page + ARGS.premiere_page - 1
            canv.setFont("Carlito", 9); canv.setFillColor(GREY)
            if n % 2:  # page impaire = belle page, à droite : folio à l'extérieur droit
                canv.drawRightString(PAGE_W - OUT_M, 9 * mm, str(n))
            else:
                canv.drawString(OUT_M, 9 * mm, str(n))
            canv.restoreState()
            return
        if doc.page > 1 or ARGS.sans_couverture:
            canv.setFont("Carlito", 8.5); canv.setFillColor(GREY)
            canv.drawString(LM, PAGE_H - 13 * mm, "LE GEAI · %s · %s — %s" % (ARGS.tome, ARGS.titre, ARGS.livraison))
            canv.drawRightString(PAGE_W - RM, PAGE_H - 13 * mm,
                                 DATE if ARGS.livraison.startswith(ENTETE) else ENTETE + " — " + DATE)
            canv.setStrokeColor(RULE); canv.setLineWidth(0.5)
            canv.line(LM, PAGE_H - 15 * mm, PAGE_W - RM, PAGE_H - 15 * mm)
            canv.setFont("Carlito", 9)
            canv.drawCentredString(PAGE_W / 2, 11 * mm, str(doc.page + ARGS.premiere_page - 1))
        canv.restoreState()

    if ARGS.kdp:
        odd_first = ARGS.premiere_page % 2 == 1
        f_odd = Frame(IN_M, BM, W, PAGE_H - TM - BM, id="fo", leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
        f_even = Frame(OUT_M, BM, W, PAGE_H - TM - BM, id="fe", leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
        t_odd = PageTemplate(id="impaire", frames=[f_odd], onPage=on_page, autoNextPageTemplate="paire")
        t_even = PageTemplate(id="paire", frames=[f_even], onPage=on_page, autoNextPageTemplate="impaire")
        templates = [t_odd, t_even] if odd_first else [t_even, t_odd]
    else:
        frame = Frame(LM, BM, W, PAGE_H - TM - BM, id="f", leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
        templates = [PageTemplate(id="p", frames=[frame], onPage=on_page)]
    doc = BaseDocTemplate(OUT, pagesize=(PAGE_W, PAGE_H), pageTemplates=templates,
                          title="Le Geai — %s : %s — %s" % (ARGS.tome, ARGS.titre, ARGS.livraison),
                          author="Collection Le Geai", subject=ENTETE, lang="fr")

    story = []
    # --- Couverture ---
    intro_paras = [b[1] for b in blocks if b[0] == "para"][:2]  # les deux paragraphes d'introduction
    if not ARGS.sans_couverture:
      story += [Spacer(1, 55 * mm),
              Paragraph("LE GEAI — ARBRES &amp; ARBUSTES DE FRANCE", cover_small),
              Paragraph(esc(ARGS.tome), cover_meta),
              Paragraph(esc(ARGS.titre), cover_title),
              Paragraph(esc(ARGS.sous_titre), cover_sub),
              Spacer(1, 10 * mm),
              Paragraph(esc(ARGS.livraison), ParagraphStyle("c3", parent=cover_meta, fontSize=12.5, leading=16, textColor=DARK)),
              Paragraph(esc(ARGS.contenu), cover_meta),
              Paragraph(ENTETE + " — " + DATE, cover_meta),
              Spacer(1, 18 * mm)]
      conv = [Paragraph("CONVENTIONS ET ÉTAT DU SOURÇAGE", label_green)]
      if ARGS.note_couverture:
          conv.append(Paragraph(inline(ARGS.note_couverture), cover_body))
      for p in intro_paras:
          txt = p.strip("*")
          conv.append(Paragraph(inline(txt), cover_body))
      story.append(box(conv, bg=REGARD_BG, left_bar=GREEN, width=W))
      story.append(PageBreak())

    first_page_done = False
    pending_season = None
    intro_skipped = 0
    cur_page = None       # clé de page courante ('28', '4-5') pour la maquette illustrée
    jacques_count = 0     # compteur pour le cycle d'attitudes par défaut
    zone_idx = 0          # rang de l'emplacement d'image dans la page courante
    in_annexe = False
    SPREAD = ARGS.double and ARGS.kdp and ARGS.illustre
    droite = []  # emplacements d'image de la page courante, posés en pleine page à droite (mode double)

    def poser_droite():
        """Page de droite : les images de la page du livre, en pleine page, avec leurs légendes."""
        if not droite:
            return
        H = PAGE_H - TM - BM
        n = len(droite)
        h_zone = (H - n * 30 * mm) / n  # 30 mm par légende et espacement
        bloc = []
        courante = []
        for key, leg, z in droite:
            bloc.extend(image_zone(key, leg, W, max_h=h_zone, zone=z, pleine=True))
            courante.extend(image_zone(key, leg, W, zone=z))
        # la page de droite : le bloc image + légende centré verticalement
        plat = []
        for f in bloc:  # KeepTogether ne se dessine pas dans une cellule : on l'ouvre
            plat.extend(f._content if isinstance(f, KeepTogether) else [f])
        cadre = Table([[KeepInFrame(W, H - 4, plat, mode="shrink")]], colWidths=[W], rowHeights=[H - 4])
        cadre.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("LEFTPADDING", (0, 0), (-1, -1), 0),
                                   ("RIGHTPADDING", (0, 0), (-1, -1), 0), ("TOPPADDING", (0, 0), (-1, -1), 0),
                                   ("BOTTOMPADDING", (0, 0), (-1, -1), 0)]))
        pleine = [PageBreak(), cadre]
        # texte tenu sur la page de gauche (paire) : images en pleine page à droite ;
        # texte déjà passé à droite : images à leur taille courante, à la suite du texte
        story.append(DocIf("(doc.page + %d) %% 2 == 0" % (ARGS.premiere_page - 1), pleine, courante))
        droite.clear()

    for kind, data in blocks:
        if kind == "doctitle":
            continue
        if kind == "page" and ARGS.kdp:
            in_annexe = data.startswith("Annexe")
        if in_annexe:
            continue
        if kind == "para" and intro_skipped < 2 and not first_page_done:
            intro_skipped += 1
            continue
        if kind == "season":
            pending_season = data
            continue
        if kind == "page":
            if SPREAD:
                poser_droite()
            if ARGS.double and ARGS.kdp:
                # commencer sur une page paire : saut de page, puis un second si l'on tombe sur une impaire
                if first_page_done:
                    story.append(PageBreak())
                story.append(DocIf("(doc.page + %d) %% 2 == 1" % (ARGS.premiere_page - 1), [PageBreak()]))
            elif first_page_done:
                story.append(PageBreak())
            first_page_done = True
            if pending_season:
                story += season_banner(pending_season, W)
                pending_season = None
            m = re.match(r"^(Pages? [\d\-]+|Annexe) — (.*)$", data)
            cur_page = m.group(1).split(" ", 1)[1] if (m and m.group(1) != "Annexe") else None
            zone_idx = 0
            if ARGS.kdp and m:
                story.append(MarquePage(m.group(1).split(" ", 1)[1]))
            elif m:
                story.append(Paragraph(m.group(1).upper(), h_pagenum))
                story.append(Paragraph(inline(m.group(2), flag_brackets=False), h_page))
            else:
                story.append(Paragraph(inline(data), h_page))
            continue
        if kind == "sub":
            story.append(Paragraph(inline(data), h_sub))
            continue
        if kind == "titleline":
            story.append(Paragraph(inline(data), ParagraphStyle("tl", parent=body_center, fontSize=12, leading=17)))
            continue
        if kind == "para":
            story.append(Paragraph(inline(data), body))
            continue
        if kind == "regard":
            story += regard_box(data, W)
            continue
        if kind == "marker":
            mk, rest = data
            illustre = ARGS.illustre and cur_page is not None
            if mk == "Bulle":
                if illustre:
                    story += jacques_illustre(rest, W, "Bulle", cur_page, jacques_count); jacques_count += 1
                else:
                    story += jacques_box(rest, W, "Bulle")
            elif mk == "Parole du Jacques":
                if illustre:
                    story += jacques_illustre(rest, W, "Parole", cur_page, jacques_count); jacques_count += 1
                else:
                    story += jacques_box(rest, W, "Parole")
            elif mk == "Légende":
                if illustre and SPREAD:
                    droite.append((cur_page, rest, zone_idx)); zone_idx += 1
                elif illustre:
                    story += image_zone(cur_page, rest, W, zone=zone_idx); zone_idx += 1
                else:
                    story += legende_box(rest, W)
            elif mk.startswith("Encadré"):
                title = mk.split("—", 1)[1].strip() if "—" in mk else ""
                story += encadre_box(title, rest, W)
            elif mk in ("Image", "Carte") and illustre and SPREAD:
                droite.append((cur_page, mk + " : " + rest, zone_idx)); zone_idx += 1
            elif mk in ("Image", "Carte") and illustre:
                story += image_zone(cur_page, mk + " : " + rest, W, zone=zone_idx); zone_idx += 1
            else:  # Image, Carte, Sommaire
                story += placeholder_box(mk, rest, W)
            continue
        if kind == "notes" and ARGS.kdp:
            NOTES_FIN.append((cur_page, data))
            continue
        if kind == "notes":
            story += notes_block(data)
            continue
        if kind == "list":
            lk, items = data
            flow = [ListItem(Paragraph(inline(it), body), leftIndent=14) for it in items]
            kw = dict(bulletFontName="Caladea", bulletFontSize=10.5, leftIndent=14)
            if lk == "num":
                story.append(ListFlowable(flow, bulletType="1", start="1", bulletFormat="%s.", **kw))
            else:
                story.append(ListFlowable(flow, bulletType="bullet", **kw))
            story.append(Spacer(1, 4))
            continue

    if SPREAD:
        poser_droite()
    if ARGS.kdp and ARGS.notes_fin:
        precedentes = json.load(open(ARGS.notes_fin, encoding="utf-8"))
        toutes = [tuple(x) for x in precedentes] + NOTES_FIN
        story += [PageBreak(), MarquePage("Notes"), Paragraph("Notes", h_page),
                  Paragraph("Les sources de chaque page, dans l'ordre du livre. Le numéro entre "
                            "parenthèses renvoie à l'appel dans le texte.", note), Spacer(1, 6)]
        for cle, lignes in toutes:
            story.append(Paragraph("Page %s" % cle, h_sub))
            for n in lignes:
                m = re.match(r"^\*\*\((\d+)\)\*\*\s*(.*)$", n)
                story.append(Paragraph("<b>(%s)</b> %s" % (m.group(1), inline(m.group(2), superscript_refs=False)), note))
            story.append(Spacer(1, 3))
    doc.build(story)
    if ARGS.kdp:
        with open(OUT[:-4] + ".calibrage.json", "w", encoding="utf-8") as fh:
            json.dump({"pages_physiques": doc.page, "debuts": CALIBRAGE, "notes": NOTES_FIN}, fh, ensure_ascii=False)
    print("OK", OUT)


if __name__ == "__main__":
    build()
