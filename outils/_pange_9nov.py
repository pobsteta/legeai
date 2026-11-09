# -*- coding: utf-8 -*-
"""9 novembre 2026, soir : l'individu suivi est un chêne du parc du château de Pange (Moselle),
au bord de la Nied française. Remplace les crochets [lieu] et réécrit le décor de haie de plaine
(pré, mare, saule, village) en décor de parc, d'après les documents publics sur le domaine :
château de 1720 (Jean-Baptiste Thomas, marquis de Pange), douves comblées et tours démolies en 1806,
parc à l'anglaise du XIXe siècle (plans du comte de Choulot), occupations militaires successives,
jardin de Louis Benech (2000-2003, label Jardin remarquable), parc romantique « aux chênes
tricentenaires », saules au bord de la Nied, domaine agricole et forestier de 300 ha.
Ce qui dépend de l'arbre lui-même (position, tour, âge) reste entre crochets.
Script à usage unique, conservé pour mémoire ; chaque remplacement est vérifié (assert)."""

REP = "/home/claude/legeai/tomes/01-le-chene/texte/"

def load(n): return open(REP + n, encoding="utf-8").read()
def save(n, s): open(REP + n, "w", encoding="utf-8").write(s)
def rep(s, old, new, count=1):
    assert old in s, "introuvable : " + old[:100]
    return s.replace(old, new, count)

# ---------------------------------------------------------------- livraison 1
L1 = "livraison-1-p01-27.md"; s = load(L1)
s = rep(s, "suit un seul chêne, le même du printemps à l'hiver, dans une haie de [lieu].",
           "suit un seul chêne, le même du printemps à l'hiver, dans le parc du château de Pange, en Moselle, au bord de la Nied.")
s = rep(s, "Il fait à peine jour. La brume traîne sur le pré, et le chêne du bout, celui de la mare, n'a plus que la moitié de ses feuilles.",
           "Il fait à peine jour. La brume traîne sur la Nied, et le grand chêne du parc n'a plus que la moitié de ses feuilles.")
s = rep(s, "Trois cents mètres. Le pré, la route, la friche aux ronces.",
           "Trois cents mètres. La rivière, la route, la friche aux ronces.")
s = rep(s, "Le point : [lieu de l'individu suivi].",
           "Le point : Pange (Moselle), où pousse l'individu suivi.")
s = rep(s, "*Le pré a reverdi, la haie aussi, et le saule de la mare s'est couvert le premier de son feuillage d'argent. Seul le chêne attend. Il attend sur une lisière qui n'a pas bougé : la haie où il pousse est déjà tracée sur la carte de Cassini, dressée sous Louis XV, et le chemin d'où vous le regardez figure au vieux cadastre, celui des géomètres de l'Empire. Le village a changé de clocher, de route et de maîtres ; la haie, non. Elle a laissé passer des générations de gelées. Elle peut bien attendre celle-ci.*",
           "*La prairie a reverdi, les saules de la rivière se sont couverts les premiers de leur feuillage d'argent, et le jardin, en bas, a ses premières fleurs. Seul le chêne attend. Il attend à une place qui n'a pas bougé : le domaine est déjà dessiné sur la carte de Cassini, dressée sous Louis XV, et le parc où il pousse figure sur les plans du siècle suivant, quand on le voulut à l'anglaise. Le château a perdu ses douves et ses tours, a vu passer des armées, des cosaques aux Américains, a été vidé puis rendu à ses maîtres ; le chêne, non. Il a laissé passer des générations de gelées. Il peut bien attendre celle-ci.*")
s = rep(s, "Fin avril. Le saule est en feuilles depuis trois semaines ; le chêne n'a pas une feuille.",
           "Fin avril. Les saules de la Nied sont en feuilles depuis trois semaines ; le chêne n'a pas une feuille.")
s = rep(s, "Regardez-le depuis le chemin : un squelette gris",
           "Regardez-le depuis l'allée : un squelette gris")
