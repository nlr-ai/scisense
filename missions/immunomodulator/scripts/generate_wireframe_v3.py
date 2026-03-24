"""
GA Wireframe v3 — Immunomodulator Manuscript MDPI Children

Changes from v2:
- P1: Per-product metaphor icons (shield, bricks, helix, bridge) replace generic pills
- P2: PMBL color changed from Teal #0D9488 to Orange #D97706
- P3: Vicious cycle now 4 stations (Viral RTIs, Th2 inflammation, Airway remodeling, Re-susceptibility)
- P4: IgA convergence label where product arrows meet tube
- P5: Mobile-first — min font 36pt, fewer labels, bigger product names
- P6: Mucus blobs smaller & less opaque
- P7: Tube amber zone less saturated (#FFF7ED)
- P8: Product arrows thicker (stroke_width=4)
- P9: Vicious cycle higher contrast (opacity 0.8)
Preserved: continuous tube, 2x2 mechanism grid, evidence gradient bars, shield icon, chevrons
"""

import svgwrite
import math
import os

W, H = 3300, 1680

# Zone boundaries
Z1_END = int(W * 0.27)   # 891
Z2_END = int(W * 0.73)   # 2409
Z3_END = W

# ── Colors ──
C_BG = "#FAFAFA"
C_ZONE1_BG = "#FEF2F2"
C_ZONE2_BG = "#FFFBEB"
C_ZONE3_BG = "#ECFDF5"

C_VIRUS = "#DC2626"
C_VIRUS_LIGHT = "#FCA5A5"
C_CYCLE = "#991B1B"

C_OM85 = "#2563EB"
C_PMBL = "#D97706"        # Changed from Teal to Orange
C_MV130 = "#7C3AED"
C_CRL1505 = "#059669"

C_TEXT = "#1F2937"
C_TEXT_MID = "#4B5563"
C_TEXT_LIGHT = "#9CA3AF"
C_ARROW = "#D1D5DB"

C_AIRWAY_SICK = "#F87171"
C_AIRWAY_TRANS = "#FFF7ED"   # Less saturated amber (was #FBBF24)
C_AIRWAY_TRANS_STROKE = "#FBBF24"  # Keep stroke visible
C_AIRWAY_HEALTHY = "#34D399"

C_MECH_BARRIER = "#D97706"
C_MECH_INNATE = "#DC2626"
C_MECH_ADAPTIVE = "#2563EB"
C_MECH_INFLAM = "#059669"

dwg = svgwrite.Drawing(
    "wireframe_GA_v3.svg",
    size=(f"{W}px", f"{H}px"),
    viewBox=f"0 0 {W} {H}",
)

# ═══════════════════════════════════════════════════════════════
# BACKGROUNDS — subtle gradient zones, no hard borders
# ═══════════════════════════════════════════════════════════════

dwg.add(dwg.rect((0, 0), (W, H), fill=C_BG))
dwg.add(dwg.rect((0, 0), (Z1_END, H), fill=C_ZONE1_BG, opacity=0.6))
dwg.add(dwg.rect((Z1_END, 0), (Z2_END - Z1_END, H), fill=C_ZONE2_BG, opacity=0.2))
dwg.add(dwg.rect((Z2_END, 0), (Z3_END - Z2_END, H), fill=C_ZONE3_BG, opacity=0.5))

# ═══════════════════════════════════════════════════════════════
# CONTINUOUS AIRWAY — a horizontal tube spanning all 3 zones
# narrative spine: sick → healing → healthy
# ═══════════════════════════════════════════════════════════════

airway_y = H * 0.48
tube_h = 120
tube_top = airway_y - tube_h
tube_bot = airway_y + tube_h

# Upper wall
for segment in [
    # Zone 1: dashed (porous epithelium)
    ((80, tube_top), (Z1_END, tube_top), C_AIRWAY_SICK, "12,8", 6),
    # Zone 2: transitioning — stroke uses visible amber, fill is desaturated
    ((Z1_END, tube_top), (Z2_END, tube_top), C_AIRWAY_TRANS_STROKE, "20,4", 5),
    # Zone 3: solid (intact)
    ((Z2_END, tube_top), (W - 80, tube_top), C_AIRWAY_HEALTHY, None, 6),
]:
    start, end, color, dash, sw = segment
    line = dwg.line(start, end, stroke=color, stroke_width=sw)
    if dash:
        line["stroke-dasharray"] = dash
    dwg.add(line)

