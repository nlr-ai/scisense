# Algorithm — Contour Extraction Pipeline

Step-by-step extraction logic. Each step has a defined input, output, and failure mode.

## A1: Full extraction flow

```
Step 1: Load image
    Input:  path to PNG (AI reference)
    Output: RGBA array (H x W x 4)
    Fail:   FileNotFoundError -> abort

Step 2: Grayscale conversion
    Input:  RGBA array
    Output: Grayscale array (H x W), values 0.0-1.0
    Method: Mean of RGB channels (equal weight)
    Fail:   Empty array -> abort

Step 3: Otsu threshold -> binary mask
    Input:  Grayscale array
    Output: Binary mask (H x W), bool
    Method: skimage.filters.threshold_otsu()
    Convention: dark pixels = silhouette (mask = grayscale < threshold)
    Fail:   Uniform image -> threshold meaningless -> abort

Step 4: Contour detection
    Input:  Binary mask
    Output: List of contour arrays (each: N x 2, row/col coords)
    Method: skimage.measure.find_contours(mask, level=0.5)
    Fail:   No contours found -> abort

Step 5: Select largest contour
    Input:  List of contour arrays
    Output: Single contour array (largest by point count)
    Method: max(contours, key=len)
    Rationale: Largest contour = main silhouette (noise contours are smaller)

Step 6: Douglas-Peucker simplification
    Input:  Dense contour (200-500 points)
    Output: Simplified polygon (target: 30-70 points)
    Method: skimage.measure.approximate_polygon(contour, tolerance=1.5)
    Parameter: tolerance=1.5 (empirically tuned on S1-S4)
    Fail:   Result < 20 or > 100 points -> adjust tolerance and retry

Step 7: Coordinate transform (row,col) -> (x,y)
    Input:  Points as (row, col) from scikit-image
    Output: Points as (x, y) with standard orientation
    Method: x = col, y = -row (flip vertical, image origin is top-left)

Step 8: Normalize to unit height
    Input:  Points in pixel coordinates
    Output: Points in normalized coordinates
    Method:
        - Compute bounding box (x_min, x_max, y_min, y_max)
        - height = y_max - y_min
        - Scale all points by 1/height
        - Translate centroid to origin (0, 0)

Step 9: Export
    Input:  Normalized points list [(x1,y1), (x2,y2), ...]
    Output: JSON file (artefacts/contours/{name}.json)
            OR Python constants (embedded in compose_ga.py)
    Format: {"name": "...", "points": [[x,y], ...], "source": "...", "tolerance": 1.5}

Step 10: Render-time smoothing (not part of extraction)
    Input:  Normalized points
    Output: SVG path string with cubic Bezier commands
    Method: _catmull_rom_to_bezier(points)
        For each triplet (P_{i-1}, P_i, P_{i+1}):
            cp1 = P_i + (P_{i+1} - P_{i-1}) / 6
            cp2 = P_{i+1} - (P_{i+2} - P_i) / 6
        Emit: C cp1.x,cp1.y cp2.x,cp2.y P_{i+1}.x,P_{i+1}.y
    Close path with Z
```

## A2: Contour matrix construction (VEC 2.0)

```
Step 1: Generate 16 AI reference images
    Grid: 4 health states x 4 age steps
    Tool: Midjourney/DALL-E with controlled prompts

Step 2: Extract contour from each (A1 steps 1-9)
    16 independent extractions

Step 3: Resample to uniform point count
    Target: 64 points per contour (median of S1-S4 range)
    Method: Arc-length parameterized resampling

Step 4: Store as contour matrix
    Format: 4x4 array of normalized contour arrays
    Index: matrix[health_idx][age_idx]

Step 5: Interpolation at render time
    Input: (Vs, age) continuous parameters
    Output: Interpolated contour (64 points)
    Method: Bilinear blend of 4 nearest grid neighbors (CP5)
```

## A3: Comparison montage generation

```
Step 1: Crop target zone from reference image
Step 2: Render extracted contour as filled SVG at matching resolution
Step 3: Place side-by-side on canvas (target left, output right)
Step 4: Save as artefacts/comparisons/target_vs_output_{name}.png
```
