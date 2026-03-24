# AXE 3: Evidence Communication — Deep Analysis

**Date:** 2026-03-24
**Status:** ANALYSIS COMPLETE — VERDICT RENDERED
**Constraint reminder:** Zone 3 = ~825 x 1680 px at 3x. Budget texte Zone 3 = 7 mots max. V5 invariant: OM-85 > PMBL > MV130 > CRL1505. V7: lisible a 50% zoom (550x280 px total). V3: aucun bloc de texte.

---

## 0. Diagnostic: Why the Current Approach Falls Short

Wireframe v3 uses four stacked horizontal fill bars (320 px wide, 120 px tall each) with product-colored fills proportional to evidence strength. The product name sits left-aligned outside the bar, the RCT count label sits inside or beside the fill.

**What it does right:**
- Correct ordering (V5 satisfied)
- Color continuity from Zone 2
- Quantitative at a glance (bar length = evidence amount)

**What it does wrong:**
- **Generic.** Any bar chart communicates quantity. This particular bar chart does not communicate *clinical maturity*, which is what matters to a pediatrician deciding whether to prescribe.
- **Equal visual weight.** Each bar occupies the same 320x120 px slot. CRL1505 (zero pediatric RCTs) gets as much canvas real estate as OM-85 (18 RCTs, 7 meta-analyses, 2116 patients). The visual grammar says "these are four comparable things" when the scientific message is "these are four things on a dramatic gradient."
- **No semantic encoding.** The bars do not tell the reader *what kind* of evidence — a bar at 100% and a bar at 30% look like "more vs. less." They do not encode the qualitative leap between "18 RCTs with meta-analyses" and "1 RCT" or between "1 RCT" and "preclinical only."
- **Dead space.** The gray background of unfilled bars (F3F4F6) occupies significant Zone 3 real estate for no informational purpose.
- **Mobile collapse.** At 50% zoom, the four bars become near-identical thin rectangles. The gradient is barely perceptible.

**Core tension:** The manuscript's unique contribution is the FIRST comparative synthesis. The evidence gradient IS the story. Zone 3 must make that gradient *visceral*, not merely correct.

---

## 1. Three Sub-Options

### Option A: Graduated Fill Bars — Refined

**Concept:** Keep horizontal bars, but eliminate generic weaknesses through asymmetric sizing, typographic hierarchy, and semantic markers.

**Layout in Zone 3 (825 x 1680 px at 3x):**

```
x=2475  (66 px margin from Zone 3 left edge at x=2409)
Total available width: ~760 px

Y-layout (top to bottom):
  y=80    "Clinical evidence" title (36px, #1F2937, center)
  y=140   Thin horizontal rule (1px, #E5E7EB)

  === OM-85 block (y=180 to y=480) — 300px tall ===
  y=190   "OM-85" label (44px bold, #2563EB)
  y=240   Bar: 700px wide, 80px tall, FULL fill (#2563EB, opacity 0.85)
  y=260   Inside bar: "18 RCTs  •  7 meta-analyses" (24px white bold)
  y=340   Below bar: "2116 patients  •  26-36% RTI reduction" (22px, #6B7280)
  y=380   Stethoscope icon (32x32 SVG) + "Robust" label (28px bold, #2563EB)
  y=440   Subtle separator line

  === PMBL block (y=500 to y=720) — 220px tall ===
  y=510   "PMBL" label (38px bold, #0D9488)
  y=550   Bar: 385px wide (55% of 700), 60px tall (#0D9488, opacity 0.75)
  y=570   Inside bar: "5 RCTs" (22px white bold)
  y=630   Below bar: "1 meta-analysis" (20px, #9CA3AF)
  y=680   No icon. "Preliminary" label (24px, #0D9488)

  === MV130 block (y=760 to y=940) — 180px tall ===
  y=770   "MV130" label (34px bold, #7C3AED)
  y=810   Bar: 140px wide (20% of 700), 48px tall (#7C3AED, opacity 0.65)
  y=830   Right of bar: "1 RCT" (22px, #7C3AED)
  y=880   "40% wheezing reduction" (20px, #9CA3AF)
  y=920   "Emerging" label (22px, #7C3AED)

  === CRL1505 block (y=980 to y=1140) — 160px tall ===
  y=990   "CRL1505" label (30px bold, #059669)
  y=1030  Bar: 50px wide (7% of 700), 36px tall (#059669, opacity 0.5)
  y=1050  Right of bar: "Preclinical" (22px, #059669)
  y=1090  Flask icon (24x24) + "Trial ongoing" (18px, #9CA3AF)
  y=1120  "NCT07154992" (16px, #D1D5DB) — optional, may violate V3 spirit

  y=1200  Vertical gradient arrow: green (#059669) at bottom → blue (#2563EB) at top
          running along left margin (x=2440), spanning from y=1100 to y=200
          Label at bottom: "Emerging" (20px)
          Label at top: "Robust" (20px)
```

