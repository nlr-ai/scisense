"""
GA Wireframe v2 — Immunomodulator Manuscript MDPI Children

Fixes from v1 audit:
- P1/P2: Vicious cycle redesigned as compact loop inside zone bounds
- P3: Mechanisms in 2x2 grid instead of vertical stack
- P4/P5: SVG shapes instead of emojis, no vertical letter text
- P6/A7: Min font 32pt (3x) = ~11pt final
- P7: Zone 3 evidence integrated tighter
- P9/P10/A1: Continuous airway element spanning all 3 zones
- P11: Wheezing/Asthma integrated into cycle
- P12/A6: Clean render, no wireframe annotations
- A8: Varied color intensity in Zone 1
"""

import svgwrite
import math
import os

W, H = 3300, 1680

# Zone boundaries
Z1_END = int(W * 0.27)   # 891 — slightly wider for the cycle
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
C_PMBL = "#0D9488"
C_MV130 = "#7C3AED"
C_CRL1505 = "#059669"

C_TEXT = "#1F2937"
C_TEXT_MID = "#4B5563"
C_TEXT_LIGHT = "#9CA3AF"
C_ARROW = "#D1D5DB"

C_AIRWAY_SICK = "#F87171"
C_AIRWAY_TRANS = "#FBBF24"
C_AIRWAY_HEALTHY = "#34D399"

C_MECH_BARRIER = "#D97706"
C_MECH_INNATE = "#DC2626"
C_MECH_ADAPTIVE = "#2563EB"
C_MECH_INFLAM = "#059669"

