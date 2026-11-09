# -*- coding: utf-8 -*-
"""Passe de sourçage du 9 novembre 2026 au soir : lève les mentions « à préciser »
des livraisons 1 et 2 (notes de bas de page), ajuste deux phrases du corps de texte
(anthocyanes p. 9, dessiccation p. 29), met à jour la bibliographie de la livraison 4.
Script à usage unique, conservé pour mémoire ; chaque remplacement est vérifié (assert)."""
import re, sys

REP = "/home/claude/legeai/tomes/01-le-chene/texte/"

def load(n):
    return open(REP + n, encoding="utf-8").read()

def save(n, s):
    open(REP + n, "w", encoding="utf-8").write(s)

def rep(s, old, new, count=1):
    assert old in s, "introuvable : " + old[:90]
    return s.replace(old, new, count)

# ---------------------------------------------------------------- livraison 1
L1 = "livraison-1-p01-27.md"
s = load(L1)

# p. 9 — anthocyanes : corps + note
s = rep(s,
 "Pourquoi rouges ? Les pigments rouges des jeunes feuilles sont les mêmes que ceux de l'automne. Au printemps, ils font office de parasol : ils protègent des tissus tout neufs, encore incapables de se défendre, d'un soleil d'avril déjà fort (1). Quand la feuille a fabriqué assez de chlorophylle, le rouge s'efface.",
 "Pourquoi rouges ? Les pigments rouges des jeunes feuilles sont les mêmes que ceux de l'automne. On leur prête deux rôles au printemps : un parasol pour des tissus tout neufs, encore incapables de se défendre d'un soleil d'avril déjà fort ; et une protection contre les insectes, qui mangent moins les feuilles rouges que les vertes — c'est ce second rôle que l'on a le mieux mesuré, chez un chêne du Midi (1). Quand la feuille a fabriqué assez de chlorophylle, le rouge s'efface.")
s = rep(s,
 "**(1)** Rôle protecteur des anthocyanes dans les jeunes feuilles : Lee D.W., Gould K.S., 2002, *Anthocyanins in leaves and other vegetative organs*, Advances in Botanical Research 37 — à préciser.",
 "**(1)** Rôle des anthocyanes dans les jeunes feuilles : Lee D.W., Gould K.S., 2002, *Anthocyanins in leaves and other vegetative organs: an introduction*, Advances in Botanical Research 37 : 1-16 ; sur un chêne, le kermès (*Quercus coccifera*) : Karageorgou P., Manetas Y., 2006, *The importance of being red when young: anthocyanins and the protection of young leaves of Quercus coccifera from insect herbivory and excess light*, Tree Physiology 26 : 613-621 — l'effet parasol n'est que faiblement mesuré sur le terrain ; les feuilles rouges sont surtout moins attaquées par les insectes que les vertes.")

# p. 13 — 900 becquées
s = rep(s,
 "**(1)** Jusqu'à 900 becquées par jour pour un couple de mésanges charbonnières — chiffre repris par le Muséum national d'histoire naturelle et la LPO dans leurs documents grand public ; à préciser par la source primaire.",
 "**(1)** Jusqu'à 900 becquées par jour : maximum pour une grande nichée, chiffre repris par le Muséum national d'histoire naturelle et la LPO. Mesures de la fréquence de nourrissage de la mésange charbonnière, au nichoir et par caméra : Gibb J.A., 1955, *Feeding rates of great tits*, British Birds 48 : 49-58 ; Royama T., 1966, *Factors governing feeding rate, food requirement and brood size of nestling great tits*, Ibis 108 : 313-347 ; Barba E. et al., 2009, *Patterns of nestling provisioning by a single-prey loader bird, great tit Parus major*, Bird Study 56 : 187-197 — la fréquence croît avec la taille de la nichée et l'âge des poussins ; plusieurs centaines de visites par jour est l'ordre de grandeur courant.")

# p. 14 — cynips, encre
s = rep(s,
 "**(1)** Cycle hétérogonique des cynips du chêne : *Flore forestière française*, t. 1, et littérature entomologique — à préciser (ex. Stone G.N. et al., 2002, Annual Review of Entomology 47).",
 "**(1)** Cycle hétérogonique des cynips du chêne (alternance d'une génération sexuée et d'une génération de femelles seules, chacune avec sa galle) : Stone G.N., Schönrogge K., Atkinson R.J., Bellido D., Pujade-Villar J., 2002, *The population biology of oak gall wasps (Hymenoptera: Cynipidae)*, Annual Review of Entomology 47 : 633-668 ; *Flore forestière française*, t. 1.")
