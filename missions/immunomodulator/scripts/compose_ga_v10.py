"""
Parametric GA Compositor V10 — "La Bronche Vivante"

4-band bronchial cross-section (longitudinal view):
  Band 1: LUMEN — virus entry (left) → IgA protection (right)
  Band 2: EPITHELIUM — broken barrier → sealed (OM-85 shield + PMBL staples)
  Band 3: LAMINA PROPRIA — dormant DC/Th2 → activated DC/trained immunity/Th1-Th2 balance
  Band 4: MUSCLE LISSE — thickened inflamed → thin resolved

Reads config/layout_v10.yaml + config/palette.yaml + config/content.yaml
Produces: wireframe_GA_v10.svg + _full.png + _delivery.png
"""

import yaml
import svgwrite
import os
import math
import json
import random

BASE = r"C:\Users\reyno\scisense\missions\immunomodulator"
CONFIG_DIR = os.path.join(BASE, "config")
OUT_DIR = os.path.join(BASE, "artefacts", "wireframes")
os.makedirs(OUT_DIR, exist_ok=True)


# ═══════════════════════════════════════════════════════════════
# UTILITIES (reused from v9)
# ═══════════════════════════════════════════════════════════════

def _lighten_hex(hex_color, factor=0.35):
    h = hex_color.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    r = int(r + (255 - r) * factor)
    g = int(g + (255 - g) * factor)
    b = int(b + (255 - b) * factor)
    return f"#{r:02x}{g:02x}{b:02x}"


def _lerp_color(c1, c2, t):
    """Linearly interpolate between two hex colors. t=0→c1, t=1→c2."""
    h1, h2 = c1.lstrip("#"), c2.lstrip("#")
    r = int(int(h1[0:2], 16) * (1 - t) + int(h2[0:2], 16) * t)
    g = int(int(h1[2:4], 16) * (1 - t) + int(h2[2:4], 16) * t)
    b = int(int(h1[4:6], 16) * (1 - t) + int(h2[4:6], 16) * t)
    return f"#{r:02x}{g:02x}{b:02x}"


def _catmull_rom_to_bezier(points):
    """Convert Catmull-Rom spline control points to cubic Bézier segments."""
    if len(points) < 4:
        return []
    segments = []
    for i in range(1, len(points) - 2):
        p0, p1, p2, p3 = points[i - 1], points[i], points[i + 1], points[i + 2]
        cp1x = p1[0] + (p2[0] - p0[0]) / 6
        cp1y = p1[1] + (p2[1] - p0[1]) / 6
        cp2x = p2[0] - (p3[0] - p1[0]) / 6
        cp2y = p2[1] - (p3[1] - p1[1]) / 6
        segments.append(((cp1x, cp1y), (cp2x, cp2y), (p2[0], p2[1])))
    return segments


def load_config():
    config = {}
    for name in ("palette", "content"):
        path = os.path.join(CONFIG_DIR, f"{name}.yaml")
        with open(path, "r", encoding="utf-8") as f:
            config[name] = yaml.safe_load(f)
    # V10 layout
    path = os.path.join(CONFIG_DIR, "layout_v10.yaml")
    with open(path, "r", encoding="utf-8") as f:
        config["layout"] = yaml.safe_load(f)
    return config


def resolve_color(palette, key):
    parts = key.split(".")
    val = palette
    for p in parts:
        if isinstance(val, dict):
            val = val.get(p, "#888888")
        else:
            return "#888888"
    return val


# ═══════════════════════════════════════════════════════════════
# CONTOUR DATA (reused from v9 — extracted from AI images)
# ═══════════════════════════════════════════════════════════════

_CONTOUR_SICK = None
_CONTOUR_HEALTHY = None


def _load_contours():
    global _CONTOUR_SICK, _CONTOUR_HEALTHY
    contour_dir = os.path.join(BASE, "artefacts", "contours")
    for fname, target in [("S3_sick_points.json", "sick"),
                          ("S4_healthy_points.json", "healthy")]:
        path = os.path.join(contour_dir, fname)
        if os.path.exists(path):
            with open(path, "r") as f:
                data = json.load(f)
            pts = data["points"] if isinstance(data, dict) else data
            if target == "sick":
                _CONTOUR_SICK = pts
            else:
                _CONTOUR_HEALTHY = pts


# ═══════════════════════════════════════════════════════════════
# LAYOUT HELPERS
# ═══════════════════════════════════════════════════════════════

def get_zone_rect(layout, zone_key, W, H):
    z = layout["zones"][zone_key]
    x = int(W * z["x_pct"])
    w = int(W * z["width_pct"])
    return x, 0, w, H


def get_bronchus_rect(layout, W, H):
    """Return (x, y, w, h) of the bronchus area."""
    bz = layout["zones"]["bronchus"]
    bx = int(W * bz["x_pct"])
    bw = int(W * bz["width_pct"])
    by = int(H * layout["bronchus"]["y_start_pct"])
    bh = int(H * (layout["bronchus"]["y_end_pct"] - layout["bronchus"]["y_start_pct"]))
    return bx, by, bw, bh


def get_band_rects(layout, W, H):
    """Return dict of band_name → (x, y, w, h) for each anatomical band."""
    bx, by, bw, bh = get_bronchus_rect(layout, W, H)
    bands = layout["bronchus"]["bands"]
    result = {}
    cum_y = by
    for band_name in ("lumen", "epithelium", "lamina", "muscle"):
        band_h = int(bh * bands[band_name]["height_pct"])
        result[band_name] = (bx, cum_y, bw, band_h)
        cum_y += band_h
    return result


def health_at_x(x, bx, bw):
    """Return H value (0→1) based on x position within bronchus."""
    if bw == 0:
        return 0.5
    t = (x - bx) / bw
    return max(0.0, min(1.0, t))


