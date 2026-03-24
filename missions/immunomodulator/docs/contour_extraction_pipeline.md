# Contour Extraction Pipeline — VEC Calibration Module

## Purpose

Translate AI-generated reference images into parametric SVG contour data for the Visual Evidence Compiler. This is the implementation of Pattern P17 (AI as calibration source).

The pipeline converts raster pixels from AI image models into clean mathematical Bezier curves that can be parametrically controlled. The output is pure vector data — no AI-generated pixels survive into the final deliverable.

---

## Architecture

```
AI Image Model (Midjourney/DALL-E/NotebookLM)
    -> Reference grid (Vs x age x ...)
    -> Edge detection + contour extraction (scikit-image)
    -> Douglas-Peucker polygon simplification
    -> Catmull-Rom -> cubic Bezier smoothing
    -> Normalized contour constants
    -> Parametric interpolation in draw_child()
    -> SVG native output (VN4 compliant)
```

Each stage reduces the data while preserving the visual information that matters:

| Stage | Data Form | Typical Size |
|-------|-----------|-------------|
| AI image | Raster pixels | 250x230 px |
| Contour extraction | Dense point list | 200-500 points |
| Douglas-Peucker simplification | Sparse polygon | 36-87 points |
| Catmull-Rom -> Bezier | Cubic curve segments | ~N/3 segments |
| Normalized constants | Python list of (x, y) | Embedded in code |

---

## Current Implementation

- **Extraction script**: inline in `compose_ga.py` session (to be extracted to `scripts/extract_contours.py`)
- **Tools**: scikit-image `find_contours()`, `approximate_polygon()` (Douglas-Peucker)
- **Smoothing**: Catmull-Rom to cubic Bezier conversion (`_catmull_rom_to_bezier()`)
- **Storage**: Contour points embedded as constants (`_CONTOUR_SICK`, `_CONTOUR_HEALTHY`)
- **Intermediate files**: `artefacts/contours/*.json` (raw extracted points), `artefacts/contours/*.svg` (visual verification)

### Key Functions

| Function | Role |
|----------|------|
| `find_contours()` | scikit-image edge detection on grayscale/binary image |
| `approximate_polygon()` | Douglas-Peucker simplification with configurable tolerance |
| `_catmull_rom_to_bezier()` | Converts Catmull-Rom spline through points into cubic Bezier control points |
| `draw_child()` | Parametric SVG renderer that consumes the normalized contour data |

### Extraction Flow (Detail)

1. Load AI reference image (PNG)
2. Convert to grayscale
3. Apply threshold or edge detection to isolate the silhouette
4. `find_contours()` returns list of contour arrays
5. Select the longest contour (main silhouette)
6. `approximate_polygon(contour, tolerance=N)` reduces point count
7. Normalize coordinates to [0, 1] range relative to image dimensions
8. Convert point sequence through `_catmull_rom_to_bezier()` for smooth curves
9. Store as Python constants or JSON

---

## Sources Used

| Contour | Source | Points | Image Size |
|---------|--------|--------|-----------|
| Sick profile | S3_enfant_target_3.png | 36 | 226x154 |
| Healthy front | S4_enfant_target_4.png | 70 | 251x174 |
| Sick alt | S1_enfant_target_1.png | 64 | 255x231 |
| Healthy alt | S2_enfant_target_2.png | 87 | 254x226 |

All source images are AI-generated references stored in `artefacts/references/`. They serve exclusively as calibration targets — none of their pixel data appears in final output.

---

## VEC 2.0 Roadmap: Contour Matrix

For full parametric control, the next iteration generates a grid of AI variants:

- **Axis 1:** Health (Vs 0 -> 1) — 4 steps
- **Axis 2:** Age (1 -> 5 years) — 4 steps
- = **16 reference images**
- Extract contours from each
- Interpolate bilinearly for any (Vs, age) combination

This eliminates the current two-contour limitation and allows `draw_child()` to render any intermediate state as a smooth blend of the extracted shapes.

### Interpolation Method

Given four corner contours at (Vs_lo, age_lo), (Vs_hi, age_lo), (Vs_lo, age_hi), (Vs_hi, age_hi):

```
contour(Vs, age) = bilinear_blend(
    C_00, C_10, C_01, C_11,
    t_vs = (Vs - Vs_lo) / (Vs_hi - Vs_lo),
    t_age = (age - age_lo) / (age_hi - age_lo)
)
```

Each contour must have the same number of control points (resampled if necessary) for point-wise interpolation to work.

---

## Comparison Pipeline (Quality Assurance)

Automated target-vs-output comparison for visual verification:

1. Crop zones from both infographic target and SVG output
2. Resize to matching dimensions
3. Generate side-by-side montage per element
4. Visual gap analysis — overlay with difference highlighting

**Output:** `artefacts/comparisons/target_vs_output_vN.png`

This pipeline validates that the parametric SVG output faithfully reproduces the visual intent of the AI reference, without requiring the AI pixels themselves.

---

## Design System Compliance

| Pattern | Requirement | How This Pipeline Satisfies It |
|---------|-------------|-------------------------------|
| P12 | AI as accelerator, not producer | AI generates calibration references only; final output is pure SVG math |
| P17 | Reference IA -> calibration | AI images are input to the extraction pipeline, not the deliverable |
| VN4 | Zero AI in final SVG deliverable | Extracted Bezier paths are mathematical data, not AI-generated pixels |

The fundamental principle: AI images are measurement instruments. The contour extraction pipeline is the measurement process. The Bezier constants are the measured data. The SVG compositor uses only the measured data.

---

## Future Module Location

For the VEC module extraction (when VEC becomes a standalone module), this pipeline should migrate to:

```
~/scisense/modules/vec/engine/calibrator.py
```

The calibrator will own the full extraction-to-constants workflow and expose a clean API:

```python
calibrator.extract(image_path, tolerance=2.0) -> ContourData
calibrator.normalize(contour, target_points=64) -> NormalizedContour
calibrator.build_matrix(image_grid, axes) -> ContourMatrix
```