s = rep(s, "**[Légende]** Notre chêne, le [25 avril], depuis le chemin. Le saule, à gauche, est en feuilles depuis le [3 avril]. Même point de vue à chaque saison.",
           "**[Légende]** Notre chêne, le [25 avril], depuis l'allée du parc. Les saules de la Nied, au bord de l'eau, sont en feuilles depuis le [3 avril]. Même point de vue à chaque saison.")
s = rep(s, "*Levez la tête. En juillet, sous le chêne, il fait plus frais qu'au pré, et il y a plus de bruit",
           "*Levez la tête. En juillet, sous le chêne, il fait plus frais que sur la pelouse en plein soleil, et il y a plus de bruit")
s = rep(s, "ses habitants de passage et ses familles installées depuis des générations — bien avant que le village ne compte ses maisons. On l'habitait déjà quand les premiers chemins y menaient les troupeaux ; on l'habite encore, sans permis ni cadastre.*",
           "ses habitants de passage et ses familles installées depuis des générations — bien avant que le jardin d'en bas ne soit dessiné. On l'habitait déjà quand le parc était à l'anglaise ; on l'habite encore, sans permis ni cadastre.*")
s = rep(s, "Et dans le fourré, de l'autre côté de la haie, les sangliers attendent.",
           "Et dans les bois du domaine, pas loin, les sangliers attendent.")
s = rep(s, "Dans la haie, un oiseau criard commence à faire des réserves.",
           "Dans le parc, un oiseau criard commence à faire des réserves.")
s = rep(s, "*Octobre. Sous le chêne, le sol craque à chaque pas, et la haie sent la feuille mouillée et le champignon. Le mot est ancien et le village l'a connu avant d'avoir un nom pour la rue : la glandée. On y menait les cochons, en automne, par le droit qu'avaient les habitants de ramasser ce que l'arbre donnait, et les registres de la seigneurie en gardent la trace, comme les sentiers que l'on prend encore sans savoir pourquoi ils passent là. Les cochons ne viennent plus. Les sangliers, si.*",
           "*Octobre. Sous le chêne, le sol craque à chaque pas, et le parc sent la feuille mouillée et le champignon. Le mot est ancien et la seigneurie l'a connu avant d'avoir un château de pierre : la glandée. On menait les cochons sous les chênes, en automne, par le droit qu'avaient les habitants de ramasser ce que l'arbre donnait, et les registres des seigneurs de Pange en gardent la trace [à vérifier aux archives], comme les allées que l'on prend encore sans savoir pourquoi elles passent là. Les cochons ne viennent plus. Les sangliers, si.*")
s = rep(s, "Regardez la haie en octobre, vers huit heures du matin.",
           "Regardez le parc en octobre, vers huit heures du matin.")
s = rep(s, "Elles tombent tard, parmi les dernières de la haie.",
           "Elles tombent tard, parmi les dernières du parc.")
s = rep(s, "dans la friche où le Jacques est venu trois cents fois, dans la mousse du talus, au pied du grillage du pré,",
           "dans la friche où le Jacques est venu trois cents fois, dans la mousse de la berge, au pied de la clôture de la prairie,")
s = rep(s, "*Janvier. Le chêne est nu sur un ciel blanc, et c'est maintenant qu'on le reconnaît le mieux : la même silhouette que sur la photographie du village d'avant la guerre, celle où l'on voit la haie, le toit de la ferme et un homme en blouse qui regarde ailleurs. Les branches ont changé — l'une est tombée, deux ont poussé — mais le dessin est le même, tortueux, large, planté. Le photographe est mort, la ferme a changé trois fois de main, et l'arbre a gardé la pose.*",
           "*Janvier. Le chêne est nu sur un ciel blanc, et c'est maintenant qu'on le reconnaît le mieux : la même silhouette que sur la carte postale du château d'avant la Grande Guerre, celle où l'on voit la Nied, la façade et les arbres du parc [à vérifier sur la carte postale]. Les branches ont changé — l'une est tombée, deux ont poussé — mais le dessin est le même, tortueux, large, planté. Le photographe est mort, le château a été occupé, vidé, rendu, restauré, et l'arbre a gardé la pose.*")
