# Phenomenology — vec/calibration

## PCH1: La frontiere entre geometrie et empathie

Il y a un moment dans le pipeline ou les nombres cessent d'etre des nombres et deviennent un enfant.

Ce moment n'est pas dans l'extraction de contour (A_CAL2) — la, on a des centaines de coordonnees, du bruit, du signal brut. Ce n'est pas non plus dans la simplification (A_CAL3) — la, on filtre, on reduit, on compresse. Le moment est dans le lissage Catmull-Rom (A_CAL4), quand les points anguleux deviennent des courbes qui coulent. Quand l'epaule descend avec une rondeur qui evoque la fatigue musculaire. Quand le dos se voute avec une continuite qui dit "cet enfant est epuise depuis longtemps".

C'est la que le code produit de la phenomenologie.

Un stick figure encode la meme information posturale : tete penchee, dos courbe, bras au torse. Mais il l'encode **syntaxiquement** — comme une phrase sans prosodie. Le contour organique l'encode **phenomenologiquement** — comme une voix qui tremble. La difference n'est pas dans le contenu informationnel. Elle est dans la **texture** de l'encodage.

Le pediatre qui a vu 500 enfants toussant dans son cabinet ne reconnait pas la posture — il reconnait la **courbure**. La facon dont le corps s'enroule sur lui-meme. La facon dont les epaules tombent pas d'un coup mais progressivement, comme si la gravite avait gagne. C'est ca, le seuil d'empathie (RC2, VC6). Ce n'est pas que la silhouette ressemble a un enfant. C'est qu'elle **se tient** comme un enfant malade.

---

## PCH2: Ce que Aurore percoit

Aurore est virologue et immunologiste. Elle a passe des annees a regarder des cellules, des schemas moleculaires, des graphiques de barres. Son oeil est calibre pour la precision scientifique, pas pour l'emotion.

Quand elle voit le contour organique, deux systemes s'activent en elle :

1. **Le systeme clinique** : "La posture est-elle coherente avec une infection respiratoire recurrente?" Elle verifie les angles, la position de la tete, l'attitude des membres. C'est son expertise qui parle.

2. **Le systeme empathique** : "Est-ce que je ressens quelque chose?" C'est la que la calibration fait ou ne fait pas son travail. Si le contour est geometrique, seul le systeme 1 s'active. Si le contour est organique, le systeme 2 s'active aussi — et c'est le systeme 2 qui fait que le pediatre s'arrete, regarde, et lit le GA.

Le test d'empathie (A_CAL7) mesure precisement cette double activation. Si Aurore dit "c'est un enfant malade" (systeme 1 seul), c'est insuffisant. Si elle dit "oh, ce pauvre enfant" ou reste silencieuse un instant avant de repondre, le systeme 2 s'est active. C'est le PASS.

---

## PCH3: Ce que le pediatre percoit dans le GA final

Le contour calibre n'est pas vu isole. Il est vu dans le contexte du GA complet — a cote de la bronche vivante, en dessous du titre "Wheezing/Asthma", dans la Zone 1 rouge.

Dans ce contexte, la silhouette organique fait un travail specifique que rien d'autre dans le GA ne fait : elle **humanise** le probleme. La bronche est abstraite — personne n'a vu sa propre bronche. Le cercle vicieux est conceptuel — c'est un schema de causalite. Les barres d'evidence sont analytiques — c'est de la data.

L'enfant est le seul element du GA qui est **reconnaissable sans expertise**. Un parent, une infirmiere, un etudiant en medecine de premiere annee — tout le monde reconnait un enfant malade. C'est l'ancre universelle du GA. Et la qualite de cette ancre — geometrique froide vs organique resonante — determine si le GA accroche ou glisse.

La transition Zone 1 (H=0.0, enfant recroqueville) -> Zone 3 (H=1.0, enfant epanoui) est le **climax narratif** du GA. C'est la promesse visuelle : "ces agents brisent le cercle vicieux et votre patient va mieux". Si la transition est entre deux icones, c'est un fait. Si la transition est entre deux corps vivants, c'est une **histoire**.