s = rep(s,
 "**(2)** Histoire et chimie de l'encre ferro-gallique — à préciser (ex. Bibliothèque nationale de France, dossiers sur les encres anciennes).",
 "**(2)** Encre ferro-gallique — composition (tanins de noix de galle, sulfate de fer, gomme arabique), usage du haut Moyen Âge au XXe siècle, altération des manuscrits : Rouchon V. et al., 2011, *Les encres ferro-galliques*, CeROArt ; Université de Liège, atelier *Encres anciennes : l'encre ferro-gallique*, 2012 ; la recette est page 55.")

# p. 16 — balanin
s = rep(s,
 "**(1)** Biologie du balanin des glands : *Flore forestière française*, t. 1 ; Bonal R. et al., travaux sur *Curculio* et la prédation des glands — à préciser.",
 "**(1)** Biologie du balanin des glands : *Flore forestière française*, t. 1 ; Espelta J.M., Bonal R., Sánchez-Humanes B., 2009, *Pre-dispersal acorn predation in mixed oak forests*, Journal of Ecology 97 : 1416-1423 (*Curculio glandium* et *C. elephas* : ponte dans le gland vert, phénologie, taille minimale du gland) ; Bonal R., Muñoz A., 2009, *Seed weevils living on the edge*, Ecological Entomology 34 : 304-309 (la larve accomplit tout son développement dans un seul gland, aux dépens des cotylédons) ; Bonal R., Muñoz A., Díaz M., 2007, *Satiation of predispersal seed predators*, Evolutionary Ecology 21 : 367-380 (la part prélevée est plus forte les années de petite récolte).")

# p. 18 — production, masting
s = rep(s,
 "**(1)** Production de glands d'un chêne adulte : ONF, *Rendez-vous techniques* n° 13, 2006 (fructification des chênes) ; WSL, réseau mastweb.ch, fiche *Quercus robur* — ordres de grandeur, à préciser.",
 "**(1)** Production de glands d'un chêne adulte : ONF, *Rendez-vous techniques* n° 13, 2006 (fructification des chênes) ; Crawley M.J., Long C.R., 1995, *Alternate bearing, predator satiation and seedling recruitment in Quercus robur L.*, Journal of Ecology 83 : 683-696 — quinze ans de comptages sur trente pédonculés du sud de l'Angleterre, récoltes variant de plus de cent fois d'une année à l'autre, avec une synchronie marquée entre arbres ; les « dizaines de milliers » et le « presque rien » sont des ordres de grandeur, l'arbre, l'année et la station faisant tout varier.")
s = rep(s,
 "**(2)** Synchronisation de la fructification et hypothèse de la satiété des prédateurs : *Flore forestière française*, t. 1, et littérature sur le *masting* — à préciser (ex. Kelly D., Sork V.L., 2002, Annual Review of Ecology and Systematics 33).",
 "**(2)** Synchronisation de la fructification et hypothèse de la satiété des prédateurs : Kelly D., Sork V.L., 2002, *Mast seeding in perennial plants: why, how, where?*, Annual Review of Ecology and Systematics 33 : 427-447 ; Crawley & Long 1995 (ci-dessus) : chez le pédonculé, les petites récoltes perdent aux insectes une part plus forte de leurs glands que les grandes, ce qui va dans le sens de la satiété, sans permettre de trancher entre stratégie évoluée et simple contrainte de ressources ; *Flore forestière française*, t. 1.")

