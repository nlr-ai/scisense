# Algorithm — vec/calibration

## A_CAL1: Generation de l'image IA source

```
ENTREE: Contexte clinique + tranche d'age + valeur H cible

1. FORMULER LE PROMPT
   - Langage naturel clinique (P_CAL1)
   - Decrire la charge physique ET emotionnelle
   - Inclure l'age, la posture attendue, le contexte familial
   - ZERO specification technique (resolution, style, format)
   - Inclure l'indicateur H:
     H=0.0 : "recroqueville, toussant, epuise par les infections repetees"
     H=1.0 : "epanoui, bras ouverts, respire librement, energie retrouvee"

2. GENERER
   - Envoyer le prompt au modele image (Ideogram ou Gemini)
   - Recuperer l'image (PNG/JPEG)
   - Sauver dans artefacts/calibration/source/{age}_{H}_raw.png

3. EVALUER (visuel rapide)
   - L'image contient-elle un enfant dans la posture attendue?
   - La silhouette est-elle suffisamment contrastee pour extraction?
   - Si NON -> reformuler le prompt (retour etape 1, max 3 tentatives)

SORTIE: Image source PNG/JPEG dans artefacts/calibration/source/
```

---

## A_CAL2: Extraction de contour brut (scikit-image)

```
ENTREE: Image source PNG/JPEG

1. PRETRAITEMENT
   - Charger l'image avec skimage.io.imread()
   - Convertir en niveaux de gris (rgb2gray)
   - Appliquer un flou gaussien (sigma=2.0) pour attenuer le bruit haute frequence
   - Binariser avec un seuil Otsu (threshold_otsu) ou manuel si Otsu echoue

2. EXTRACTION
   - skimage.measure.find_contours(image_binaire, level=0.5)
   - Recuperer tous les contours detectes
   - Filtrer par aire : garder uniquement le contour principal (aire maximale)
     -> le contour principal est la silhouette de l'enfant
   - Si plusieurs contours de taille comparable (ex: bras separes du corps)
     -> les fusionner par hull convexe partiel ou les traiter separement

3. SAUVER
   - Exporter les coordonnees brutes en JSON:
     {
       "source": "artefacts/calibration/source/{age}_{H}_raw.png",
       "contour_raw": [[x1,y1], [x2,y2], ...],
       "n_points": N,
       "bounding_box": [x_min, y_min, x_max, y_max],
       "area": A
     }
   - Fichier: artefacts/contours/{SN}_{state}_points.json

SORTIE: Fichier JSON contour brut (centaines de points)
```

---

## A_CAL3: Simplification Douglas-Peucker

```
ENTREE: Fichier JSON contour brut (A_CAL2 output)

1. CHARGER
   - Lire les coordonnees brutes depuis le JSON
   - Convertir en numpy array

2. SIMPLIFIER
   - skimage.measure.approximate_polygon(contour, tolerance=epsilon)
   - OU rdp (Ramer-Douglas-Peucker) via la librairie rdp
   - epsilon = perimetre_contour * facteur_simplification
   - facteur_simplification initial: 0.02 (2% du perimetre)

3. EVALUER
   - Compter les points resultants
   - Cible: 25-50 points pour une silhouette enfant
   - Si > 50 points: augmenter epsilon et re-simplifier
   - Si < 15 points: diminuer epsilon (trop de perte de forme)
   - Calculer le Hausdorff distance entre contour brut et contour simplifie
     -> si > 5% du diametre du bounding box: ALERTE (trop de deformation)

4. SAUVER
   - Ajouter au JSON:
     {
       "contour_simplified": [[x1,y1], [x2,y2], ...],
       "n_points_simplified": M,
       "epsilon": epsilon_utilisee,
       "hausdorff_distance": d
     }

SORTIE: JSON enrichi avec contour simplifie (25-50 points)
```

---

## A_CAL4: Lissage Catmull-Rom -> Bezier cubique

