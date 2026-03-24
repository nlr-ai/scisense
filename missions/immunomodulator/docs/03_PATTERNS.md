# Patterns — Mission Immunomodulateur GA

## P1: Flux narratif gauche→droite

Le GA raconte une histoire en 3 zones dans un cadre panoramique (1100×560, V1). Le pédiatre lit de gauche à droite : Problème → Intervention → Résolution. Pas de quadrants statiques. Drives B4 (cercle vicieux brisé), B1→B2→B3 (progression zone par zone).

**Evidence:** Jambor & Bornhäuser 2024, rule #4 (expert consensus). Direction de lecture naturelle L→R améliore la compréhension.

## P2: Framework dynamique des 3 Versions

À chaque itération, Silas définit 3 axes de variation pertinents pour l'obstacle cognitif à résoudre. Les axes changent à chaque boucle. Pas d'axes statiques prédéfinis. Toutes les versions sont qualité maximale (VN3). Voir → `PROCESS.md`. Implements A2 (orchestration des 3 agents).

**Evidence:** Design heuristic (non validé empiriquement). Cible Vague 2 de recherche.

## P3: Compression métaphorique

Chaque produit est encodé par une métaphore visuelle justifiée scientifiquement, pas par une liste de cytokines. La métaphore sert la cognition du pédiatre, pas la précision du chercheur.

| Produit | Métaphore | Justification |
|---------|-----------|---------------|
| OM-85 | Bouclier/Verrou | ↓ACE2/TMPRSS2 |
| PMBL | Maçon | ↑E-cadhérine |
| MV130 | Programmateur | Trained immunity épigénétique |
| CRL1505 | Pont Gut-Lung | Axe intestin-poumon |

Source : `Blueprint d'Impact Stratégique...md`

**Evidence:** Jambor & Bornhäuser 2024, rule #3 (expert consensus). Intégration fluide texte+visuels > exhaustivité.

## P4: Agents autonomes en parallèle

Chaque axe de variation est un agent qui produit, documente, s'auto-critique (3 filtres), et re-itère sans feedback humain. Le feedback d'Aurore n'est demandé que pour les décisions scientifiques/esthétiques non-automatisables.

**Evidence:** Design heuristic (non validé empiriquement). Cible Vague 2 de recherche.

## P5: La science se prend en compte elle-même

Le design du GA n'est pas séparé de la science — c'est la science qui encode ses propres mécanismes de transmission. Insight d'Aurore. Voir → `narrative:scisense:meta_science` dans le workspace.

**Evidence:** Design heuristic (non validé empiriquement). Cible Vague 2 de recherche.

## P6: Mobile-first

Le GA est vu principalement sur téléphone (table des matières MDPI). La lisibilité à petite taille prime sur la richesse à grande taille. Validated by V7 (lisibilité 50% zoom). Health: H1 (conformité inclut lisibilité).

**Evidence:** Lee & Yoo 2023 (expert consensus). 87% des sens = vision, GA vus en TOC mobile.

## P7: Cohérence chromatique produit-identité

Chaque produit a une couleur unique et constante sur tout le GA — icônes, barres, flèches, légendes. Le pédiatre associe couleur=produit sans légende explicite. Implemented by B5. Health: H1 (palette check inclus dans conformité).

**Evidence:** Jambor & Bornhäuser 2024, rule #8 (expert consensus). Changement de couleur = changement de sens.

## P8: Itération E2E, pas waterfall

Chaque boucle d'itération produit un **rendu complet évaluable** (pas juste un wireframe). Le cycle est : SVG → PNG full res → PNG delivery → auto-critique → correction → re-render. On ne passe PAS par des phases séparées (wireframe seul → éléments seuls → assemblage seul). L'agent voit le résultat final à chaque tour et s'ajuste. Fail loud si le rendu est cassé (cf. v3 delivery blank). Health: H5.

**Evidence:** Design heuristic (non validé empiriquement). Cible Vague 2 de recherche.

## P9: Provenance des assets

Chaque élément visuel du GA a une source traçable : SVG programmatique (libre de droits par construction), icône vectorielle sourcée (URL + licence), ou élément original créé par Silas. Pas d'éléments IA génératifs dans le livrable final (VN4). Pas de BioRender sans licence commerciale vérifiée (V6). Un fichier `artefacts/PROVENANCE.md` liste chaque élément et sa source. Health: H1 (S1e).

