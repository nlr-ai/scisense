"""
GA Wireframe Generator — Immunomodulator Manuscript MDPI Children
Generates an annotated SVG wireframe at 3300×1680 px (3x working resolution).
Final delivery will be downscaled to 1100×560.
"""

import svgwrite

W, H = 3300, 1680
MARGIN = 60

# Zone boundaries (x positions)
Z1_END = int(W * 0.25)      # 825
Z2_END = int(W * 0.75)      # 2475
Z3_END = W                   # 3300

# Colors
C_BG = "#FAFAFA"
C_ZONE1_BG = "#FEE2E2"      # red-orange pale
C_ZONE2_BG = "#FFF7ED"      # warm neutral
C_ZONE3_BG = "#ECFDF5"      # blue-green pale
C_VIRUS = "#DC2626"
C_OM85 = "#2563EB"
C_PMBL = "#0D9488"
C_MV130 = "#7C3AED"
C_CRL1505 = "#059669"
C_TEXT = "#1F2937"
C_TEXT_LIGHT = "#6B7280"
C_ARROW = "#9CA3AF"
C_EPITHELIUM_SICK = "#F87171"
C_EPITHELIUM_HEALTHY = "#34D399"
C_MUCUS = "#FCD34D"

dwg = svgwrite.Drawing(
    "wireframe_GA.svg",
    size=(f"{W}px", f"{H}px"),
    viewBox=f"0 0 {W} {H}",
)

# ── Background ──
dwg.add(dwg.rect((0, 0), (W, H), fill=C_BG))

# ── Zone backgrounds ──
dwg.add(dwg.rect((0, 0), (Z1_END, H), fill=C_ZONE1_BG, opacity=0.5))
dwg.add(dwg.rect((Z1_END, 0), (Z2_END - Z1_END, H), fill=C_ZONE2_BG, opacity=0.3))
dwg.add(dwg.rect((Z2_END, 0), (Z3_END - Z2_END, H), fill=C_ZONE3_BG, opacity=0.5))

# ── Zone dividers (dashed) ──
for x in [Z1_END, Z2_END]:
    dwg.add(dwg.line((x, 0), (x, H), stroke=C_ARROW, stroke_width=2, stroke_dasharray="12,8"))