s = rep(s, "[Vignette : la photographie ancienne du village, redessinée, si elle existe.]",
           "[Vignette : la carte postale ancienne du château et du parc, redessinée, si l'arbre y figure.]")
s = rep(s, "Sur le chemin, les cupules de l'automne sont noires et molles.",
           "Sur l'allée, les cupules de l'automne sont noires et molles.")
s = rep(s, "- La photographie ancienne du village pour le regard de la page 23 ; la carte de Cassini et le cadastre napoléonien pour le regard de la page 8 ; les archives seigneuriales ou communales pour la glandée de la page 18.",
           "- Le lieu est fixé (9 novembre) : le parc du château de Pange, Moselle, au bord de la Nied française ; les regards des pages 8, 11, 18 et 23 ont été réécrits pour ce décor d'après les documents publics sur le domaine (château de 1720, douves et tours supprimées en 1806, parc à l'anglaise du XIXe siècle, occupations militaires, jardin de Louis Benech 2000-2003, « chênes tricentenaires »). Restent à l'auteur : la carte postale ancienne du château pour le regard de la page 23 ; la feuille de Cassini et les plans du parc (XVIIIe siècle, comte de Choulot) pour la page 8 ; les archives de la seigneurie pour la glandée de la page 18 ; la position exacte du chêne dans le parc, son tour et son âge (page 34).")
save(L1, s)

# ---------------------------------------------------------------- livraison 2
L2 = "livraison-2-p28-45.md"; s = load(L2)
s = rep(s, "Les trois distances à l'échelle du village de [lieu] :", "Les trois distances à l'échelle de Pange :")
s = rep(s, "Le clocher, pour l'échelle.", "Le château et le clocher, pour l'échelle.")
s = rep(s, "Le nôtre a quatre-vingts ans. Un mètre quatre-vingts de tour à hauteur de poitrine, vingt-deux mètres de haut [à mesurer], des branches maîtresses qui partent à trois mètres du sol parce qu'il a toujours eu le pré d'un côté. Dans la forêt voisine,",
           "Le nôtre : [tour à 1,30 m, hauteur et âge à mesurer dans le parc de Pange — les chênes du parc sont dits tricentenaires ; le tour permettra d'en juger, page 54]. Un chêne de parc de quatre-vingts ans, lui, fait un mètre quatre-vingts de tour à hauteur de poitrine et une vingtaine de mètres de haut, avec des branches maîtresses qui partent à trois mètres du sol parce qu'il a toujours eu la lumière d'un côté. Dans la forêt voisine,")
s = rep(s, "posée sur la plus haute branche morte, qui surveille le pré.", "posée sur la plus haute branche morte, qui surveille la prairie.")
s = rep(s, "Tous ces habitants sont présents en juillet sur un chêne de haie de plaine ;", "Tous ces habitants sont présents en juillet sur un chêne de parc ou de haie, en plaine ;")
s = rep(s, "« Je suis au troisième. Avec vue sur la friche. »", "« Je suis au troisième. Avec vue sur la Nied. »")
s = rep(s, "vérifier la présence de chacun sur le chêne suivi ou dans sa haie, en juillet", "vérifier la présence de chacun sur le chêne suivi ou dans le parc de Pange, en juillet")
save(L2, s)

# ---------------------------------------------------------------- livraison 3
L3 = "livraison-3-p46-53.md"; s = load(L3)
s = rep(s, "*Posez le doigt sur [lieu], tout en haut de la carte.", "*Posez le doigt sur Pange, tout en haut de la carte.")
s = rep(s, "Le cercle rouge : [lieu].", "Le cercle rouge : Pange.", count=2)
s = rep(s, "*[Sur la photographie ancienne de lieu : la rue, les maisons, et ce qu'on y voit de chêne — les poutres, un portail, les piquets d'une clôture. À écrire devant l'image, une fois fournie.] Regardez bien la maison du fond. Tout ce qui, dedans, tient le toit depuis qu'elle existe est sorti d'une forêt qu'on voit au bout de la rue.*",
           "*[Sur la carte postale ancienne du château de Pange : la façade sur la Nied, le pont, les arbres du parc, et ce qu'on y voit de chêne — à écrire devant l'image, une fois fournie.] Regardez bien la toiture. Ce qui la tient, depuis que le château existe, est sorti d'une forêt qu'on voit depuis la terrasse [charpente et provenance du bois à vérifier auprès des propriétaires].*")
