"""
GA Wireframe v4b — Converged Design with visibility fixes

Based on v4. Fixes applied:
1. PMBL bricks much larger (60x36 at 3x), stroke_width=2
2. Child pictograms enhanced: larger heads, posture, distress/health marks
3. CRL1505 bridge arc: thicker (stroke_width=4), opacity=0.5, organ endpoint icons
4. Zone 2 cross-section larger (+25%), product names positioned around it
5. CRL1505 opacity in Zone 2 raised to 0.55 (evidence hierarchy in staircase, not opacity)
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
C_CYCLE = "#991B1B"

C_OM85 = "#2563EB"
C_PMBL = "#0D9488"
C_MV130 = "#7C3AED"
C_CRL1505 = "#059669"

C_TEXT = "#1F2937"
C_TEXT_MID = "#4B5563"
C_TEXT_LIGHT = "#9CA3AF"

C_AIRWAY_SICK = "#F87171"
C_AIRWAY_HEALTHY = "#34D399"

OUT_DIR = r"C:\Users\reyno\scisense\missions\immunomodulator\artefacts\wireframes"
os.makedirs(OUT_DIR, exist_ok=True)

svg_path = os.path.join(OUT_DIR, "wireframe_GA_v4b.svg")
dwg = svgwrite.Drawing(
    svg_path,
    size=(f"{W}px", f"{H}px"),
    viewBox=f"0 0 {W} {H}",
)

# ═══════════════════════════════════════════════════════════════
# BACKGROUNDS — zone fills
# ═══════════════════════════════════════════════════════════════

dwg.add(dwg.rect((0, 0), (W, H), fill=C_BG))
dwg.add(dwg.rect((0, 0), (Z1_END, H), fill=C_ZONE1_BG, opacity=0.6))
dwg.add(dwg.rect((Z1_END, 0), (Z2_END - Z1_END, H), fill=C_ZONE2_BG, opacity=0.25))
dwg.add(dwg.rect((Z2_END, 0), (Z3_END - Z2_END, H), fill=C_ZONE3_BG, opacity=0.5))


# ═══════════════════════════════════════════════════════════════
# HELPER: Draw concentric bronchial cross-section
# ═══════════════════════════════════════════════════════════════

def draw_bronchial_cross_section(dwg, cx, cy, outer_r, state="sick"):
    """Draw a concentric circular bronchial cross-section.

    state: 'sick', 'transitioning', or 'healthy'
    Returns dict with ring radii for external annotation.
    """
    wall_r = outer_r
    epithelium_r = outer_r * 0.75
    lumen_r = outer_r * 0.50

    if state == "sick":
        # Outer wall — thick, inflamed red
        dwg.add(dwg.circle(center=(cx, cy), r=wall_r,
                           fill="#FCA5A5", opacity=0.25,
                           stroke=C_AIRWAY_SICK, stroke_width=8))
        # Epithelium ring — dashed/broken (porous barrier)
        dwg.add(dwg.circle(center=(cx, cy), r=epithelium_r,
                           fill="none",
                           stroke="#DC2626", stroke_width=5,
                           stroke_dasharray="18,12"))
        # Lumen — white with mucus suggestion
        dwg.add(dwg.circle(center=(cx, cy), r=lumen_r,
                           fill="white", opacity=0.9,
                           stroke="#FCA5A5", stroke_width=2))
        # Mucus dots inside lumen
        for angle_deg, r_frac in [(30, 0.3), (150, 0.25), (250, 0.35)]:
            angle = math.radians(angle_deg)
            mx = cx + lumen_r * r_frac * math.cos(angle)
            my = cy + lumen_r * r_frac * math.sin(angle)
            dwg.add(dwg.circle(center=(mx, my), r=8,
                               fill="#FCD34D", opacity=0.35))

    elif state == "transitioning":
        # Outer wall — medium thickness, amber/healing
        dwg.add(dwg.circle(center=(cx, cy), r=wall_r,
                           fill="#FEF3C7", opacity=0.2,
                           stroke="#FBBF24", stroke_width=5))
        # Epithelium ring — partially broken (some dashes, some solid)
        # Left half dashed (still healing), right half more solid
        # Use a single dashed circle with longer dashes = partially repaired
        dwg.add(dwg.circle(center=(cx, cy), r=epithelium_r,
                           fill="none",
                           stroke="#92400E", stroke_width=4,
                           stroke_dasharray="30,8"))
        # Lumen — clearer
        dwg.add(dwg.circle(center=(cx, cy), r=lumen_r,
                           fill="white", opacity=0.95,
                           stroke="#D4A574", stroke_width=2))

    elif state == "healthy":
        # Outer wall — normal thickness, green
        dwg.add(dwg.circle(center=(cx, cy), r=wall_r,
                           fill="#D1FAE5", opacity=0.2,
                           stroke=C_AIRWAY_HEALTHY, stroke_width=5))
        # Epithelium ring — solid, intact
        dwg.add(dwg.circle(center=(cx, cy), r=epithelium_r,
                           fill="none",
                           stroke="#065F46", stroke_width=4))
        # Lumen — clear, open
        dwg.add(dwg.circle(center=(cx, cy), r=lumen_r,
                           fill="white", opacity=0.95,
                           stroke=C_AIRWAY_HEALTHY, stroke_width=2))

    return {"wall_r": wall_r, "epithelium_r": epithelium_r, "lumen_r": lumen_r}


# ═══════════════════════════════════════════════════════════════
# HELPER: Child pictogram (simple stick figure)
# ═══════════════════════════════════════════════════════════════

def draw_child(dwg, cx, cy, color, healthy=False):
    """Enhanced child pictogram with posture and distress/health marks.

    Zone 1 (healthy=False): larger red-tinted head, drooping posture, cough marks.
    Zone 3 (healthy=True): green-tinted head, upright posture, sparkle marks.
    """
    head_r = 25  # Larger head (~25px radius at 3x)
    # Head — filled with tinted color
    head_fill_opacity = 0.25 if not healthy else 0.2
    dwg.add(dwg.circle(center=(cx, cy), r=head_r,
                       fill=color, opacity=head_fill_opacity,
                       stroke=color, stroke_width=3.5))

    if healthy:
        # ── HEALTHY CHILD: upright posture ──
        body_bottom = cy + head_r + 55
        # Body — straight vertical
        dwg.add(dwg.line((cx, cy + head_r), (cx, body_bottom),
                         stroke=color, stroke_width=3.5))
        # Arms up (V-shape, celebrating)
        arm_y = cy + head_r + 18
        arm_span = 30
        dwg.add(dwg.line((cx, arm_y), (cx - arm_span, arm_y - 22),
                         stroke=color, stroke_width=3.5))
        dwg.add(dwg.line((cx, arm_y), (cx + arm_span, arm_y - 22),
                         stroke=color, stroke_width=3.5))
        # Legs — slightly spread, standing firm
        leg_span = 22
        dwg.add(dwg.line((cx, body_bottom), (cx - leg_span, body_bottom + 38),
                         stroke=color, stroke_width=3.5))
        dwg.add(dwg.line((cx, body_bottom), (cx + leg_span, body_bottom + 38),
                         stroke=color, stroke_width=3.5))
        # ── Sparkle / health marks (3 small stars around head) ──
        for angle_deg, dist in [(35, 38), (145, 36), (90, 42)]:
            angle = math.radians(angle_deg)
            sx = cx + dist * math.cos(angle)
            sy = cy - dist * math.sin(angle)
            # 4-pointed star
            sr = 7
            star_d = (f"M {sx},{sy - sr} L {sx + sr*0.3},{sy - sr*0.3} "
                      f"L {sx + sr},{sy} L {sx + sr*0.3},{sy + sr*0.3} "
                      f"L {sx},{sy + sr} L {sx - sr*0.3},{sy + sr*0.3} "
                      f"L {sx - sr},{sy} L {sx - sr*0.3},{sy - sr*0.3} Z")
            dwg.add(dwg.path(d=star_d, fill=color, opacity=0.45))
        # Small smile on face
        smile_d = f"M {cx - 8},{cy + 5} Q {cx},{cy + 14} {cx + 8},{cy + 5}"
        dwg.add(dwg.path(d=smile_d, fill="none", stroke=color, stroke_width=2, opacity=0.6))

    else:
        # ── SICK CHILD: drooping posture ──
        # Body — slightly tilted/curved to show fatigue
        body_bottom = cy + head_r + 50
        # Curved body (slight leftward droop)
        body_d = f"M {cx},{cy + head_r} Q {cx - 8},{cy + head_r + 30} {cx - 5},{body_bottom}"
        dwg.add(dwg.path(d=body_d, fill="none", stroke=color, stroke_width=3.5))
        # Arms hanging down limply
        arm_y = cy + head_r + 18
        arm_span = 26
        dwg.add(dwg.line((cx - 3, arm_y), (cx - arm_span - 5, arm_y + 25),
                         stroke=color, stroke_width=3))
        dwg.add(dwg.line((cx - 3, arm_y), (cx + arm_span - 2, arm_y + 22),
                         stroke=color, stroke_width=3))
        # Legs — close together, weak stance
        leg_span = 14
        dwg.add(dwg.line((cx - 5, body_bottom), (cx - leg_span - 3, body_bottom + 35),
                         stroke=color, stroke_width=3))
        dwg.add(dwg.line((cx - 5, body_bottom), (cx + leg_span - 3, body_bottom + 35),
                         stroke=color, stroke_width=3))
        # ── Cough / distress marks near head (3 small puff arcs) ──
        for i, (dx, dy) in enumerate([(32, -8), (40, 2), (36, -18)]):
            puff_x = cx + dx
            puff_y = cy + dy
            puff_r = 5 + i * 2
            puff_d = f"M {puff_x},{puff_y - puff_r} A {puff_r},{puff_r} 0 0,1 {puff_x},{puff_y + puff_r}"
            dwg.add(dwg.path(d=puff_d, fill="none",
                             stroke=color, stroke_width=2, opacity=0.5))
        # Sad/unwell expression
        frown_d = f"M {cx - 7},{cy + 8} Q {cx},{cy + 2} {cx + 7},{cy + 8}"
        dwg.add(dwg.path(d=frown_d, fill="none", stroke=color, stroke_width=2, opacity=0.5))


# ═══════════════════════════════════════════════════════════════
# HELPER: Virus icon
# ═══════════════════════════════════════════════════════════════

def draw_virus(dwg, cx, cy, r, color):
    dwg.add(dwg.circle(center=(cx, cy), r=r, fill=color, opacity=0.85))
    for i in range(8):
        angle = i * math.pi / 4
        x1 = cx + r * math.cos(angle)
        y1 = cy + r * math.sin(angle)
        x2 = cx + (r + 10) * math.cos(angle)
        y2 = cy + (r + 10) * math.sin(angle)
        dwg.add(dwg.line((x1, y1), (x2, y2), stroke=color, stroke_width=2.5))
        dwg.add(dwg.circle(center=(x2, y2), r=3.5, fill=color))


# ═══════════════════════════════════════════════════════════════
# ZONE 1 — THE PROBLEM (left ~27%)
# ═══════════════════════════════════════════════════════════════

z1_cx = Z1_END // 2 + 70  # ~516 — shifted right to prevent left-side label clipping
z1_cy = H * 0.44     # Cross-section center (shifted up to leave room for cycle + label)
bronch_r = 140       # Outer radius of cross-section (smaller for clearance)

# Draw sick bronchial cross-section
rings = draw_bronchial_cross_section(dwg, z1_cx, z1_cy, bronch_r, "sick")

# Virus icons penetrating through epithelium gaps
# Position them at the boundary between wall and epithelium
for angle_deg, vr in [(45, 22), (140, 18), (310, 16)]:
    angle = math.radians(angle_deg)
    vx = z1_cx + (rings["epithelium_r"] + 30) * math.cos(angle)
    vy = z1_cy + (rings["epithelium_r"] + 30) * math.sin(angle)
    draw_virus(dwg, vx, vy, vr, C_VIRUS)
    # Penetration arrow toward lumen
    ix = z1_cx + (rings["epithelium_r"] - 15) * math.cos(angle)
    iy = z1_cy + (rings["epithelium_r"] - 15) * math.sin(angle)
    dwg.add(dwg.line((vx, vy), (ix, iy),
                     stroke=C_VIRUS, stroke_width=2, opacity=0.4,
                     stroke_dasharray="5,4"))

# Virus labels
v_style = f"font-family:Arial;font-size:30px;fill:{C_VIRUS};text-anchor:middle;font-weight:bold"
dwg.add(dwg.text("RSV", insert=(z1_cx + 175, z1_cy - 170), style=v_style))
dwg.add(dwg.text("RV", insert=(z1_cx - 160, z1_cy + 10), style=v_style))

# Child pictogram above cross-section (sick/red tint)
draw_child(dwg, z1_cx, z1_cy - bronch_r - 100, C_VIRUS, healthy=False)

# ── Vicious cycle — 4 stations AROUND the cross-section ──
cycle_r = bronch_r + 120  # Radius of the cycle ring (tighter to fit in Zone 1)

# 4 stations at cardinal positions around the cross-section
stations = [
    ("Viral RTIs",        90),   # top
    ("Th2 bias",          0),    # right (shortened from "Th2 inflammation")
    ("Remodeling",        270),  # bottom (shortened from "Airway remodeling")
    ("Re-susceptibility", 180),  # left
]

stn_style_base = "font-family:Arial;font-size:26px;font-weight:bold"

for label, angle_deg in stations:
    angle = math.radians(angle_deg)
    sx = z1_cx + cycle_r * math.cos(angle)
    sy = z1_cy - cycle_r * math.sin(angle)  # SVG y flipped

    # Station dot
    dwg.add(dwg.circle(center=(sx, sy), r=7, fill=C_CYCLE, opacity=0.8))

    # Label positioning depends on station location
    if angle_deg == 90:  # top
        anchor = "middle"
        tx, ty = sx, sy - 20
    elif angle_deg == 0:  # right
        anchor = "start"
        tx, ty = sx + 15, sy + 8
    elif angle_deg == 270:  # bottom
        anchor = "middle"
        tx, ty = sx, sy + 28
    else:  # left
        anchor = "end"
        tx, ty = sx - 12, sy + 8

    stn_style = f"{stn_style_base};fill:{C_CYCLE};text-anchor:{anchor}"
    dwg.add(dwg.text(label, insert=(tx, ty), style=stn_style))

# Arc arrows connecting 4 stations clockwise
# Clockwise visual: top → right → bottom → left → top
# In math angles: 90 → 0 → 270(=-90) → 180 → 90(=450)
arc_pairs = [
    (80, 10),     # top → right
    (350, 280),   # right → bottom
    (260, 190),   # bottom → left
    (170, 100),   # left → top
]

for start_deg, end_deg in arc_pairs:
    s = math.radians(start_deg)
    e = math.radians(end_deg)
    x1 = z1_cx + cycle_r * math.cos(s)
    y1 = z1_cy - cycle_r * math.sin(s)
    x2 = z1_cx + cycle_r * math.cos(e)
    y2 = z1_cy - cycle_r * math.sin(e)

    d = f"M {x1},{y1} A {cycle_r},{cycle_r} 0 0,0 {x2},{y2}"
    dwg.add(dwg.path(d=d, fill="none", stroke=C_CYCLE, stroke_width=2.5, opacity=0.6))

    # Arrowhead at end
    tangent_angle = e - math.pi / 2
    ax = x2 + 12 * math.cos(tangent_angle + 0.3)
    ay = y2 - 12 * math.sin(tangent_angle + 0.3)
    bx = x2 + 12 * math.cos(tangent_angle - 0.3)
    by = y2 - 12 * math.sin(tangent_angle - 0.3)
    dwg.add(dwg.polygon([(x2, y2), (ax, ay), (bx, by)], fill=C_CYCLE, opacity=0.6))

# "Wheezing / Asthma" label below cycle
bottom_style = f"font-family:Arial;font-size:36px;fill:#7F1D1D;text-anchor:middle;font-weight:bold"
dwg.add(dwg.text("Wheezing / Asthma",
                  insert=(z1_cx, z1_cy + cycle_r + 65), style=bottom_style))


# ═══════════════════════════════════════════════════════════════
# ZONE 2 — INTERVENTION (center ~46%)
# ═══════════════════════════════════════════════════════════════

z2_cx = (Z1_END + Z2_END) // 2   # ~1650
z2_cy = H * 0.48                  # Cross-section center (nudged up for bridge room)
bronch2_r = 275                   # 25% larger cross-section for Zone 2 (was 220)

# Header
prod_header = f"font-family:Arial;font-size:36px;fill:{C_TEXT_MID};text-anchor:middle;font-weight:bold"
dwg.add(dwg.text("Immunomodulators",
                  insert=(z2_cx, 55), style=prod_header))

# Draw transitioning bronchial cross-section
rings2 = draw_bronchial_cross_section(dwg, z2_cx, z2_cy, bronch2_r, "transitioning")

# ── Products ACT ON the cross-section ──

# 1. OM-85 SHIELD — arc wrapping OUTSIDE the cross-section (~120 degrees, top)
#    Largest/most prominent. Full opacity.
shield_start = math.radians(150)   # from upper-left
shield_end = math.radians(30)     # to upper-right
shield_r = rings2["wall_r"] + 25

# Draw shield arc
sx1 = z2_cx + shield_r * math.cos(shield_start)
sy1 = z2_cy - shield_r * math.sin(shield_start)
sx2 = z2_cx + shield_r * math.cos(shield_end)
sy2 = z2_cy - shield_r * math.sin(shield_end)

# Thick blue shield arc
shield_d = f"M {sx1},{sy1} A {shield_r},{shield_r} 0 0,0 {sx2},{sy2}"
dwg.add(dwg.path(d=shield_d, fill="none",
                 stroke=C_OM85, stroke_width=14, opacity=1.0))
# Second thinner arc outside for visual weight
shield_r2 = shield_r + 18
sx1b = z2_cx + shield_r2 * math.cos(shield_start)
sy1b = z2_cy - shield_r2 * math.sin(shield_start)
sx2b = z2_cx + shield_r2 * math.cos(shield_end)
sy2b = z2_cy - shield_r2 * math.sin(shield_end)
shield_d2 = f"M {sx1b},{sy1b} A {shield_r2},{shield_r2} 0 0,0 {sx2b},{sy2b}"
dwg.add(dwg.path(d=shield_d2, fill="none",
                 stroke=C_OM85, stroke_width=6, opacity=0.5))

# OM-85 label near the shield
om85_label_angle = math.radians(90)  # top center
om85_lx = z2_cx + (shield_r + 50) * math.cos(om85_label_angle)
om85_ly = z2_cy - (shield_r + 50) * math.sin(om85_label_angle)
om85_style = f"font-family:Arial;font-size:42px;fill:{C_OM85};text-anchor:middle;font-weight:bold"
dwg.add(dwg.text("OM-85", insert=(om85_lx, om85_ly), style=om85_style))

# Small shield icon near label
shield_icon_y = om85_ly - 50
dwg.add(dwg.path(
    d=f"M {om85_lx},{shield_icon_y - 18} "
      f"C {om85_lx + 20},{shield_icon_y - 12} "
      f"  {om85_lx + 20},{shield_icon_y + 6} "
      f"  {om85_lx},{shield_icon_y + 20} "
      f"C {om85_lx - 20},{shield_icon_y + 6} "
      f"  {om85_lx - 20},{shield_icon_y - 12} "
      f"  {om85_lx},{shield_icon_y - 18} Z",
    fill=C_OM85, opacity=0.2,
    stroke=C_OM85, stroke_width=2,
))

# 2. PMBL BRICKS — filling gaps in the epithelium ring (right side)
#    Teal bricks patching the epithelium — LARGER for visibility
brick_positions = []
for angle_deg in [330, 350, 10, 30]:
    angle = math.radians(angle_deg)
    bx = z2_cx + rings2["epithelium_r"] * math.cos(angle)
    by = z2_cy - rings2["epithelium_r"] * math.sin(angle)
    brick_positions.append((bx, by, angle))
    # Draw brick — 60x36 at 3x = 20x12 at delivery
    bw, bh = 60, 36
    # Rotate brick to align with the tangent of the circle
    dwg.add(dwg.rect(
        (bx - bw/2, by - bh/2), (bw, bh),
        rx=4, ry=4,
        fill=C_PMBL, opacity=0.6,
        stroke=C_PMBL, stroke_width=2,
        transform=f"rotate({-angle_deg}, {bx}, {by})"
    ))

# PMBL label (right side of cross-section)
pmbl_lx = z2_cx + rings2["wall_r"] + 65
pmbl_ly = z2_cy + 10
pmbl_style = f"font-family:Arial;font-size:38px;fill:{C_PMBL};text-anchor:start;font-weight:bold"
dwg.add(dwg.text("PMBL", insert=(pmbl_lx, pmbl_ly), style=pmbl_style))

# Small brick icon near PMBL label
for i in range(3):
    bix = pmbl_lx + i * 22
    biy = pmbl_ly + 12
    dwg.add(dwg.rect((bix, biy), (18, 10), rx=2, ry=2,
                      fill=C_PMBL, opacity=0.35,
                      stroke=C_PMBL, stroke_width=1.5))

# 3. MV130 HELIX — zigzag/wave pattern INSIDE the lumen
#    Violet, reprogramming
helix_points = []
num_helix_pts = 12
for i in range(num_helix_pts):
    angle = math.radians(i * 360 / num_helix_pts)
    # Zigzag between two radii inside lumen
    r_inner = rings2["lumen_r"] * 0.3
    r_outer = rings2["lumen_r"] * 0.65
    r = r_inner if i % 2 == 0 else r_outer
    hx = z2_cx + r * math.cos(angle)
    hy = z2_cy + r * math.sin(angle)
    helix_points.append((hx, hy))

# Draw helix as connected path
helix_d = f"M {helix_points[0][0]},{helix_points[0][1]} "
for hx, hy in helix_points[1:]:
    helix_d += f"L {hx},{hy} "
helix_d += "Z"
dwg.add(dwg.path(d=helix_d, fill=C_MV130, fill_opacity=0.08,
                 stroke=C_MV130, stroke_width=3, stroke_opacity=0.5))

# MV130 label — positioned LEFT of cross-section (outside, for visibility)
mv130_lx = z2_cx - rings2["wall_r"] - 65
mv130_ly = z2_cy + 10
mv130_style = f"font-family:Arial;font-size:38px;fill:{C_MV130};text-anchor:end;font-weight:bold"
dwg.add(dwg.text("MV130", insert=(mv130_lx, mv130_ly), style=mv130_style))
# Small helix icon near MV130 label
for i in range(3):
    hix = mv130_lx - 60 + i * 18
    hiy = mv130_ly + 15 + (8 if i % 2 == 0 else -4)
    dwg.add(dwg.circle(center=(hix, hiy), r=5,
                       fill=C_MV130, opacity=0.3))

# 4. CRL1505 BRIDGE — curved arc BELOW the cross-section (gut-lung axis)
#    Green, systemic
bridge_cx = z2_cx
bridge_top_y = z2_cy + rings2["wall_r"] + 20
bridge_bot_y = bridge_top_y + 100
bridge_width = 180

# Bridge arc
bridge_d = (f"M {bridge_cx - bridge_width/2},{bridge_top_y} "
            f"Q {bridge_cx},{bridge_bot_y + 40} "
            f"  {bridge_cx + bridge_width/2},{bridge_top_y}")
dwg.add(dwg.path(d=bridge_d, fill="none",
                 stroke=C_CRL1505, stroke_width=4, opacity=0.55))

# Bridge pillars — thicker, visible
for px in [bridge_cx - bridge_width/2, bridge_cx + bridge_width/2]:
    dwg.add(dwg.line((px, bridge_top_y), (px, bridge_top_y + 40),
                     stroke=C_CRL1505, stroke_width=3, opacity=0.55))

# CRL1505 label below bridge
crl_style = f"font-family:Arial;font-size:34px;fill:{C_CRL1505};text-anchor:middle;font-weight:bold"
dwg.add(dwg.text("CRL1505", insert=(bridge_cx, bridge_bot_y + 55), style=crl_style))

# Gut-lung axis: labeled circles at each end of the bridge
# LEFT endpoint: intestine-like squiggle (gut)
gut_cx = bridge_cx - bridge_width/2
gut_cy = bridge_top_y + 55
dwg.add(dwg.circle(center=(gut_cx, gut_cy), r=20,
                   fill=C_CRL1505, opacity=0.12,
                   stroke=C_CRL1505, stroke_width=2))
# Intestine squiggle inside circle
gut_squig = (f"M {gut_cx - 10},{gut_cy - 8} "
             f"Q {gut_cx - 4},{gut_cy - 12} {gut_cx},{gut_cy - 5} "
             f"Q {gut_cx + 4},{gut_cy + 2} {gut_cx},{gut_cy + 6} "
             f"Q {gut_cx - 4},{gut_cy + 12} {gut_cx + 6},{gut_cy + 10}")
dwg.add(dwg.path(d=gut_squig, fill="none",
                 stroke=C_CRL1505, stroke_width=2, opacity=0.7))
gut_label_style = f"font-family:Arial;font-size:20px;fill:{C_CRL1505};text-anchor:middle;font-weight:bold"
dwg.add(dwg.text("Gut", insert=(gut_cx, gut_cy + 38), style=gut_label_style))

# RIGHT endpoint: lung-like shape
lung_cx = bridge_cx + bridge_width/2
lung_cy = bridge_top_y + 55
dwg.add(dwg.circle(center=(lung_cx, lung_cy), r=20,
                   fill=C_CRL1505, opacity=0.12,
                   stroke=C_CRL1505, stroke_width=2))
# Simplified lung lobes inside
lung_d = (f"M {lung_cx},{lung_cy - 10} "
          f"C {lung_cx - 12},{lung_cy - 6} {lung_cx - 12},{lung_cy + 8} {lung_cx - 2},{lung_cy + 12} "
          f"M {lung_cx},{lung_cy - 10} "
          f"C {lung_cx + 12},{lung_cy - 6} {lung_cx + 12},{lung_cy + 8} {lung_cx + 2},{lung_cy + 12}")
dwg.add(dwg.path(d=lung_d, fill="none",
                 stroke=C_CRL1505, stroke_width=2, opacity=0.7))
lung_label_style = f"font-family:Arial;font-size:20px;fill:{C_CRL1505};text-anchor:middle;font-weight:bold"
dwg.add(dwg.text("Lung", insert=(lung_cx, lung_cy + 38), style=lung_label_style))

# ── IgA convergence label at center of cross-section ──
iga_style = f"font-family:Arial;font-size:36px;fill:{C_TEXT};text-anchor:middle;font-weight:bold"
dwg.add(dwg.rect((z2_cx - 55, z2_cy + rings2["lumen_r"] * 0.3),
                 (110, 44), rx=10, ry=10,
                 fill="white", opacity=0.85))
dwg.add(dwg.text("\u2191 IgA",
                  insert=(z2_cx, z2_cy + rings2["lumen_r"] * 0.3 + 33),
                  style=iga_style))

# ── Opacity note: all products clearly visible in Zone 2 ──
# Evidence hierarchy is communicated by the STAIRCASE in Zone 3, NOT by opacity here.
# OM-85: full opacity (shield arc, stroke_width=14)
# PMBL: 0.6 (bricks, clearly visible)
# MV130: 0.5 stroke (helix inside lumen)
# CRL1505: 0.55 (bridge arc — visible, not hidden)

# Connecting lines from product labels to their action zones (subtle)
# OM-85: label to shield arc
dwg.add(dwg.line((om85_lx, om85_ly + 8), (om85_lx, om85_ly + 30),
                 stroke=C_OM85, stroke_width=2, opacity=0.3))
# PMBL: label to bricks area — horizontal connector
dwg.add(dwg.line((pmbl_lx - 5, pmbl_ly - 6),
                 (z2_cx + rings2["epithelium_r"] + 5, z2_cy),
                 stroke=C_PMBL, stroke_width=1.5, opacity=0.25,
                 stroke_dasharray="8,6"))


# ═══════════════════════════════════════════════════════════════
# ZONE 3 — EVIDENCE + RESOLUTION (right ~27%)
# ═══════════════════════════════════════════════════════════════

z3_cx = (Z2_END + Z3_END) // 2   # ~2855
z3_cy_bronch = H * 0.18          # Upper portion for healthy cross-section (higher up)
bronch3_r = 110                   # Smaller than Zone 1 (more room for staircase)

# Healthy bronchial cross-section
rings3 = draw_bronchial_cross_section(dwg, z3_cx, z3_cy_bronch, bronch3_r, "healthy")

# Child pictogram above (healthy/green)
draw_child(dwg, z3_cx, z3_cy_bronch - bronch3_r - 90, "#059669", healthy=True)

# "Protected airways" label with shield+checkmark
outcome_style = f"font-family:Arial;font-size:32px;fill:#065F46;text-anchor:middle;font-weight:bold"
dwg.add(dwg.text("Protected airways",
                  insert=(z3_cx, z3_cy_bronch + bronch3_r + 40), style=outcome_style))

# Shield+checkmark icon
shield_cx = z3_cx + 130
shield_cy = z3_cy_bronch + bronch3_r + 25
shield_s = 22
dwg.add(dwg.path(
    d=f"M {shield_cx},{shield_cy - shield_s} "
      f"C {shield_cx + shield_s * 1.1},{shield_cy - shield_s * 0.5} "
      f"  {shield_cx + shield_s * 1.1},{shield_cy + shield_s * 0.3} "
      f"  {shield_cx},{shield_cy + shield_s * 1.0} "
      f"C {shield_cx - shield_s * 1.1},{shield_cy + shield_s * 0.3} "
      f"  {shield_cx - shield_s * 1.1},{shield_cy - shield_s * 0.5} "
      f"  {shield_cx},{shield_cy - shield_s} Z",
    fill=C_AIRWAY_HEALTHY, opacity=0.2,
    stroke=C_AIRWAY_HEALTHY, stroke_width=2,
))
# Checkmark
dwg.add(dwg.path(
    d=f"M {shield_cx - 9},{shield_cy} L {shield_cx - 2},{shield_cy + 9} L {shield_cx + 12},{shield_cy - 8}",
    fill="none", stroke=C_AIRWAY_HEALTHY, stroke_width=3,
))

# ── TRANSLATIONAL STAIRCASE (below cross-section) ──
stair_top = z3_cy_bronch + bronch3_r + 80
stair_bottom = H - 80
stair_x = z3_cx - 30  # Central axis slightly left of center

# "Clinical evidence" title
ev_title_style = f"font-family:Arial;font-size:32px;fill:{C_TEXT};text-anchor:middle;font-weight:bold"
dwg.add(dwg.text("Clinical evidence", insert=(z3_cx, stair_top), style=ev_title_style))

stair_path_x = stair_x + 60  # Path axis

# 4 stations along vertical path
stair_total_h = stair_bottom - stair_top - 60
station_spacing = stair_total_h / 4

s1_y = stair_top + 60                    # OM-85 (top = most evidence)
s2_y = stair_top + 60 + station_spacing  # PMBL
s3_y = stair_top + 60 + 2 * station_spacing  # MV130
s4_y = stair_top + 60 + 3 * station_spacing  # CRL1505

# Vertical path segments with varying thickness and color
# Segment 4 (OM-85 to PMBL) — thickest, blue
dwg.add(dwg.line((stair_path_x, s1_y), (stair_path_x, s2_y),
                 stroke=C_OM85, stroke_width=6))
# Segment 3 (PMBL to MV130) — medium, teal
dwg.add(dwg.line((stair_path_x, s2_y), (stair_path_x, s3_y),
                 stroke=C_PMBL, stroke_width=4))
# Segment 2 (MV130 to CRL1505) — thin, violet
dwg.add(dwg.line((stair_path_x, s3_y), (stair_path_x, s4_y),
                 stroke=C_MV130, stroke_width=3))
# Segment 1 (CRL1505 to bottom) — thinnest, dashed, green
dwg.add(dwg.line((stair_path_x, s4_y), (stair_path_x, stair_bottom),
                 stroke=C_CRL1505, stroke_width=2,
                 stroke_dasharray="8,6"))

# Station dots (size encodes evidence)
dwg.add(dwg.circle(center=(stair_path_x, s1_y), r=14,
                   fill=C_OM85, opacity=0.9))
dwg.add(dwg.circle(center=(stair_path_x, s2_y), r=11,
                   fill=C_PMBL, opacity=0.8))
dwg.add(dwg.circle(center=(stair_path_x, s3_y), r=8,
                   fill=C_MV130, opacity=0.7))
dwg.add(dwg.circle(center=(stair_path_x, s4_y), r=6,
                   fill=C_CRL1505, opacity=0.5))

# Platform shelves (horizontal branches)
# OM-85: extends LEFT, widest (350px)
om85_plat_left = stair_path_x - 350
dwg.add(dwg.line((om85_plat_left, s1_y), (stair_path_x, s1_y),
                 stroke=C_OM85, stroke_width=4))

# PMBL: extends LEFT, 260px
pmbl_plat_left = stair_path_x - 260
dwg.add(dwg.line((pmbl_plat_left, s2_y), (stair_path_x, s2_y),
                 stroke=C_PMBL, stroke_width=3))

# MV130: extends LEFT, 170px
mv130_plat_left = stair_path_x - 170
dwg.add(dwg.line((mv130_plat_left, s3_y), (stair_path_x, s3_y),
                 stroke=C_MV130, stroke_width=2))

# CRL1505: extends RIGHT (opposite side! — signals different status), 150px
crl_plat_right = stair_path_x + 150
dwg.add(dwg.line((stair_path_x, s4_y), (crl_plat_right, s4_y),
                 stroke=C_CRL1505, stroke_width=1.5,
                 stroke_dasharray="6,4"))

# Product labels on platforms
# OM-85
om85_ev_style = f"font-family:Arial;font-size:38px;fill:{C_OM85};text-anchor:start;font-weight:bold"
dwg.add(dwg.text("OM-85", insert=(om85_plat_left + 5, s1_y - 15), style=om85_ev_style))
om85_rct_style = f"font-family:Arial;font-size:28px;fill:{C_OM85};text-anchor:start;opacity:0.8"
dwg.add(dwg.text("18 RCTs", insert=(om85_plat_left + 5, s1_y + 30), style=om85_rct_style))

# PMBL
pmbl_ev_style = f"font-family:Arial;font-size:34px;fill:{C_PMBL};text-anchor:start;font-weight:bold"
dwg.add(dwg.text("PMBL", insert=(pmbl_plat_left + 5, s2_y - 12), style=pmbl_ev_style))
pmbl_rct_style = f"font-family:Arial;font-size:24px;fill:{C_PMBL};text-anchor:start;opacity:0.8"
dwg.add(dwg.text("5 RCTs", insert=(pmbl_plat_left + 5, s2_y + 26), style=pmbl_rct_style))

# MV130
mv130_ev_style = f"font-family:Arial;font-size:30px;fill:{C_MV130};text-anchor:start;font-weight:bold"
dwg.add(dwg.text("MV130", insert=(mv130_plat_left + 5, s3_y - 10), style=mv130_ev_style))
mv130_rct_style = f"font-family:Arial;font-size:22px;fill:{C_MV130};text-anchor:start;opacity:0.8"
dwg.add(dwg.text("1 RCT", insert=(mv130_plat_left + 5, s3_y + 22), style=mv130_rct_style))

# CRL1505 (on the RIGHT side of the path)
crl_ev_style = f"font-family:Arial;font-size:28px;fill:{C_CRL1505};text-anchor:start;font-weight:bold"
dwg.add(dwg.text("CRL1505", insert=(stair_path_x + 20, s4_y - 10), style=crl_ev_style))
crl_rct_style = f"font-family:Arial;font-size:20px;fill:{C_CRL1505};text-anchor:start;opacity:0.7"
dwg.add(dwg.text("Preclinical", insert=(stair_path_x + 20, s4_y + 20), style=crl_rct_style))

# RCT dots along the path (density encoding)
# OM-85 segment: 18 dots between s1_y and s2_y
om85_seg_len = s2_y - s1_y
for j in range(18):
    dot_y = s1_y + (j + 1) * om85_seg_len / 19
    dwg.add(dwg.circle(center=(stair_path_x, dot_y), r=4,
                       fill=C_OM85, opacity=0.3))

# PMBL segment: 5 dots between s2_y and s3_y
pmbl_seg_len = s3_y - s2_y
for j in range(5):
    dot_y = s2_y + (j + 1) * pmbl_seg_len / 6
    dwg.add(dwg.circle(center=(stair_path_x, dot_y), r=3.5,
                       fill=C_PMBL, opacity=0.25))

# MV130 segment: 1 dot between s3_y and s4_y
mv130_seg_len = s4_y - s3_y
dot_y = s3_y + mv130_seg_len / 2
dwg.add(dwg.circle(center=(stair_path_x, dot_y), r=3.5,
                   fill=C_MV130, opacity=0.2))

# CRL1505 segment: 0 dots (no pediatric RCTs)

# Axis endpoint labels
bedside_style = f"font-family:Arial;font-size:22px;fill:{C_OM85};text-anchor:start;opacity:0.6"
dwg.add(dwg.text("Bedside", insert=(stair_path_x + 20, s1_y - 35), style=bedside_style))

lab_style = f"font-family:Arial;font-size:22px;fill:{C_CRL1505};text-anchor:start;opacity:0.6"
dwg.add(dwg.text("Laboratory", insert=(stair_path_x + 20, stair_bottom + 20), style=lab_style))


# ═══════════════════════════════════════════════════════════════
# FLOW INDICATORS — subtle chevrons between zones
# ═══════════════════════════════════════════════════════════════

chevron_style = f"font-family:Arial;font-size:60px;fill:#D1D5DB;text-anchor:middle"
# Between Zone 1 and Zone 2
for y_off in [-100, 0, 100]:
    dwg.add(dwg.text("\u203A", insert=(Z1_END, H/2 + y_off), style=chevron_style))
# Between Zone 2 and Zone 3
for y_off in [-100, 0, 100]:
    dwg.add(dwg.text("\u203A", insert=(Z2_END, H/2 + y_off), style=chevron_style))


# ═══════════════════════════════════════════════════════════════
# Save SVG
# ═══════════════════════════════════════════════════════════════

dwg.saveas(svg_path)
print(f"Saved SVG: {svg_path}")


# ═══════════════════════════════════════════════════════════════
# Convert to PNG using Playwright (headless Chromium)
# ═══════════════════════════════════════════════════════════════

full_png = os.path.join(OUT_DIR, "wireframe_GA_v4b_full.png")
delivery_png = os.path.join(OUT_DIR, "wireframe_GA_v4b_delivery.png")

try:
    from playwright.sync_api import sync_playwright
    from PIL import Image

    svg_abs = os.path.abspath(svg_path).replace("\\", "/")
    svg_url = f"file:///{svg_abs}"

    with sync_playwright() as p:
        browser = p.chromium.launch()

        # Full resolution: 3300x1680
        page = browser.new_page(viewport={"width": 3300, "height": 1680})
        page.goto(svg_url)
        page.wait_for_timeout(500)
        page.screenshot(path=full_png, full_page=False)
        page.close()
        print(f"Saved full-res PNG: {full_png}")

        # Delivery size: 1100x560 via resizing the full-res PNG
        try:
            img = Image.open(full_png)
            img_resized = img.resize((1100, 560), Image.LANCZOS)
            img_resized.save(delivery_png)
            print(f"Saved delivery PNG: {delivery_png}")
        except Exception as e2:
            print(f"Delivery resize failed: {e2}")
            # Fallback: render at 1100x560 via HTML wrapper
            page2 = browser.new_page(viewport={"width": 1100, "height": 560})
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
            print(f"Saved delivery PNG (fallback): {delivery_png}")

        browser.close()

except ImportError as e:
    print(f"PNG conversion skipped — missing dependency: {e}")
    print("SVG file is still valid and can be opened in any browser.")

except Exception as e:
    print(f"PNG conversion error: {e}")
    import traceback
    traceback.print_exc()
    print("SVG file is still valid and can be opened in any browser.")
