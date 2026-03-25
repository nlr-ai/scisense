# Health — vec/design_system

4 health checkers propres au design system + 2 checkers herites de la mission (H7, H8).

```
DS-R1 (coherence chromatique)     ← DS-H1 (palette + couleur)       ← DS-S1a-c (3 sense signals)
DS-R2 (impact cognitif PH1)      ← DS-H2 (test PH1 3s)            ← DS-S2a-c (3 sense signals)
DS-R3 (convergence IgA)          ← H7    (convergence)             ← S7a-b   (2 sense signals)
DS-R4 (fracture cycle)           ← H8    (cycle fracture)          ← S8a-b   (2 sense signals)
DS-R5 (hierarchie typographique) ← DS-H3 (typo check)             ← DS-S3a-d (4 sense signals)
DS-R6 (equilibre spatial)        ← DS-H4 (spatial check)          ← DS-S4a-d (4 sense signals)
```

---

## DS-H1: Coherence chromatique → validates DS-R1

La palette canonique est respectee dans le SVG. Les couleurs-produit sont constantes et exclusives. Le rouge est reserve au pathologique.

### Sense signals

| ID | Signal | Checks | Automation |
|----|--------|--------|------------|
| DS-S1a | 5 hex produit presents | Grep #2563EB, #0D9488, #7C3AED, #059669, #DC2626 dans le SVG | Auto — grep dans SVG |
| DS-S1b | Rouge exclusivement pathologique | Aucun element positif/neutre n'utilise #DC2626 ou ses derives | Semi-auto — grep + review contexte |
| DS-S1c | Pas de couleur parasite saturee | Toutes les couleurs saturees du SVG sont dans la palette autorisee | Auto — extraction couleurs + comparaison |

**Checker:** Integre dans `validate_ga.py` (palette sub-check existant) + extensions DS-A1.

**Carrier:** Silas (auto-check).

**Status:** Partiellement implemente — le grep des 4 hex produit est dans validate_ga.py. Les checks DS-S1b (contexte rouge) et DS-S1c (couleurs parasites) a ajouter.

---

## DS-H2: Test PH1 3 secondes → validates DS-R2

Le GA declenche la sequence perceptive complete (scan → identification → comprehension) en 3 secondes sur ecran mobile.

### Sense signals

| ID | Signal | Checks | Automation |
|----|--------|--------|------------|
| DS-S2a | Gate 1 — scan 1s | Transition chromatique rouge→vert perceptible en 1 seconde sur PNG 50% | Manuel — verification visuelle |
| DS-GLANCE | Gate 2 — identification 2s | ≥ 3 elements reconnus (virus, voie respiratoire, enfant, "Wheezing/Asthma") en 2 secondes | Manuel — verification visuelle |
| DS-S2c | Gate 3 — comprehension 3s | 4 agents colores + convergence + gradient de preuves compris en 3 secondes | Manuel — verification visuelle |

