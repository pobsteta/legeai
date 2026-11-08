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
"""
import re
import argparse
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer,
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
ARGS = ap.parse_args()
SRC, OUT, DATE = ARGS.src, ARGS.out, ARGS.date

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
    inner = [Paragraph("ENCADRÉ", label)]
    if title:
        inner.append(Paragraph(inline(title), ParagraphStyle("et", parent=encadre, fontName="Caladea-Bold", spaceAfter=2)))
    inner.append(Paragraph(inline(text), encadre))
    return [KeepTogether(box(inner, border=RULE, width=W)), Spacer(1, 7)]


def placeholder_box(kind, text, W):
    return [KeepTogether(box([Paragraph(kind.upper(), label), Paragraph(inline(text), legende)],
                             bg=PLACE_BG, border=RULE, pad=5, width=W)), Spacer(1, 6)]


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

    def flush_para():
        nonlocal para, pending_regard
        if para:
            text = " ".join(para).strip()
            if pending_regard:
                blocks.append(("regard", text))
                pending_regard = False
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
            flush_para(); flush_list(); continue
        if line.startswith("# "):
            flush_para(); flush_list(); blocks.append(("doctitle", line[2:].strip())); continue
        if line.startswith("## ") or line.startswith("### "):
            flush_para(); flush_list()
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
            flush_para(); flush_list()
            kind, rest = m.group(1), m.group(2)
            if kind == "Regard":
                pending_regard = True
                if rest:
                    para.append(rest)
            else:
                blocks.append(("marker", (kind, rest)))
            continue
        if re.match(r"^\*\*\(\d+\)\*\*", line):
            flush_para(); flush_list()
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


# ---------- Construction ----------
def build():
    md = open(SRC, encoding="utf-8").read()
    blocks = parse(md)

    PAGE_W, PAGE_H = A4
    LM = RM = 22 * mm
    TM, BM = 20 * mm, 17 * mm
    W = PAGE_W - LM - RM

    def on_page(canv, doc):
        canv.saveState()
        if doc.page > 1:
            canv.setFont("Carlito", 8.5); canv.setFillColor(GREY)
            canv.drawString(LM, PAGE_H - 13 * mm, "LE GEAI · %s · %s — %s" % (ARGS.tome, ARGS.titre, ARGS.livraison))
            canv.drawRightString(PAGE_W - RM, PAGE_H - 13 * mm, "Manuscrit de travail — " + DATE)
            canv.setStrokeColor(RULE); canv.setLineWidth(0.5)
            canv.line(LM, PAGE_H - 15 * mm, PAGE_W - RM, PAGE_H - 15 * mm)
            canv.setFont("Carlito", 9)
            canv.drawCentredString(PAGE_W / 2, 11 * mm, str(doc.page))
        canv.restoreState()

    frame = Frame(LM, BM, W, PAGE_H - TM - BM, id="f", leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
    doc = BaseDocTemplate(OUT, pagesize=A4, pageTemplates=[PageTemplate(id="p", frames=[frame], onPage=on_page)],
                          title="Le Geai — %s : %s — %s" % (ARGS.tome, ARGS.titre, ARGS.livraison),
                          author="Collection Le Geai", subject="Manuscrit de travail", lang="fr")

    story = []
    # --- Couverture ---
    intro_paras = [b[1] for b in blocks if b[0] == "para"][:2]  # les deux paragraphes d'introduction
    story += [Spacer(1, 55 * mm),
              Paragraph("LE GEAI — ARBRES &amp; ARBUSTES DE FRANCE", cover_small),
              Paragraph(esc(ARGS.tome), cover_meta),
              Paragraph(esc(ARGS.titre), cover_title),
              Paragraph(esc(ARGS.sous_titre), cover_sub),
              Spacer(1, 10 * mm),
              Paragraph(esc(ARGS.livraison), ParagraphStyle("c3", parent=cover_meta, fontSize=12.5, leading=16, textColor=DARK)),
              Paragraph(esc(ARGS.contenu), cover_meta),
              Paragraph("Manuscrit de travail — " + DATE, cover_meta),
              Spacer(1, 18 * mm)]
    conv = [Paragraph("CONVENTIONS ET ÉTAT DU SOURÇAGE", label_green)]
    for p in intro_paras:
        txt = p.strip("*")
        conv.append(Paragraph(inline(txt), cover_body))
    story.append(box(conv, bg=REGARD_BG, left_bar=GREEN, width=W))
    story.append(PageBreak())

    first_page_done = False
    pending_season = None
    intro_skipped = 0
    for kind, data in blocks:
        if kind == "doctitle":
            continue
        if kind == "para" and intro_skipped < 2 and not first_page_done:
            intro_skipped += 1
            continue
        if kind == "season":
            pending_season = data
            continue
        if kind == "page":
            if first_page_done:
                story.append(PageBreak())
            first_page_done = True
            if pending_season:
                story += season_banner(pending_season, W)
                pending_season = None
            m = re.match(r"^(Pages? [\d\-]+|Annexe) — (.*)$", data)
            if m:
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
            if mk == "Bulle":
                story += jacques_box(rest, W, "Bulle")
            elif mk == "Parole du Jacques":
                story += jacques_box(rest, W, "Parole")
            elif mk == "Légende":
                story += legende_box(rest, W)
            elif mk.startswith("Encadré"):
                title = mk.split("—", 1)[1].strip() if "—" in mk else ""
                story += encadre_box(title, rest, W)
            else:  # Image, Carte, Sommaire
                story += placeholder_box(mk, rest, W)
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

    doc.build(story)
    print("OK", OUT)


if __name__ == "__main__":
    build()