# Lower wall (mirror)
for segment in [
    ((80, tube_bot), (Z1_END, tube_bot), C_AIRWAY_SICK, "12,8", 6),
    ((Z1_END, tube_bot), (Z2_END, tube_bot), C_AIRWAY_TRANS_STROKE, "20,4", 5),
    ((Z2_END, tube_bot), (W - 80, tube_bot), C_AIRWAY_HEALTHY, None, 6),
]:
    start, end, color, dash, sw = segment
    line = dwg.line(start, end, stroke=color, stroke_width=sw)
    if dash:
        line["stroke-dasharray"] = dash
    dwg.add(line)

# Fill inside tube — gradient suggestion (left=inflamed, right=clear)
dwg.add(dwg.rect((80, tube_top + 6), (Z1_END - 80, tube_h * 2 - 12),
                  fill=C_AIRWAY_SICK, opacity=0.08))
# Zone 2 interior: very light desaturated amber
dwg.add(dwg.rect((Z1_END, tube_top + 5), (Z2_END - Z1_END, tube_h * 2 - 10),
                  fill=C_AIRWAY_TRANS, opacity=0.25))
# Zone 3 interior: greenish
dwg.add(dwg.rect((Z2_END, tube_top + 6), (W - 80 - Z2_END, tube_h * 2 - 12),
                  fill=C_AIRWAY_HEALTHY, opacity=0.08))

# Tube end caps (rounded)
dwg.add(dwg.ellipse(center=(80, airway_y), r=(20, tube_h),
                     fill="none", stroke=C_AIRWAY_SICK, stroke_width=6,
                     stroke_dasharray="12,8"))
dwg.add(dwg.ellipse(center=(W - 80, airway_y), r=(20, tube_h),
                     fill="none", stroke=C_AIRWAY_HEALTHY, stroke_width=6))


# ═══════════════════════════════════════════════════════════════
# ZONE 1 — THE PROBLEM (left ~27%)
# ═══════════════════════════════════════════════════════════════

z1_cx = Z1_END // 2

# ── Virus icons penetrating the tube ──
def draw_virus(dwg, cx, cy, r, color):
    dwg.add(dwg.circle(center=(cx, cy), r=r, fill=color, opacity=0.85))
    for i in range(8):
        angle = i * math.pi / 4
        x1 = cx + r * math.cos(angle)
        y1 = cy + r * math.sin(angle)
        x2 = cx + (r + 12) * math.cos(angle)
        y2 = cy + (r + 12) * math.sin(angle)
        dwg.add(dwg.line((x1, y1), (x2, y2), stroke=color, stroke_width=3))
        dwg.add(dwg.circle(center=(x2, y2), r=4, fill=color))

draw_virus(dwg, 200, tube_top - 80, 26, C_VIRUS)
draw_virus(dwg, 420, tube_top - 110, 20, C_VIRUS)
draw_virus(dwg, 620, tube_top - 60, 18, C_VIRUS)

# Penetration arrows (virus → into tube through gaps)
for vx, vy in [(200, tube_top - 50), (420, tube_top - 86), (620, tube_top - 38)]:
    dwg.add(dwg.line((vx, vy), (vx, tube_top + 15),
                     stroke=C_VIRUS, stroke_width=2, opacity=0.5,
                     stroke_dasharray="6,4"))

# Virus labels — font bumped to 36pt min
v_style = f"font-family:Arial;font-size:36px;fill:{C_VIRUS};text-anchor:middle;font-weight:bold"
dwg.add(dwg.text("RSV", insert=(200, tube_top - 118), style=v_style))
dwg.add(dwg.text("RV", insert=(420, tube_top - 142), style=v_style))