**Key refinements vs. v3:**
- **Asymmetric block heights:** OM-85 gets 300px, CRL1505 gets 160px. Size encodes importance.
- **Asymmetric bar heights:** 80px → 60px → 48px → 36px. The bars physically shrink.
- **Typography scales down:** Product name font decreases from 44px to 30px. Subsidiary labels decrease proportionally.
- **Semantic markers:** Stethoscope for OM-85 (clinical practice), flask for CRL1505 (lab). These are not decorative; they encode qualitative category.
- **Side gradient arrow:** Continuous visual reference for the gradient axis.

**Word count:** "Clinical evidence" (2) + "OM-85" + "PMBL" + "MV130" + "CRL1505" (4 names, already counted in Zone 2) + "18 RCTs", "5 RCTs", "1 RCT", "Preclinical" (7 labels) + "Robust", "Emerging" (2). Names are shared with Zone 2, so net new = ~9 words. Tight but feasible if we drop "7 meta-analyses" and "2116 patients" to keep under budget. Stripped version: "Clinical evidence" + 4 RCT labels + "Robust" + "Emerging" = 7 words net new.

---

### Option B: Spatial Dominance

**Concept:** Abandon bars entirely. Use the *physical area* each product occupies as the evidence encoding. OM-85 dominates Zone 3 visually. CRL1505 is a small marker. The pediatrician does not read a chart — they *see* dominance.

**Layout in Zone 3 (825 x 1680 px at 3x):**

```
Zone 3 background: #ECFDF5 (pale blue-green, as spec)

y=80    "Clinical evidence" title (36px, center, #1F2937)
y=130   Thin rule

=== OM-85 dominant block (y=160 to y=900) — 740px tall, ~55% of Zone 3 height ===
  Large rounded rectangle: 720 x 700 px
  Fill: #2563EB at 0.12 opacity (light blue wash)
  Border: 3px solid #2563EB
  Center content:
    - Shield/capsule icon from Zone 2 (reused), scaled to 120x120 px
    - "OM-85" (48px bold, #2563EB)
    - "18 RCTs" (36px bold, #2563EB)
    - Below: 18 small filled circles (arranged in 3 rows of 6), each = 1 RCT
      Each circle: 20px diameter, #2563EB, opacity 0.6
    - Stethoscope icon (40x40) at bottom-right corner

=== PMBL block (y=920 to y=1200) — 280px tall, ~17% ===
  Medium rounded rectangle: 500 x 250 px (centered)
  Fill: #0D9488 at 0.10 opacity
  Border: 2px solid #0D9488
  Center:
    - Brick/mason icon from Zone 2, 60x60 px
    - "PMBL" (38px bold, #0D9488)
    - "5 RCTs" (28px bold, #0D9488)
    - 5 filled circles in a row (16px each)

=== MV130 block (y=1220 to y=1400) — 180px tall, ~11% ===
  Small rounded rectangle: 320 x 150 px (centered)
  Fill: #7C3AED at 0.08 opacity
  Border: 1.5px solid #7C3AED
  Center:
    - Star/programmer icon from Zone 2, 40x40 px
    - "MV130" (32px bold, #7C3AED)
    - "1 RCT" (24px, #7C3AED)
    - 1 filled circle (16px)

=== CRL1505 block (y=1420 to y=1540) — 120px tall, ~7% ===
  Tiny rounded rectangle: 200 x 100 px (centered)
  Fill: #059669 at 0.06 opacity
  Border: 1px dashed #059669 (dashed = not yet established)
  Center:
    - Bridge/gut-lung icon from Zone 2, 28x28 px
    - "CRL1505" (26px bold, #059669)
    - "Preclinical" (20px, #059669)
    - No circles (zero pediatric RCTs)
    - Small flask icon (20x20) in corner

=== Bottom annotation (y=1560 to y=1640) ===
  Left-aligned: microscope icon (20x20) + "Laboratory" (18px, #9CA3AF)
  Right-aligned: stethoscope icon (20x20) + "Clinical practice" (18px, #9CA3AF)
  Arrow between them pointing up (indicating the blocks above ascend from lab to clinical)
```

