# Results — vec/calibration

5 resultats mesurables. Mapping 1:1 avec les HEALTH checkers.

---

## RC1: Contours organiques exploitables

Les silhouettes humaines (enfant malade, enfant sain) et les cellules biologiques (cellules dendritiques, epithelium) sont disponibles sous forme de chemins SVG natifs (cubic Bezier) directement injectables dans le compositeur parametrique (compose_ga_v10.py). Ces contours ne sont pas des polylines brutes — ce sont des courbes lisses, organiques, expressives, qui passent le test de fluidite visuelle a l'oeil nu.

**Sense:** Comparaison visuelle target (image IA source) vs output (contour SVG rendu). Le contour SVG doit etre reconnaissable comme la meme silhouette que l'image IA source, sans artefacts geometriques (angles droits parasites, auto-intersections, segments lineaires visibles).
**Health:** HC1 (gap organique < seuil acceptable — voir 08_HEALTH)
**Carrier:** Silas (verification visuelle automatisee + manuelle)

---

## RC2: Seuil d'empathie clinique atteint

Un pediatre qui voit la silhouette de l'enfant malade (H=0.0) projette immediatement son patient. En moins de 2 secondes, il reconnait un enfant souffrant — pas un stick figure, pas un pictogramme geometrique, pas une forme abstraite. La silhouette declenche la resonance clinique qui ancre tout le GA (B7, PH1).

**Critere:** La silhouette organique extraite declenche la reconnaissance "enfant souffrant" significativement plus vite qu'un pictogramme geometrique equivalent (stick figure, icone standard). Le seuil est qualitatif : Aurore (immunologiste + clinicienne) valide que la projection clinique s'active en <2s.
**Sense:** Test d'empathie — presentation de la silhouette calibree isolee (sans contexte GA) a Aurore. Reponse attendue : "Je vois un enfant malade" vs "Je vois une forme".
**Health:** HC2 (sign-off Aurore empathie)
**Carrier:** Aurore + Silas

---

## RC3: Continuite du vecteur de sante H

La transformation enfant malade (H=0.0) -> enfant sain (H=1.0) est visuellement continue et non un collage de deux silhouettes distinctes. Le compositeur peut generer n'importe quelle posture intermediaire H=0.3, H=0.5, H=0.7 — et chaque intermediaire est aussi organique que les extremes. La continuity du vecteur H est la preuve que la calibration est parametrique et pas discrete.

**Critere:** Pour au moins 5 valeurs de H (0.0, 0.25, 0.5, 0.75, 1.0), la silhouette generee est fluide, sans rupture de continuite, sans artefacts d'interpolation.
**Sense:** Rendu de la sequence H=0.0 -> 1.0 en strip horizontale (5 frames). Verification visuelle : la transformation est un morphing continu, pas un crossfade entre deux images.
**Health:** HC3 (continuite H verifiee — voir 08_HEALTH)
**Carrier:** Silas

---

## RC4: Zero pixel IA dans le livrable

Aucun pixel de l'image IA source ne se retrouve dans le livrable final. Les contours extraits sont des chemins SVG — du code, pas des pixels. L'image IA est un calibrateur ephemere : elle informe la geometrie, puis disparait. Le livrable est 100% vectoriel, 100% libre de droits, 100% reproductible.

**Critere:** Le fichier SVG final ne contient aucune balise `<image>`, aucun `data:image/`, aucun raster embarque. Tous les elements visuels sont des `<path>`, `<circle>`, `<rect>`, `<line>`, `<polygon>` — du code pur.
**Sense:** Grep automatique dans le SVG pour les balises raster.
**Health:** HC4 (zero pixel IA — direct enforcement de VN4)
**Carrier:** Silas (script automatique)

---

## RC5: Calibration multi-dimensionnelle integree

Au-dela des contours (volumes), l'image IA calibre aussi les ratios d'espacement, la densite locale, le poids visuel relatif, les textures, et la tonalite emotionnelle. Ces parametres sont extraits de l'infographie IA et traduits en valeurs YAML injectables dans le compositeur. La calibration n'est pas un pipeline de contours — c'est un pipeline de parametres visuels complets.

**Critere:** Pour chaque image IA traitee, un fichier `calibration_params.yaml` est produit contenant au minimum : ratios d'espacement (margin, gap, padding), densite locale (elements/zone), poids visuel relatif (aire * opacite par element), et tonalite chromatique (hue, saturation, lightness dominantes).
**Sense:** Le fichier YAML existe et ses valeurs sont injectees dans le layout du compositeur.
**Health:** HC5 (parametres calibres presentes — voir 08_HEALTH)
**Carrier:** Silas

---

## Guarantee Loop

```
RC1 (contours organiques)       <- HC1 (gap organique)        <- SC1 (target vs output comparison)
RC2 (seuil empathie)            <- HC2 (sign-off Aurore)       <- SC2 (test empathie isole)
RC3 (continuite H)              <- HC3 (continuite verifiee)   <- SC3 (strip H=0->1)
RC4 (zero pixel IA)             <- HC4 (grep raster)           <- SC4 (grep automatique SVG)
RC5 (calibration integrale)     <- HC5 (params presents)       <- SC5 (YAML existence + injection)
```

## Ce qui n'est pas un RESULT de ce module

- La conformite MDPI du GA (-> vec/editorial, R1)
- La validation scientifique par Aurore (-> vec/audit, R2)
- Le rendu E2E du GA (-> vec/pipeline, H5)
- Le design system visuel (-> vec/design_system)

Ce module produit des **contours et parametres calibres**. Les autres modules les consomment.
