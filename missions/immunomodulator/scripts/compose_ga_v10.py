"""
Parametric GA Compositor V10.4 — "La Bronche Vivante"

4-band bronchial cross-section (longitudinal view):
  Band 1: LUMEN — virus entry (left) -> IgA protection (right)
  Band 2: EPITHELIUM — broken barrier -> sealed (OM-85 shield + PMBL staples)
  Band 3: LAMINA PROPRIA — dormant DC/Th2 -> activated DC/trained immunity/Th1-Th2 balance
  Band 4: MUSCLE LISSE — thickened inflamed -> thin resolved

Reads config/layout_v10.yaml + config/palette.yaml + config/content.yaml
Produces: wireframe_GA_v10.svg + _full.png + _delivery.png

V10.3 changes:
  - Extracted reusable drawing functions to scisense/scripts/vec_lib.py
  - Fix 1: Band labels (Lumen, Epithelium, Lamina propria, Muscle) on left edge
  - Fix 2: Zone orientation text (Pathological / Protected)
  - Fix 3: Increased epithelium density (36 cells) + subtle gradient fills
  - Fix 4: OM-85 shield 3x bigger (visual anchor, P21)
  - Fix 5: Convergence lines originate from actual product locations
  - Fix 6: Stronger cycle-break (thicker arrow, bigger fractures)
  - Fix 7: Increased DC cell size (dc_radius 55)
  - Fix 8: Visible dormant DC (darker gray + dim red halo)
  - Fix 9: More lumen content (mucus droplets left, 6 IgA right)
  - Fix 10: Evidence bar label overflow fix (abbreviate Preclinical)

V10.4 changes (calibrated from V2A_4 NotebookLM infographic):
  - Fix 1: Cilia on epithelium cells (defining feature of respiratory epithelium)
  - Fix 2: Horizontal band gradients (sick red -> healthy green inside tissue)
  - Fix 3: Evidence bars darker for stronger evidence (luminance = strength)
  - Fix 4: CRL1505 relay arc opacity reduced (0.7 -> 0.55)
  - Fix 5: Vicious cycle repositioned to wrap around bronchus left entrance
"""

import yaml
import svgwrite
import os
import sys
import math
import json
import random

# Add scisense root to path for vec_lib import
_SCISENSE_ROOT = os.path.normpath(os.path.join(
    os.path.dirname(__file__), "..", "..", ".."))
if _SCISENSE_ROOT not in sys.path:
    sys.path.insert(0, _SCISENSE_ROOT)

from scripts.vec_lib import (
    lighten_hex,
    lerp_color,
    darken_hex,
    catmull_rom_to_bezier,
    draw_virus_icon,
    draw_iga_y,
    draw_dc_cell,
    draw_th_balance,
    draw_child_contour,
    draw_gradient_band,
    draw_mucus_droplet,
    render_png,
)

BASE = r"C:\Users\reyno\scisense\missions\immunomodulator"
CONFIG_DIR = os.path.join(BASE, "config")
OUT_DIR = os.path.join(BASE, "artefacts", "wireframes")
os.makedirs(OUT_DIR, exist_ok=True)


# ===================================================================
# CONFIG LOADING
# ===================================================================

def load_config():
    config = {}
    for name in ("palette", "content"):
        path = os.path.join(CONFIG_DIR, f"{name}.yaml")
        with open(path, "r", encoding="utf-8") as f:
            config[name] = yaml.safe_load(f)
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


# ===================================================================
# CONTOUR DATA (extracted from AI images)
# ===================================================================

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


# ===================================================================
# LAYOUT HELPERS
# ===================================================================

def get_zone_rect(layout, zone_key, W, H):
    z = layout["zones"][zone_key]
    x = int(W * z["x_pct"])
    w = int(W * z["width_pct"])
    return x, 0, w, H


def get_bronchus_rect(layout, W, H):
    bz = layout["zones"]["bronchus"]
    bx = int(W * bz["x_pct"])
    bw = int(W * bz["width_pct"])
    by = int(H * layout["bronchus"]["y_start_pct"])
    bh = int(H * (layout["bronchus"]["y_end_pct"] - layout["bronchus"]["y_start_pct"]))
    return bx, by, bw, bh


def get_band_rects(layout, W, H):
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
    if bw == 0:
        return 0.5
    t = (x - bx) / bw
    return max(0.0, min(1.0, t))


