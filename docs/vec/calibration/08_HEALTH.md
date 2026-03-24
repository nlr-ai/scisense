# Health — vec/calibration

5 health checkers: mapping 1:1 avec les 5 results.

```
RC1 (contours organiques)       <- HC1 (gap organique)        <- SC1a-SC1e (5 sense signals)
RC2 (seuil empathie)            <- HC2 (sign-off Aurore)       <- SC2 (test empathie)
RC3 (continuite H)              <- HC3 (continuite verifiee)   <- SC3a-SC3b (2 sense signals)
RC4 (zero pixel IA)             <- HC4 (grep raster)           <- SC4 (grep automatique)
RC5 (calibration integrale)     <- HC5 (params presents)       <- SC5a-SC5b (2 sense signals)
```

---

## HC1: Contours organiques exploitables -> validates RC1

Le contour SVG produit par le pipeline est ferme, sans auto-intersection, organiquement fluide, et suffisamment fidele a la source IA.

### Sense signals

| ID | Signal | Checks | Automation |
|----|--------|--------|------------|
| SC1a | Path ferme | `d` attribut commence par `M`, finit par `Z` | Auto — regex sur SVG |
| SC1b | Zero auto-intersection | Aucun segment Bezier ne croise un segment non-adjacent | Auto — test geometrique (shapely ou custom) |
| SC1c | Zero segment lineaire visible | Courbure non-nulle pour chaque segment Bezier (distance control-point > epsilon au segment droit) | Semi-auto — calcul + verification visuelle |
| SC1d | IoU > 0.80 | Intersection over Union entre masque source et masque contour | Auto — scikit-image regionprops |
| SC1e | Points 15-60 | Nombre de points apres Douglas-Peucker dans la fourchette | Auto — lecture JSON |

**Checker:** Integre dans `calibrate_contour.py` (A_CAL5). Le script refuse de produire le SVG final si un check echoue. Fail Loud : le message d'erreur indique quel check a echoue et avec quelle valeur.

**Carrier:** Silas (automatique pour SC1a-SC1e, verification visuelle finale manuelle).

**Status:** Loop ouverte — script non implemente.

---

## HC2: Seuil d'empathie clinique -> validates RC2

La silhouette H=0.0 declenche la reconnaissance "enfant malade" chez Aurore en <2s, sans contexte.

### Sense signal

| ID | Signal | Method |
|----|--------|--------|
| SC2 | Test empathie Aurore | Presentation de la silhouette isolee (fond neutre, pas de legende). Question : "Qu'est-ce que tu vois?" Reponse attendue : identification spontanee d'un enfant malade. Temps de reaction < 2s. |

**Checker:** Reponse explicite d'Aurore. Pas de silence interprete comme validation. Le test inclut un comparatif avec un stick figure geometrique (meme posture, meme taille) pour valider que le gain organique est reel.

**Carrier:** Aurore.

**Ce que HC2 PASS signifie:**
- La calibration a depasse le seuil purement geometrique
- Le pipeline produit des contours qui encodent la souffrance corporelle, pas juste la posture
- Le module a rempli sa raison d'etre

**Ce que HC2 FAIL signifie:**
- Le contour est trop simplifie (epsilon trop eleve dans Douglas-Peucker)
- Ou le prompt IA n'a pas genere une posture suffisamment expressive
- Ou la courbure Bezier ne capture pas la fluidite necessaire
- Action : recalibrer epsilon, reformuler le prompt, ou augmenter le nombre de points

**Status:** Loop ouverte — GA pas encore presente a Aurore. Priorite haute.

---

## HC3: Continuite du vecteur H -> validates RC3

L'interpolation entre H=0.0 et H=1.0 produit des postures intermediaires naturelles et fluides.

### Sense signals