# ═══════════════════════════════════════════════════════════════
# DRAWING: BACKGROUND + GRADIENT
# ═══════════════════════════════════════════════════════════════

def draw_background(dwg, layout, palette, W, H):
    dwg.add(dwg.rect((0, 0), (W, H), fill=palette["background"]))

    grad = layout["gradient"]
    lg = dwg.linearGradient(("0%", "0%"), ("100%", "0%"), id="bg_grad")
    lg.add_stop_color("0%", grad["left_color"])
    lg.add_stop_color("50%", grad["center_color"])
    lg.add_stop_color("100%", grad["right_color"])
    dwg.defs.add(lg)
    dwg.add(dwg.rect((0, 0), (W, H), fill="url(#bg_grad)", opacity=0.6))


# ═══════════════════════════════════════════════════════════════
# DRAWING: BRONCHUS FRAME + BAND SEPARATORS
# ═══════════════════════════════════════════════════════════════

def draw_bronchus_frame(dwg, layout, palette, W, H):
    bx, by, bw, bh = get_bronchus_rect(layout, W, H)
    bc = layout["bronchus"]

    # Outer frame
    dwg.add(dwg.rect(
        (bx, by), (bw, bh),
        rx=bc["corner_radius"], ry=bc["corner_radius"],
        fill="none",
        stroke=bc["border_color"],
        stroke_width=bc["border_width"]
    ))

    # Band background fills (subtle alternation)
    bands = get_band_rects(layout, W, H)
    band_fills = {
        "lumen": palette["bands"]["lumen"],
        "epithelium": palette["bands"]["lamina_bg"],
        "lamina": palette["bands"]["lumen"],
        "muscle": palette["bands"]["lamina_bg"],
    }
    for bname, (bx2, by2, bw2, bh2) in bands.items():
        dwg.add(dwg.rect((bx2, by2), (bw2, bh2),
                         fill=band_fills.get(bname, "#FFFFFF"),
                         opacity=0.3))

    # Separator lines between bands
    sep_w = bc["separator_width"]
    sep_c = bc["separator_color"]
    sep_d = bc.get("separator_dash", "8,4")
    band_list = list(bands.values())
    for i in range(len(band_list) - 1):
        _, by_i, bw_i, bh_i = band_list[i]
        y_sep = by_i + bh_i
        dwg.add(dwg.line(
            (bx, y_sep), (bx + bw, y_sep),
            stroke=sep_c, stroke_width=sep_w,
            stroke_dasharray=sep_d
        ))


# ═══════════════════════════════════════════════════════════════
# DRAWING: BAND 1 — LUMEN
# ═══════════════════════════════════════════════════════════════

def draw_virus_icon(dwg, cx, cy, r, color):
    """Simple virus: circle + spikes."""
    dwg.add(dwg.circle((cx, cy), r, fill=color, opacity=0.85))
    spike_count = 8
    spike_len = r * 0.65
    tip_r = r * 0.18
    for i in range(spike_count):
        angle = 2 * math.pi * i / spike_count
        sx = cx + (r + spike_len) * math.cos(angle)
        sy = cy + (r + spike_len) * math.sin(angle)
        dwg.add(dwg.line((cx + r * 0.9 * math.cos(angle),
                          cy + r * 0.9 * math.sin(angle)),
                         (sx, sy),
                         stroke=color, stroke_width=2))
        dwg.add(dwg.circle((sx, sy), tip_r, fill=color))


def draw_iga_y(dwg, cx, cy, height, color):
    """IgA secretory antibody Y shape."""
    stem_h = height * 0.55
    arm_h = height * 0.45
    arm_spread = height * 0.35
    sw = max(3, height * 0.15)
    # Stem
    dwg.add(dwg.line((cx, cy), (cx, cy - stem_h),
                     stroke=color, stroke_width=sw, stroke_linecap="round"))
    # Left arm
    dwg.add(dwg.line((cx, cy - stem_h), (cx - arm_spread, cy - stem_h - arm_h),
                     stroke=color, stroke_width=sw, stroke_linecap="round"))
    # Right arm
    dwg.add(dwg.line((cx, cy - stem_h), (cx + arm_spread, cy - stem_h - arm_h),
                     stroke=color, stroke_width=sw, stroke_linecap="round"))


