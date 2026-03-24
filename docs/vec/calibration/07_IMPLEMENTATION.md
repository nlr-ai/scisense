# Implementation — vec/calibration

## Architecture fichiers

```
scisense/
├── scripts/
│   ├── calibrate_contour.py         # Pipeline single-image (A_CAL2 -> A_CAL5)
│   ├── calibrate_matrix.py          # Contour Matrix (A_CAL6)
│   └── extract_integral_params.py   # Extraction parametres integraux (A_CAL8)
│
├── missions/immunomodulator/
│   ├── artefacts/
│   │   ├── contours/                # SVG contours finaux + JSON intermediaires
│   │   │   ├── S1_sick_contour.svg            # EXISTANT — polyline brute manuelle
│   │   │   ├── S2_healthy_contour.svg         # EXISTANT — polyline brute manuelle
│   │   │   ├── S3_sick_contour.svg            # EXISTANT — polyline brute manuelle
│   │   │   ├── S4_healthy_contour.svg         # EXISTANT — polyline brute manuelle
│   │   │   ├── S{N}_{state}_points.json       # A CREER — JSON intermediaire pipeline
│   │   │   └── S{N}_{state}_bezier.svg        # A CREER — SVG Bezier cubique pipeline
│   │   ├── calibration/
│   │   │   ├── source/                        # Images IA sources (ephemeres)
│   │   │   ├── contour_matrix.png             # Grille complete (A_CAL6)
│   │   │   ├── selection.json                 # Selection documentee
│   │   │   ├── empathy_test.md                # Resultat test Aurore (A_CAL7)
│   │   │   └── calibration_params.yaml        # Parametres integraux (A_CAL8)
│   │   └── comparisons/
│   │       ├── target_vs_output_{SN}_{state}.png   # Superposition source/contour
│   │       └── report_{SN}_{state}.json             # Rapport IoU/Hausdorff
│   │
│   └── config/
│       └── layout_v10.yaml          # EXISTANT — recoit les params calibres
│
└── docs/vec/calibration/            # Ce doc chain (10 facets)
```

## Scripts — responsabilites

### `calibrate_contour.py`

**Responsabilite:** Executer le pipeline complet pour une seule image source. Encapsule A_CAL2 (extraction), A_CAL3 (Douglas-Peucker), A_CAL4 (Catmull-Rom -> Bezier), A_CAL5 (comparaison).

**Interface:**
```bash
python scripts/calibrate_contour.py \
    --source artefacts/calibration/source/age4_H0_raw.png \
    --output artefacts/contours/S5_sick \
    --epsilon 0.02 \
    --sigma 2.0 \
    --target-points 30
```

**Arguments:**
- `--source` : chemin vers l'image IA source (PNG/JPEG)
- `--output` : prefixe de sortie (produit `_points.json`, `_contour.svg`, et la comparaison)
- `--epsilon` : facteur de simplification Douglas-Peucker (defaut: 0.02 = 2% du perimetre)
- `--sigma` : sigma du flou gaussien pre-extraction (defaut: 2.0)
- `--target-points` : nombre cible de points apres simplification (ajuste epsilon automatiquement)

**Dependances:** scikit-image, numpy, rdp, Pillow, svgwrite

**Sortie:** 3 fichiers — `_points.json` (donnees intermediaires), `_contour.svg` (Bezier cubique), `target_vs_output.png` (comparaison)

**Status:** Non implemente.

---

### `calibrate_matrix.py`

**Responsabilite:** Orchestrer la Contour Matrix (A_CAL6). Appelle `calibrate_contour.py` pour chaque cellule, genere les intermediaires par interpolation, produit la visualisation grille.

**Interface:**
```bash
python scripts/calibrate_matrix.py \
    --ages "2-3,4-6,7-10" \
    --source-dir artefacts/calibration/source/ \
    --output-dir artefacts/calibration/
```

**Dependances:** calibrate_contour.py, numpy, Pillow (pour la grille PNG)

**Status:** Non implemente.

---

### `extract_integral_params.py`

**Responsabilite:** Extraire les parametres multi-dimensionnels d'une infographie IA (A_CAL8). Produit un `calibration_params.yaml`.

**Interface:**
```bash
python scripts/extract_integral_params.py \
    --source artefacts/calibration/source/infographic_1.png \
    --output artefacts/calibration/calibration_params.yaml
```

**Dependances:** scikit-image, numpy, Pillow, PyYAML

**Status:** Non implemente. Ce script est le plus semi-automatique — il propose des valeurs que Silas valide manuellement.

---

## Dependances Python

| Package | Version min | Usage |
|---------|-------------|-------|
| scikit-image | 0.21+ | find_contours, rgb2gray, threshold_otsu, approximate_polygon |
| numpy | 1.24+ | Arrays, interpolation |
| rdp | 0.8+ | Ramer-Douglas-Peucker (alternative a approximate_polygon) |
| Pillow | 10.0+ | Lecture/ecriture images, compositing, mesures |
| svgwrite | 1.4+ | Generation SVG natif |
| PyYAML | 6.0+ | Lecture/ecriture config YAML |

**Note:** Pas de dependance lourde (pas de TensorFlow, pas de PyTorch). Le pipeline est purement geometrique — scikit-image et numpy suffisent. C'est delibere : le pipeline doit rester leger, rapide (<5s par image), et sans GPU.

---

## Integration avec le compositeur

Le compositeur (`compose_ga_v10.py`) consomme les contours SVG via le YAML de layout :

```yaml
# layout_v10.yaml (extrait)
children:
  sick:
    contour_path: "artefacts/contours/S5_sick_contour.svg"
    position: [x, y]
    scale: 0.8
    fill: "#DC2626"
    opacity: 0.85
  healthy:
    contour_path: "artefacts/contours/S6_healthy_contour.svg"
    position: [x, y]
    scale: 0.8
    fill: "#059669"
    opacity: 0.85
```

Le compositeur lit le `<path d="..."/>` du SVG et l'injecte directement dans le GA SVG avec les transformations (translate, scale). Il ne re-rasterise jamais le contour — tout reste vectoriel.

---

## Artefacts existants (etat au 24 mars 2026)

4 contours SVG existent deja dans `missions/immunomodulator/artefacts/contours/`. Ce sont des **polylines brutes** tracees manuellement a partir d'images IA, PAS des sorties du pipeline algorithmique :

| Fichier | Type | Points | Observations |
|---------|------|--------|-------------|
| S1_sick_contour.svg | Polyline brute | ~60 | Silhouette enfant avec bras tenant un objet. Angles visibles. |
| S2_healthy_contour.svg | Polyline brute | ~80 | Silhouette enfant bras ouverts. Certains segments lineaires. |
| S3_sick_contour.svg | Polyline brute | ~30 | Silhouette enfant compact. Plus simple. |
| S4_healthy_contour.svg | Polyline brute | ~60 | Silhouette enfant bras tres ouverts. Segments visibles doigts. |

Ces contours sont des preuves de concept. Le pipeline algorithmique les remplacera avec des Bezier cubiques organiques. Les fichiers existants sont preserves comme reference historique (P11).