**Checker:** Protocole DS-A2 (test d'impact cognitif PH1). Execute par Silas a chaque iteration. Valide par Aurore pour le sign-off final (H2).

**Carrier:** Silas (execution protocole) + Aurore (validation clinique).

**Status:** Loop ouverte — protocole defini, a executer sur V10.2.

---

## H7: Convergence IgA → validates DS-R3, B8

Les 4 flux-produits convergent vers un point focal unique dans le lumen.

### Sense signals

| ID | Signal | Checks | Automation |
|----|--------|--------|------------|
| S7a | 4 lignes de convergence colorees | 4 lignes visibles dans la bande lumen, chacune d'une couleur produit distincte (#2563EB, #0D9488, #7C3AED, #059669) | Semi-auto — verification visuelle + SVG parse |
| S7b | Formes Y IgA au point focal | Formes Y (~15px) regroupees au point de convergence, dans le lumen apical | Semi-auto — verification visuelle |

**Checker:** Protocole DS-A4 (verification convergence IgA).

**Carrier:** Silas (verification visuelle) + NotebookLM (audit).

**Status:** Loop ouverte — convergence IgA a implementer dans V10.2 (prochaine action).

---

## H8: Cycle fracture → validates DS-R4, B4

La rupture du cercle vicieux par la lance verte est visuellement explicite.

### Sense signals

| ID | Signal | Checks | Automation |
|----|--------|--------|------------|
| S8a | Lance verte brise le cycle rouge | Element vert traversant physiquement le cercle vicieux rouge | Semi-auto — verification visuelle |
| S8b | Marques de fracture au point d'impact | Eclats ou lignes de rupture visibles a l'endroit de la traversee | Semi-auto — verification visuelle |

**Checker:** Protocole DS-A5 (verification fracture du cycle).

**Carrier:** Silas (verification visuelle) + Aurore.

**Status:** Loop ouverte — fracture a implementer dans V10.2 (prochaine action).

---

## DS-H3: Hierarchie typographique → validates DS-R5

Les 30 mots sont distribues en 3 niveaux avec les font-sizes correctes et la lisibilite a 50% zoom.

### Sense signals

| ID | Signal | Checks | Automation |
|----|--------|--------|------------|
| DS-S3a | Word count ≤ 30 | Parse SVG `<text>` elements, count words | Auto — integre dans validate_ga.py (S1b) |
| DS-S3b | Font-sizes par niveau | Niveau 1 >= 32, Niveau 2 in [24-30], Niveau 3 in [18-22] (format 3x) | Auto — parse SVG font-size attributes |
| DS-S3c | Niveau 1 hors bronche | Les labels de Niveau 1 sont positionnes en dehors du cadre bronche | Semi-auto — SVG coordinates vs bronche bbox |
| DS-S3d | Lisibilite V7 tous niveaux | Tous les niveaux presents sont lisibles a 550x280 | Manuel — verification visuelle |

**Checker:** Partiellement dans validate_ga.py (S1b = word count). DS-S3b et DS-S3c a ajouter.

**Carrier:** Silas (auto-check + verification visuelle).

**Status:** Partiellement implemente. Word count OK. Font-size check et placement check a ajouter.

---

## DS-H4: Equilibre spatial → validates DS-R6

Densite, espace negatif, poids visuel et flux de lecture sont equilibres.

### Sense signals

| ID | Signal | Checks | Automation |
|----|--------|--------|------------|
| DS-S4a | Gradient de densite L→R | Z1 faible < Z3 moyenne < Z2 haute | Semi-auto — count elements par zone |
| DS-S4b | Lumen > 60% vide | Surface occupee du lumen < 40% de l'aire totale de la bande | Semi-auto — aire elements vs aire bande |
| DS-S4c | Respiration 5% | Aucun element majeur ne touche un bord ou un voisin sans padding | Semi-auto — bounding box analysis |
| DS-S4d | Hierarchie poids visuel | enfants > bronche > evidence_bars > cycle > legende > arc_crl1505 | Manuel — estimation visuelle |

**Checker:** Protocole DS-A3 (validation spatiale multi-critere). Principalement manuel avec aide SVG parse.

**Carrier:** Silas (verification visuelle) + NotebookLM (audit spatial).

**Status:** Loop ouverte — protocole defini, a executer sur V10.2.

---

## Open loops / Escalations

| Loop | Missing link | What's needed | Who | Status |
|------|-------------|---------------|-----|--------|
| DS-H1 → DS-R1 | DS-S1b, DS-S1c | Ajouter checks contexte rouge + couleurs parasites dans validate_ga.py | Silas | A faire |
| DS-H2 → DS-R2 | Protocole non execute | Executer DS-A2 sur chaque wireframe a partir de V10.2 | Silas + Aurore | Ouvert |
| H7 → DS-R3 | Convergence non implementee | Implementer draw_convergence_iga() dans compose_ga.py | Silas | Prochaine action |
| H8 → DS-R4 | Fracture non implementee | Implementer draw_health_lance() dans compose_ga.py | Silas | Prochaine action |
| DS-H3 → DS-R5 | DS-S3b, DS-S3c | Ajouter checks font-size et placement dans validate_ga.py | Silas | A faire |
| DS-H4 → DS-R6 | Protocole non execute | Executer DS-A3 sur chaque wireframe a partir de V10.2 | Silas + NotebookLM | Ouvert |