# Mucus blobs inside tube (Zone 1 only) — SMALLER radius, LOWER opacity
for dx, dy in [(-80, -40), (60, 30), (-20, 60)]:
    dwg.add(dwg.circle(center=(z1_cx + dx, airway_y + dy), r=10,
                        fill="#FCD34D", opacity=0.25))

# ── Vicious cycle — 4 stations, higher contrast ──
cycle_cx = z1_cx
cycle_cy = tube_bot + 300
cycle_r = 220  # Use a circle for 4 evenly spaced stations

# Cycle ring (dotted)
dwg.add(dwg.circle(center=(cycle_cx, cycle_cy), r=cycle_r,
                    fill="none", stroke=C_CYCLE, stroke_width=3,
                    stroke_dasharray="8,6", opacity=0.5))

# 4 stations on the cycle (top, right, bottom, left)
stations = [
    ("Viral RTIs",           90,   0, -40),   # top (270 deg in math = top)
    ("Th2 inflammation",     0,    50, 8),     # right
    ("Airway remodeling",    270,  0,  40),    # bottom
    ("Re-susceptibility",    180, -50, 8),     # left
]

stn_style = f"font-family:Arial;font-size:36px;fill:{C_CYCLE};text-anchor:middle;font-weight:bold"

for label, angle_deg_visual, tx_off, ty_off in stations:
    # Convert from visual (0=right, 90=top) to math (0=right, positive=CCW)
    angle = math.radians(angle_deg_visual)
    sx = cycle_cx + cycle_r * 0.7 * math.cos(angle)
    sy = cycle_cy - cycle_r * 0.7 * math.sin(angle)  # minus because SVG y is down

    # Station dot
    dwg.add(dwg.circle(center=(sx, sy), r=8, fill=C_CYCLE, opacity=0.8))

    # Label
    dwg.add(dwg.text(label, insert=(sx + tx_off, sy + ty_off), style=stn_style))

# Arrow arc segments on the cycle path (4 arcs for 4 stations)
# Angles in math convention (0=right, CCW positive)
# Visual: top(90) → right(0) → bottom(270) → left(180) → top(90)
arc_segments = [
    (80, 10),    # top → right
    (350, 280),  # right → bottom
    (260, 190),  # bottom → left
    (170, 100),  # left → top
]

for start_deg, end_deg in arc_segments:
    s = math.radians(start_deg)
    e = math.radians(end_deg)
    x1 = cycle_cx + cycle_r * math.cos(s)
    y1 = cycle_cy - cycle_r * math.sin(s)
    x2 = cycle_cx + cycle_r * math.cos(e)
    y2 = cycle_cy - cycle_r * math.sin(e)

    # Determine sweep direction: we go clockwise (visual), which in SVG is sweep=1
    # but since SVG y is flipped, we need sweep=0 for CW visual
    d = f"M {x1},{y1} A {cycle_r},{cycle_r} 0 0,0 {x2},{y2}"
    dwg.add(dwg.path(d=d, fill="none", stroke=C_CYCLE, stroke_width=3, opacity=0.8))

    # Arrowhead at end
    # Tangent direction at the end point (perpendicular to radius, in CW direction)
    tangent_angle = e - math.pi / 2  # 90 deg CW from radius
    ax = x2 + 14 * math.cos(tangent_angle + 0.3)
    ay = y2 - 14 * math.sin(tangent_angle + 0.3)
    bx = x2 + 14 * math.cos(tangent_angle - 0.3)
    by = y2 - 14 * math.sin(tangent_angle - 0.3)
    dwg.add(dwg.polygon([(x2, y2), (ax, ay), (bx, by)], fill=C_CYCLE, opacity=0.8))

# Connection from cycle to tube
dwg.add(dwg.line((cycle_cx, cycle_cy - cycle_r), (cycle_cx, tube_bot + 20),
                 stroke=C_CYCLE, stroke_width=2, stroke_dasharray="6,4", opacity=0.3))

# Bottom label
bottom_style = f"font-family:Arial;font-size:40px;fill:#7F1D1D;text-anchor:middle;font-weight:bold"
dwg.add(dwg.text("Wheezing / Asthma", insert=(cycle_cx, cycle_cy + cycle_r + 55), style=bottom_style))


