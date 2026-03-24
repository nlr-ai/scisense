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
> **Note:** A5 est désormais appelé par A7 (compositeur paramétrique). Le pipeline reste le même, mais l'entrée est `compose_ga_v10.py` au lieu d'un script monolithique.

Chaque itération (A1 step 1 "PRODUIRE") exécute ce pipeline complet. Pas de rendu partiel.

```
ENTRÉE: script Python compose_ga_v10.py

1. GÉNÉRER SVG
   - svgwrite produit le .svg vectoriel
   - Validation: fichier non-vide, parseable

2. RENDRE FULL RES
   - Playwright HTML wrapper → PNG 3300×1680
   - Méthode: SVG enveloppé dans un HTML minimal, rendu via Playwright
     à la taille de livraison avec 2x device_scale_factor (= 600 DPI effectif)
   - Validation: dimensions correctes, fichier > 50 KB

3. RENDRE DELIVERY
   - Pillow resize LANCZOS → PNG 1100×560 (depuis full res, pas depuis SVG)
   - Validation: dimensions correctes, fichier > 5 KB, PAS blanc
   - Métadonnée DPI: 600 DPI inscrit dans le PNG delivery

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

SORTIE: wireframe_GA_v10.svg + wireframe_GA_v10_full.png + wireframe_GA_v10_delivery.png
        + résultat auto-check (PASS/FAIL par signal)
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

## A7: Compositeur paramétrique (compose_ga_v10.py)

Replaces A1 step 1 "PRODUIRE" for future iterations. The autonomous agents (A1, A2) now call A7 instead of writing monolithic scripts.

Architecture V10: 4 bandes anatomiques (lumen, épithélium, lamina propria, muscle lisse) remplacent le modèle brick wall + zones. Tout est généré paramétriquement — pas d'injection d'assets SVG externes.

```
ENTRÉE: config/layout_v10.yaml + config/palette.yaml + config/content.yaml

1. CHARGER CONFIG
   - palette.yaml → couleurs (bandes, produits, cycle, fond)
   - layout_v10.yaml → positions, tailles, gaps, géométrie des 4 bandes
   - content.yaml → labels (budget mots vérifié)

2. CRÉER CANVAS (3300×1680)