# p. 22 — marcescence
s = rep(s,
 "**(2)** Marcescence : hypothèses discutées — à préciser.",
 "**(2)** Marcescence : trois hypothèses discutées, aucune tranchée. Protection contre les dents : Svendsen C.R., 2001, *Effects of marcescent leaves on winter browsing by large herbivores in northern temperate deciduous forests*, Alces 37 : 475-482 — en février, les cerfs ont moins brouté le hêtre et le charme feuillés que défeuillés, mais le chêne autant dans les deux cas. Recyclage des éléments minéraux au printemps : Otto C., Nilsson L.M., 1981, *Why do beech and oak trees retain leaves until spring?*, Oikos 37 : 387-390 — non confirmé chez un chêne espagnol par Abadía A. et al., 1996, *Marcescence and senescence in a submediterranean oak*, Plant, Cell & Environment 19 : 685-694, qui y voient plutôt une photosynthèse prolongée en arrière-saison. La marcescence est plus fréquente sur les jeunes arbres et les branches basses.")

# p. 24 — lichens
s = rep(s,
 "**(1)** Lichens corticoles comme indicateurs de la qualité de l'air : méthode de l'indice de pureté atmosphérique — à préciser (ex. Van Haluwyn C., Lerond M., 1993, *Guide des lichens*).",
 "**(1)** Lichens corticoles comme indicateurs de la qualité de l'air : LeBlanc F., De Sloover J., 1970, *Relation between industrialization and the distribution and growth of epiphytic lichens and mosses in Montreal*, Canadian Journal of Botany 48 : 1485-1496 (indice de pureté atmosphérique) ; Van Haluwyn C., Lerond M., 1993, *Guide des lichens*, Lechevalier ; AFNOR, norme NF X43-903 (2008), *Biosurveillance de l'environnement — détermination d'un indice biologique de lichens épiphytes*.")

# p. 26 — caches
s = rep(s,
 "**(1)** Mémoire spatiale et récupération des caches : Bossema I., 1979 ; études comparées sur les corvidés — à préciser.",
 "**(1)** Mémoire spatiale et récupération des caches : Bossema I., 1979, Behaviour 70 (repères visuels, récupération plusieurs mois après) ; chez d'autres corvidés cacheurs : Balda R.P., Kamil A.C., 1992, *Long-term spatial memory in Clark's nutcracker*, Animal Behaviour 44 : 761-769 (caches retrouvées après neuf mois) ; Clayton N.S., Dickinson A., 1998, *Episodic-like memory during cache recovery by scrub jays*, Nature 395 : 272-274.")

# en-tête et annexe
s = rep(s,
 " Les notes marquées « à préciser » attendent une page ou un chiffre exact ; les sources principales sont établies.*",
 " Toutes les notes sont sourcées (passe de sourçage du 9 novembre 2026).*")
s = rep(s,
 "- Références primaires à préciser : anthocyanes (Lee & Gould 2002), cycle des cynips (Stone et al. 2002), encre ferro-gallique (BnF), balanin (Bonal), *masting* (Kelly & Sork 2002), marcescence, lichens bio-indicateurs, nourrissage des mésanges (source primaire derrière les « 900 becquées »).",
 "- Références primaires : levées le 9 novembre 2026 (anthocyanes : Lee & Gould 2002, Karageorgou & Manetas 2006 ; cynips : Stone et al. 2002 ; encre : Rouchon 2011, Liège 2012 ; balanin : Espelta 2009, Bonal 2007, 2009 ; glandée : Crawley & Long 1995, Kelly & Sork 2002 ; marcescence : Svendsen 2001, Otto & Nilsson 1981, Abadía 1996 ; lichens : LeBlanc & De Sloover 1970, AFNOR 2008 ; mésanges : Gibb 1955, Royama 1966, Barba 2009 ; caches : Balda & Kamil 1992, Clayton & Dickinson 1998). La phrase sur les feuilles rouges (p. 9) a été réécrite : l'effet parasol est une hypothèse peu confirmée, l'effet contre les insectes est mesuré.")
save(L1, s)

# ---------------------------------------------------------------- livraison 2
L2 = "livraison-2-p28-45.md"
s = load(L2)

