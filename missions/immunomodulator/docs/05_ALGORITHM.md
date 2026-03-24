# Algorithm — Mission Immunomodulateur GA

## A1: Boucle d'itération autonome (par agent)

```
ENTRÉE: axe de variation assigné + état actuel du GA + MISSION.md + GA_SPEC.md

1. PRODUIRE
   - Lire GA_SPEC.md pour les contraintes (Zone 1/2/3, palette, budget texte)
   - Générer le wireframe SVG selon l'axe assigné
   - Rendre en PNG (3300×1680 full + 1100×560 delivery)

2. DOCUMENTER
   - Écrire ce qui a été fait et pourquoi dans un fichier axe_N_notes.md
   - Lister les choix de design et leurs justifications scientifiques

3. AUTO-CRITIQUER (3 filtres)
   Filtre A — Conformité MDPI:
     - ratio OK? mots ≤ 27? pas de titre/affil? ≠ Fig1? ≠ Fig2? libre droits?
   Filtre B — Fidélité scientifique:
     - 4 produits distincts? hiérarchie preuves? axe gut-lung CRL1505?
   Filtre C — Impact cognitif:
     - reconnaissance douleur Zone 1? aha 3s? espace respire? mobile lisible?

4. DÉCIDER
   Si les 3 filtres PASS → SORTIR avec verdict PASS
   Si un filtre FAIL et la correction est technique → CORRIGER et retour à 1
   Si un filtre FAIL et nécessite jugement humain → SORTIR avec verdict NEEDS_FEEDBACK + question précise

SORTIE: wireframe + notes + verdict (PASS | NEEDS_FEEDBACK)
```

## A2: Orchestration des 3 agents parallèles

```
ENTRÉE: feedback Aurore (ou état initial)

1. DIAGNOSTIC — identifier l'obstacle cognitif principal
2. DÉCLARER 3 AXES — 3 variables pertinentes, justifier
3. LANCER 3 agents en parallèle (chacun exécute A1)
4. ATTENDRE convergence des 3 agents
5. COMPARER les 3 résultats
6. Si les 3 sont PASS → présenter à Aurore pour choix
   Si certains NEEDS_FEEDBACK → consolider les questions
7. BOUCLE avec le feedback

SORTIE: 3 wireframes documentés + comparaison + recommandation
```

## A3: Contenu par zone (référence)

Voir → `GA_SPEC.md` sections 2.2, 2.3, 2.4 pour le contenu exact de chaque zone.
Ne pas dupliquer ici.

## A4: Validation pré-soumission

```
ENTRÉE: GA final (PNG 1100×560) + extracted_references.txt

1. VÉRIFIER CONFORMITÉ MDPI
   - Dimensions ≥ 560×1100 (V1)
   - Comptage mots ≤ 30 (V3)
   - Absence titre/affiliations/refs (V2)
   - Non-redondance Fig1/Fig2 (V4)
   - Lisibilité 50% zoom (V7)
   - Libre de droits (V6)

2. VÉRIFIER FIDÉLITÉ SCIENTIFIQUE
   - Hiérarchie preuves correcte (V5)
   - 4 produits distincts présents
   - Pas de cytokines (VN3)
   - Pas de schéma fabrication (VN2)

3. VÉRIFIER RÉFÉRENCES
   - Comptage = 124
   - Format MDPI conforme
   - Pas de doublons

4. DÉCIDER
   Si tout PASS → soumission à Aurore pour approbation finale
   Si FAIL → corriger et retour à 1

SORTIE: dossier soumission (GA PNG + références) ou liste de corrections
```

Delivers R1 (GA conforme MDPI), R3 (références formatées), and feeds into R4 (acceptation Mindy Ma).

## A5: Pipeline de rendu E2E (par itération)
> **Note:** A5 est désormais appelé par A7 (compositeur paramétrique). Le pipeline reste le même, mais l'entrée est `compose_ga.py` au lieu d'un script monolithique.

Chaque itération (A1 step 1 "PRODUIRE") exécute ce pipeline complet. Pas de rendu partiel.

