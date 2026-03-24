# Implementation — Contour Extraction Pipeline

## Current state

Extraction logic is inline in the session that produced `compose_ga.py`. Contour constants are embedded directly as Python lists (`_CONTOUR_SICK`, `_CONTOUR_HEALTHY`) in the compositor script. No standalone extraction script exists yet.

## Tools and dependencies

| Tool | Role | Version |
|------|------|---------|
| scikit-image | `find_contours()`, `approximate_polygon()` (Douglas-Peucker) | >= 0.19 |
| Pillow | Image loading (PNG -> RGBA) | >= 9.0 |
| numpy | Array operations, coordinate transforms | >= 1.24 |
| svgwrite (future) | SVG path generation for comparison montages | >= 1.4 |

All dependencies are pure Python, no native compilation required. Runs on Windows natively (parent constraint: NO Docker, NO WSL).

## File map

### Current (inline, mission-scoped)

| File | Role |
|------|------|
| `scripts/compose_ga.py` | Contains embedded contour constants and `_catmull_rom_to_bezier()` |
| `artefacts/contours/*.json` | Raw extracted points (4 contours: S1-S4) |
| `artefacts/contours/*.svg` | Visual verification renders |
| `artefacts/references/S{1-4}_enfant_target_{1-4}.png` | AI reference images (calibration sources) |
| `artefacts/comparisons/target_vs_output_*.png` | Comparison montages |

### Future (VEC module extraction)

| File | Role |
|------|------|
| `~/scisense/modules/vec/engine/calibrator.py` | Standalone extraction + normalization |
| `~/scisense/modules/vec/engine/interpolator.py` | Contour matrix + bilinear blending |
| `~/scisense/modules/vec/artefacts/matrix/` | 16-contour grid storage |

### Future API (calibrator.py)

```python
calibrator.extract(image_path, tolerance=2.0) -> ContourData
calibrator.normalize(contour, target_points=64) -> NormalizedContour
calibrator.build_matrix(image_grid, axes) -> ContourMatrix
```

## Key functions

| Function | Location | Role |
|----------|----------|------|
| `find_contours()` | scikit-image | Edge detection on binary mask |
| `approximate_polygon()` | scikit-image | Douglas-Peucker simplification |
| `_catmull_rom_to_bezier()` | `compose_ga.py` (inline) | Catmull-Rom spline -> cubic Bezier control points |
| `draw_child()` | `compose_ga.py` (inline) | Parametric SVG renderer consuming normalized contour data |

## Dependencies on parent module

- **P14 (compositeur parametrique):** Contour data flows into `draw_child()` via YAML config
- **P15 (Health Vector $H$):** Contour interpolation is parameterized by $H$
- **P17 (Reference IA -> calibration):** This pipeline IS the implementation of P17 for organic shapes
- **VN4 (zero AI in final):** Architectural compliance — only math data crosses the boundary