def draw_lumen(dwg, layout, palette, W, H):
    bx, by, bw, bh = get_band_rects(layout, W, H)["lumen"]
    bc = layout["band_content"]["lumen"]
    virus_color = palette["virus"]

    # Viruses on the left
    random.seed(42)
    for i in range(bc["virus_count"]):
        vx_min = bx + int(bw * bc["virus_x_range"][0])
        vx_max = bx + int(bw * bc["virus_x_range"][1])
        vx = random.randint(vx_min, vx_max)
        vy = by + int(bh * 0.3) + random.randint(0, int(bh * 0.4))
        draw_virus_icon(dwg, vx, vy, bc["virus_radius"], virus_color)

    # Red arrows showing virus direction
    for i in range(2):
        ax = bx + int(bw * 0.15) + i * int(bw * 0.12)
        ay = by + int(bh * 0.5)
        dwg.add(dwg.line((ax, ay), (ax + 40, ay),
                         stroke=virus_color, stroke_width=3,
                         opacity=0.5))
        # Arrowhead
        dwg.add(dwg.polygon(
            [(ax + 40, ay - 6), (ax + 52, ay), (ax + 40, ay + 6)],
            fill=virus_color, opacity=0.5
        ))

    # === FIX 1: IgA CONVERGENCE POINT ===
    # 4 colored curved lines (one per product) converging from mid-bronchus
    # toward the IgA focal point on the right
    convergence_x = bx + int(bw * 0.65)  # focal point where lines converge
    convergence_y = by + int(bh * 0.55)   # vertical center of lumen band

    product_colors = [
        palette["products"]["om85"],
        palette["products"]["pmbl"],
        palette["products"]["mv130"],
        palette["products"]["crl1505"],
    ]
    # Each line starts from a different vertical offset in the mid-bronchus area
    # and curves toward the convergence point
    line_origins = [
        (bx + int(bw * 0.35), by + int(bh * 0.20)),  # om85 - top
        (bx + int(bw * 0.38), by + int(bh * 0.40)),  # pmbl - upper-mid
        (bx + int(bw * 0.36), by + int(bh * 0.60)),  # mv130 - lower-mid
        (bx + int(bw * 0.40), by + int(bh * 0.80)),  # crl1505 - bottom
    ]
    for (ox, oy), color in zip(line_origins, product_colors):
        # Quadratic Bezier: origin -> control point -> convergence
        # Control point is midway, with slight vertical bias toward convergence_y
        ctrl_x = (ox + convergence_x) * 0.5 + 15
        ctrl_y = (oy + convergence_y) * 0.5
        path_d = f"M {ox},{oy} Q {ctrl_x},{ctrl_y} {convergence_x},{convergence_y}"
        dwg.add(dwg.path(d=path_d, fill="none",
                         stroke=color, stroke_width=2.5,
                         opacity=0.45, stroke_linecap="round"))

    # IgA Y antibodies on the right — clustered around the convergence focal point
    iga_colors = [
        palette["products"]["om85"],
        palette["products"]["pmbl"],
        palette["products"]["mv130"],
        palette["products"]["crl1505"],
    ]
    for i in range(bc["iga_count"]):
        # Cluster the Y shapes around the convergence point, spreading rightward
        ix_start = convergence_x + 10
        ix_end = bx + int(bw * bc["iga_x_range"][1])
        ix = ix_start + int((ix_end - ix_start) * i / max(1, bc["iga_count"] - 1))
        iy = by + int(bh * 0.75)
        color_i = iga_colors[i % len(iga_colors)]
        draw_iga_y(dwg, ix, iy, bc["iga_height"], color_i)

    # Small convergence glow at focal point
    dwg.add(dwg.circle((convergence_x, convergence_y), 12,
                       fill="#FFFFFF", opacity=0.4))
    dwg.add(dwg.circle((convergence_x, convergence_y), 8,
                       fill="#059669", opacity=0.15))

    # "LUMEN" label (tiny, top-left of band)
    # dwg.add(dwg.text("LUMEN", insert=(bx + 10, by + 20),
    #                  font_size=18, fill="#9CA3AF", font_family="Helvetica, Arial, sans-serif"))


# ═══════════════════════════════════════════════════════════════
# DRAWING: BAND 2 — EPITHELIUM
# ═══════════════════════════════════════════════════════════════

def draw_epithelium(dwg, layout, palette, W, H):
    bx, by, bw, bh = get_band_rects(layout, W, H)["epithelium"]
    bc = layout["band_content"]["epithelium"]
    n_cells = bc["cell_count"]
    cell_w = bw / n_cells
    cell_h = int(bh * bc["cell_height_pct"])
    cell_y = by + (bh - cell_h) // 2

    # Determine gaps (sick side = left)
    gap_indices = set()
    random.seed(7)
    sick_cell_limit = n_cells // 3  # leftmost third has gaps
    candidates = list(range(sick_cell_limit))
    random.shuffle(candidates)
    for g in candidates[:bc["gap_count_sick"]]:
        gap_indices.add(g)

    om85_color = palette["products"]["om85"]
    pmbl_color = palette["products"]["pmbl"]

    for i in range(n_cells):
        cx = bx + int(i * cell_w)
        t = i / max(1, n_cells - 1)  # 0=left(sick) → 1=right(healthy)

        # Cell color transitions from red-ish to green-ish
        cell_color = _lerp_color(
            palette["bands"]["epithelium_sick"],
            palette["bands"]["epithelium_healthy"],
            t
        )

        if i in gap_indices:
            # Gap: draw cell smaller with visible break
            gap_size = int(cell_w * 0.35)
            dwg.add(dwg.rect(
                (cx, cell_y), (int(cell_w) - gap_size, cell_h),
                fill=cell_color, stroke="#D1D5DB", stroke_width=1,
                rx=2, ry=2
            ))
            # Red gap indicator
            dwg.add(dwg.rect(
                (cx + int(cell_w) - gap_size, cell_y + int(cell_h * 0.1)),
                (gap_size - 2, int(cell_h * 0.8)),
                fill=palette["virus"], opacity=0.2
            ))
        else:
            # Intact cell
            dwg.add(dwg.rect(
                (cx + 1, cell_y), (int(cell_w) - 2, cell_h),
                fill=cell_color, stroke="#D1D5DB", stroke_width=1,
                rx=2, ry=2
            ))

            # PMBL staples between cells (right portion)
            if t > 0.45 and i > 0 and i not in gap_indices:
                staple_x = cx
                staple_y1 = cell_y + int(cell_h * 0.25)
                staple_y2 = cell_y + int(cell_h * 0.75)
                # Small teal bracket between cells
                dwg.add(dwg.line(
                    (staple_x, staple_y1), (staple_x, staple_y2),
                    stroke=pmbl_color, stroke_width=3, opacity=0.7
                ))
                # Small horizontal ticks
                dwg.add(dwg.line(
                    (staple_x - 3, staple_y1), (staple_x + 3, staple_y1),
                    stroke=pmbl_color, stroke_width=2
                ))
                dwg.add(dwg.line(
                    (staple_x - 3, staple_y2), (staple_x + 3, staple_y2),
                    stroke=pmbl_color, stroke_width=2
                ))

    # OM-85 shield on surface (transition zone)
    shield_x = bx + int(bw * bc["shield_x_pct"])
    shield_y = cell_y - 10
    shield_w, shield_h = 50, 55
    # Shield shape (rounded trapezoid)
    shield_path = f"M {shield_x},{shield_y} "
    shield_path += f"L {shield_x + shield_w},{shield_y} "
    shield_path += f"L {shield_x + shield_w},{shield_y + shield_h * 0.7} "
    shield_path += f"Q {shield_x + shield_w / 2},{shield_y + shield_h} {shield_x},{shield_y + shield_h * 0.7} Z"
    dwg.add(dwg.path(d=shield_path, fill=om85_color, opacity=0.6,
                     stroke=om85_color, stroke_width=2))
    # Lock icon in center
    lock_cx = shield_x + shield_w / 2
    lock_cy = shield_y + shield_h * 0.45
    dwg.add(dwg.circle((lock_cx, lock_cy), 6, fill="none",
                       stroke="white", stroke_width=2))
    dwg.add(dwg.rect((lock_cx - 5, lock_cy + 3), (10, 8),
                     fill="white", rx=1))


