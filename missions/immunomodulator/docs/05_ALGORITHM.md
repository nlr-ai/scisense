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

## A5-A10: VEC Engine Algorithms

These algorithms are now maintained in the VEC module doc chain:
- A5 (Pipeline E2E) → `docs/vec/pipeline/05_ALGORITHM.md`
- A6 (Choix d'outil de rendu) → `docs/vec/pipeline/05_ALGORITHM.md`
- A7 (Compositeur paramétrique) → `docs/vec/pipeline/05_ALGORITHM.md`
- A8 (Phase Concept ASCII) → `docs/vec/orchestration/05_ALGORITHM.md`
- A9 (Phase Audit NotebookLM) → `docs/vec/audit/05_ALGORITHM.md`
- A10 (7 intelligences) → `docs/vec/orchestration/05_ALGORITHM.md`
