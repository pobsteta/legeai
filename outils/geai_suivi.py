from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.formatting.rule import CellIsRule
from openpyxl.utils import get_column_letter

FONT = "Arial"
wb = Workbook()

# ---------- données ----------
especes = [
    (1, "Le Chêne (pédonculé & sessile)", "Quercus robur / Q. petraea", "QUE-ROB / QUE-PET", "Octobre A1"),
    (2, "Le Sapin pectiné", "Abies alba", "ABI-ALB", "Novembre A1"),
    (3, "L'Épicéa", "Picea abies", "PIC-ABI", "Décembre A1"),
    (4, "Le Douglas", "Pseudotsuga menziesii", "PSE-MEN", "Janvier A1"),
    (5, "Le Pin sylvestre", "Pinus sylvestris", "PIN-SYL", "Février A1"),
    (6, "Le Chêne pubescent", "Quercus pubescens", "QUE-PUB", "Mars A1"),
    (7, "Le Charme", "Carpinus betulus", "CAR-BET", "Avril A1"),
    (8, "Le Hêtre", "Fagus sylvatica", "FAG-SYL", "Mai A1"),
    (9, "Le Frêne", "Fraxinus excelsior", "FRA-EXC", "Juin A1"),
    (10, "Le Châtaignier", "Castanea sativa", "CAS-SAT", "Juillet A1"),
    (11, "Le Chêne vert", "Quercus ilex", "QUE-ILE", "Août A1"),
    (12, "Le Pin maritime", "Pinus pinaster", "PIN-PIN", "Septembre A1"),
    (13, "Le Fusain", "Euonymus europaeus", "EUO-EUR", "Octobre A2"),
    (14, "Le Houx", "Ilex aquifolium", "ILE-AQU", "Novembre A2"),
    (15, "Le Cornouiller sanguin", "Cornus sanguinea", "COR-SAN", "Décembre A2"),
    (16, "Le Noisetier", "Corylus avellana", "COR-AVE", "Janvier A2"),
    (17, "Le Buis", "Buxus sempervirens", "BUX-SEM", "Février A2"),
    (18, "Le Prunellier", "Prunus spinosa", "PRU-SPI", "Mars A2"),
    (19, "L'Aubépine", "Crataegus monogyna", "CRA-MON", "Avril A2"),
    (20, "Le Genêt à balais", "Cytisus scoparius", "CYT-SCO", "Mai A2"),
    (21, "Le Troène", "Ligustrum vulgare", "LIG-VUL", "Juin A2"),
    (22, "La Bourdaine", "Frangula alnus", "FRA-ALN", "Juillet A2"),
    (23, "L'Églantier", "Rosa canina", "ROS-CAN", "Août A2"),
    (24, "Le Sureau", "Sambucus nigra", "SAM-NIG", "Septembre A2"),
    ("HS", "La Ronce & le Lierre", "Rubus fruticosus agg. / Hedera helix", "RUB-FRU / HED-HEL", "Octobre A3"),
]

groupes = [
    ("Planche d'identification", ["Feuille recto-verso", "Bourgeon", "Écorce jeune & vieille", "Fleur",
                                  "Fruit & graine", "Plantule", "Silhouette été", "Silhouette hiver"]),
    ("L'année (individu suivi)", ["Printemps", "Été", "Automne", "Hiver"]),
    ("La vie (4 âges)", ["Graine", "Jeune pousse", "Adulte", "Sénescence"]),
    ("Repérage", ["Individu suivi (GPS)", "Vieil arbre", "Arbre mort", "Habitants & traces"]),
]
cases = [c for _, cols in groupes for c in cols]
N_CASES = len(cases)  # 20

