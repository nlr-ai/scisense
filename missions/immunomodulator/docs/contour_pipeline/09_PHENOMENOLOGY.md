# Phenomenology — Contour Extraction Pipeline

## CPH1: How Aurore perceives the pipeline output

Aurore sees the **comparison montage**: the AI reference image on the left, the SVG-rendered extracted contour on the right, at delivery resolution. She judges:

- Does the silhouette feel organic or robotic?
- Does the child's posture communicate the health state (sick/healthy)?
- Would a pediatrician project their patient onto this shape in < 2s? (parent PH1)

She never sees point arrays, tolerance values, or coordinate systems. The montage is her sole interface with the pipeline. If the montage looks wrong, the pipeline failed — regardless of what the metrics say.

## CPH2: How Silas perceives the pipeline output

Silas monitors quantitative signals:

- **Point count** (R1): 36-87 range across S1-S4, target sweet spot 30-70
- **Bounding box aspect ratio** (CV4): verifies no degenerate shapes
- **File structure** (CH1): valid JSON, correct keys, no raster contamination
- **Render integrity** (CH2): SVG file exists, non-blank, contains path data

These are the "vital signs" of the extraction. A contour that passes all metrics but fails the montage test (CPH1) needs tolerance adjustment. A contour that looks great but violates CV2 needs resampling.

## CPH3: The "aha" moment

The pipeline succeeds when the extracted SVG silhouette is **visually indistinguishable from the AI source at delivery resolution** (100x150px). At that scale, the polygon simplification and Bezier smoothing eliminate the differences between a 250px raster image and a mathematical curve.

This is the proof that CP1 works: the measurement instrument (pipeline) captured the essential geometry, and the measured data (Bezier constants) reproduces the phenomenon (organic silhouette) without the original signal (AI pixels).

## CPH4: Feedback reinjection

| Observer | Feedback signal | Pipeline adjustment |
|----------|----------------|---------------------|
| Aurore | "Too geometric / robotic" | Lower Douglas-Peucker tolerance (more points, more detail) |
| Aurore | "Looks good but wrong posture" | New AI reference image needed (different prompt), not a pipeline fix |
| Silas | Point count > 100 | Increase tolerance or apply resampling |
| Silas | Self-intersection detected | Manual editing of problem segment, or re-extract with different threshold |
| Silas | Montage shows major shape divergence | Check threshold step (Step 3) — may need adaptive thresholding instead of Otsu |

The pipeline is calibrated by human perception (Aurore) and constrained by machine validation (Silas). Neither alone is sufficient. This mirrors parent PH5 (feedback reinjection loop).