**Evidence:** Design heuristic (non validé empiriquement). Cible Vague 2 de recherche.

## P10: Rendu multi-résolution

Le GA existe toujours en 3 résolutions simultanées :
- **Source** : SVG vectoriel (éditable, scalable)
- **Full res** : PNG 3300×1680 (travail + print 300 DPI)
- **Delivery** : PNG 1100×560 (soumission MDPI + test mobile)
Si l'une des 3 est manquante ou corrompue, le pipeline est en échec. Health: H5.

**Evidence:** Design heuristic (non validé empiriquement). Cible Vague 2 de recherche.

## P11: Version archival

Chaque itération est numérotée et préservée dans `artefacts/wireframes/`. On ne surécrit jamais un artefact précédent. Chaque version porte son numéro (v1, v2, v3, v4...). Les fichiers de dérivation sont dans `iterations/`. L'historique complet est dans SYNC.

**Evidence:** Design heuristic (non validé empiriquement). Cible Vague 2 de recherche.

## P12: IA générative comme accélérateur, pas comme producteur

L'IA générative (NotebookLM infographies, Midjourney, DALL-E) est utilisée comme **référence spatiale et concept art**, jamais dans le livrable final (VN4). Le pattern :

```
NotebookLM analyse le wireframe courant
    → génère un prompt d'infographie optimisé
    → produit un concept art (moodboard)
    → Silas reçoit comme guide spatial
    → traduit en SVG programmatique (le seul livrable)
    → rendu E2E (A5) → auto-critique → itère
```

L'IA générative calibre les volumes, les couleurs, l'équilibre spatial AVANT que Silas code. Le livrable final combine la lisibilité clinique d'un concept humain/IA (R2) avec la conformité technique d'un fichier scripté (R1). Les infographies concept sont archivées dans `artefacts/concepts/` comme sources de dérivation, jamais comme livrables.

**Evidence:** Design heuristic (non validé empiriquement). Cible Vague 2 de recherche.

## P13: Multi-intelligence collaborative

La mission utilise 3 formes d'intelligence en synergie :
- **NotebookLM** : digestion de données brutes, synthèses exhaustives, audit qualité, concept art
- **Silas (Claude Code)** : implémentation SVG programmatique, pipeline technique, auto-critique, doc chain
- **Aurore** : validation scientifique, jugement esthétique, décisions stratégiques

Chaque intelligence a son domaine. Aucune ne fait le travail d'une autre. Le flux est cyclique, pas hiérarchique : NotebookLM informe → Silas implémente → Aurore tranche → NotebookLM analyse le résultat → boucle.

**Evidence:** Design heuristic (non validé empiriquement). Cible Vague 2 de recherche.

## P14: Compositeur paramétrique à générateurs

Le script ne dessine plus des formes hardcodées. Il appelle des **fonctions génératrices** avec des paramètres du YAML. Pas d'assets statiques — tout est généré dynamiquement. Changer une posture = éditer un nombre dans le YAML, pas réécrire du code ni re-sourcer un fichier. Implements A5 (pipeline E2E), A7 (compositeur).

**Evidence:** Design heuristic (non validé empiriquement). Cible Vague 2 de recherche.

## P15: Vecteur de Santé ($H$)

Tous les éléments visuels qui évoluent entre Zone 1 et Zone 3 sont des **fonctions d'une variable unique $H$** (Health Vector, 0.0→1.0). Le mur de briques, la posture de l'enfant, la couleur de fond — tout est paramétré par $H$. Zone 1 = H(0.0), Zone 3 = H(1.0). La transformation est continue, pas un collage de 3 images distinctes.

**Evidence:** Design heuristic (non validé empiriquement). Cible Vague 2 de recherche.

## P16: Cinématique posturale (squelette paramétrique)

Les silhouettes humaines (enfant malade/sain) sont générées par un squelette de 8-10 points d'ancrage (tête, C7, épaules, coudes, poignets, bassin, genoux) dont les coordonnées sont des fonctions de $H$. L'enveloppe organique est un path de Bézier cubique calculé algorithmiquement. Résultat : des silhouettes pleines et expressives, pas des stick figures, entièrement générées par le code.

