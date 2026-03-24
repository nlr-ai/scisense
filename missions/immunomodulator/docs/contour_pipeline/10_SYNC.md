# Sync — Contour Extraction Pipeline

## Current state: 24 mars 2026

### Phase: OPERATIONAL (4 contours extracted) — VEC 2.0 contour matrix NOT YET STARTED

### What exists

4 contours extracted from AI reference images using the inline extraction in compose_ga.py session:

| Contour | Source | Points | Image Size | Status |
|---------|--------|--------|-----------|--------|
| S1 (sick alt) | S1_enfant_target_1.png | 64 | 255x231 | Extracted, normalized |
| S2 (healthy alt) | S2_enfant_target_2.png | 87 | 254x226 | Extracted, normalized |
| S3 (sick profile) | S3_enfant_target_3.png | 36 | 226x154 | Extracted, normalized |
| S4 (healthy front) | S4_enfant_target_4.png | 70 | 251x174 | Extracted, normalized |

All 4 pass CV2 (point count 20-100). All stored as JSON in `artefacts/contours/` and embedded as Python constants in `compose_ga.py`.

### What works

- Full extraction flow (A1 steps 1-9): load -> grayscale -> threshold -> contour -> simplify -> normalize -> export
- Catmull-Rom -> Bezier smoothing at render time (A1 step 10)
- Comparison montage generation (A3)
- VN4 compliance verified (no raster data in output)

### What's missing

| Item | Status | Blocker |
|------|--------|---------|
| Standalone extraction script (`extract_contours.py`) | NOT STARTED | Currently inline in session |
| Automated validation script (`validate_contour.py`) | NOT STARTED | Checks performed manually |
| Contour matrix (16 variants, CP2) | NOT STARTED | Needs 16 AI reference images generated |
| Uniform resampling for matrix interpolation | NOT STARTED | Depends on matrix |
| Automated visual similarity scoring (SSIM) | NOT STARTED | Open loop in CH2 |
| VEC module extraction to `~/scisense/modules/vec/` | NOT STARTED | Post-mission extraction |

### Relationship to parent module

This is a sub-module of the immunomodulator GA mission. It implements:
- P12 (IA generative comme accelerateur)
- P17 (Reference IA -> calibration)
- P14 (compositeur parametrique) — contour data feeds draw_child()
- P15 (Health Vector $H$) — contour interpolation parameterized by $H$
- VN4 (zero AI in final)

### VEC 2.0 roadmap

The contour matrix approach (CP2) is the next evolution:

1. Generate 16 AI reference images (4 health states x 4 age steps)
2. Extract contour from each using this pipeline
3. Resample all to uniform point count (64 target)
4. Store as 4x4 matrix
5. Bilinear interpolation at render time (CP5)

This eliminates the current two-contour limitation (sick/healthy only) and enables continuous parameterization along both health and age axes.

### Future module location

When VEC becomes a standalone module:
```
~/scisense/modules/vec/
    engine/calibrator.py    <- extraction + normalization (A1)
    engine/interpolator.py  <- contour matrix + blending (A2)
    artefacts/matrix/       <- 16-contour grid storage
    docs/                   <- this doc chain migrates here
```

### Handoff

1. This doc chain (`docs/contour_pipeline/`) for process and constraints
2. `docs/contour_extraction_pipeline.md` for the original monolithic documentation (predecessor)
3. `artefacts/contours/*.json` for extracted data
4. `artefacts/references/S{1-4}_enfant_target_{1-4}.png` for calibration sources
5. `artefacts/comparisons/` for visual verification montages
6. Parent `docs/10_SYNC.md` for mission-level context

### History

| Date | Action |
|------|--------|
| 2026-03-24 | Contour extraction pipeline built inline during compose_ga.py session |
| 2026-03-24 | 4 contours extracted (S1-S4), embedded as Python constants |
| 2026-03-24 | Architecture pivot to approach (iii) — hybrid math + extracted contours |
| 2026-03-24 | Monolithic documentation written (`contour_extraction_pipeline.md`) |
| 2026-03-24 | Doc chain conversion: 10-facet module format created (`docs/contour_pipeline/`) |
