# Objectives — Contour Extraction Pipeline

## O1: Goal

Translate AI-generated reference images into parametric SVG contour data that `draw_child()` can consume. The pipeline is the measurement instrument that converts raster calibration sources into mathematical curve constants. Delivers R1-R4.

Extends parent P17 (Reference IA -> calibration des parametres): AI images are input to extraction, not the deliverable. The Bezier constants are the measured data.

## Non-Goals

- **CNO1: Not a general image vectorizer.** This pipeline handles silhouette extraction from controlled AI-generated reference images with clean backgrounds. It does not handle photographs, complex scenes, or multi-object segmentation.
- **CNO2: Not a real-time renderer.** Extraction runs offline during calibration. The rendering path (Catmull-Rom -> Bezier -> SVG) runs at compose time, not extraction time.
- **CNO3: Not a replacement for artistic judgment.** The pipeline produces candidate contours. Visual quality assessment (organic feel, clinical empathy trigger) requires human or AI review via comparison montage (CV5).

## Tradeoffs

- **CT1: Organic quality vs. point count.** Lower tolerance in Douglas-Peucker preserves more anatomical detail but increases point count. Higher tolerance produces smoother interpolation but loses subtle curves. Target: 30-70 points (sweet spot identified empirically from S1-S4 extractions).
- **CT2: Automation vs. manual curation.** Fully automated extraction may produce artifacts (noise contours, inverted masks). Current approach: automated extraction + visual verification montage. Future: automated similarity scoring.
- **CT3: Single-contour vs. multi-part.** Current pipeline extracts only the largest contour (dominant silhouette). Anatomical details (fingers, facial features) that form separate contours are lost. Acceptable at delivery resolution (100x150px).