**Why this works:**
- **Pre-attentive processing.** Before reading a single label, the viewer sees one enormous blue block, one medium teal block, one small violet block, one tiny green block. The hierarchy is encoded in the most primitive visual channel: area.
- **Dot-per-RCT encoding.** 18 dots vs. 5 vs. 1 vs. 0 is immediately countable without reading numbers. This is a unit chart, not a bar chart — more concrete, more memorable.
- **Icon reuse.** The product icons from Zone 2 appear again, reinforcing cross-zone continuity.
- **Dashed border for CRL1505.** The visual grammar of "dashed = incomplete/provisional" is universally understood in scientific and technical illustration.

**Word count:** "Clinical evidence" (2) + product names (shared) + RCT labels (4) + "Preclinical" (1) = 7 net new. Within budget.

**Risk:** Could look like a simple infographic rather than a medical journal figure. The blocks must be sufficiently refined (subtle fills, scientific icons, no bright cartoon colors) to maintain MDPI Q2 esthetic.

---

### Option C: Pathway/Trajectory — "Translational Staircase"

**Concept:** A vertical path from "Laboratory" at the bottom to "Clinical Practice" at the top. Products are positioned as milestones along this path. The metaphor: translational medicine is a journey from bench to bedside. OM-85 has arrived. CRL1505 has just started.

**Layout in Zone 3 (825 x 1680 px at 3x):**

