# Patterns — vec/calibration

Les patterns de calibration sont derives des patterns mission (03_PATTERNS.md). Ce document les contextualise pour le pipeline contour + calibration integrale.

---

## P12 applique: L'IA est l'accelerateur, le code est le produit

L'image IA n'est jamais un livrable. C'est un **oracle visuel** — on lui pose une question ("a quoi ressemble un enfant de 4 ans recroqueville par la toux?") et elle repond avec une richesse organique qu'aucun squelette parametrique ne peut atteindre seul. Le pipeline calibration extrait cette richesse et la convertit en geometrie pure.

```
Question en langage naturel (prompt)
    -> Image IA (pixels, ephemere)
        -> Pipeline extraction (scikit-image, Douglas-Peucker, Catmull-Rom)
            -> Path SVG (code, permanent)
                -> Compositeur parametrique (inject dans compose_ga_v10.py)
```

L'image IA a la meme relation au livrable qu'un brouillon papier a une these : elle informe, elle n'est pas publiee.

---

## P15 applique: Le vecteur de sante H gouverne la posture

Chaque silhouette extraite est indexee par sa valeur H. Le pipeline ne produit pas "une silhouette malade" et "une silhouette saine" — il produit **deux extremes d'une fonction continue**.

| H | Posture | Colonne vertebrale | Tete | Bras | Jambes |
|---|---------|-------------------|------|------|--------|
| 0.0 | Recroqueville | Flexion thoracique 30-40deg | Penchee avant, regard au sol | Tombants, colles au corps, main(s) a la poitrine (toux) | Rapprochees, genoux legerement flechis |
| 0.5 | Neutre/transition | Legere flexion 10-15deg | Droite, regard horizontal | Le long du corps, detendus | Ecartees, genoux droits |
| 1.0 | Epanoui | Extension, epaules ouvertes | Levee, regard vers le haut | Ouverts, ecartes du corps (celebration) | Ecartees, stable, ancree |

L'interpolation entre ces etats est gouvernee par les points d'ancrage du squelette parametrique (P16). Chaque point est une fonction lineaire de H :

```
point_x(H) = sick_x + H * (healthy_x - sick_x)
point_y(H) = sick_y + H * (healthy_y - sick_y)
```

L'enveloppe organique (Bezier cubique) est recalculee a chaque valeur de H.

---

## P16 applique: Cinematique posturale — le squelette sous la peau

Le contour organique n'est pas dessine directement. Il est **derive** d'un squelette de 8-10 points d'ancrage anatomiques :

```
         [tete]
           |
         [C7] (vertebre cervicale 7)
        /     \
  [epaule_G]  [epaule_D]
      |            |
  [coude_G]   [coude_D]
      |            |
  [poignet_G] [poignet_D]
        \     /
        [bassin]
        /     \
  [genou_G]  [genou_D]
      |            |
  [cheville_G] [cheville_D]
```

Chaque point a des coordonnees (x, y) qui sont fonctions de H. Le pipeline fonctionne en 2 couches :

1. **Couche squelette :** Les points d'ancrage definissent la posture. Ils viennent soit des coordonnees extraites de l'image IA (calibration), soit de valeurs interpolees (generation parametrique).

2. **Couche enveloppe :** L'algorithme Catmull-Rom -> Bezier cubique genere une courbe lisse qui "habille" le squelette. Les distances du contour aux points d'ancrage definissent la morphologie (epaisseur des membres, volume du torse, courbure de la tete).

Le squelette est le signal — l'enveloppe est le rendu.

---

## P17 applique: Calibration integrale — le multi-dimensionnel

L'infographie IA (NotebookLM, Ideogram, Gemini) n'est pas un calibrateur de contours uniquement. Elle produit une **reponse visuelle integree** a la question posee. Cette reponse encode des dimensions que le pipeline contour seul ne capture pas :

| Dimension | Ce qu'on extrait | Comment | Destination YAML |
|-----------|-----------------|---------|-----------------|
| **Volumes** | Contours organiques | Pipeline scikit-image (automatique) | `children.contours` |
| **Couleurs en contexte** | Palette dominante, temperature, saturation | Analyse histogramme (semi-auto) | `palette.yaml` refinement |
| **Espacements** | Ratios margin/gap/padding entre elements | Mesure manuelle sur l'infographie | `layout.spacing` |
| **Densite locale** | Nombre d'elements par zone | Comptage visuel | `layout.density` |
| **Poids visuel** | Aire * opacite * contraste par element | Estimation visuelle | `layout.weights` |
| **Espace negatif** | Ratio vide/plein par zone | Mesure manuelle | `layout.negative_space` |
| **Hierarchie de lecture** | Ordre dans lequel l'oeil parcourt l'image | Observation + inference | `layout.reading_order` |
| **Tonalite emotionnelle** | Chaleureuse/froide, grave/legere | Jugement qualitatif | `palette.emotional_tone` |

