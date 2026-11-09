# -*- coding: utf-8 -*-
"""Assemble la maquette de relecture illustrée du tome 1 : les livraisons de texte disponibles,
construites par build_pdf.py en mode --illustre, enchaînées dans un seul PDF numéroté en continu.

Usage :
    python3 outils/build_maquette.py [--date "9 novembre 2026"] [--out tomes/01-le-chene/pdf/maquette-illustree.pdf]

Ce que fait le mode illustré (voir build_pdf.py) :
  - les images déjà produites sont placées à leur page (tomes/01-le-chene/maquette/images.json) ;
  - là où l'image n'existe pas encore, un cadre gris « image à produire » porte la légende, qui sert de brief ;
  - le Jacques détouré (planche modèle v0, douze attitudes) est posé à chaque bulle et à chaque Parole,
    avec une bulle vectorielle en Patrick Hand (tomes/01-le-chene/maquette/poses.json).
"""
import argparse
import os
import subprocess
import sys
import tempfile

from pypdf import PdfReader, PdfWriter

REPO = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
TEXTE = os.path.join(REPO, "tomes", "01-le-chene", "texte")
BUILD = os.path.join(REPO, "outils", "build_pdf.py")

LIVRAISONS = [
    ("livraison-1-p01-27.md", "Ouverture · Reconnaître · Qui êtes-vous ? · L'année"),
    ("livraison-2-p28-45.md", "La vie (quatre âges) · Les habitants · Seul ou en forêt"),
    ("livraison-3-p46-53.md", "D'où il vient, où il va · L'arbre et nous"),
    ("livraison-4-p54-64.md", "Et vous ? · L'énigme · Chênes remarquables · Lexique, sources, courrier"),
]

NOTE = ("**Maquette illustrée.** Les images déjà produites sont en place (planches comparatives, Jacques v0) ; "
        "chaque cadre gris est une image à produire, et sa légende en est le brief. Le Jacques est posé à chaque "
        "bulle dans l'une des douze attitudes de sa planche modèle v0 — il sera remplacé par le Jacques v1 issu des "
        "photos de l'auteur ; les bulles sont vectorielles, composées en Patrick Hand (OFL), jamais générées dans l'image. "
        "Le format A4 est celui de la relecture, pas celui du livre.")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", default="9 novembre 2026")
    ap.add_argument("--out", default=os.path.join(REPO, "tomes", "01-le-chene", "pdf", "maquette-illustree.pdf"))
    args = ap.parse_args()

    parts = [(f, c) for f, c in LIVRAISONS if os.path.exists(os.path.join(TEXTE, f))]
    if not parts:
        sys.exit("aucune livraison trouvée dans " + TEXTE)
    pages = [p.split("-p")[1].split(".")[0] for p, _ in parts]  # '01-27', '28-45', ...
    debut, fin = pages[0].split("-")[0].lstrip("0"), pages[-1].split("-")[1]
    label = "Maquette de relecture illustrée — pages %s à %s" % (debut, fin)
    contenu = " · ".join(c.split(" · ")[0] for _, c in parts) + " · …"

    tmp = tempfile.mkdtemp(prefix="maquette_")
    writer = PdfWriter()
    offset = 1
    for i, (f, c) in enumerate(parts):
        out = os.path.join(tmp, f.replace(".md", ".pdf"))
        cmd = [sys.executable, BUILD, os.path.join(TEXTE, f), out, "--illustre",
               "--tome", "Tome 1", "--titre", "Le Chêne", "--sous-titre", "La vie secrète du roi de nos forêts",
               "--livraison", label, "--contenu", contenu, "--date", args.date,
               "--premiere-page", str(offset)]
        if i == 0:
            cmd += ["--note-couverture", NOTE]
        else:
            cmd += ["--sans-couverture"]
        subprocess.run(cmd, check=True, cwd=REPO)
        r = PdfReader(out)
        for pg in r.pages:
            writer.add_page(pg)
        offset += len(r.pages)
        print("  %s : %d pages" % (f, len(r.pages)))
    writer.add_metadata({"/Title": "Le Geai — Tome 1 : Le Chêne — " + label, "/Author": "Collection Le Geai"})
    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    with open(args.out, "wb") as fh:
        writer.write(fh)
    print("OK", args.out, "(%d pages)" % (offset - 1))


if __name__ == "__main__":
    main()
