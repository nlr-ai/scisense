# Implementation — vec/design_system

## DS-I1: Fichiers du design system

| Fichier | Role | Ref |
|---------|------|-----|
| `config/palette.yaml` | Palette canonique (5 couleurs produit + neutres + fonds) — single source of truth | P7, B5, DS-V1 |
| `config/layout.yaml` | Positions, tailles, proportions des 4 bandes, zones 27/46/27, marges | P29, P30, DS-V8 |
| `config/content.yaml` | Labels avec niveaux typographiques (1/2/3), budget mots | P28, DS-V4 |
| `scripts/compose_ga.py` | Compositeur parametrique — lit les 3 configs, genere le SVG | A7 |
| `scripts/validate_ga.py` | Tribunal editorial — verifie H1 (conformite MDPI) incluant palette sub-check | DS-A1 |
| `docs/vec/design_system/` | Ce module — 10 facets du design system | |

## DS-I2: Structure de palette.yaml

```yaml
# palette.yaml — Single Source of Truth pour les couleurs
products:
  om85: "#2563EB"       # Bleu — 18 RCTs, ancre dominante
  pmbl: "#0D9488"       # Teal — 5 RCTs
  mv130: "#7C3AED"      # Violet — 1 RCT
  crl1505: "#059669"    # Vert — preclinique

pathological:
  virus: "#DC2626"      # Rouge — exclusivement pathologique
  cycle: "#DC2626"      # Meme rouge que virus (DS-V2)
  inflammation: "#F59E0B"  # Amber — gradient inflammation

anatomical_bands:
  lumen: "#F8FAFC"      # Quasi-blanc (air)
  epithelium: "#E2E8F0"  # Gris tres clair
  lamina_propria: "#CBD5E1"  # Gris clair
  muscle_smooth_sick: "#FDE68A"  # Amber (inflammation)
  muscle_smooth_healthy: "#BBF7D0"  # Vert pale (resolution)

background:
  canvas: "#FFFFFF"
  gradient_left: "#FEE2E2"   # Rose pale (malade)
  gradient_right: "#DCFCE7"  # Vert pale (sain)
```

## DS-I3: Structure de layout.yaml (section design system)

```yaml
# Extrait de layout.yaml — parametres relevant pour le design system
zones:
  z1_ratio: 0.27    # Zone 1 gauche (probleme)
  z2_ratio: 0.46    # Zone 2 centre (intervention)
  z3_ratio: 0.27    # Zone 3 droite (resolution)

bands:              # 4 bandes anatomiques (V2-A layout)
  lumen:
    y_start: 0.05
    height_ratio: 0.25
  epithelium:
    y_start: 0.30
    height_ratio: 0.20
  lamina_propria:
    y_start: 0.50
    height_ratio: 0.20
  muscle_smooth:
    y_start: 0.70
    height_ratio: 0.15

children:           # Pictogrammes enfants (V12)
  z1_child:
    position: "left_margin"
    scale: 1.0
  z3_child:
    position: "right_margin"
    scale: 1.0

convergence:        # Point focal IgA (B8)
  point_x_ratio: 0.73    # Dans Z3, bande lumen
  point_y_ratio: 0.15    # Haut du lumen
  iga_count: 6           # Nombre de formes Y
  iga_size: 15           # px

fracture:           # Cycle vicieux et lance (B4)
  cycle_center_x: 0.14   # Dans Z1
  cycle_center_y: 0.50
  cycle_radius: 60
  lance_origin_x: 0.50   # Part du centre
  lance_target_x: 0.14   # Vers le cycle
```

## DS-I4: Structure de content.yaml (section design system)

```yaml
# Extrait de content.yaml — labels avec niveaux typographiques
labels:
  - text: "Wheezing/Asthma"
    level: 1                    # Ancre — font-size >= 32 (3x)
    placement: "z1_margin_top"

  - text: "Clinical evidence"
    level: 1
    placement: "z3_margin_top"

  - text: "OM-85"
    level: 2                    # Contexte — font-size 24-30 (3x)
    placement: "near_shield"
    color: "#2563EB"

  - text: "PMBL"
    level: 2
    placement: "near_bricks"
    color: "#0D9488"

  # ... etc.

  - text: "Th1"
    level: 3                    # Ponctuation — font-size 18-22 (3x)
    placement: "near_epithelium_z3"
    optional: true              # Supprime si budget serre

word_budget: 30                 # V3 — maximum absolu
```

## DS-I5: Fonctions du compositeur (compose_ga.py) liees au design system

Le compositeur parametrique contient les fonctions generatrices suivantes qui implementent les patterns du design system :

| Fonction | Pattern | Ref |
|----------|---------|-----|
| `draw_background_gradient()` | Gradient L→R rouge→vert (PH1 seconde 1) | P7, DS-R2 |
| `draw_anatomical_bands()` | 4 bandes avec textures (P27) et gradient L→R par bande | P30, P27 |
| `draw_epithelium_wall()` | Mur de briques avec breches (Z1) et restauration (Z3) | P18, P27 |
| `draw_child_contour(h)` | Enfant parametrique par Health Vector (P15, P16) | P20, V12 |
| `draw_vicious_cycle()` | Cercle ferme 4 stations rouge (P23, DS-V16) | DS-B4 |
| `draw_health_lance()` | Lance verte fracturant le cycle (P23, DS-V17) | DS-B4 |
| `draw_shield_om85()` | Bouclier encastre sur briques (P18) | DS-B5 |
| `draw_bricks_pmbl()` | Briques teal comblant breches (P18) | DS-B5 |
| `draw_helix_mv130()` | Helice dans noyau DC (P18, P19) | DS-B5 |
| `draw_bridge_crl1505()` | Arc systemique depuis le bas (P19, V13) | DS-B5 |
| `draw_convergence_iga()` | 4 flux colores vers point focal + formes Y (B8) | DS-B8 |
| `draw_evidence_bars()` | Barres proportionnelles par produit (P21, B3) | DS-R1 |
| `draw_labels()` | Labels 3 niveaux depuis content.yaml (P28) | DS-R5 |
| `draw_legend()` | Legende produits-couleurs (P7) | DS-R1 |
| `draw_iga_anchors()` | Micro-ancres Y dans le lumen (P22) | DS-V14 |
| `draw_dc_cell()` | Cellule dendritique filopodiale (P20) | DS-V13 |

## DS-I6: Dependances

- `palette.yaml` → lu par `compose_ga.py` et `validate_ga.py`
- `layout.yaml` → lu par `compose_ga.py`
- `content.yaml` → lu par `compose_ga.py` et `validate_ga.py` (word count check)
- `svgwrite` (pip) → generation SVG programmatique
- Playwright → rendu HTML wrapper → PNG
- Pillow → resize LANCZOS, verification non-blank

## DS-I7: Integration avec les autres modules VEC

```
vec/pipeline     → consomme le SVG genere par compose_ga.py (A5/A7)
vec/editorial    → validate_ga.py verifie aussi la palette (H1 palette sub-check)
vec/design_system → CE MODULE — definit les patterns visuels
vec/calibration  → fournit les contours organiques pour draw_child_contour()
vec/audit        → NotebookLM verifie le respect des patterns (H6)
vec/exploration  → sub-agents analysent la lisibilite et l'impact visuel
vec/orchestration → gate checks incluent DS-H1 a DS-H4
```