```
Zone 3 background: vertical gradient from #ECFDF5 (top, clinical = resolved)
                    to #FEF2F2 (bottom, lab = early)
                    This gradient inverts Zone 1's "problem" color, creating a
                    full narrative arc across the GA.

y=60    "Clinical evidence" title (36px, center, #1F2937)

=== Vertical pathway ===
  Central axis: x=2820 (center of Zone 3)
  Path: vertical line from y=1580 (bottom) to y=140 (top)
  Path style: 6px wide, gradient from #059669 (bottom) to #2563EB (top)

  4 "stations" along the path, marked by horizontal branches:

  --- Station 1: SUMMIT (y=200) ---
  Platform: horizontal shelf extending left from the path
  Width: 500px (x=2520 to x=2820)

  On the platform:
    Stethoscope icon (48x48, #2563EB) at left
    "OM-85" (40px bold, #2563EB)
    "18 RCTs" (30px, #2563EB)
    A solid ground beneath: thick line (4px, #2563EB) = established
    Small flag/pennant at the top of the path (summit marker)

  Right of path at same y:
    Small badge: "26-36% RTI ↓" (22px, #4B5563) — optional, may drop for budget

  --- Station 2: UPPER SLOPE (y=560) ---
  Platform: horizontal shelf, 380px wide (x=2640 to x=2820)
  Narrower than Station 1 = less established

    Mason/brick icon (36x36, #0D9488)
    "PMBL" (34px bold, #0D9488)
    "5 RCTs" (26px, #0D9488)
    Ground line: 2.5px, #0D9488

  --- Station 3: MID SLOPE (y=920) ---
  Platform: short shelf, 240px wide (x=2760 to x=2820)
  Even narrower

    Star icon (28x28, #7C3AED)
    "MV130" (30px bold, #7C3AED)
    "1 RCT" (22px, #7C3AED)
    Ground line: 1.5px, #7C3AED

  --- Station 4: BASE CAMP (y=1300) ---
  Platform: minimal shelf, 160px wide (x=2820 to x=2980) — extends RIGHT
  (different side of path = qualitatively different status)

    Flask/microscope icon (24x24, #059669)
    "CRL1505" (26px bold, #059669)
    "Preclinical" (20px, #059669)
    Ground line: 1px dashed, #059669
    Small upward arrow (↑) on the path above CRL1505 = "ascending"

  --- Axis labels ---
  y=1560  Bottom of path: microscope icon + "Laboratory" (22px, #9CA3AF)
  y=120   Top of path: stethoscope icon + "Bedside" (22px, #9CA3AF)
          [or "Clinical practice" but "Bedside" = 1 word, better for budget]

  --- Path detail ---
  Between stations: the path line changes character:
    Base to Station 4: thin dashed (#059669, 2px)
    Station 4 to 3: thin solid (#7C3AED, 3px)
    Station 3 to 2: medium solid (#0D9488, 4px)
    Station 2 to 1: thick solid (#2563EB, 6px)

  This thickening path reinforces: more evidence = more solid ground.
```

**Why this works:**
- **Narrative encoding.** The pediatrician reads a *story*: translational medicine as a climb from bench to bedside. This is the narrative they learned in medical school. It maps to their mental model of evidence maturity.
- **Spatial position = semantics.** Height on the axis directly encodes clinical maturity. No legend needed. No bar chart literacy required.
- **Platform width as secondary encoding.** Wider shelf = more established = more stable ground. This double-encodes the hierarchy (position + width).
- **Path thickness as tertiary encoding.** The thickening line from bottom to top triple-encodes the gradient. Even in a black-and-white print, the hierarchy reads.
- **Cross-zone narrative arc.** Zone 1 (red, problem, bottom) → Zone 2 (amber, intervention, middle) → Zone 3 (green summit, evidence/resolution, top). If Zone 3's background gradient runs from pale red at bottom to pale green at top, it recapitulates the entire GA narrative within itself.
- **CRL1505 on opposite side of path.** Subtle but powerful: it has not yet "crossed over" to clinical evidence. Preclinical is literally on a different side.

**Word count:** "Clinical evidence" (2) + "18 RCTs" + "5 RCTs" + "1 RCT" + "Preclinical" (4 labels) + "Bedside" + "Laboratory" (2 axis labels) = 8 net new words. At budget limit. Drop "Laboratory" label and rely on microscope icon alone to save 1 word. Or merge "Clinical evidence" title with "Bedside" to read "Clinical evidence" at the summit only.

**Risk:** Vertical orientation in a horizontal (panoramic) canvas. Zone 3 is 825px wide and 1680px tall — vertical axis works WITH the zone's aspect ratio, not against it. This is actually an advantage.

---

## 2. Self-Critique Against Three Filters

### Filter 1: MDPI Compliance

| Criterion | Option A (Bars) | Option B (Spatial) | Option C (Pathway) |
|-----------|----------------|-------------------|-------------------|
| V1: Dimensions | PASS — fits Zone 3 | PASS | PASS |
| V2: No titles/affiliations | PASS | PASS | PASS |
| V3: Text budget ≤ 30 words total | RISK — stripped version = 7 words, but temptation to add stats | PASS — 7 words clean | RISK — 8 words, needs trimming |
| V5: Hierarchy exact | PASS — bar length + asymmetric sizing | PASS — area dominance unmistakable | PASS — vertical position is unambiguous |
| V7: Lisible at 50% zoom | RISK — small bars for MV130/CRL1505 become tiny | MODERATE RISK — CRL1505 block is very small by design | PASS — vertical positions remain distinct at any zoom |
| R2: Not identical to Fig 1/2 | PASS | PASS | PASS |
| R3: No text blocks | PASS | PASS | PASS |
| Overall | 4/5 | 4.5/5 | 5/5 |

