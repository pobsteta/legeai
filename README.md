# Le Geai — Arbres & arbustes de France

*« La collection la plus lue dans les cabanes. »*

Dépôt de travail de la collection **Le Geai** : vingt-cinq tomes mensuels sur les arbres et arbustes de France, pour les 7 à 77 ans, dans l'esprit de *La Hulotte*, racontés par **le Jacques**, un geai des chênes. Tout ce qui sert à fabriquer la série est ici : le positionnement, la charte, les énigmes, le personnage, le plan de photographie, le chemin de fer et le texte de chaque tome, et les outils qui produisent les PDF de relecture et le tableur de suivi.

Référence botanique de toute la collection : la *Flore forestière française* (IDF, 3 tomes). Les images sont générées avec Magnific (outil retenu le 9 novembre 2026) à partir des photographies de l'auteur, vérifiées contre la *Flore*, déclarées à KDP et mentionnées au colophon.

## Arborescence

```
collection/                        — ce qui vaut pour les 25 tomes
  01-fiche-de-positionnement.md    — identité, cible, fil conducteur, Amazon, plan de parution, énigmes, plan d'action
  02-charte-de-style.md            — esprit, sept piliers, le Jacques, structure (une année, une vie), trois registres, image, maquette, contrôle
  03-les-24-charades-de-l-enigme.md — une charade à tiroirs par tome ; réponses ILS ONT MARCHÉ / ELLES ONT VOLÉ
  04-fiche-de-personnage-le-jacques.md — le narrateur : identité, anatomie, douze attitudes, expressions, bulle, voix, INPI
  05-brief-atrioma-planche-modele-du-jacques.md — le brief prêt à coller dans le générateur (FR + EN)
  jacques/                         — images du Jacques : planche modèle v0 (trois angles), douze attitudes détourées, huit têtes, police des bulles (maquette d'étude du 9 nov.)
photos/                            — la banque de photos, chemin critique de la production
  fiche-de-prises-de-vue.md        — protocole, liste universelle, fiches des 25 espèces, calendrier
  suivi-des-photos.xlsx            — grille de suivi (25 espèces × 20 cases), individus suivis, sorties, fenêtres
tomes/
  01-le-chene/
    chemin-de-fer.md               — les 64 pages du tome 1, page par page, avec images, marges et sources
    echantillon-de-voix.md         — l'échantillon validé des trois registres (p. 3, 8-12, 44-45, 49, 51)
    texte/livraison-1-p01-27.md    — texte définitif des pages 1 à 27 (ouverture, planche, état civil, l'année)
    texte/livraison-2-p28-45.md    — texte définitif des pages 28 à 45 (la vie en quatre âges, les habitants, seul ou en forêt)
    texte/livraison-3-p46-53.md    — texte définitif des pages 46 à 53 (d'où il vient, où il va ; l'arbre et nous, menaces et protection)
    pdf/livraison-{1,2,3}-*.pdf    — les PDF de relecture correspondants (texte seul)
    pdf/maquette-illustree.pdf     — maquette de relecture illustrée des livraisons disponibles : images existantes en place, cadres « image à produire » avec leur brief, le Jacques à chaque bulle
    maquette/images.json           — images placées dans la maquette, par page (chemin, note, hauteur, zones, une planche par page)
    maquette/generation-ids.json   — identifiants Magnific des images générées le 9 novembre (originaux 2 k dans le compte de l'auteur)
    images/                        — les 44 images générées (copies 1 024 px) et les 7 figures vectorielles (PNG + PDF) ; prompts-images.md : prompts, identifiants, contrôle, écartés
    maquette/poses.json            — attitude du Jacques (J1-J12) à poser près de chaque bulle et Parole, par page
    cartes/carte-cassini-forets-de-chene.{svg,pdf,png} — carte « à la manière de Cassini » des plus belles forêts de chêne (base de la p. 58)
    planches/                      — planches comparatives pédonculé / sessile (maquette d'étude, p. 4-5) : planches I (feuille, gland), II (bourgeon, écorce) et III (port, fleur), éléments, prompts et contrôle
references/                        — fiches techniques de référence (CNPF, ONF…) et leur synthèse
  reconnaissance-chenes-sessile-pedoncule.md — les fiches pour distinguer les deux chênes, liens et critères ; PDF à déposer à côté
outils/
  build_pdf.py                     — markdown d'une livraison → PDF de relecture (reportlab) ; avec --illustre, maquette illustrée (images, cadres à produire, Jacques et bulles en Patrick Hand)
  build_maquette.py                — enchaîne les livraisons disponibles en mode illustré dans un seul PDF numéroté en continu
  figures_vectorielles.py          — cartes, échelle des vies, chromosomes et graphique IGN dessinés en vectoriel (matplotlib, shapely ; données Natural Earth et france-geojson, voir l'en-tête)
  geai_suivi.py                    — génère le classeur de suivi des photos vierge (openpyxl)
  carte_cassini.py                 — génère la carte de Cassini des forêts de chêne (shapely, SVG ; données Natural Earth et france-geojson, voir l'en-tête du script)
  compose_planches.py              — assemble les planches comparatives à partir de planches/elements/ (Pillow)
  jacques_planche.py               — détoure les vignettes du Jacques et compose sa planche de présentation
  retouche_oreillettes.py          — retouche de la base de la feuille de pédonculé (9 nov. au matin), remplacée le jour même par une génération 2 k ; conservé comme trace
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
| `**[Encadré — titre]**` | cadre dans la page (ex. « Chez le sessile ») ; seul sur sa ligne, il ouvre un encadré long qui prend les paragraphes suivants jusqu'au prochain marqueur (ex. « Hildegarde dit », p. 49) |
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
  --livraison "Texte, livraison 1 — pages 1 à 27" --date "8 novembre 2026 · p. 4-5 revues le 9"
python3 outils/build_pdf.py tomes/01-le-chene/texte/livraison-2-p28-45.md tomes/01-le-chene/pdf/livraison-2-p28-45.pdf \
  --tome "Tome 1" --titre "Le Chêne" --sous-titre "La vie secrète du roi de nos forêts" \
  --livraison "Texte, livraison 2 — pages 28 à 45" --contenu "La vie (quatre âges) · Les habitants · Seul ou en forêt" \
  --date "9 novembre 2026"
python3 outils/build_pdf.py tomes/01-le-chene/texte/livraison-3-p46-53.md tomes/01-le-chene/pdf/livraison-3-p46-53.pdf \
  --tome "Tome 1" --titre "Le Chêne" --sous-titre "La vie secrète du roi de nos forêts" \
  --livraison "Texte, livraison 3 — pages 46 à 53" --contenu "D'où il vient, où il va · L'arbre et nous, menaces et protection" \
  --date "9 novembre 2026"

# Figures de données (télécharger d'abord les GeoJSON dans GEO_DIR : voir l'en-tête du script)
GEO_DIR=/tmp/geo python3 outils/figures_vectorielles.py

# Maquette de relecture illustrée (toutes les livraisons présentes dans texte/ ; 100 pages A4 le 9 novembre au soir)
python3 outils/build_maquette.py --date "9 novembre 2026"

# Classeur de suivi des photos vierge
python3 outils/geai_suivi.py photos/suivi-des-photos.xlsx

# Carte de Cassini des forêts de chêne (télécharger d'abord les données : voir l'en-tête du script)
python3 outils/carte_cassini.py && rsvg-convert -f pdf -o carte.pdf geo/carte-cassini-forets-de-chene.svg
```

