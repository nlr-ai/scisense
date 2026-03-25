"""
vec_lib — Reusable VEC (Visual Evidence Compiler) drawing primitives.

Pure SVG drawing functions for parametric scientific figures.
No global state. All dependencies passed as parameters.
"""

import math
import os
import random


# ===================================================================
# COLOR UTILITIES
# ===================================================================

def lighten_hex(hex_color, factor=0.35):
    """Lighten a hex color toward white by the given factor (0-1)."""
    h = hex_color.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    r = int(r + (255 - r) * factor)
    g = int(g + (255 - g) * factor)
    b = int(b + (255 - b) * factor)
    return f"#{r:02x}{g:02x}{b:02x}"


def lerp_color(c1, c2, t):
    """Linearly interpolate between two hex colors. t=0 -> c1, t=1 -> c2."""
    h1, h2 = c1.lstrip("#"), c2.lstrip("#")
    r = int(int(h1[0:2], 16) * (1 - t) + int(h2[0:2], 16) * t)
    g = int(int(h1[2:4], 16) * (1 - t) + int(h2[2:4], 16) * t)
    b = int(int(h1[4:6], 16) * (1 - t) + int(h2[4:6], 16) * t)
    return f"#{r:02x}{g:02x}{b:02x}"


def darken_hex(hex_color, factor=0.3):
    """Darken a hex color toward black by the given factor (0-1)."""
    h = hex_color.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    r = int(r * (1 - factor))
    g = int(g * (1 - factor))
    b = int(b * (1 - factor))
    return f"#{r:02x}{g:02x}{b:02x}"


# ===================================================================
# SPLINE UTILITIES
# ===================================================================

def catmull_rom_to_bezier(points):
    """Convert Catmull-Rom spline control points to cubic Bezier segments.

    Returns list of ((cp1x, cp1y), (cp2x, cp2y), (endx, endy)) tuples.
    """
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


# ===================================================================
# DRAWING: VIRUS ICON
# ===================================================================

def draw_virus_icon(dwg, cx, cy, r, color):
    """Simple virus: circle + spikes with spherical tips."""
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


# ===================================================================
# DRAWING: IgA Y-SHAPE ANTIBODY
# ===================================================================

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


# ===================================================================
# DRAWING: DENDRITIC CELL
# ===================================================================

def draw_dc_cell(dwg, cx, cy, radius, color, active=False, helix_color=None):
    """Dendritic cell with irregular branches.

    Args:
        dwg: svgwrite Drawing
        cx, cy: center coordinates
        radius: outer radius including branches
        color: base cell color (hex)
        active: if True, longer branches + glow
        helix_color: if set, draw MV130 helix in nucleus (trained immunity)
    """
    n_branches = 7
    random.seed(int(cx) + int(cy))

    # Body
    body_fill = color if not active else lighten_hex(color, 0.3)
    dwg.add(dwg.circle((cx, cy), radius * 0.5, fill=body_fill, opacity=0.6))

    # Nucleus
    nucleus_r = radius * 0.25
    dwg.add(dwg.circle((cx, cy), nucleus_r, fill=color, opacity=0.8))

    # Branches
    for i in range(n_branches):
        angle = 2 * math.pi * i / n_branches + random.uniform(-0.3, 0.3)
        branch_len = radius * (0.7 + random.uniform(0, 0.5))
        if active:
            branch_len *= 1.3
        bx = cx + branch_len * math.cos(angle)
        by = cy + branch_len * math.sin(angle)
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
        amp = nucleus_r * 0.4
        prev_x1, prev_x2, prev_y = None, None, None
        for j in range(20):
            t = j / 19
            y = hy_start + (hy_end - hy_start) * t
            x1 = hx + amp * math.sin(t * math.pi * 3)
            x2 = hx - amp * math.sin(t * math.pi * 3)
            if prev_x1 is not None:
                dwg.add(dwg.line((prev_x1, prev_y), (x1, y),
                                 stroke=helix_color, stroke_width=1.5))
                dwg.add(dwg.line((prev_x2, prev_y), (x2, y),
                                 stroke=helix_color, stroke_width=1.5))
            prev_x1, prev_x2, prev_y = x1, x2, y
        # Trained immunity glow (gold)
        dwg.add(dwg.circle((cx, cy), nucleus_r * 1.5,
                           fill="#FDE68A", opacity=0.15))


