#!/usr/bin/env python3
"""Assemble l'intérieur du tome 1 au format KDP (7 × 10 pouces) et mesure le calibrage.

Construit les quatre livraisons avec build_pdf.py --kdp, à la suite (folios continus),
les concatène, puis écrit un rapport : pages physiques occupées par chaque page du
livre, comparées au budget du chemin de fer (1 page, 2 pour les doubles pages).
"""
import argparse, json, subprocess, sys
from pathlib import Path
from pypdf import PdfReader, PdfWriter

RACINE = Path(__file__).resolve().parent.parent
TOME = RACINE / "tomes/01-le-chene"
LIVRAISONS = ["livraison-1-p01-27", "livraison-2-p28-45", "livraison-3-p46-53", "livraison-4-p54-64"]
BUDGET_TOTAL = 64
ap = argparse.ArgumentParser()
ap.add_argument("--format", default="7x10", choices=["7x10", "8x10", "8.25x11", "8.5x11"])
ap.add_argument("--double", action="store_true", help="une double page par page du chemin de fer (budget 144)")
A = ap.parse_args(); FMT = A.format
SUFFIXE = FMT + ("-double" if A.double else "")
if A.double:
    BUDGET_TOTAL = 144

sortie = TOME / "pdf"; sortie.mkdir(exist_ok=True)
tmp = Path("/tmp/kdp"); tmp.mkdir(exist_ok=True)
debuts, fichiers, notes, page = [], [], [], 2 if A.double else 1  # page 1 : titre
for i, nom in enumerate(LIVRAISONS):
    out = tmp / f"{nom}-{SUFFIXE}.pdf"
    cmd = [sys.executable, str(RACINE / "outils/build_pdf.py"), str(TOME / "texte" / f"{nom}.md"),
           str(out), "--illustre", "--kdp", "--format", FMT, "--sans-couverture", "--premiere-page", str(page)] + (["--double"] if A.double else [])
    if i == len(LIVRAISONS) - 1:  # la dernière livraison porte les notes de tout le volume
        nf = tmp / f"notes-{SUFFIXE}.json"; nf.write_text(json.dumps(notes, ensure_ascii=False), encoding="utf-8")
        cmd += ["--notes-fin", str(nf)]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL)
    cal = json.loads(out.with_suffix(".calibrage.json").read_text(encoding="utf-8"))
    debuts += cal["debuts"]; notes += cal["notes"]; fichiers.append(out); page += cal["pages_physiques"]
total = page - 1
blanche = None
if A.double:  # page de titre provisoire, blanche, en page 1
    from reportlab.pdfgen import canvas
    blanche = tmp / "blanche.pdf"; r = PdfReader(str(fichiers[0])).pages[0].mediabox
    c = canvas.Canvas(str(blanche), pagesize=(float(r.width), float(r.height))); c.showPage(); c.save()
    fichiers.insert(0, blanche)

w = PdfWriter()
for f in fichiers:
    for p in PdfReader(str(f)).pages:
        w.add_page(p)
pdf = sortie / f"interieur-kdp-{SUFFIXE}.pdf"
with open(pdf, "wb") as fh:
    w.write(fh)

lignes, depassements = [], []
for i, (cle, debut) in enumerate(debuts):
    fin = debuts[i + 1][1] if i + 1 < len(debuts) else total + 1
    occupe = fin - debut
    if cle == "Notes":
        lignes.append(f"| Notes (fin de volume) | {debut} | {occupe} | — | hors chemin de fer |")
        continue
    a, _, b = cle.partition("-")
    budget = (int(b) - int(a) + 1 if b else 1) * (2 if A.double else 1)
    ecart = occupe - budget
    parite = ""
    if budget == 2 and debut % 2:
        parite = " — commence sur une page de droite"
    lignes.append(f"| {cle} | {debut} | {occupe} | {budget} | {'+' if ecart > 0 else ''}{ecart}{parite} |")
    if ecart > 0:
        depassements.append((ecart, cle))

depassements.sort(reverse=True)
pages_notes = next((total + 1 - d for c, d in debuts if c == "Notes"), 0)
rapport = [
    f"# Tome 1 — Calibrage de l'intérieur KDP, format {FMT.replace('x', ' × ')} pouces",
    "",
    "Marges miroir, corps 11 pt, notes de source renvoyées en fin de volume. "
    f"Généré par `outils/build_kdp.py --format {FMT}{' --double' if A.double else ''}`."
    + (" Chaque page du chemin de fer devient une double page, ouverte sur une page paire (à gauche) ; "
       "la page 1 est réservée au titre." if A.double else ""),
    "",
    f"**Pages physiques : {total}**, dont {total - pages_notes} pour les 64 pages du livre "
    f"et {pages_notes} pour les notes en fin de volume (budget du chemin de fer : {BUDGET_TOTAL}).",
    "",
    "Pages du livre qui débordent le plus : "
    + ", ".join(f"p. {c} (+{e})" for e, c in depassements[:10]) + ".",
    "",
    "Repère (7 × 10) : une page en corps 11 tient environ 450 mots sans image, "
    "environ 230 avec une image de 10 cm, la bulle et la légende.",
    "",
    "| Page du livre | Commence à | Pages occupées | Budget | Écart |",
    "|---|---|---|---|---|",
    *lignes,
    "",
]
(TOME / f"pdf/calibrage-kdp-{SUFFIXE}.md").write_text("\n".join(rapport), encoding="utf-8")
print(pdf, total)
