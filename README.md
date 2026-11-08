# Le Geai — Arbres & arbustes de France

*« La collection la plus lue dans les cabanes. »*

Dépôt de travail de la collection **Le Geai** : vingt-cinq tomes mensuels sur les arbres et arbustes de France, pour les 7 à 77 ans, dans l'esprit de *La Hulotte*, racontés par **le Jacques**, un geai des chênes. Tout ce qui sert à fabriquer la série est ici : le positionnement, la charte, les énigmes, le personnage, le plan de photographie, le chemin de fer et le texte de chaque tome, et les outils qui produisent les PDF de relecture et le tableur de suivi.

Référence botanique de toute la collection : la *Flore forestière française* (IDF, 3 tomes). Les images sont générées avec Atrioma à partir des photographies de l'auteur, vérifiées contre la *Flore*, déclarées à KDP et mentionnées au colophon.

## Arborescence

```
collection/                        — ce qui vaut pour les 25 tomes
  01-fiche-de-positionnement.md    — identité, cible, fil conducteur, Amazon, plan de parution, énigmes, plan d'action
  02-charte-de-style.md            — esprit, sept piliers, le Jacques, structure (une année, une vie), trois registres, image, maquette, contrôle
  03-les-24-charades-de-l-enigme.md — une charade à tiroirs par tome ; réponses ILS ONT MARCHÉ / ELLES ONT VOLÉ
  04-fiche-de-personnage-le-jacques.md — le narrateur : identité, anatomie, douze attitudes, expressions, bulle, voix, INPI
  05-brief-atrioma-planche-modele-du-jacques.md — le brief prêt à coller dans le générateur (FR + EN)
photos/                            — la banque de photos, chemin critique de la production
  fiche-de-prises-de-vue.md        — protocole, liste universelle, fiches des 25 espèces, calendrier
  suivi-des-photos.xlsx            — grille de suivi (25 espèces × 20 cases), individus suivis, sorties, fenêtres
tomes/
  01-le-chene/
    chemin-de-fer.md               — les 64 pages du tome 1, page par page, avec images, marges et sources
    echantillon-de-voix.md         — l'échantillon validé des trois registres (p. 3, 8-12, 44-45, 49, 51)
    texte/livraison-1-p01-27.md    — texte définitif des pages 1 à 27 (ouverture, planche, état civil, l'année)
    pdf/livraison-1-p01-27.pdf     — le PDF de relecture correspondant
    cartes/carte-cassini-forets-de-chene.{svg,pdf,png} — carte « à la manière de Cassini » des plus belles forêts de chêne (base de la p. 58)
    planches/                      — planches comparatives pédonculé / sessile (maquette d'étude, p. 4-5) : planches I et II, éléments, prompts et contrôle
references/                        — fiches techniques de référence (CNPF, ONF…) et leur synthèse
  reconnaissance-chenes-sessile-pedoncule.md — les fiches pour distinguer les deux chênes, liens et critères ; PDF à déposer à côté
outils/
  build_pdf.py                     — markdown d'une livraison → PDF de relecture (reportlab)
  geai_suivi.py                    — génère le classeur de suivi des photos vierge (openpyxl)
  carte_cassini.py                 — génère la carte de Cassini des forêts de chêne (shapely, SVG ; données Natural Earth et france-geojson, voir l'en-tête du script)
  compose_planches.py              — assemble les planches comparatives à partir de planches/elements/ (Pillow)
  requirements.txt
```

## Ordre de lecture