# ---------- styles ----------
thin = Side(style="thin", color="BFBFBF")
border = Border(left=thin, right=thin, top=thin, bottom=thin)
fill_head = PatternFill("solid", fgColor="2F5233")
fill_group = {
    "Planche d'identification": PatternFill("solid", fgColor="DDEBD6"),
    "L'année (individu suivi)": PatternFill("solid", fgColor="FFF2CC"),
    "La vie (4 âges)": PatternFill("solid", fgColor="DEEAF6"),
    "Repérage": PatternFill("solid", fgColor="EDEDED"),
}
fill_ok = PatternFill("solid", fgColor="A9D18E")
fill_input = PatternFill("solid", fgColor="FFFFFF")
white_bold = Font(name=FONT, bold=True, color="FFFFFF", size=10)
bold = Font(name=FONT, bold=True, size=10)
normal = Font(name=FONT, size=10)
small = Font(name=FONT, size=9, italic=True, color="595959")
center = Alignment(horizontal="center", vertical="center", wrap_text=True)
left = Alignment(horizontal="left", vertical="center", wrap_text=True)
rot = Alignment(horizontal="center", vertical="bottom", textRotation=90, wrap_text=True)

# ---------- feuille Suivi ----------
ws = wb.active
ws.title = "Suivi"

ws["A1"] = "Le Geai — Banque de photos : grille de suivi"
ws["A1"].font = Font(name=FONT, bold=True, size=14, color="2F5233")
ws["A2"] = ("Mode d'emploi : dans chaque case blanche, choisir ✓ dans la liste déroulante (ou taper ✓) quand une photo "
            "validée existe (nette, échelle dans le cadre, bonne espèce, bonne saison). Les colonnes « Complet » et "
            "« Manque » se calculent seules. Une espèce est prête quand ses 20 cases sont cochées.")
ws["A2"].font = small
ws["A2"].alignment = left
ws.merge_cells("A2:AA2")
ws.row_dimensions[2].height = 42

HEAD_GROUP_ROW, HEAD_ROW, FIRST = 4, 5, 6
fixed_cols = ["N°", "Tome / espèce", "Nom latin", "Code dossier", "Parution"]
for i, h in enumerate(fixed_cols, start=1):
    c = ws.cell(row=HEAD_ROW, column=i, value=h)
    c.font = white_bold; c.fill = fill_head; c.alignment = center; c.border = border
    ws.merge_cells(start_row=HEAD_GROUP_ROW, start_column=i, end_row=HEAD_GROUP_ROW, end_column=i)
    g = ws.cell(row=HEAD_GROUP_ROW, column=i); g.fill = fill_head; g.border = border

col = len(fixed_cols) + 1
first_case_col = col
for gname, cols in groupes:
    ws.merge_cells(start_row=HEAD_GROUP_ROW, start_column=col, end_row=HEAD_GROUP_ROW, end_column=col + len(cols) - 1)
    g = ws.cell(row=HEAD_GROUP_ROW, column=col, value=gname)
    g.font = bold; g.fill = fill_group[gname]; g.alignment = center; g.border = border
    for k in range(len(cols)):
        ws.cell(row=HEAD_GROUP_ROW, column=col + k).border = border
    for name in cols:
        c = ws.cell(row=HEAD_ROW, column=col, value=name)
        c.font = Font(name=FONT, bold=True, size=9); c.fill = fill_group[gname]; c.alignment = rot; c.border = border
        ws.column_dimensions[get_column_letter(col)].width = 4.6
        col += 1
last_case_col = col - 1
COMPLET_COL, MANQUE_COL = col, col + 1
for cc, h in ((COMPLET_COL, "Complet"), (MANQUE_COL, "Manque")):
    c = ws.cell(row=HEAD_ROW, column=cc, value=h)
    c.font = white_bold; c.fill = fill_head; c.alignment = rot; c.border = border
    ws.cell(row=HEAD_GROUP_ROW, column=cc).fill = fill_head
    ws.cell(row=HEAD_GROUP_ROW, column=cc).border = border
    ws.column_dimensions[get_column_letter(cc)].width = 7
ws.row_dimensions[HEAD_ROW].height = 108
ws.row_dimensions[HEAD_GROUP_ROW].height = 20

dv = DataValidation(type="list", formula1='"✓"', allow_blank=True, showDropDown=False)
dv.error = "Choisir ✓ ou laisser vide"; dv.errorTitle = "Case de suivi"
ws.add_data_validation(dv)