# ═══════════════════════════════════════════════════════════════
# ZONE 2 — INTERVENTION + MECHANISMS (center ~46%)
# ═══════════════════════════════════════════════════════════════

z2_cx = (Z1_END + Z2_END) // 2
z2_left = Z1_END + 60
z2_right = Z2_END - 60

# ── 4 products with per-product metaphor icons ──
products = [
    ("OM-85",   C_OM85,    "shield"),
    ("PMBL",    C_PMBL,    "bricks"),
    ("MV130",   C_MV130,   "helix"),
    ("CRL1505", C_CRL1505, "bridge"),
]

product_y = 140
product_spacing = (z2_right - z2_left) / 5


def draw_product_shield(dwg, cx, cy, color):
    """OM-85: Shield with lock symbol."""
    s = 38
    # Shield shape
    dwg.add(dwg.path(
        d=f"M {cx},{cy - s} "
          f"C {cx + s * 1.2},{cy - s * 0.6} "
          f"  {cx + s * 1.2},{cy + s * 0.3} "
          f"  {cx},{cy + s * 1.1} "
          f"C {cx - s * 1.2},{cy + s * 0.3} "
          f"  {cx - s * 1.2},{cy - s * 0.6} "
          f"  {cx},{cy - s} Z",
        fill=color, opacity=0.15,
        stroke=color, stroke_width=3,
    ))
    # Lock body (small rectangle)
    lw, lh = 14, 12
    dwg.add(dwg.rect((cx - lw / 2, cy - 2), (lw, lh), rx=2, ry=2,
                      fill=color, opacity=0.6))
    # Lock shackle (arc)
    dwg.add(dwg.path(
        d=f"M {cx - 6},{cy - 2} A 6,7 0 0,1 {cx + 6},{cy - 2}",
        fill="none", stroke=color, stroke_width=2.5,
    ))


def draw_product_bricks(dwg, cx, cy, color):
    """PMBL: Brick wall being sealed (2-3 bricks with mortar lines)."""
    bw, bh = 24, 14
    gap = 3
    # 3 bricks in 2 rows with offset
    positions = [
        (cx - bw - gap / 2, cy - bh - gap / 2),
        (cx + gap / 2, cy - bh - gap / 2),
        (cx - bw / 2, cy + gap / 2),
    ]
    for x, y in positions:
        dwg.add(dwg.rect((x, y), (bw, bh), rx=2, ry=2,
                          fill=color, opacity=0.2, stroke=color, stroke_width=2))
    # Mortar lines (horizontal + vertical)
    dwg.add(dwg.line((cx - bw - gap, cy - gap / 2), (cx + bw + gap, cy - gap / 2),
                      stroke=color, stroke_width=1.5, opacity=0.5))
    # Sealing effect — glow around bricks
    dwg.add(dwg.circle(center=(cx, cy), r=30, fill=color, opacity=0.06))


def draw_product_helix(dwg, cx, cy, color):
    """MV130: DNA helix / gear-cog icon (programmer metaphor)."""
    # Simple gear/cog
    r_outer = 26
    r_inner = 16
    teeth = 8
    points = []
    for i in range(teeth * 2):
        angle = i * math.pi / teeth - math.pi / 2
        r = r_outer if i % 2 == 0 else r_inner
        points.append((cx + r * math.cos(angle), cy + r * math.sin(angle)))
    dwg.add(dwg.polygon(points, fill=color, opacity=0.15, stroke=color, stroke_width=2))
    # Center dot
    dwg.add(dwg.circle(center=(cx, cy), r=6, fill=color, opacity=0.4))


