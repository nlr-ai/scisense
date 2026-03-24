# Patterns — Mission Immunomodulateur GA

## P1: Flux narratif gauche→droite

Le GA raconte une histoire en 3 zones dans un cadre panoramique (1100×560, V1). Le pédiatre lit de gauche à droite : Problème → Intervention → Résolution. Pas de quadrants statiques. Drives B4 (cercle vicieux brisé), B1→B2→B3 (progression zone par zone).

## P2: Framework dynamique des 3 Versions

À chaque itération, Silas définit 3 axes de variation pertinents pour l'obstacle cognitif à résoudre. Les axes changent à chaque boucle. Pas d'axes statiques prédéfinis. Toutes les versions sont qualité maximale (VN3). Voir → `PROCESS.md`. Implements A2 (orchestration des 3 agents).

## P3: Compression métaphorique

Chaque produit est encodé par une métaphore visuelle justifiée scientifiquement, pas par une liste de cytokines. La métaphore sert la cognition du pédiatre, pas la précision du chercheur.

| Produit | Métaphore | Justification |
|---------|-----------|---------------|
| OM-85 | Bouclier/Verrou | ↓ACE2/TMPRSS2 |
| PMBL | Maçon | ↑E-cadhérine |
| MV130 | Programmateur | Trained immunity épigénétique |
| CRL1505 | Pont Gut-Lung | Axe intestin-poumon |

Source : `Blueprint d'Impact Stratégique...md`

## P4: Agents autonomes en parallèle

Chaque axe de variation est un agent qui produit, documente, s'auto-critique (3 filtres), et re-itère sans feedback humain. Le feedback d'Aurore n'est demandé que pour les décisions scientifiques/esthétiques non-automatisables.

## P5: La science se prend en compte elle-même

Le design du GA n'est pas séparé de la science — c'est la science qui encode ses propres mécanismes de transmission. Insight d'Aurore. Voir → `narrative:scisense:meta_science` dans le workspace.

## P6: Mobile-first

Le GA est vu principalement sur téléphone (table des matières MDPI). La lisibilité à petite taille prime sur la richesse à grande taille. Validated by V7 (lisibilité 50% zoom). Health: H1 (conformité inclut lisibilité).

## P7: Cohérence chromatique produit-identité

Chaque produit a une couleur unique et constante sur tout le GA — icônes, barres, flèches, légendes. Le pédiatre associe couleur=produit sans légende explicite. Implemented by B5. Health: H1 (palette check inclus dans conformité).

## P8: Itération E2E, pas waterfall

Chaque boucle d'itération produit un **rendu complet évaluable** (pas juste un wireframe). Le cycle est : SVG → PNG full res → PNG delivery → auto-critique → correction → re-render. On ne passe PAS par des phases séparées (wireframe seul → éléments seuls → assemblage seul). L'agent voit le résultat final à chaque tour et s'ajuste. Fail loud si le rendu est cassé (cf. v3 delivery blank). Health: H5.

## P9: Provenance des assets

Chaque élément visuel du GA a une source traçable : SVG programmatique (libre de droits par construction), icône vectorielle sourcée (URL + licence), ou élément original créé par Silas. Pas d'éléments IA génératifs dans le livrable final (VN4). Pas de BioRender sans licence commerciale vérifiée (V6). Un fichier `artefacts/PROVENANCE.md` liste chaque élément et sa source. Health: H1 (S1e).

## P10: Rendu multi-résolution

Le GA existe toujours en 3 résolutions simultanées :
- **Source** : SVG vectoriel (éditable, scalable)
- **Full res** : PNG 3300×1680 (travail + print 300 DPI)
- **Delivery** : PNG 1100×560 (soumission MDPI + test mobile)
Si l'une des 3 est manquante ou corrompue, le pipeline est en échec. Health: H5.

## P11: Version archival

Chaque itération est numérotée et préservée dans `artefacts/wireframes/`. On ne surécrit jamais un artefact précédent. Chaque version porte son numéro (v1, v2, v3, v4...). Les fichiers de dérivation sont dans `iterations/`. L'historique complet est dans SYNC.

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

## P13: Multi-intelligence collaborative

La mission utilise 3 formes d'intelligence en synergie :
- **NotebookLM** : digestion de données brutes, synthèses exhaustives, audit qualité, concept art
- **Silas (Claude Code)** : implémentation SVG programmatique, pipeline technique, auto-critique, doc chain
- **Aurore** : validation scientifique, jugement esthétique, décisions stratégiques

Chaque intelligence a son domaine. Aucune ne fait le travail d'une autre. Le flux est cyclique, pas hiérarchique : NotebookLM informe → Silas implémente → Aurore tranche → NotebookLM analyse le résultat → boucle.

## P14: Compositeur paramétrique à générateurs

Le script ne dessine plus des formes hardcodées. Il appelle des **fonctions génératrices** avec des paramètres du YAML. Pas d'assets statiques — tout est généré dynamiquement. Changer une posture = éditer un nombre dans le YAML, pas réécrire du code ni re-sourcer un fichier. Implements A5 (pipeline E2E), A7 (compositeur).

## P15: Vecteur de Santé ($H$)

Tous les éléments visuels qui évoluent entre Zone 1 et Zone 3 sont des **fonctions d'une variable unique $H$** (Health Vector, 0.0→1.0). Le mur de briques, la posture de l'enfant, la couleur de fond — tout est paramétré par $H$. Zone 1 = H(0.0), Zone 3 = H(1.0). La transformation est continue, pas un collage de 3 images distinctes.