Les dimensions "Volumes" sont automatisees. Toutes les autres sont **semi-automatiques** : le pipeline propose une valeur, Silas valide et ajuste. C'est un trade-off explicite (O_CAL5).

---

## P_CAL1: Prompt engineering pour images IA — zero contrainte technique

Le prompt envoye au modele image (Ideogram, Gemini) doit etre en **langage naturel clinique**. Pas de specifications techniques (resolution, style, format). Pas de jargon IA ("photorealistic, 4k, cinematic lighting"). Le modele produit sa meilleure reponse quand il est libre de choisir sa propre representation.

**Bon prompt:**
> "Un enfant de 4 ans recroqueville sur lui-meme, toussant, les yeux brillants de fievre. Sa mere le tient contre elle. On sent l'epuisement des infections repetees — c'est le cinquieme episode cette annee. L'image doit faire ressentir la fatigue chronique, pas l'urgence aigue."

**Mauvais prompt:**
> "Illustration medicale d'un enfant toussant, style line art, fond blanc, resolution 1024x1024, pas de texte."

Le mauvais prompt contraint le reseau neuronal dans un espace de solutions etroit. Le bon prompt lui donne un **contexte emotionnel riche** et le laisse trouver la forme optimale. C'est cette forme — non contrainte, emergente — qui porte l'organicite que le pipeline doit ensuite extraire.

**Attention:** Le prompt doit decrire la **charge physique et emotionnelle** de l'etat clinique, pas ses symptomes techniques. "Infections respiratoires recurrentes" ne provoque rien. "Cinquieme episode cette annee, sa mere est epuisee" provoque une image.

---

## P_CAL2: La Contour Matrix — exploration systematique

La calibration n'est pas un one-shot. C'est une **grille d'exploration** :

```
           H=0.0 (malade)    H=0.5 (transition)    H=1.0 (sain)
Age 2-3    [prompt_a1]        [interpole]            [prompt_a2]
Age 4-6    [prompt_b1]        [interpole]            [prompt_b2]
Age 7-10   [prompt_c1]        [interpole]            [prompt_c2]
```

Chaque cellule contient un prompt, une image IA, et un contour extrait. Les intermediaires (H=0.5) sont interpoles, pas generes par IA — c'est le test de continuite de RC3.

La matrice permet de :
- Comparer la robustesse du pipeline sur differentes morphologies (ages differents)
- Choisir la tranche d'age la plus expressive pour le GA final
- Valider que le vecteur H est coherent a travers les morphologies

La matrice est une grille de calibration, pas un catalogue d'assets. On en choisit un seul contour final pour le GA.

---

## P_CAL3: Douglas-Peucker AVANT Catmull-Rom — simplifier avant de lisser

L'ordre des operations est critique :

```
FAUX: find_contours -> Catmull-Rom (lisse le bruit)
JUSTE: find_contours -> Douglas-Peucker (elimine le bruit) -> Catmull-Rom (lisse le signal)
```

Douglas-Peucker reduit un contour de 500 points a 30-50 points en eliminant les points qui contribuent moins de epsilon a la forme. C'est un filtre passe-bas geometrique. Si on lisse avant de simplifier, on propage le bruit dans les courbes Bezier et on obtient des oscillations parasites.

Le parametre epsilon de Douglas-Peucker est le seul free constant critique du pipeline. Il doit etre calibre empiriquement : trop petit = trop de details, artefacts de pixelisation. Trop grand = perte de la forme organique. La valeur de reference pour les silhouettes enfant est ~2-5% du perimetre du contour.

---

## P_CAL4: Catmull-Rom -> Bezier cubique — la mathematique de l'organicite

Catmull-Rom est un spline d'interpolation qui passe par tous les points de controle (contrairement au Bezier qui ne passe que par les extremites). C'est exactement ce qu'on veut : la courbe epouse les points du contour simplifie.

La conversion Catmull-Rom -> Bezier cubique est analytique (pas une approximation) :

```
Pour chaque segment (P0, P1, P2, P3):
    CP1 = P1 + (P2 - P0) / 6
    CP2 = P2 - (P3 - P1) / 6
    -> Bezier cubique de P1 a P2 avec control points CP1, CP2
```

Le resultat est un path SVG natif (`<path d="M ... C ... C ... Z"/>`) directement injectable dans le compositeur. Pas de dependance externe, pas de rasterisation, pas de pixel.

Ce path est **du code**. Il peut etre versionne, diff-e, parametrise. C'est la materialisation de VN4 : zero pixel IA dans le livrable.