def draw_product_bridge(dwg, cx, cy, color):
    """CRL1505: Bridge/arc shape (gut-lung bridge metaphor)."""
    # Arc
    arc_w = 48
    arc_h = 24
    dwg.add(dwg.path(
        d=f"M {cx - arc_w / 2},{cy + 10} A {arc_w / 2},{arc_h} 0 0,1 {cx + arc_w / 2},{cy + 10}",
        fill="none", stroke=color, stroke_width=3,
    ))
    # Pillars
    for px_off in [-arc_w / 2, arc_w / 2]:
        dwg.add(dwg.line((cx + px_off, cy + 10), (cx + px_off, cy + 26),
                          stroke=color, stroke_width=3))
    # Labels at bridge ends
    tiny = f"font-family:Arial;font-size:18px;fill:{color};text-anchor:middle;font-weight:bold"
    dwg.add(dwg.text("gut", insert=(cx - arc_w / 2, cy + 40), style=tiny))
    dwg.add(dwg.text("lung", insert=(cx + arc_w / 2, cy + 40), style=tiny))
    # Bridge deck fill
    dwg.add(dwg.rect((cx - arc_w / 2, cy + 6), (arc_w, 6), rx=2, ry=2,
                      fill=color, opacity=0.1))


product_icon_drawers = {
    "shield": draw_product_shield,
    "bricks": draw_product_bricks,
    "helix":  draw_product_helix,
    "bridge": draw_product_bridge,
}

# Store product x positions for IgA label
product_xs = []

for i, (name, color, icon_key) in enumerate(products):
    px = z2_left + product_spacing * (i + 1)
    product_xs.append(px)

    # Product icon (replaces pill)
    icon_cy = product_y - 8
    product_icon_drawers[icon_key](dwg, px, icon_cy, color)

    # Product name — BIGGER (40pt)
    name_style = f"font-family:Arial;font-size:40px;fill:{color};text-anchor:middle;font-weight:bold"
    dwg.add(dwg.text(name, insert=(px, product_y + 60), style=name_style))

    # Arrow down to tube — THICKER (stroke_width=4)
    dwg.add(dwg.line(
        (px, product_y + 75),
        (px, tube_top - 10),
        stroke=color, stroke_width=4, opacity=0.5,
    ))
    # Arrowhead
    dwg.add(dwg.polygon(
        [(px, tube_top - 4), (px - 9, tube_top - 22), (px + 9, tube_top - 22)],
        fill=color, opacity=0.5,
    ))

# ── IgA convergence label at the tube ──
iga_cx = sum(product_xs) / len(product_xs)
iga_style = f"font-family:Arial;font-size:38px;fill:{C_TEXT};text-anchor:middle;font-weight:bold"
# Position it right at the tube top edge, centered among arrows
dwg.add(dwg.rect((iga_cx - 60, tube_top + 8), (120, 46), rx=10, ry=10,
                  fill="white", opacity=0.85))
dwg.add(dwg.text("\u2191 IgA", insert=(iga_cx, tube_top + 42), style=iga_style))

# Label above products
prod_header = f"font-family:Arial;font-size:36px;fill:{C_TEXT_MID};text-anchor:middle;font-weight:bold"
dwg.add(dwg.text("Bacterial-derived immunomodulators", insert=(z2_cx, 55), style=prod_header))


# ═══════════════════════════════════════════════════════════════
# ZONE 2 — 2x2 MECHANISM GRID (below tube)
# ═══════════════════════════════════════════════════════════════

grid_top = tube_bot + 80
grid_left = z2_left + 40
grid_right = z2_right - 40
grid_col_w = (grid_right - grid_left) / 2
grid_row_h = 300

mechanisms = [
    ("Epithelial barrier", C_MECH_BARRIER, 0, 0, "barrier"),
    ("Innate immunity",    C_MECH_INNATE,  1, 0, "innate"),
    ("Adaptive balance",   C_MECH_ADAPTIVE, 0, 1, "adaptive"),
    ("Inflammation control", C_MECH_INFLAM, 1, 1, "inflam"),
]


def draw_barrier_icon(dwg, cx, cy, size, color):
    """Bricks forming a wall."""
    s = size
    rows = 3
    cols = 4
    bw = s * 2 / cols
    bh = s / rows
    for r in range(rows):
        offset = bw / 2 if r % 2 else 0
        for c in range(cols):
            x = cx - s + c * bw + offset
            y = cy - s / 2 + r * bh
            if x + bw > cx + s:
                continue
            dwg.add(dwg.rect((x, y), (bw - 3, bh - 3), rx=2, ry=2,
                             fill=color, opacity=0.2, stroke=color, stroke_width=1.5))


