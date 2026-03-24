# Implementation — Mission Immunomodulateur GA

## I1: Fichiers de production

| Fichier | Rôle | Ref |
|---------|------|-----|
| `scripts/compose_ga.py` | Compositeur paramétrique | A7 |
| `config/palette.yaml` | Couleurs (single source of truth) | P7 |
| `config/layout.yaml` | Positions, tailles, proportions | P14 |
| `config/content.yaml` | Labels, budget mots | V3 |
| `assets/*.svg` | Éléments visuels injectables (currentColor) | P15 |
| `artefacts/wireframes/` | Tous les rendus versionnés | P11 |
| `artefacts/concepts/` | Concept art NotebookLM (référence, pas livrable) | P12 |
| `extracted_references.txt` | 124 références au format MDPI | R3 |

## I2: Stack technique

| Outil | Usage | Ref |
|-------|-------|-----|
| Python `svgwrite` | Génération SVG programmatique (wireframes, icônes, barres) | V6 (libre de droits) |
| Python `svglib` + `reportlab` | Rendu SVG → PNG | H1 (multi-taille) |
| Python `Pillow` | Manipulation image si nécessaire | |
| Inkscape (optionnel) | Finition vectorielle manuelle | |

## I3: Données source

Voir → `MISSION.md` pour la liste complète des fichiers de données.
Tous dans `data/import/missions/immunomodulator-manuscript/`.

## I4: Palette de couleurs

Voir → `GA_SPEC.md` section 2.6 pour la palette complète. Validated by H1 (palette check inclus dans conformité).

## I5: Dépendances

- `svgwrite` (pip)
- `svglib` + `reportlab` (pip)
- Police: Arial/Helvetica (système) ou Inter (à installer si nécessaire)

## I6: Scripts de validation (à créer)

Script `validate_ga.py` qui implémente A4 (validation pré-soumission) :
- Vérifie dimensions PNG (V1)
- Compte les mots SVG (V3)
- Grep hex codes palette (B5)
- Vérifie comptage refs = 124 (R3)
Status: non implémenté. Needed to close H1 loop automatically.

## I7: Structure du dossier mission

```
immunomodulator/
├── MISSION.md              ← hub de pointeurs
├── GA_SPEC.md              ← contraintes techniques
├── config/
│   ├── palette.yaml        ← couleurs
│   ├── layout.yaml         ← positions/tailles
│   └── content.yaml        ← labels/mots
├── assets/                 ← SVG snippets (currentColor)
│   ├── child_sick.svg
│   ├── child_healthy.svg
│   ├── shield_om85.svg
│   ├── helix_mv130.svg
│   ├── bridge_crl1505.svg
│   └── dc_cell.svg
├── scripts/
│   ├── compose_ga.py       ← LE compositeur
│   └── generate_wireframe_v*.py  ← anciens scripts (archivés)
├── docs/                   ← doc chain 10 facets
├── iterations/             ← analyses par axe
├── artefacts/
│   ├── wireframes/         ← SVG + PNG versionnés
│   └── concepts/           ← concept art NotebookLM
└── sources/                ← documents bruts NotebookLM
```