```
ENTRÉE: script Python generate_wireframe_vN.py

1. GÉNÉRER SVG
   - svgwrite produit le .svg vectoriel
   - Validation: fichier non-vide, parseable

2. RENDRE FULL RES
   - svglib + reportlab → PNG 3300×1680
   - Fallback si svglib échoue: Pillow resize depuis un rendu alternatif
   - Validation: dimensions correctes, fichier > 50 KB

3. RENDRE DELIVERY
   - Pillow resize LANCZOS → PNG 1100×560 (depuis full res, pas depuis SVG)
   - Raison: svglib casse au downscale (bug v3). Pillow resize est fiable.
   - Validation: dimensions correctes, fichier > 5 KB, PAS blanc

4. TEST LISIBILITÉ
   - Pillow resize → 550×280 (50% de delivery = test V7)
   - Vérification visuelle: tous les labels lisibles?
   - Si non → augmenter font size ou simplifier et retour à 1

5. AUTO-CHECK PALETTE
   - Grep dans le SVG pour les 4 hex codes produits (#2563EB, #0D9488, #7C3AED, #059669)
   - Si un manque → Fail Loud

6. ARCHIVER
   - Copier les 3 fichiers (svg, full, delivery) dans artefacts/wireframes/ avec numéro de version
   - Ne jamais écraser un artefact existant (P11)

SORTIE: 3 fichiers archivés + résultat auto-check (PASS/FAIL par signal)
```

Implements P8 (E2E), P10 (multi-résolution), P11 (version archival). Health: H5.

## A6: Choix d'outil de rendu final

Le rendu final pour soumission à MDPI nécessite un niveau de qualité publication. Le pipeline SVG programmatique (svgwrite) produit des wireframes de travail mais pas des visuels publication-ready.

```
DÉCISION À PRENDRE (escalation):

Option 1: SVG pur poussé au max
  + 100% libre de droits (V6), 100% reproductible, versionnable
  + Tout est code, modifiable par Silas
  - Limité pour l'anatomie réaliste et le line art médical
  - Résultat "schématique", risque de paraître amateur pour un Q2

Option 2: SVG base + Figma/Inkscape finition
  + Le code pose la structure, l'outil vectoriel ajoute le polish
  + Rendu pro
  - Nécessite intervention manuelle d'Aurore ou NLR
  - Perd la reproductibilité automatique

Option 3: SVG wireframe → prompt guidé → génération IA → nettoyage vectoriel
  + Visuels potentiellement frappants
  - VN4 interdit les éléments IA dans le livrable final
  - Copyright ambigu (V6)
  - Résultat non-reproductible

Option 4: BioRender
  + Éléments biomédicaux professionnels, style publication
  - Licence commerciale à vérifier (V6)
  - Coût
  - Dépendance externe

RECOMMANDATION: Option 1 pour les itérations + Option 2 pour la finition.
Le code SVG reste la source de vérité. Aurore/NLR font le polish final
dans Inkscape si le rendu SVG pur n'atteint pas le Q2 standard.

STATUS: Non tranché. NEEDS_FEEDBACK NLR/Aurore.
```

## A7: Compositeur paramétrique (compose_ga.py)

Replaces A1 step 1 "PRODUIRE" for future iterations. The autonomous agents (A1, A2) now call A7 instead of writing monolithic scripts.

```
ENTRÉE: config/*.yaml + assets/*.svg

1. CHARGER CONFIG
   - palette.yaml → couleurs
   - layout.yaml → positions, tailles, gaps
   - content.yaml → labels (budget mots vérifié)

2. CRÉER CANVAS (3300×1680)

3. DESSINER INFRASTRUCTURE
   - Fonds par zone (gradient ou plat, depuis palette)
   - Mur de briques continu (gaps depuis layout.z1_gaps)
   - PMBL repair bricks (positions depuis layout.z2_repair_bricks)
   - Briques saines Z3 (toutes présentes, couleur healthy)
   - Cercle vicieux (stations depuis layout.vicious_cycle)
   - Blocs 3D évidence (widths depuis layout.evidence_blocks)
   - Labels (depuis content.yaml)

4. INJECTER ASSETS
   Pour chaque element dans layout.elements:
     - Lire le SVG snippet depuis assets/
     - Remplacer currentColor par la couleur de palette
     - Envelopper dans <g transform="translate(x,y) scale(s)">
     - Insérer dans le document

5. SAUVER SVG

6. RENDRE PNG (A5 pipeline: full via svglib, delivery via Pillow resize)

7. AUTO-CHECK (H1 + H5)
   - Dimensions, word count, palette grep, delivery non-blank

SORTIE: wireframe_GA_vN.svg + _full.png + _delivery.png
```
