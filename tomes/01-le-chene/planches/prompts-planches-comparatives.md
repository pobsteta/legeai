# Tome 1 — Planches comparatives pédonculé / sessile : prompts et état

*Dessins « hyperréalistes » en noir et blanc, style gravure botanique, générés le 8 novembre 2026 avec Magnific (mode auto, offre gratuite, 1 k) à partir des seuls critères écrits des fiches CNPF et de la formation ONF 2008 de F. Lebourgeois — les photographies de ces documents sont protégées et n'ont jamais été données au générateur ; elles ont servi au contrôle, après coup, comme le veut la charte (section 6). Les originaux (1 024 px) sont dans le projet personnel Magnific de l'auteur, sous les identifiants ci-dessous ; les copies du dépôt font 600 × 800 px (maquette d'étude). Pour l'impression, régénérer en 2 k ou refaire dans Atrioma avec les mêmes prompts, puis repasser la liste de contrôle.*

## Bloc de style (en tête de chaque prompt)

```
Gravure botanique scientifique en noir et blanc, dessin hyperréaliste à la plume, hachures fines, papier blanc, sans aucun texte ni lettre ni légende. [sujet] Rien d'autre dans l'image.
```

## Éléments retenus

| Élément | Identifiant Magnific | Fichier | Contrôle |
|---|---|---|---|
| Feuille pédonculé | `ovPxVs5829` | `elements/pedoncule_feuille.png` | Pétiole court, lobes irréguliers, plus large au tiers supérieur, petites oreillettes : conforme. Les oreillettes restent discrètes ; à accentuer légèrement dans la version définitive. |
| Feuille sessile | `Sy8W1prUb8` (variante `1lMRQYIr4r`) | `elements/sessile_feuille.png` | Long pétiole, base en coin, lobes réguliers, plus large au milieu : conforme. |
| Glands pédonculé | `gOoYkr9SXO` | `elements/pedoncule_glands.png` | Long pédoncule grêle, glands allongés à l'extrémité : conforme (les deux glands sont jointifs ; par un à trois, parfois espacés, dans la nature). |
| Glands sessile | `1lMRQkUr4r` | `elements/sessile_glands.png` | Glands trapus en bouquet, assis sur le rameau, feuille à long pétiole : conforme. |
| Bourgeons pédonculé | `8a4jDvtIrU` | `elements/pedoncule_bourgeons.png` | Bourgeons globuleux en bouquet terminal : conforme. |
| Bourgeons sessile | `u5GOm10QLD` | `elements/sessile_bourgeons.png` | Bourgeons pointus, effilés : conforme (bouquet de deux ; en préférer quatre ou cinq dans la version définitive). |
| Écorce pédonculé | `1lMRF8Er4r` (recadrée : signature parasite en bas à droite) | `elements/pedoncule_ecorce.png` | Plaques larges et profondes, sillons marqués : conforme aux photos Lebourgeois (rhytidome épais, trapézoïdal). |
| Écorce sessile | `fHZw8DqCDY` | `elements/sessile_ecorce.png` | Fissures fines en long, lanières étroites : conforme (rhytidome mince, fissuré en long). |

## Écartés

- `N2uXUhs6D9` (premier essai) : pétiole long et texte parasite — feuille de sessile déguisée.
- `huigdqzvqL`, `ksV3uUq16B` : base cunéiforme, trop régulières pour un pédonculé.
- `xSp2HzLjfW` : « oreillettes » caricaturales, deux lobes ronds énormes.
- `p8w5YWVehw` : pédoncule qui continue au-delà des glands.
- `gOoY1ftSXO` : écorce en plaques rondes, aspect de boue séchée.
- `mE6ldDphJQ` : port trop régulier et symétrique pour un pédonculé — à refaire.

## Prompts des éléments

**Feuille pédonculé.** Une seule feuille adulte de chêne pédonculé (Quercus robur) vue de dessus, verticale, sur un court bout de rameau. Le pétiole est quasi inexistant, 2 à 3 millimètres, la feuille semble collée au rameau ; base du limbe cordée avec deux petits lobes arrondis (oreillettes) de chaque côté ; limbe obovale, 8 à 10 lobes arrondis inégaux et irréguliers, plus grande largeur dans le tiers supérieur, sommet large ; nombreuses petites nervures intercalaires aboutissant dans les sinus ; limbe mat.

**Feuille sessile.** Une seule feuille adulte de chêne sessile (Quercus petraea) vue de dessus, verticale, sur un court bout de rameau. Long pétiole net, 15 à 20 millimètres ; base du limbe en coin, sans oreillette ; limbe elliptique régulier, 10 à 14 lobes courts, arrondis, peu profonds, symétriques ; plus grande largeur à mi-hauteur ; sommet petit ; nervures secondaires allant chacune au bout d'un lobe, sans nervure intercalaire ; limbe luisant.

**Glands pédonculé.** Un court segment de rameau d'où part un long pédoncule grêle de 6 à 8 centimètres, tige fine et nue bien plus longue que les glands, portant à son extrémité deux glands mûrs allongés et cylindriques dans leur cupule à écailles serrées, nettement séparés ; une feuille à pétiole très court partiellement visible à la base.

**Glands sessile.** Un court segment de rameau portant, directement collés sur le bois sans aucune tige, un bouquet serré de trois ou quatre glands mûrs ovoïdes et trapus, plus larges à la base, dans leur cupule ; à côté, une feuille à long pétiole.

**Bourgeons pédonculé.** Extrémité d'un rameau d'hiver, grossie trois fois, sans feuilles : bouquet terminal de quatre ou cinq bourgeons ovoïdes, courts, globuleux et arrondis, à écailles imbriquées ; bourgeons latéraux plus petits le long du rameau anguleux, cicatrices foliaires.

**Bourgeons sessile.** Même cadrage : bouquet terminal de quatre ou cinq bourgeons ovoïdes allongés, nettement pointus et effilés, fusiformes ; bourgeons latéraux pointus.

**Écorce pédonculé.** Un carré d'environ 30 centimètres de tronc d'un vieux chêne pédonculé, vu de face : rhytidome très épais, profondément crevassé, en plaques trapézoïdales larges et bombées séparées par des sillons profonds, crêtes rugueuses. Cadrage serré sur l'écorce seule.

**Écorce sessile.** Un carré d'environ 30 centimètres de tronc d'un chêne sessile adulte : rhytidome mince, finement fissuré dans le sens de la longueur, en fines lanières verticales étroites, peu profondes et régulières, aspect finement strié. Cadrage serré sur l'écorce seule.

## À générer (quota du jour atteint) — planche III, le port

**Port pédonculé.** Dessin à la plume, noir et blanc, sans texte. Silhouette complète d'un chêne pédonculé adulte isolé dans un pré, en hiver, sans feuilles, vu de face, des racines à la cime : tronc court et massif qui se divise bas en grosses branches maîtresses tortueuses et noueuses partant en coude ; ramification désordonnée ; houppier très large, plus large que haut, au contour irrégulier. Un homme debout au pied pour l'échelle. *Insister sur l'irrégularité : le premier essai a donné un arbre symétrique.*

**Port sessile.** Même consigne : fût droit, long et conique, sans branche basse, qui monte haut avant de se diviser ; branches régulières, fines, dressées en éventail ; houppier régulier, plus haut que large. Un homme au pied.

## Assemblage

`outils/compose_planches.py` assemble les planches (deux colonnes, une espèce par colonne ; une ligne par critère ; légendes tirées des fiches). Pour l'édition définitive : régénérer chaque élément en 2 k, repasser la liste de contrôle de la charte (section 6 : vérification point par point contre la *Flore forestière française* et contre une photo de l'auteur), puis remplacer les fichiers de `elements/`.