| ID | Signal | Checks | Automation |
|----|--------|--------|------------|
| SC3a | Strip H continue | 5 frames (H=0.0, 0.25, 0.5, 0.75, 1.0) rendus en strip horizontale. Aucune rupture visible. | Semi-auto — rendu auto, inspection visuelle |
| SC3b | Pas de degenescence intermediaire | Chaque frame intermediaire passe les checks VC1-VC3 (ferme, pas d'auto-intersection, pas de lineaire). | Auto — re-run HC1 checks sur chaque frame |

**Checker:** `calibrate_matrix.py` genere la strip et run les checks VC1-VC3 sur chaque frame. La verification visuelle finale est manuelle.

**Carrier:** Silas.

**Ce que HC3 FAIL signifie:**
- L'interpolation lineaire des points d'ancrage est insuffisante (certaines articulations se croisent aux intermediaires)
- Action : passer a une interpolation spherique (slerp) pour les angles, ou ajouter des contraintes articulaires

**Status:** Loop ouverte — pipeline non implemente.

---

## HC4: Zero pixel IA dans le livrable -> validates RC4

Le SVG final ne contient aucun element raster.

### Sense signal

| ID | Signal | Checks | Automation |
|----|--------|--------|------------|
| SC4 | Grep raster = 0 | `grep -c "<image\|data:image\|xlink:href" livrable.svg` = 0 | Auto — grep |

**Checker:** Automatique. Une seule commande grep. Si le resultat est > 0, le build est bloque. Pas d'exception, pas de cas particulier.

**Carrier:** Silas (integre dans le pipeline de validation, ou dans `validate_ga.py`).

**Note:** Ce check est deja implicite dans le pipeline editorial (vec/editorial, H1, S1e). Le dupliquer ici est delibere — c'est la responsabilite directe du module calibration de ne jamais injecter de raster. La detection en amont (ici) est plus valuable que la detection en aval (editorial).

**Status:** Trivial a implementer. Pas encore formalise dans un script.

---

## HC5: Calibration integrale actionnee -> validates RC5

Les parametres multi-dimensionnels extraits de l'infographie IA sont injectes dans le compositeur et produisent un changement perceptible.

### Sense signals

| ID | Signal | Checks | Automation |
|----|--------|--------|------------|
| SC5a | YAML existe | `calibration_params.yaml` present et parseable | Auto — file exists + yaml.safe_load |
| SC5b | Difference perceptible | Deux rendus GA (avant/apres injection des params) sont visuellement distincts | Semi-auto — rendu auto, comparaison manuelle |

**Checker:** SC5a est automatique. SC5b necessite un jugement visuel — le script peut calculer un SSIM (Structural Similarity Index) entre les deux rendus, mais le verdict final est humain (est-ce que le GA avec params calibres est MEILLEUR?).

**Carrier:** Silas.

**Ce que HC5 FAIL signifie:**
- Les parametres extraits sont trop faibles pour impacter le rendu (valeurs trop proches des defaults)
- Ou l'infographie IA source n'etait pas assez differente du layout actuel
- Action : utiliser une infographie IA plus contrastee, ou augmenter l'amplitude des parametres extraits

**Status:** Loop ouverte — script non implemente. Priorite basse (apres HC1, HC2, HC3).

---

## Open Loops / Escalations

| Loop | Missing link | What's needed | Who | Priority |
|------|-------------|---------------|-----|----------|
| HC1 -> RC1 | Script `calibrate_contour.py` | Implementation du pipeline A_CAL2-A_CAL5 | Silas | HAUTE |
| HC2 -> RC2 | Test empathie Aurore | Contour calibre + envoi a Aurore | Silas + Aurore | HAUTE (apres HC1) |
| HC3 -> RC3 | Script `calibrate_matrix.py` | Implementation de la Contour Matrix A_CAL6 | Silas | MOYENNE |
| HC4 -> RC4 | Grep raster dans pipeline | Ajouter SC4 dans validate_ga.py ou calibrate_contour.py | Silas | BASSE (trivial) |
| HC5 -> RC5 | Script `extract_integral_params.py` | Implementation A_CAL8 | Silas | BASSE |

## Dependance amont

HC1 est le goulot : tant que le pipeline single-image ne produit pas un contour PASS, les autres health checks ne peuvent pas etre executes. HC2 depend d'un contour HC1-PASS. HC3 depend de deux contours HC1-PASS (H=0 et H=1). HC4 est independant mais trivial. HC5 est independant mais basse priorite.

```
HC1 (contour) ──►  HC2 (empathie)
     │
     ├──────────►  HC3 (continuite H) [necessite 2x HC1 PASS]
     │
     └──────────►  HC4 (zero pixel) [independant, trivial]

HC5 (integral) ─── [independant, basse priorite]
```