### Filter 2: Scientific Accuracy & Communication

| Criterion | Option A | Option B | Option C |
|-----------|----------|----------|----------|
| Hierarchy immediately readable (R3, 3-second test) | YES — bars are universally understood | YES — area dominance is pre-attentive | YES — height = maturity is intuitive |
| Qualitative gap OM-85↔CRL1505 conveyed | MODERATE — proportional bars suggest quantitative difference, not qualitative leap | STRONG — 55% vs 7% area makes the gap visceral | STRONGEST — summit vs base camp is a qualitative metaphor, not just quantitative |
| Risk of false equivalence | HIGH — four equal-height slots suggest four comparable products | LOW — grossly different areas prevent false equivalence | LOWEST — products are not even in the same category (different path segments) |
| "Preclinical" status clear for CRL1505 | MODERATE — label says it, but bar format implies it has *some* clinical data | GOOD — dashed border + no dots | BEST — on opposite side of path + bottom position + dashed line |
| Overall | 3/5 | 4/5 | 5/5 |

### Filter 3: Visual Impact (Scroll-Stopping)

| Criterion | Option A | Option B | Option C |
|-----------|----------|----------|----------|
| Novelty (vs. every other GA in Children) | LOW — bar charts are the default in every systematic review GA | MODERATE — unusual but not unprecedented | HIGH — staircase/pathway metaphor is rare in medical GAs |
| Emotional resonance for pediatrician | LOW — a chart to read | MODERATE — visual dominance creates a "wow, OM-85 really is ahead" moment | HIGH — the climb metaphor resonates with the clinical journey from bench to bedside |
| Memorability after 5 seconds | LOW — "I saw a bar chart" | MODERATE — "I saw that one product was much bigger" | HIGH — "I saw a path from lab to clinic, and one product was at the top" |
| Integration with Zone 1-2 narrative flow | WEAK — Zone 3 becomes a standalone infographic | MODERATE — icon reuse connects to Zone 2 | STRONG — the vertical axis echoes the problem→solution→evidence narrative |
| Overall | 2/5 | 3.5/5 | 5/5 |

---

## 3. Zone 2 Integration: Should Products Carry Evidence Indicators?

### The Question

Zone 2 currently shows 4 product icons (capsule, brick, star, bridge) with convergent arrows toward shared mechanisms. Should each icon in Zone 2 also encode its evidence level?

### Analysis

**Arguments FOR integration:**
- The reader who scans Zone 2 (intervention) immediately wonders "but which one should I use?" If evidence is only in Zone 3, they must shift gaze right and mentally re-map products.
- A visual cue on the Zone 2 product icon (opacity, size, border weight) would allow the reader to grasp the hierarchy *before* even reaching Zone 3.

**Arguments AGAINST integration:**
- Zone 2's message is "these 4 products converge on shared mechanisms." Introducing evidence variation here muddies the mechanistic message with clinical maturity — two different axes on one visual.
- MDPI V3 (text budget) is already tight. Adding evidence visual cues to Zone 2 does not add text but adds visual complexity.
- The GA narrative is designed as a LEFT→RIGHT flow: Problem → Intervention → Evidence. Injecting Zone 3's message into Zone 2 breaks the flow and makes Zone 3 redundant.

**Verdict: AGAINST full integration, FOR subtle hinting.**

The recommended approach is a single, minimal encoding in Zone 2 that foreshadows the gradient without competing with the mechanistic message:

**Recommended implementation — opacity gradient on convergent arrows:**
- OM-85's arrow: full opacity (1.0), thick (5px)
- PMBL's arrow: 0.7 opacity, 4px
- MV130's arrow: 0.5 opacity, 3px
- CRL1505's arrow: 0.3 opacity, 2px, dashed

