"""
Parametric GA Compositor V16 — Evidence-First Iteration

Based on V15. Changes driven by claim mapping analysis:
  - 9/14 paper claims were UNMAPPED in V15
  - "Evidence" narrative received only 18% reader attention
  - Claims c3-c9 (quantitative evidence per product) were invisible

V16 fixes:
  - Evidence bars: wider (0.28 vs 0.18), taller, moved up
  - Outcome labels next to each bar (claims c4,c5,c7,c9)
  - Bronchus narrowed to 0.68 to make room
  - Evidence title: "Hierarchie de l'Evidence Scientifique"

V15 restructures to match Aurore's V3 design:

Changes from V14:
  1. LAYOUT: 2 horizontal panels instead of 3 vertical zones
     - TOP (~60%): bronchus spanning FULL WIDTH, children at edges,
       vicious cycle bottom-left, evidence bars bottom-right
     - BOTTOM (~40%): product pills -> mechanism boxes -> outcome badges
  2. BACKGROUND: pure white (#FFFFFF), no warm-to-cool gradient
  3. CENTRAL ARROW: large semi-transparent arrow in bronchus center (left->right)
     communicating the pathological -> protected transformation
  4. Removed: zone_headers (3 colored pills), disease_cascade (integrated into cycle),
     mechanism_to_evidence_arrow (no longer needed in new layout)

Reads config/layout_v17.yaml + config/palette.yaml + config/content.yaml
Produces: wireframe_GA_v17.svg + _full.png + _delivery.png
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
    draw_stipple_field,
    draw_crosshatch,
    draw_fiber_lines,
    draw_tight_junction,
    draw_cell_nucleus,
    draw_macrophage,
    draw_t_helper,
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
    path = os.path.join(CONFIG_DIR, "layout_v17.yaml")
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
# ACCESSIBILITY: PRODUCT HATCHING PATTERNS
# ===================================================================

def add_product_patterns(dwg, palette):
    """Add hatching/dot patterns keyed by product for non-color differentiation."""
    products = palette["products"]

    # OM-85: diagonal lines (////)
    pat_om85 = dwg.pattern(id="pat_om85", size=(12, 12),
                           patternUnits="userSpaceOnUse")
    pat_om85.add(dwg.rect((0, 0), (12, 12), fill=products["om85"], opacity=0.15))
    pat_om85.add(dwg.line((0, 12), (12, 0), stroke="white",
                          stroke_width=2, opacity=0.5))
    dwg.defs.add(pat_om85)

    # PMBL: dots
    pat_pmbl = dwg.pattern(id="pat_pmbl", size=(10, 10),
                           patternUnits="userSpaceOnUse")
    pat_pmbl.add(dwg.rect((0, 0), (10, 10), fill=products["pmbl"], opacity=0.15))
    pat_pmbl.add(dwg.circle((5, 5), 2, fill="white", opacity=0.5))
    dwg.defs.add(pat_pmbl)

    # MV130: cross-hatch (X)
    pat_mv130 = dwg.pattern(id="pat_mv130", size=(12, 12),
                            patternUnits="userSpaceOnUse")
    pat_mv130.add(dwg.rect((0, 0), (12, 12), fill=products["mv130"], opacity=0.15))
    pat_mv130.add(dwg.line((0, 0), (12, 12), stroke="white",
                           stroke_width=1.5, opacity=0.5))
    pat_mv130.add(dwg.line((12, 0), (0, 12), stroke="white",
                           stroke_width=1.5, opacity=0.5))
    dwg.defs.add(pat_mv130)

    # CRL1505: horizontal dashes
    pat_crl = dwg.pattern(id="pat_crl1505", size=(14, 8),
                          patternUnits="userSpaceOnUse")
    pat_crl.add(dwg.rect((0, 0), (14, 8), fill=products["crl1505"], opacity=0.15))
    pat_crl.add(dwg.line((0, 4), (10, 4), stroke="white",
                         stroke_width=2, opacity=0.5))
    dwg.defs.add(pat_crl)


PRODUCT_PATTERN_IDS = {
    "om85": "pat_om85",
    "pmbl": "pat_pmbl",
    "mv130": "pat_mv130",
    "crl1505": "pat_crl1505",
}


# ===================================================================
# V15 LAYOUT HELPERS — full-width bronchus (no zones)
# ===================================================================

def get_bronchus_rect(layout, W, H):
    """V15: bronchus uses its own x_pct/width_pct (full width with margins)."""
    bc = layout["bronchus"]
    bx = int(W * bc["x_pct"])
    bw = int(W * bc["width_pct"])
    by = int(H * bc["y_start_pct"])
    bh = int(H * (bc["y_end_pct"] - bc["y_start_pct"]))
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
# MECHANISM BOX ICONS (same as V14)
# ===================================================================

def draw_icon_barrier(dwg, cx, cy, size, color):
    """Horizontal lines = wall metaphor for epithelial barrier."""
    half = size / 2
    n_lines = 5
    for i in range(n_lines):
        y = cy - half + (i * size / (n_lines - 1))
        x1 = cx - half * 0.8
        x2 = cx + half * 0.8
        sw = 3 if i % 2 == 0 else 2
        dwg.add(dwg.line((x1, y), (x2, y),
                         stroke=color, stroke_width=sw, opacity=0.85,
                         stroke_linecap="round"))
    dwg.add(dwg.line((cx - half * 0.8, cy - half), (cx - half * 0.8, cy + half),
                     stroke=color, stroke_width=2, opacity=0.5))
    dwg.add(dwg.line((cx + half * 0.8, cy - half), (cx + half * 0.8, cy + half),
                     stroke=color, stroke_width=2, opacity=0.5))


def draw_icon_innate(dwg, cx, cy, size, color):
    """Starburst / explosion = innate immune activation."""
    half = size / 2
    n_rays = 8
    for i in range(n_rays):
        angle = math.radians(i * 360 / n_rays)
        inner_r = half * 0.3
        outer_r = half * 0.9
        x1 = cx + inner_r * math.cos(angle)
        y1 = cy + inner_r * math.sin(angle)
        x2 = cx + outer_r * math.cos(angle)
        y2 = cy + outer_r * math.sin(angle)
        dwg.add(dwg.line((x1, y1), (x2, y2),
                         stroke=color, stroke_width=2.5, opacity=0.85,
                         stroke_linecap="round"))
    dwg.add(dwg.circle((cx, cy), half * 0.28,
                        fill=color, opacity=0.7))


def draw_icon_adaptive(dwg, cx, cy, size, color):
    """Y-shape = antibody for adaptive response."""
    half = size / 2
    stem_top_y = cy - half * 0.15
    stem_bot_y = cy + half * 0.85
    dwg.add(dwg.line((cx, stem_top_y), (cx, stem_bot_y),
                     stroke=color, stroke_width=3, opacity=0.85,
                     stroke_linecap="round"))
    arm_top_y = cy - half * 0.75
    arm_left_x = cx - half * 0.6
    dwg.add(dwg.line((cx, stem_top_y), (arm_left_x, arm_top_y),
                     stroke=color, stroke_width=3, opacity=0.85,
                     stroke_linecap="round"))
    arm_right_x = cx + half * 0.6
    dwg.add(dwg.line((cx, stem_top_y), (arm_right_x, arm_top_y),
                     stroke=color, stroke_width=3, opacity=0.85,
                     stroke_linecap="round"))
    dwg.add(dwg.circle((arm_left_x, arm_top_y), 3.5,
                        fill=color, opacity=0.7))
    dwg.add(dwg.circle((arm_right_x, arm_top_y), 3.5,
                        fill=color, opacity=0.7))


def draw_icon_inflammation(dwg, cx, cy, size, color):
    """Downward arrow in circle = inflammation control / suppression."""
    half = size / 2
    dwg.add(dwg.circle((cx, cy), half * 0.85,
                        fill="none", stroke=color, stroke_width=2.5, opacity=0.8))
    arrow_top = cy - half * 0.45
    arrow_bot = cy + half * 0.35
    dwg.add(dwg.line((cx, arrow_top), (cx, arrow_bot),
                     stroke=color, stroke_width=3, opacity=0.85,
                     stroke_linecap="round"))
    head_w = half * 0.35
    dwg.add(dwg.polygon([
        (cx - head_w, arrow_bot - 2),
        (cx, arrow_bot + half * 0.25),
        (cx + head_w, arrow_bot - 2),
    ], fill=color, opacity=0.85))


ICON_DRAWERS = {
    "barrier": draw_icon_barrier,
    "innate": draw_icon_innate,
    "adaptive": draw_icon_adaptive,
    "inflammation": draw_icon_inflammation,
}


# ===================================================================
# V15: BACKGROUND — pure white, no gradient
# ===================================================================

def draw_background(dwg, layout, palette, W, H):
    """V15: Clean white background — no warm-to-cool gradient."""
    dwg.add(dwg.rect((0, 0), (W, H), fill="#FFFFFF"))


# ===================================================================
# V15: PANEL DIVIDER
# ===================================================================

def draw_panel_divider(dwg, layout, W, H):
    """V15: Subtle gray line between top and bottom panels."""
    pd = layout.get("panel_divider", {})
    y = int(H * pd.get("y_pct", 0.625))
    color = pd.get("color", "#E5E7EB")
    width = pd.get("width", 2)
    margin = int(W * pd.get("margin_x_pct", 0.02))
    dwg.add(dwg.line((margin, y), (W - margin, y),
                     stroke=color, stroke_width=width))


# ===================================================================
# V15: CENTRAL DIRECTIONAL ARROW
# ===================================================================

def draw_central_arrow(dwg, layout, W, H):
    """V15: Large semi-transparent arrow in center of bronchus, left->right."""
    ca = layout.get("central_arrow", {})
    if not ca.get("enabled", False):
        return

    bx, by, bw, bh = get_bronchus_rect(layout, W, H)
    color = ca.get("color", "#1D3557")
    opacity = ca.get("opacity", 0.20)
    arrow_w_pct = ca.get("width_pct", 0.30)
    arrow_h = ca.get("height", 80)
    head_w = ca.get("head_width", 60)

    # Center the arrow in the bronchus
    y_center = by + int(bh * ca.get("y_center_pct", 0.5))
    arrow_total_w = int(bw * arrow_w_pct)
    shaft_w = arrow_total_w - head_w

    # Start from center of bronchus
    start_x = bx + int(bw * 0.35)
    shaft_end_x = start_x + shaft_w
    tip_x = start_x + arrow_total_w

    shaft_half_h = arrow_h * 0.35  # shaft is thinner than head

    # Draw arrow as a polygon: shaft + arrowhead
    points = [
        (start_x, y_center - shaft_half_h),                    # top-left of shaft
        (shaft_end_x, y_center - shaft_half_h),                # top-right of shaft
        (shaft_end_x, y_center - arrow_h / 2),                 # top of arrowhead
        (tip_x, y_center),                                     # tip
        (shaft_end_x, y_center + arrow_h / 2),                 # bottom of arrowhead
        (shaft_end_x, y_center + shaft_half_h),                # bottom-right of shaft
        (start_x, y_center + shaft_half_h),                    # bottom-left of shaft
    ]

    dwg.add(dwg.polygon(points, fill=color, opacity=opacity))


# ===================================================================
# V15: BRONCHUS GLOW
# ===================================================================

def draw_bronchus_glow(dwg, layout, W, H):
    """Subtle shadow/glow around the bronchus."""
    bc = layout["bronchus"]
    if not bc.get("glow_enabled", False):
        return

    bx, by, bw, bh = get_bronchus_rect(layout, W, H)
    glow_color = bc.get("glow_color", "#000000")
    glow_opacity = bc.get("glow_opacity", 0.08)
    glow_blur = bc.get("glow_blur", 30)
    cr = bc["corner_radius"]

    n_layers = 6
    for i in range(n_layers, 0, -1):
        pad = int(glow_blur * i / n_layers)
        layer_opacity = glow_opacity * (1.0 - i / (n_layers + 1)) * 0.7
        dwg.add(dwg.rect(
            (bx - pad, by - pad + 4), (bw + 2 * pad, bh + 2 * pad),
            rx=cr + pad // 2, ry=cr + pad // 2,
            fill=glow_color, opacity=layer_opacity
        ))


# ===================================================================
# BRONCHUS FRAME + BAND SEPARATORS
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

    # 3-stop band gradients (sick -> neutral -> healthy)
    bands = get_band_rects(layout, W, H)
    band_gradient_triplets = {
        "lumen":      ("#FEF2F2", "#FAFAFA", "#F0FDF4"),
        "epithelium": ("#FECDD3", "#F3F4F6", "#D1FAE5"),
        "lamina":     ("#FEE2E2", "#F9FAFB", "#ECFDF5"),
    }
    for bname, (bx2, by2, bw2, bh2) in bands.items():
        if bname in band_gradient_triplets:
            sick_col, mid_col, healthy_col = band_gradient_triplets[bname]
            grad_id = f"band_grad_{bname}"
            band_lg = dwg.linearGradient(("0%", "0%"), ("100%", "0%"), id=grad_id)
            band_lg.add_stop_color("0%", sick_col)
            band_lg.add_stop_color("45%", mid_col)
            band_lg.add_stop_color("100%", healthy_col)
            dwg.defs.add(band_lg)
            dwg.add(dwg.rect((bx2, by2), (bw2, bh2),
                             fill=f"url(#{grad_id})", opacity=0.50))
        elif bname == "muscle":
            dwg.add(dwg.rect((bx2, by2), (bw2, bh2),
                             fill=palette["bands"]["lamina_bg"],
                             opacity=0.3))

    # Separator lines
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
# BAND LABELS
# ===================================================================

def draw_band_labels(dwg, layout, palette, W, H):
    bands = get_band_rects(layout, W, H)
    font_family = layout["font"]["family"]

    bl_cfg = layout.get("band_labels", {})
    label_font_size = bl_cfg.get("font_size", 20)
    label_color = bl_cfg.get("color", "#9CA3AF")

    band_names = {
        "lumen": "Lumen",
        "epithelium": "Epithelium",
        "lamina": "Lamina propria",
        "muscle": "Muscle",
    }

    for bname, (bx, by, bw, bh) in bands.items():
        label = band_names.get(bname, bname)
        lx = bx + 20
        ly = by + bh // 2
        label_len = len(label) * label_font_size * 0.55
        back_w = label_len
        back_h = label_font_size + 8
        back_x = lx - label_len / 2
        back_y = ly - back_h / 2
        backing = dwg.rect((back_x, back_y), (back_w, back_h),
                           fill="white", opacity=0.72, rx=4, ry=4)
        backing.attribs["transform"] = f"rotate(-90, {lx}, {ly})"
        dwg.add(backing)
        txt = dwg.text(label, insert=(lx, ly + label_font_size * 0.35),
                       font_size=label_font_size, fill=label_color,
                       font_family=font_family,
                       text_anchor="middle",
                       transform=f"rotate(-90, {lx}, {ly})")
        dwg.add(txt)


# ===================================================================
# V15: ZONE ORIENTATION TEXT (above bronchus, full width)
# ===================================================================

def draw_zone_orientation(dwg, layout, palette, W, H):
    bx, by, bw, bh = get_bronchus_rect(layout, W, H)
    font_family = layout["font"]["family"]
    zo = layout.get("zone_orientation", {})
    fs = zo.get("font_size", 36)
    op = zo.get("opacity", 0.85)

    # Pathological label (left side)
    path_cfg = zo.get("pathological", {})
    path_text = path_cfg.get("text", "Pathological")
    path_color = path_cfg.get("color", "#DC2626")
    path_x, path_y = bx + 24, by - 14
    dwg.add(dwg.rect((path_x - 4, path_y - 28), (220, 36),
                     fill="white", opacity=0.7, rx=4))
    dwg.add(dwg.text(path_text,
                     insert=(path_x, path_y),
                     font_size=fs,
                     fill=path_color,
                     font_family=font_family,
                     font_weight="bold",
                     opacity=op))

    # Protected label (right side)
    prot_cfg = zo.get("protected", {})
    prot_text = prot_cfg.get("text", "Protected")
    prot_color = prot_cfg.get("color", "#059669")
    prot_x = bx + bw - 24
    dwg.add(dwg.rect((prot_x - 175, by - 42), (180, 36),
                     fill="white", opacity=0.7, rx=4))
    dwg.add(dwg.text(prot_text,
                     insert=(prot_x, by - 14),
                     font_size=fs,
                     fill=prot_color,
                     font_family=font_family,
                     font_weight="bold",
                     text_anchor="end",
                     opacity=op))


# ===================================================================
# V15: PRODUCT PILLS (centered above full-width bronchus)
# ===================================================================

def draw_product_pills(dwg, layout, palette, content, W, H):
    """Draw 4 colored product pills centered above the bronchus."""
    pp = layout["product_pills"]
    font_family = layout["font"]["family"]
    y = int(H * pp["y_pct"])
    pill_h = pp["pill_height"]
    pill_rx = pp["pill_rx"]
    pill_gap = pp["pill_gap"]
    fs = pp["font_size"]
    text_color = pp["text_color"]

    products = [
        ("OM-85", palette["products"]["om85"], "om85"),
        ("PMBL", palette["products"]["pmbl"], "pmbl"),
        ("MV130", palette["products"]["mv130"], "mv130"),
        ("CRL1505", palette["products"]["crl1505"], "crl1505"),
    ]

    pill_widths = []
    for name, _, _ in products:
        pw = max(140, len(name) * fs * 0.65 + 40)
        pill_widths.append(int(pw))

    total_w = sum(pill_widths) + pill_gap * (len(products) - 1)

    # V15: center above the full-width bronchus
    bx, _, bw, _ = get_bronchus_rect(layout, W, H)
    start_x = bx + (bw - total_w) // 2

    cx = start_x
    for i, (name, color, key) in enumerate(products):
        pw = pill_widths[i]
        dwg.add(dwg.rect((cx, y), (pw, pill_h),
                         fill=color, rx=pill_rx, ry=pill_rx, opacity=0.92))
        pat_id = PRODUCT_PATTERN_IDS.get(key)
        if pat_id:
            dwg.add(dwg.rect((cx, y), (pw, pill_h),
                             fill=f"url(#{pat_id})", rx=pill_rx, ry=pill_rx,
                             opacity=0.6))
        dwg.add(dwg.text(name,
                         insert=(cx + pw // 2, y + pill_h * 0.68),
                         font_size=fs, fill=text_color,
                         font_family=font_family, font_weight="bold",
                         text_anchor="middle"))
        cx += pw + pill_gap


# ===================================================================
# V15: VICIOUS CYCLE (bottom-left of top panel)
# ===================================================================

def draw_vicious_cycle(dwg, layout, palette, W, H):
    """V15: Vicious cycle positioned at bottom-left of top panel."""
    vc = layout["vicious_cycle"]
    font_family = layout["font"]["family"]

    cx = int(W * vc["center_x_pct"])
    cy = int(H * vc["center_y_pct"])
    rx, ry = vc["radius_x"], vc["radius_y"]

    # Red circle arc
    path_d = f"M {cx},{cy - ry} "
    path_d += f"A {rx},{ry} 0 1 1 {cx - 1},{cy - ry}"
    dwg.add(dwg.path(d=path_d, fill="none",
                     stroke=palette["virus"], stroke_width=3.5, opacity=0.65))

    for station in vc["stations"]:
        angle = math.radians(station["angle_deg"])
        sx = cx + (rx + 20) * math.cos(angle)
        sy = cy + (ry + 20) * math.sin(angle)
        anchor = "middle"
        if abs(station["angle_deg"]) < 45:
            anchor = "start" if station["angle_deg"] >= 0 else "middle"
        elif station["angle_deg"] == 180 or station["angle_deg"] == 170:
            anchor = "end"
        dwg.add(dwg.text(station["label"],
                         insert=(sx, sy),
                         font_size=vc["font_size"],
                         fill=palette["text"]["primary"],
                         font_family=font_family,
                         text_anchor=anchor))

    # Bottom label
    dwg.add(dwg.text(vc["bottom_label"],
                     insert=(cx, cy + ry + 40),
                     font_size=vc["font_size"] + 4,
                     fill=palette["virus"],
                     font_family=font_family,
                     font_weight="bold",
                     text_anchor="middle"))


# ===================================================================
# V15: EVIDENCE BARS (bottom-right of top panel)
# ===================================================================

def draw_evidence_bars(dwg, layout, palette, W, H):
    """V17: Evidence in own panel — full width, proportional heights, background."""
    ev = layout["evidence"]
    font_family = layout["font"]["family"]

    ev_x = int(W * ev["x_pct"])
    ev_w = int(W * ev["width_pct"])
    y = int(H * ev["y_start_pct"])
    max_bar_w = int(ev_w * ev["max_width_pct"])

    # V17: Background for the evidence section
    bg_color = ev.get("background_color")
    if bg_color:
        bg_rx = ev.get("background_rx", 8)
        panels = layout.get("panels", {})
        ev_panel = panels.get("evidence", {})
        bg_h = int(H * ev_panel.get("height_pct", 0.20))
        bg_y = int(H * ev_panel.get("y_pct", 0.46))
        dwg.add(dwg.rect((ev_x - 20, bg_y), (ev_w + 40, bg_h),
                         fill=bg_color, rx=bg_rx, ry=bg_rx))

    height_multipliers = ev.get("bar_height_multipliers", {})

    # Title
    title_y = y - 20
    title_fw = ev.get("title_font_weight", 800)
    dwg.add(dwg.text(ev["title"],
                     insert=(ev_x + ev_w // 2, title_y),
                     font_size=ev["title_font_size"],
                     fill=palette["text"]["primary"],
                     font_family=font_family,
                     font_weight=str(title_fw),
                     text_anchor="middle"))

    # Title underline
    if ev.get("title_underline", False):
        title_text_w = len(ev["title"]) * ev["title_font_size"] * 0.5
        ul_x1 = ev_x + ev_w // 2 - title_text_w // 2
        ul_x2 = ev_x + ev_w // 2 + title_text_w // 2
        ul_y = title_y + 8
        dwg.add(dwg.line((ul_x1, ul_y), (ul_x2, ul_y),
                         stroke=palette["text"]["primary"],
                         stroke_width=3, opacity=0.6))

    evidence_opacity = {
        "om85": 1.0,
        "pmbl": 0.85,
        "mv130": 0.70,
        "crl1505": 0.55,
    }

    rct_inside = ev.get("rct_inside_bars", True)

    for item in ev["items"]:
        bar_w = int(max_bar_w * item["width_pct"])
        color = resolve_color(palette, f"products.{item['product']}")
        bar_x = ev_x + 10
        # V17: proportional bar heights
        h_mult = height_multipliers.get(item["product"], 1.0)
        bar_h = int(ev["bar_height"] * h_mult)
        bar_opacity = evidence_opacity.get(item["product"], 0.85)

        # Draw bar
        dwg.add(dwg.rect((bar_x, y), (bar_w, bar_h),
                         fill=color, rx=8, ry=8, opacity=bar_opacity))

        # Accessibility pattern overlay
        pat_id = PRODUCT_PATTERN_IDS.get(item["product"])
        if pat_id:
            dwg.add(dwg.rect((bar_x, y), (bar_w, bar_h),
                             fill=f"url(#{pat_id})", rx=8, ry=8,
                             opacity=0.4))

        product_name = item.get("name", item["product"].upper())
        label = item["label"]
        name_fs = 30
        label_fs = 26

        if rct_inside and bar_w > 160:
            dwg.add(dwg.text(product_name,
                             insert=(bar_x + 14, y + bar_h * 0.62),
                             font_size=name_fs, fill="white",
                             font_family=font_family, font_weight="bold"))
            dwg.add(dwg.text(label,
                             insert=(bar_x + bar_w - 14, y + bar_h * 0.62),
                             font_size=label_fs, fill="white",
                             font_family=font_family, font_weight="bold",
                             text_anchor="end", opacity=0.95))
        elif bar_w > 80:
            dwg.add(dwg.text(product_name,
                             insert=(bar_x + 10, y + bar_h * 0.62),
                             font_size=name_fs - 4, fill="white",
                             font_family=font_family, font_weight="bold"))
            dwg.add(dwg.text(label,
                             insert=(bar_x + bar_w + 10, y + bar_h * 0.62),
                             font_size=label_fs,
                             fill=palette["text"]["secondary"],
                             font_family=font_family, font_weight="bold"))
        else:
            dwg.add(dwg.text(product_name,
                             insert=(bar_x + 6, y + bar_h * 0.62),
                             font_size=22, fill="white",
                             font_family=font_family, font_weight="bold"))
            dwg.add(dwg.text(label,
                             insert=(bar_x + bar_w + 8, y + bar_h * 0.62),
                             font_size=label_fs,
                             fill=palette["text"]["secondary"],
                             font_family=font_family, font_weight="bold"))

        # V16: Outcome label to the right of the bar (claims c4,c5,c7,c9)
        outcome = item.get("outcome", "")
        if outcome:
            outcome_x = bar_x + bar_w + 15
            outcome_y = y + bar_h * 0.6
            dwg.add(dwg.text(outcome,
                             insert=(outcome_x, outcome_y),
                             font_size=20, fill=palette["text"]["secondary"],
                             font_family=font_family, font_weight="normal",
                             opacity=0.85))

        y += bar_h + ev["bar_gap"]


# ===================================================================
# V16: BOTTOM PANEL — mechanism flow (WHAT -> HOW -> RESULT)
# ===================================================================

def draw_bottom_panel(dwg, layout, palette, content, W, H):
    """V15: Bottom panel with product pills -> mechanism boxes -> outcome badges."""
    bp = layout.get("bottom_panel", {})
    font_family = layout["font"]["family"]

    # Section title
    title_y = int(H * bp.get("title_y_pct", 0.66))
    title_color = bp.get("title_color", "#1F2937")
    dwg.add(dwg.text(bp.get("title", "MECHANISM OF ACTION"),
                     insert=(W // 2, title_y),
                     font_size=bp.get("title_font_size", 44),
                     fill=title_color,
                     font_family=font_family,
                     font_weight=str(bp.get("title_font_weight", 800)),
                     text_anchor="middle"))

    # Title underline
    title_text = bp.get("title", "MECHANISM OF ACTION")
    title_text_w = len(title_text) * bp.get("title_font_size", 44) * 0.45
    ul_y = title_y + 10
    dwg.add(dwg.line((W // 2 - title_text_w // 2, ul_y),
                     (W // 2 + title_text_w // 2, ul_y),
                     stroke=title_color, stroke_width=3, opacity=0.4))

    # --- Left column: Product pills ---
    pc = bp.get("products_column", {})
    pc_x = int(W * pc.get("x_pct", 0.04))
    pc_w = int(W * pc.get("width_pct", 0.18))
    pc_y = int(H * pc.get("y_start_pct", 0.72))
    pill_h = pc.get("pill_height", 56)
    pill_gap = pc.get("pill_gap", 16)
    pill_rx = pc.get("pill_rx", 28)
    pill_fs = pc.get("font_size", 32)

    products = [
        ("OM-85", palette["products"]["om85"], "om85"),
        ("PMBL", palette["products"]["pmbl"], "pmbl"),
        ("MV130", palette["products"]["mv130"], "mv130"),
        ("CRL1505", palette["products"]["crl1505"], "crl1505"),
    ]

    product_centers = []  # for drawing arrows
    for i, (name, color, key) in enumerate(products):
        py = pc_y + i * (pill_h + pill_gap)
        # Full-width pill in the column
        dwg.add(dwg.rect((pc_x, py), (pc_w, pill_h),
                         fill=color, rx=pill_rx, ry=pill_rx, opacity=0.92))
        pat_id = PRODUCT_PATTERN_IDS.get(key)
        if pat_id:
            dwg.add(dwg.rect((pc_x, py), (pc_w, pill_h),
                             fill=f"url(#{pat_id})", rx=pill_rx, ry=pill_rx,
                             opacity=0.5))
        dwg.add(dwg.text(name,
                         insert=(pc_x + pc_w // 2, py + pill_h * 0.65),
                         font_size=pill_fs, fill="#FFFFFF",
                         font_family=font_family, font_weight="bold",
                         text_anchor="middle"))
        product_centers.append((pc_x + pc_w, py + pill_h // 2))

    # --- Center column: Mechanism boxes ---
    mc = bp.get("mechanisms_column", {})
    mc_x = int(W * mc.get("x_pct", 0.28))
    mc_w = int(W * mc.get("width_pct", 0.38))
    mc_y = int(H * mc.get("y_start_pct", 0.72))
    box_h = mc.get("box_height", 56)
    box_gap = mc.get("box_gap", 16)
    box_rx = mc.get("box_rx", 12)
    border_w = mc.get("border_left_width", 8)
    title_fs = mc.get("title_font_size", 30)
    icon_size = mc.get("icon_size", 36)
    icon_gap = mc.get("icon_gap", 12)
    bg_color = mc.get("bg_color", "#FFFFFF")
    bg_opacity = mc.get("bg_opacity", 0.94)
    border_color = mc.get("border_color", "#D1D5DB")

    boxes = content.get("mechanism_boxes", [])
    mech_centers = []  # for drawing arrows
    for i, box_data in enumerate(boxes):
        by_box = mc_y + i * (box_h + box_gap)
        color_key = box_data.get("border_color_key", "om85")
        left_border_color = palette["products"].get(color_key, "#888888")

        # Background rect
        dwg.add(dwg.rect((mc_x, by_box), (mc_w, box_h),
                         fill=bg_color, opacity=bg_opacity,
                         stroke=border_color, stroke_width=2,
                         rx=box_rx, ry=box_rx))

        # Colored left border strip
        dwg.add(dwg.rect((mc_x, by_box + 4), (border_w, box_h - 8),
                         fill=left_border_color, rx=4, ry=4, opacity=0.92))

        # Accessibility pattern overlay on left border
        pat_id = PRODUCT_PATTERN_IDS.get(color_key)
        if pat_id:
            dwg.add(dwg.rect((mc_x, by_box + 4), (border_w, box_h - 8),
                             fill=f"url(#{pat_id})", rx=4, ry=4, opacity=0.5))

        # Draw icon
        icon_key = box_data.get("icon", "")
        icon_cx = mc_x + border_w + 10 + icon_size / 2
        icon_cy = by_box + box_h / 2
        icon_drawer = ICON_DRAWERS.get(icon_key)
        if icon_drawer:
            icon_drawer(dwg, icon_cx, icon_cy, icon_size, left_border_color)

        # Title
        title_x = mc_x + border_w + 10 + icon_size + icon_gap
        title_y_box = by_box + box_h * 0.62
        dwg.add(dwg.text(box_data["title"],
                         insert=(title_x, title_y_box),
                         font_size=title_fs,
                         fill=palette["text"]["primary"],
                         font_family=font_family,
                         font_weight="bold"))

        mech_centers.append((mc_x, by_box + box_h // 2, mc_x + mc_w, by_box + box_h // 2))

    # --- Right column: Outcome badges ---
    oc = bp.get("outcomes_column", {})
    oc_x = int(W * oc.get("x_pct", 0.72))
    oc_w = int(W * oc.get("width_pct", 0.24))
    oc_y = int(H * oc.get("y_start_pct", 0.72))
    badge_h = oc.get("badge_height", 56)
    badge_gap = oc.get("badge_gap", 16)
    badge_rx = oc.get("badge_rx", 28)
    badge_fs = oc.get("font_size", 28)
    badge_bg = oc.get("bg_color", "#059669")
    badge_text_color = oc.get("text_color", "#FFFFFF")
    badge_border = oc.get("border_color", "#047857")

    outcome_items = oc.get("items", [])
    outcome_centers = []  # for arrows
    for i, item in enumerate(outcome_items):
        oy = oc_y + i * (badge_h + badge_gap)
        text = item["text"]

        dwg.add(dwg.rect((oc_x, oy), (oc_w, badge_h),
                         fill=badge_bg, rx=badge_rx, ry=badge_rx,
                         stroke=badge_border, stroke_width=2,
                         opacity=0.92))
        dwg.add(dwg.text(text,
                         insert=(oc_x + oc_w // 2, oy + badge_h * 0.65),
                         font_size=badge_fs, fill=badge_text_color,
                         font_family=font_family, font_weight="bold",
                         text_anchor="middle"))
        outcome_centers.append((oc_x, oy + badge_h // 2))

    # --- Arrows: products -> mechanisms ---
    arrows_cfg = bp.get("arrows", {})
    arrow_color = arrows_cfg.get("color", "#9CA3AF")
    arrow_w = arrows_cfg.get("width", 3)
    arrow_opacity = arrows_cfg.get("opacity", 0.6)
    head_size = arrows_cfg.get("head_size", 10)

    for i, (px_end, py_center) in enumerate(product_centers):
        if i < len(mech_centers):
            mx_start = mech_centers[i][0]
            my_center = mech_centers[i][1]

            # Arrow from right edge of product pill to left edge of mechanism box
            gap_start = px_end + 8
            gap_end = mx_start - 8

            # Curved arrow
            ctrl_x = (gap_start + gap_end) / 2
            ctrl_y = (py_center + my_center) / 2
            path_d = f"M {gap_start},{py_center} Q {ctrl_x},{ctrl_y} {gap_end},{my_center}"
            dwg.add(dwg.path(d=path_d, fill="none",
                             stroke=arrow_color, stroke_width=arrow_w,
                             opacity=arrow_opacity, stroke_linecap="round"))
            # Arrowhead
            dwg.add(dwg.polygon([
                (gap_end - head_size, my_center - head_size * 0.5),
                (gap_end, my_center),
                (gap_end - head_size, my_center + head_size * 0.5),
            ], fill=arrow_color, opacity=arrow_opacity))

    # --- Arrows: mechanisms -> outcomes ---
    for i in range(len(mech_centers)):
        # Map multiple mechanisms to fewer outcomes
        outcome_idx = min(i, len(outcome_centers) - 1)
        if outcome_idx < 0:
            continue

        mx_end = mech_centers[i][2]
        my_center = mech_centers[i][3]
        ox_start = outcome_centers[outcome_idx][0]
        oy_center = outcome_centers[outcome_idx][1]

        gap_start = mx_end + 8
        gap_end = ox_start - 8

        ctrl_x = (gap_start + gap_end) / 2
        ctrl_y = (my_center + oy_center) / 2
        path_d = f"M {gap_start},{my_center} Q {ctrl_x},{ctrl_y} {gap_end},{oy_center}"
        dwg.add(dwg.path(d=path_d, fill="none",
                         stroke=arrow_color, stroke_width=arrow_w,
                         opacity=arrow_opacity, stroke_linecap="round"))
        # Arrowhead
        dwg.add(dwg.polygon([
            (gap_end - head_size, oy_center - head_size * 0.5),
            (gap_end, oy_center),
            (gap_end - head_size, oy_center + head_size * 0.5),
        ], fill=arrow_color, opacity=arrow_opacity))


# ===================================================================
# DRAWING: BAND 1 — LUMEN (adapted for full-width bronchus)
# ===================================================================

def draw_lumen(dwg, layout, palette, W, H):
    bx, by, bw, bh = get_band_rects(layout, W, H)["lumen"]
    bc = layout["band_content"]["lumen"]
    dc = layout.get("density", {})
    virus_color = palette["virus"]

    # Stipple texture
    stipple_color = palette.get("density", {}).get("lumen_stipple", "#CBD5E1")
    draw_stipple_field(dwg, bx, by, bw, bh,
                       color=stipple_color,
                       density=dc.get("lumen_stipple_density", 0.0005),
                       r_min=dc.get("stipple_r_min", 1.0),
                       r_max=dc.get("stipple_r_max", 2.0),
                       opacity=0.10, seed=100)

    # Viruses (sick side)
    random.seed(42)
    for i in range(bc["virus_count"]):
        vx_min = bx + int(bw * bc["virus_x_range"][0])
        vx_max = bx + int(bw * bc["virus_x_range"][1])
        vx = random.randint(vx_min, vx_max)
        vy = by + int(bh * 0.3) + random.randint(0, int(bh * 0.4))
        draw_virus_icon(dwg, vx, vy, bc["virus_radius"], virus_color)

    # Extra small virus particles
    extra_count = dc.get("virus_count_extra", 4)
    extra_r = dc.get("virus_extra_radius", 16)
    extra_x_range = dc.get("virus_extra_x_range", [0.02, 0.25])
    random.seed(200)
    for i in range(extra_count):
        vx = bx + int(bw * extra_x_range[0]) + random.randint(
            0, int(bw * (extra_x_range[1] - extra_x_range[0])))
        vy = by + int(bh * 0.15) + random.randint(0, int(bh * 0.7))
        draw_virus_icon(dwg, vx, vy, extra_r, virus_color)

    # Red arrows (viral invasion)
    for i in range(2):
        ax = bx + int(bw * 0.10) + i * int(bw * 0.08)
        ay = by + int(bh * 0.5)
        dwg.add(dwg.line((ax, ay), (ax + 40, ay),
                         stroke=virus_color, stroke_width=3, opacity=0.5))
        dwg.add(dwg.polygon(
            [(ax + 40, ay - 6), (ax + 52, ay), (ax + 40, ay + 6)],
            fill=virus_color, opacity=0.5
        ))

    # Mucus droplets (sick side)
    random.seed(99)
    for i in range(8):
        mx = bx + int(bw * 0.02) + random.randint(0, int(bw * 0.20))
        my = by + int(bh * 0.15) + random.randint(0, int(bh * 0.65))
        mr = random.randint(3, 9)
        draw_mucus_droplet(dwg, mx, my, mr, color="#D97706", opacity=0.40)

    # Convergence lines from product locations
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

    shield_x = epi_bx + int(epi_bw * epi_bc["shield_x_pct"]) + 60
    shield_y = epi_by + epi_bh // 2
    staple_x = epi_bx + int(epi_bw * 0.68)
    staple_y = epi_by + epi_bh // 2
    dc_healthy_x = lam_bx + int(lam_bw * lam_bc["dc_healthy_x_pct"])
    dc_y_center = lam_by + int(lam_bh * 0.72)
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

    # IgA Y shapes (healthy side)
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

    # Convergence glow
    dwg.add(dwg.circle((convergence_x, convergence_y), 14,
                       fill="#FFFFFF", opacity=0.45))
    dwg.add(dwg.circle((convergence_x, convergence_y), 9,
                       fill="#059669", opacity=0.18))


# ===================================================================
# DRAWING: BAND 2 — EPITHELIUM
# ===================================================================

def draw_epithelium(dwg, layout, palette, W, H):
    bx, by, bw, bh = get_band_rects(layout, W, H)["epithelium"]
    bc = layout["band_content"]["epithelium"]
    dc = layout.get("density", {})

    stipple_color = palette.get("density", {}).get("epithelium_stipple", "#9CA3AF")
    draw_stipple_field(dwg, bx, by, bw, bh,
                       color=stipple_color,
                       density=dc.get("epithelium_stipple_density", 0.0010),
                       r_min=dc.get("stipple_r_min", 1.0),
                       r_max=dc.get("stipple_r_max", 2.0),
                       opacity=0.08, seed=101)

    n_cells = dc.get("epithelium_cells", 42)
    cell_w = bw / n_cells
    cell_h = int(bh * bc["cell_height_pct"])
    cell_y = by + (bh - cell_h) // 2

    gap_indices = set()
    random.seed(7)
    sick_cell_limit = n_cells // 3
    candidates = list(range(sick_cell_limit))
    random.shuffle(candidates)
    for g in candidates[:bc["gap_count_sick"]]:
        gap_indices.add(g)

    om85_color = palette["products"]["om85"]
    pmbl_color = palette["products"]["pmbl"]
    nucleus_color = palette.get("density", {}).get("epithelium_nucleus", "#6B7280")
    tj_color = palette.get("density", {}).get("tight_junction", "#374151")
    nucleus_prob = dc.get("nucleus_probability", 0.7)
    n_cilia_cfg = dc.get("cilia_per_cell", 6)
    tj_n_zigs = dc.get("tight_junction_n_zigs", 6)
    tj_amplitude = dc.get("tight_junction_amplitude", 3)

    random.seed(300)

    for i in range(n_cells):
        cx = bx + int(i * cell_w)
        t = i / max(1, n_cells - 1)

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
            cell_rx = 2 + int(t * 2)
            dwg.add(dwg.rect(
                (cx + 1, cell_y), (int(cell_w) - 2, cell_h),
                fill=f"url(#{grad_id})", stroke="#D1D5DB", stroke_width=1,
                rx=cell_rx, ry=cell_rx
            ))

            if random.random() < nucleus_prob:
                nuc_cx = cx + cell_w * 0.5
                nuc_cy = cell_y + cell_h * 0.55
                nuc_rx = cell_w * 0.22
                nuc_ry = cell_h * 0.18
                draw_cell_nucleus(dwg, nuc_cx, nuc_cy, nuc_rx, nuc_ry,
                                  nucleus_color, opacity=0.25)

            if t > 0.25:
                cilia_h_base = int(cell_h * 0.20)
                cilia_scale = 0.35 + 0.65 * ((t - 0.25) / 0.75)
                cilia_h = max(2, int(cilia_h_base * cilia_scale))
                cilia_color = lerp_color(cell_base, "#1F2937", 0.3)
                wave_amp = dc.get("cilia_wave_amplitude", 2)
                for c in range(n_cilia_cfg):
                    cx_cilia = cx + int(cell_w * (c + 0.5) / n_cilia_cfg)
                    wave_offset = wave_amp * math.sin(c * 1.2 + i * 0.7)
                    dwg.add(dwg.line(
                        (cx_cilia, cell_y - 1),
                        (cx_cilia + wave_offset, cell_y - cilia_h),
                        stroke=cilia_color,
                        stroke_width=1.3, stroke_linecap="round"
                    ))

            if t > 0.50 and i > 0 and (i - 1) not in gap_indices:
                draw_tight_junction(dwg, cx, cell_y + int(cell_h * 0.1),
                                    cell_y + int(cell_h * 0.9),
                                    tj_color, n_zigs=tj_n_zigs,
                                    amplitude=tj_amplitude,
                                    stroke_width=1.0,
                                    opacity=0.3 + 0.3 * t)

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

    # OM-85 shield
    shield_x = bx + int(bw * bc["shield_x_pct"])
    shield_y = cell_y - 25
    shield_w, shield_h = 120, 130

    shield_path = f"M {shield_x},{shield_y} "
    shield_path += f"L {shield_x + shield_w},{shield_y} "
    shield_path += f"L {shield_x + shield_w},{shield_y + shield_h * 0.7} "
    shield_path += f"Q {shield_x + shield_w / 2},{shield_y + shield_h} {shield_x},{shield_y + shield_h * 0.7} Z"
    dwg.add(dwg.path(d=shield_path, fill=om85_color, opacity=0.6,
                     stroke=om85_color, stroke_width=2))

    lock_cx = shield_x + shield_w / 2
    lock_cy = shield_y + shield_h * 0.4
    dwg.add(dwg.circle((lock_cx, lock_cy), 12, fill="none",
                       stroke="white", stroke_width=3))
    dwg.add(dwg.rect((lock_cx - 10, lock_cy + 8), (20, 16),
                     fill="white", rx=2))
    dwg.add(dwg.text("OM-85",
                     insert=(lock_cx, lock_cy + 38),
                     font_size=18, fill="white",
                     font_family=layout["font"]["family"],
                     font_weight="bold",
                     text_anchor="middle",
                     opacity=0.9))


# ===================================================================
# DRAWING: BAND 3 — LAMINA PROPRIA
# ===================================================================

def draw_lamina_propria(dwg, layout, palette, W, H):
    bx, by, bw, bh = get_band_rects(layout, W, H)["lamina"]
    bc = layout["band_content"]["lamina"]
    dc_cfg = layout.get("density", {})

    split_y = by + int(bh * bc["split_pct"])

    om85_color = palette["products"]["om85"]
    mv130_color = palette["products"]["mv130"]
    crl1505_color = palette["products"]["crl1505"]
    pmbl_color = palette["products"]["pmbl"]

    density_pal = palette.get("density", {})

    # Stipple
    stipple_color = density_pal.get("lamina_stipple", "#D1D5DB")
    draw_stipple_field(dwg, bx, by, bw, bh,
                       color=stipple_color,
                       density=dc_cfg.get("lamina_stipple_density", 0.0008),
                       r_min=dc_cfg.get("stipple_r_min", 1.0),
                       r_max=dc_cfg.get("stipple_r_max", 2.0),
                       opacity=0.10, seed=102)

    # Crosshatch
    draw_crosshatch(dwg, bx, by, bw, bh,
                    color=stipple_color,
                    spacing=dc_cfg.get("lamina_crosshatch_spacing", 36),
                    stroke_width=0.6,
                    opacity=dc_cfg.get("lamina_crosshatch_opacity", 0.04))

    dc_radius = bc.get("dc_radius", 48)

    # Dormant DC (sick side)
    dc_x_sick = bx + int(bw * bc["dc_sick_x_pct"])
    dc_y = split_y + int((by + bh - split_y) * 0.5)
    dormant_color = "#6B7280"

    dwg.add(dwg.circle((dc_x_sick, dc_y), dc_radius * 1.5,
                       fill="#DC2626", opacity=0.06))
    dwg.add(dwg.circle((dc_x_sick, dc_y), dc_radius * 1.2,
                       fill="#DC2626", opacity=0.08))
    draw_dc_cell(dwg, dc_x_sick, dc_y, dc_radius, dormant_color,
                 active=False, helix_color=None)

    # Active DC with MV130 helix (right side)
    dc_x_healthy = bx + int(bw * bc["dc_healthy_x_pct"])
    draw_dc_cell(dwg, dc_x_healthy, dc_y, dc_radius * 1.2,
                 mv130_color, active=True, helix_color=mv130_color)

    # OM-85 blue halo
    dwg.add(dwg.circle((dc_x_healthy, dc_y), dc_radius * 1.6,
                       fill="none", stroke=om85_color, stroke_width=2,
                       stroke_dasharray="4,3", opacity=0.5))

    # PMBL secondary mark
    pmbl_dot_x = dc_x_healthy + dc_radius * 1.3
    pmbl_dot_y = dc_y - dc_radius * 0.5
    dwg.add(dwg.circle((pmbl_dot_x, pmbl_dot_y), 7,
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

    # Macrophages
    mac_r = dc_cfg.get("macrophage_radius", 20)
    mac_dormant_color = density_pal.get("macrophage_dormant", "#9CA3AF")
    mac_active_color = density_pal.get("macrophage_active", "#3B82F6")

    mac_sick_count = dc_cfg.get("macrophage_count_sick", 2)
    random.seed(400)
    for m in range(mac_sick_count):
        mx = bx + int(bw * 0.06) + random.randint(0, int(bw * 0.14))
        my = split_y + random.randint(int((by + bh - split_y) * 0.15),
                                       int((by + bh - split_y) * 0.85))
        draw_macrophage(dwg, mx, my, mac_r, mac_dormant_color,
                        active=False, opacity=0.45, seed=m + 400)

    mac_healthy_count = dc_cfg.get("macrophage_count_healthy", 3)
    for m in range(mac_healthy_count):
        mx = bx + int(bw * 0.55) + random.randint(0, int(bw * 0.30))
        my = split_y + random.randint(int((by + bh - split_y) * 0.15),
                                       int((by + bh - split_y) * 0.85))
        draw_macrophage(dwg, mx, my, mac_r, mac_active_color,
                        active=True, opacity=0.45, seed=m + 410)

    # T-helper cells
    th_color = density_pal.get("t_helper", "#60A5FA")
    th_count = dc_cfg.get("t_helper_count", 4)
    th_r = dc_cfg.get("t_helper_radius", 14)
    random.seed(500)
    for t_i in range(th_count):
        tx = bx + int(bw * 0.30) + random.randint(0, int(bw * 0.55))
        ty = by + random.randint(int((split_y - by) * 0.15),
                                  int((split_y - by) * 0.85))
        draw_t_helper(dwg, tx, ty, th_r, th_color, opacity=0.5,
                      font_family=layout["font"]["family"])

    # Treg cells
    treg_color = density_pal.get("treg", "#34D399")
    treg_count = dc_cfg.get("treg_count", 2)
    treg_r = dc_cfg.get("treg_radius", 16)
    for t_i in range(treg_count):
        tx = bx + int(bw * 0.65) + random.randint(0, int(bw * 0.25))
        ty = by + random.randint(int((split_y - by) * 0.2),
                                  int((split_y - by) * 0.8))
        draw_t_helper(dwg, tx, ty, treg_r, treg_color, label="Treg",
                      opacity=0.55, font_family=layout["font"]["family"])

    # Immune cell scatter dots
    scatter_density = dc_cfg.get("immune_scatter_density", 0.0006)
    scatter_r_min = dc_cfg.get("immune_scatter_r_min", 3)
    scatter_r_max = dc_cfg.get("immune_scatter_r_max", 6)
    draw_stipple_field(dwg, bx, by, int(bw * 0.35), bh,
                       color="#F87171",
                       density=scatter_density * 0.8,
                       r_min=scatter_r_min, r_max=scatter_r_max,
                       opacity=0.12, seed=600)
    draw_stipple_field(dwg, bx + int(bw * 0.55), by, int(bw * 0.45), bh,
                       color=om85_color,
                       density=scatter_density * 0.5,
                       r_min=scatter_r_min, r_max=scatter_r_max,
                       opacity=0.08, seed=601)

    # UPPER: Adaptive Balance
    bal_x_sick = bx + int(bw * 0.17)
    bal_y = by + int((split_y - by) * 0.5)
    draw_th_balance(dwg, bal_x_sick, bal_y, bc["balance_width"] * 0.8,
                    "#9CA3AF", balanced=False,
                    text_color=palette["text"]["secondary"],
                    font_family=layout["font"]["family"])

    bal_x_healthy = bx + int(bw * bc["balance_x_pct"])
    draw_th_balance(dwg, bal_x_healthy, bal_y, bc["balance_width"],
                    om85_color, balanced=True,
                    text_color=palette["text"]["secondary"],
                    font_family=layout["font"]["family"])


# ===================================================================
# DRAWING: BAND 4 — MUSCLE LISSE
# ===================================================================

def draw_muscle(dwg, layout, palette, W, H):
    bx, by, bw, bh = get_band_rects(layout, W, H)["muscle"]
    bc = layout["band_content"]["muscle"]
    dc_cfg = layout.get("density", {})
    density_pal = palette.get("density", {})

    draw_gradient_band(dwg, bx, by, bw, bh,
                       palette["bands"]["muscle_sick"],
                       palette["bands"]["muscle_healthy"],
                       n_slices=40, opacity=0.7,
                       thickness_left=bc["thickness_sick_pct"],
                       thickness_right=bc["thickness_healthy_pct"])

    fiber_color = density_pal.get("muscle_fiber", "#92400E")
    n_fibers = dc_cfg.get("muscle_fiber_count", 12)
    fiber_opacity = dc_cfg.get("muscle_fiber_opacity", 0.08)
    draw_fiber_lines(dwg, bx, by, bw, bh,
                     color=fiber_color,
                     n_fibers=n_fibers,
                     stroke_width=1.2,
                     opacity=fiber_opacity,
                     seed=700)


# ===================================================================
# CRL1505 RELAY ARC
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

    # Intestine icon
    squig_w = 40
    squig_path = f"M {gut_x - squig_w},{gut_y} "
    for j in range(6):
        sy = gut_y + (12 if j % 2 == 0 else -12)
        sx = gut_x - squig_w + (j + 1) * squig_w * 2 / 6
        squig_path += f"S {sx - 5},{sy} {sx},{gut_y} "
    dwg.add(dwg.path(d=squig_path, fill="none",
                     stroke=crl_color, stroke_width=3.5, opacity=0.7))
    dwg.add(dwg.text("gut", insert=(gut_x + squig_w + 8, gut_y + 10),
                     font_size=32, fill=crl_color, opacity=0.8,
                     font_family="Helvetica, Arial, sans-serif"))

    # Arc from gut to lamina
    mid_x = (gut_x + target_x) / 2 + 60
    mid_y = (gut_y + target_y) / 2
    arc_path = f"M {gut_x},{gut_y - 15} Q {mid_x},{mid_y} {target_x},{target_y}"
    dwg.add(dwg.path(d=arc_path, fill="none",
                     stroke=crl_color, stroke_width=relay["arc_width"],
                     stroke_dasharray="10,5", opacity=0.55))
    dwg.add(dwg.polygon(
        [(target_x - 7, target_y + 2), (target_x, target_y - 12), (target_x + 7, target_y + 2)],
        fill=crl_color, opacity=0.55
    ))


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

    svg_path = os.path.join(OUT_DIR, "wireframe_GA_v17.svg")
    full_png = os.path.join(OUT_DIR, "wireframe_GA_v17_full.png")
    delivery_png = os.path.join(OUT_DIR, "wireframe_GA_v17_delivery.png")

    print(f"Canvas: {W}x{H}, delivery: {dw}x{dh}")

    dwg = svgwrite.Drawing(svg_path, size=(f"{W}px", f"{H}px"),
                           viewBox=f"0 0 {W} {H}")
    dwg.attribs["xmlns"] = "http://www.w3.org/2000/svg"

    # 0. Accessibility patterns
    print("  Adding accessibility patterns...")
    add_product_patterns(dwg, palette)

    # 1. V15: Clean white background (no gradient)
    print("  Drawing background...")
    draw_background(dwg, layout, palette, W, H)

    # 2. Product pills (above bronchus, centered)
    print("  Drawing product pills...")
    draw_product_pills(dwg, layout, palette, content, W, H)

    # 3. Bronchus glow
    print("  Drawing bronchus glow...")
    draw_bronchus_glow(dwg, layout, W, H)

    # 4. Bronchus frame + band separators
    print("  Drawing bronchus frame...")
    draw_bronchus_frame(dwg, layout, palette, W, H)

    # 5. Band 4: Muscle (bottom, behind everything)
    print("  Drawing muscle band...")
    draw_muscle(dwg, layout, palette, W, H)

    # 6. Band 2: Epithelium
    print("  Drawing epithelium...")
    draw_epithelium(dwg, layout, palette, W, H)

    # 7. Band 1: Lumen
    print("  Drawing lumen...")
    draw_lumen(dwg, layout, palette, W, H)

    # 8. Band 3: Lamina propria
    print("  Drawing lamina propria...")
    draw_lamina_propria(dwg, layout, palette, W, H)

    # 9. V15: Central directional arrow
    print("  Drawing central arrow...")
    draw_central_arrow(dwg, layout, W, H)

    # 10. CRL1505 relay arc
    print("  Drawing CRL1505 relay...")
    draw_crl1505_relay(dwg, layout, palette, W, H)

    # 11. Child silhouettes — at the edges of the canvas
    print("  Drawing children...")
    cs = layout["child_sick"]
    child_sick_x = int(W * cs["x_pct"])
    child_sick_y = int(H * cs["y_pct"])
    draw_child_contour(dwg, child_sick_x, child_sick_y, cs["scale"],
                       _CONTOUR_SICK, palette["virus"], is_sick=True)

    ch = layout["child_healthy"]
    child_healthy_x = int(W * ch["x_pct"])
    child_healthy_y = int(H * ch["y_pct"])
    draw_child_contour(dwg, child_healthy_x, child_healthy_y, ch["scale"],
                       _CONTOUR_HEALTHY, palette["products"]["crl1505"],
                       is_sick=False)

    # 12. Vicious cycle (bottom-left of top panel)
    print("  Drawing vicious cycle...")
    draw_vicious_cycle(dwg, layout, palette, W, H)

    # 13. Evidence bars (bottom-right of top panel)
    print("  Drawing evidence bars...")
    draw_evidence_bars(dwg, layout, palette, W, H)

    # 14. Band labels
    print("  Drawing band labels...")
    draw_band_labels(dwg, layout, palette, W, H)

    # 15. Zone orientation text
    print("  Drawing zone orientation...")
    draw_zone_orientation(dwg, layout, palette, W, H)

    # 16. Panel divider
    print("  Drawing panel divider...")
    draw_panel_divider(dwg, layout, W, H)

    # 17. V15: Bottom panel (mechanism flow)
    print("  Drawing bottom panel...")
    draw_bottom_panel(dwg, layout, palette, content, W, H)

    # Save SVG
    dwg.save()
    print(f"\nSVG saved: {svg_path}")

    # Render PNG
    print("Rendering PNG...")
    render_png(svg_path, full_png, delivery_png, W, H, dw, dh)

    print("\nV15 compilation complete.")


if __name__ == "__main__":
    main()