for r, (num, nom, latin, code, mois) in enumerate(especes, start=FIRST):
    vals = [num, nom, latin, code, mois]
    for i, v in enumerate(vals, start=1):
        c = ws.cell(row=r, column=i, value=v)
        c.font = normal; c.border = border
        c.alignment = center if i in (1, 5) else left
    ws.cell(row=r, column=3).font = Font(name=FONT, size=10, italic=True)
    for cc in range(first_case_col, last_case_col + 1):
        c = ws.cell(row=r, column=cc)
        c.border = border; c.alignment = center; c.font = Font(name=FONT, size=12); c.fill = fill_input
        dv.add(c)
    rng = f"{get_column_letter(first_case_col)}{r}:{get_column_letter(last_case_col)}{r}"
    c = ws.cell(row=r, column=COMPLET_COL, value=f'=COUNTIF({rng},"✓")/{N_CASES}')
    c.number_format = "0%"; c.font = bold; c.alignment = center; c.border = border
    c = ws.cell(row=r, column=MANQUE_COL, value=f'={N_CASES}-COUNTIF({rng},"✓")')
    c.font = normal; c.alignment = center; c.border = border
    ws.row_dimensions[r].height = 24

LAST = FIRST + len(especes) - 1
# ligne de total
tr = LAST + 1
ws.cell(row=tr, column=2, value="Toutes espèces — avancement").font = bold
for cc in range(first_case_col, last_case_col + 1):
    L = get_column_letter(cc)
    c = ws.cell(row=tr, column=cc, value=f'=COUNTIF({L}{FIRST}:{L}{LAST},"✓")')
    c.font = Font(name=FONT, size=9, bold=True); c.alignment = center; c.border = border
    c.fill = PatternFill("solid", fgColor="F2F2F2")
c = ws.cell(row=tr, column=COMPLET_COL,
            value=f'=AVERAGE({get_column_letter(COMPLET_COL)}{FIRST}:{get_column_letter(COMPLET_COL)}{LAST})')
c.number_format = "0%"; c.font = bold; c.alignment = center; c.border = border
c = ws.cell(row=tr, column=MANQUE_COL,
            value=f'=SUM({get_column_letter(MANQUE_COL)}{FIRST}:{get_column_letter(MANQUE_COL)}{LAST})')
c.font = bold; c.alignment = center; c.border = border
ws.cell(row=tr + 1, column=2, value="Ligne du bas : nombre d'espèces cochées par case ; à droite, avancement moyen et total des cases manquantes.").font = small
ws.merge_cells(start_row=tr + 1, start_column=2, end_row=tr + 1, end_column=COMPLET_COL)

# mise en forme conditionnelle : vert quand ✓
full = f"{get_column_letter(first_case_col)}{FIRST}:{get_column_letter(last_case_col)}{LAST}"
ws.conditional_formatting.add(full, CellIsRule(operator="equal", formula=['"✓"'], fill=fill_ok,
                                               font=Font(name=FONT, bold=True, color="1E4620")))
# complet : dégradé simple
from openpyxl.formatting.rule import ColorScaleRule
ws.conditional_formatting.add(f"{get_column_letter(COMPLET_COL)}{FIRST}:{get_column_letter(COMPLET_COL)}{LAST}",
                              ColorScaleRule(start_type="num", start_value=0, start_color="F8CBAD",
                                             mid_type="num", mid_value=0.5, mid_color="FFE699",
                                             end_type="num", end_value=1, end_color="A9D18E"))

ws.column_dimensions["A"].width = 5
ws.column_dimensions["B"].width = 30
ws.column_dimensions["C"].width = 26
ws.column_dimensions["D"].width = 17
ws.column_dimensions["E"].width = 12
ws.freeze_panes = ws.cell(row=FIRST, column=3)  # N° et espèce restent visibles en défilant
ws.sheet_view.zoomScale = 90