# ═══════════════════════════════════════════════════════════════
# DRAWING: BAND 3 — LAMINA PROPRIA
# ═══════════════════════════════════════════════════════════════

def draw_dc_cell(dwg, cx, cy, radius, color, active=False, helix_color=None):
    """Dendritic cell with irregular branches."""
    n_branches = 7
    random.seed(int(cx) + int(cy))

    # Body
    body_fill = color if not active else _lighten_hex(color, 0.3)
    dwg.add(dwg.circle((cx, cy), radius * 0.5, fill=body_fill, opacity=0.6))

    # Nucleus
    nucleus_r = radius * 0.25
    dwg.add(dwg.circle((cx, cy), nucleus_r, fill=color, opacity=0.8))

    # Branches
    for i in range(n_branches):
        angle = 2 * math.pi * i / n_branches + random.uniform(-0.3, 0.3)
        branch_len = radius * (0.7 + random.uniform(0, 0.5))
        if active:
            branch_len *= 1.3  # longer branches when activated
        bx = cx + branch_len * math.cos(angle)
        by = cy + branch_len * math.sin(angle)
        # Curved branch via quadratic bezier
        mid_x = cx + branch_len * 0.5 * math.cos(angle + 0.2)
        mid_y = cy + branch_len * 0.5 * math.sin(angle + 0.2)
        path_d = f"M {cx},{cy} Q {mid_x},{mid_y} {bx},{by}"
        sw = 3 if active else 2
        dwg.add(dwg.path(d=path_d, fill="none", stroke=color,
                         stroke_width=sw, stroke_linecap="round"))

    # Active glow
    if active:
        dwg.add(dwg.circle((cx, cy), radius * 1.2, fill=color, opacity=0.08))
        dwg.add(dwg.circle((cx, cy), radius * 0.9, fill=color, opacity=0.12))

    # MV130 helix in nucleus (trained immunity)
    if helix_color:
        hx = cx
        hy_start = cy - nucleus_r * 0.7
        hy_end = cy + nucleus_r * 0.7
        n_rungs = 4
        amp = nucleus_r * 0.4
        for j in range(20):
            t = j / 19
            y = hy_start + (hy_end - hy_start) * t
            x1 = hx + amp * math.sin(t * math.pi * 3)
            x2 = hx - amp * math.sin(t * math.pi * 3)
            if j > 0:
                dwg.add(dwg.line((prev_x1, prev_y), (x1, y),
                                 stroke=helix_color, stroke_width=1.5))
                dwg.add(dwg.line((prev_x2, prev_y), (x2, y),
                                 stroke=helix_color, stroke_width=1.5))
            prev_x1, prev_x2, prev_y = x1, x2, y
        # Trained immunity glow (gold)
        dwg.add(dwg.circle((cx, cy), nucleus_r * 1.5,
                           fill="#FDE68A", opacity=0.15))


def draw_th_balance(dwg, cx, cy, width, color_om85, balanced=True):
    """Th1/Th2 balance scale."""
    # Fulcrum triangle
    tri_h = 22
    dwg.add(dwg.polygon(
        [(cx, cy + tri_h), (cx - 12, cy + tri_h + 14), (cx + 12, cy + tri_h + 14)],
        fill="#9CA3AF"
    ))
    # Beam
    tilt = 0 if balanced else 12  # tilted toward Th2 if unbalanced
    lx = cx - width / 2
    rx = cx + width / 2
    ly = cy - tilt
    ry = cy + tilt
    dwg.add(dwg.line((lx, ly), (rx, ry),
                     stroke=color_om85 if balanced else "#9CA3AF",
                     stroke_width=4))
    # Pans
    pan_w = 30
    dwg.add(dwg.rect((lx - pan_w / 2, ly - 4), (pan_w, 8),
                     fill=color_om85 if balanced else "#6B7280", rx=2))
    dwg.add(dwg.rect((rx - pan_w / 2, ry - 4), (pan_w, 8),
                     fill=color_om85 if balanced else "#DC2626", rx=2))
    # Labels
    font_s = 26
    dwg.add(dwg.text("Th1", insert=(lx - 5, ly - 14),
                     font_size=font_s, fill=palette_global["text"]["secondary"],
                     font_family="Helvetica, Arial, sans-serif",
                     text_anchor="middle"))
    dwg.add(dwg.text("Th2", insert=(rx + 5, ry - 14),
                     font_size=font_s, fill=palette_global["text"]["secondary"],
                     font_family="Helvetica, Arial, sans-serif",
                     text_anchor="middle"))


palette_global = {}  # set in main()


