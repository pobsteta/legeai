# Le Jacques — images du narrateur (maquette d'étude v0, 9 novembre 2026)

*Ce dossier contient la première planche modèle du Jacques et ses douze attitudes, générées avec Magnific (plan Plus, 2 k) le 9 novembre 2026, d'après le brief `collection/05-brief-atrioma-planche-modele-du-jacques.md` et la fiche de personnage `collection/04-fiche-de-personnage-le-jacques.md`. C'est une **maquette d'étude** : le Jacques y est dessiné à partir de la seule description écrite de la fiche (sections 2 à 5), aucune photographie ni dessin d'autrui n'ayant été donné au générateur. La version définitive (`Jacques_modele_v1`) sera refaite à partir des photographies de geais de l'auteur (fiche de prises de vue, point E), en image de référence, puis gelée et déposée avec la marque.*

## Contenu

| Fichier | Ce que c'est |
|---|---|
| `Jacques_planche_v0.png` / `.pdf` | La planche de présentation : trois angles, douze attitudes avec leur bulle d'exemple, huit têtes, pied explicatif. |
| `sources/Jacques_modele_v0_JNhfAn4Oq4.png` | Passe A — planche modèle, trois angles (profil, trois-quarts, face), 1 024 px. **Image de référence** de toutes les autres générations. |
| `sources/Jacques_tetes_v0_p8wO1Zwehw.png` | Passe C — les huit têtes (neutre, curieux, fier, vexé, endormi, crieur, complice, surpris). |
| `sources/Jacques_Jnn_nom_<identifiant>.png` | Passe B — les douze attitudes, fond blanc, 800 px (copies locales ; originaux 2 k dans le projet Magnific de l'auteur). |
| `vignettes/Jacques_Jnn_nom_v0.png` | Les mêmes, **détourées** (PNG à fond transparent), prêtes à poser dans la marge ; détourage par remplissage depuis les bords (`outils/jacques_planche.py`). |
| `PatrickHand-Regular.ttf`, `OFL-PatrickHand.txt` | La police manuscrite proposée pour les bulles (Patrick Hand, Patrick Wagesreiter, licence SIL OFL 1.1 — impression commerciale autorisée), avec sa licence. |

## Les douze attitudes retenues

| N° | Pose | Identifiant Magnific | Variante non retenue | Contrôle |
|---|---|---|---|---|
| J1 | Le guetteur | `lJBIZTbgv9` | `vQ32jySa47` (de profil strict) | Conforme. |
| J2 | Le porteur | `iGFbe9g3uK` | `u5GYUCJQLD` (tourné à gauche) | Gland au bec, corps penché : conforme ; **le gosier n'est pas visiblement gonflé** — à demander explicitement dans la v1. |
| J3 | Le planteur | `gOotGRgSXO` | `huiZL13vqL` | Bec dans la mousse, gland à demi visible, queue relevée : conforme. |
| J4 | Le chercheur | `bxcVPzh5Y2` | `bxcVPnv5Y2` (non examiné) | Patte qui gratte, trois feuilles mortes, traits de mouvement : conforme. |
| J5 | En vol | `aFRAlMWfSh` | `u5GYwdkQLD` (vue de face, bon aussi) | Vu de dessus, deux panneaux bleus, croupion blanc, queue déployée : conforme. |
| J6 | Le vantard | `huiZsfSvqL` | `rgDd3jbxtc` (tête trop tournée) | Huppe dressée, poitrail bombé, bec levé, queue relevée : conforme. |
| J7 | Le vexé | `KLTDN4Kkqp` | `s7X8AZJl8e` (bon aussi) | Tête rentrée, œil vers le bas, huppe plaquée : conforme. |
| J8 | Le dubitatif | `JNhf0hnOq4` | `0esSEs9TfW` (bon aussi) | Tête penchée, œil sur le lecteur : conforme. |
| J9 | La sentinelle | `tCN3jMpmZJ` | `Lwdo2qAswO` | De face, bec ouvert, huppe dressée, ailes écartées : conforme. |
| J10 | Le gourmand | `O6vCVRhynm` | `aFRAS5EfSh` | Chenille verte au bec, œil vers le lecteur : conforme. |
| J11 | Le patient | `rgDdRY3xtc` | `DoUJqr2pcl` | En boule, paupière mi-close, huppe plaquée : conforme. |
| J12 | Le scribe | `Bhy912VoQR` | `P3fuDkp42C` | Plume bleue barrée de sa propre aile au bec, sur une pierre plate : conforme. |

Planche modèle : `JNhfAn4Oq4` retenu ; variantes `lJBI6iDgv9`, `79ma2GNJAL`, `s7X8NiEl8e` (toutes conformes, trait très proche). Têtes : `p8wO1Zwehw` retenu ; `mE6RUTNhJQ` écarté (clin d'œil et sourcil froncé, interdits par la fiche).

## Ce que le contrôle a donné (fiche de personnage, section 10)

- Calotte striée noir et blanc, moustache noire, gorge blanche, iris pâle, un seul œil de profil, pas de sourcil : **conforme** sur les douze.
- Panneau bleu barré de noir sur l'aile seulement, tache blanche de l'aile, rémiges noires, queue noire : **conforme**. Croupion blanc : visible en J5 et sur les poses de dos ; caché ailleurs, c'est normal.
- Bec fort et sombre, pattes brun rosé : conforme. **Doigts** : le nombre n'est pas toujours lisible (trois devant, un derrière) — à vérifier en v1 à partir des photos.
- Rien d'humain, aucun signe de bande dessinée autre que les traits de mouvement (J4) : conforme.
- Même trait et même palette que la planche A : conforme — c'est l'apport de l'image de référence : vingt-deux générations, un seul oiseau.
- **Réserves pour la v1** : le dos est rendu plus gris que nature (le manteau d'un geai est brun rosé, à peine plus gris que le ventre) ; le gosier de J2 ; le détail des doigts ; et, par construction, aucune de ces images ne vient encore d'une photographie de l'auteur.

## Comment on s'en sert

- Dans la marge extérieure (30 mm), oiseau de 22 à 30 mm de haut, une bulle par page, deux vignettes par double page au plus (charte, section 6 ; fiche, section 3).
- La bulle est posée à la maquette, en vectoriel, en Patrick Hand 11 à 12 points, pointe vers le bec ; jamais générée dans l'image.
- Nommage dans les tomes : `Jacques_J03_planteur_T01p20_v0.png` (pose, nom, tome et page, version).

## Coût

Passe A : 4 images × 65 crédits ; passe B : 24 × 65 ; passe C : 2 × 100 — soit 2 020 crédits environ, le 9 novembre 2026, sur le compte abonné.