# ===================================================================
# DRAWING: BACKGROUND + GRADIENT
# ===================================================================

def draw_background(dwg, layout, palette, W, H):
    dwg.add(dwg.rect((0, 0), (W, H), fill=palette["background"]))

    grad = layout["gradient"]
    lg = dwg.linearGradient(("0%", "0%"), ("100%", "0%"), id="bg_grad")
    lg.add_stop_color("0%", grad["left_color"])
    lg.add_stop_color("50%", grad["center_color"])
    lg.add_stop_color("100%", grad["right_color"])
    dwg.defs.add(lg)
    dwg.add(dwg.rect((0, 0), (W, H), fill="url(#bg_grad)", opacity=0.6))


# ===================================================================
# DRAWING: BRONCHUS FRAME + BAND SEPARATORS
# ===================================================================

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

    # === V10.4 FIX 2: Band-level horizontal gradients (sick->healthy tissue color) ===
    bands = get_band_rects(layout, W, H)
    band_gradient_pairs = {
        "lumen":      ("#FEF2F2", "#F0FDF4"),   # pale red -> pale green
        "epithelium": ("#FECDD3", "#D1FAE5"),   # pink -> mint
        "lamina":     ("#FEE2E2", "#ECFDF5"),   # pale red -> pale green
        # muscle already has its own gradient from draw_muscle(), skip
    }
    for bname, (bx2, by2, bw2, bh2) in bands.items():
        if bname in band_gradient_pairs:
            sick_col, healthy_col = band_gradient_pairs[bname]
            grad_id = f"band_grad_{bname}"
            band_lg = dwg.linearGradient(("0%", "0%"), ("100%", "0%"), id=grad_id)
            band_lg.add_stop_color("0%", sick_col)
            band_lg.add_stop_color("100%", healthy_col)
            dwg.defs.add(band_lg)
            dwg.add(dwg.rect((bx2, by2), (bw2, bh2),
                             fill=f"url(#{grad_id})", opacity=0.4))
        elif bname == "muscle":
            # Keep subtle fill for muscle (gradient handled by draw_muscle)
            dwg.add(dwg.rect((bx2, by2), (bw2, bh2),
                             fill=palette["bands"]["lamina_bg"],
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


# ===================================================================
# FIX 1: BAND LABELS (Level 3 typography, P28)
# ===================================================================

def draw_band_labels(dwg, layout, palette, W, H):
    """Draw small rotated labels on the LEFT edge of each band."""
    bands = get_band_rects(layout, W, H)
    font_family = layout["font"]["family"]
    label_color = "#9CA3AF"
    label_font_size = 20

    band_names = {
        "lumen": "Lumen",
        "epithelium": "Epithelium",
        "lamina": "Lamina propria",
        "muscle": "Muscle",
    }

    for bname, (bx, by, bw, bh) in bands.items():
        label = band_names.get(bname, bname)
        # Position: just inside the left edge, vertically centered
        lx = bx + 14
        ly = by + bh // 2
        # Rotated -90 degrees around insertion point
        txt = dwg.text(label, insert=(lx, ly),
                       font_size=label_font_size, fill=label_color,
                       font_family=font_family,
                       text_anchor="middle",
                       transform=f"rotate(-90, {lx}, {ly})")
        dwg.add(txt)


# ===================================================================
# FIX 2: ZONE ORIENTATION TEXT
# ===================================================================

def draw_zone_orientation(dwg, layout, palette, W, H):
    """Draw 'Pathological' at top-left, 'Protected' at top-right of bronchus."""
    bx, by, bw, bh = get_bronchus_rect(layout, W, H)
    font_family = layout["font"]["family"]

    # Pathological (left side) — red-ish
    dwg.add(dwg.text("Pathological",
                     insert=(bx + 20, by - 12),
                     font_size=28,
                     fill="#DC2626",
                     font_family=font_family,
                     font_weight="bold",
                     opacity=0.7))

    # Protected (right side) — green-ish
    dwg.add(dwg.text("Protected",
                     insert=(bx + bw - 20, by - 12),
                     font_size=28,
                     fill="#059669",
                     font_family=font_family,
                     font_weight="bold",
                     text_anchor="end",
                     opacity=0.7))


# ===================================================================
# DRAWING: BAND 1 — LUMEN (with fixes 5, 9)
# ===================================================================

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
                         stroke=virus_color, stroke_width=3, opacity=0.5))
        dwg.add(dwg.polygon(
            [(ax + 40, ay - 6), (ax + 52, ay), (ax + 40, ay + 6)],
            fill=virus_color, opacity=0.5
        ))

    # === FIX 9: MUCUS DROPLETS on sick side ===
    random.seed(99)
    for i in range(5):
        mx = bx + int(bw * 0.03) + random.randint(0, int(bw * 0.25))
        my = by + int(bh * 0.15) + random.randint(0, int(bh * 0.65))
        mr = random.randint(4, 8)
        draw_mucus_droplet(dwg, mx, my, mr, color="#D97706", opacity=0.45)

    # === FIX 5: CONVERGENCE LINES from actual product locations ===
    bands = get_band_rects(layout, W, H)
    epi_bx, epi_by, epi_bw, epi_bh = bands["epithelium"]
    lam_bx, lam_by, lam_bw, lam_bh = bands["lamina"]

    epi_bc = layout["band_content"]["epithelium"]
    lam_bc = layout["band_content"]["lamina"]

    convergence_x = bx + int(bw * 0.65)
    convergence_y = by + int(bh * 0.55)

    product_colors = [
        palette["products"]["om85"],
        palette["products"]["pmbl"],
        palette["products"]["mv130"],
        palette["products"]["crl1505"],
    ]

    # OM-85 shield position (from epithelium band)
    shield_x = epi_bx + int(epi_bw * epi_bc["shield_x_pct"]) + 60
    shield_y = epi_by + epi_bh // 2

    # PMBL staples midpoint (from epithelium band, right side)
    staple_x = epi_bx + int(epi_bw * 0.68)
    staple_y = epi_by + epi_bh // 2

    # MV130 helix (from DC healthy in lamina)
    dc_healthy_x = lam_bx + int(lam_bw * lam_bc["dc_healthy_x_pct"])
    dc_y_center = lam_by + int(lam_bh * 0.72)

    # CRL1505 arc endpoint (from lamina right side)
    crl_relay = layout["crl1505_relay"]
    crl_target_x = lam_bx + int(lam_bw * crl_relay["target_x_pct"])
    crl_target_y = lam_by + lam_bh

    line_origins = [
        (shield_x, shield_y),
        (staple_x, staple_y),
        (dc_healthy_x, dc_y_center),
        (crl_target_x, crl_target_y),
    ]
    for (ox, oy), color in zip(line_origins, product_colors):
        ctrl_x = (ox + convergence_x) * 0.5 + 15
        ctrl_y = (oy + convergence_y) * 0.5
        path_d = f"M {ox},{oy} Q {ctrl_x},{ctrl_y} {convergence_x},{convergence_y}"
        dwg.add(dwg.path(d=path_d, fill="none",
                         stroke=color, stroke_width=2.5,
                         opacity=0.45, stroke_linecap="round"))

    # === FIX 9: MORE IgA Y shapes (iga_count 4 -> 6) ===
    iga_count = 6
    iga_colors = [
        palette["products"]["om85"],
        palette["products"]["pmbl"],
        palette["products"]["mv130"],
        palette["products"]["crl1505"],
    ]
    for i in range(iga_count):
        ix_start = convergence_x + 10
        ix_end = bx + int(bw * bc["iga_x_range"][1])
        ix = ix_start + int((ix_end - ix_start) * i / max(1, iga_count - 1))
        iy = by + int(bh * 0.75)
        color_i = iga_colors[i % len(iga_colors)]
        draw_iga_y(dwg, ix, iy, bc["iga_height"], color_i)

    # Small convergence glow at focal point
    dwg.add(dwg.circle((convergence_x, convergence_y), 12,
                       fill="#FFFFFF", opacity=0.4))
    dwg.add(dwg.circle((convergence_x, convergence_y), 8,
                       fill="#059669", opacity=0.15))