# p. 28 — composition
s = rep(s,
 "**(1)** Dimensions et poids des glands : *Flore forestière française*, t. 1 ; composition (amidon, lipides, protéines, tanins) : ordres de grandeur de la littérature sur les glands de chênes blancs européens — à préciser (ex. travaux de l'INRAE sur la conservation des glands ; analyses alimentaires des glands).",
 "**(1)** Dimensions et poids des glands : *Flore forestière française*, t. 1. Composition — amidon autour de la moitié du poids sec, protéines et lipides de quelques pour cent chacun chez les chênes blancs, tanins variables selon l'espèce et la maturité : Vinha A.F., Barreira J.C.M., Costa A.S.G., Oliveira M.B.P.P., 2016, *A new age for Quercus spp. fruits: review on nutritional and phytochemical composition and related biological activities of acorns*, Comprehensive Reviews in Food Science and Food Safety 15 : 947-981 ; Suszka B., Muller C., Bonnet-Masimbert M., 1994, *Graines des feuillus forestiers : de la récolte au semis*, INRA Éditions.")

# p. 29 — dessiccation (corps + note), café, bovins
s = rep(s,
 "Il est gorgé d'eau — près de la moitié de son poids — et qu'il en perde une part, un quart suffit, il meurt (1).",
 "Il est gorgé d'eau — près de la moitié de son poids — et qu'il en perde une part, un cinquième suffit, il meurt (1).")
s = rep(s,
 "**(1)** Graines récalcitrantes, sensibles à la dessiccation : *Flore forestière française*, t. 1 ; ONF, *Rendez-vous techniques* n° 13, 2006 ; seuil de teneur en eau — ordre de grandeur, à préciser.",
 "**(1)** Graines récalcitrantes : Finch-Savage W.E., 1992, *Embryo water status and survival in the recalcitrant species Quercus robur L.: evidence for a critical moisture content*, Journal of Experimental Botany 43 : 663-669 — le gland mûr contient 45 à 50 % d'eau ; la viabilité chute dès que la teneur passe sous 40 % environ, seuil critique retenu par les pépinières (Suszka, Muller & Bonnet-Masimbert 1994 ; ONF, *Rendez-vous techniques* n° 13, 2006) ; *Flore forestière française*, t. 1.")
s = rep(s,
 "**(2)** Consommation humaine des glands (lessivage des tanins, farine, succédané de café) : Couplan F., *Le régal végétal* ; témoignages des deux guerres mondiales sur les ersatz de café — à préciser par une source historique.",
 "**(2)** Consommation humaine des glands (lessivage des tanins, farine, succédané de café) : Couplan F., *Le régal végétal* ; Vinha et al. 2016 (ci-dessus). Succédanés de café — glands, orge, figues, chicorée — plus courants que le vrai café jusqu'à la Seconde Guerre mondiale : *Dictionnaire historique de la Suisse*, art. « Café » ; en France sous l'Occupation, glands et céréales torréfiés à la maison faute de café : Veillon D., 1995, *Vivre et survivre en France, 1939-1947*, Payot.")
s = rep(s,
 "**(3)** Intoxication des bovins et des chevaux par les glands (tanins) : littérature vétérinaire — à préciser (ex. fiches du Centre national d'informations toxicologiques vétérinaires).",
 "**(3)** Intoxication des bovins et des chevaux par les glands — tanins hydrolysables, glands verts les plus toxiques, pédonculé plus que sessile, atteinte digestive puis rénale, accoutumance de certains animaux : GDS Creuse (Boubet B.), *L'intoxication aux glands, une pathologie souvent mortelle chez les bovins*, 2020 et 2025, d'après le Centre national d'informations toxicologiques vétérinaires (CNITV, VetAgro Sup, Lyon) : la moitié des appels pour intoxication végétale des bovins, quatrième motif d'appel pour les équidés.")

# p. 31 — mulot, plantule
s = rep(s,
 "**(1)** Mise en réserve des glands par les rongeurs forestiers (mulots *Apodemus*) et distances de transport : *Flore forestière française*, t. 1 ; den Ouden J., Jansen P.A., Smit R., 2005, dans Forget P.-M. et al. (dir.), *Seed Fate*, CABI — à préciser.",
 "**(1)** Mise en réserve des glands par les mulots (*Apodemus sylvaticus*) et distances de transport, quelques dizaines de mètres, sous couvert : den Ouden J., Jansen P.A., Smit R., 2005, *Jays, mice and oaks: predation and dispersal of Quercus robur and Q. petraea in north-western Europe*, dans Forget P.-M., Lambert J.E., Hulme P.E., Vander Wall S.B. (dir.), *Seed Fate: Predation, Dispersal and Seedling Establishment*, CABI, p. 223-239 ; *Flore forestière française*, t. 1.")