`build_pdf.py` utilise les polices Caladea et Carlito (paquet `fonts-crosextra-caladea` / `fonts-crosextra-carlito` sous Debian/Ubuntu) ; adapter le chemin `FD` en tête du script si elles sont ailleurs. Les bulles de la maquette illustrée sont composées en Patrick Hand (`collection/jacques/PatrickHand-Regular.ttf`, licence OFL) ; le Jacques est pris dans `collection/jacques/vignettes/`. Une page sans image dans `maquette/images.json` reçoit un cadre gris dont la légende est le brief ; une page sans attitude dans `maquette/poses.json` reçoit une attitude du cycle par défaut.

## État au 9 novembre 2026

- Collection : positionnement, charte, 24 charades, fiche de personnage et brief de la planche modèle rédigés et validés. Générateur d'images retenu : Magnific. **Planche modèle v0 du Jacques** (trois angles, douze attitudes, huit têtes) générée le 9 novembre d'après la seule description de la fiche — maquette d'étude, à refaire en v1 à partir des photos de geais de l'auteur (`collection/jacques/`).
- Photos : fiche de prises de vue et tableur de suivi prêts ; la campagne commence maintenant (glandée en cours, geais au travail — point E, indispensable à la planche modèle du Jacques).
- Tome 1 *Le Chêne* : chemin de fer de 64 pages, échantillon de voix validé, **livraisons 1 (p. 1-27), 2 (p. 28-45) et 3 (p. 46-53) écrites et sourcées** (les livraisons 2 et 3 reprennent les pages 44-45, 49 et 51 de l'échantillon de voix, désormais sourcées ; la p. 51 corrige l'entrée « tanins contre le mildiou », infirmée par l'étude de 2025), carte de Cassini des forêts de chêne, trois planches comparatives pédonculé / sessile en maquette d'étude (pièce de 1 € à l'échelle dans chaque case au centimètre, homme debout pour le port ; loupe sur le bourgeon terminal dans les cases des bourgeons ; tous les dessins régénérés en 2 k le 9 novembre sur le compte Magnific abonné — voir `planches/prompts-planches-comparatives.md`). **Maquette de relecture illustrée** des pages 1 à 53 (`pdf/maquette-illustree.pdf`, 9 novembre au soir) : **toutes les images sont en place** — les trois planches (une par page), 44 images générées avec Magnific en 2 k d'après les légendes (3 245 crédits, deux reprises : pic mar, manuscrit sans texte), 7 figures de données dessinées en vectoriel, le Jacques à chacune des 52 bulles et Paroles. Statut maquette d'étude : les vues de l'individu suivi (p. 8, 18, 23, 34) et le Jacques sont à refaire d'après les photos de l'auteur ; les planches d'identification sont à contrôler ; numéros, cercles et légendes internes seront posés en vectoriel (`images/prompts-images.md`). Reste la livraison 4 (p. 54-64 : à faire, énigme, repères, sources, courrier, suite), puis la production des images page par page.
- À fournir par l'auteur : le lieu de l'individu suivi (pour vérifier les regards sur Cassini et le cadastre), une photographie ancienne du village, les dates réelles de débourrement, les noms lorrains du chêne, le chapitre « De quercu » de la *Physica* (Monat ou Verten), un chêne remarquable lorrain pour la p. 58, le nom d'auteur de couverture.

## Droits

Textes, personnage et documents : © l'auteur, tous droits réservés. Le nom « Le Geai », le cartouche et « le Jacques » sont destinés à un dépôt INPI (voir la fiche de personnage, section 11). Les images générées sont déclarées comme telles à KDP ; aucune planche d'ouvrage protégé n'est utilisée pour les produire.