# ===================================================================
# DRAWING: BAND 2 — EPITHELIUM (with fixes 3, 4)
# ===================================================================

def draw_epithelium(dwg, layout, palette, W, H):
    bx, by, bw, bh = get_band_rects(layout, W, H)["epithelium"]
    bc = layout["band_content"]["epithelium"]

    # === FIX 3: Increased density (24 -> 36 cells) ===
    n_cells = 36
    cell_w = bw / n_cells
    cell_h = int(bh * bc["cell_height_pct"])
    cell_y = by + (bh - cell_h) // 2

    # Determine gaps (sick side = left)
    gap_indices = set()
    random.seed(7)
    sick_cell_limit = n_cells // 3
    candidates = list(range(sick_cell_limit))
    random.shuffle(candidates)
    for g in candidates[:bc["gap_count_sick"]]:
        gap_indices.add(g)

    om85_color = palette["products"]["om85"]
    pmbl_color = palette["products"]["pmbl"]

    for i in range(n_cells):
        cx = bx + int(i * cell_w)
        t = i / max(1, n_cells - 1)

        # === FIX 3: Gradient fills on cells (P27 texture) ===
        cell_base = lerp_color(
            palette["bands"]["epithelium_sick"],
            palette["bands"]["epithelium_healthy"],
            t
        )
        cell_top = cell_base
        cell_bottom = darken_hex(cell_base, 0.08)

        grad_id = f"cell_grad_{i}"
        cell_lg = dwg.linearGradient(("0%", "0%"), ("0%", "100%"), id=grad_id)
        cell_lg.add_stop_color("0%", cell_top)
        cell_lg.add_stop_color("100%", cell_bottom)
        dwg.defs.add(cell_lg)

        if i in gap_indices:
            gap_size = int(cell_w * 0.35)
            dwg.add(dwg.rect(
                (cx, cell_y), (int(cell_w) - gap_size, cell_h),
                fill=f"url(#{grad_id})", stroke="#D1D5DB", stroke_width=1,
                rx=2, ry=2
            ))
            dwg.add(dwg.rect(
                (cx + int(cell_w) - gap_size, cell_y + int(cell_h * 0.1)),
                (gap_size - 2, int(cell_h * 0.8)),
                fill=palette["virus"], opacity=0.2
            ))
        else:
            dwg.add(dwg.rect(
                (cx + 1, cell_y), (int(cell_w) - 2, cell_h),
                fill=f"url(#{grad_id})", stroke="#D1D5DB", stroke_width=1,
                rx=2, ry=2
            ))

            # === V10.4 FIX 1: CILIA on top of intact cells ===
            # Cilia only appear in transition zone and healthy side (t > 0.3)
            # Height increases with health (t)
            if t > 0.3:
                n_cilia = 4
                cilia_h_base = int(cell_h * 0.18)
                # Scale cilia height with health: 0.3->1.0 maps to 0.4->1.0 of base height
                cilia_scale = 0.4 + 0.6 * ((t - 0.3) / 0.7)
                cilia_h = max(2, int(cilia_h_base * cilia_scale))
                cilia_color = lerp_color(cell_base, "#1F2937", 0.3)
                for c in range(n_cilia):
                    cx_cilia = cx + int(cell_w * (c + 1) / (n_cilia + 1))
                    dwg.add(dwg.line(
                        (cx_cilia, cell_y - 1), (cx_cilia, cell_y - cilia_h),
                        stroke=cilia_color,
                        stroke_width=1.5, stroke_linecap="round"
                    ))

            # PMBL staples between cells (right portion)
            if t > 0.45 and i > 0 and i not in gap_indices:
                staple_x = cx
                staple_y1 = cell_y + int(cell_h * 0.25)
                staple_y2 = cell_y + int(cell_h * 0.75)
                dwg.add(dwg.line(
                    (staple_x, staple_y1), (staple_x, staple_y2),
                    stroke=pmbl_color, stroke_width=3, opacity=0.7
                ))
                dwg.add(dwg.line(
                    (staple_x - 3, staple_y1), (staple_x + 3, staple_y1),
                    stroke=pmbl_color, stroke_width=2
                ))
                dwg.add(dwg.line(
                    (staple_x - 3, staple_y2), (staple_x + 3, staple_y2),
                    stroke=pmbl_color, stroke_width=2
                ))

    # === FIX 4: OM-85 shield 3x bigger (visual anchor, P21) ===
    shield_x = bx + int(bw * bc["shield_x_pct"])
    shield_y = cell_y - 25
    shield_w, shield_h = 120, 130  # Was 50x55

    shield_path = f"M {shield_x},{shield_y} "
    shield_path += f"L {shield_x + shield_w},{shield_y} "
    shield_path += f"L {shield_x + shield_w},{shield_y + shield_h * 0.7} "
    shield_path += f"Q {shield_x + shield_w / 2},{shield_y + shield_h} {shield_x},{shield_y + shield_h * 0.7} Z"
    dwg.add(dwg.path(d=shield_path, fill=om85_color, opacity=0.6,
                     stroke=om85_color, stroke_width=2))

    # Lock icon in center (proportionally bigger)
    lock_cx = shield_x + shield_w / 2
    lock_cy = shield_y + shield_h * 0.4
    dwg.add(dwg.circle((lock_cx, lock_cy), 12, fill="none",
                       stroke="white", stroke_width=3))
    dwg.add(dwg.rect((lock_cx - 10, lock_cy + 8), (20, 16),
                     fill="white", rx=2))

    # "OM-85" label inside shield
    dwg.add(dwg.text("OM-85",
                     insert=(lock_cx, lock_cy + 38),
                     font_size=18, fill="white",
                     font_family=layout["font"]["family"],
                     font_weight="bold",
                     text_anchor="middle",
                     opacity=0.9))


