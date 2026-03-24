# Results — Contour Extraction Pipeline

4 measurable outcomes. Mapping 1:1 with HEALTH checkers.

## R1: Parsimony — < 100 control points

The extracted contour has fewer than 100 control points after Douglas-Peucker simplification. This ensures the data is compact enough for parametric interpolation and embedded storage, while preserving silhouette fidelity.

**Sense:** `len(points)` after extraction. Target range: 20-100.
**Health:** CH3 (point count bounds check)
**Validated by:** CV2

## R2: Delivery legibility — recognizable silhouette at 100x150px

The contour path, when rendered as a filled SVG at 100x150px (the approximate child pictogram size in the GA delivery PNG), produces a recognizable human silhouette. The pediatrician projects their patient in < 2s (PH1 from parent module).

**Sense:** Visual verification via comparison montage (target vs. output at delivery resolution).
**Health:** CH2 (SVG render non-blank, > 1KB)
**Validated by:** CV5

## R3: Automation feasibility — < 30s per image

The full pipeline (load, threshold, extract, simplify, normalize, export) runs in under 30 seconds per reference image on the development machine. This enables the 16-image contour matrix (VEC 2.0) without manual intervention per image.

**Sense:** Wall-clock timing of extraction script.
**Health:** CH1 (valid JSON output produced, implying completion)
**Validated by:** CV1

## R4: VN4 compliance — zero AI pixels in final

The output SVG contains only mathematical Bezier curve data derived from measurement of AI reference images. No AI-generated pixel data survives into the deliverable. Extends parent VN4, V6, P12, P17.

**Sense:** Output is a JSON/Python constant of (x,y) coordinate pairs + SVG path of cubic Bezier segments. No raster data embedded.
**Health:** CH1 (valid JSON with points array, no embedded images)
**Validated by:** CV1

## Guarantee Loop

```
R1 (parsimony)    <- CH3 (point count check)      <- S_CH3 (len(points) in [20,100])
R2 (legibility)   <- CH2 (SVG render non-blank)    <- S_CH2 (file size > 1KB)
R3 (automation)   <- CH1 (valid JSON output)       <- S_CH1 (file exists + valid JSON parse)
R4 (VN4 compliant)<- CH1 (valid JSON, no raster)   <- S_CH1 (structure check: points array only)
```
