# Validation — Contour Extraction Pipeline

## Invariants (MUST)

**CV1: Single closed path.** The extracted contour MUST be a single closed path (first point == last point, or explicitly closed). Multiple disjoint paths indicate a fragmented extraction. Health: CH1. Supports R3, R4.

**CV2: Point count in [20, 100].** The simplified polygon MUST have between 20 and 100 control points. Below 20: shape is too crude to be recognizable. Above 100: data is too heavy for parametric interpolation and violates R1 (parsimony). Health: CH3. Supports R1.

**CV3: No self-intersections.** The contour path MUST NOT self-intersect. Self-intersections produce rendering artifacts (inverted fills, bowtie shapes). Detectable by checking for edge crossings in the simplified polygon. Health: manual check via montage (CV5).

**CV4: Bounding box aspect ratio in [0.3, 3.0].** The normalized contour's bounding box aspect ratio (width/height) MUST fall within 0.3 to 3.0. Outside this range indicates a degenerate extraction (e.g., a thin line or a near-square blob that is not a human silhouette). Health: CH1 (structural check). Supports R2.

**CV5: Visual verification against source.** Every extracted contour MUST have a comparison montage (target vs. output) archived in `artefacts/comparisons/`. The montage is the ultimate validation that the mathematical contour preserves the visual intent of the AI reference. Health: CH2 (SVG render non-blank). Carrier: Aurore (aesthetic judgment) + Silas (metric checks).

## Invariants (NEVER)

**CVN1: NEVER embed raster data.** The output JSON/constants MUST contain only coordinate pairs. No base64 images, no pixel arrays, no image file references in the deliverable path. Enforces R4, parent VN4.

**CVN2: NEVER skip visual verification.** An extracted contour without a comparison montage is unvalidated. Do not use unvalidated contours in `compose_ga.py`. Enforces CV5.

## Invariants (PIPELINE)

**CV6: Tolerance parameter documented.** The Douglas-Peucker tolerance used for each extraction MUST be recorded in the output JSON metadata. Different images may require different tolerances. Reproducibility requires the parameter. Supports A1 step 6.

**CV7: Source image archived.** The AI reference image used for extraction MUST be preserved in `artefacts/references/`. The contour is meaningless without its calibration source. Supports parent P9 (provenance), V11.