# ---------- feuille Individus suivis ----------
wi = wb.create_sheet("Individus suivis")
wi["A1"] = "Les 25 individus suivis toute l'année"
wi["A1"].font = Font(name=FONT, bold=True, size=14, color="2F5233")
wi["A2"] = ("Un sujet adulte par espèce, accessible toute l'année, dégagé, photographié depuis le même point fixe à "
            "chaque saison. Remplir les colonnes blanches ; la première ligne est un exemple à remplacer.")
wi["A2"].font = small; wi["A2"].alignment = left
wi.merge_cells("A2:J2"); wi.row_dimensions[2].height = 36
heads = ["N°", "Espèce", "Lieu (commune, lieu-dit)", "Latitude", "Longitude", "Point de vue fixe (repère)",
         "Remplaçant (lieu)", "Vieil arbre repéré (lieu)", "Arbre mort repéré (lieu)", "Notes"]
widths = [5, 30, 28, 11, 11, 28, 24, 24, 24, 30]
for i, (h, w) in enumerate(zip(heads, widths), start=1):
    c = wi.cell(row=4, column=i, value=h)
    c.font = white_bold; c.fill = fill_head; c.alignment = center; c.border = border
    wi.column_dimensions[get_column_letter(i)].width = w
wi.row_dimensions[4].height = 32
exemple = ["ex.", "Le Chêne (pédonculé & sessile)", "Boult-aux-Bois, lisière du bois communal", 49.4328, 4.8341,
           "Depuis la borne du chemin, face nord", "Chêne isolé de la prairie Dupont",
           "Chêne creux du cimetière (cavités, lierre)", "Chandelle morte, parcelle 12", "Exemple à remplacer"]
for i, v in enumerate(exemple, start=1):
    c = wi.cell(row=5, column=i, value=v); c.font = Font(name=FONT, size=10, italic=True, color="7F7F7F")
    c.border = border; c.alignment = left
for r, (num, nom, *_rest) in enumerate(especes, start=6):
    for i in range(1, len(heads) + 1):
        c = wi.cell(row=r, column=i); c.border = border; c.alignment = left; c.font = normal
    wi.cell(row=r, column=1, value=num).alignment = center
    wi.cell(row=r, column=2, value=nom)
    wi.row_dimensions[r].height = 22
wi.freeze_panes = "C5"

# ---------- feuille Sorties ----------
wsj = wb.create_sheet("Sorties")
wsj["A1"] = "Journal des sorties"
wsj["A1"].font = Font(name=FONT, bold=True, size=14, color="2F5233")
wsj["A2"] = ("Une ligne par sortie. Noter ce qui a été pris et ce qui manque encore ; reporter ensuite les ✓ dans "
             "la feuille Suivi. La première ligne est un exemple à remplacer.")
wsj["A2"].font = small; wsj["A2"].alignment = left
wsj.merge_cells("A2:G2"); wsj.row_dimensions[2].height = 30
heads = ["Date", "Lieu", "Espèce(s)", "Saison / âge", "Éléments photographiés", "Manque encore", "Notes"]
widths = [12, 26, 26, 16, 34, 30, 34]
for i, (h, w) in enumerate(zip(heads, widths), start=1):
    c = wsj.cell(row=4, column=i, value=h)
    c.font = white_bold; c.fill = fill_head; c.alignment = center; c.border = border
    wsj.column_dimensions[get_column_letter(i)].width = w
exemple = ["2026-11-14", "Boult-aux-Bois, lisière du bois communal", "Chêne pédonculé, Chêne sessile",
           "Automne / adulte, graine", "Glands avec pédoncules (les deux), cupules, feuilles R/V, glands germés sous litière, écorce vieille",
           "Bourgeons (janvier), silhouette hiver", "Geai observé cachant des glands — 3 photos pour la feuille de modèle"]
for i, v in enumerate(exemple, start=1):
    c = wsj.cell(row=5, column=i, value=v); c.font = Font(name=FONT, size=10, italic=True, color="7F7F7F")
    c.border = border; c.alignment = left
wsj.row_dimensions[5].height = 48
for r in range(6, 66):
    for i in range(1, len(heads) + 1):
        c = wsj.cell(row=r, column=i); c.border = border; c.alignment = left; c.font = normal
