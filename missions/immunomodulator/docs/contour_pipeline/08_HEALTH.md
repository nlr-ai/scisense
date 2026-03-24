# Health — Contour Extraction Pipeline

3 health checkers + 1 open loop. Mapping to results.

```
R1 (parsimony)     <- CH3 (point count bounds)    <- S_CH3 (len check)
R2 (legibility)    <- CH2 (SVG render non-blank)   <- S_CH2 (file size check)
R3 (automation)    <- CH1 (valid JSON output)      <- S_CH1 (file + parse check)
R4 (VN4 compliant) <- CH1 (structure check)        <- S_CH1 (no raster data)
```

---

## CH1: Valid JSON output -> validates R3, R4

The extraction pipeline produces a valid JSON file containing a points array and metadata. No embedded raster data.

### Sense signals

| ID | Signal | Checks | Automation |
|----|--------|--------|------------|
| S_CH1a | File exists | `artefacts/contours/{name}.json` exists | Auto — `os.path.exists()` |
| S_CH1b | Valid JSON | File parses as valid JSON | Auto — `json.load()` succeeds |
| S_CH1c | Points array present | JSON has `"points"` key with list of [x,y] pairs | Auto — structure check |
| S_CH1d | No raster data | JSON has no `"image"`, `"base64"`, `"pixels"` keys | Auto — key absence check |
| S_CH1e | Metadata present | JSON has `"source"`, `"tolerance"` keys (CV6) | Auto — key presence check |

**Checker:** Post-extraction validation script (to be integrated into calibrator.py).

**Carrier:** Silas.

**Status:** Partially closed — checks performed manually after extraction. No automated checker script yet.

---

## CH2: SVG render non-blank -> validates R2

The SVG render of the extracted contour is a non-trivial file (not blank, not corrupt).

### Sense signals

| ID | Signal | Checks | Automation |
|----|--------|--------|------------|
| S_CH2a | SVG file exists | `artefacts/contours/{name}.svg` exists | Auto — `os.path.exists()` |
| S_CH2b | File size > 1KB | SVG is not an empty/stub file | Auto — `os.path.getsize() > 1024` |
| S_CH2c | Contains path data | SVG has at least one `<path>` element with `d` attribute | Auto — XML parse + check |

**Checker:** Post-render validation (part of comparison montage generation, A3).

**Carrier:** Silas (automated) + Aurore (visual judgment via montage, CV5).

**Status:** Partially closed — SVG files generated for S1-S4, visual inspection done. No automated checker.

---

## CH3: Point count within bounds -> validates R1

The simplified polygon has between 20 and 100 control points (CV2).

### Sense signals

| ID | Signal | Checks | Automation |
|----|--------|--------|------------|
| S_CH3a | Point count >= 20 | `len(points) >= 20` | Auto |
| S_CH3b | Point count <= 100 | `len(points) <= 100` | Auto |

**Checker:** Inline assertion during extraction (A1 step 6). If violated, adjust tolerance and retry.

**Carrier:** Silas.

**Status:** Closed for S1-S4 (all within bounds: 36, 70, 64, 87 points).

---

## Open loops

| Loop | Missing link | What's needed | Who |
|------|-------------|---------------|-----|
| CH2 -> R2 | Automated visual similarity scoring | Structural similarity (SSIM) or perceptual hash between reference and render | Silas |
| CH1 -> R3 | Automated timing check | Wall-clock measurement integrated into extraction script | Silas |
| All | Standalone checker script | Consolidate S_CH1-S_CH3 into a single `validate_contour.py` | Silas |
| CH3 -> CP2 | Uniform resampling validation | When contour matrix is built, verify all 16 contours have identical point counts | Silas |