# ===================================================================
# DRAWING: BAND 3 — LAMINA PROPRIA (with fixes 7, 8)
# ===================================================================

def draw_lamina_propria(dwg, layout, palette, W, H):
    bx, by, bw, bh = get_band_rects(layout, W, H)["lamina"]
    bc = layout["band_content"]["lamina"]

    split_y = by + int(bh * bc["split_pct"])

    om85_color = palette["products"]["om85"]
    mv130_color = palette["products"]["mv130"]
    crl1505_color = palette["products"]["crl1505"]
    pmbl_color = palette["products"]["pmbl"]

    # === FIX 7: Increased DC radius (42 -> 55) ===
    dc_radius = 55

    # === LOWER: Innate / Trained Immunity ===

    # === FIX 8: Dormant DC — darker gray + dim red halo ===
    dc_x_sick = bx + int(bw * bc["dc_sick_x_pct"])
    dc_y = split_y + int((by + bh - split_y) * 0.5)
    dormant_color = "#6B7280"

    # Dim red halo to show inflammation context
    dwg.add(dwg.circle((dc_x_sick, dc_y), dc_radius * 1.5,
                       fill="#DC2626", opacity=0.06))
    dwg.add(dwg.circle((dc_x_sick, dc_y), dc_radius * 1.2,
                       fill="#DC2626", opacity=0.08))

    draw_dc_cell(dwg, dc_x_sick, dc_y, dc_radius, dormant_color,
                 active=False, helix_color=None)

    # Active DC with MV130 helix (right side) — also bigger
    dc_x_healthy = bx + int(bw * bc["dc_healthy_x_pct"])
    draw_dc_cell(dwg, dc_x_healthy, dc_y, dc_radius * 1.2,
                 mv130_color, active=True, helix_color=mv130_color)

    # OM-85 blue halo on healthy DC
    dwg.add(dwg.circle((dc_x_healthy, dc_y), dc_radius * 1.6,
                       fill="none", stroke=om85_color, stroke_width=2,
                       stroke_dasharray="4,3", opacity=0.5))

    # PMBL secondary mark
    pmbl_dot_x = dc_x_healthy + dc_radius * 1.3
    pmbl_dot_y = dc_y - dc_radius * 0.5
    dwg.add(dwg.circle((pmbl_dot_x, pmbl_dot_y), 6,
                       fill=pmbl_color, opacity=0.6))

    # Arrow dormant -> active
    arrow_y = dc_y
    arrow_x1 = dc_x_sick + dc_radius * 1.5
    arrow_x2 = dc_x_healthy - dc_radius * 1.8
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
                    "#9CA3AF", balanced=False,
                    text_color=palette["text"]["secondary"],
                    font_family=layout["font"]["family"])

    # Balanced Th1/Th2 (right) — OM-85 blue
    bal_x_healthy = bx + int(bw * bc["balance_x_pct"])
    draw_th_balance(dwg, bal_x_healthy, bal_y, bc["balance_width"],
                    om85_color, balanced=True,
                    text_color=palette["text"]["secondary"],
                    font_family=layout["font"]["family"])