def draw_innate_icon(dwg, cx, cy, size, color):
    """Star/burst — innate immunity activation."""
    points = []
    for i in range(10):
        angle = i * math.pi / 5 - math.pi / 2
        r = size if i % 2 == 0 else size * 0.5
        points.append((cx + r * math.cos(angle), cy + r * math.sin(angle)))
    dwg.add(dwg.polygon(points, fill=color, opacity=0.15, stroke=color, stroke_width=2))
    dwg.add(dwg.circle(center=(cx, cy), r=size * 0.3, fill=color, opacity=0.25))


def draw_adaptive_icon(dwg, cx, cy, size, color):
    """Balance/scale — Th1/Th2 equilibrium."""
    dwg.add(dwg.polygon(
        [(cx, cy + size * 0.4), (cx - size * 0.2, cy + size * 0.7), (cx + size * 0.2, cy + size * 0.7)],
        fill=color, opacity=0.2, stroke=color, stroke_width=2))
    dwg.add(dwg.line((cx - size * 0.8, cy + size * 0.1), (cx + size * 0.8, cy + size * 0.3),
                     stroke=color, stroke_width=3))
    for px_off, py_off, label in [(-size * 0.8, size * 0.1, "Th1"), (size * 0.8, size * 0.3, "Th2")]:
        dwg.add(dwg.circle(center=(cx + px_off, cy + py_off), r=size * 0.2,
                           fill=color, opacity=0.1, stroke=color, stroke_width=1.5))
        lst = f"font-family:Arial;font-size:22px;fill:{color};text-anchor:middle;font-weight:bold"
        dwg.add(dwg.text(label, insert=(cx + px_off, cy + py_off + 8), style=lst))


def draw_inflam_icon(dwg, cx, cy, size, color):
    """Thermometer — inflammation decreasing."""
    dwg.add(dwg.rect((cx - size * 0.15, cy - size * 0.6), (size * 0.3, size * 1.0),
                     rx=size * 0.15, ry=size * 0.15,
                     fill="none", stroke=color, stroke_width=2))
    fill_h = size * 0.35
    dwg.add(dwg.rect((cx - size * 0.12, cy + size * 0.4 - fill_h), (size * 0.24, fill_h),
                     rx=4, ry=4, fill=color, opacity=0.3))
    dwg.add(dwg.circle(center=(cx, cy + size * 0.55), r=size * 0.22,
                       fill=color, opacity=0.2, stroke=color, stroke_width=2))
    ax, ay = cx + size * 0.5, cy
    dwg.add(dwg.line((ax, ay - size * 0.3), (ax, ay + size * 0.3),
                     stroke=color, stroke_width=3))
    dwg.add(dwg.polygon(
        [(ax, ay + size * 0.4), (ax - 8, ay + size * 0.2), (ax + 8, ay + size * 0.2)],
        fill=color))


icon_drawers = {
    "barrier": draw_barrier_icon,
    "innate": draw_innate_icon,
    "adaptive": draw_adaptive_icon,
    "inflam": draw_inflam_icon,
}

for name, color, col, row, icon_key in mechanisms:
    mx = grid_left + col * grid_col_w + grid_col_w / 2
    my = grid_top + row * grid_row_h + grid_row_h / 2

    # Background card
    card_w, card_h = grid_col_w - 40, grid_row_h - 40
    dwg.add(dwg.rect(
        (mx - card_w / 2, my - card_h / 2),
        (card_w, card_h),
        rx=16, ry=16,
        fill="white", opacity=0.7,
        stroke=color, stroke_width=2,
    ))

    # Icon
    icon_cx = mx - card_w / 4
    icon_cy = my - 10
    icon_drawers[icon_key](dwg, icon_cx, icon_cy, 45, color)

    # Label — 36pt min
    label_style = f"font-family:Arial;font-size:36px;fill:{C_TEXT};text-anchor:start;font-weight:bold"
    dwg.add(dwg.text(name, insert=(icon_cx + 65, my - 20), style=label_style))

    # Sub-label — 28pt min
    sub_texts = {
        "barrier": "\u2191 Tight junctions",
        "innate": "DC / Macrophage",
        "adaptive": "Th1/Th2 rebalance",
        "inflam": "\u2193 Cytokine storm",
    }
    sub_style = f"font-family:Arial;font-size:28px;fill:{C_TEXT_LIGHT};text-anchor:start"
    dwg.add(dwg.text(sub_texts[icon_key], insert=(icon_cx + 65, my + 18), style=sub_style))