wsj.freeze_panes = "A5"

# ---------- feuille Fenêtres ----------
wf = wb.create_sheet("Fenêtres")
wf["A1"] = "Calendrier des prises de vue"
wf["A1"].font = Font(name=FONT, bold=True, size=14, color="2F5233")
wf["A2"] = "Ce qui se photographie à chaque fenêtre, toutes espèces confondues. Détail par espèce : fiche de prises de vue du projet."
wf["A2"].font = small; wf.merge_cells("A2:C2")
heads = ["Fenêtre", "Priorités", "Fait ?"]
widths = [20, 95, 8]
for i, (h, w) in enumerate(zip(heads, widths), start=1):
    c = wf.cell(row=4, column=i, value=h)
    c.font = white_bold; c.fill = fill_head; c.alignment = center; c.border = border
    wf.column_dimensions[get_column_letter(i)].width = w
fenetres = [
    ("Novembre – décembre",
     "Fruits et graines encore en place : glands (deux chênes, pédoncules), faînes, châtaignes, cônes (épicéa, douglas, pin sylvestre), "
     "samares, cenelles, prunelles, cynorhodons et bédégars, fusain, houx, troène, bourdaine. Glands germés. Floraison du lierre et ses "
     "insectes. Feuillages d'automne. Geais au travail. Choix et marquage des 25 individus suivis ; repérage des vieux arbres et des arbres morts."),
    ("Janvier – février",
     "Silhouettes d'hiver depuis les points fixes ; écorces jeune et vieille ; bourgeons en macro (frêne noir, hêtre fusiforme, douglas pointu, "
     "bourdaine nu, charme appliqué) ; cônes et graines des résineux ; chatons du noisetier et ses fleurs rouges ; rameaux rouges du cornouiller ; "
     "baies de houx et de troène sur rameaux nus ; sureau qui débourre ; écorce saumon du pin sylvestre."),
    ("Mars – mai",
     "Prunellier puis aubépine en fleur ; buis en fleur ; chatons des chênes, du charme, du hêtre ; frêne en fleur avant ses feuilles ; feuillaison "
     "du hêtre ; pollen des pins et de l'épicéa ; semis et plantules de toutes les espèces (l'âge « jeune pousse ») ; genêt en fleur (mai) ; "
     "chenilles de pyrale ; cônes de pin sylvestre ouverts."),
    ("Juin – août",
     "Feuillages complets recto-verso ; fruits en formation ; chatons du châtaignier ; fleurs du sureau, du troène, de l'églantier, de la bourdaine ; "
     "gousses du genêt qui claquent ; noisettes vertes ; hôtes de la canopée ; voyage dans le Midi : chêne vert, chêne pubescent, pin maritime, "
     "buis — avec le tome 3 de la Flore forestière française."),
    ("Septembre – octobre",
     "Fruits mûrs et dispersion : noisettes, mûres, baies de sureau, bogues, glands, cônes de douglas ; couleurs ; deuxième chance pour tout ce "
     "qui manque de l'automne précédent. Les tomes 1 à 3 doivent être bouclés."),
]
dv2 = DataValidation(type="list", formula1='"✓"', allow_blank=True)
wf.add_data_validation(dv2)
for r, (f, p) in enumerate(fenetres, start=5):
    a = wf.cell(row=r, column=1, value=f); a.font = bold; a.alignment = left; a.border = border
    b = wf.cell(row=r, column=2, value=p); b.font = normal; b.alignment = left; b.border = border
    c = wf.cell(row=r, column=3); c.border = border; c.alignment = center; c.font = Font(name=FONT, size=12)
    dv2.add(c)
    wf.row_dimensions[r].height = 78
wf.conditional_formatting.add("C5:C9", CellIsRule(operator="equal", formula=['"✓"'], fill=fill_ok))

import sys
wb.save(sys.argv[1] if len(sys.argv) > 1 else "suivi-des-photos.xlsx")
print("ok", N_CASES, first_case_col, last_case_col, COMPLET_COL, MANQUE_COL, LAST)