# ===================================================================
# DRAWING: BAND 4 — MUSCLE LISSE (uses draw_gradient_band)
# ===================================================================

def draw_muscle(dwg, layout, palette, W, H):
    bx, by, bw, bh = get_band_rects(layout, W, H)["muscle"]
    bc = layout["band_content"]["muscle"]

    draw_gradient_band(dwg, bx, by, bw, bh,
                       palette["bands"]["muscle_sick"],
                       palette["bands"]["muscle_healthy"],
                       n_slices=40, opacity=0.7,
                       thickness_left=bc["thickness_sick_pct"],
                       thickness_right=bc["thickness_healthy_pct"])


# ===================================================================
# DRAWING: VICIOUS CYCLE (compact, in margin_left)
# ===================================================================

def draw_vicious_cycle(dwg, layout, palette, W, H):
    ml_x, _, ml_w, _ = get_zone_rect(layout, "margin_left", W, H)
    vc = layout["vicious_cycle"]

    # === V10.4 FIX 5: Position cycle at bronchus left edge (wrapping entrance) ===
    bx_bronch, by_bronch, bw_bronch, bh_bronch = get_bronchus_rect(layout, W, H)
    # Center horizontally at the border between margin and bronchus
    cx = bx_bronch
    # Center vertically at the bronchus midpoint
    cy = by_bronch + bh_bronch // 2
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