This creates a subtle visual echo: the viewer notices that the arrows "fade" from left to right (or from OM-85 to CRL1505) and this primes them for Zone 3's explicit evidence gradient. The icons themselves remain equal in size and prominence — preserving Zone 2's mechanistic message. The arrows are the only variable.

This approach:
- Preserves Zone 2's primary message (convergent mechanisms)
- Introduces no new text
- Primes the reader for Zone 3 without revealing the full story
- Maintains V5 compliance (OM-85 > PMBL > MV130 > CRL1505 in arrow weight)
- Adds zero cognitive load (arrow opacity difference is pre-attentive)

---

## 4. Verdict

**Option C (Pathway/Trajectory) is the strongest design for Zone 3.**

Scoring summary:

| Filter | A (Bars) | B (Spatial) | C (Pathway) |
|--------|----------|-------------|-------------|
| MDPI compliance | 4/5 | 4.5/5 | 5/5 |
| Scientific accuracy | 3/5 | 4/5 | 5/5 |
| Visual impact | 2/5 | 3.5/5 | 5/5 |
| **Total** | **9/15** | **12/15** | **15/15** |

**Rationale:**

1. **It encodes the manuscript's unique value.** The first comparative synthesis is a story about *where each product stands on the translational journey.* A staircase from lab to bedside IS that story, visually.

2. **Triple redundancy in hierarchy encoding.** Position (height), platform width, and path thickness all independently communicate the same gradient. Even in grayscale, even at 50% zoom, even for a colorblind reader, the hierarchy reads.

3. **It transforms Zone 3 from a chart into a narrative.** Bar charts say "here are numbers." The pathway says "here is a clinical journey — and here is where each product stands on it." This is the difference between information and meaning.

4. **It works with the panoramic format.** Zone 3 is 825px wide and 1680px tall — a strongly vertical space. A vertical pathway exploits this aspect ratio, while horizontal bars fight it (bars are wide objects crammed into a narrow space).

5. **Cross-zone narrative coherence.** Zone 1 = problem (virus, inflammation, vicious cycle). Zone 2 = intervention (products, mechanisms). Zone 3 = "how far along is each solution?" The pathway answers that question in a way bars never can.

**Status: NO NEEDS_FEEDBACK flag required.** The analysis is self-contained and the verdict is clear. If the implementing agent finds a technical constraint I have not foreseen (SVG complexity, render issues at small scale), Option B is the fallback — it shares the core principle of spatial hierarchy but is simpler to implement.

---

## 5. Wireframe Description — Option C (Pathway/Translational Staircase)

This section is precise enough for direct SVG implementation.

### 5.1 Zone 3 Container

```
Rectangle: x=2409, y=0, w=891, h=1680
Fill: vertical linear gradient
  stop 0% (y=0):   #ECFDF5 (pale green — clinical, resolved)
  stop 100% (y=1680): #F5F3FF (pale violet — early, emerging)
Opacity: 0.5
```

### 5.2 Title

```
Text: "Clinical evidence"
Position: x=2854 (center of Zone 3), y=70
Font: Arial, 36px, bold
Fill: #1F2937
Anchor: middle
```

### 5.3 Central Path (Vertical Axis)

```
Axis line: x=2820 (slightly right of Zone 3 center)

Segment 1 — Base to CRL1505 station (y=1540 to y=1300):
  Line: x=2820, y1=1540, y2=1300
  Stroke: #059669, 2px, dash-array="8,6"

Segment 2 — CRL1505 to MV130 (y=1300 to y=920):
  Line: x=2820, y1=1300, y2=920
  Stroke: #7C3AED, 3px, solid

Segment 3 — MV130 to PMBL (y=920 to y=560):
  Line: x=2820, y1=920, y2=560
  Stroke: #0D9488, 4px, solid

Segment 4 — PMBL to OM-85 (y=560 to y=200):
  Line: x=2820, y1=560, y2=200
  Stroke: #2563EB, 6px, solid
```