s = rep(s,
 "**(1)** Germination hypogée et croissance de la plantule la première année : *Flore forestière française*, t. 1 ; proportion racine/tige au premier été — ordre de grandeur des pépinières forestières, à préciser selon la station.",
 "**(1)** Germination hypogée et croissance de la plantule la première année : *Flore forestière française*, t. 1 ; Harmer R., 1990, *Relation of shoot growth phases in seedling oak to development of the tap root, lateral roots and fine root tips*, New Phytologist 115 : 23-27 (le pivot pousse avant et entre les poussées de la tige) ; *La Hulotte*, *Plantez un chêne*, 2024 (20 à 40 cm de tige, près d'un mètre de racine au premier été) ; les proportions varient avec le sol, l'ombre et l'eau.")

# p. 32 — ronce
s = rep(s,
 "**(3)** Effet protecteur des ronciers contre l'abroutissement des semis de chêne : études de régénération en forêt feuillue — à préciser (ONF, INRAE).",
 "**(3)** Effet protecteur des buissons et des ronces contre l'abroutissement des semis de chêne : Jensen A.M., Götmark F., Löf M., 2012, *Shrubs protect oak seedlings against ungulate browsing in temperate broadleaved forests of conservation interest: a field experiment*, Forest Ecology and Management 266 : 187-193 — dix forêts du sud de la Suède : moins de dégâts de dents sous les buissons, mais plus de mortalité au bout de deux ans et demi, car ce qui protège fait aussi de l'ombre ; Smit C., den Ouden J., Müller-Schärer H., 2006, *Unpalatable plants facilitate tree sapling survival in wooded pastures*, Journal of Applied Ecology 43 : 305-312.")

# p. 33 — première fructification
s = rep(s,
 "arbres isolés plus précoces : *Flore forestière française*, t. 1 — à préciser.",
 "arbres isolés plus précoces, vers 20 à 30 ans : *Flore forestière française*, t. 1 ; les trente pédonculés suivis quinze ans par Crawley & Long (1995, Journal of Ecology 83) pour leurs glands allaient de 43 cm à plus de 6 m de tour.")

# p. 34 — Tronçais
s = rep(s,
 "— ONF, forêt domaniale de Tronçais ; à préciser (dates et sources d'archives).",
 "— ordonnance de Colbert sur le fait des eaux et forêts (août 1669) et réformation de la forêt de Tronçais (1670) pour la marine ; ONF, forêt domaniale de Tronçais, Forêt d'Exception® (2018) ; Corvol A., 1987, *L'Homme aux bois. Histoire des relations de l'homme et de la forêt, XVIIe-XXe siècle*, Fayard.")

# p. 35 — truffe
s = rep(s,
 "hôtes de la truffe noire *Tuber melanosporum* (chênes pubescent et vert, sols calcaires) : INRAE, filière trufficole — à préciser.",
 "hôtes de la truffe noire *Tuber melanosporum* (chênes pubescent et vert, noisetier, sols calcaires) : Le Tacon F., 2017, *Les truffes. Biologie, écologie et domestication*, AgroParisTech, Nancy, 304 p.")

# p. 37 — descente de cime
s = rep(s,
 "**(1)** Descente de cime et sénescence des chênes : Drénou C., *Les racines, face cachée des arbres* et *L'arbre : au-delà des idées reçues*, IDF — à préciser (chapitres) ; Raimbault P., modèles architecturaux des arbres.",
 "**(1)** Descente de cime et sénescence des chênes : Raimbault P., Tanguy M., 1993, *La gestion des arbres d'ornement. 1re partie : une méthode d'analyse et de diagnostic de la partie aérienne*, Revue forestière française 45 (2) : 97-117 — dix stades de développement, le neuvième étant la descente de cime, le dixième la dislocation ; Drénou C., Bouvier M., Lemaire J., 2011 et 2012 (méthode ARCHI, voir page 44) ; Drénou C., 2016, *L'arbre : au-delà des idées reçues*, IDF.")

