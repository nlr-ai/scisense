# SYNC — vec/calibration

## Status

| Facet | Status | Date |
|-------|--------|------|
| 01_RESULTS | COMPLETE | 2026-03-24 |
| 02_OBJECTIVES | COMPLETE | 2026-03-24 |
| 03_PATTERNS | COMPLETE | 2026-03-24 |
| 04_BEHAVIORS | COMPLETE | 2026-03-24 |
| 05_ALGORITHM | COMPLETE | 2026-03-24 |
| 06_VALIDATION | COMPLETE | 2026-03-24 |
| 07_IMPLEMENTATION | COMPLETE | 2026-03-24 |
| 08_HEALTH | COMPLETE | 2026-03-24 |
| 09_PHENOMENOLOGY | COMPLETE | 2026-03-24 |
| 10_SYNC | ACTIVE | 2026-03-24 |

## Module State

**Phase:** Doc chain complete. Implementation pending.
**Artefacts existants:** S1_sick_contour.svg, S2_healthy_contour.svg, S3_sick_contour.svg, S4_healthy_contour.svg — contours polyline bruts extraits manuellement, pas encore passés par le pipeline Douglas-Peucker / Catmull-Rom / Bezier.
**Scripts:** Aucun script de calibration n'existe encore. Le pipeline est entierement specifie mais non implemente.
**Blockers:** Aucun bloqueur technique. Le pipeline peut etre implemente incrementalement.

## Historique

| Date | Changement | Auteur |
|------|-----------|--------|
| 2026-03-24 | Creation complete du doc chain 10 facets | Silas |

## Remarques / Questions

- Les 4 contours SVG existants (S1-S4) utilisent des polylines `L` (line-to) pas des courbes `C` (cubic Bezier). Ce sont des preuves de concept, pas des sorties pipeline. Le pipeline les remplacera.
- Le parametre epsilon de Douglas-Peucker (facteur_simplification = 0.02) est le seul free constant critique. Il devra etre calibre empiriquement sur les premieres images IA.
- La dependance a Aurore pour HC2 (test empathie) est un goulot d'etranglement humain. Preparer plusieurs contours candidats avant de solliciter son attention.
- L'extraction des parametres integraux (A_CAL8, RC5, HC5) est la partie la plus semi-automatique du module. Elle necessitte un jugement visuel que le code seul ne peut pas fournir.

## Consignes recues

*(Espace reserve pour les instructions live de NLR ou Aurore.)*

## Handoff

**Pour le prochain agent/session:**
1. Les 10 facets sont specifies. Aucun code n'existe encore.
2. Les 4 SVG contours existants sont des polylines brutes — ils ont ete traces manuellement a partir d'images IA (Ideogram). Ils illustrent le concept mais n'ont pas traverse le pipeline algorithmique (find_contours -> Douglas-Peucker -> Catmull-Rom -> Bezier).
3. La Contour Matrix (grille age x vecteur de sante H) est specifiee en 05_ALGORITHM mais pas encore implementee.
4. La priorite d'implementation est: d'abord le pipeline single-image (A_CAL1 -> A_CAL5), puis la Contour Matrix (A_CAL6), puis le seuil d'empathie (A_CAL7).
5. Les points.json intermediaires (S3_sick_points.json, S4_healthy_points.json) n'existent pas encore — ils seront produits par le pipeline.