# "Shared mechanisms" label
shared_style = f"font-family:Arial;font-size:28px;fill:{C_TEXT_LIGHT};text-anchor:middle;letter-spacing:4px"
dwg.add(dwg.text("SHARED MECHANISMS", insert=(z2_cx, grid_top - 10), style=shared_style))


# ═══════════════════════════════════════════════════════════════
# ZONE 3 — CLINICAL EVIDENCE (right ~27%)
# ═══════════════════════════════════════════════════════════════

z3_cx = (Z2_END + Z3_END) // 2

# ── Healthy outcome label (top) ──
outcome_style = f"font-family:Arial;font-size:38px;fill:#065F46;text-anchor:middle;font-weight:bold"
dwg.add(dwg.text("Protected airways", insert=(z3_cx, tube_top - 50), style=outcome_style))

# Shield icon above tube
shield_cx = z3_cx
shield_cy = tube_top - 110
shield_s = 40
dwg.add(dwg.path(
    d=f"M {shield_cx},{shield_cy - shield_s} "
      f"C {shield_cx + shield_s * 1.2},{shield_cy - shield_s * 0.6} "
      f"  {shield_cx + shield_s * 1.2},{shield_cy + shield_s * 0.3} "
      f"  {shield_cx},{shield_cy + shield_s * 1.1} "
      f"C {shield_cx - shield_s * 1.2},{shield_cy + shield_s * 0.3} "
      f"  {shield_cx - shield_s * 1.2},{shield_cy - shield_s * 0.6} "
      f"  {shield_cx},{shield_cy - shield_s} Z",
    fill=C_AIRWAY_HEALTHY, opacity=0.2,
    stroke=C_AIRWAY_HEALTHY, stroke_width=3,
))
# Checkmark inside shield
dwg.add(dwg.path(
    d=f"M {shield_cx - 15},{shield_cy} L {shield_cx - 3},{shield_cy + 14} L {shield_cx + 18},{shield_cy - 12}",
    fill="none", stroke=C_AIRWAY_HEALTHY, stroke_width=4,
))

# ── Evidence gradient (below tube) ──
bar_top = tube_bot + 100
bar_x = z3_cx - 160
bar_w = 320
bar_item_h = 140
bar_gap = 16

ev_title_style = f"font-family:Arial;font-size:36px;fill:{C_TEXT};text-anchor:middle;font-weight:bold"
dwg.add(dwg.text("Clinical evidence", insert=(z3_cx, bar_top - 20), style=ev_title_style))

evidence_items = [
    ("OM-85",   C_OM85,    1.0,  "18 RCTs"),
    ("PMBL",    C_PMBL,    0.55, "5 RCTs"),
    ("MV130",   C_MV130,   0.30, "1 RCT"),
    ("CRL1505", C_CRL1505, 0.12, "Preclinical"),
]