```
ENTREE: JSON enrichi avec contour simplifie (A_CAL3 output)

1. CHARGER
   - Lire les points simplifies depuis le JSON
   - S'assurer que le contour est ferme (premier point = dernier point)

2. CATMULL-ROM SPLINE
   - Pour chaque segment consecutif de 4 points (P0, P1, P2, P3):
     a. Calculer les points de controle Bezier:
        CP1 = P1 + (P2 - P0) / 6
        CP2 = P2 - (P3 - P1) / 6
     b. Le segment Bezier cubique va de P1 a P2 avec CP1, CP2
   - Pour les extremites (contour ferme):
     -> P0 du premier segment = avant-dernier point
     -> P3 du dernier segment = deuxieme point

3. GENERER LE PATH SVG
   - M x1,y1 (move to premier point)
   - C cp1x,cp1y cp2x,cp2y x2,y2 (pour chaque segment)
   - Z (fermer le path)
   - Formater avec precision 1 decimale (suffisant pour SVG)

4. VALIDER
   - Parser le path SVG avec xml.etree
   - Verifier qu'il est un path ferme (commence par M, finit par Z)
   - Verifier l'absence d'auto-intersections (test simplifie: aucun segment ne croise un segment non-adjacent)
   - Rendre un PNG temporaire et verifier visuellement

5. SAUVER
   - SVG: artefacts/contours/{SN}_{state}_contour.svg
   - Ajouter au JSON:
     {
       "svg_path_d": "M ... C ... Z",
       "n_bezier_segments": K,
       "self_intersections": true/false
     }

SORTIE: Fichier SVG natif + JSON enrichi complet
```

---

## A_CAL5: Comparaison target vs output

```
ENTREE: Image source (A_CAL1) + SVG contour final (A_CAL4)

1. RENDRE LE SVG
   - Rendre le SVG contour en PNG a la meme resolution que l'image source
   - Remplir le contour avec une couleur semi-transparente (opacity 0.5)

2. SUPERPOSER
   - Placer le contour rendu sur l'image source (alpha compositing)
   - Aligner via les bounding boxes
   - Sauver: artefacts/comparisons/target_vs_output_{SN}_{state}.png

3. MESURER LE GAP
   - Binariser l'image source (silhouette = 1, fond = 0)
   - Binariser le contour rendu (interieur = 1, exterieur = 0)
   - Calculer:
     a. IoU (Intersection over Union) entre les deux masques
     b. Gap = 1 - IoU
     c. Hausdorff distance entre les contours des deux masques

4. EVALUER
   - IoU > 0.80 -> PASS (le contour capture suffisamment la silhouette)
   - IoU 0.70-0.80 -> REVIEW (calibration a ajuster)
   - IoU < 0.70 -> FAIL (epsilon trop eleve ou extraction defectueuse)
   - NOTE: le seuil IoU est deliberement bas (0.80 pas 0.95) parce que
     l'objectif est l'organicite, pas la fidelite pixel. Un contour plus
     simple qui "coule" est prefere a un contour bruite qui "copie".

5. SAUVER LE RAPPORT
   - artefacts/comparisons/report_{SN}_{state}.json:
     {
       "iou": 0.XX,
       "hausdorff": D,
       "verdict": "PASS|REVIEW|FAIL",
       "source": "...",
       "svg": "..."
     }

SORTIE: Image de comparaison PNG + rapport JSON
```

---

## A_CAL6: Contour Matrix — exploration systematique

```
ENTREE: Definition de la grille (tranches d'age x valeurs H)

1. DEFINIR LA GRILLE
   - Ages: [2-3, 4-6, 7-10]
   - H extremes: [0.0, 1.0]
   - -> 6 cellules a generer (3 ages x 2 extremes)
   - Les intermediaires (H=0.25, 0.5, 0.75) sont interpoles, pas generes

2. POUR CHAQUE CELLULE (age, H):
   a. Executer A_CAL1 (generation image IA)
   b. Executer A_CAL2 (extraction contour brut)
   c. Executer A_CAL3 (simplification Douglas-Peucker)
   d. Executer A_CAL4 (lissage Catmull-Rom -> Bezier)
   e. Executer A_CAL5 (comparaison target vs output)
   f. Si verdict FAIL -> reformuler le prompt et re-executer (max 3 tentatives)

3. GENERER LES INTERMEDIAIRES
   - Pour chaque tranche d'age:
     a. Charger les squelettes (points d'ancrage) de H=0.0 et H=1.0
     b. Interpoler lineairement pour H=0.25, 0.5, 0.75
     c. Generer l'enveloppe Bezier pour chaque intermediaire (A_CAL4 etape 2-3)
     d. Rendre en PNG pour inspection visuelle

4. COMPARER ET SELECTIONNER
   - Pour chaque tranche d'age, generer une strip horizontale:
     H=0.0 | H=0.25 | H=0.5 | H=0.75 | H=1.0
   - Evaluer:
     a. Expressivite: quelle tranche d'age declenche le plus de projection clinique?
     b. Continuite: les intermediaires sont-ils naturels (pas de rupture)?
     c. Qualite technique: IoU > 0.80 pour les extremes?
   - Selectionner la tranche d'age gagnante pour le GA

5. SAUVER
   - artefacts/calibration/contour_matrix.png (grille complete)
   - artefacts/calibration/selection.json:
     {
       "selected_age": "4-6",
       "justification": "...",
       "iou_sick": 0.XX,
       "iou_healthy": 0.XX
     }

SORTIE: Contour Matrix visualisee + selection documentee
```

