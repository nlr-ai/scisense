# Validation — vec/calibration

## Invariants (MUST)

**VC1: Contour ferme.** Tout path SVG produit par le pipeline DOIT etre ferme (commencer par `M`, finir par `Z`). Un contour ouvert est un contour casse — il ne peut pas etre rempli, il ne peut pas etre injecte dans le compositeur. Health: HC1.

**VC2: Contour sans auto-intersection.** Le path SVG ne DOIT pas se croiser lui-meme. Une auto-intersection produit des artefacts de remplissage (zones inversees, trous visuels). Le test est geometrique : aucun segment Bezier ne croise un segment non-adjacent. Health: HC1.

**VC3: Organicite — zero segment lineaire visible.** Le contour final ne DOIT contenir aucun segment qui apparaisse comme une ligne droite a la resolution de livraison (1100x560). Tout segment doit avoir une courbure non-nulle. Un seul segment lineaire visible casse l'illusion organique et ramene le contour a un polygone. Health: HC1.

**VC4: IoU > 0.80 avec la source.** Le contour extrait DOIT capturer au moins 80% de la silhouette source (mesure par Intersection over Union). En dessous de 0.80, le contour deforme trop la forme originale et perd la posture qui encode H. Health: HC1.

**VC5: Nombre de points simplifies 15-60.** Apres Douglas-Peucker, le contour simplifie DOIT contenir entre 15 et 60 points. Moins de 15 = perte de forme critique. Plus de 60 = le Bezier resultant sera trop complexe pour le compositeur et potentiellement bruite. Health: HC1.

**VC6: Empathie clinique <2s.** La silhouette H=0.0 DOIT declencher la reconnaissance "enfant malade" chez un clinicien (proxy: Aurore) en moins de 2 secondes, sans contexte. C'est la raison d'etre du module. Si un stick figure fait aussi bien, le pipeline de calibration n'apporte pas de valeur ajoutee et doit etre repense. Health: HC2.

---

## Invariants (NEVER)

**VCN1: JAMAIS de pixel raster dans le SVG.** Aucune balise `<image>`, aucun `data:image/`, aucun `xlink:href` pointant vers un fichier raster. Le SVG contient exclusivement des elements vectoriels. C'est l'enforcement direct de VN4. Health: HC4.

**VCN2: JAMAIS de contour non-simplifie dans le compositeur.** Le contour brut (sortie de find_contours, centaines de points) ne DOIT jamais etre injecte directement dans le SVG du GA. Il doit toujours passer par Douglas-Peucker + Catmull-Rom avant injection. Injecter le brut produit un SVG massif, lent a rendre, et visuellement bruite.

**VCN3: JAMAIS de prompt technique pour l'image IA.** Le prompt envoye au modele image ne DOIT contenir aucune specification technique (resolution, style, format, "photorealistic", "4k"). Il DOIT etre en langage naturel clinique (P_CAL1). Un prompt technique contraint le reseau neuronal et reduit l'organicite de sa sortie.

**VCN4: JAMAIS d'interpolation de pixels.** L'interpolation entre H=0.0 et H=1.0 se fait au niveau des **points d'ancrage du squelette** (coordonnees), PAS au niveau des pixels (crossfade/morphing image). L'interpolation de pixels est une operation raster qui viole VN4 et produit des artefacts de blending.

---

## Invariants (PIPELINE)

**VC7: Ordre des operations.** Douglas-Peucker DOIT etre applique AVANT Catmull-Rom. Jamais l'inverse. Inverser propage le bruit dans les courbes Bezier et produit des oscillations (P_CAL3). Health: implicite dans le pipeline.

**VC8: Archivage complet.** Chaque execution du pipeline produit un JSON intermediaire contenant : contour brut, contour simplifie, path SVG, parametres (epsilon, IoU), et source. Rien n'est perdu en route. L'historique complet de chaque contour est tracable. Implements P11 (version archival).

**VC9: Source documentee.** Chaque contour SVG dans le compositeur a une chaine de provenance documentee : prompt IA -> image source -> JSON brut -> JSON simplifie -> SVG. Si un maillon est manquant, la provenance est cassee et le contour ne peut pas etre verifie. Implements P9, V11.

---

## Checklist de validation pre-injection

Avant d'injecter un contour dans le compositeur (`compose_ga_v10.py`), verifier :

| # | Check | Critere | Auto/Manuel |
|---|-------|---------|-------------|
| 1 | Path ferme | `d` commence par M, finit par Z | Auto |
| 2 | Zero auto-intersection | Aucun croisement non-adjacent | Auto |
| 3 | Zero segment lineaire visible | Courbure non-nulle partout | Semi-auto |
| 4 | IoU > 0.80 | Mesure vs source IA | Auto |
| 5 | Points 15-60 | Count apres Douglas-Peucker | Auto |
| 6 | Zero pixel raster | Grep `<image>` et `data:image` = 0 | Auto |
| 7 | Source documentee | JSON intermediaire existe et est complet | Auto |
| 8 | Empathie <2s | Test Aurore | Manuel |