for i, (name, color, fill_frac, label) in enumerate(evidence_items):
    iy = bar_top + i * (bar_item_h + bar_gap)

    # Product name — 36pt
    name_style = f"font-family:Arial;font-size:36px;fill:{color};text-anchor:end;font-weight:bold"
    dwg.add(dwg.text(name, insert=(bar_x - 16, iy + bar_item_h / 2 + 12), style=name_style))

    # Background bar
    dwg.add(dwg.rect(
        (bar_x, iy + 10), (bar_w, bar_item_h - 20),
        rx=10, ry=10, fill="#F3F4F6",
    ))

    # Filled portion
    filled_w = max(bar_w * fill_frac, 30)
    dwg.add(dwg.rect(
        (bar_x, iy + 10), (filled_w, bar_item_h - 20),
        rx=10, ry=10, fill=color, opacity=0.75,
    ))

    # Evidence label
    if fill_frac >= 0.4:
        ev_label_style = f"font-family:Arial;font-size:28px;fill:white;text-anchor:start;font-weight:bold"
        dwg.add(dwg.text(label, insert=(bar_x + 16, iy + bar_item_h / 2 + 10), style=ev_label_style))
    else:
        ev_label_style = f"font-family:Arial;font-size:28px;fill:{color};text-anchor:start;font-weight:bold"
        dwg.add(dwg.text(label, insert=(bar_x + filled_w + 12, iy + bar_item_h / 2 + 10), style=ev_label_style))

# Gradient direction indicators
grad_style = f"font-family:Arial;font-size:24px;fill:{C_TEXT_LIGHT};text-anchor:end"
dwg.add(dwg.text("Robust", insert=(bar_x - 16, bar_top + 30), style=grad_style))
total_h = 4 * bar_item_h + 3 * bar_gap
dwg.add(dwg.text("Emerging", insert=(bar_x - 16, bar_top + total_h - 10), style=grad_style))


# ═══════════════════════════════════════════════════════════════
# FLOW ARROWS — chevrons inside tube
# ═══════════════════════════════════════════════════════════════

chevron_style = f"font-family:Arial;font-size:48px;fill:{C_ARROW};text-anchor:middle"
for cx_pos in [Z1_END - 40, Z1_END + 60, z2_cx - 100, z2_cx + 100, Z2_END - 40, Z2_END + 60]:
    dwg.add(dwg.text("\u203A", insert=(cx_pos, airway_y + 16), style=chevron_style))


# ═══════════════════════════════════════════════════════════════
# Save SVG
# ═══════════════════════════════════════════════════════════════

out_dir = r"C:\Users\reyno\scisense\missions\immunomodulator"
svg_path = os.path.join(out_dir, "wireframe_GA_v3.svg")
dwg.saveas(svg_path)
print(f"Saved SVG: {svg_path}")


# ═══════════════════════════════════════════════════════════════
# Convert to PNG using Playwright (headless Chromium)
# ═══════════════════════════════════════════════════════════════

try:
    from playwright.sync_api import sync_playwright
    from PIL import Image

    svg_abs = os.path.abspath(svg_path).replace("\\", "/")
    svg_url = f"file:///{svg_abs}"

    full_png = os.path.join(out_dir, "wireframe_GA_v3_full.png")
    delivery_png = os.path.join(out_dir, "wireframe_GA_v3_delivery.png")

    with sync_playwright() as p:
        browser = p.chromium.launch()

        # Full resolution: 3300x1680
        page = browser.new_page(viewport={"width": 3300, "height": 1680})
        page.goto(svg_url)
        page.wait_for_timeout(500)
        page.screenshot(path=full_png, full_page=False)
        page.close()
        print(f"Saved full-res PNG: {full_png}")

        # Delivery size: 1100x560
        page2 = browser.new_page(viewport={"width": 1100, "height": 560})
        # Use an HTML wrapper that scales the SVG to fit the viewport
        html_content = f"""<!DOCTYPE html>
        <html><head><style>
        body {{ margin:0; padding:0; overflow:hidden; }}
        img {{ width:1100px; height:560px; }}
        </style></head>
        <body><img src="{svg_url}"></body></html>"""
        page2.set_content(html_content)
        page2.wait_for_timeout(500)
        page2.screenshot(path=delivery_png, full_page=False)
        page2.close()
        print(f"Saved delivery PNG: {delivery_png}")

        browser.close()

except ImportError as e:
    print(f"PNG conversion skipped — missing dependency: {e}")
    print("Install with: pip install playwright && python -m playwright install chromium")
    print("SVG file is still valid and can be opened in any browser or Inkscape")

except Exception as e:
    print(f"PNG conversion error: {e}")
    import traceback
    traceback.print_exc()
    print("SVG file is still valid and can be opened in any browser or Inkscape")