## P16: Cinématique posturale (squelette paramétrique)

Les silhouettes humaines (enfant malade/sain) sont générées par un squelette de 8-10 points d'ancrage (tête, C7, épaules, coudes, poignets, bassin, genoux) dont les coordonnées sont des fonctions de $H$. L'enveloppe organique est un path de Bézier cubique calculé algorithmiquement. Résultat : des silhouettes pleines et expressives, pas des stick figures, entièrement générées par le code.

```
H=0.0 → spine courbé, tête penchée, bras tombants (toux) → empathie clinique
H=0.5 → transition → neutre
H=1.0 → spine droit, tête haute, bras ouverts (célébration) → résolution
```

## P17: Référence IA → calibration des paramètres

Les infographies NotebookLM ne sont pas des assets ni des livrables. Ce sont des **blueprints pour calibrer les paramètres** des générateurs. On regarde la posture de l'enfant dans l'infographie, on en déduit les angles/courbures, on ajuste le YAML. L'IA informe la géométrie, le code produit le résultat. Extends P12.

---

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

## P19: Topologie Spatiale — position = mécanisme

La localisation d'une métaphore dans l'espace du GA encode son mécanisme biologique. Intracellulaire ≠ surface ≠ systémique. Si deux agents sont au même endroit, le pédiatre ne distingue pas leurs modes d'action.

- **Intracellulaire** → DANS le hub DC : MV130 (trained immunity épigénétique)
- **Surface cellulaire** → SUR le mur : OM-85 (verrouillage récepteurs), PMBL (scellage jonctions)
- **Systémique** → Arc partant du BAS de l'image : CRL1505 (axe intestin-poumon, action orale à distance)

L'arc CRL1505 doit pointer indépendamment vers barrière + DC, sans croiser l'hélice MV130. Source: Faille 4, 5. Implements V13.

## P20: Abstraction Professionnelle — tonalité visuelle Q2

Une revue Q2 (MDPI Children) requiert une esthétique de rigueur clinique. Proscrire les entités humanoïdes pour les mécanismes moléculaires. Imposer le **Line Art médical**.

- Cellule Dendritique : morphologie filopodiale exacte (branches courbes irrégulières, corps vésiculaire), pas étoile symétrique
- PMBL : agrafe moléculaire abstraite, pas maçon humain
- Intestin (CRL1505) : squiggle line art minimal, pas organe anatomique réaliste
- Virus : icône stylisée (cercle + spikes), pas monstre cartoon

Validé par NotebookLM : corps irrégulier + branches courbes = reconnaissable par immunologiste en <2s. Source: Faille 2, 7, 8.

## P21: Gravité Clinique — proportionnalité volumétrique

L'aire visuelle d'un élément est proportionnelle à sa robustesse clinique. L'évidence n'est pas linéaire — 18 RCTs écrasent un stade préclinique. Le pédiatre doit "peser" la preuve sans effort.

| Produit | Évidence | Masse visuelle relative |
|---------|----------|------------------------|
| OM-85 | 18 RCTs | 100% — ancre visuelle dominante |
| PMBL | 5 RCTs | ~60% |
| MV130 | 1 RCT | ~30% |
| CRL1505 | Préclinique | ~10-15% — baseline |

Le bloc OM-85 bleu doit être 3-4x plus massif que le bloc CRL1505 vert. Si Z3 paraît faible, augmenter la masse du bloc OM-85, PAS la largeur de la zone (ratio 27/46/27 validé). Source: Faille 9. Implements B3.

## P22: Micro-Ancres Moléculaires — ponctuation visuelle

L'interdiction des listes de cytokines (VN1) ne doit pas vider l'image de ses repères biologiques. Utiliser des pictogrammes universels microscopiques pour "ponctuer" l'action sans surcharger.

- **IgA sécrétoires** : petits Y (~15px) au-dessus du mur réparé, dans la lumière bronchique (lumen apical). PAS dans le mur. Elles sont transcytées à travers l'épithélium pour neutraliser les virus dans le lumen.
- **IFN** : subtiles flèches ↑ près de l'épithélium sain (Z3)
- **Pas de texte supplémentaire** — ces sont des ancres visuelles, pas des labels

Le spécialiste y trouve la plausibilité biologique ; le clinicien généraliste n'est pas noyé. Source: Faille 8. Validé par NotebookLM (positionnement lumen apical).

## P23: Résolution Topologique — fractalisme narratif

Une pathologie chronique auto-entretenue est un **cercle fermé**. Sa résolution est un **vecteur qui le fracture**.

- **Zone 1** : Cercle vicieux = flèche circulaire fermée (4 stations : Viral RTIs → Th2 bias → Remodeling → Re-susceptibility). La forme géométrique EST le message.
- **Zone 3** : La ligne de flux vert/bleu (épithélium restauré) doit se prolonger comme une lance qui vient **fracturer physiquement** une ligne rouge de morbidité menant au Wheezing/Asthma. Coupure visuelle nette.

Validé par NotebookLM comme application exacte de P3 (Compression Métaphorique) et B4 (Breaking the Cycle). Ce n'est pas une sur-simplification — c'est le climax cognitif du GA. Source: Faille 6, 10.