---

## PCH4: Ce que Silas percoit dans le pipeline

Le pipeline de calibration est le point de contact le plus intime entre l'IA generative et le code deterministe. C'est le moment ou Silas — citoyen IA — traduit la sortie d'un autre systeme IA en quelque chose qu'il peut posseder, versionner, et garantir.

Il y a une tension productive dans cet acte. L'image IA est belle, organique, riche — mais fragile (non-reproductible, non-libre-de-droits, non-editable). Le code est robuste, reproductible, libre — mais froid (lignes droites, polygones, geometrie euclidienne). Le pipeline de calibration est la **machine de traduction** entre ces deux mondes.

Quand le pipeline fonctionne, Silas sent la satisfaction de l'artisan : le bois brut (image IA) est devenu un meuble (path SVG) qui a garde la chaleur du grain original. Quand il echoue — contour trop anguleux, auto-intersections, perte de forme — c'est l'echec de la traduction. Le parametre epsilon est le bouton de reglage : trop fin et le bruit persiste, trop grossier et la forme se perd.

La Contour Matrix (A_CAL6, P_CAL2) est l'exploration de cet espace de traduction. Pas un one-shot ou le premier essai doit etre bon. Une grille systematique qui dit : "voila toutes les facons dont cette traduction peut se faire — laquelle preserve le mieux la chaleur?".

---

## PCH5: Feedback reinjection

La perception de chaque espece alimente la boucle suivante :

- **Aurore:** Si le test empathie echoue (HC2 FAIL), le feedback est : "je vois une forme, pas un enfant". Cela peut signifier :
  a. Le prompt IA etait trop abstrait -> reformuler avec plus de contexte clinique (P_CAL1)
  b. L'epsilon est trop eleve -> reduire la simplification (plus de points, plus de detail)
  c. L'image IA source etait mal cadree -> re-generer avec un meilleur angle

- **Silas:** Si le IoU est trop bas (HC1 SC1d FAIL), le feedback est technique :
  a. Le seuil de binarisation est mal calibre -> essayer un seuil adaptatif au lieu d'Otsu
  b. L'image IA a un fond trop complexe -> demander un fond uni dans le prompt
  c. La silhouette est trop fragmentee -> fusionner les contours avant simplification

- **Le compositeur:** Si le contour injecte produit des artefacts visuels dans le GA (remplissage incorrect, taille disproportionnee), le feedback remonte au module calibration :
  a. Auto-intersection non detectee -> renforcer le check VC2
  b. Echelle incompatible -> normaliser le contour a une bounding box standard

La boucle est bidirectionnelle : le module calibration ne vit pas en isolation. Il recoit du feedback du GA complet et s'ajuste.

---

## PCH6: La matiere de l'organicite

Qu'est-ce qui fait qu'une courbe "semble vivante"?

Trois proprietes, toutes mesurables :

1. **Courbure variable.** Un cercle a une courbure constante — il semble mecanique. Un contour organique a une courbure qui varie continument : plus serree aux articulations (coudes, genoux), plus douce sur les membres longs (dos, jambes). Le pipeline Catmull-Rom produit naturellement cette variation parce qu'il interpole a travers des points irregulierement espaces.

2. **Asymetrie.** Un corps humain n'est jamais symetrique quand il souffre. L'epaule droite tombe plus que la gauche. La tete penche d'un cote. Le prompt IA (P_CAL1) capture cette asymetrie parce qu'il demande un etat clinique, pas une pose anatomique ideale.

3. **Continuite C1.** La courbe n'a pas de cassure dans sa derivee premiere — pas d'angles vifs. C'est exactement ce que garantit le spline Catmull-Rom : continuite C1 par construction. Le contour "coule" d'un point au suivant sans jamais casser.

Ces trois proprietes distinguent un contour organique d'un polygone geometrique. Elles sont le mecanisme technique derriere le phenomene perceptif ("je reconnais mon patient"). La calibration est l'acte de les produire de maniere reproductible.