---

## A_CAL7: Validation empathie (boucle humaine)

```
ENTREE: Contour SVG selectionne (A_CAL6 output) + Aurore

1. PREPARER LE TEST
   - Rendre la silhouette H=0.0 isolee (fond neutre, pas de contexte GA)
   - Rendre la silhouette H=1.0 isolee
   - Rendre une silhouette geometrique equivalente (stick figure meme posture)

2. PRESENTER A AURORE
   - Envoyer les 3 images via MCP (send)
   - Question: "Qu'est-ce que tu vois dans chaque image? En combien de temps?"
   - PAS de contexte prealable ("c'est un enfant malade")
   - L'objectif est de mesurer si la silhouette organique active la reconnaissance
     SANS aide contextuelle

3. EVALUER LA REPONSE
   - Si Aurore dit "un enfant malade" en <2s pour la silhouette organique
     et PAS pour le stick figure -> RC2 PASS
   - Si elle dit "une forme" ou met > 5s -> RC2 FAIL, recalibrer
   - Si elle identifie les deux en <2s -> le stick figure suffit
     (hypothese a falsifier — P_CAL1 prefere l'organique par defaut)

4. DOCUMENTER
   - artefacts/calibration/empathy_test.md:
     - Reponse Aurore verbatim
     - Temps de reaction (estime)
     - Verdict RC2
     - Ajustements necessaires

SORTIE: Verdict RC2 (PASS/FAIL) + documentation
```

---

## A_CAL8: Extraction des parametres integraux (P17 elargi)

```
ENTREE: Infographie IA (NotebookLM, Ideogram, Gemini)

1. CHARGER L'INFOGRAPHIE
   - L'infographie est une image complete (pas juste une silhouette)
   - Elle represente un GA ou un concept art du GA entier

2. EXTRAIRE LES PARAMETRES GEOMETRIQUES
   - Mesurer les marges (pixels du bord au premier element)
   - Mesurer les gaps entre elements principaux
   - Calculer les ratios: margin/total_width, gap/element_width
   - Calculer la densite locale par zone (nombre d'elements / aire de la zone)

3. EXTRAIRE LES PARAMETRES CHROMATIQUES
   - Histogramme des couleurs dominantes (top 5-10)
   - Temperature de couleur globale (warm/cool)
   - Saturation moyenne par zone
   - Contraste entre elements et fond

4. ESTIMER LES PARAMETRES QUALITATIFS
   - Poids visuel relatif: classer les elements par (aire * opacite * contraste)
   - Hierarchie de lecture: ordre probable de scan visuel
   - Tonalite emotionnelle: {grave, neutre, legere} x {chaude, froide}
   - Espace negatif: ratio vide/plein global et par zone

5. GENERER LE YAML
   - calibration_params.yaml:
     ```yaml
     source: "artefacts/calibration/source/infographic_N.png"
     spacing:
       margin_left_ratio: 0.05
       margin_right_ratio: 0.05
       gap_between_zones_ratio: 0.03
       # ...
     density:
       zone_1: 3  # elements
       zone_2: 8
       zone_3: 5
     weights:
       children: 1.0
       bronchus: 0.8
       evidence_bars: 0.6
       vicious_cycle: 0.5
       legend: 0.2
     emotional_tone: "grave-warm"
     ```

6. VALIDER
   - Injecter les params dans le compositeur (compose_ga_v10.py)
   - Re-rendre le GA
   - Comparer visuellement: le GA avec params calibres vs sans
   - Si la difference est perceptible et ameliore -> COMMIT
   - Si pas de difference -> les params sont trop faibles, ajuster

SORTIE: calibration_params.yaml + comparaison visuelle before/after
```