def draw_lamina_propria(dwg, layout, palette, W, H):
    bx, by, bw, bh = get_band_rects(layout, W, H)["lamina"]
    bc = layout["band_content"]["lamina"]

    # Split into upper (adaptive) and lower (innate/trained)
    split_y = by + int(bh * bc["split_pct"])

    om85_color = palette["products"]["om85"]
    mv130_color = palette["products"]["mv130"]
    crl1505_color = palette["products"]["crl1505"]
    pmbl_color = palette["products"]["pmbl"]
    dc_color = palette["text"]["secondary"]

    # === LOWER: Innate / Trained Immunity ===

    # Dormant DC (left side)
    dc_x_sick = bx + int(bw * bc["dc_sick_x_pct"])
    dc_y = split_y + int((by + bh - split_y) * 0.5)
    draw_dc_cell(dwg, dc_x_sick, dc_y, bc["dc_radius"], dc_color,
                 active=False, helix_color=None)

    # Active DC with MV130 helix (right side)
    dc_x_healthy = bx + int(bw * bc["dc_healthy_x_pct"])
    draw_dc_cell(dwg, dc_x_healthy, dc_y, bc["dc_radius"] * 1.2,
                 mv130_color, active=True, helix_color=mv130_color)

    # OM-85 blue halo on healthy DC (additional activation marker)
    dwg.add(dwg.circle((dc_x_healthy, dc_y), bc["dc_radius"] * 1.6,
                       fill="none", stroke=om85_color, stroke_width=2,
                       stroke_dasharray="4,3", opacity=0.5))

    # PMBL secondary mark (small teal dot near DC)
    pmbl_dot_x = dc_x_healthy + bc["dc_radius"] * 1.3
    pmbl_dot_y = dc_y - bc["dc_radius"] * 0.5
    dwg.add(dwg.circle((pmbl_dot_x, pmbl_dot_y), 6,
                       fill=pmbl_color, opacity=0.6))

    # Arrow dormant → active
    arrow_y = dc_y
    arrow_x1 = dc_x_sick + bc["dc_radius"] * 1.5
    arrow_x2 = dc_x_healthy - bc["dc_radius"] * 1.8
    dwg.add(dwg.line((arrow_x1, arrow_y), (arrow_x2, arrow_y),
                     stroke="#9CA3AF", stroke_width=2, stroke_dasharray="6,3"))
    dwg.add(dwg.polygon(
        [(arrow_x2, arrow_y - 5), (arrow_x2 + 10, arrow_y), (arrow_x2, arrow_y + 5)],
        fill="#9CA3AF"
    ))

    # === UPPER: Adaptive Balance ===

    # Unbalanced Th1/Th2 (left)
    bal_x_sick = bx + int(bw * 0.22)
    bal_y = by + int((split_y - by) * 0.5)
    draw_th_balance(dwg, bal_x_sick, bal_y, bc["balance_width"] * 0.8,
                    "#9CA3AF", balanced=False)

    # Balanced Th1/Th2 (right) — OM-85 blue
    bal_x_healthy = bx + int(bw * bc["balance_x_pct"])
    draw_th_balance(dwg, bal_x_healthy, bal_y, bc["balance_width"],
                    om85_color, balanced=True)


# ═══════════════════════════════════════════════════════════════
# DRAWING: BAND 4 — MUSCLE LISSE
# ═══════════════════════════════════════════════════════════════

def draw_muscle(dwg, layout, palette, W, H):
    bx, by, bw, bh = get_band_rects(layout, W, H)["muscle"]
    bc = layout["band_content"]["muscle"]

    # Gradient from thick-amber (left) to thin-green (right)
    n_slices = 40
    for i in range(n_slices):
        t = i / (n_slices - 1)  # 0=sick, 1=healthy
        sx = bx + int(bw * t)
        sw = max(1, bw // n_slices + 1)

        thickness_pct = bc["thickness_sick_pct"] * (1 - t) + bc["thickness_healthy_pct"] * t
        slice_h = int(bh * thickness_pct)
        slice_y = by + (bh - slice_h) // 2

        color = _lerp_color(
            palette["bands"]["muscle_sick"],
            palette["bands"]["muscle_healthy"],
            t
        )
        dwg.add(dwg.rect((sx, slice_y), (sw, slice_h), fill=color, opacity=0.7))


# ═══════════════════════════════════════════════════════════════
# DRAWING: CHILD SILHOUETTES (organic contours from v9)
# ═══════════════════════════════════════════════════════════════

def draw_child_contour(dwg, cx, cy, scale, contour_points, fill_color, is_sick=True):
    """Draw child silhouette from extracted contour points."""
    if not contour_points:
        # Fallback: simple circle + stick figure
        dwg.add(dwg.circle((cx, cy), 20 * scale, fill=fill_color, opacity=0.5))
        return

    # Normalize and transform points
    xs = [p[0] for p in contour_points]
    ys = [p[1] for p in contour_points]
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)
    range_x = max_x - min_x or 1
    range_y = max_y - min_y or 1

    target_h = 180 * scale
    aspect = range_x / range_y
    target_w = target_h * aspect

    transformed = []
    for px, py in contour_points:
        tx = cx - target_w / 2 + (px - min_x) / range_x * target_w
        ty = cy - target_h / 2 + (py - min_y) / range_y * target_h
        transformed.append((tx, ty))

    # Build smooth Bézier path
    if len(transformed) >= 4:
        # Close the loop for Catmull-Rom
        padded = [transformed[-1]] + transformed + [transformed[0], transformed[1]]
        segments = _catmull_rom_to_bezier(padded)
        if segments:
            path_d = f"M {transformed[0][0]},{transformed[0][1]} "
            for cp1, cp2, end in segments:
                path_d += f"C {cp1[0]},{cp1[1]} {cp2[0]},{cp2[1]} {end[0]},{end[1]} "
            path_d += "Z"
            dwg.add(dwg.path(d=path_d, fill=fill_color, opacity=0.75,
                             stroke=fill_color, stroke_width=1.5))
    else:
        # Fallback: polygon
        dwg.add(dwg.polygon(transformed, fill=fill_color, opacity=0.6))

    # Expression marks
    head_y = cy - target_h * 0.35
    if is_sick:
        # Distress lines
        for j in range(3):
            lx = cx + target_w * 0.3 + j * 8
            ly = head_y - 10 + j * 6
            dwg.add(dwg.line((lx, ly), (lx + 10, ly - 5),
                             stroke=fill_color, stroke_width=1.5, opacity=0.5))
    else:
        # Sparkles
        for j in range(3):
            sx = cx + target_w * 0.25 + j * 15
            sy = head_y - 15 + j * 8
            dwg.add(dwg.line((sx - 4, sy), (sx + 4, sy), stroke=fill_color, stroke_width=1.5))
            dwg.add(dwg.line((sx, sy - 4), (sx, sy + 4), stroke=fill_color, stroke_width=1.5))