```
H=0.0 → spine courbé, tête penchée, bras tombants (toux) → empathie clinique
H=0.5 → transition → neutre
H=1.0 → spine droit, tête haute, bras ouverts (célébration) → résolution
```

**Evidence:** Design heuristic (non validé empiriquement). Cible Vague 2 de recherche.

## P17: Référence IA → calibration des paramètres

Les infographies NotebookLM ne sont pas des assets ni des livrables. Ce sont des **blueprints pour calibrer les paramètres** des générateurs. On regarde la posture de l'enfant dans l'infographie, on en déduit les angles/courbures, on ajuste le YAML. L'IA informe la géométrie, le code produit le résultat. Extends P12.

**Élargissement V10 : Calibration Intégrale.** L'infographie IA n'est pas un calibrateur de volumes uniquement. C'est un **calibrateur multi-dimensionnel** qui produit une réponse intégrée à : volumes, couleurs en contexte, textures, espacements, espaces négatifs, ancrage, hiérarchie de lecture, et tonalité émotionnelle. Silas extrait de chaque infographie non seulement les contours (approche iii) mais aussi les **ratios d'espacement**, la **densité locale**, et le **poids visuel relatif** des éléments pour recalibrer ses paramètres YAML. Chaque infographie IA informe les patterns P7, P18, P20, P21, P22, P26-P31.

**Evidence:** Design heuristic (non validé empiriquement). Cible Vague 2 de recherche.

## P24: Concept ASCII avant wireframe

Avant tout wireframe SVG, produire des **propositions en ASCII art** dans un PDF. Cette phase force la réflexion sur le flux narratif et la structure spatiale AVANT de toucher au code. Le cycle est :

```
DIAGNOSTIC → AXES DE VARIATION → 3 PROPOSITIONS ASCII → PDF → VÉRIFICATION VISUELLE → ENVOI AURORE → FEEDBACK → WIREFRAME
```

L'ASCII art suffit pour qu'Aurore valide la direction. Pas besoin de code pour trancher entre 3 architectures visuelles. Économise des jours de wireframing dans la mauvaise direction.

**Evidence:** Design heuristic (non validé empiriquement). Cible Vague 2 de recherche.

## P25: Vérification visuelle obligatoire

**Tout artefact généré (PDF, PNG, SVG) doit être relu visuellement avant envoi ou validation.** Un fichier qui compile n'est pas un fichier qui communique. Utiliser le Read tool pour voir le rendu réel. Cela attrape : texte tronqué, ASCII art cassé, pages blanches, encodage Unicode, mise en page décalée.

**Evidence:** Design heuristic (non validé empiriquement). Cible Vague 2 de recherche.

## P26: Espace Négatif — le silence visuel

Ce qui n'est PAS dessiné est aussi important que ce qui l'est. L'espace négatif (l'air autour des éléments) donne la lisibilité et guide le regard. Un GA surchargé est un GA illisible — le pédiatre décroche en <1s.