### 5.4 Station Markers (circles on the path)

```
Station dot size encodes evidence:
  OM-85:   circle cx=2820, cy=200,  r=16, fill=#2563EB, opacity=0.9
  PMBL:    circle cx=2820, cy=560,  r=12, fill=#0D9488, opacity=0.8
  MV130:   circle cx=2820, cy=920,  r=9,  fill=#7C3AED, opacity=0.7
  CRL1505: circle cx=2820, cy=1300, r=6,  fill=#059669, opacity=0.5
```

### 5.5 Platform Shelves (horizontal branches)

Each platform extends LEFT from the path (except CRL1505, which extends RIGHT to signal "different category").

```
OM-85 platform:
  Line: x1=2440, y1=200, x2=2820, y2=200
  Stroke: #2563EB, 4px, solid
  Width: 380px (dominant)

PMBL platform:
  Line: x1=2540, y1=560, x2=2820, y2=560
  Stroke: #0D9488, 3px, solid
  Width: 280px

MV130 platform:
  Line: x1=2640, y1=920, x2=2820, y2=920
  Stroke: #7C3AED, 2px, solid
  Width: 180px

CRL1505 platform:
  Line: x1=2820, y1=1300, x2=3000, y2=1300
  Stroke: #059669, 1.5px, dash-array="6,4"
  Width: 180px — extends RIGHT (opposite side)
```

### 5.6 Product Labels (on platforms)

```
OM-85:
  Product name: "OM-85", x=2460, y=185, font=Arial 42px bold, fill=#2563EB, anchor=start
  Evidence:     "18 RCTs", x=2460, y=230, font=Arial 28px bold, fill=#2563EB, anchor=start, opacity=0.8

PMBL:
  Product name: "PMBL", x=2560, y=545, font=Arial 36px bold, fill=#0D9488, anchor=start
  Evidence:     "5 RCTs", x=2560, y=585, font=Arial 24px, fill=#0D9488, anchor=start, opacity=0.8

MV130:
  Product name: "MV130", x=2660, y=905, font=Arial 32px bold, fill=#7C3AED, anchor=start
  Evidence:     "1 RCT", x=2660, y=942, font=Arial 22px, fill=#7C3AED, anchor=start, opacity=0.8

CRL1505:
  Product name: "CRL1505", x=2840, y=1285, font=Arial 28px bold, fill=#059669, anchor=start
  Evidence:     "Preclinical", x=2840, y=1320, font=Arial 20px, fill=#059669, anchor=start, opacity=0.7
```

### 5.7 Icons (semantic markers at each station)

```
OM-85 — Stethoscope (signals: clinical practice)
  Position: x=2780, y=170 (left of station dot, on platform)
  Size: 40x40 px
  Color: #2563EB, opacity 0.6
  Shape: SVG path — circle head + tube going down and curving

PMBL — Clipboard with checkmark (signals: accumulating evidence)
  Position: x=2510, y=530
  Size: 32x32 px
  Color: #0D9488, opacity 0.5
  [Alternative: magnifying glass over document]

MV130 — Single document page (signals: one study)
  Position: x=2620, y=890
  Size: 28x28 px
  Color: #7C3AED, opacity 0.5

CRL1505 — Flask/beaker (signals: laboratory stage)
  Position: x=3010, y=1270
  Size: 24x24 px
  Color: #059669, opacity 0.4
```

### 5.8 Axis Endpoint Labels

```
Top (clinical):
  Stethoscope mini-icon (20x20) at x=2800, y=120
  Text: "Bedside", x=2850, y=135, font=Arial 22px, fill=#2563EB, opacity=0.5, anchor=start

Bottom (laboratory):
  Flask mini-icon (20x20) at x=2800, y=1560
  Text: "Laboratory", x=2850, y=1575, font=Arial 22px, fill=#059669, opacity=0.5, anchor=start
```