# p. 39 — bois mort
s = rep(s,
 "**(1)** Décomposition du bois mort de chêne et succession des organismes : Vallauri D. et al., 2005, *Bois mort et à cavités* ; durées — ordres de grandeur, à préciser.",
 "**(1)** Décomposition du bois mort de chêne et succession des organismes : Vallauri D. et al., 2005, *Bois mort et à cavités* ; durées : Rock J., Badeck F.-W., Harmon M.E., 2008, *Estimating decomposition rate constants for European tree species from literature sources*, European Journal of Forest Research 127 : 301-313 — le chêne a l'une des constantes de décomposition les plus faibles des feuillus européens : plusieurs décennies pour perdre la moitié de sa masse, un siècle et plus pour un gros tronc.")

# p. 41 — coucou
s = rep(s,
 "régime du coucou gris (chenilles velues) : LPO, fiche *Cuculus canorus* — à préciser.",
 "régime du coucou gris — les chenilles velues qu'aucun autre oiseau ne mange, processionnaires comprises : Barbaro L., Battisti A., 2011, *Birds as predators of the pine processionary moth*, Biological Control 56 : 107-114 (coucou gris et coucou geai, prédateurs réguliers grâce à la paroi de leur gésier) ; Cramp S. (dir.), 1985, *The Birds of the Western Palearctic*, vol. IV, Oxford University Press.")

# annexe
s = rep(s,
 "- Composition du gland (amidon, lipides, protéines, tanins) et seuil de dessiccation : une source quantitative (INRAE, littérature sur les graines récalcitrantes).\n- Sources historiques du « café de glands » et du pain de glands (deux guerres, famines) ; intoxication des bovins et chevaux (CNITV).\n- Croissance des semis selon la station (hauteur et racine au premier été) ; effet protecteur de la ronce (ONF, INRAE).\n- Descente de cime : chapitres précis de Drénou ; durées de décomposition du bois mort de chêne.\n- Chênes remarquables : âges mesurés ou estimés, sources (A.R.B.R.E.S., ONF Tronçais), et le chêne lorrain de la page 58 — à visiter.\n",
 "- Sources levées le 9 novembre 2026 : composition du gland (Vinha 2016 ; Suszka 1994) et seuil de dessiccation (Finch-Savage 1992 : « un cinquième » remplace « un quart ») ; café de glands (DHS ; Veillon 1995) ; bovins (GDS Creuse d'après le CNITV) ; mulot (den Ouden 2005) ; plantule (Harmer 1990 ; La Hulotte 2024) ; ronce (Jensen 2012 ; Smit 2006) ; Tronçais (Colbert 1669-1670 ; Corvol 1987) ; truffe (Le Tacon 2017) ; descente de cime (Raimbault & Tanguy 1993) ; bois mort (Rock 2008) ; coucou (Barbaro & Battisti 2011 ; Cramp 1985).\n- Chênes remarquables : traités page 58 (livraison 4) ; le chêne lorrain est celui de l'Attaque, à Montmédy.\n")
s = rep(s,
 "- Régime du coucou gris (chenilles velues, processionnaires) : fiche LPO ou source ornithologique.\n", "")
save(L2, s)

# ---------------------------------------------------------------- livraison 4
L4 = "livraison-4-p54-64.md"
s = load(L4)
s = rep(s,
 "Les mentions « à préciser » qui subsistent dans les notes des pages 1 à 53 sont levées ou signalées ici ; rien de ce qui porte un chiffre dans ce livre n'a été écrit sans source.",
 "Les notes des pages 1 à 53 ont toutes été levées ; rien de ce qui porte un chiffre dans ce livre n'a été écrit sans source.")