# ═══════════════════════════════════════════════════════════════
# DRAWING: VICIOUS CYCLE (compact, in margin_left)
# ═══════════════════════════════════════════════════════════════

def draw_vicious_cycle(dwg, layout, palette, W, H):
    ml_x, _, ml_w, _ = get_zone_rect(layout, "margin_left", W, H)
    vc = layout["vicious_cycle"]

    cx = ml_x + int(ml_w * vc["center_x_pct"])
    cy = int(H * vc["center_y_pct"])
    rx, ry = vc["radius_x"], vc["radius_y"]
    font_family = layout["font"]["family"]

    # Red circle arc (nearly closed)
    path_d = f"M {cx},{cy - ry} "
    path_d += f"A {rx},{ry} 0 1 1 {cx - 1},{cy - ry}"
    dwg.add(dwg.path(d=path_d, fill="none",
                     stroke=palette["virus"], stroke_width=3, opacity=0.6))

    # Station labels
    for station in vc["stations"]:
        angle = math.radians(station["angle_deg"])
        sx = cx + (rx + 20) * math.cos(angle)
        sy = cy + (ry + 20) * math.sin(angle)
        anchor = "middle"
        if abs(station["angle_deg"]) < 45:
            anchor = "start" if station["angle_deg"] >= 0 else "middle"
        elif station["angle_deg"] == 180:
            anchor = "end"
        dwg.add(dwg.text(station["label"],
                         insert=(sx, sy),
                         font_size=vc["font_size"],
                         fill=palette["text"]["primary"],
                         font_family=font_family,
                         text_anchor=anchor))

    # Bottom label
    dwg.add(dwg.text(vc["bottom_label"],
                     insert=(cx, cy + ry + 45),
                     font_size=vc["font_size"] + 2,
                     fill=palette["virus"],
                     font_family=font_family,
                     font_weight="bold",
                     text_anchor="middle"))


# ═══════════════════════════════════════════════════════════════
# DRAWING: CYCLE-BREAK VISUAL (P23 Résolution Topologique, B4)
# ═══════════════════════════════════════════════════════════════

def draw_cycle_break(dwg, layout, palette, W, H):
    """Draw a green arrow/lance from the healthy bronchus side that
    visually 'fractures' the vicious cycle, implementing Pattern P23
    (Résolution Topologique) and Behavior B4."""
    # Get bronchus right edge
    bx_bronch, by_bronch, bw_bronch, bh_bronch = get_bronchus_rect(layout, W, H)
    bronchus_right_x = bx_bronch  # left edge of bronchus = where it meets margin_left

    # Get vicious cycle center
    ml_x, _, ml_w, _ = get_zone_rect(layout, "margin_left", W, H)
    vc = layout["vicious_cycle"]
    cycle_cx = ml_x + int(ml_w * vc["center_x_pct"])
    cycle_cy = int(H * vc["center_y_pct"])
    cycle_rx = vc["radius_x"]

    # Arrow starts from left edge of bronchus at roughly its vertical center
    arrow_start_x = bronchus_right_x
    arrow_start_y = by_bronch + bh_bronch // 2

    # Arrow target: right edge of the vicious cycle
    arrow_end_x = cycle_cx + cycle_rx - 10
    arrow_end_y = cycle_cy

    # Green arrow color (blend of healthy colors)
    arrow_color = "#059669"

    # Draw the arrow shaft as a quadratic bezier curve that arcs from
    # the bronchus leftward toward the cycle
    ctrl_x = (arrow_start_x + arrow_end_x) * 0.5
    ctrl_y = min(arrow_start_y, arrow_end_y) - 40  # arc upward slightly

    path_d = f"M {arrow_start_x},{arrow_start_y} Q {ctrl_x},{ctrl_y} {arrow_end_x},{arrow_end_y}"
    dwg.add(dwg.path(d=path_d, fill="none",
                     stroke=arrow_color, stroke_width=5,
                     opacity=0.75, stroke_linecap="round"))

    # Arrowhead at the tip (pointing left)
    head_size = 14
    dwg.add(dwg.polygon([
        (arrow_end_x, arrow_end_y),
        (arrow_end_x + head_size, arrow_end_y - head_size * 0.6),
        (arrow_end_x + head_size, arrow_end_y + head_size * 0.6),
    ], fill=arrow_color, opacity=0.8))

    # Small green glow at arrow origin (healthy bronchus)
    dwg.add(dwg.circle((arrow_start_x, arrow_start_y), 10,
                       fill=arrow_color, opacity=0.15))

    # Fracture marks where the arrow meets the cycle (2-3 short diagonal lines in red)
    fracture_color = palette["virus"]  # red
    fracture_marks = [
        (arrow_end_x + 5, arrow_end_y - 12, arrow_end_x + 18, arrow_end_y - 22),
        (arrow_end_x + 2, arrow_end_y + 10, arrow_end_x + 16, arrow_end_y + 22),
        (arrow_end_x + 10, arrow_end_y - 3, arrow_end_x + 24, arrow_end_y + 3),
    ]
    for x1, y1, x2, y2 in fracture_marks:
        dwg.add(dwg.line((x1, y1), (x2, y2),
                         stroke=fracture_color, stroke_width=3,
                         opacity=0.7, stroke_linecap="round"))

    # Small "crack" label
    label_x = arrow_end_x + 20
    label_y = arrow_end_y + 38
    dwg.add(dwg.text("break",
                     insert=(label_x, label_y),
                     font_size=24,
                     fill=arrow_color,
                     font_family="Helvetica, Arial, sans-serif",
                     font_style="italic",
                     opacity=0.6))