# ===================================================================
# DRAWING: Th1/Th2 BALANCE SCALE
# ===================================================================

def draw_th_balance(dwg, cx, cy, width, color_active, balanced=True,
                    text_color="#6B7280", font_family="Helvetica, Arial, sans-serif"):
    """Th1/Th2 balance scale.

    Args:
        dwg: svgwrite Drawing
        cx, cy: center of the beam
        width: total beam width
        color_active: color for balanced state beam/pans
        balanced: if False, tilts toward Th2
        text_color: color for Th1/Th2 labels
        font_family: font family string
    """
    # Fulcrum triangle
    tri_h = 22
    dwg.add(dwg.polygon(
        [(cx, cy + tri_h), (cx - 12, cy + tri_h + 14), (cx + 12, cy + tri_h + 14)],
        fill="#9CA3AF"
    ))
    # Beam
    tilt = 0 if balanced else 12
    lx = cx - width / 2
    rx = cx + width / 2
    ly = cy - tilt
    ry = cy + tilt
    dwg.add(dwg.line((lx, ly), (rx, ry),
                     stroke=color_active if balanced else "#9CA3AF",
                     stroke_width=4))
    # Pans
    pan_w = 30
    dwg.add(dwg.rect((lx - pan_w / 2, ly - 4), (pan_w, 8),
                     fill=color_active if balanced else "#6B7280", rx=2))
    dwg.add(dwg.rect((rx - pan_w / 2, ry - 4), (pan_w, 8),
                     fill=color_active if balanced else "#DC2626", rx=2))
    # Labels
    font_s = 26
    dwg.add(dwg.text("Th1", insert=(lx - 5, ly - 14),
                     font_size=font_s, fill=text_color,
                     font_family=font_family,
                     text_anchor="middle"))
    dwg.add(dwg.text("Th2", insert=(rx + 5, ry - 14),
                     font_size=font_s, fill=text_color,
                     font_family=font_family,
                     text_anchor="middle"))


# ===================================================================
# DRAWING: CHILD SILHOUETTE (organic contour from extracted points)
# ===================================================================

def draw_child_contour(dwg, cx, cy, scale, contour_points, fill_color, is_sick=True):
    """Draw child silhouette from extracted contour points.

    Args:
        dwg: svgwrite Drawing
        cx, cy: center position
        scale: size multiplier
        contour_points: list of [x, y] from JSON contour extraction
        fill_color: hex color
        is_sick: if True, draws distress lines; else sparkles
    """
    if not contour_points:
        dwg.add(dwg.circle((cx, cy), 20 * scale, fill=fill_color, opacity=0.5))
        return

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

    if len(transformed) >= 4:
        padded = [transformed[-1]] + transformed + [transformed[0], transformed[1]]
        segments = catmull_rom_to_bezier(padded)
        if segments:
            path_d = f"M {transformed[0][0]},{transformed[0][1]} "
            for cp1, cp2, end in segments:
                path_d += f"C {cp1[0]},{cp1[1]} {cp2[0]},{cp2[1]} {end[0]},{end[1]} "
            path_d += "Z"
            dwg.add(dwg.path(d=path_d, fill=fill_color, opacity=0.75,
                             stroke=fill_color, stroke_width=1.5))
    else:
        dwg.add(dwg.polygon(transformed, fill=fill_color, opacity=0.6))

    # Expression marks
    head_y = cy - target_h * 0.35
    if is_sick:
        for j in range(3):
            lx = cx + target_w * 0.3 + j * 8
            ly = head_y - 10 + j * 6
            dwg.add(dwg.line((lx, ly), (lx + 10, ly - 5),
                             stroke=fill_color, stroke_width=1.5, opacity=0.5))
    else:
        for j in range(3):
            sx = cx + target_w * 0.25 + j * 15
            sy = head_y - 15 + j * 8
            dwg.add(dwg.line((sx - 4, sy), (sx + 4, sy),
                             stroke=fill_color, stroke_width=1.5))
            dwg.add(dwg.line((sx, sy - 4), (sx, sy + 4),
                             stroke=fill_color, stroke_width=1.5))


