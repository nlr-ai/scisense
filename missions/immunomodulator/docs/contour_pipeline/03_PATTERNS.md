# Patterns — Contour Extraction Pipeline

## CP1: AI as calibration source

AI-generated images are measurement targets, not assets. The pipeline measures their geometry and discards their pixels. The output is pure mathematical data. This is the concrete implementation of parent P17 (Reference IA -> calibration) and P12 (IA generative comme accelerateur, pas comme producteur).

```
AI image (pixels) --[measurement]--> contour points (math) --[smoothing]--> Bezier curves (math) --[render]--> SVG (math)
```

No pixel data crosses the boundary. VN4 compliance is architectural, not a policy check.

## CP2: Contour matrix approach

For parametric control across health state and age, the pipeline generates a grid of AI variants along two axes:

- **Axis 1:** Health (Vs 0 -> 1) — 4 steps
- **Axis 2:** Age (1 -> 5 years) — 4 steps
- = **16 reference images**, each extracted independently

The grid enables bilinear interpolation between neighbors for any (Vs, age) combination. Each contour in the matrix must have the same number of control points (resampled if necessary) for point-wise blending.

Extends parent P15 (Health Vector $H$): the contour matrix makes $H$ continuous for organic shapes, not just inorganic elements (walls, blocks).

## CP3: Catmull-Rom -> Bezier smoothing

Raw extracted polygons have sharp corners at each control point. The pipeline converts the polygon into a smooth cubic Bezier path via Catmull-Rom spline interpolation:

1. Treat the simplified polygon points as Catmull-Rom control points
2. For each segment, derive the two cubic Bezier control points from the surrounding Catmull-Rom points
3. The resulting path passes through all original points but with smooth tangent continuity

This produces organic curves that look hand-drawn rather than polygonal, critical for clinical empathy (parent PH1).

## CP4: Normalized coordinate system

All extracted contours are stored in a unit coordinate system:

- **Height normalized to 1.0** (tallest extent)
- **Origin at centroid** (centered)
- **Aspect ratio preserved** (width varies with shape)

This makes contours scale-independent and composable. At render time, `draw_child()` applies translation and scale from the YAML config. Supports parent P14 (compositeur parametrique a generateurs).

## CP5: Bilinear interpolation between grid neighbors

Given four corner contours C_00, C_10, C_01, C_11 at grid positions, any intermediate contour is computed as:

```
contour(Vs, age) = bilinear_blend(C_00, C_10, C_01, C_11, t_vs, t_age)
```

Where `t_vs` and `t_age` are normalized interpolation parameters. This requires all four corners to have identical point counts (enforced by resampling during extraction).

Extends parent P15 (Health Vector $H$): enables continuous $H$ parameterization for organic silhouettes.