# ═══════════════════════════════════════════════════════════════
# DRAWING: EVIDENCE BARS (in margin_right)
# ═══════════════════════════════════════════════════════════════

def draw_evidence_bars(dwg, layout, palette, W, H):
    mr_x, _, mr_w, _ = get_zone_rect(layout, "margin_right", W, H)
    ev = layout["evidence"]
    font_family = layout["font"]["family"]

    y = int(H * ev["y_start_pct"])
    max_bar_w = int(mr_w * ev["max_width_pct"])

    # Title
    dwg.add(dwg.text(ev["title"],
                     insert=(mr_x + mr_w // 2, y - 10),
                     font_size=ev["title_font_size"],
                     fill=palette["text"]["primary"],
                     font_family=font_family,
                     font_weight="bold",
                     text_anchor="middle"))

    for item in ev["items"]:
        bar_w = int(max_bar_w * item["width_pct"])
        color = resolve_color(palette, f"products.{item['product']}")

        bar_x = mr_x + 10
        dwg.add(dwg.rect((bar_x, y), (bar_w, ev["bar_height"]),
                         fill=color, rx=4, ry=4, opacity=0.85))
        label_fs = ev["title_font_size"] - 4
        # Place label inside bar if wide enough, else right of bar
        if bar_w > 80:
            dwg.add(dwg.text(item["label"],
                             insert=(bar_x + 8, y + ev["bar_height"] * 0.72),
                             font_size=label_fs, fill="white",
                             font_family=font_family, font_weight="bold"))
        else:
            dwg.add(dwg.text(item["label"],
                             insert=(bar_x + bar_w + 6, y + ev["bar_height"] * 0.72),
                             font_size=label_fs,
                             fill=palette["text"]["secondary"],
                             font_family=font_family))
        y += ev["bar_height"] + ev["bar_gap"]


# ═══════════════════════════════════════════════════════════════
# DRAWING: CRL1505 RELAY ARC (from bottom to lamina)
# ═══════════════════════════════════════════════════════════════

def draw_crl1505_relay(dwg, layout, palette, W, H):
    relay = layout["crl1505_relay"]
    bands = get_band_rects(layout, W, H)
    bx_bronch, _, bw_bronch, _ = get_bronchus_rect(layout, W, H)

    crl_color = palette["products"]["crl1505"]

    # Gut icon position (below bronchus)
    gut_x = bx_bronch + int(bw_bronch * relay["gut_icon_x_pct"])
    gut_y = int(H * relay["gut_icon_y_pct"])

    # Target: right side of lamina propria band
    lam_x, lam_y, lam_w, lam_h = bands["lamina"]
    target_x = lam_x + int(lam_w * relay["target_x_pct"])
    target_y = lam_y + lam_h

    # Intestine icon (squiggle)
    squig_w = 35
    squig_path = f"M {gut_x - squig_w},{gut_y} "
    for j in range(6):
        sy = gut_y + (10 if j % 2 == 0 else -10)
        sx = gut_x - squig_w + (j + 1) * squig_w * 2 / 6
        squig_path += f"S {sx - 5},{sy} {sx},{gut_y} "
    dwg.add(dwg.path(d=squig_path, fill="none",
                     stroke=crl_color, stroke_width=3, opacity=0.7))
    # Label
    dwg.add(dwg.text("gut", insert=(gut_x + squig_w + 5, gut_y + 8),
                     font_size=28, fill=crl_color, opacity=0.8,
                     font_family="Helvetica, Arial, sans-serif"))

    # Arc from gut to lamina
    mid_x = (gut_x + target_x) / 2 + 60
    mid_y = (gut_y + target_y) / 2
    arc_path = f"M {gut_x},{gut_y - 15} Q {mid_x},{mid_y} {target_x},{target_y}"
    dwg.add(dwg.path(d=arc_path, fill="none",
                     stroke=crl_color, stroke_width=relay["arc_width"],
                     stroke_dasharray="10,5", opacity=0.7))
    # Arrowhead at target
    dwg.add(dwg.polygon(
        [(target_x - 6, target_y + 2), (target_x, target_y - 10), (target_x + 6, target_y + 2)],
        fill=crl_color, opacity=0.7
    ))


# ═══════════════════════════════════════════════════════════════
# DRAWING: PRODUCT LEGEND (below bronchus)
# ═══════════════════════════════════════════════════════════════

def draw_legend(dwg, layout, palette, content, W, H):
    leg = layout["legend"]
    font_family = layout["font"]["family"]
    y = int(H * leg["y_pct"])

    products = [
        ("OM-85", palette["products"]["om85"]),
        ("PMBL", palette["products"]["pmbl"]),
        ("MV130", palette["products"]["mv130"]),
        ("CRL1505", palette["products"]["crl1505"]),
    ]

    total_w = len(products) * (leg["square_size"] + leg["gap"] + 80)
    start_x = (W - total_w) // 2

    for i, (name, color) in enumerate(products):
        x = start_x + i * (leg["square_size"] + leg["gap"] + 80)
        dwg.add(dwg.rect((x, y), (leg["square_size"], leg["square_size"]),
                         fill=color, rx=3))
        dwg.add(dwg.text(name,
                         insert=(x + leg["square_size"] + 8, y + leg["square_size"] * 0.75),
                         font_size=leg["font_size"],
                         fill=palette["text"]["primary"],
                         font_family=font_family))


# ═══════════════════════════════════════════════════════════════
# RENDERING (reused from v9)
# ═══════════════════════════════════════════════════════════════

def render_png(svg_path, full_png, delivery_png, W, H, dw, dh):
    """Render SVG to PNG via Playwright (Windows fallback)."""
    try:
        from PIL import Image
        Image.MAX_IMAGE_PIXELS = 300_000_000

        from playwright.sync_api import sync_playwright

        # Wrap SVG in minimal HTML for reliable rendering
        abs_svg = os.path.abspath(svg_path).replace("\\", "/")
        html_wrapper = os.path.join(os.path.dirname(svg_path), "_render_v10.html")
        with open(html_wrapper, "w") as hf:
            hf.write(f"""<!DOCTYPE html>
<html><head><style>
  body {{ margin: 0; padding: 0; background: white; }}
  img {{ display: block; width: {dw}px; height: {dh}px; }}
</style></head>
<body><img src="file:///{abs_svg}"></body></html>""")

        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page(
                viewport={"width": dw, "height": dh},
                device_scale_factor=2
            )
            abs_html = os.path.abspath(html_wrapper).replace("\\", "/")
            page.goto(f"file:///{abs_html}")
            page.wait_for_timeout(2000)
            page.screenshot(path=full_png, full_page=True, timeout=30000)
            browser.close()
        os.remove(html_wrapper)

        img = Image.open(full_png)
        delivery = img.resize((dw, dh), Image.LANCZOS)
        delivery.save(delivery_png, dpi=(600, 600))
        print(f"  Full PNG: {full_png} ({img.size[0]}x{img.size[1]})")
        print(f"  Delivery: {delivery_png} ({dw}x{dh}, 600 DPI)")
    except Exception as e:
        print(f"  PNG render failed: {e}")
        print("  SVG file is still available for manual rendering.")


# ═══════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════

def main():
    global palette_global
    import random

    print("Loading config...")
    config = load_config()
    layout = config["layout"]
    palette = config["palette"]
    content = config["content"]
    palette_global = palette

    W = layout["canvas"]["width"]
    H = layout["canvas"]["height"]
    dw = layout["canvas"]["delivery_width"]
    dh = layout["canvas"]["delivery_height"]

    print("Loading contours...")
    _load_contours()

    svg_path = os.path.join(OUT_DIR, "wireframe_GA_v10.svg")
    full_png = os.path.join(OUT_DIR, "wireframe_GA_v10_full.png")
    delivery_png = os.path.join(OUT_DIR, "wireframe_GA_v10_delivery.png")

    print(f"Canvas: {W}x{H}, delivery: {dw}x{dh}")

    dwg = svgwrite.Drawing(svg_path, size=(f"{W}px", f"{H}px"),
                           viewBox=f"0 0 {W} {H}")
    dwg.attribs["xmlns"] = "http://www.w3.org/2000/svg"

    # 1. Background gradient
    print("  Drawing background...")
    draw_background(dwg, layout, palette, W, H)

    # 2. Bronchus frame + band separators
    print("  Drawing bronchus frame...")
    draw_bronchus_frame(dwg, layout, palette, W, H)

    # 3. Band 4: Muscle (bottom, behind everything)
    print("  Drawing muscle band...")
    draw_muscle(dwg, layout, palette, W, H)

    # 4. Band 2: Epithelium
    print("  Drawing epithelium...")
    draw_epithelium(dwg, layout, palette, W, H)

    # 5. Band 1: Lumen
    print("  Drawing lumen...")
    draw_lumen(dwg, layout, palette, W, H)

    # 6. Band 3: Lamina propria
    print("  Drawing lamina propria...")
    draw_lamina_propria(dwg, layout, palette, W, H)

    # 7. CRL1505 relay arc
    print("  Drawing CRL1505 relay...")
    draw_crl1505_relay(dwg, layout, palette, W, H)

    # 8. Child silhouettes
    print("  Drawing children...")
    ml_x, _, ml_w, _ = get_zone_rect(layout, "margin_left", W, H)
    mr_x, _, mr_w, _ = get_zone_rect(layout, "margin_right", W, H)

    cs = layout["child_sick"]
    child_sick_x = ml_x + int(ml_w * cs["x_pct"])
    child_sick_y = int(H * cs["y_pct"])
    draw_child_contour(dwg, child_sick_x, child_sick_y, cs["scale"],
                       _CONTOUR_SICK, palette["virus"], is_sick=True)

    ch = layout["child_healthy"]
    child_healthy_x = mr_x + int(mr_w * ch["x_pct"])
    child_healthy_y = int(H * ch["y_pct"])
    draw_child_contour(dwg, child_healthy_x, child_healthy_y, ch["scale"],
                       _CONTOUR_HEALTHY, palette["products"]["crl1505"],
                       is_sick=False)

    # 9. Vicious cycle
    print("  Drawing vicious cycle...")
    draw_vicious_cycle(dwg, layout, palette, W, H)

    # 9b. Cycle-break visual (P23 + B4)
    print("  Drawing cycle break...")
    draw_cycle_break(dwg, layout, palette, W, H)

    # 10. Evidence bars
    print("  Drawing evidence bars...")
    draw_evidence_bars(dwg, layout, palette, W, H)

    # 11. Product legend
    print("  Drawing legend...")
    draw_legend(dwg, layout, palette, content, W, H)

    # Save SVG
    dwg.save()
    print(f"\nSVG saved: {svg_path}")

    # Render PNG
    print("Rendering PNG...")
    render_png(svg_path, full_png, delivery_png, W, H, dw, dh)

    print("\nV10 compilation complete.")


if __name__ == "__main__":
    main()