# bibliographie : insertions alphabétiques
ins = {
 "Antonelli M., Barbieri G., Donelli D., 2019,":
   "Abadía A., Gil E., Morales F., Montañés L., Montserrat G., Abadía J., 1996, *Marcescence and senescence in a submediterranean oak (Quercus subpyrenaica)*, Plant, Cell & Environment 19 : 685-694. — AFNOR, 2008, norme NF X43-903, *Biosurveillance de l'environnement — détermination d'un indice biologique de lichens épiphytes*. — Antonelli M., Barbieri G., Donelli D., 2019,",
 "Bartholomé J., Brachi B.,":
   "Balda R.P., Kamil A.C., 1992, *Long-term spatial memory in Clark's nutcracker*, Animal Behaviour 44 : 761-769. — Barba E., Atiénzar F., Marín M., Monrós J.S., Gil-Delgado J.A., 2009, *Patterns of nestling provisioning by a single-prey loader bird, great tit Parus major*, Bird Study 56 : 187-197. — Barbaro L., Battisti A., 2011, *Birds as predators of the pine processionary moth*, Biological Control 56 : 107-114. — Bartholomé J., Brachi B.,",
 "Bonal R. et al., travaux sur *Curculio* et la prédation des glands (à préciser) ; Bonnet-Masimbert M., 1984,":
   "Bonal R., Muñoz A., Díaz M., 2007, *Satiation of predispersal seed predators: the importance of considering both plant and seed levels*, Evolutionary Ecology 21 : 367-380 ; Bonal R., Muñoz A., 2009, *Seed weevils living on the edge*, Ecological Entomology 34 : 304-309 ; Bonnet-Masimbert M., 1984,",
 "Clark J.S. et al., 1998,":
   "Clayton N.S., Dickinson A., 1998, *Episodic-like memory during cache recovery by scrub jays*, Nature 395 : 272-274. — Corvol A., 1987, *L'Homme aux bois. Histoire des relations de l'homme et de la forêt, XVIIe-XXe siècle*, Fayard. — Crawley M.J., Long C.R., 1995, *Alternate bearing, predator satiation and seedling recruitment in Quercus robur L.*, Journal of Ecology 83 : 683-696. — Clark J.S. et al., 1998,",
 "den Ouden J., Jansen P.A., Smit R., 2005, dans Forget P.-M. et al. (dir.), *Seed Fate*, CABI (mise en réserve des glands par les rongeurs).":
   "den Ouden J., Jansen P.A., Smit R., 2005, *Jays, mice and oaks: predation and dispersal of Quercus robur and Q. petraea in north-western Europe*, dans Forget P.-M., Lambert J.E., Hulme P.E., Vander Wall S.B. (dir.), *Seed Fate: Predation, Dispersal and Seedling Establishment*, CABI, p. 223-239.",
 "Epaud F., 2019,":
   "Espelta J.M., Bonal R., Sánchez-Humanes B., 2009, *Pre-dispersal acorn predation in mixed oak forests: interspecific differences are driven by the interplay among seed phenology, seed size and predator size*, Journal of Ecology 97 : 1416-1423. — Finch-Savage W.E., 1992, *Embryo water status and survival in the recalcitrant species Quercus robur L.: evidence for a critical moisture content*, Journal of Experimental Botany 43 : 663-669. — Epaud F., 2019,",
 "Géroudet P., 1998,":
   "Gibb J.A., 1955, *Feeding rates of great tits*, British Birds 48 : 49-58. — Géroudet P., 1998,",
 "Jactel H., Brockerhoff E.G., 2007,":
   "Harmer R., 1990, *Relation of shoot growth phases in seedling oak to development of the tap root, lateral roots and fine root tips*, New Phytologist 115 : 23-27. — Jensen A.M., Götmark F., Löf M., 2012, *Shrubs protect oak seedlings against ungulate browsing in temperate broadleaved forests of conservation interest: a field experiment*, Forest Ecology and Management 266 : 187-193. — Jactel H., Brockerhoff E.G., 2007,",
 "Karst J., Jones M.D., Hoeksema J.D., 2023,":
   "Karageorgou P., Manetas Y., 2006, *The importance of being red when young: anthocyanins and the protection of young leaves of Quercus coccifera from insect herbivory and excess light*, Tree Physiology 26 : 613-621. — Karst J., Jones M.D., Hoeksema J.D., 2023,",
 "Lebourgeois F., 2001,":
   "LeBlanc F., De Sloover J., 1970, *Relation between industrialization and the distribution and growth of epiphytic lichens and mosses in Montreal*, Canadian Journal of Botany 48 : 1485-1496. — Le Tacon F., 2017, *Les truffes. Biologie, écologie et domestication*, AgroParisTech, Nancy, 304 p. — Lebourgeois F., 2001,",
 "Lee D.W., Gould K.S., 2002, *Anthocyanins in leaves and other vegetative organs*, Advances in Botanical Research 37.":
   "Lee D.W., Gould K.S., 2002, *Anthocyanins in leaves and other vegetative organs: an introduction*, Advances in Botanical Research 37 : 1-16.",
 "Pastoureau M., 2011,":
   "Otto C., Nilsson L.M., 1981, *Why do beech and oak trees retain leaves until spring?*, Oikos 37 : 387-390. — Pastoureau M., 2011,",
 "Reed T.E., Grøtan V.,":
   "Raimbault P., Tanguy M., 1993, *La gestion des arbres d'ornement. 1re partie : une méthode d'analyse et de diagnostic de la partie aérienne*, Revue forestière française 45 (2) : 97-117. — Reed T.E., Grøtan V.,",
 "Roman L.A., Scatena F.N., 2011,":
   "Rock J., Badeck F.-W., Harmon M.E., 2008, *Estimating decomposition rate constants for European tree species from literature sources*, European Journal of Forest Research 127 : 301-313. — Roman L.A., Scatena F.N., 2011,",
 "Sáenz-Romero C. et al., 2017,":
   "Royama T., 1966, *Factors governing feeding rate, food requirement and brood size of nestling great tits, Parus major*, Ibis 108 : 313-347. — Sáenz-Romero C. et al., 2017,",
 "Stone G.N. et al., 2002,":
   "Smit C., den Ouden J., Müller-Schärer H., 2006, *Unpalatable plants facilitate tree sapling survival in wooded pastures*, Journal of Applied Ecology 43 : 305-312. — Stone G.N. et al., 2002,",
 "Terhürne-Berson R., Litt T., Cheddadi R., 2004,":
   "Suszka B., Muller C., Bonnet-Masimbert M., 1994, *Graines des feuillus forestiers : de la récolte au semis*, INRA Éditions. — Svendsen C.R., 2001, *Effects of marcescent leaves on winter browsing by large herbivores in northern temperate deciduous forests*, Alces 37 : 475-482. — Terhürne-Berson R., Litt T., Cheddadi R., 2004,",
 "Van Haluwyn C., Lerond M., 1993,":
   "Veillon D., 1995, *Vivre et survivre en France, 1939-1947*, Payot. — Vinha A.F., Barreira J.C.M., Costa A.S.G., Oliveira M.B.P.P., 2016, *A new age for Quercus spp. fruits: review on nutritional and phytochemical composition and related biological activities of acorns*, Comprehensive Reviews in Food Science and Food Safety 15 : 947-981. — Van Haluwyn C., Lerond M., 1993,",
}
for old, new in ins.items():
    s = rep(s, old, new)