# ── Zone labels (top) ──
zone_label_style = "font-family:Arial;font-weight:bold;font-size:28px;fill:#9CA3AF;text-anchor:middle"
dwg.add(dwg.text("ZONE 1 — PROBLÈME", insert=(Z1_END // 2, 36), style=zone_label_style))
dwg.add(dwg.text("ZONE 2 — INTERVENTION + MÉCANISMES", insert=((Z1_END + Z2_END) // 2, 36), style=zone_label_style))
dwg.add(dwg.text("ZONE 3 — ÉVIDENCE CLINIQUE", insert=((Z2_END + Z3_END) // 2, 36), style=zone_label_style))

# ── Percentage labels ──
pct_style = "font-family:Arial;font-size:22px;fill:#D1D5DB;text-anchor:middle"
dwg.add(dwg.text("~25%", insert=(Z1_END // 2, 62), style=pct_style))
dwg.add(dwg.text("~50%", insert=((Z1_END + Z2_END) // 2, 62), style=pct_style))
dwg.add(dwg.text("~25%", insert=((Z2_END + Z3_END) // 2, 62), style=pct_style))


# ══════════════════════════════════════════════════════════════════════
# ZONE 1 — THE PROBLEM
# ══════════════════════════════════════════════════════════════════════

z1_cx = Z1_END // 2  # center x of zone 1
z1_cy = H // 2       # center y

# Airway cross-section (sick) — ellipse representing bronchial lumen
airway_rx, airway_ry = 180, 260
dwg.add(dwg.ellipse(
    center=(z1_cx, z1_cy),
    r=(airway_rx, airway_ry),
    fill="white", stroke=C_EPITHELIUM_SICK, stroke_width=12,
    opacity=0.9,
))

# Thickened wall (outer ring)
dwg.add(dwg.ellipse(
    center=(z1_cx, z1_cy),
    r=(airway_rx + 40, airway_ry + 40),
    fill="none", stroke=C_EPITHELIUM_SICK, stroke_width=8,
    stroke_dasharray="18,10",  # porous/broken
    opacity=0.6,
))

# Label inside airway
airway_label = "font-family:Arial;font-size:24px;fill:#9CA3AF;text-anchor:middle;font-style:italic"
dwg.add(dwg.text("Bronchial lumen", insert=(z1_cx, z1_cy + 8), style=airway_label))
dwg.add(dwg.text("(porous epithelium)", insert=(z1_cx, z1_cy + 38), style=airway_label))

# Mucus blobs
for dx, dy in [(-60, -120), (40, -80), (-20, 100), (70, 60)]:
    dwg.add(dwg.circle(
        center=(z1_cx + dx, z1_cy + dy),
        r=18,
        fill=C_MUCUS, opacity=0.5,
    ))

# Virus icons (simple: circle + spikes)
def draw_virus(dwg, cx, cy, r, color):
    dwg.add(dwg.circle(center=(cx, cy), r=r, fill=color, opacity=0.85))
    # 6 spikes
    import math
    for i in range(6):
        angle = i * math.pi / 3
        x1 = cx + r * math.cos(angle)
        y1 = cy + r * math.sin(angle)
        x2 = cx + (r + 14) * math.cos(angle)
        y2 = cy + (r + 14) * math.sin(angle)
        dwg.add(dwg.line((x1, y1), (x2, y2), stroke=color, stroke_width=4))
        dwg.add(dwg.circle(center=(x2, y2), r=5, fill=color))

draw_virus(dwg, z1_cx - 140, z1_cy - 200, 28, C_VIRUS)
draw_virus(dwg, z1_cx + 100, z1_cy - 260, 22, C_VIRUS)
draw_virus(dwg, z1_cx - 200, z1_cy + 50, 20, C_VIRUS)

# Virus labels
virus_style = "font-family:Arial;font-size:20px;fill:#DC2626;text-anchor:middle;font-weight:bold"
dwg.add(dwg.text("RSV", insert=(z1_cx - 140, z1_cy - 240), style=virus_style))
dwg.add(dwg.text("RV", insert=(z1_cx + 100, z1_cy - 296), style=virus_style))

# ── Vicious cycle arrows ──
# Three text nodes around the airway with curved arrow suggestion
cycle_r = airway_ry + 120
import math

cycle_labels = [
    ("Viral RTIs", -90),           # top
    ("Dysregulated\ninflammation", 30),  # bottom-right
    ("Airway\nremodeling", 210),   # bottom-left  (was 150, moving to separate better)
]

cycle_style = "font-family:Arial;font-size:26px;fill:#991B1B;text-anchor:middle;font-weight:bold"

for label, angle_deg in cycle_labels:
    angle = math.radians(angle_deg)
    tx = z1_cx + (cycle_r + 40) * math.cos(angle)
    ty = z1_cy + (cycle_r + 40) * math.sin(angle)
    lines = label.split("\n")
    for i, line in enumerate(lines):
        dwg.add(dwg.text(line, insert=(tx, ty + i * 30), style=cycle_style))

# Circular arrow (SVG arc path)
# Draw 3 arc segments with arrowheads
def arc_segment(dwg, cx, cy, r, start_deg, end_deg, color, width=4):
    """Draw an arc from start_deg to end_deg."""
    s = math.radians(start_deg)
    e = math.radians(end_deg)
    x1 = cx + r * math.cos(s)
    y1 = cy + r * math.sin(s)
    x2 = cx + r * math.cos(e)
    y2 = cy + r * math.sin(e)
    large = 1 if (end_deg - start_deg) > 180 else 0
    d = f"M {x1},{y1} A {r},{r} 0 {large},1 {x2},{y2}"
    dwg.add(dwg.path(d=d, fill="none", stroke=color, stroke_width=width))
    # Arrowhead at end
    arrow_angle = math.radians(end_deg + 90)  # perpendicular
    ax = x2 + 12 * math.cos(math.radians(end_deg + 20))
    ay = y2 + 12 * math.sin(math.radians(end_deg + 20))
    bx = x2 + 12 * math.cos(math.radians(end_deg - 20))
    by = y2 + 12 * math.sin(math.radians(end_deg - 20))
    dwg.add(dwg.polygon([(x2, y2), (ax, ay), (bx, by)], fill=color))

arc_segment(dwg, z1_cx, z1_cy, cycle_r, -60, -10, "#B91C1C", 5)
arc_segment(dwg, z1_cx, z1_cy, cycle_r, 60, 130, "#B91C1C", 5)
arc_segment(dwg, z1_cx, z1_cy, cycle_r, 180, 250, "#B91C1C", 5)

# Bottom label
wheezing_style = "font-family:Arial;font-size:32px;fill:#7F1D1D;text-anchor:middle;font-weight:bold"
dwg.add(dwg.text("Wheezing / Asthma", insert=(z1_cx, H - 80), style=wheezing_style))


# ══════════════════════════════════════════════════════════════════════
# ZONE 2 — INTERVENTION + MECHANISMS
# ══════════════════════════════════════════════════════════════════════

z2_cx = (Z1_END + Z2_END) // 2  # center of zone 2
z2_left = Z1_END + MARGIN
z2_right = Z2_END - MARGIN

# ── Sub-zone 2A: The 4 agents (top 35%) ──
products = [
    ("OM-85", C_OM85, "capsule"),
    ("PMBL", C_PMBL, "tablet"),
    ("MV130", C_MV130, "spray"),
    ("CRL1505", C_CRL1505, "probiotic"),
]

product_y = 180
product_spacing = (z2_right - z2_left) / 5

for i, (name, color, form) in enumerate(products):
    px = z2_left + product_spacing * (i + 1)

    # Product icon placeholder (rounded rect)
    icon_w, icon_h = 100, 70
    dwg.add(dwg.rect(
        (px - icon_w // 2, product_y - icon_h // 2),
        (icon_w, icon_h),
        rx=15, ry=15,
        fill=color, opacity=0.15,
        stroke=color, stroke_width=3,
    ))

    # Form icon placeholder text
    form_style = f"font-family:Arial;font-size:18px;fill:{color};text-anchor:middle;font-style:italic"
    dwg.add(dwg.text(f"[{form}]", insert=(px, product_y + 6), style=form_style))

    # Product name
    name_style = f"font-family:Arial;font-size:30px;fill:{color};text-anchor:middle;font-weight:bold"
    dwg.add(dwg.text(name, insert=(px, product_y + icon_h // 2 + 40), style=name_style))

    # Convergent arrow down to mechanism zone
    arrow_end_y = 520
    dwg.add(dwg.line(
        (px, product_y + icon_h // 2 + 50),
        (z2_cx, arrow_end_y),
        stroke=color, stroke_width=3, opacity=0.5,
    ))
    # Arrowhead
    dwg.add(dwg.polygon(
        [(z2_cx, arrow_end_y), (z2_cx - 8, arrow_end_y - 16), (z2_cx + 8, arrow_end_y - 16)],
        fill=color, opacity=0.5,
    ))

# Convergence point label
conv_style = "font-family:Arial;font-size:22px;fill:#9CA3AF;text-anchor:middle;font-style:italic"
dwg.add(dwg.text("convergent action", insert=(z2_cx, arrow_end_y + 30), style=conv_style))

# ── Sub-zone 2B: 4 mechanisms (bottom 60%) ──
mech_y_start = 600
mech_spacing_y = 240

mechanisms = [
    ("Epithelial barrier", "Bricks closing / tight junctions", "#F59E0B", "🧱"),
    ("Innate immunity", "DC/Macrophage activating (glow)", "#EF4444", "🔬"),
    ("Adaptive balance", "Th1/Th2 scale rebalancing", "#3B82F6", "⚖️"),
    ("Inflammation control", "Thermostat going down", "#10B981", "🌡️"),
]

for i, (label, description, color, emoji) in enumerate(mechanisms):
    my = mech_y_start + i * mech_spacing_y

    # Icon placeholder (circle)
    icon_cx = z2_cx - 300
    dwg.add(dwg.circle(
        center=(icon_cx, my + 40),
        r=50,
        fill=color, opacity=0.12,
        stroke=color, stroke_width=3,
    ))

    # Emoji placeholder
    emoji_style = f"font-family:Arial;font-size:40px;text-anchor:middle"
    dwg.add(dwg.text(emoji, insert=(icon_cx, my + 55), style=emoji_style))

    # Mechanism label
    mech_label_style = f"font-family:Arial;font-size:32px;fill:{C_TEXT};text-anchor:start;font-weight:bold"
    dwg.add(dwg.text(label, insert=(icon_cx + 80, my + 35), style=mech_label_style))

    # Description annotation (wireframe only, won't be in final)
    desc_style = f"font-family:Arial;font-size:20px;fill:#D1D5DB;text-anchor:start;font-style:italic"
    dwg.add(dwg.text(f"→ {description}", insert=(icon_cx + 80, my + 65), style=desc_style))

# Bracket or connector showing all 4 mechanisms are shared
bracket_x = icon_cx - 80
dwg.add(dwg.line(
    (bracket_x, mech_y_start + 20),
    (bracket_x, mech_y_start + 3 * mech_spacing_y + 60),
    stroke=C_ARROW, stroke_width=3,
))
bracket_label_style = "font-family:Arial;font-size:20px;fill:#9CA3AF;text-anchor:middle;writing-mode:tb"
# Vertical text alongside bracket
for j, ch in enumerate("SHARED MECHANISMS"):
    dwg.add(dwg.text(ch, insert=(bracket_x - 25, mech_y_start + 30 + j * 40),
                     style="font-family:Arial;font-size:20px;fill:#D1D5DB;text-anchor:middle"))


# ══════════════════════════════════════════════════════════════════════
# ZONE 3 — CLINICAL EVIDENCE
# ══════════════════════════════════════════════════════════════════════

z3_cx = (Z2_END + Z3_END) // 2

# Healthy airway
airway3_rx, airway3_ry = 150, 220
dwg.add(dwg.ellipse(
    center=(z3_cx, 400),
    r=(airway3_rx, airway3_ry),
    fill="white", stroke=C_EPITHELIUM_HEALTHY, stroke_width=12,
    opacity=0.9,
))
# Solid outer wall (intact)
dwg.add(dwg.ellipse(
    center=(z3_cx, 400),
    r=(airway3_rx + 35, airway3_ry + 35),
    fill="none", stroke=C_EPITHELIUM_HEALTHY, stroke_width=8,
    opacity=0.6,
))
healthy_label = "font-family:Arial;font-size:24px;fill:#6B7280;text-anchor:middle;font-style:italic"
dwg.add(dwg.text("Healthy airway", insert=(z3_cx, 395), style=healthy_label))
dwg.add(dwg.text("(intact epithelium)", insert=(z3_cx, 425), style=healthy_label))

# ── Evidence gradient bar ──
bar_x = z3_cx - 120
bar_w = 240
bar_top = 750
bar_height = 700
bar_item_h = bar_height // 4

evidence_title = "font-family:Arial;font-size:28px;fill:#1F2937;text-anchor:middle;font-weight:bold"
dwg.add(dwg.text("Clinical evidence", insert=(z3_cx, bar_top - 20), style=evidence_title))

evidence_items = [
    ("OM-85", C_OM85, 1.0, "18 RCTs"),
    ("PMBL", C_PMBL, 0.55, "5 RCTs"),
    ("MV130", C_MV130, 0.30, "1 RCT"),
    ("CRL1505", C_CRL1505, 0.12, "Preclinical"),
]

for i, (name, color, fill_frac, label) in enumerate(evidence_items):
    iy = bar_top + i * bar_item_h

    # Background bar
    dwg.add(dwg.rect(
        (bar_x, iy + 10),
        (bar_w, bar_item_h - 20),
        rx=8, ry=8,
        fill="#E5E7EB",
    ))

    # Filled portion
    dwg.add(dwg.rect(
        (bar_x, iy + 10),
        (bar_w * fill_frac, bar_item_h - 20),
        rx=8, ry=8,
        fill=color, opacity=0.7,
    ))

    # Product name (left of bar)
    name_style = f"font-family:Arial;font-size:26px;fill:{color};text-anchor:end;font-weight:bold"
    dwg.add(dwg.text(name, insert=(bar_x - 15, iy + bar_item_h // 2 + 8), style=name_style))

    # Evidence label (inside bar)
    ev_style = "font-family:Arial;font-size:22px;fill:white;text-anchor:start;font-weight:bold"
    text_x = bar_x + 12
    if fill_frac < 0.3:
        ev_style = f"font-family:Arial;font-size:22px;fill:{color};text-anchor:start;font-weight:bold"
        text_x = bar_x + bar_w * fill_frac + 10
    dwg.add(dwg.text(label, insert=(text_x, iy + bar_item_h // 2 + 8), style=ev_style))

# Arrow from evidence down
arrow_style = "font-family:Arial;font-size:18px;fill:#9CA3AF;text-anchor:middle"
dwg.add(dwg.text("▲ Robust", insert=(z3_cx, bar_top + 4), style=arrow_style))
dwg.add(dwg.text("▼ Emerging", insert=(z3_cx, bar_top + bar_height + 25), style=arrow_style))


# ══════════════════════════════════════════════════════════════════════
# FLOW ARROWS between zones
# ══════════════════════════════════════════════════════════════════════

# Big arrow Zone 1 → Zone 2
for y_offset in [H // 2 - 30, H // 2, H // 2 + 30]:
    pass  # keeping clean

# Thick transition arrow Z1→Z2
arrow_mid_y = H // 2
dwg.add(dwg.polygon(
    [(Z1_END - 30, arrow_mid_y - 50),
     (Z1_END + 50, arrow_mid_y),
     (Z1_END - 30, arrow_mid_y + 50)],
    fill=C_ARROW, opacity=0.3,
))

# Thick transition arrow Z2→Z3
dwg.add(dwg.polygon(
    [(Z2_END - 30, arrow_mid_y - 50),
     (Z2_END + 50, arrow_mid_y),
     (Z2_END - 30, arrow_mid_y + 50)],
    fill=C_ARROW, opacity=0.3,
))


# ══════════════════════════════════════════════════════════════════════
# DIMENSION ANNOTATIONS (wireframe only)
# ══════════════════════════════════════════════════════════════════════

dim_style = "font-family:Arial;font-size:18px;fill:#E5E7EB;text-anchor:middle"
dwg.add(dwg.text(f"{W}px × {H}px (3x working)", insert=(W // 2, H - 20), style=dim_style))
dwg.add(dwg.text("Final: 1100×560 px", insert=(W // 2, H - 4), style=dim_style))


# ── Save ──
import os
out_dir = r"C:\Users\reyno\scisense\missions\immunomodulator"
svg_path = os.path.join(out_dir, "wireframe_GA.svg")
dwg.saveas(svg_path)
print(f"Wireframe saved: {svg_path}")
print(f"Dimensions: {W}×{H} px")
