# Behaviors — Contour Extraction Pipeline

Observable system effects. What the pipeline does.

## CB1: Silhouette extraction

Given a reference image (AI-generated PNG), the pipeline extracts the dominant silhouette contour. It isolates the foreground shape from the background using grayscale conversion and Otsu thresholding, then selects the largest connected contour as the primary silhouette.

**Input:** PNG image (typically 200-260px, AI-generated reference)
**Output:** Dense point list (200-500 points)
**Implements:** CP1 (AI as calibration source), parent P17

## CB2: Point simplification

The dense contour is reduced to 30-70 control points via Douglas-Peucker polygon approximation. The tolerance parameter controls the tradeoff between fidelity and parsimony (CT1).

**Input:** Dense point list (200-500 points)
**Output:** Simplified polygon (30-70 points, typical)
**Implements:** R1 (parsimony), CV2 (point count bounds)

## CB3: Bezier smoothing

The simplified polygon is converted to a smooth cubic Bezier path via Catmull-Rom spline conversion. Sharp polygon corners become smooth tangent-continuous curves, producing organic silhouettes that trigger clinical empathy (parent PH1).

**Input:** Simplified polygon (N points)
**Output:** Cubic Bezier path (~N/3 segments)
**Implements:** CP3 (Catmull-Rom -> Bezier)

## CB4: Coordinate normalization

All contour points are normalized to a unit coordinate system: height = 1.0, centered at origin, aspect ratio preserved. This makes contours portable across different render contexts and composable with the parametric compositor.

**Input:** Points in image pixel coordinates (row, col)
**Output:** Points in normalized coordinates (x, y), unit height, centered
**Implements:** CP4 (normalized coordinate system), parent P14 (compositeur parametrique)

## CB5: Export to storage

Normalized contour data is exported as JSON files (for tooling) and/or embedded as Python constants (for `compose_ga.py`). The export format contains only coordinate pairs — no pixel data, no image references.

**Input:** Normalized contour points
**Output:** `artefacts/contours/*.json` and/or Python constants in `compose_ga.py`
**Implements:** R4 (VN4 compliance)

## CB6: Comparison montage generation

For quality assurance, the pipeline generates side-by-side comparison montages: the AI reference image alongside the SVG render of the extracted contour at delivery resolution. This enables visual verification (CV5) without requiring automated similarity scoring.

**Input:** Reference PNG + rendered SVG of extracted contour
**Output:** `artefacts/comparisons/target_vs_output_*.png`
**Implements:** CV5, parent P8 (iteration E2E)