3. DESSINER (séquence stricte)
   a. Background gradient (palette.background)
   b. Cadre bronche (bronchus frame — contour anatomique principal)
   c. 4 bandes anatomiques:
      - Lumen (cavité, fond clair)
      - Épithélium (couche cellulaire, contours paramétriques)
      - Lamina propria (tissu conjonctif, zone d'action principale)
      - Muscle lisse (couche externe)
   d. Contours enfants (children contours — éléments cellulaires dans chaque bande)
   e. Cercle vicieux (stations depuis layout_v10.vicious_cycle)
   f. Barres d'évidence (evidence bars, widths depuis layout_v10.evidence_bars)
   g. Relais CRL1505 (flèche/mécanisme d'action)
   h. Légende (legend — produits, couleurs, symboles)

4. SAUVER SVG

5. RENDRE PNG (A5 pipeline: full via Playwright HTML wrapper, delivery via Pillow resize)

6. AUTO-CHECK (H1 + H5)
   - Dimensions, word count, palette grep, delivery non-blank

SORTIE: wireframe_GA_v10.svg + wireframe_GA_v10_full.png + wireframe_GA_v10_delivery.png
```

## A8: Phase CONCEPT ASCII (P24)

Avant toute compilation code, une phase concept en ASCII permet de valider la direction avec Aurore sans investir de temps de développement.

```
1. DIAGNOSTIC
   - Identifier l'obstacle cognitif principal du lecteur
   - Formuler en une phrase ce que le GA doit résoudre visuellement

2. AXES DE VARIATION (P2)
   - Définir 3 variables indépendantes (ex: métaphore visuelle, flux de lecture, granularité anatomique)
   - Chaque axe produit une proposition distincte

3. 3 PROPOSITIONS ASCII
   - Pour chaque axe: dessiner le layout + flow en ASCII art
   - Pas de code, pas de SVG — uniquement la structure spatiale et le parcours visuel
   - Annoter les zones (bandes, cycle, évidence, légende)

4. PDF GENERATION
   - Script: generate_proposal_pdf.py (reportlab)
   - Produit un PDF propre avec les 3 propositions ASCII + annotations
   - Inclut le diagnostic et la justification de chaque axe

5. VÉRIFICATION VISUELLE (P25)
   - Read le PDF généré avant envoi — vérifier lisibilité et cohérence
   - Si illisible → corriger et régénérer

6. ENVOI AURORE
   - Envoyer le PDF via MCP (send) pour GO/NO-GO
   - Question explicite: "Quelle direction te parle le plus?"

7. FEEDBACK
   - Si GO → procéder à la compilation (A7)
   - Si NO → re-diagnostiquer (retour à étape 1) avec le feedback intégré

SORTIE: PDF concept + décision GO/NO-GO d'Aurore
```

## A9: Phase AUDIT NotebookLM

Cycle d'audit externe via NotebookLM pour valider la cohérence scientifique et visuelle avant livraison.

```
1. EXPORT
   - python export_notebooklm.py
   - Crée un répertoire plat S0N/ contenant tous les fichiers sources
     (docs, specs, configs, artefacts — 17+ fichiers)

2. UPLOAD
   - Charger les fichiers S0N/ dans NotebookLM
   - Charger le system prompt: config/notebooklm_system_prompt.md (V2.4)

3. AUDIT REQUEST
   - NotebookLM analyse l'ensemble et retourne:
     a. Problèmes identifiés (incohérences, gaps, erreurs)
     b. Patterns applicables (P1-P25, B1-B8) avec justification
     c. Suggestions concrètes d'amélioration

4. OUTPUT FORMS
   - NotebookLM peut produire plusieurs formats:
     a. Report (analyse textuelle détaillée)
     b. Slide deck (SD1/SD2/SD3...) — présentations thématiques
     c. Podcast (audio synthétique pour exploration)
     d. Infographic (résumé visuel des findings)

5. INTEGRATION
   - Silas lit l'output et traduit en:
     a. Corrections code (compose_ga_v10.py, configs)
     b. Mises à jour documentation (doc chain)
     c. Nouveaux patterns ou behaviors si découverte

6. SUB-AGENTS (optionnel)
   - Lancer des sous-agents spécialisés pour exploration ciblée:
     a. Angle immunologie (validation mécanismes, hiérarchie preuves)
     b. Angle communication visuelle (lisibilité, impact cognitif)
     c. Matrice produit-mécanisme (couverture et cohérence des 4 produits)

SORTIE: rapport d'audit + corrections intégrées + documentation mise à jour
```

## A10: Les 7 formes d'intelligence

Chaque phase du processus mobilise une ou plusieurs formes d'intelligence. Aucune n'est substituable par une autre.

| ID | Intelligence | Capacité | Phases d'utilisation |
|----|-------------|----------|---------------------|
| I1 | **Aurore** | Validation clinique, jugement esthétique, expertise domaine | Phase CONCEPT (A8) + VALIDATION (A4) |
| I2 | **NLR** | Architecture, process, system design, arbitrage structurel | Phase CONCEPT (A8) + tout pivot architectural |
| I3 | **NotebookLM** | Analyse profonde, synthèse multi-sources → outputs: infographic, slide deck, podcast, report | Phase AUDIT (A9) |
| I4 | **Silas** | Code, SVG, PDF, documentation, orchestration, sous-agents | Toutes les phases |
| I5 | **AI Image models** (Ideogram/Gemini) | Extraction de contours organiques, calibration phénoménologique | Phase CALIBRATION |
| I6 | **Sub-agents** | Exploration spécialisée avec angle/prompt spécifique | Phase AUDIT (A9) |
| I7 | **Scripts** | Validation automatisée: validate_ga.py, export_notebooklm.py, transcribe_podcast.py | Phase COMPILATION (A7) + AUDIT (A9) |