# ===================================================================
# DRAWING: CYCLE-BREAK VISUAL (P23, B4) — FIX 6: Stronger
# ===================================================================

def draw_cycle_break(dwg, layout, palette, W, H):
    """Draw a green arrow/lance from the healthy bronchus side that
    visually 'fractures' the vicious cycle. FIX 6: thicker arrow, bigger fractures."""
    bx_bronch, by_bronch, bw_bronch, bh_bronch = get_bronchus_rect(layout, W, H)
    bronchus_right_x = bx_bronch

    ml_x, _, ml_w, _ = get_zone_rect(layout, "margin_left", W, H)
    vc = layout["vicious_cycle"]
    cycle_cx = ml_x + int(ml_w * vc["center_x_pct"])
    cycle_cy = int(H * vc["center_y_pct"])
    cycle_rx = vc["radius_x"]

    arrow_start_x = bronchus_right_x
    arrow_start_y = by_bronch + bh_bronch // 2

    arrow_end_x = cycle_cx + cycle_rx - 10
    arrow_end_y = cycle_cy

    arrow_color = "#059669"

    ctrl_x = (arrow_start_x + arrow_end_x) * 0.5
    ctrl_y = min(arrow_start_y, arrow_end_y) - 40

    path_d = f"M {arrow_start_x},{arrow_start_y} Q {ctrl_x},{ctrl_y} {arrow_end_x},{arrow_end_y}"

    # === FIX 6: Thicker arrow (5 -> 10) ===
    dwg.add(dwg.path(d=path_d, fill="none",
                     stroke=arrow_color, stroke_width=10,
                     opacity=0.75, stroke_linecap="round"))

    # Arrowhead — bigger
    head_size = 20
    dwg.add(dwg.polygon([
        (arrow_end_x, arrow_end_y),
        (arrow_end_x + head_size, arrow_end_y - head_size * 0.6),
        (arrow_end_x + head_size, arrow_end_y + head_size * 0.6),
    ], fill=arrow_color, opacity=0.8))

    # Green glow at arrow origin
    dwg.add(dwg.circle((arrow_start_x, arrow_start_y), 14,
                       fill=arrow_color, opacity=0.2))

    # === FIX 6: Bigger fracture marks ===
    fracture_color = palette["virus"]
    fracture_marks = [
        (arrow_end_x + 5, arrow_end_y - 16, arrow_end_x + 28, arrow_end_y - 32),
        (arrow_end_x + 2, arrow_end_y + 14, arrow_end_x + 26, arrow_end_y + 32),
        (arrow_end_x + 12, arrow_end_y - 5, arrow_end_x + 36, arrow_end_y + 5),
        (arrow_end_x + 8, arrow_end_y + 4, arrow_end_x + 30, arrow_end_y + 18),
    ]
    for x1, y1, x2, y2 in fracture_marks:
        dwg.add(dwg.line((x1, y1), (x2, y2),
                         stroke=fracture_color, stroke_width=5,
                         opacity=0.8, stroke_linecap="round"))

    # "break" label
    label_x = arrow_end_x + 25
    label_y = arrow_end_y + 45
    dwg.add(dwg.text("break",
                     insert=(label_x, label_y),
                     font_size=26,
                     fill=arrow_color,
                     font_family="Helvetica, Arial, sans-serif",
                     font_style="italic",
                     font_weight="bold",
                     opacity=0.7))


