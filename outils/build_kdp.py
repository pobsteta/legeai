#!/usr/bin/env python3
"""Assemble l'intérieur du tome 1 au format KDP (7 × 10 pouces) et mesure le calibrage.

Construit les quatre livraisons avec build_pdf.py --kdp, à la suite (folios continus),
les concatène, puis écrit un rapport : pages physiques occupées par chaque page du
livre, comparées au budget du chemin de fer (1 page, 2 pour les doubles pages).
"""
import json, subprocess, sys
from pathlib import Path
from pypdf import PdfReader, PdfWriter

RACINE = Path(__file__).resolve().parent.parent
TOME = RACINE / "tomes/01-le-chene"
LIVRAISONS = ["livraison-1-p01-27", "livraison-2-p28-45", "livraison-3-p46-53", "livraison-4-p54-64"]
BUDGET_TOTAL = 64

sortie = TOME / "pdf"; sortie.mkdir(exist_ok=True)
tmp = Path("/tmp/kdp"); tmp.mkdir(exist_ok=True)
debuts, fichiers, page = [], [], 1
for nom in LIVRAISONS:
    out = tmp / f"{nom}.pdf"
    subprocess.run([sys.executable, str(RACINE / "outils/build_pdf.py"), str(TOME / "texte" / f"{nom}.md"),
                    str(out), "--illustre", "--kdp", "--sans-couverture", "--premiere-page", str(page)],
                   check=True, stdout=subprocess.DEVNULL)
    cal = json.loads(out.with_suffix(".calibrage.json").read_text(encoding="utf-8"))
    debuts += cal["debuts"]; fichiers.append(out); page += cal["pages_physiques"]
total = page - 1

w = PdfWriter()
for f in fichiers:
    for p in PdfReader(str(f)).pages:
        w.add_page(p)
pdf = sortie / "interieur-kdp-prototype.pdf"
with open(pdf, "wb") as fh:
    w.write(fh)

lignes, depassements = [], []
for i, (cle, debut) in enumerate(debuts):
    fin = debuts[i + 1][1] if i + 1 < len(debuts) else total + 1
    occupe = fin - debut
    a, _, b = cle.partition("-")
    budget = int(b) - int(a) + 1 if b else 1
    ecart = occupe - budget
    parite = ""
    if budget == 2 and debut % 2:
        parite = " — commence sur une page de droite"
    lignes.append(f"| {cle} | {debut} | {occupe} | {budget} | {'+' if ecart > 0 else ''}{ecart}{parite} |")
    if ecart > 0:
        depassements.append((ecart, cle))

depassements.sort(reverse=True)
rapport = [
    "# Tome 1 — Calibrage de l'intérieur KDP (prototype)",
    "",
    f"Format 7 × 10 pouces, marges miroir, corps 11 pt. Généré par `outils/build_kdp.py`.",
    "",
    f"**Pages physiques : {total}** pour un budget de **{BUDGET_TOTAL}** "
    f"(écart : {total - BUDGET_TOTAL:+d}).",
    "",
    "Pages du livre qui débordent le plus : "
    + ", ".join(f"p. {c} (+{e})" for e, c in depassements[:10]) + ".",
    "",
    "Repère : une page de 7 × 10 pouces en corps 11 tient environ 450 mots sans image, "
    "environ 230 avec une image de 10 cm, la bulle et la légende.",
    "",
    "| Page du livre | Commence à | Pages occupées | Budget | Écart |",
    "|---|---|---|---|---|",
    *lignes,
    "",
]
(TOME / "pdf/calibrage-kdp.md").write_text("\n".join(rapport), encoding="utf-8")
print(pdf, total)