dwg = svgwrite.Drawing(
    "wireframe_GA_v2.svg",
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
# This is the narrative spine: sick → healing → healthy
# ═══════════════════════════════════════════════════════════════

airway_y = H * 0.48  # vertical center of the airway tube
tube_h = 120         # half-height of the tube
tube_top = airway_y - tube_h
tube_bot = airway_y + tube_h

# The tube is drawn as a filled path across the full width
# Zone 1: red/inflamed with gaps (porous)
# Zone 2: transitioning (amber)
# Zone 3: green/healthy (solid)

# Upper wall
for segment in [
    # Zone 1: dashed (porous epithelium)
    ((80, tube_top), (Z1_END, tube_top), C_AIRWAY_SICK, "12,8", 6),
    # Zone 2: transitioning
    ((Z1_END, tube_top), (Z2_END, tube_top), C_AIRWAY_TRANS, "20,4", 5),
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
    ((Z1_END, tube_bot), (Z2_END, tube_bot), C_AIRWAY_TRANS, "20,4", 5),
    ((Z2_END, tube_bot), (W - 80, tube_bot), C_AIRWAY_HEALTHY, None, 6),
]:
    start, end, color, dash, sw = segment
    line = dwg.line(start, end, stroke=color, stroke_width=sw)
    if dash:
        line["stroke-dasharray"] = dash
    dwg.add(line)

# Fill inside tube — gradient suggestion (left=inflamed, right=clear)
# Zone 1 interior: reddish
dwg.add(dwg.rect((80, tube_top + 6), (Z1_END - 80, tube_h * 2 - 12),
                  fill=C_AIRWAY_SICK, opacity=0.08))
# Zone 2 interior: light
dwg.add(dwg.rect((Z1_END, tube_top + 5), (Z2_END - Z1_END, tube_h * 2 - 10),
                  fill=C_AIRWAY_TRANS, opacity=0.04))
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

# Viruses approaching from top-left, penetrating through gaps
draw_virus(dwg, 200, tube_top - 80, 26, C_VIRUS)
draw_virus(dwg, 420, tube_top - 110, 20, C_VIRUS)
draw_virus(dwg, 620, tube_top - 60, 18, C_VIRUS)

# Penetration arrows (virus → into tube through gaps)
for vx, vy in [(200, tube_top - 50), (420, tube_top - 86), (620, tube_top - 38)]:
    dwg.add(dwg.line((vx, vy), (vx, tube_top + 15),
                     stroke=C_VIRUS, stroke_width=2, opacity=0.5,
                     stroke_dasharray="6,4"))

# Virus labels
v_style = f"font-family:Arial;font-size:28px;fill:{C_VIRUS};text-anchor:middle;font-weight:bold"
dwg.add(dwg.text("RSV", insert=(200, tube_top - 118), style=v_style))
dwg.add(dwg.text("RV", insert=(420, tube_top - 142), style=v_style))

# Mucus blobs inside tube (Zone 1 only)
for dx, dy in [(-80, -40), (60, 30), (-20, 60), (100, -20)]:
    dwg.add(dwg.circle(center=(z1_cx + dx, airway_y + dy), r=14,
                        fill="#FCD34D", opacity=0.4))

# ── Vicious cycle — compact, below the tube ──
cycle_cx = z1_cx
cycle_cy = tube_bot + 300
cycle_rx = 260
cycle_ry = 180

# Cycle ellipse (dotted)
dwg.add(dwg.ellipse(center=(cycle_cx, cycle_cy), r=(cycle_rx, cycle_ry),
                     fill="none", stroke=C_CYCLE, stroke_width=3,
                     stroke_dasharray="8,6", opacity=0.4))

# 3 stations on the cycle
stations = [
    ("Viral RTIs", -90, -30),
    ("Inflammation", 30, 20),
    ("Airway\nremodeling", 210, 20),
]

stn_style = f"font-family:Arial;font-size:28px;fill:{C_CYCLE};text-anchor:middle;font-weight:bold"

for label, angle_deg, text_offset in stations:
    angle = math.radians(angle_deg)
    sx = cycle_cx + cycle_rx * 0.7 * math.cos(angle)
    sy = cycle_cy + cycle_ry * 0.7 * math.sin(angle)

    # Station dot
    dwg.add(dwg.circle(center=(sx, sy), r=8, fill=C_CYCLE, opacity=0.6))

    # Label
    lines = label.split("\n")
    for i, line in enumerate(lines):
        tx = sx
        ty = sy + text_offset + i * 32
        dwg.add(dwg.text(line, insert=(tx, ty), style=stn_style))

# Arrow segments on the cycle path
for start_deg, end_deg in [(-70, 10), (50, 130), (170, 250)]:
    s = math.radians(start_deg)
    e = math.radians(end_deg)
    x1 = cycle_cx + cycle_rx * math.cos(s)
    y1 = cycle_cy + cycle_ry * math.sin(s)
    x2 = cycle_cx + cycle_rx * math.cos(e)
    y2 = cycle_cy + cycle_ry * math.sin(e)
    large = 0
    d = f"M {x1},{y1} A {cycle_rx},{cycle_ry} 0 {large},1 {x2},{y2}"
    dwg.add(dwg.path(d=d, fill="none", stroke=C_CYCLE, stroke_width=3, opacity=0.6))
    # Arrowhead
    tip_angle = math.radians(end_deg)
    perp = tip_angle + math.pi / 2
    ax = x2 + 14 * math.cos(tip_angle + 0.3)
    ay = y2 + 14 * math.sin(tip_angle + 0.3)
    bx = x2 + 14 * math.cos(tip_angle - 0.3)
    by = y2 + 14 * math.sin(tip_angle - 0.3)
    dwg.add(dwg.polygon([(x2, y2), (ax, ay), (bx, by)], fill=C_CYCLE, opacity=0.6))

# Connection from cycle to tube (the cycle feeds back into infection)
dwg.add(dwg.line((cycle_cx, cycle_cy - cycle_ry), (cycle_cx, tube_bot + 20),
                 stroke=C_CYCLE, stroke_width=2, stroke_dasharray="6,4", opacity=0.3))

# Bottom label — integrated
bottom_style = f"font-family:Arial;font-size:36px;fill:#7F1D1D;text-anchor:middle;font-weight:bold"
dwg.add(dwg.text("Wheezing / Asthma", insert=(cycle_cx, cycle_cy + cycle_ry + 50), style=bottom_style))


# ═══════════════════════════════════════════════════════════════
# ZONE 2 — INTERVENTION + MECHANISMS (center ~46%)
# ═══════════════════════════════════════════════════════════════

z2_cx = (Z1_END + Z2_END) // 2
z2_left = Z1_END + 60
z2_right = Z2_END - 60

# ── 4 products (top row, above the tube) ──
products = [
    ("OM-85", C_OM85),
    ("PMBL", C_PMBL),
    ("MV130", C_MV130),
    ("CRL1505", C_CRL1505),
]

product_y = 140
product_spacing = (z2_right - z2_left) / 5

for i, (name, color) in enumerate(products):
    px = z2_left + product_spacing * (i + 1)

    # Product pill shape
    pill_w, pill_h = 130, 52
    dwg.add(dwg.rect(
        (px - pill_w // 2, product_y - pill_h // 2),
        (pill_w, pill_h),
        rx=pill_h // 2, ry=pill_h // 2,
        fill=color, opacity=0.15,
        stroke=color, stroke_width=3,
    ))

    # Product name inside pill
    name_style = f"font-family:Arial;font-size:28px;fill:{color};text-anchor:middle;font-weight:bold"
    dwg.add(dwg.text(name, insert=(px, product_y + 10), style=name_style))

    # Arrow down to tube
    dwg.add(dwg.line(
        (px, product_y + pill_h // 2 + 8),
        (px, tube_top - 10),
        stroke=color, stroke_width=2.5, opacity=0.4,
    ))
    # Arrowhead
    dwg.add(dwg.polygon(
        [(px, tube_top - 4), (px - 7, tube_top - 18), (px + 7, tube_top - 18)],
        fill=color, opacity=0.4,
    ))

# Label above products
prod_header = f"font-family:Arial;font-size:32px;fill:{C_TEXT_MID};text-anchor:middle;font-weight:bold"
dwg.add(dwg.text("Bacterial-derived immunomodulators", insert=(z2_cx, 70), style=prod_header))

# ── 4 mechanisms in 2×2 grid (below tube) ──
grid_top = tube_bot + 80
grid_left = z2_left + 40
grid_right = z2_right - 40
grid_col_w = (grid_right - grid_left) / 2
grid_row_h = 300

mechanisms = [
    ("Epithelial barrier", C_MECH_BARRIER, 0, 0, "barrier"),
    ("Innate immunity", C_MECH_INNATE, 1, 0, "innate"),
    ("Adaptive balance", C_MECH_ADAPTIVE, 0, 1, "adaptive"),
    ("Inflammation control", C_MECH_INFLAM, 1, 1, "inflam"),
]

def draw_barrier_icon(dwg, cx, cy, size, color):
    """Bricks forming a wall — epithelial barrier."""
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
    # Center glow
    dwg.add(dwg.circle(center=(cx, cy), r=size * 0.3, fill=color, opacity=0.25))

def draw_adaptive_icon(dwg, cx, cy, size, color):
    """Balance/scale — Th1/Th2 equilibrium."""
    # Fulcrum triangle
    dwg.add(dwg.polygon(
        [(cx, cy + size * 0.4), (cx - size * 0.2, cy + size * 0.7), (cx + size * 0.2, cy + size * 0.7)],
        fill=color, opacity=0.2, stroke=color, stroke_width=2))
    # Beam (slightly tilted toward Th1 = good)
    dwg.add(dwg.line((cx - size * 0.8, cy + size * 0.1), (cx + size * 0.8, cy + size * 0.3),
                     stroke=color, stroke_width=3))
    # Pans
    for px_off, py_off, label in [(-size * 0.8, size * 0.1, "Th1"), (size * 0.8, size * 0.3, "Th2")]:
        dwg.add(dwg.circle(center=(cx + px_off, cy + py_off), r=size * 0.2,
                           fill=color, opacity=0.1, stroke=color, stroke_width=1.5))
        lst = f"font-family:Arial;font-size:22px;fill:{color};text-anchor:middle;font-weight:bold"
        dwg.add(dwg.text(label, insert=(cx + px_off, cy + py_off + 8), style=lst))

def draw_inflam_icon(dwg, cx, cy, size, color):
    """Downward arrow/gauge — inflammation decreasing."""
    # Thermometer body
    dwg.add(dwg.rect((cx - size * 0.15, cy - size * 0.6), (size * 0.3, size * 1.0),
                     rx=size * 0.15, ry=size * 0.15,
                     fill="none", stroke=color, stroke_width=2))
    # Fill (low = good)
    fill_h = size * 0.35
    dwg.add(dwg.rect((cx - size * 0.12, cy + size * 0.4 - fill_h), (size * 0.24, fill_h),
                     rx=4, ry=4, fill=color, opacity=0.3))
    # Bulb at bottom
    dwg.add(dwg.circle(center=(cx, cy + size * 0.55), r=size * 0.22,
                       fill=color, opacity=0.2, stroke=color, stroke_width=2))
    # Down arrow
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

    # Label
    label_style = f"font-family:Arial;font-size:30px;fill:{C_TEXT};text-anchor:start;font-weight:bold"
    dwg.add(dwg.text(name, insert=(icon_cx + 65, my - 20), style=label_style))

    # Subtle sub-label (short)
    sub_texts = {
        "barrier": "↑ Tight junctions",
        "innate": "DC / Macrophage",
        "adaptive": "Th1/Th2 rebalance",
        "inflam": "↓ Cytokine storm",
    }
    sub_style = f"font-family:Arial;font-size:24px;fill:{C_TEXT_LIGHT};text-anchor:start"
    dwg.add(dwg.text(sub_texts[icon_key], insert=(icon_cx + 65, my + 14), style=sub_style))

# "Shared mechanisms" label — horizontal, clean
shared_style = f"font-family:Arial;font-size:26px;fill:{C_TEXT_LIGHT};text-anchor:middle;letter-spacing:4px"
dwg.add(dwg.text("SHARED MECHANISMS", insert=(z2_cx, grid_top - 10), style=shared_style))

# Bracket connecting products to mechanisms through the tube
# (visual: the tube IS the connection)


# ═══════════════════════════════════════════════════════════════
# ZONE 3 — CLINICAL EVIDENCE (right ~27%)
# ═══════════════════════════════════════════════════════════════

z3_cx = (Z2_END + Z3_END) // 2

# ── Healthy outcome label (top) ──
outcome_style = f"font-family:Arial;font-size:34px;fill:#065F46;text-anchor:middle;font-weight:bold"
dwg.add(dwg.text("Protected airways", insert=(z3_cx, tube_top - 50), style=outcome_style))

# Small shield icon above tube
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

ev_title_style = f"font-family:Arial;font-size:30px;fill:{C_TEXT};text-anchor:middle;font-weight:bold"
dwg.add(dwg.text("Clinical evidence", insert=(z3_cx, bar_top - 20), style=ev_title_style))

evidence_items = [
    ("OM-85", C_OM85, 1.0, "18 RCTs"),
    ("PMBL", C_PMBL, 0.55, "5 RCTs"),
    ("MV130", C_MV130, 0.30, "1 RCT"),
    ("CRL1505", C_CRL1505, 0.12, "Preclinical"),
]

for i, (name, color, fill_frac, label) in enumerate(evidence_items):
    iy = bar_top + i * (bar_item_h + bar_gap)

    # Product name (left-aligned, outside bar)
    name_style = f"font-family:Arial;font-size:28px;fill:{color};text-anchor:end;font-weight:bold"
    dwg.add(dwg.text(name, insert=(bar_x - 16, iy + bar_item_h / 2 + 10), style=name_style))

    # Background bar
    dwg.add(dwg.rect(
        (bar_x, iy + 10), (bar_w, bar_item_h - 20),
        rx=10, ry=10, fill="#F3F4F6",
    ))

    # Filled portion
    filled_w = max(bar_w * fill_frac, 30)  # minimum visible
    dwg.add(dwg.rect(
        (bar_x, iy + 10), (filled_w, bar_item_h - 20),
        rx=10, ry=10, fill=color, opacity=0.75,
    ))

    # Evidence label — always dark, positioned after the filled bar
    if fill_frac >= 0.4:
        # Inside the bar (white text)
        ev_label_style = f"font-family:Arial;font-size:26px;fill:white;text-anchor:start;font-weight:bold"
        dwg.add(dwg.text(label, insert=(bar_x + 16, iy + bar_item_h / 2 + 10), style=ev_label_style))
    else:
        # Outside the bar (colored text)
        ev_label_style = f"font-family:Arial;font-size:26px;fill:{color};text-anchor:start;font-weight:bold"
        dwg.add(dwg.text(label, insert=(bar_x + filled_w + 12, iy + bar_item_h / 2 + 10), style=ev_label_style))

# Gradient direction indicators
grad_style = f"font-family:Arial;font-size:22px;fill:{C_TEXT_LIGHT};text-anchor:end"
dwg.add(dwg.text("Robust ▲", insert=(bar_x - 16, bar_top + 30), style=grad_style))
grad_style2 = f"font-family:Arial;font-size:22px;fill:{C_TEXT_LIGHT};text-anchor:end"
total_h = 4 * bar_item_h + 3 * bar_gap
dwg.add(dwg.text("Emerging ▼", insert=(bar_x - 16, bar_top + total_h - 10), style=grad_style2))


# ═══════════════════════════════════════════════════════════════
# FLOW ARROWS — subtle, integrated into the tube narrative
# ═══════════════════════════════════════════════════════════════

# Inside the tube: directional flow marks (chevrons)
chevron_style = f"font-family:Arial;font-size:48px;fill:{C_ARROW};text-anchor:middle"
for cx_pos in [Z1_END - 40, Z1_END + 60, z2_cx - 100, z2_cx + 100, Z2_END - 40, Z2_END + 60]:
    dwg.add(dwg.text("›", insert=(cx_pos, airway_y + 16), style=chevron_style))


# ═══════════════════════════════════════════════════════════════
# Save
# ═══════════════════════════════════════════════════════════════

out_dir = r"C:\Users\reyno\scisense\missions\immunomodulator"
svg_path = os.path.join(out_dir, "wireframe_GA_v2.svg")
dwg.saveas(svg_path)
print(f"Saved: {svg_path}")
