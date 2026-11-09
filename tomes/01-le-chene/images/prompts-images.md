# Tome 1 — Images de la maquette illustrée : prompts, identifiants, état

*Quarante-quatre images générées avec Magnific le 9 novembre 2026 entre 17 h 20 et 17 h 50 (compte abonné pascal.obstetar@gmail.com, plan Plus, mode auto, 2 k ; 65 crédits l'image, 100 pour les formats 2:1 — 3 245 crédits en tout, deux reprises comprises), d'après les seules légendes du texte (livraisons 1 à 3), qui servent de briefs. Aucune photographie ni planche d'autrui n'a été donnée au générateur ; le Jacques a pour seule référence sa planche modèle v0 (`JNhfAn4Oq4`, dessinée d'après la fiche de personnage). Les originaux 2 k sont dans le projet personnel Magnific de l'auteur ; les copies du dépôt font 1 024 px (maquette de relecture). Sept figures de données (cartes, échelle des vies, chromosomes, graphique IGN) ne sont pas générées mais dessinées en vectoriel par `outils/figures_vectorielles.py`.*

*Statut : **maquette d'étude**. Conformément à la charte (section 6), chaque image qui montre l'individu suivi, le village ou le Jacques sera refaite à partir des photographies de l'auteur ; les planches d'identification (feuilles des cousins, fleurs, galles, hôtes du vieux bois) passeront la liste de contrôle botanique avant parution. Les numéros, cercles, légendes internes et flèches ne sont jamais générés : ils seront posés en vectoriel à la mise en page.*

## Les deux blocs de style

**Gravure** (planches, coupes, schémas) :
```
Gravure botanique scientifique en noir et blanc, dessin hyperréaliste à la plume, hachures fines, papier blanc, sans aucun texte ni lettre ni chiffre ni légende ni cadre. [sujet]
```

**Scène** (l'année, la vie, les habitants, l'arbre et nous) :
```
Illustration de livre naturaliste : dessin à la plume et à l'encre noire, hachures fines pour les volumes, rehaussé d'un lavis d'aquarelle sobre en deux ou trois teintes (vert sourd, ocre, brun), papier blanc visible, sans aucun texte ni lettre ni chiffre ni légende ni cadre. [sujet]
```

Pour le Jacques, on ajoute la référence `JNhfAn4Oq4` (type image) et la formule « le geai des chênes de l'image de référence, exactement le même oiseau, même trait et mêmes couleurs ».

## Les images, page par page

| Page | Identifiant | Format | Sujet (après le bloc de style) | Contrôle et réserves |
|---|---|---|---|---|
| 1 | `TdlylfPVNR` | 3:4, gravure | Un seul gland de chêne pédonculé germé, posé au centre du papier blanc, vu de côté : la coque brune fendue à la pointe, une radicule blanche et épaisse qui en sort et plonge vers le bas en s'effilant, la cupule écailleuse encore attachée. Rien d'autre, beaucoup de blanc autour. | Conforme. |
| 3 | `fHZcZSSCDY` | 3:4, scène + réf. | Le geai de référence posé de trois quarts sur une branche de chêne en octobre, un gland dans le bec, le gosier visiblement gonflé par d'autres glands ; quelques feuilles brunies et un gland sur la branche. Fond blanc. | Gosier non gonflé (comme J2) : à demander autrement en v1. Provisoire : Jacques v0. |
| 6-7 (2) | `eI767rRdqL` | 2:1, gravure | Sept feuilles de chênes européens côte à côte à la même échelle, bien séparées, chacune avec son pétiole : pubescent (lobée, dessous duveteux) ; chêne vert (petite, ovale, entière, à bord légèrement denté, dessous feutré) ; chêne-liège (petite, ovale, dentée) ; kermès (très petite, bord épineux comme du houx) ; tauzin (profondément lobée, lobes étroits et irréguliers) ; chevelu (lobée, lobes pointus) ; rouge d'Amérique (grande, lobes pointus terminés par une fine soie). | Planche d'identification : à contrôler feuille par feuille contre la *Flore* (le tauzin et le chevelu surtout). |
| 8 | `fHZcZ44CDY` | 3:4, scène | Un chêne pédonculé isolé dans une haie de plaine, vu depuis un chemin de terre, fin avril : grosses branches tortueuses encore entièrement nues, alors que la haie, le pré et un saule à gauche au bord d'une mare sont déjà en feuilles vert tendre. Ciel clair, Lorraine. | **Provisoire** : individu suivi, à refaire d'après la photo de l'auteur, même point de vue. |
| 9 | `LwdhdMFswO` | 2:1, scène | Le même rameau de chêne pédonculé dessiné quatre fois côte à côte, à quinze jours d'intervalle : bourgeons éclatés laissant sortir de minuscules feuilles rouges froissées ; jeunes feuilles cuivrées lobées, molles et pendantes ; feuilles vert tendre dépliées ; feuilles vertes coriaces de plein été. Même échelle. | Conforme. |
| 10 | `jUemeePLD0` | 3:2, gravure + rouge | À gauche, un chaton mâle grandeur nature pendant d'un rameau au feuillage naissant ; à droite, très agrandies, trois fleurs femelles au sommet d'un long pédoncule dressé, chacune un minuscule bourgeon écailleux coiffé de trois stigmates recourbés, seuls rehaussés de rouge. | Stigmates à vérifier sur le vivant en mai. |
| 11 | `u5GVGWBQLD` | 3:4, scène | Sous une branche de chêne en mai aux feuilles trouées, une chenille verte de tordeuse descend au bout d'un fil de soie ; au-dessus, une mésange charbonnière en vol, une chenille au bec. | Conforme. |
| 12 | `8a424ZkIrU` | 3:2, scène | Rameau de chêne en juillet : premières feuilles mangées, réduites aux nervures et à des lambeaux ; au bout, une pousse de la Saint-Jean droite aux jeunes feuilles rouge cuivré, contrastant avec les vieilles feuilles vert sombre. | Conforme. |
| 13 | `fHZcZBBCDY` | 3:4, scène | Le houppier d'un grand chêne vu d'en bas, allongé au pied du tronc, un midi de juillet : grosses branches en étoile, feuillage en couches, taches de ciel. Pleine page. | Conforme. |
| 14 | `P3fbf7X42C` | 3:2, gravure | Cinq galles grandeur nature : galle-cerise sous une feuille ; galle en artichaut au bout d'un rameau ; pomme de chêne spongieuse ; petite galle lenticulaire au revers d'une feuille ; noix de galle ligneuse. À droite, une galle coupée : chambre centrale et larve blanche repliée. | Conforme ; noms à vérifier contre un guide des galles. |
| 15 | `mE6z6tAhJQ` | 3:4, gravure | En haut un rameau à pousse de la Saint-Jean ; en dessous, très agrandie, la coupe d'un cerne : bois initial à gros vaisseaux ronds en anneau, bois final dense, limite nette, rayons ligneux. | Schéma : à vérifier contre une vraie coupe. |
| 16 | `1lM8DLbr4r` | 3:2, gravure | Balanin très grossi (corps ovale écailleux, rostre très fin et long recourbé, antennes coudées) ; gland vert coupé en long avec sa larve blanche en C ; gland brun entier percé d'un trou de sortie rond. | Conforme. |
| 17 | `mE6ziQThJQ` | 3:2, scène | Rameau fin août : feuilles coriaces vert sombre, ternes, tachées, grignotées ; deux glands verts allongés en cupule sur un long pédoncule grêle. | Conforme. |
| 18 | `0esOlItTfW` | 3:4, scène | Le chêne de haie en octobre, feuillage brun-roux clairsemé, glands dans l'herbe ; à l'orée d'un bois, une laie et ses marcassins rayés. Lumière basse. | **Provisoire** : individu suivi. |
| 19 | `79mQhG1JAL` | 2:1, gravure | Six glands en ligne, grandeur nature : labouré par un groin ; entaillé par des incisives ; décortiqué par lambeaux ; intact et luisant ; intact dans sa cupule ; percé d'un trou de sortie. | Conforme. |
| 20 | `1lM8Digr4r` | 4:3, scène + réf. | Le geai de référence, de profil au sol dans une friche d'octobre, le bec enfoncé dans la mousse où il cache un gland, la queue relevée ; herbes sèches, feuilles mortes, un gland à côté. | Conforme ; la carte des caches (partie droite de la légende) reste à dessiner en vectoriel. Provisoire : Jacques v0. |
| 21 | `iGFrbhR3uK` | 3:4, gravure + brun | Coupe du sol d'une friche en novembre : litière de feuilles mortes ; juste dessous un gland couché dont la radicule blanche plonge sur vingt centimètres ; aucune tige. Fines racines des herbes. | Conforme. |
| 22 | `TdlyUrAVNR` | 3:2, scène | Friche fin novembre : ronces aux dernières feuilles rougies, herbes couchées, prunelliers, brume basse ; au fond une haie et un grand chêne nu. Aucun animal, aucune personne. | Conforme. |
| 23 | `Cq20z2lEEy` | 3:4, scène | Le chêne de haie en janvier, entièrement nu, branches maîtresses en coude, givre, saule nu, mare gelée, ciel bas. | **Provisoire** : individu suivi ; médaillon des bourgeons (planche II) et vignette du village à ajouter. |
| 24 | `lJBaItBgv9` | 3:4, scène | Un morceau d'écorce grandeur nature : quatre lichens (plaques grises, rosettes jaune vif, foliacé gris-vert, buisson gris), mousse à la base ; dans une crevasse, araignée, chrysalide, grappe d'œufs, trou de sortie. | Conforme ; numéros à poser en vectoriel. |
| 25 | `8a426AKIrU` | 3:4, gravure | Rondelle de chêne de quatre-vingts ans : écorce, aubier clair, cœur sombre, cernes larges et étroits, fente radiale ; dessous, tarière de Pressler et carotte. | Conforme ; années à légender en vectoriel. |
| 26 | `gOoftQtSXO` | 3:2, scène | Jeune chêne de deux ans à tige coupée en biais par un chevreuil, repousse latérale ; à droite, gros plan d'une tige portant la trace de dents. | La trace est dessinée sur un tronc épais : à refaire sur une tige fine. |
| 27 | `dtJiPnvXSL` | 3:4, scène | Friche fin mars ; au premier plan, une tige rouge sombre de dix centimètres sort d'un coussin de mousse et déplie quatre petites feuilles rougeâtres ; au fond, haie et grand chêne nu. | Conforme. |
| 28 | `vQ3Y2B6a47` | 3:2, gravure | Gland de pédonculé coupé en long dans sa cupule : paroi, tégument, deux gros cotylédons, embryon et radicule à la pointe ; à droite, gland entier de sessile, plus court et plus large. | Conforme ; termes à poser en vectoriel. |
| 29 | `s7Xvtwml8e` | 3:2, scène | Nature morte : glands, glands pelés, bol de farine grise, tasse de café fumante, torchon de lin. | Conforme. |
| 30 | `UPIEaNjwny` | 4:3, scène | Vue aérienne oblique d'un village lorrain de plaine : toits serrés le long d'une rue unique, clocher, vergers, prés, haies, un grand chêne isolé, une friche, la lisière d'un bois. Aucun personnage. | Conforme ; les trois cercles à poser en vectoriel. |
| 31 | `yiaqQnJPW9` | 2:1, gravure | Trois stades à la même échelle, sol en coupe : gland à radicule ; jeune tige rougeâtre qui lève, gland vidé sous terre ; plantule de juin à six feuilles et pivot trois fois plus long que la tige. | Conforme. |
| 32 | `O6vHu08ynm` | 1:1, scène | Semis de six feuilles au centre ; en cercle, six dessins séparés : tête de chevreuil ; feuille noircie givrée ; sol craquelé sous un soleil ; feuille poudrée de blanc ; ombre d'un arbre ; rameau de ronce. | Conforme. |
| 33 | `jUem8GELD0` | 2:1, gravure | Quatre chênes à la même échelle : semis d'un an (enfant à côté), dix ans (enfant), cinquante ans (adulte), cent cinquante ans (adulte). | Conforme. |
| 34 | `6AQ15hhiJO` | 3:4, scène | Chêne de haie de quatre-vingts ans en plein été, branches basses, houppier large ; un adulte de dos au pied. | **Provisoire** : individu suivi ; médaillon de la coupe du tronc à ajouter. |
| 35 | `MBS4OsnDCm` | 3:4, scène | Coupe du sol sous un chêne en octobre : cèpe, russule, amanite tue-mouches en surface ; pivot, traçantes, radicelles gainées de filaments blancs reliés aux champignons. | Conforme. |
| 37 | `s7Xvto4l8e` | 3:4, scène | Très vieux chêne de plein champ, trapu, tronc creux, cime descendante aux branches mortes blanchies ; langue-de-bœuf rouge, polypore soufré jaune ; cavités, écorce décollée, pied creux. | Conforme ; repères numérotés à poser en vectoriel. |
| 38 | `1lM8te4r4r` (remplace `KLTBdqZkqp`) | 3:4, planche | Lucane et sa larve ; grand capricorne et sa galerie ; pique-prune sur du terreau ; pic mar (tout le dessus de la tête rouge) à sa loge ; noctule accrochée ; martre au poitrail jaune. | Première version : pic épeiche (calotte noire, nuque rouge) au lieu du pic mar — refaite ; la seconde a la calotte rouge, la moustache reste à corriger en v1. |
| 39 | `bxcdeK15Y2` | 2:1, scène | Le même chêne mort debout (chandelle écorcée, trous de pics) puis couché (motte dressée, trou d'eau, mousses, fougères, semis sur le tronc). | Conforme. |
| 40-41 | `XmO3iv5Bfo` | 3:4, scène | Le chêne de haie en coupe du sous-sol à la cime, comme une maison ouverte : racines, terrier de blaireau, mulot, ver, larve ; cèpe, langue-de-bœuf, fougères, lierre ; lichens, grimpereau, sittelle, pic épeiche, chauve-souris ; hulotte, martre ; chenilles, galles, mésange, écureuil et son nid, pigeon ramier, geai ; buse au sommet. | Conforme ; vérifier la présence des trente habitants, numéros à poser en vectoriel. |
| 42-43 | `3zHxrVyREY` | 2:1, planche + réf. | Cinq portraits séparés : le geai de référence ; un cynips près d'une galle ; une chenille de processionnaire grise à longs poils et bande sombre ; un lucane mâle ; un balanin. | Conforme ; le réseau du bas de double page reste à dessiner en vectoriel. |
| 44 | `0esOJftTfW` | 2:1, gravure | Trois chênes adultes à la même échelle, un homme au pied de chacun : isolé (tronc court, houppier large) ; en forêt mélangée (fût long, houppier haut) ; en futaie pure (colonne parmi les colonnes, sol nu). | Conforme. |
| 45 | `cpLJ7EC0eP` | 3:4, scène | Depuis le pied d'un chêne, la lumière de juin à travers le feuillage : rayons obliques, taches de soleil sur l'herbe et l'écorce, feuilles à contre-jour. | Conforme. |
| 48 | `Sy8CfVMUb8` | 2:1, scène | Ferme de charpente ancienne (tenons, chevilles) ; merrain fendu au coin, fil droit visible ; barrique en cours de montage, douelles en rose cerclées de fer. | Conforme. |
| 49 | `tCNGnybmZJ` (remplace `p8wN9soehw`) | 3:2, scène | Page de parchemin dont l'écriture n'est suggérée que par des lignes ondulées, lettrine en feuille de chêne ; noix de galle ; botte d'écorces liées ; écorçoir en os de cheval ; encrier. | Première version : pseudo-texte lisible (« fausse manuscrit médiéval… »), contraire à la charte — refaite sans lettre. |
| 50 (frise) | `9ZEK5KCNYZ` | 2:1 (4:1 refusé), gravure | Cinq scènes alignées : prêtres grecs au pied du chêne de Dodone ; missionnaire abattant un chêne à la hache devant la foule ; druide à la faucille cueillant le gui ; roi couronné assis au pied d'un chêne écoutant des paysans ; révolutionnaires plantant un jeune arbre sur une place. | Conforme. |
| 53 | `P3fbqx242C` | 2:1, scène + réf. | Haie de plaine en octobre : très vieux chêne roux chargé de glands à gauche, friche aux ronces, jeune chêne de deux ans isolé loin à droite ; dans la haie, le geai de référence, un gland au bec. | Conforme. Provisoire : Jacques v0. |

## Figures dessinées en vectoriel (`outils/figures_vectorielles.py`)

| Page | Fichier | Contenu | Ce qu'il faut savoir |
|---|---|---|---|
| 6-7 (1) | `p06-07-carte-deux-chenes` | Présence du pédonculé et du sessile par département. | Transcription indicative des cartes IGN/MFR ; la liste des départements « absents » est dans le script, à vérifier. |
| 36 | `p36-echelle-des-vies` | Les 25 espèces : première graine, vie courante, record. | Valeurs de l'annexe A du chemin de fer, à confirmer. |
| 46 | `p46-europe-refuges` | Glace, steppe, trois refuges, flèches de la remontée. | Limite des glaces simplifiée ; d'après Brewer 2002 et Petit 2002. |
| 47 | `p47-france-trois-chenes` | Trois cartes : pédonculé, sessile, pubescent ; flèches ; Verdun et Tronçais. | Aires indicatives par département. |
| 50 (carte) | `p50-carte-toponymes` | Dix-sept noms de lieux en trois couleurs. | Exemples choisis ; les noms lorrains sont à fournir. |
| 51 | `p51-chromosomes` | Douze chromosomes, mutations, deux régions de résistance. | Longueurs et positions indicatives (Plomion 2018, Bartholomé 2020). |
| 52 | `p52-graphique-ign` | Mortalité par période ; symptômes par essence en 2025. | La barre 2015-2024 n'a pas de valeur affichée : seul le « + 125 % » est publié. |

## Écartés

- `KLTBdqZkqp` (p. 38) : pic épeiche au lieu du pic mar.
- `p8wN9soehw` (p. 49) : texte parasite lisible sur le manuscrit.

Les deux sont conservés dans `images/ecartes/`.