# ===================================================================
# DRAWING: GRADIENT BAND
# ===================================================================

def draw_gradient_band(dwg, x, y, w, h, color_left, color_right, n_slices=40,
                       opacity=0.7, thickness_left=1.0, thickness_right=1.0):
    """Draw a horizontal band with color lerp and optional thickness taper.

    Args:
        dwg: svgwrite Drawing
        x, y, w, h: bounding rectangle
        color_left, color_right: hex colors for left and right ends
        n_slices: number of vertical slices for the gradient
        opacity: fill opacity
        thickness_left: fraction of h at left edge (1.0 = full)
        thickness_right: fraction of h at right edge
    """
    for i in range(n_slices):
        t = i / max(1, n_slices - 1)
        sx = x + int(w * t)
        sw = max(1, w // n_slices + 1)
        thickness_pct = thickness_left * (1 - t) + thickness_right * t
        slice_h = int(h * thickness_pct)
        slice_y = y + (h - slice_h) // 2
        color = lerp_color(color_left, color_right, t)
        dwg.add(dwg.rect((sx, slice_y), (sw, slice_h), fill=color, opacity=opacity))


# ===================================================================
# DRAWING: MUCUS DROPLET
# ===================================================================

def draw_mucus_droplet(dwg, cx, cy, r, color="#D97706", opacity=0.5):
    """Small mucus droplet (amber circle with highlight)."""
    dwg.add(dwg.circle((cx, cy), r, fill=color, opacity=opacity))
    # Small highlight
    dwg.add(dwg.circle((cx - r * 0.25, cy - r * 0.25), r * 0.35,
                       fill="#FFFFFF", opacity=0.4))


# ===================================================================
# DRAWING: STIPPLE TEXTURE (organic tissue background)
# ===================================================================

def draw_stipple_field(dwg, x, y, w, h, color, density=0.003,
                       r_min=1, r_max=3, opacity=0.15, seed=0):
    """Fill a rectangular region with random stipple dots.

    Args:
        dwg: svgwrite Drawing
        x, y, w, h: bounding rectangle
        color: dot fill color (hex)
        density: dots per square pixel (e.g. 0.003 = ~3 dots per 1000 px^2)
        r_min, r_max: dot radius range
        opacity: dot opacity
        seed: random seed for reproducibility
    """
    n_dots = max(1, int(w * h * density))
    rng = random.Random(seed)
    for _ in range(n_dots):
        dx = x + rng.random() * w
        dy = y + rng.random() * h
        dr = rng.uniform(r_min, r_max)
        dwg.add(dwg.circle((dx, dy), dr, fill=color, opacity=opacity))


# ===================================================================
# DRAWING: CROSS-HATCH TEXTURE (fibrous tissue)
# ===================================================================

def draw_crosshatch(dwg, x, y, w, h, color, spacing=18,
                    stroke_width=0.8, opacity=0.12, angle_deg=45):
    """Fill a rectangle with a cross-hatch pattern (two sets of parallel lines).

    Args:
        dwg: svgwrite Drawing
        x, y, w, h: bounding rectangle
        color: line color (hex)
        spacing: distance between parallel lines
        stroke_width: line width
        opacity: line opacity
        angle_deg: angle of primary hatch lines (secondary = -angle)
    """
    # We create a clipping path to constrain lines to the rectangle
    clip_id = f"clip_hatch_{int(x)}_{int(y)}"
    clip = dwg.defs.add(dwg.clipPath(id=clip_id))
    clip.add(dwg.rect((x, y), (w, h)))

    g = dwg.g(clip_path=f"url(#{clip_id})")

    diag = math.sqrt(w * w + h * h)
    cx_r, cy_r = x + w / 2, y + h / 2

    for angle_sign in [1, -1]:
        angle = math.radians(angle_deg * angle_sign)
        cos_a, sin_a = math.cos(angle), math.sin(angle)
        n_lines = int(diag / spacing) + 2
        for i in range(-n_lines, n_lines + 1):
            offset = i * spacing
            # Line perpendicular to angle, shifted by offset
            px = cx_r + offset * (-sin_a)
            py = cy_r + offset * cos_a
            x1 = px - diag * cos_a
            y1 = py - diag * sin_a
            x2 = px + diag * cos_a
            y2 = py + diag * sin_a
            g.add(dwg.line((x1, y1), (x2, y2),
                           stroke=color, stroke_width=stroke_width,
                           opacity=opacity))
    dwg.add(g)


# ===================================================================
# DRAWING: FIBER PATTERN (muscle/connective tissue)
# ===================================================================

def draw_fiber_lines(dwg, x, y, w, h, color, n_fibers=12,
                     stroke_width=1.0, opacity=0.15, seed=0):
    """Draw wavy horizontal fiber lines across a rectangular region.

    Args:
        dwg: svgwrite Drawing
        x, y, w, h: bounding rectangle
        color: fiber color (hex)
        n_fibers: number of fiber lines
        stroke_width: line width
        opacity: line opacity
        seed: random seed
    """
    rng = random.Random(seed)
    for i in range(n_fibers):
        fy = y + h * (i + 0.5) / n_fibers + rng.uniform(-2, 2)
        n_pts = 8
        pts = []
        for j in range(n_pts):
            px = x + w * j / (n_pts - 1)
            py = fy + rng.uniform(-h * 0.06, h * 0.06)
            pts.append((px, py))
        if len(pts) >= 4:
            padded = [pts[0]] + pts + [pts[-1]]
            segments = catmull_rom_to_bezier(padded)
            if segments:
                path_d = f"M {pts[0][0]},{pts[0][1]} "
                for cp1, cp2, end in segments:
                    path_d += f"C {cp1[0]},{cp1[1]} {cp2[0]},{cp2[1]} {end[0]},{end[1]} "
                dwg.add(dwg.path(d=path_d, fill="none",
                                 stroke=color, stroke_width=stroke_width,
                                 opacity=opacity))


# ===================================================================
# DRAWING: TIGHT JUNCTION (zigzag between epithelial cells)
# ===================================================================

def draw_tight_junction(dwg, x, y_top, y_bottom, color, n_zigs=5,
                        amplitude=3, stroke_width=1.2, opacity=0.5):
    """Draw a zigzag tight junction line between two epithelial cells.

    Args:
        dwg: svgwrite Drawing
        x: x position of the junction
        y_top, y_bottom: vertical extent
        color: junction color (hex)
        n_zigs: number of zigzag segments
        amplitude: horizontal displacement of zigzag
        stroke_width: line width
        opacity: line opacity
    """
    h = y_bottom - y_top
    pts = []
    for i in range(n_zigs * 2 + 1):
        t = i / (n_zigs * 2)
        py = y_top + h * t
        px = x + amplitude * (1 if i % 2 == 1 else -1 if i % 2 == 0 and i > 0 else 0)
        pts.append((px, py))
    path_d = f"M {pts[0][0]},{pts[0][1]} "
    for px, py in pts[1:]:
        path_d += f"L {px},{py} "
    dwg.add(dwg.path(d=path_d, fill="none", stroke=color,
                     stroke_width=stroke_width, opacity=opacity))


# ===================================================================
# DRAWING: CELL NUCLEUS (organelle hint)
# ===================================================================

def draw_cell_nucleus(dwg, cx, cy, rx, ry, color, opacity=0.35):
    """Draw an elliptical nucleus with a nucleolus dot inside.

    Args:
        dwg: svgwrite Drawing
        cx, cy: center
        rx, ry: horizontal and vertical radii
        color: nucleus color (hex)
        opacity: fill opacity
    """
    dwg.add(dwg.ellipse((cx, cy), (rx, ry), fill=color, opacity=opacity,
                        stroke=color, stroke_width=0.8, stroke_opacity=opacity + 0.1))
    # Nucleolus (darker small dot)
    dwg.add(dwg.circle((cx + rx * 0.15, cy - ry * 0.1), min(rx, ry) * 0.3,
                       fill=color, opacity=min(1.0, opacity + 0.2)))


# ===================================================================
# DRAWING: MACROPHAGE (irregular amoeboid shape)
# ===================================================================

def draw_macrophage(dwg, cx, cy, radius, color, active=False, opacity=0.6, seed=0):
    """Draw a macrophage with an irregular amoeboid outline.

    Args:
        dwg: svgwrite Drawing
        cx, cy: center
        radius: approximate radius
        color: fill color (hex)
        active: if True, brighter fill + pseudopods extended
        opacity: fill opacity
        seed: random seed
    """
    rng = random.Random(seed)
    n_points = 10
    pts = []
    for i in range(n_points):
        angle = 2 * math.pi * i / n_points
        r_var = radius * (0.75 + rng.uniform(0, 0.5))
        if active:
            r_var *= 1.2
        pts.append((cx + r_var * math.cos(angle), cy + r_var * math.sin(angle)))

    if len(pts) >= 4:
        padded = [pts[-1]] + pts + [pts[0], pts[1]]
        segments = catmull_rom_to_bezier(padded)
        if segments:
            fill_color = lighten_hex(color, 0.2) if active else color
            path_d = f"M {pts[0][0]},{pts[0][1]} "
            for cp1, cp2, end in segments:
                path_d += f"C {cp1[0]},{cp1[1]} {cp2[0]},{cp2[1]} {end[0]},{end[1]} "
            path_d += "Z"
            dwg.add(dwg.path(d=path_d, fill=fill_color, opacity=opacity,
                             stroke=color, stroke_width=1.5))

    # Nucleus (kidney-shaped = ellipse offset)
    nuc_rx = radius * 0.35
    nuc_ry = radius * 0.25
    dwg.add(dwg.ellipse((cx - radius * 0.1, cy), (nuc_rx, nuc_ry),
                        fill=darken_hex(color, 0.3), opacity=min(1.0, opacity + 0.15)))


# ===================================================================
# DRAWING: T-HELPER CELL (small round cell with halo)
# ===================================================================

def draw_t_helper(dwg, cx, cy, radius, color, label=None, opacity=0.6,
                  font_family="Helvetica, Arial, sans-serif"):
    """Draw a T-helper cell (small round cell with optional label).

    Args:
        dwg: svgwrite Drawing
        cx, cy: center
        radius: cell radius
        color: fill color
        label: optional label (e.g. "Th1", "Treg")
        opacity: fill opacity
        font_family: font for label
    """
    # Outer membrane
    dwg.add(dwg.circle((cx, cy), radius, fill=color, opacity=opacity,
                       stroke=darken_hex(color, 0.2), stroke_width=1.2))
    # Nucleus
    dwg.add(dwg.circle((cx, cy), radius * 0.55, fill=darken_hex(color, 0.25),
                       opacity=min(1.0, opacity + 0.1)))
    if label:
        dwg.add(dwg.text(label, insert=(cx, cy + radius * 0.25),
                         font_size=max(8, int(radius * 0.7)),
                         fill="white", font_family=font_family,
                         text_anchor="middle", font_weight="bold"))


# ===================================================================
# RENDERING: SVG -> PNG via Playwright
# ===================================================================

def render_png(svg_path, full_png, delivery_png, W, H, dw, dh):
    """Render SVG to full-resolution PNG and delivery PNG via Playwright.

    Args:
        svg_path: path to the source SVG
        full_png: output path for the full-resolution screenshot
        delivery_png: output path for the delivery-sized PNG
        W, H: canvas dimensions (used for reference, not rendering)
        dw, dh: delivery dimensions (viewport size for Playwright)
    """
    try:
        from PIL import Image
        Image.MAX_IMAGE_PIXELS = 300_000_000

        from playwright.sync_api import sync_playwright

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