# institutions : GDS Creuse / CNITV, Cramp
s = rep(s,
 "— *La Hulotte*, notice *Plantez un chêne*, 2024.",
 "— GDS Creuse (Boubet B.), *L'intoxication aux glands, une pathologie souvent mortelle chez les bovins*, 2020 et 2025, d'après le Centre national d'informations toxicologiques vétérinaires (CNITV, VetAgro Sup, Lyon). — Cramp S. (dir.), 1985, *The Birds of the Western Palearctic*, vol. IV, Oxford University Press. — *La Hulotte*, notice *Plantez un chêne*, 2024.")
s = rep(s,
 "*Dictionnaire historique de la Suisse*, art. « Glandage, glandée ».",
 "*Dictionnaire historique de la Suisse*, art. « Glandage, glandée » et « Café ».")
# annexe de la livraison 4
s = rep(s,
 "- Les sources encore « à préciser » des livraisons 1 et 2 : composition du gland et seuil de dessiccation ; café et pain de glands ; intoxication des bovins ; croissance des semis selon la station ; protection par la ronce ; marcescence ; lichens bio-indicateurs ; les « 900 becquées » des mésanges ; régime du coucou.\n", "")
s = rep(s,
 "les mentions « à préciser » encore ouvertes dans les notes des pages 1 à 53 (composition du gland, seuil de dessiccation, marcescence, lichens, nourrissage des mésanges, protection par la ronce) sont listées ci-dessous et non levées.",
 "les mentions « à préciser » des notes des pages 1 à 53 ont été levées le 9 novembre au soir (vingt références ajoutées à la bibliographie ; deux phrases du corps de texte ajustées en conséquence : les feuilles rouges de la page 9, le seuil d'eau du gland page 29).")
save(L4, s)
print("sourçage : OK")