1. `collection/01-fiche-de-positionnement.md` — pourquoi, pour qui, dans quel ordre (25 tomes, un par mois à partir d'octobre).
2. `collection/02-charte-de-style.md` — comment on écrit et comment on dessine ; la liste de contrôle avant publication est à la fin.
3. `collection/04-fiche-de-personnage-le-jacques.md` puis `05-brief-atrioma…` — le narrateur, puis sa planche modèle, premier chantier d'image.
4. `photos/fiche-de-prises-de-vue.md` — quoi photographier, quand ; le tableur tient le compte.
5. `tomes/01-le-chene/` — le tome en cours : chemin de fer, puis texte par livraisons.

## Conventions du texte

Chaque tome est écrit en Markdown, une page du livre = une section `## Page N — titre` (ou `### Page N` à l'intérieur d'une saison `## PRINTEMPS`, `## ÉTÉ`, `## AUTOMNE`, `## HIVER`). Les trois registres et les éléments de page sont balisés :

| Balise | Registre / usage |
|---|---|
| `**[Regard]**` suivi d'un paragraphe en `*italique*` | le regard, sur l'image d'ouverture du chapitre — jamais de chiffre de mesure |
| texte courant | l'enquête — les faits, sources en notes |
| `**[Bulle]** « … »` | le Jacques, bulle de marge (une par page) |
| `**[Parole du Jacques]** « … »` | le Jacques, cartouche (un par chapitre) |
| `**[Légende]**` | sous l'image |
| `**[Encadré — titre]**` | cadre dans la page (ex. « Chez le sessile ») |
| `**[Image]**`, `**[Carte]**`, `**[Sommaire]**` | emplacement d'image ou de carte |
| `**(n)** …` | note de bas de page, numérotée par page ; `(n)` dans le texte renvoie à la note |
| `[lieu]`, `[25 avril]`… | ce qui dépend de l'individu suivi et reste à vérifier (Cassini, cadastre, archives) |

Les livraisons d'un tome se succèdent dans `tomes/NN-espece/texte/` : `livraison-1-p01-27.md`, `livraison-2-p28-45.md`, etc. Le chemin de fer reste la référence de la pagination.

## Outils

```bash
pip install -r outils/requirements.txt

# PDF de relecture d'une livraison (une page A4 par page du livre + couverture + annexe)
python3 outils/build_pdf.py tomes/01-le-chene/texte/livraison-1-p01-27.md tomes/01-le-chene/pdf/livraison-1-p01-27.pdf \
  --tome "Tome 1" --titre "Le Chêne" --sous-titre "La vie secrète du roi de nos forêts" \
  --livraison "Texte, livraison 1 — pages 1 à 27" --date "8 novembre 2026"

# Classeur de suivi des photos vierge
python3 outils/geai_suivi.py photos/suivi-des-photos.xlsx

# Carte de Cassini des forêts de chêne (télécharger d'abord les données : voir l'en-tête du script)
python3 outils/carte_cassini.py && rsvg-convert -f pdf -o carte.pdf geo/carte-cassini-forets-de-chene.svg
```

`build_pdf.py` utilise les polices Caladea et Carlito (paquet `fonts-crosextra-caladea` / `fonts-crosextra-carlito` sous Debian/Ubuntu) ; adapter le chemin `FD` en tête du script si elles sont ailleurs.

## État au 8 novembre 2026

- Collection : positionnement, charte, 24 charades, fiche de personnage et brief Atrioma rédigés et validés.
- Photos : fiche de prises de vue et tableur de suivi prêts ; la campagne commence maintenant (glandée en cours, geais au travail — point E, indispensable à la planche modèle du Jacques).
- Tome 1 *Le Chêne* : chemin de fer de 64 pages, échantillon de voix validé, **livraison 1 (p. 1-27) écrite et sourcée**. Restent les livraisons 2 (p. 28-45 : la vie, les habitants, « Seul ou en forêt »), 3 (p. 46-53 : le voyage, l'arbre et nous, menaces) et 4 (p. 54-64 : à faire, énigme, repères, sources, courrier, suite).
- À fournir par l'auteur : le lieu de l'individu suivi (pour vérifier les regards sur Cassini et le cadastre), une photographie ancienne du village, les dates réelles de débourrement, les noms lorrains du chêne, le chapitre « De quercu » de la *Physica* (Monat ou Verten), un chêne remarquable lorrain pour la p. 58, le nom d'auteur de couverture.

## Droits

Textes, personnage et documents : © l'auteur, tous droits réservés. Le nom « Le Geai », le cartouche et « le Jacques » sont destinés à un dépôt INPI (voir la fiche de personnage, section 11). Les images générées sont déclarées comme telles à KDP ; aucune planche d'ouvrage protégé n'est utilisée pour les produire.