# ===================================================================
# DRAWING: EVIDENCE BARS (in margin_right) — FIX 10: label overflow
# ===================================================================

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

    # === V10.4 FIX 3: Evidence strength opacity (darker = stronger evidence) ===
    evidence_opacity = {
        "om85": 1.0,       # darkest (18 RCTs)
        "pmbl": 0.85,      # medium
        "mv130": 0.70,     # lighter
        "crl1505": 0.55,   # lightest (P34)
    }

    for item in ev["items"]:
        bar_w = int(max_bar_w * item["width_pct"])
        color = resolve_color(palette, f"products.{item['product']}")

        bar_x = mr_x + 10

        # === FIX 10: Abbreviate labels that overflow ===
        label = item["label"]
        if label == "Preclinical" and bar_w < 80:
            label = "Preclin."

        bar_opacity = evidence_opacity.get(item["product"], 0.85)
        dwg.add(dwg.rect((bar_x, y), (bar_w, ev["bar_height"]),
                         fill=color, rx=4, ry=4, opacity=bar_opacity))
        label_fs = ev["title_font_size"] - 4
        if bar_w > 80:
            dwg.add(dwg.text(label,
                             insert=(bar_x + 8, y + ev["bar_height"] * 0.72),
                             font_size=label_fs, fill="white",
                             font_family=font_family, font_weight="bold"))
        else:
            dwg.add(dwg.text(label,
                             insert=(bar_x + bar_w + 6, y + ev["bar_height"] * 0.72),
                             font_size=label_fs,
                             fill=palette["text"]["secondary"],
                             font_family=font_family))
        y += ev["bar_height"] + ev["bar_gap"]


# ===================================================================
# DRAWING: CRL1505 RELAY ARC (from bottom to lamina)
# ===================================================================

def draw_crl1505_relay(dwg, layout, palette, W, H):
    relay = layout["crl1505_relay"]
    bands = get_band_rects(layout, W, H)
    bx_bronch, _, bw_bronch, _ = get_bronchus_rect(layout, W, H)

    crl_color = palette["products"]["crl1505"]

    gut_x = bx_bronch + int(bw_bronch * relay["gut_icon_x_pct"])
    gut_y = int(H * relay["gut_icon_y_pct"])

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
    dwg.add(dwg.text("gut", insert=(gut_x + squig_w + 5, gut_y + 8),
                     font_size=28, fill=crl_color, opacity=0.8,
                     font_family="Helvetica, Arial, sans-serif"))

    # Arc from gut to lamina
    mid_x = (gut_x + target_x) / 2 + 60
    mid_y = (gut_y + target_y) / 2
    # === V10.4 FIX 4: CRL1505 arc opacity reduced (0.7 -> 0.55) ===
    arc_path = f"M {gut_x},{gut_y - 15} Q {mid_x},{mid_y} {target_x},{target_y}"
    dwg.add(dwg.path(d=arc_path, fill="none",
                     stroke=crl_color, stroke_width=relay["arc_width"],
                     stroke_dasharray="10,5", opacity=0.55))
    dwg.add(dwg.polygon(
        [(target_x - 6, target_y + 2), (target_x, target_y - 10), (target_x + 6, target_y + 2)],
        fill=crl_color, opacity=0.55
    ))


# ===================================================================
# DRAWING: PRODUCT LEGEND (below bronchus)
# ===================================================================

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


# ===================================================================
# MAIN
# ===================================================================

def main():
    print("Loading config...")
    config = load_config()
    layout = config["layout"]
    palette = config["palette"]
    content = config["content"]

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

    # 12. Band labels (FIX 1)
    print("  Drawing band labels...")
    draw_band_labels(dwg, layout, palette, W, H)

    # 13. Zone orientation text (FIX 2)
    print("  Drawing zone orientation...")
    draw_zone_orientation(dwg, layout, palette, W, H)

    # Save SVG
    dwg.save()
    print(f"\nSVG saved: {svg_path}")

    # Render PNG
    print("Rendering PNG...")
    render_png(svg_path, full_png, delivery_png, W, H, dw, dh)

    print("\nV10.4 compilation complete.")


if __name__ == "__main__":
    main()