### 5.9 Optional Enhancement: RCT Dots

Small filled circles along the path between stations, representing individual RCTs. These provide a concrete, countable encoding.

```
OM-85 segment (y=200 to y=560): 18 dots
  Positioned at equal intervals along the path
  Each dot: r=5, fill=#2563EB, opacity=0.35
  Spacing: (560-200) / 19 = ~19px apart

PMBL segment (y=560 to y=920): 5 dots
  Each dot: r=4, fill=#0D9488, opacity=0.30
  Spacing: (920-560) / 6 = ~60px apart

MV130 segment (y=920 to y=1300): 1 dot
  Single dot at y=1110 (midpoint)
  r=4, fill=#7C3AED, opacity=0.25

CRL1505 segment (y=1300 to y=1540): 0 dots
  Empty path — reinforces "no pediatric RCTs"
```

This creates a striking visual effect: the upper portion of the path is *dense* with evidence dots, the lower portion is sparse, and the bottom is empty. The density gradient tells the whole story before a single label is read.

### 5.10 Zone 2 Integration (Arrow Opacity Gradient)

To be applied to the existing wireframe v3 arrows from Zone 2 products down to the shared mechanisms:

```
OM-85 arrow:   stroke-opacity=1.0, stroke-width=5, solid
PMBL arrow:    stroke-opacity=0.7, stroke-width=4, solid
MV130 arrow:   stroke-opacity=0.5, stroke-width=3, solid
CRL1505 arrow: stroke-opacity=0.3, stroke-width=2, dash-array="8,4"
```

### 5.11 Word Budget Verification

| Element | Words | Notes |
|---------|-------|-------|
| "Clinical evidence" | 2 | Title |
| "18 RCTs" | 1 | Number + abbreviation |
| "5 RCTs" | 1 | |
| "1 RCT" | 1 | |
| "Preclinical" | 1 | |
| "Bedside" | 1 | Axis top |
| **Total Zone 3 net new** | **7** | Product names shared with Zone 2, not counted |

Budget met: 7 words. Total GA budget = Zone 1 (8) + Zone 2 (12) + Zone 3 (7) = 27 words. Within the 30-word ceiling.

### 5.12 50% Zoom Verification (V7)

At 50% zoom (1650 x 840 px), Zone 3 becomes ~412 x 840 px:
- Path axis and station dots remain clearly visible (proportionally scaled geometric shapes)
- Platform widths maintain their relative differences (380 vs 280 vs 180 vs 180 px → 190 vs 140 vs 90 vs 90)
- Product names at 42/36/32/28 px become 21/18/16/14 px — all above the 8pt minimum (which is ~11px at screen resolution)
- RCT dots at r=5 become r=2.5 — visible as a density pattern even if individual dots blur
- The overall shape — wide at top, narrow at bottom, path thickening upward — reads as a gestalt even at thumbnail size

This is the critical advantage over bars: the staircase shape is recognizable as a shape, whereas four bars of decreasing length at thumbnail become four indistinguishable lines.

---

## 6. Implementation Notes for SVG Agent

1. Build the path segments first (section 5.3), then overlay station markers (5.4), then platforms (5.5), then labels (5.6), then icons (5.7). This layering order prevents occlusion.

2. The RCT dots (5.9) are optional in v1 wireframe — add them in v2 if the base staircase reads well.

3. The CRL1505 platform extending RIGHT is a deliberate design choice. If it creates layout issues at the edge of Zone 3 (x=3000 is well within Zone 3's right boundary at x=3300), there is no problem. If it feels visually unbalanced, the fallback is to extend it left like the others but with a dashed line and smaller platform.

4. The Zone 2 arrow opacity gradient (5.10) is a separate change from Zone 3. It can be implemented independently and tested independently.

5. Icons (5.7) are the last priority. Simple geometric placeholders (circle for stethoscope, triangle for flask) are fine in wireframe stage. Semantic icons come in the visual element sourcing phase (pipeline step 2).