s = rep(s, "« Dix sur cent. Dans ma haie, c'est le deuxième à gauche. »", "« Dix sur cent. Dans mon parc, c'est le deuxième à gauche. »")
s = rep(s, "- La photographie ancienne du village (regard de la page 48) et le nom du bois sur la feuille de Cassini (regard de la page 46) — l'auteur.",
           "- La carte postale ancienne du château de Pange (regard de la page 48) et le nom du bois sur la feuille de Cassini (regard de la page 46) — l'auteur. Le lieu est fixé le 9 novembre : parc du château de Pange (Moselle).")
save(L3, s)

# ---------------------------------------------------------------- livraison 4
L4 = "livraison-4-p54-64.md"; s = load(L4)
s = rep(s, "deux imitations enregistrées par l'auteur dans la haie de [lieu] [adresse à fixer].",
           "deux imitations enregistrées par l'auteur dans le parc du château de Pange [adresse à fixer].")
s = rep(s, "le lieu de l'individu suivi en rouge.", "Pange, où pousse l'individu suivi, en rouge.")
save(L4, s)

# ---------------------------------------------------------------- figures
F = "/home/claude/claude/legeai/outils/figures_vectorielles.py".replace("/home/claude/claude/", "/home/claude/")
s = open(F, encoding="utf-8").read()
s = rep(s, 'ax.plot([6.2], [48.7], marker="o", ms=7, color=RED, mec="white", mew=1.2)\n    ax.text(6.2, 48.35, "[lieu de l\'individu suivi]", fontsize=8.5, color=RED, ha="center", va="top")',
           'ax.plot([LIEU[0]], [LIEU[1]], marker="o", ms=7, color=RED, mec="white", mew=1.2)\n    ax.text(LIEU[0], LIEU[1] - 0.3, "Pange (Moselle), l\'individu suivi", fontsize=8.5, color=RED, ha="center", va="top")')
s = rep(s, 'ax.plot([6.2], [48.7], marker="o", ms=9, mfc="none", mec=RED, mew=2)\n    ax.text(7.2, 48.4, "[lieu]", fontsize=9, color=RED)',
           'ax.plot([LIEU[0]], [LIEU[1]], marker="o", ms=9, mfc="none", mec=RED, mew=2)\n    ax.text(7.3, 48.7, "Pange", fontsize=9, color=RED)')
s = rep(s, 'ax.plot([6.2], [48.7], marker="o", ms=8, mfc="none", mec=RED, mew=1.8)\n    ax.text(6.55, 48.7, "[lieu]", fontsize=8.5, color=RED, va="center")',
           'ax.plot([LIEU[0]], [LIEU[1]], marker="o", ms=8, mfc="none", mec=RED, mew=1.8)\n    ax.text(LIEU[0] + 0.35, LIEU[1], "Pange", fontsize=8.5, color=RED, va="center")')
s = rep(s, 'ax.plot([6.2], [48.7], marker="o", ms=9, mfc="none", mec=RED, mew=1.8)\n    ax.text(6.55, 48.7, "[lieu]", fontsize=8.5, color=RED, va="center")',
           'ax.plot([LIEU[0]], [LIEU[1]], marker="o", ms=9, mfc="none", mec=RED, mew=1.8)\n    ax.text(LIEU[0] + 0.35, LIEU[1], "Pange", fontsize=8.5, color=RED, va="center")')
s = rep(s, 'FOND = ', 'LIEU = (6.353896, 49.083583)  # château de Pange (Moselle), géocodeur IGN, objet « château », 9 novembre 2026\nFOND = ')
open(F, "w", encoding="utf-8").write(s)
print("Pange : OK")
