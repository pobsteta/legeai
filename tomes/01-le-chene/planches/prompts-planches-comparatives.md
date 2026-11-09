# Tome 1 — Planches comparatives pédonculé / sessile : prompts et état

*Dessins « hyperréalistes » en noir et blanc, style gravure botanique, générés les 8 et 9 novembre 2026 avec Magnific (mode auto, offre gratuite, 1 k ; outil retenu pour la collection le 9 novembre) à partir des seuls critères écrits des fiches CNPF et de la formation ONF 2008 de F. Lebourgeois — les photographies de ces documents et les planches de la* Flore forestière française *sont protégées et n'ont jamais été données au générateur ; elles ont servi au contrôle, après coup, comme le veut la charte (section 6). Les originaux (1 024 px) sont dans le projet personnel Magnific de l'auteur, sous les identifiants ci-dessous ; les copies du dépôt font 600 × 800 px (maquette d'étude). Pour l'impression, régénérer en 2 k avec une offre payante, à partir des photographies de l'auteur (pièce de 1 € dans le cadre), avec les mêmes prompts, puis repasser la liste de contrôle.*

## Bloc de style (en tête de chaque prompt)

```
Gravure botanique scientifique en noir et blanc, dessin hyperréaliste à la plume, hachures fines, papier blanc, sans aucun texte ni lettre ni légende. [sujet] Rien d'autre dans l'image.
```

## Échelle (ajoutée le 9 novembre)

- **Dessins au centimètre** (feuille, gland, bourgeon, écorce) : une **pièce de 1 € (23,25 mm)** dessinée au trait par `outils/compose_planches.py`, à l'échelle du sujet de chaque case — posée sur le papier dans un coin libre, ou sur l'écorce. **Silhouettes** : l'homme debout au pied de l'arbre.
- L'échelle de chaque case (pixels par centimètre dans la case de 600 × 800) est fixée d'après les dimensions typiques des fiches, pas mesurée sur une photo : feuilles 66 px/cm (feuille de 10 à 11 cm, pétiole compris) ; glands 56 px/cm (gland de pédonculé 2,5 cm au bout d'un pédoncule de 8 cm, gland de sessile 2 cm) ; bourgeons 108 px/cm (bourgeon terminal de 6,5 mm pédonculé, 8,5 mm sessile, rameau grossi trois fois ; le dessin du sessile est réduit à 87 % pour mettre les deux colonnes au même grossissement) ; écorces 30 px/cm (plaques de 4 cm de large, lanières de 1,5 cm ; cadre de 20 cm environ).
- Dans l'édition définitive, la pièce sera **dans le cadre des photographies de l'auteur** (fiche de prises de vue : « échelle dans le cadre ») et l'échelle en sera déduite, non convenue.

## Éléments retenus

| Élément | Identifiant Magnific | Fichier | Contrôle |
|---|---|---|---|
| Feuille pédonculé | `ovPxVs5829`, **base retouchée le 9 nov.** (voir ci-dessous) | `elements/pedoncule_feuille.png` (original sans retouche : `elements/avant-retouche/`) | Pétiole court, lobes irréguliers, plus large au tiers supérieur : conforme. Oreillettes : trop discrètes dans l'original ; après retouche, deux petits lobes arrondis de part et d'autre du pétiole très court, conformes à la planche de la *Flore forestière française* (Q. robur, p. 731 : base « à oreillettes », pétiole très court) et aux fiches CNPF. |
| Feuille sessile | `Sy8W1prUb8` (variante `1lMRQYIr4r`) | `elements/sessile_feuille.png` | Long pétiole, base en coin, lobes réguliers, plus large au milieu : conforme (*Flore*, Q. petraea, p. 725). |
| Glands pédonculé | `gOoYkr9SXO` | `elements/pedoncule_glands.png` | Long pédoncule grêle, glands allongés à l'extrémité : conforme (les deux glands sont jointifs ; par un à trois, parfois espacés, dans la nature). |
| Glands sessile | `1lMRQkUr4r` | `elements/sessile_glands.png` | Glands trapus en bouquet, assis sur le rameau, feuille à long pétiole : conforme. |
| Bourgeons pédonculé | `8a4jDvtIrU` | `elements/pedoncule_bourgeons.png` | Bourgeons globuleux en bouquet terminal : conforme. |
| Bourgeons sessile | `mE66ZIJhJQ` (9 nov., remplace `u5GOm10QLD`, archivé dans `elements/avant-retouche/`) | `elements/sessile_bourgeons.png` | Bouquet terminal de bourgeons pointus, effilés, bourgeons latéraux pointus, rameau de même cadrage que celui du pédonculé : conforme. La version précédente n'avait que deux bourgeons et un grossissement deux fois plus fort. |
| Écorce pédonculé | `1lMRF8Er4r` (recadrée : signature parasite en bas à droite) | `elements/pedoncule_ecorce.png` | Plaques larges et profondes, sillons marqués : conforme aux photos Lebourgeois (rhytidome épais, trapézoïdal). |
| Écorce sessile | `fHZw8DqCDY` | `elements/sessile_ecorce.png` | Fissures fines en long, lanières étroites : conforme (rhytidome mince, fissuré en long). |
| Port pédonculé | `dtJ7zsLXSL` (9 nov.) | `elements/pedoncule_port.png` | Tronc court divisé bas, branches tortueuses, houppier large : conforme aux silhouettes de Lebourgeois (p. 2). |
| Port sessile | `TdlsRJyVNR` (9 nov.) | `elements/sessile_port.png` | Fût long et droit, houppier régulier en éventail : conforme. |

## La retouche de la feuille de pédonculé (9 novembre)

Onze régénérations (`bxccMXp5Y2`, `MBSSJ9TDCm`, `yiaau5DPW9`, `bxccMBe5Y2`, `VXggOBWMMU`, `5j00esOKxe`, `jUeeI7DLD0`, `tCNN2ucmZJ`, `O6vvFafynm`, `rgDD8elxtc`, `9ZEE5QpNYZ`), en français puis en anglais, avec la base décrite de toutes les manières (« cordée », « en cœur renversé », « deux petits lobes qui recouvrent le pétiole », « pas en coin »), n'ont donné aucune oreillette : le mode auto gratuit garde une base effilée et un pétiole visible (plusieurs essais ont en outre un papier gris ou un texte parasite). Le plafond quotidien a été atteint au douzième essai.

La base du dessin retenu a donc été **retouchée par déformation locale** (`outils/retouche_oreillettes.py` : maillage Pillow, étirement vertical des 10 derniers millimètres du limbe de part et d'autre du pétiole, profil gaussien, 31 px d'allongement au plus, pétiole et rameau intacts ; un bourgeon latéral du bout de rameau, déplacé par l'opération, a été effacé). Rien n'a été dessiné à la main ni emprunté : ce sont les hachures du dessin lui-même, étirées. La retouche se voit de près (hachures allongées dans les oreillettes) et convient à une maquette d'étude ; la version définitive se fera à partir d'une photographie de l'auteur, avec une offre Magnific payante (image de référence, outil de retouche de zone), et ne devra pas en avoir besoin.

## Écartés

- `N2uXUhs6D9` (premier essai) : pétiole long et texte parasite — feuille de sessile déguisée.
- `huigdqzvqL`, `ksV3uUq16B` : base cunéiforme, trop régulières pour un pédonculé.
- `xSp2HzLjfW` : « oreillettes » caricaturales, deux lobes ronds énormes.
- Les onze régénérations de la feuille du 9 novembre (liste ci-dessus) : pas d'oreillettes.
- `xSppBkXjfW`, `xSppB1sjfW` (bourgeons sessile, 9 nov.) : bons rameaux, mais bouquet terminal de deux ou trois bourgeons seulement.
- `p8w5YWVehw` : pédoncule qui continue au-delà des glands.
- `gOoY1ftSXO` : écorce en plaques rondes, aspect de boue séchée.
- `mE6ldDphJQ`, `3zHFUaJREY` : port trop régulier et symétrique pour un pédonculé.
- `8a4PcN0IrU`, `gOoBqtPSXO` : « plus haut que large » pris au pied de la lettre — silhouettes de peuplier, pas de chêne sessile ; le prompt retenu fixe les proportions (tronc nu sur la moitié de la hauteur, houppier ovale large des deux tiers de sa hauteur) et dit « c'est un chêne, pas un peuplier ».

## Prompts des éléments

**Feuille pédonculé** (dessin retenu, 8 nov.). Une seule feuille adulte de chêne pédonculé (Quercus robur) vue de dessus, verticale, sur un court bout de rameau. Le pétiole est quasi inexistant, 2 à 3 millimètres, la feuille semble collée au rameau ; base du limbe cordée avec deux petits lobes arrondis (oreillettes) de chaque côté ; limbe obovale, 8 à 10 lobes arrondis inégaux et irréguliers, plus grande largeur dans le tiers supérieur, sommet large ; nombreuses petites nervures intercalaires aboutissant dans les sinus ; limbe mat.

*Formulation la plus explicite essayée le 9 nov., sans succès en mode auto — à reprendre avec une image de référence :* « Key feature: an AURICULATE base. The blade narrows toward the base, then at the very base it flares out again into two small rounded ear-like lobes (auricles), one on each side, which point backwards and downwards and overlap the petiole; the petiole is extremely short, 3 to 5 millimetres, almost hidden between the two auricles. The auricles are clearly visible at first glance but small, about half the size of an ordinary lobe. »

**Feuille sessile.** Une seule feuille adulte de chêne sessile (Quercus petraea) vue de dessus, verticale, sur un court bout de rameau. Long pétiole net, 15 à 20 millimètres ; base du limbe en coin, sans oreillette ; limbe elliptique régulier, 10 à 14 lobes courts, arrondis, peu profonds, symétriques ; plus grande largeur à mi-hauteur ; sommet petit ; nervures secondaires allant chacune au bout d'un lobe, sans nervure intercalaire ; limbe luisant.

**Glands pédonculé.** Un court segment de rameau d'où part un long pédoncule grêle de 6 à 8 centimètres, tige fine et nue bien plus longue que les glands, portant à son extrémité deux glands mûrs allongés et cylindriques dans leur cupule à écailles serrées, nettement séparés ; une feuille à pétiole très court partiellement visible à la base.

**Glands sessile.** Un court segment de rameau portant, directement collés sur le bois sans aucune tige, un bouquet serré de trois ou quatre glands mûrs ovoïdes et trapus, plus larges à la base, dans leur cupule ; à côté, une feuille à long pétiole.

**Bourgeons pédonculé.** Extrémité d'un rameau d'hiver, grossie trois fois, sans feuilles : bouquet terminal de quatre ou cinq bourgeons ovoïdes, courts, globuleux et arrondis, à écailles imbriquées ; bourgeons latéraux plus petits le long du rameau anguleux, cicatrices foliaires.

**Bourgeons sessile** (9 nov.). Extrémité d'un rameau d'hiver de chêne sessile (Quercus petraea), sans feuilles, grossie trois fois, le rameau d'environ 10 centimètres de long posé en diagonale du coin inférieur gauche vers le coin supérieur droit, mince et anguleux, occupant presque toute la hauteur de l'image : à son extrémité, un bouquet terminal serré de quatre ou cinq bourgeons ovoïdes allongés, nettement pointus et effilés, fusiformes, de 8 millimètres de long, à écailles imbriquées, le bourgeon central un peu plus gros que les autres ; le long du rameau, trois ou quatre petits bourgeons latéraux pointus, alternes, au-dessus de cicatrices foliaires. Les bourgeons sont petits par rapport à la longueur du rameau.

**Écorce pédonculé.** Un carré d'environ 30 centimètres de tronc d'un vieux chêne pédonculé, vu de face : rhytidome très épais, profondément crevassé, en plaques trapézoïdales larges et bombées séparées par des sillons profonds, crêtes rugueuses. Cadrage serré sur l'écorce seule.

**Écorce sessile.** Un carré d'environ 30 centimètres de tronc d'un chêne sessile adulte : rhytidome mince, finement fissuré dans le sens de la longueur, en fines lanières verticales étroites, peu profondes et régulières, aspect finement strié. Cadrage serré sur l'écorce seule.

## Planche III, le port (générée le 9 novembre)

**Port pédonculé.** Silhouette complète d'un vieux chêne pédonculé isolé dans un pré, en hiver, sans feuilles, vu de face, des racines à la cime : tronc court et très massif qui se divise bas, à hauteur d'homme, en plusieurs grosses branches maîtresses tortueuses et noueuses, qui partent en coude, zigzaguent et changent de direction ; ramification désordonnée, asymétrique ; houppier très large, nettement plus large que haut, au contour irrégulier et bosselé ; aucune symétrie. Un homme debout au pied pour l'échelle.

**Port sessile.** Silhouette complète d'un chêne sessile adulte ayant poussé en forêt, en hiver, sans feuilles, vu de face, avec un homme au pied. C'est un chêne, pas un peuplier : proportions réalistes. Tronc droit et cylindrique, nu sur la moitié inférieure de la hauteur totale, puis prolongé dans le houppier en s'affinant ; houppier ovale et ample, à peu près aussi large que les deux tiers de sa propre hauteur, formé de branches assez fortes montant obliquement en éventail, ramification de chêne, rameaux anguleux ; contour régulier, sans branche basse.

## Contrôle contre la *Flore forestière française* (9 novembre)

Planches Q. robur (p. 731) et Q. petraea (p. 725) du tome 1, consultées sur l'exemplaire de l'auteur (photographies du 9 novembre, non versées au dépôt : œuvre protégée). Points vérifiés : feuille de pédonculé presque sessile, à oreillettes, lobes irréguliers ; glands de pédonculé au bout d'un long pédoncule, nettement séparés ; rameau de pédonculé à bourgeons ovoïdes groupés ; feuille de sessile à long pétiole et base en coin ; glands de sessile assis, groupés ; bourgeons de sessile ovoïdes pointus (figure cotée en millimètres). Les planches de la *Flore* montrent aussi la plantule (« sj ») et, pour le sessile, le gland germé — à prévoir pour la planche d'identification définitive (élément « plantule » de la fiche de prises de vue).

## Assemblage

`outils/compose_planches.py` assemble les planches (deux colonnes, une espèce par colonne ; une ligne par critère ; légendes tirées des fiches ; pièce de 1 € à l'échelle dans les cases au centimètre). Pour l'édition définitive : régénérer chaque élément en 2 k à partir des photographies de l'auteur, repasser la liste de contrôle de la charte (section 6 : vérification point par point contre la *Flore forestière française* et contre la photo d'origine), puis remplacer les fichiers de `elements/` et ajuster `ECHELLE` d'après la pièce photographiée.