Règles :
- Chaque élément visuel majeur (enfant, bronche, barres d'évidence) doit avoir un espace de respiration d'au moins 5% de sa propre dimension autour de lui
- Le lumen de la bronche est un espace négatif fonctionnel — il DOIT rester majoritairement vide (c'est de l'air) pour que les virus (gauche) et les IgA (droite) soient lisibles par contraste
- Les marges gauche et droite (enfants + cycle/évidence) ne doivent pas coller au cadre de la bronche
- L'espace négatif encode aussi l'information : un lumen vide côté sain = "l'air passe librement" = résolution

Calibré par : infographie IA (P17 élargi). Tradeoff T1 (densité vs lisibilité).

**Evidence:** Design heuristic (non validé empiriquement). Cible Vague 2 de recherche.

## P27: Texture et Matérialité — le tissu vivant

La différence entre un épithélium qui "semble vivant" et des rectangles plats. Le rendu SVG programmatique a tendance à produire des formes géométriques froides. La texture encode la biologie sans ajouter de mots.

Techniques de texture en SVG pur :
- **Gradient subtil** sur les cellules épithéliales (pas de fill plat)
- **Opacité variable** sur le muscle lisse (gradient amber→vert = inflammation qui se résout)
- **Irrégularité contrôlée** sur les branches DC (P20 impose des branches courbes irrégulières, pas des étoiles symétriques)
- **Bruit de Perlin** simulé via des micro-variations de position (seed aléatoire fixe pour reproductibilité)

Ce que la texture ne fait PAS : ajouter du détail photoréaliste. On reste en line art médical (P20). La texture est une micro-variation, pas un rendu 3D.

Calibré par : infographie IA (P17 élargi). Renforce P20 (abstraction professionnelle).

**Evidence:** Design heuristic (non validé empiriquement). Cible Vague 2 de recherche.

## P28: Hiérarchie Typographique — les 30 mots qui comptent

Le budget de 30 mots (V3) n'est pas juste un plafond — c'est un système de hiérarchie. Chaque mot a un poids visuel qui encode son importance.

3 niveaux typographiques :
- **Niveau 1 (ancre)** : les mots que le pédiatre lit en premier. Plus grands, plus gras. Ex: "Wheezing/Asthma", "Clinical evidence". Font-size ≥ 32 au format 3x.
- **Niveau 2 (contexte)** : les labels de mécanismes et produits. Taille moyenne. Ex: "OM-85", "Viral RTIs", "18 RCTs". Font-size 24-30 au format 3x.
- **Niveau 3 (ponctuation)** : les micro-labels optionnels. Petits mais lisibles. Ex: "Th1", "Th2", "gut". Font-size 18-22 au format 3x. Peuvent être supprimés si le budget est serré.

Règle : le test de lisibilité V7 (50% zoom = 550×280) doit passer pour TOUS les niveaux. Si le Niveau 3 ne passe pas, le supprimer plutôt que le réduire.

Placement : les labels de Niveau 1 sont toujours HORS de la bronche (marges ou légende). Les labels de Niveau 2 sont dans ou près de leurs éléments. Le Niveau 3 est collé à son objet.

**Evidence:** Design heuristic (non validé empiriquement). Cible Vague 2 de recherche.

## P29: Densité Locale — le gradient d'information

La densité d'information n'est pas uniforme sur le GA. Elle suit un gradient qui encode la narration :

- **Zone 1 (gauche)** : densité FAIBLE. Le problème doit être immédiatement lisible. Un enfant, un cercle vicieux, quelques virus. Pas de surcharge.
- **Zone 2 (centre/bronche)** : densité HAUTE. C'est le coeur scientifique. Les 4 bandes, les attributions produit, les transformations L→R. La densité est justifiée parce que le pédiatre y arrive APRÈS avoir compris le problème.
- **Zone 3 (droite)** : densité MOYENNE. Résolution (enfant sain) + outil de décision (barres d'évidence). Clair et actionable.

Ce gradient suit naturellement le flux de lecture L→R (P1) : accroche simple → complexité justifiée → conclusion actionable.

Si une zone est trop dense, la correction n'est pas de compresser les éléments mais de vérifier si tous les éléments de cette zone sont nécessaires (P3 compression métaphorique).

**Evidence:** Design heuristic (non validé empiriquement). Cible Vague 2 de recherche.

## P30: Flux de Lecture Secondaire — l'axe vertical

P1 définit le flux principal gauche→droite. Mais la "Bronche Vivante" (V2-A) introduit un flux secondaire VERTICAL : du lumen (haut) vers le muscle lisse (bas). Ce flux encode la profondeur tissulaire.

Les deux flux coexistent :
- **Axe horizontal (P1)** : malade → sain (le temps / l'intervention)
- **Axe vertical (P30)** : surface → profondeur (la localisation anatomique)

Le regard du pédiatre fait un L inversé :
1. Scan horizontal rapide (P1) : rouge à gauche, vert à droite = "ça guérit"
2. Scan vertical dans la zone d'intérêt : "comment ça guérit" = les 4 couches

Ce flux vertical est ce qui distingue V2-A des designs classiques 3-zones. La topologie spatiale (P19) ne peut fonctionner que si le pédiatre lit AUSSI de haut en bas.

**Evidence:** Design heuristic (non validé empiriquement). Cible Vague 2 de recherche.

## P31: Poids Visuel Relatif — la balance des éléments

Chaque élément du GA a un poids visuel (aire × opacité × contraste × saturation). Le poids visuel relatif doit refléter l'importance clinique ET le niveau de preuve.

Hiérarchie de poids attendue :
1. **Enfants** (Z1/Z3) : poids maximal — ce sont les ancrages émotionnels (B1, B7, V12)
2. **Bronche** (centre) : poids majeur — c'est le sujet scientifique
3. **Evidence bars** (Z3) : poids moyen-fort — c'est l'outil de décision (B3)
4. **Cercle vicieux** (Z1) : poids moyen — contexte clinique (B4)
5. **Légende** : poids faible — référence, pas contenu central
6. **Arc CRL1505** : poids faible — information secondaire (préclinique)

Ce qui viole P31 : un arc CRL1505 aussi épais que le bouclier OM-85 (le préclinique ne doit pas avoir le même poids visuel que 18 RCTs). Une légende plus grande que les barres d'évidence.

Renforce P21 (gravité clinique) au niveau de l'image entière, pas juste de la Zone 3.

**Evidence:** Design heuristic (non validé empiriquement). Cible Vague 2 de recherche.

---

> **Note:** Les patterns VEC génériques (P24-P34) sont maintenus dans `docs/vec/design_system/03_PATTERNS.md`.
> Les patterns ci-dessous sont conservés ici pour référence historique et parce qu'ils contiennent
> des détails spécifiques à la mission immunomodulateur.

## Design System Biologique — Méta-Patterns (extraits de l'audit SD1)

Les patterns P18-P23 sont le **lexique sémiotique** de SciSense : les règles de traduction entre biologie clinique et représentation visuelle. Chaque faille de l'audit v4 (SD1_Graphical_Abstract_Precision_Audit.pdf) est la conséquence de la violation d'un de ces patterns. Validés par NotebookLM (24 mars 2026).

## P18: Embodiment Actif — la physicalité de l'action

Les métaphores visuelles ne doivent jamais léviter. Elles doivent **s'encastrer, fusionner ou percuter** le tissu qu'elles modifient. Un agent qui flotte dans le vide est déconnecté de son action biologique — le pédiatre ne comprend pas le mécanisme.

| Agent | Action biologique | Contrainte visuelle |
|-------|------------------|---------------------|
| OM-85 | ↓ACE2/TMPRSS2 à la surface cellulaire | Bouclier encastré SUR les briques, entre virus et épithélium |
| PMBL | ↑E-cadhérine entre cellules | Briques teal comblant physiquement les brèches + agrafes moléculaires |
| MV130 | Reprogrammation épigénétique intracellulaire | Hélice DANS le noyau de la DC |

Source: Faille 3 (OM-85 flottant), Faille 2 (PMBL cartoon). Implements B2.

**Evidence:** Design heuristic (non validé empiriquement). Cible Vague 2 de recherche.

## P19: Topologie Spatiale — position = mécanisme

La localisation d'une métaphore dans l'espace du GA encode son mécanisme biologique. Intracellulaire ≠ surface ≠ systémique. Si deux agents sont au même endroit, le pédiatre ne distingue pas leurs modes d'action.

- **Intracellulaire** → DANS le hub DC : MV130 (trained immunity épigénétique)
- **Surface cellulaire** → SUR le mur : OM-85 (verrouillage récepteurs), PMBL (scellage jonctions)
- **Systémique** → Arc partant du BAS de l'image : CRL1505 (axe intestin-poumon, action orale à distance)

L'arc CRL1505 doit pointer indépendamment vers barrière + DC, sans croiser l'hélice MV130. Source: Faille 4, 5. Implements V13.

**Evidence:** Design heuristic (non validé empiriquement). Cible Vague 2 de recherche.

## P20: Abstraction Professionnelle — tonalité visuelle Q2

Une revue Q2 (MDPI Children) requiert une esthétique de rigueur clinique. Proscrire les entités humanoïdes pour les mécanismes moléculaires. Imposer le **Line Art médical**.

- Cellule Dendritique : morphologie filopodiale exacte (branches courbes irrégulières, corps vésiculaire), pas étoile symétrique
- PMBL : agrafe moléculaire abstraite, pas maçon humain
- Intestin (CRL1505) : squiggle line art minimal, pas organe anatomique réaliste
- Virus : icône stylisée (cercle + spikes), pas monstre cartoon

Validé par NotebookLM : corps irrégulier + branches courbes = reconnaissable par immunologiste en <2s. Source: Faille 2, 7, 8.

**Evidence:** Design heuristic (non validé empiriquement). Cible Vague 2 de recherche.

## P21: Gravité Clinique — proportionnalité volumétrique

L'aire visuelle d'un élément est proportionnelle à sa robustesse clinique. L'évidence n'est pas linéaire — 18 RCTs écrasent un stade préclinique. Le pédiatre doit "peser" la preuve sans effort.

| Produit | Évidence | Masse visuelle relative |
|---------|----------|------------------------|
| OM-85 | 18 RCTs | 100% — ancre visuelle dominante |
| PMBL | 5 RCTs | ~60% |
| MV130 | 1 RCT | ~30% |
| CRL1505 | Préclinique | ~10-15% — baseline |

Le bloc OM-85 bleu doit être 3-4x plus massif que le bloc CRL1505 vert. Si Z3 paraît faible, augmenter la masse du bloc OM-85, PAS la largeur de la zone (ratio 27/46/27 validé). Source: Faille 9. Implements B3.

**Evidence:** Cleveland & McGill 1984 + loi de Stevens (RCT + psychophysique). Aire compresse les différences (beta~0.7) ; longueur recommandée comme canal primaire.

## P22: Micro-Ancres Moléculaires — ponctuation visuelle

L'interdiction des listes de cytokines (VN1) ne doit pas vider l'image de ses repères biologiques. Utiliser des pictogrammes universels microscopiques pour "ponctuer" l'action sans surcharger.

- **IgA sécrétoires** : petits Y (~15px) au-dessus du mur réparé, dans la lumière bronchique (lumen apical). PAS dans le mur. Elles sont transcytées à travers l'épithélium pour neutraliser les virus dans le lumen.
- **IFN** : subtiles flèches ↑ près de l'épithélium sain (Z3)
- **Pas de texte supplémentaire** — ces sont des ancres visuelles, pas des labels

Le spécialiste y trouve la plausibilité biologique ; le clinicien généraliste n'est pas noyé. Source: Faille 8. Validé par NotebookLM (positionnement lumen apical).

**Evidence:** Jambor & Bornhäuser 2024, rule #7 (expert consensus). Le texte désambiguïse les pictogrammes.

## P23: Résolution Topologique — fractalisme narratif

Une pathologie chronique auto-entretenue est un **cercle fermé**. Sa résolution est un **vecteur qui le fracture**.

- **Zone 1** : Cercle vicieux = flèche circulaire fermée (4 stations : Viral RTIs → Th2 bias → Remodeling → Re-susceptibility). La forme géométrique EST le message.
- **Zone 3** : La ligne de flux vert/bleu (épithélium restauré) doit se prolonger comme une lance qui vient **fracturer physiquement** une ligne rouge de morbidité menant au Wheezing/Asthma. Coupure visuelle nette.

**Précision SD3 (slide 15)** : La flèche verte de santé (health arrow) doit **physiquement FRACTURER** le tracé rouge du cercle vicieux. Ce n'est pas une transition implicite gauche→droite — c'est un élément graphique explicite : la lance verte coupe net le cycle rouge. "La coupure visuelle nette symbolise l'arrêt de la morbidité. C'est le climax cognitif du design." La fracture doit être perceptible comme un acte — un moment de rupture, pas un fondu. Renforce B4 (le cercle vicieux est brisé).

Validé par NotebookLM (SD1 + SD3) comme application exacte de P3 (Compression Métaphorique) et B4 (Breaking the Cycle). Ce n'est pas une sur-simplification — c'est le climax cognitif du GA. Source: Faille 6, 10 (SD1), Slide 15 (SD3).

**Evidence:** Design heuristic (non validé empiriquement). Cible Vague 2 de recherche.
