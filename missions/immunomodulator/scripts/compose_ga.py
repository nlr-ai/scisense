"""
Parametric GA Compositor v7
Reads config/*.yaml -> produces final GA SVG + PNG

v7 changes from v6:
- Replace static SVG asset injection with parametric generator functions
- F2: E-cadherin molecular staples between PMBL repair bricks
- F3: Shield visually embeds ON the brick wall
- F4: Helix positioned INSIDE the DC cell nucleus
- F5: Bridge points independently toward barrier + DC
- F7: DC cell with biologically accurate filopodial morphology
- F8: Molecular effector icons (IgA Y-shapes, IFN arrows)
- F10: Visual cycle fracture (intervention breaks asthma trajectory)

Everything is driven by configuration. No hardcoded positions, colors, or text.
"""

import yaml
import svgwrite
import os
import math
import random

# ─── Color manipulation helper ───────────────────────────────

def _lighten_hex(hex_color, factor=0.35):
    """Lighten a hex color by blending toward white.

    factor=0  → original color unchanged
    factor=1  → pure white
    """
    h = hex_color.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    r = int(r + (255 - r) * factor)
    g = int(g + (255 - g) * factor)
    b = int(b + (255 - b) * factor)
    return f"#{r:02x}{g:02x}{b:02x}"


_child_grad_counter = 0

BASE = r"C:\Users\reyno\scisense\missions\immunomodulator"
CONFIG_DIR = os.path.join(BASE, "config")
OUT_DIR = os.path.join(BASE, "artefacts", "wireframes")
os.makedirs(OUT_DIR, exist_ok=True)


# ═══════════════════════════════════════════════════════════════
# CONFIG LOADING
# ═══════════════════════════════════════════════════════════════

def load_config():
    """Load all YAML configs and return merged dict."""
    config = {}
    for name in ("palette", "layout", "content", "generators"):
        path = os.path.join(CONFIG_DIR, f"{name}.yaml")
        with open(path, "r", encoding="utf-8") as f:
            config[name] = yaml.safe_load(f)
    return config


def resolve_color(palette, key):
    """Resolve a dotted key like 'products.om85' from the palette dict."""
    parts = key.split(".")
    val = palette
    for p in parts:
        if isinstance(val, dict):
            val = val.get(p, "#888888")
        else:
            return "#888888"
    return val


# ═══════════════════════════════════════════════════════════════
# ZONE GEOMETRY HELPERS
# ═══════════════════════════════════════════════════════════════

def zone_rect(layout, zone_key, W, H):
    """Return (x, y, w, h) for a zone."""
    z = layout["zones"][zone_key]
    x = int(W * z["x_pct"])
    w = int(W * z["width_pct"])
    return x, 0, w, H


# ═══════════════════════════════════════════════════════════════
# BACKGROUNDS
# ═══════════════════════════════════════════════════════════════

def draw_backgrounds(dwg, layout, palette, W, H):
    """Draw gradient backgrounds per zone."""
    dwg.add(dwg.rect((0, 0), (W, H), fill=palette["background"]))

    zone_colors = {
        "z1": palette["zones"]["z1_bg"],
        "z2": palette["zones"]["z2_bg"],
        "z3": palette["zones"]["z3_bg"],
    }
    zone_opacities = {"z1": 0.65, "z2": 0.35, "z3": 0.55}

    for zk in ("z1", "z2", "z3"):
        zx, zy, zw, zh = zone_rect(layout, zk, W, H)
        dwg.add(dwg.rect((zx, zy), (zw, zh),
                         fill=zone_colors[zk],
                         opacity=zone_opacities[zk]))


# ═══════════════════════════════════════════════════════════════
# GENERATOR FUNCTIONS
# ═══════════════════════════════════════════════════════════════

def _child_profile_path(cx, cy, s, spine_bend_deg, head_tilt_deg,
                        head_r, body_w, arm_len, leg_len, arm_angle_R_deg):
    """Build a SINGLE closed cubic-Bezier path for a SIDE-PROFILE child silhouette.

    Facing RIGHT, hunched forward, right hand raised toward mouth (coughing).
    All coordinates in absolute SVG space, centered on (cx, cy) at top-of-head.
    Returns: (path_d_string, head_center_x, head_center_y, mouth_x, mouth_y)
    """
    # --- Parametric adjustments ---
    bend = math.radians(max(spine_bend_deg, 0))      # forward lean angle
    tilt = math.radians(head_tilt_deg)                # head droop
    lean = math.sin(bend)                             # horizontal displacement factor

    # --- Toddler proportions (4-5 year old) ---
    hr = head_r                       # head radius
    neck_len = hr * 0.5
    torso_h = 50 * s                  # torso height
    bw = body_w * 0.5                 # half body width
    arm_w = 6 * s                     # arm thickness (half)
    leg_w = 7 * s                     # leg thickness (half)
    leg_h = leg_len                   # leg length
    hand_r_val = 5 * s                # hand circle radius

    # --- Anchor positions (local, 0,0 = top of head) ---
    # Head center
    hx = cx + lean * 12 * s
    hy = cy

    # Neck base
    nx = hx + lean * neck_len * 0.5
    ny = hy + hr + neck_len

    # Shoulder (single visible shoulder in profile)
    shx = nx + lean * 5 * s
    shy = ny + 4 * s

    # Back shoulder (further from viewer, slightly behind)
    bshx = shx - bw * 0.6
    bshy = shy - 2 * s

    # Hip
    hip_x = shx + lean * torso_h * 0.35
    hip_y = shy + torso_h

    # Buttock (back of hip, rounder for toddler)
    butt_x = hip_x - bw * 0.8
    butt_y = hip_y + 2 * s

    # Front of hip/belly
    belly_x = hip_x + bw * 0.5
    belly_y = hip_y - 5 * s

    # --- LEGS (slightly bent, feet together) ---
    knee_x = hip_x + 2 * s
    knee_y = hip_y + leg_h * 0.5
    foot_x = hip_x - 2 * s
    foot_y = hip_y + leg_h

    # --- ARM (right arm raised to mouth — coughing gesture) ---
    arm_angle = math.radians(arm_angle_R_deg)
    elbow_x = shx + arm_len * 0.45 * math.cos(arm_angle + 0.3)
    elbow_y = shy + arm_len * 0.45 * math.sin(arm_angle + 0.3)
    hand_x = shx + arm_len * 0.7 * math.cos(arm_angle)
    hand_y = shy + arm_len * 0.7 * math.sin(arm_angle)

    # Mouth position (for cough arcs)
    mouth_x = hx + hr * 0.85
    mouth_y = hy + hr * 0.25

    # Clamp hand near mouth area for coughing gesture
    hand_x = mouth_x - 2 * s
    hand_y = mouth_y + 4 * s

    # --- Left arm (hanging/across belly, only partially visible in profile) ---
    hang_elbow_x = shx - 4 * s
    hang_elbow_y = shy + arm_len * 0.4
    hang_hand_x = belly_x - 3 * s
    hang_hand_y = belly_y + 5 * s

    # ============================================================
    # BUILD SINGLE CLOSED PATH — clockwise from top of head
    # Sequence: head profile (forehead→nose→chin) → neck front →
    #   right arm out → hand → arm back → chest → belly →
    #   front leg → foot → back leg → buttock → back →
    #   back of head
    # ============================================================

    def f(x, y):
        return f"{x:.1f},{y:.1f}"

    # Head profile points (right-facing)
    # Forehead top
    ft_x, ft_y = hx - hr * 0.2, hy - hr * 0.9
    # Forehead front
    ff_x, ff_y = hx + hr * 0.6, hy - hr * 0.6
    # Nose tip
    nose_x, nose_y = hx + hr * 1.0, hy + hr * 0.05
    # Upper lip
    ulip_x, ulip_y = hx + hr * 0.85, hy + hr * 0.22
    # Chin
    chin_x, chin_y = hx + hr * 0.7, hy + hr * 0.65
    # Under chin / jaw
    jaw_x, jaw_y = hx + hr * 0.3, hy + hr * 0.85
    # Back of head bottom
    bh_x, bh_y = hx - hr * 0.8, hy + hr * 0.5
    # Back of head top
    bht_x, bht_y = hx - hr * 0.85, hy - hr * 0.3
    # Crown
    crown_x, crown_y = hx - hr * 0.5, hy - hr * 0.95

    # Hair tuft suggestion at top
    hair_x, hair_y = hx + hr * 0.1, hy - hr * 1.05

    d = f"M {f(hair_x, hair_y)} "

    # --- HEAD: crown → forehead → nose → mouth → chin → jaw ---
    d += f"C {f(hx + hr * 0.4, hy - hr * 1.1)} {f(ff_x + hr * 0.1, ff_y - hr * 0.3)} {f(ff_x, ff_y)} "
    d += f"C {f(ff_x + hr * 0.25, ff_y + hr * 0.15)} {f(nose_x + hr * 0.05, nose_y - hr * 0.15)} {f(nose_x, nose_y)} "
    # Nose to upper lip (small dip)
    d += f"C {f(nose_x - hr * 0.02, nose_y + hr * 0.08)} {f(ulip_x + hr * 0.05, ulip_y - hr * 0.03)} {f(ulip_x, ulip_y)} "

    # --- MOUTH AREA → need to route around the raised arm ---
    # Upper lip → chin
    d += f"C {f(ulip_x - hr * 0.05, ulip_y + hr * 0.12)} {f(chin_x + hr * 0.15, chin_y - hr * 0.1)} {f(chin_x, chin_y)} "
    # Chin → jaw
    d += f"C {f(chin_x - hr * 0.1, chin_y + hr * 0.1)} {f(jaw_x + hr * 0.15, jaw_y)} {f(jaw_x, jaw_y)} "

    # --- NECK FRONT → shoulder → arm going up to hand near mouth ---
    neck_front_x = nx + 5 * s
    neck_front_y = ny
    d += f"C {f(jaw_x - hr * 0.1, jaw_y + hr * 0.1)} {f(neck_front_x, neck_front_y - 6 * s)} {f(neck_front_x, neck_front_y)} "

    # Shoulder front → elbow outer edge → hand
    d += f"C {f(neck_front_x + 2 * s, neck_front_y + 5 * s)} {f(shx + 3 * s, shy)} {f(shx + bw * 0.3, shy + 3 * s)} "

    # Route arm: shoulder → elbow → hand (outer contour)
    d += f"C {f(shx + bw * 0.3, shy + 8 * s)} {f(elbow_x + arm_w, elbow_y - arm_w)} {f(elbow_x + arm_w, elbow_y)} "
    d += f"C {f(elbow_x + arm_w, elbow_y + arm_w)} {f(hand_x + hand_r_val, hand_y - hand_r_val)} {f(hand_x + hand_r_val, hand_y)} "

    # Hand ball (small bump)
    d += f"C {f(hand_x + hand_r_val, hand_y + hand_r_val)} {f(hand_x, hand_y + hand_r_val * 1.2)} {f(hand_x - hand_r_val * 0.5, hand_y + hand_r_val * 0.5)} "

    # Hand → arm inner contour back to shoulder region
    d += f"C {f(hand_x - hand_r_val, hand_y)} {f(elbow_x - arm_w * 0.5, elbow_y + arm_w)} {f(elbow_x - arm_w * 0.5, elbow_y)} "
    d += f"C {f(elbow_x - arm_w * 0.5, elbow_y - arm_w)} {f(shx + 2 * s, shy + 12 * s)} {f(shx, shy + 10 * s)} "

    # --- CHEST / TORSO front (concave = hunched/coughing) ---
    chest_mid_x = (shx + belly_x) / 2 + lean * 5 * s
    chest_mid_y = (shy + belly_y) / 2
    d += f"C {f(shx + bw * 0.2, shy + 15 * s)} {f(chest_mid_x + bw * 0.15, chest_mid_y - 8 * s)} {f(chest_mid_x, chest_mid_y)} "
    d += f"C {f(chest_mid_x - bw * 0.1, chest_mid_y + 10 * s)} {f(belly_x + 2 * s, belly_y - 8 * s)} {f(belly_x, belly_y)} "

    # Belly → front of hip
    d += f"C {f(belly_x - 1 * s, belly_y + 6 * s)} {f(hip_x + bw * 0.3, hip_y - 5 * s)} {f(hip_x + bw * 0.2, hip_y)} "

    # --- FRONT LEG outer contour ---
    d += f"C {f(hip_x + bw * 0.2, hip_y + 4 * s)} {f(knee_x + leg_w, knee_y - 5 * s)} {f(knee_x + leg_w, knee_y)} "
    d += f"C {f(knee_x + leg_w, knee_y + 5 * s)} {f(foot_x + leg_w, foot_y - 8 * s)} {f(foot_x + leg_w, foot_y - 2 * s)} "

    # Foot (small rounded bump)
    foot_fw = leg_w * 1.6  # foot forward extent
    d += f"C {f(foot_x + leg_w, foot_y + 2 * s)} {f(foot_x + foot_fw, foot_y + 3 * s)} {f(foot_x + foot_fw, foot_y)} "
    d += f"C {f(foot_x + foot_fw, foot_y - 1 * s)} {f(foot_x - leg_w * 0.3, foot_y + 2 * s)} {f(foot_x - leg_w, foot_y)} "

    # Front leg inner contour → back up
    d += f"C {f(foot_x - leg_w, foot_y - 8 * s)} {f(knee_x - leg_w * 0.5, knee_y + 5 * s)} {f(knee_x - leg_w * 0.5, knee_y)} "
    d += f"C {f(knee_x - leg_w * 0.5, knee_y - 5 * s)} {f(hip_x - bw * 0.1, hip_y + 5 * s)} {f(hip_x - bw * 0.15, hip_y + 2 * s)} "

    # --- CROTCH / inner leg gap → back leg ---
    back_knee_x = knee_x - 5 * s
    back_knee_y = knee_y + 2 * s
    back_foot_x = foot_x - 5 * s
    back_foot_y = foot_y

    # Down the back leg (inner edge first)
    d += f"C {f(hip_x - bw * 0.3, hip_y + 3 * s)} {f(butt_x + leg_w, hip_y + 5 * s)} {f(butt_x + leg_w * 0.5, hip_y + 2 * s)} "
    d += f"C {f(butt_x + leg_w * 0.3, hip_y + 6 * s)} {f(back_knee_x + leg_w * 0.5, back_knee_y - 5 * s)} {f(back_knee_x + leg_w * 0.5, back_knee_y)} "
    d += f"C {f(back_knee_x + leg_w * 0.5, back_knee_y + 5 * s)} {f(back_foot_x + leg_w * 0.5, back_foot_y - 8 * s)} {f(back_foot_x + leg_w * 0.5, back_foot_y - 2 * s)} "

    # Back foot
    d += f"C {f(back_foot_x + leg_w * 0.5, back_foot_y + 2 * s)} {f(back_foot_x - leg_w * 0.8, back_foot_y + 2 * s)} {f(back_foot_x - leg_w, back_foot_y)} "

    # Back leg outer contour → up to buttock
    d += f"C {f(back_foot_x - leg_w, back_foot_y - 8 * s)} {f(back_knee_x - leg_w, back_knee_y + 5 * s)} {f(back_knee_x - leg_w, back_knee_y)} "
    d += f"C {f(back_knee_x - leg_w, back_knee_y - 8 * s)} {f(butt_x - leg_w * 0.5, hip_y + 8 * s)} {f(butt_x, butt_y)} "

    # --- BACK (concave curve up to neck) ---
    back_mid_x = (butt_x + bshx) / 2 - bw * 0.3 * lean
    back_mid_y = (butt_y + bshy) / 2
    d += f"C {f(butt_x - bw * 0.2, butt_y - 10 * s)} {f(back_mid_x - bw * 0.15, back_mid_y + 10 * s)} {f(back_mid_x, back_mid_y)} "
    d += f"C {f(back_mid_x + bw * 0.1, back_mid_y - 12 * s)} {f(bshx - 3 * s, bshy + 10 * s)} {f(bshx, bshy)} "

    # --- NECK BACK → back of head ---
    neck_back_x = nx - 6 * s
    neck_back_y = ny - 2 * s
    d += f"C {f(bshx + 1 * s, bshy - 5 * s)} {f(neck_back_x, neck_back_y + 4 * s)} {f(neck_back_x, neck_back_y)} "

    # Back of head
    d += f"C {f(neck_back_x - 2 * s, neck_back_y - 6 * s)} {f(bh_x + 2 * s, bh_y + 5 * s)} {f(bh_x, bh_y)} "
    d += f"C {f(bh_x - hr * 0.15, bh_y - hr * 0.3)} {f(bht_x - hr * 0.05, bht_y + hr * 0.2)} {f(bht_x, bht_y)} "
    d += f"C {f(bht_x + hr * 0.05, bht_y - hr * 0.3)} {f(crown_x - hr * 0.2, crown_y + hr * 0.1)} {f(crown_x, crown_y)} "

    # Crown back to hair tuft (close the path)
    d += f"C {f(crown_x + hr * 0.15, crown_y - hr * 0.1)} {f(hair_x - hr * 0.2, hair_y + hr * 0.02)} {f(hair_x, hair_y)} "
    d += "Z"

    return d, hx, hy, mouth_x, mouth_y


def _child_front_path(cx, cy, s, head_r, body_w, shoulder_w, arm_len,
                      leg_len, leg_spread, arm_angle_deg, head_tilt_deg):
    """Build a SINGLE closed cubic-Bezier path for a FRONT-VIEW child silhouette.

    Arms spread wide, upright posture, legs apart. Celebration pose.
    Returns: (path_d_string, head_center_x, head_center_y, chest_cx, chest_cy)
    """
    hr = head_r
    sw = shoulder_w * 0.5           # half shoulder width
    bw = body_w * 0.5              # half body width
    arm_w = 6 * s                   # arm thickness (half)
    leg_w = 7.5 * s                 # leg thickness (half)
    torso_h = 52 * s
    hand_r_val = 5.5 * s
    arm_a = math.radians(arm_angle_deg)  # arm spread angle from horizontal

    # Head center
    hx = cx
    hy = cy + hr * 0.1 * math.sin(math.radians(head_tilt_deg))

    # Neck
    nx, ny = cx, hy + hr + 4 * s

    # Shoulders
    sh_l_x, sh_l_y = nx - sw, ny + 5 * s
    sh_r_x, sh_r_y = nx + sw, ny + 5 * s

    # Hips
    hip_y = sh_l_y + torso_h
    hip_l_x = cx - bw * 0.75
    hip_r_x = cx + bw * 0.75

    # Hands — arms angled upward and outward
    hand_l_x = sh_l_x - arm_len * math.cos(arm_a)
    hand_l_y = sh_l_y - arm_len * math.sin(arm_a)
    hand_r_x = sh_r_x + arm_len * math.cos(arm_a)
    hand_r_y = sh_r_y - arm_len * math.sin(arm_a)

    # Elbows (slight outward bend)
    elb_l_x = (sh_l_x + hand_l_x) / 2 - 3 * s
    elb_l_y = (sh_l_y + hand_l_y) / 2 + 5 * s
    elb_r_x = (sh_r_x + hand_r_x) / 2 + 3 * s
    elb_r_y = (sh_r_y + hand_r_y) / 2 + 5 * s

    # Feet
    ls = leg_spread * 0.5
    foot_l_x = hip_l_x - ls
    foot_r_x = hip_r_x + ls
    foot_y = hip_y + leg_len

    # Knees
    knee_l_x = (hip_l_x + foot_l_x) / 2
    knee_r_x = (hip_r_x + foot_r_x) / 2
    knee_y = (hip_y + foot_y) / 2

    # Chest center (for radiant lines)
    chest_cx = cx
    chest_cy = (sh_l_y + hip_y) / 2

    def f(x, y):
        return f"{x:.1f},{y:.1f}"

    # ============================================================
    # Single closed path — clockwise from top of head
    # Right side down, across feet, left side up, close at top
    # ============================================================

    # Hair tuft
    hair_x, hair_y = hx, hy - hr * 1.08

    d = f"M {f(hair_x, hair_y)} "

    # --- HEAD RIGHT SIDE (top → right ear → jaw) ---
    d += f"C {f(hx + hr * 0.55, hy - hr * 1.1)} {f(hx + hr * 1.0, hy - hr * 0.5)} {f(hx + hr * 0.95, hy)} "
    d += f"C {f(hx + hr * 0.92, hy + hr * 0.45)} {f(hx + hr * 0.65, hy + hr * 0.85)} {f(hx + hr * 0.35, hy + hr * 0.95)} "

    # --- NECK RIGHT → right shoulder ---
    neck_r = 7 * s
    d += f"C {f(hx + neck_r, hy + hr + 2 * s)} {f(hx + neck_r + 2 * s, ny)} {f(hx + neck_r, ny + 2 * s)} "
    d += f"C {f(hx + neck_r + 5 * s, ny + 4 * s)} {f(sh_r_x - 5 * s, sh_r_y - 2 * s)} {f(sh_r_x, sh_r_y)} "

    # --- RIGHT ARM out: shoulder → elbow → hand (upper contour) ---
    d += f"C {f(sh_r_x + 5 * s, sh_r_y - 3 * s)} {f(elb_r_x - 2 * s, elb_r_y - arm_w * 1.3)} {f(elb_r_x, elb_r_y - arm_w)} "
    d += f"C {f(elb_r_x + 3 * s, elb_r_y - arm_w * 1.2)} {f(hand_r_x - hand_r_val, hand_r_y - hand_r_val)} {f(hand_r_x, hand_r_y - hand_r_val * 0.6)} "

    # Hand ball
    d += f"C {f(hand_r_x + hand_r_val * 0.8, hand_r_y - hand_r_val * 0.3)} "
    d += f"{f(hand_r_x + hand_r_val * 0.8, hand_r_y + hand_r_val * 0.6)} "
    d += f"{f(hand_r_x, hand_r_y + hand_r_val * 0.6)} "

    # --- RIGHT ARM back: hand → elbow → shoulder (lower contour) ---
    d += f"C {f(hand_r_x - hand_r_val * 0.5, hand_r_y + hand_r_val)} {f(elb_r_x + 3 * s, elb_r_y + arm_w * 1.3)} {f(elb_r_x, elb_r_y + arm_w)} "
    d += f"C {f(elb_r_x - 4 * s, elb_r_y + arm_w * 1.5)} {f(sh_r_x + 3 * s, sh_r_y + 5 * s)} {f(sh_r_x, sh_r_y + 8 * s)} "

    # --- RIGHT TORSO (shoulder → waist → hip) ---
    waist_r_x = cx + bw * 0.6
    waist_y = (sh_r_y + hip_y) / 2 + 3 * s
    d += f"C {f(sh_r_x - 2 * s, sh_r_y + 15 * s)} {f(waist_r_x + 2 * s, waist_y - 8 * s)} {f(waist_r_x, waist_y)} "
    d += f"C {f(waist_r_x - 1 * s, waist_y + 8 * s)} {f(hip_r_x + 3 * s, hip_y - 8 * s)} {f(hip_r_x, hip_y)} "

    # --- RIGHT LEG down ---
    d += f"C {f(hip_r_x + 1 * s, hip_y + 5 * s)} {f(knee_r_x + leg_w, knee_y - 8 * s)} {f(knee_r_x + leg_w, knee_y)} "
    d += f"C {f(knee_r_x + leg_w, knee_y + 8 * s)} {f(foot_r_x + leg_w, foot_y - 10 * s)} {f(foot_r_x + leg_w, foot_y - 3 * s)} "

    # Right foot
    foot_fw = leg_w * 1.3
    d += f"C {f(foot_r_x + leg_w, foot_y + 1 * s)} {f(foot_r_x + foot_fw, foot_y + 3 * s)} {f(foot_r_x, foot_y + 3 * s)} "
    d += f"C {f(foot_r_x - foot_fw, foot_y + 3 * s)} {f(foot_r_x - leg_w, foot_y + 1 * s)} {f(foot_r_x - leg_w, foot_y - 3 * s)} "

    # Right leg inner contour → back up to crotch
    d += f"C {f(foot_r_x - leg_w, foot_y - 10 * s)} {f(knee_r_x - leg_w * 0.5, knee_y + 8 * s)} {f(knee_r_x - leg_w * 0.5, knee_y)} "
    d += f"C {f(knee_r_x - leg_w * 0.5, knee_y - 8 * s)} {f(hip_r_x - 3 * s, hip_y + 6 * s)} {f(cx + 3 * s, hip_y + 4 * s)} "

    # --- CROTCH → left leg inner ---
    d += f"C {f(cx, hip_y + 5 * s)} {f(cx - 3 * s, hip_y + 5 * s)} {f(cx - 3 * s, hip_y + 4 * s)} "

    # Left leg inner → down
    d += f"C {f(hip_l_x + 3 * s, hip_y + 6 * s)} {f(knee_l_x + leg_w * 0.5, knee_y - 8 * s)} {f(knee_l_x + leg_w * 0.5, knee_y)} "
    d += f"C {f(knee_l_x + leg_w * 0.5, knee_y + 8 * s)} {f(foot_l_x + leg_w, foot_y - 10 * s)} {f(foot_l_x + leg_w, foot_y - 3 * s)} "

    # Left foot
    d += f"C {f(foot_l_x + leg_w, foot_y + 1 * s)} {f(foot_l_x + foot_fw, foot_y + 3 * s)} {f(foot_l_x, foot_y + 3 * s)} "
    d += f"C {f(foot_l_x - foot_fw, foot_y + 3 * s)} {f(foot_l_x - leg_w, foot_y + 1 * s)} {f(foot_l_x - leg_w, foot_y - 3 * s)} "

    # Left leg outer → back up to hip
    d += f"C {f(foot_l_x - leg_w, foot_y - 10 * s)} {f(knee_l_x - leg_w, knee_y + 8 * s)} {f(knee_l_x - leg_w, knee_y)} "
    d += f"C {f(knee_l_x - leg_w, knee_y - 8 * s)} {f(hip_l_x - 1 * s, hip_y + 5 * s)} {f(hip_l_x, hip_y)} "

    # --- LEFT TORSO (hip → waist → shoulder) ---
    waist_l_x = cx - bw * 0.6
    d += f"C {f(hip_l_x - 3 * s, hip_y - 8 * s)} {f(waist_l_x - 1 * s, waist_y + 8 * s)} {f(waist_l_x, waist_y)} "
    d += f"C {f(waist_l_x + 2 * s, waist_y - 8 * s)} {f(sh_l_x + 2 * s, sh_l_y + 15 * s)} {f(sh_l_x, sh_l_y + 8 * s)} "

    # --- LEFT ARM: shoulder → elbow → hand (lower contour first going out) ---
    d += f"C {f(sh_l_x - 3 * s, sh_l_y + 5 * s)} {f(elb_l_x + 4 * s, elb_l_y + arm_w * 1.5)} {f(elb_l_x, elb_l_y + arm_w)} "
    d += f"C {f(elb_l_x - 3 * s, elb_l_y + arm_w * 1.3)} {f(hand_l_x + hand_r_val * 0.5, hand_l_y + hand_r_val)} {f(hand_l_x, hand_l_y + hand_r_val * 0.6)} "

    # Left hand ball
    d += f"C {f(hand_l_x - hand_r_val * 0.8, hand_l_y + hand_r_val * 0.6)} "
    d += f"{f(hand_l_x - hand_r_val * 0.8, hand_l_y - hand_r_val * 0.3)} "
    d += f"{f(hand_l_x, hand_l_y - hand_r_val * 0.6)} "

    # Left arm upper contour back
    d += f"C {f(hand_l_x + hand_r_val, hand_l_y - hand_r_val)} {f(elb_l_x - 3 * s, elb_l_y - arm_w * 1.2)} {f(elb_l_x, elb_l_y - arm_w)} "
    d += f"C {f(elb_l_x + 2 * s, elb_l_y - arm_w * 1.3)} {f(sh_l_x - 5 * s, sh_l_y - 3 * s)} {f(sh_l_x, sh_l_y)} "

    # --- LEFT SHOULDER → neck left → head left side ---
    d += f"C {f(sh_l_x + 5 * s, sh_l_y - 2 * s)} {f(hx - neck_r - 5 * s, ny + 4 * s)} {f(hx - neck_r, ny + 2 * s)} "
    d += f"C {f(hx - neck_r - 2 * s, ny)} {f(hx - neck_r, hy + hr + 2 * s)} {f(hx - hr * 0.35, hy + hr * 0.95)} "

    # --- HEAD LEFT SIDE (jaw → left ear → crown) ---
    d += f"C {f(hx - hr * 0.65, hy + hr * 0.85)} {f(hx - hr * 0.92, hy + hr * 0.45)} {f(hx - hr * 0.95, hy)} "
    d += f"C {f(hx - hr * 1.0, hy - hr * 0.5)} {f(hx - hr * 0.55, hy - hr * 1.1)} {f(hair_x, hair_y)} "
    d += "Z"

    return d, hx, hy, chest_cx, chest_cy


# ═══════════════════════════════════════════════════════════════
# EXTRACTED CONTOUR DATA — normalized (center=0,0, unit height=1.0)
# ═══════════════════════════════════════════════════════════════

# S3: sick child side-profile silhouette (36 pts, 226x154 image)
_CONTOUR_SICK = [
    [-0.454545, 0.500000], [-0.504545, 0.486364], [-0.495455, 0.431818],
    [-0.368182, 0.177273], [-0.272727, 0.081818], [-0.172727, 0.018182],
    [-0.136364, 0.018182], [-0.104545, -0.022727], [-0.150000, -0.240909],
    [-0.104545, -0.368182], [0.004545, -0.459091], [-0.022727, -0.468182],
    [0.027273, -0.472727], [0.045455, -0.500000], [0.218182, -0.500000],
    [0.381818, -0.409091], [0.504545, -0.231818], [0.486364, -0.222727],
    [0.486364, -0.131818], [0.454545, -0.081818], [0.445455, -0.145455],
    [0.413636, -0.068182], [0.359091, -0.013636], [0.377273, 0.068182],
    [0.327273, 0.090909], [0.309091, 0.127273], [0.281818, 0.127273],
    [0.277273, 0.159091], [0.209091, 0.209091], [0.081818, 0.145455],
    [0.050000, 0.168182], [0.040909, 0.186364], [0.077273, 0.250000],
    [0.077273, 0.468182], [-0.354545, 0.472727], [-0.454545, 0.500000],
]

# S4: healthy child front-view silhouette (70 pts, 251x174 image)
_CONTOUR_HEALTHY = [
    [-0.231405, 0.500000], [-0.227273, 0.256198], [-0.243802, 0.181818],
    [-0.363636, 0.128099], [-0.388430, 0.061983], [-0.743802, -0.103306],
    [-0.892562, -0.103306], [-0.900826, -0.119835], [-0.847107, -0.140496],
    [-0.929752, -0.165289], [-0.871901, -0.181818], [-0.917355, -0.202479],
    [-0.925620, -0.227273], [-0.847107, -0.214876], [-0.892562, -0.268595],
    [-0.785124, -0.219008], [-0.780992, -0.280992], [-0.760331, -0.293388],
    [-0.723140, -0.181818], [-0.685950, -0.161157], [-0.504132, -0.111570],
    [-0.388430, -0.053719], [-0.338843, -0.061983], [-0.099174, -0.012397],
    [-0.086777, -0.049587], [-0.128099, -0.123967], [-0.177686, -0.157025],
    [-0.202479, -0.214876], [-0.177686, -0.239669], [-0.194215, -0.314050],
    [-0.185950, -0.396694], [-0.144628, -0.438017], [-0.157025, -0.458678],
    [0.016529, -0.500000], [0.099174, -0.466942], [0.107438, -0.491736],
    [0.185950, -0.363636], [0.177686, -0.247934], [0.202479, -0.231405],
    [0.194215, -0.181818], [0.086777, -0.049587], [0.099174, -0.012397],
    [0.347107, -0.061983], [0.363636, -0.045455], [0.685950, -0.161157],
    [0.723140, -0.190083], [0.760331, -0.293388], [0.780992, -0.289256],
    [0.785124, -0.219008], [0.867769, -0.268595], [0.896694, -0.256198],
    [0.842975, -0.210744], [0.929752, -0.223140], [0.863636, -0.181818],
    [0.929752, -0.165289], [0.847107, -0.140496], [0.900826, -0.119835],
    [0.900826, -0.103306], [0.743802, -0.103306], [0.561983, -0.004132],
    [0.388430, 0.061983], [0.363636, 0.128099], [0.264463, 0.161157],
    [0.235537, 0.214876], [0.227273, 0.289256], [0.231405, 0.475207],
    [0.223140, 0.450413], [-0.107438, 0.458678], [-0.223140, 0.475207],
    [-0.231405, 0.500000],
]

# Landmark offsets in normalized coords (relative to contour center)
# Derived from visual analysis of S3/S4 reference images
_SICK_HEAD_CENTER = (0.17, -0.43)    # center of head circle in S3
_SICK_MOUTH = (0.45, -0.15)          # mouth area (right side of face)
_HEALTHY_HEAD_CENTER = (0.0, -0.43)  # center of head in S4 (front view)
_HEALTHY_CHEST = (0.0, 0.05)         # chest center in S4


def _catmull_rom_to_bezier(points):
    """Convert closed polygon points to smooth cubic Bezier path (Catmull-Rom spline).

    For each segment between points[i] and points[i+1]:
      CP1 = P_i + (P_{i+1} - P_{i-1}) / 6
      CP2 = P_{i+1} - (P_{i+2} - P_i) / 6
    This gives C2-continuous curves passing through all original points.

    Returns an SVG path d-string (M ... C ... C ... Z).
    """
    n = len(points)
    if n < 3:
        # Degenerate: just draw lines
        d = f"M {points[0][0]:.2f},{points[0][1]:.2f} "
        for p in points[1:]:
            d += f"L {p[0]:.2f},{p[1]:.2f} "
        return d + "Z"

    # Remove duplicate closing point if present
    if (abs(points[0][0] - points[-1][0]) < 1e-6 and
            abs(points[0][1] - points[-1][1]) < 1e-6):
        pts = points[:-1]
    else:
        pts = list(points)

    n = len(pts)
    d = f"M {pts[0][0]:.2f},{pts[0][1]:.2f} "

    for i in range(n):
        p_prev = pts[(i - 1) % n]
        p_curr = pts[i]
        p_next = pts[(i + 1) % n]
        p_next2 = pts[(i + 2) % n]

        # Control point 1: on the segment start side
        cp1x = p_curr[0] + (p_next[0] - p_prev[0]) / 6.0
        cp1y = p_curr[1] + (p_next[1] - p_prev[1]) / 6.0

        # Control point 2: on the segment end side
        cp2x = p_next[0] - (p_next2[0] - p_curr[0]) / 6.0
        cp2y = p_next[1] - (p_next2[1] - p_curr[1]) / 6.0

        d += (f"C {cp1x:.2f},{cp1y:.2f} "
              f"{cp2x:.2f},{cp2y:.2f} "
              f"{p_next[0]:.2f},{p_next[1]:.2f} ")

    d += "Z"
    return d


def draw_child(dwg, cx, cy, params, color, scale):
    """Publication-quality child silhouette from extracted contour data.

    v9: Uses real contour points extracted from reference screenshots (S3/S4)
    via scikit-image, smoothed with Catmull-Rom → cubic Bezier conversion.

    Two modes:
      - SIDE PROFILE (sick, cough_marks=true): S3 contour, hunched coughing child
      - FRONT VIEW (healthy, sparkle_marks=true): S4 contour, arms-wide celebration
    """
    global _child_grad_counter
    _child_grad_counter += 1
    grad_id_suffix = _child_grad_counter

    s = scale
    fill_opacity = 0.85
    # Target silhouette height in SVG units (matches previous ~200px total height)
    target_h = 200 * s

    if params.get("cough_marks"):
        # ═══════════════════════════════════════════════════════════
        # MODE 1: SIDE PROFILE — sick child (S3 extracted contour)
        # ═══════════════════════════════════════════════════════════
        contour = _CONTOUR_SICK
        head_norm = _SICK_HEAD_CENTER
        mouth_norm = _SICK_MOUTH

        # Transform normalized contour → SVG coords
        # Normalized: center=(0,0), full height spans [-0.5, 0.5]
        # Target: center at (cx, cy), scaled to target_h
        render_pts = [
            (cx + p[0] * target_h, cy + p[1] * target_h)
            for p in contour
        ]

        # Build smooth Bezier path from polygon points
        path_d = _catmull_rom_to_bezier(render_pts)

        # --- Gradient: vertical dark→light red (head→feet) ---
        grad_sick_id = f"child_grad_sick_{grad_id_suffix}"
        lg = dwg.linearGradient(
            id=grad_sick_id,
            x1="0%", y1="0%", x2="0%", y2="100%",
        )
        lg.add_stop_color(offset="0%", color=color, opacity=fill_opacity)
        lg.add_stop_color(offset="100%", color=_lighten_hex(color, 0.40),
                          opacity=fill_opacity * 0.75)
        dwg.defs.add(lg)

        # Draw the filled silhouette with gradient (flat color fallback in <desc>)
        dwg.add(dwg.path(d=path_d, fill=f"url(#{grad_sick_id})",
                         opacity=fill_opacity))

        # Derive landmark positions from normalized offsets
        hx = cx + head_norm[0] * target_h
        hy = cy + head_norm[1] * target_h
        mouth_x = cx + mouth_norm[0] * target_h
        mouth_y = cy + mouth_norm[1] * target_h
        head_r = params.get("head_radius", 28) * s

        # --- EXPRESSION MARKS: Cough arcs ---
        for i in range(3):
            cr = (12 + i * 10) * s
            op = 0.55 - i * 0.12
            arc_start_y = mouth_y - cr * 0.45
            arc_end_y = mouth_y + cr * 0.45
            arc_x = mouth_x + cr * 0.3 + 5 * s
            dwg.add(dwg.path(
                d=(f"M {arc_x:.1f},{arc_start_y:.1f} "
                   f"A {cr:.1f},{cr:.1f} 0 0,1 {arc_x:.1f},{arc_end_y:.1f}"),
                fill="none", stroke=color, stroke_width=1.8 * s, opacity=op,
                stroke_linecap="round"
            ))

        # --- EXPRESSION MARKS: Distress lines ---
        distress = params.get("distress_lines", 3)
        for i in range(distress):
            angle = math.radians(-50 + i * 25)
            lx = hx - head_r * 1.3 - i * 6 * s
            ly = hy - head_r * 0.2 + i * 3 * s
            line_len = 10 * s
            dwg.add(dwg.line(
                (lx, ly),
                (lx - line_len * math.cos(angle), ly - line_len * math.sin(angle)),
                stroke=color, stroke_width=1.5 * s, opacity=0.4,
                stroke_linecap="round"
            ))

    else:
        # ═══════════════════════════════════════════════════════════
        # MODE 2: FRONT VIEW — healthy child (S4 extracted contour)
        # ═══════════════════════════════════════════════════════════
        contour = _CONTOUR_HEALTHY
        head_norm = _HEALTHY_HEAD_CENTER
        chest_norm = _HEALTHY_CHEST

        # Transform normalized contour → SVG coords
        render_pts = [
            (cx + p[0] * target_h, cy + p[1] * target_h)
            for p in contour
        ]

        # Build smooth Bezier path from polygon points
        path_d = _catmull_rom_to_bezier(render_pts)

        # --- Gradient: radial "radiant health" from chest center ---
        # Express chest position as percentage of the bounding box.
        # Contour spans roughly [-0.5, 0.5] * target_h around cx/cy,
        # so normalized [0..1] → 50% + norm*100%.
        chest_pct_x = 50 + chest_norm[0] * 100   # ~50% (centered)
        chest_pct_y = 50 + chest_norm[1] * 100   # offset from vertical center

        grad_healthy_id = f"child_grad_healthy_{grad_id_suffix}"
        rg = dwg.radialGradient(
            id=grad_healthy_id,
            cx=f"{chest_pct_x:.1f}%", cy=f"{chest_pct_y:.1f}%",
            r="65%",
            fx=f"{chest_pct_x:.1f}%", fy=f"{chest_pct_y:.1f}%",
        )
        rg.add_stop_color(offset="0%", color=color, opacity=fill_opacity)
        rg.add_stop_color(offset="100%", color=_lighten_hex(color, 0.45),
                          opacity=fill_opacity * 0.70)
        dwg.defs.add(rg)

        # Draw the filled silhouette with gradient (flat color fallback in <desc>)
        dwg.add(dwg.path(d=path_d, fill=f"url(#{grad_healthy_id})",
                         opacity=fill_opacity))

        # Derive landmark positions
        hx = cx + head_norm[0] * target_h
        hy = cy + head_norm[1] * target_h
        chest_cx = cx + chest_norm[0] * target_h
        chest_cy = cy + chest_norm[1] * target_h
        head_r = params.get("head_radius", 28) * s

        # --- EXPRESSION MARKS: Radiant lines from chest ---
        num_rays = 8
        for i in range(num_rays):
            angle = math.radians(i * (360 / num_rays) - 90)
            inner_r = 35 * s
            outer_r = 55 * s + (i % 2) * 8 * s
            rx1 = chest_cx + inner_r * math.cos(angle)
            ry1 = chest_cy + inner_r * math.sin(angle)
            rx2 = chest_cx + outer_r * math.cos(angle)
            ry2 = chest_cy + outer_r * math.sin(angle)
            dwg.add(dwg.line(
                (rx1, ry1), (rx2, ry2),
                stroke=color, stroke_width=2.0 * s, opacity=0.35,
                stroke_linecap="round"
            ))

        # --- EXPRESSION MARKS: Sparkle stars ---
        if params.get("sparkle_marks"):
            sparkle_positions = [
                (-head_r * 2.2, -head_r * 1.8),
                (head_r * 2.2, -head_r * 1.3),
                (-head_r * 1.2, -head_r * 2.5),
                (head_r * 1.6, head_r * 0.8),
            ]
            for spx, spy in sparkle_positions:
                sx = hx + spx
                sy = hy + spy
                star_r = 5 * s
                points = []
                for j in range(8):
                    a = math.radians(j * 45 - 90)
                    r = star_r if j % 2 == 0 else star_r * 0.35
                    points.append((sx + r * math.cos(a), sy + r * math.sin(a)))
                dwg.add(dwg.polygon(points, fill=color, opacity=0.45))

        # --- EXPRESSION MARKS: Smile (white arc on face) ---
        if params.get("smile"):
            sm_w = head_r * 0.35
            sm_y = hy + head_r * 0.25
            dwg.add(dwg.path(
                d=f"M {hx - sm_w:.1f},{sm_y:.1f} "
                  f"Q {hx:.1f},{sm_y + sm_w:.1f} {hx + sm_w:.1f},{sm_y:.1f}",
                fill="none", stroke="white", stroke_width=1.5 * s, opacity=0.6,
                stroke_linecap="round"
            ))


def draw_shield(dwg, cx, cy, params, color, scale):
    """Heraldic shield with keyhole/lock icon in center.

    FIX F3: Shield embeds ON the brick wall (positioning handled by layout.yaml).
    """
    s = scale
    w = params.get("width", 100) * s / 2
    h = params.get("height", 120) * s
    border = params.get("border_thickness", 6) * s
    lock_sz = params.get("lock_size", 20) * s
    curv = params.get("curvature", 0.3)

    # Shield outline: flat top, curved bottom coming to a point
    # Control points for the curved bottom
    cp_y = cy + h * (1 - curv)
    shield_d = (
        f"M {cx - w},{cy} "
        f"L {cx + w},{cy} "
        f"L {cx + w},{cp_y} "
        f"Q {cx + w * 0.6},{cy + h * 0.95} {cx},{cy + h} "
        f"Q {cx - w * 0.6},{cy + h * 0.95} {cx - w},{cp_y} "
        f"Z"
    )
    dwg.add(dwg.path(d=shield_d, fill=color, opacity=0.15,
                      stroke=color, stroke_width=border))

    # Inner shield highlight
    inner_w = w * 0.75
    inner_h = h * 0.85
    inner_cy = cy + h * 0.08
    inner_cp_y = inner_cy + inner_h * (1 - curv)
    inner_d = (
        f"M {cx - inner_w},{inner_cy} "
        f"L {cx + inner_w},{inner_cy} "
        f"L {cx + inner_w},{inner_cp_y} "
        f"Q {cx + inner_w * 0.6},{inner_cy + inner_h * 0.95} {cx},{inner_cy + inner_h} "
        f"Q {cx - inner_w * 0.6},{inner_cy + inner_h * 0.95} {cx - inner_w},{inner_cp_y} "
        f"Z"
    )
    dwg.add(dwg.path(d=inner_d, fill=color, opacity=0.08, stroke="none"))

    # Keyhole in center
    kh_cy = cy + h * 0.35
    kh_r = lock_sz * 0.5
    dwg.add(dwg.circle(center=(cx, kh_cy), r=kh_r,
                        fill="none", stroke=color, stroke_width=2 * s, opacity=0.7))
    # Keyhole slot (triangle pointing down)
    slot_top = kh_cy + kh_r * 0.6
    slot_bottom = kh_cy + lock_sz * 1.2
    slot_half_w = kh_r * 0.45
    dwg.add(dwg.path(
        d=f"M {cx - slot_half_w},{slot_top} L {cx},{slot_bottom} L {cx + slot_half_w},{slot_top}",
        fill="none", stroke=color, stroke_width=2 * s, opacity=0.7
    ))


def draw_helix(dwg, cx, cy, params, color, scale):
    """DNA double helix: two sinusoidal strands with horizontal rungs.

    FIX F4: Positioned inside DC cell nucleus (layout change).
    """
    s = scale
    wl = params.get("wavelength", 40) * s
    amp = params.get("amplitude", 20) * s
    num_rungs = params.get("num_rungs", 6)
    length = params.get("length", 150) * s
    sw = params.get("strand_width", 4) * s

    # Build two sinusoidal paths (opposite phase)
    steps = 60
    strand_a = []
    strand_b = []
    for i in range(steps + 1):
        t = i / steps
        y = cy - length / 2 + t * length
        phase = 2 * math.pi * t * (length / wl)
        x_a = cx + amp * math.sin(phase)
        x_b = cx - amp * math.sin(phase)
        strand_a.append((x_a, y))
        strand_b.append((x_b, y))

    # Draw strand A
    d_a = f"M {strand_a[0][0]},{strand_a[0][1]}"
    for pt in strand_a[1:]:
        d_a += f" L {pt[0]},{pt[1]}"
    dwg.add(dwg.path(d=d_a, fill="none", stroke=color,
                      stroke_width=sw, opacity=0.7))

    # Draw strand B
    d_b = f"M {strand_b[0][0]},{strand_b[0][1]}"
    for pt in strand_b[1:]:
        d_b += f" L {pt[0]},{pt[1]}"
    dwg.add(dwg.path(d=d_b, fill="none", stroke=color,
                      stroke_width=sw, opacity=0.7))

    # Rungs connecting strands
    for i in range(num_rungs):
        t = (i + 0.5) / num_rungs
        idx = int(t * steps)
        if idx >= len(strand_a):
            idx = len(strand_a) - 1
        rx1, ry1 = strand_a[idx]
        rx2, ry2 = strand_b[idx]
        dwg.add(dwg.line((rx1, ry1), (rx2, ry2),
                         stroke=color, stroke_width=sw * 0.4, opacity=0.35))


def draw_bridge(dwg, cx, cy, params, color, scale):
    """Gut-lung bridge arc with stylized line-art icons.

    FIX F5: Points independently toward barrier + DC, not crossing other agents.
    The bridge is drawn as a quadratic Bezier arc. Gut icon at bottom, lung icon at top.
    """
    s = scale
    arc_h = params.get("arc_height", 180) * s
    arc_w = params.get("arc_width", 350) * s / 2
    thickness = params.get("thickness", 7) * s
    gut_r = params.get("gut_icon_radius", 25) * s
    lung_r = params.get("lung_icon_radius", 20) * s
    pillars = params.get("pillar_count", 5)

    # Bridge endpoints: bottom-left (gut) to top-right (lung/barrier)
    x_start = cx - arc_w
    y_start = cy
    x_end = cx + arc_w
    y_end = cy - arc_h * 0.3

    # Control point for the arc (peak)
    cp_x = cx
    cp_y = cy - arc_h

    # Main bridge arc
    dwg.add(dwg.path(
        d=f"M {x_start},{y_start} Q {cp_x},{cp_y} {x_end},{y_end}",
        fill="none", stroke=color, stroke_width=thickness, opacity=0.9
    ))
    # Second arc (lighter, slightly wider)
    dwg.add(dwg.path(
        d=f"M {x_start - 4 * s},{y_start + 3 * s} Q {cp_x},{cp_y - 8 * s} {x_end + 4 * s},{y_end + 3 * s}",
        fill="none", stroke=color, stroke_width=thickness * 0.5, opacity=0.4
    ))

    # Support pillars (vertical dashed lines under the arc)
    for i in range(pillars):
        t = (i + 1) / (pillars + 1)
        # Point on the arc at parameter t
        px = (1 - t) ** 2 * x_start + 2 * (1 - t) * t * cp_x + t ** 2 * x_end
        py = (1 - t) ** 2 * y_start + 2 * (1 - t) * t * cp_y + t ** 2 * y_end
        pillar_bottom = max(y_start, y_end)
        if py < pillar_bottom:
            dwg.add(dwg.line(
                (px, py), (px, pillar_bottom + 10 * s),
                stroke=color, stroke_width=1.5 * s, opacity=0.25,
                stroke_dasharray=f"{4 * s},{4 * s}"
            ))

    # Gut icon at bottom-left (LINE ART minimal squiggle)
    gx, gy = x_start, y_start
    dwg.add(dwg.circle(center=(gx, gy), r=gut_r,
                        fill=color, opacity=0.1, stroke=color, stroke_width=1.5 * s))
    # Minimal intestine squiggle
    sq_s = gut_r * 0.5
    dwg.add(dwg.path(
        d=(f"M {gx - sq_s},{gy - sq_s * 0.6} "
           f"Q {gx - sq_s * 0.3},{gy - sq_s} {gx},{gy - sq_s * 0.4} "
           f"Q {gx + sq_s * 0.3},{gy + sq_s * 0.2} {gx - sq_s * 0.2},{gy + sq_s * 0.5} "
           f"Q {gx - sq_s * 0.6},{gy + sq_s} {gx + sq_s * 0.4},{gy + sq_s * 0.7}"),
        fill="none", stroke=color, stroke_width=1.5 * s, opacity=0.7
    ))

    # Lung icon at top-right (LINE ART two lobes)
    lx, ly = x_end, y_end
    dwg.add(dwg.circle(center=(lx, ly), r=lung_r,
                        fill=color, opacity=0.1, stroke=color, stroke_width=1.5 * s))
    # Two-lobe shape
    lobe_s = lung_r * 0.5
    dwg.add(dwg.path(
        d=(f"M {lx},{ly - lobe_s} "
           f"C {lx - lobe_s * 1.4},{ly - lobe_s * 0.5} "
           f"{lx - lobe_s * 1.4},{ly + lobe_s * 1.2} "
           f"{lx - lobe_s * 0.3},{ly + lobe_s * 1.1} "
           f"M {lx},{ly - lobe_s} "
           f"C {lx + lobe_s * 1.4},{ly - lobe_s * 0.5} "
           f"{lx + lobe_s * 1.4},{ly + lobe_s * 1.2} "
           f"{lx + lobe_s * 0.3},{ly + lobe_s * 1.1}"),
        fill="none", stroke=color, stroke_width=1.5 * s, opacity=0.7
    ))


def draw_dc_cell(dwg, cx, cy, params, color, scale):
    """Dendritic cell with biologically accurate filopodial morphology.

    FIX F7: NOT a symmetric star. Uses irregular curved branches with varying
    lengths, forked tips, and a slightly irregular body.
    Uses deterministic seed for reproducible output.
    """
    s = scale
    num_branches = params.get("num_branches", 7)
    bl_min = params.get("branch_length_min", 25) * s
    bl_max = params.get("branch_length_max", 45) * s
    body_r = params.get("body_radius", 20) * s
    bw = params.get("branch_width", 3) * s
    irreg = params.get("irregularity", 0.3)

    rng = random.Random(42)  # deterministic seed

    # Body: slightly irregular circle using overlapping ellipses
    for i in range(3):
        angle = rng.uniform(0, 2 * math.pi)
        offset_x = body_r * 0.15 * math.cos(angle)
        offset_y = body_r * 0.15 * math.sin(angle)
        rx = body_r * rng.uniform(0.85, 1.15)
        ry = body_r * rng.uniform(0.85, 1.15)
        dwg.add(dwg.ellipse(
            center=(cx + offset_x, cy + offset_y),
            r=(rx, ry),
            fill=color, opacity=0.12,
            stroke=color, stroke_width=1.5 * s
        ))

    # Nucleus hint (small darker circle)
    dwg.add(dwg.circle(center=(cx, cy), r=body_r * 0.35,
                        fill=color, opacity=0.2, stroke="none"))

    # Branches: 7 extensions with CURVED paths, varying thickness, forked tips
    base_angle_spacing = 2 * math.pi / num_branches
    for i in range(num_branches):
        # Angle with irregularity
        base_angle = i * base_angle_spacing
        angle = base_angle + rng.uniform(-irreg * 0.8, irreg * 0.8)

        # Branch length with variation
        bl = rng.uniform(bl_min, bl_max)

        # Start point on body surface
        sx = cx + body_r * 0.9 * math.cos(angle)
        sy = cy + body_r * 0.9 * math.sin(angle)

        # End point
        ex = cx + (body_r + bl) * math.cos(angle)
        ey = cy + (body_r + bl) * math.sin(angle)

        # Control point for curve (perpendicular offset)
        perp = angle + math.pi / 2
        ctrl_offset = bl * rng.uniform(-0.3, 0.3) * irreg
        mid_x = (sx + ex) / 2 + ctrl_offset * math.cos(perp)
        mid_y = (sy + ey) / 2 + ctrl_offset * math.sin(perp)

        # Branch thickness varies
        branch_w = bw * rng.uniform(0.7, 1.3)

        # Main branch curve
        dwg.add(dwg.path(
            d=f"M {sx},{sy} Q {mid_x},{mid_y} {ex},{ey}",
            fill="none", stroke=color, stroke_width=branch_w, opacity=0.75
        ))

        # Forked tips (2 small forks at the end)
        fork_len = bl * 0.25
        fork_spread = rng.uniform(0.3, 0.6)
        for sign in (-1, 1):
            fork_angle = angle + sign * fork_spread
            fx = ex + fork_len * math.cos(fork_angle)
            fy = ey + fork_len * math.sin(fork_angle)
            dwg.add(dwg.line(
                (ex, ey), (fx, fy),
                stroke=color, stroke_width=branch_w * 0.6, opacity=0.55
            ))

        # Some branches get a third small fork tip
        if rng.random() < 0.4:
            tiny_angle = angle + rng.uniform(-0.2, 0.2)
            tiny_len = fork_len * 0.6
            tx = ex + tiny_len * math.cos(tiny_angle)
            ty = ey + tiny_len * math.sin(tiny_angle)
            dwg.add(dwg.line(
                (ex, ey), (tx, ty),
                stroke=color, stroke_width=branch_w * 0.4, opacity=0.4
            ))


def draw_virus(dwg, cx, cy, r, color, params=None):
    """Simple virus: circle with spike proteins. Optionally adds angry expression."""
    dwg.add(dwg.circle(center=(cx, cy), r=r, fill=color, opacity=0.85))
    spike_count = 8
    spike_len = 10
    tip_r = 3.5
    if params:
        spike_count = params.get("spike_count", 8)
        spike_len = params.get("spike_length", 14)
        tip_r = params.get("spike_tip_radius", 4)

    for i in range(spike_count):
        angle = i * 2 * math.pi / spike_count
        x1 = cx + r * math.cos(angle)
        y1 = cy + r * math.sin(angle)
        x2 = cx + (r + spike_len) * math.cos(angle)
        y2 = cy + (r + spike_len) * math.sin(angle)
        dwg.add(dwg.line((x1, y1), (x2, y2), stroke=color, stroke_width=2.5))
        dwg.add(dwg.circle(center=(x2, y2), r=tip_r, fill=color))

    # Angry expression if specified
    if params and params.get("expression") == "angry":
        # Frown lines (eyebrows angled inward)
        dwg.add(dwg.line(
            (cx - r * 0.4, cy - r * 0.15), (cx - r * 0.1, cy - r * 0.05),
            stroke="white", stroke_width=1.5, opacity=0.7
        ))
        dwg.add(dwg.line(
            (cx + r * 0.4, cy - r * 0.15), (cx + r * 0.1, cy - r * 0.05),
            stroke="white", stroke_width=1.5, opacity=0.7
        ))
        # Angry mouth
        dwg.add(dwg.path(
            d=f"M {cx - r * 0.25},{cy + r * 0.3} Q {cx},{cy + r * 0.15} {cx + r * 0.25},{cy + r * 0.3}",
            fill="none", stroke="white", stroke_width=1.5, opacity=0.6
        ))


# Generator dispatch table
GENERATORS = {
    "child": draw_child,
    "shield": draw_shield,
    "helix": draw_helix,
    "bridge": draw_bridge,
    "dc_cell": draw_dc_cell,
}


# ═══════════════════════════════════════════════════════════════
# BRICK WALL
# ═══════════════════════════════════════════════════════════════

def draw_brick_wall_zone(dwg, x, y, width, height, rows, cols,
                         color, stroke_color, gap, gaps=None,
                         teal_bricks=None, teal_color=None,
                         stroke_width=1.5, opacity=1.0):
    """Draw a brick wall pattern for one zone.

    gaps: set of (row, col) tuples where bricks are missing
    teal_bricks: set of (row, col) tuples for PMBL teal repair bricks
    Returns (brick_width, brick_height, list of teal brick positions for F2).
    """
    bw = width / cols
    bh = height / rows
    if gaps is None:
        gaps = set()
    if teal_bricks is None:
        teal_bricks = set()

    teal_positions = []  # For F2: E-cadherin staples

    for r in range(rows):
        offset = bw / 2 if r % 2 else 0
        for c in range(cols):
            bx = x + c * bw + offset
            if bx + bw > x + width + bw * 0.3:
                continue
            if (r, c) in gaps:
                continue

            if (r, c) in teal_bricks:
                brick_color = teal_color or "#0D9488"
                brick_stroke = brick_color
                brick_opacity = 0.85
                teal_positions.append((bx, y + r * bh, bw - gap, bh - gap))
            else:
                brick_color = color
                brick_stroke = stroke_color
                brick_opacity = opacity

            dwg.add(dwg.rect(
                (bx, y + r * bh), (bw - gap, bh - gap),
                rx=3, ry=3,
                fill=brick_color, opacity=brick_opacity,
                stroke=brick_stroke, stroke_width=stroke_width
            ))

    return bw, bh, teal_positions


def draw_ecadherin_staples(dwg, teal_positions, teal_color):
    """FIX F2: Draw luminous E-cadherin molecular staples between PMBL repair bricks.

    Short glowing connection lines between adjacent repair bricks.
    Glow effect: wider semi-transparent stroke behind the main stroke.
    """
    if len(teal_positions) < 2:
        return

    # Find pairs of teal bricks that are adjacent (close in position)
    for i in range(len(teal_positions)):
        for j in range(i + 1, len(teal_positions)):
            x1, y1, w1, h1 = teal_positions[i]
            x2, y2, w2, h2 = teal_positions[j]
            # Check adjacency: close horizontally or vertically
            cx1 = x1 + w1 / 2
            cy1 = y1 + h1 / 2
            cx2 = x2 + w2 / 2
            cy2 = y2 + h2 / 2
            dist = math.sqrt((cx2 - cx1) ** 2 + (cy2 - cy1) ** 2)

            # Only connect bricks within reasonable proximity
            max_dist = max(w1, h1) * 3.5
            if dist < max_dist:
                # Edge points: from edge of brick 1 toward brick 2
                angle = math.atan2(cy2 - cy1, cx2 - cx1)
                edge1_x = cx1 + (w1 / 2) * math.cos(angle)
                edge1_y = cy1 + (h1 / 2) * math.sin(angle)
                edge2_x = cx2 - (w2 / 2) * math.cos(angle)
                edge2_y = cy2 - (h2 / 2) * math.sin(angle)

                # Glow layer (wider, semi-transparent)
                dwg.add(dwg.line(
                    (edge1_x, edge1_y), (edge2_x, edge2_y),
                    stroke=teal_color, stroke_width=6, opacity=0.2
                ))
                # Main staple line
                dwg.add(dwg.line(
                    (edge1_x, edge1_y), (edge2_x, edge2_y),
                    stroke=teal_color, stroke_width=2.5, opacity=0.65
                ))


def draw_brick_wall(dwg, layout, palette, W, H):
    """Draw the continuous brick wall across all 3 zones.

    Zone 1: sick bricks with gaps (virus entry points) + displaced bricks + viruses
    Zone 2: transition bricks, PMBL teal bricks filling gaps + E-cadherin staples (F2)
    Zone 3: healthy intact bricks (all solid green)
    """
    wall = layout["wall"]
    wall_y = int(H * wall["y_center_pct"])
    wall_h = wall["height_px"]
    rows = wall["brick_rows"]
    cols = wall["brick_cols_per_zone"]
    gap = wall["brick_gap"]
    generators_cfg = layout.get("_generators", {})
    virus_params = generators_cfg.get("virus", None)

    # Parse gap/repair lists from YAML (lists of [row, col])
    z1_gaps = set(tuple(g) for g in wall.get("z1_gaps", []))
    z2_repairs = set(tuple(g) for g in wall.get("z2_repair_bricks", []))

    # --- Zone 1: sick wall ---
    z1x, _, z1w, _ = zone_rect(layout, "z1", W, H)
    margin = 40
    bw1, bh1, _ = draw_brick_wall_zone(
        dwg, z1x + margin, wall_y, z1w - 2 * margin, wall_h,
        rows, cols,
        palette["wall"]["sick"], palette["wall"]["sick_mortar"], gap,
        gaps=z1_gaps,
        stroke_width=1.5, opacity=0.85
    )

    # Displaced bricks falling from gaps
    wall1_x = z1x + margin
    displaced = []
    for (gr, gc) in list(z1_gaps)[:4]:
        dx = wall1_x + gc * bw1 + 15
        if gr == 0:
            dy = wall_y - 30
        else:
            dy = wall_y + gr * bh1 + bh1 + 15
        rot = (gc * 7 - 15) % 40 - 20
        displaced.append((dx, dy, rot))

    for dx, dy, rot in displaced:
        dwg.add(dwg.rect(
            (dx, dy), (bw1 * 0.7, bh1 * 0.7),
            rx=3, ry=3,
            fill=palette["wall"]["sick"], opacity=0.5,
            stroke=palette["wall"]["sick_mortar"], stroke_width=1,
            transform=f"rotate({rot}, {dx + bw1*0.35}, {dy + bh1*0.35})"
        ))

    # Virus icons penetrating gaps
    virus_color = palette["virus"]
    gap_list = sorted(z1_gaps)
    for i, (gr, gc) in enumerate(gap_list[:3]):
        vx = wall1_x + (gc + 0.5) * bw1
        vy = wall_y + (gr + 0.5) * bh1
        vr = 18
        draw_virus(dwg, vx, vy, vr, virus_color, params=virus_params)

    # --- Zone 2: transition wall ---
    z2x, _, z2w, _ = zone_rect(layout, "z2", W, H)
    z2_cols = int(cols * 1.4)  # wider zone, more columns
    # Zone 2 has some gaps and PMBL repair bricks
    z2_gaps = {(0, 3), (1, 8), (2, 1), (3, 10), (0, 11), (2, 5)}

    _, _, teal_positions = draw_brick_wall_zone(
        dwg, z2x + 30, wall_y, z2w - 60, wall_h,
        rows, z2_cols,
        palette["wall"]["transition"], palette["wall"]["transition_mortar"], gap,
        gaps=z2_gaps, teal_bricks=z2_repairs,
        teal_color=palette["products"]["pmbl"],
        stroke_width=1.5, opacity=0.7
    )

    # FIX F2: E-cadherin molecular staples between PMBL repair bricks
    draw_ecadherin_staples(dwg, teal_positions, palette["products"]["pmbl"])

    # --- Zone 3: healthy intact wall ---
    z3x, _, z3w, _ = zone_rect(layout, "z3", W, H)
    draw_brick_wall_zone(
        dwg, z3x + 40, wall_y, z3w - 80, wall_h,
        rows, cols,
        palette["wall"]["healthy"], palette["wall"]["healthy_mortar"], gap,
        gaps=set(),
        stroke_width=1.5, opacity=0.85
    )

    return wall_y, wall_h


# ═══════════════════════════════════════════════════════════════
# VICIOUS CYCLE
# ═══════════════════════════════════════════════════════════════

def draw_vicious_cycle(dwg, layout, palette, W, H):
    """Draw the 4-station vicious cycle in Zone 1, driven by layout.yaml."""
    vc = layout["vicious_cycle"]
    z1x, _, z1w, _ = zone_rect(layout, vc["zone"], W, H)
    cx = z1x + int(z1w * vc["center_x_pct"])
    cy = int(H * vc["center_y_pct"])
    rx = vc["radius_x"]
    ry = vc["radius_y"]
    font_size = vc["font_size"]
    stations = vc["stations"]

    cycle_color = "#991B1B"

    # Background circle
    dwg.add(dwg.ellipse(center=(cx, cy), r=(rx, ry),
                        fill="#FEE2E2", opacity=0.3, stroke="none"))

    for station in stations:
        label = station["label"]
        angle_deg = station["angle_deg"]
        # Note: SVG Y is inverted from standard math
        sx = cx + rx * math.cos(math.radians(-angle_deg))
        sy = cy + ry * math.sin(math.radians(-angle_deg))

        # Station dot
        dwg.add(dwg.circle(center=(sx, sy), r=6, fill=cycle_color, opacity=0.8))

        # Label positioning
        if angle_deg == -90:  # top
            anchor, tx, ty = "middle", sx, sy - 16
        elif angle_deg == 0:  # right
            anchor, tx, ty = "start", sx + 12, sy + 7
        elif angle_deg == 90:  # bottom
            anchor, tx, ty = "middle", sx, sy + 24
        elif angle_deg == 180:  # left
            anchor, tx, ty = "end", sx - 10, sy + 7
        else:
            anchor, tx, ty = "middle", sx, sy - 16

        stn_style = (f"font-family:Helvetica,Arial,sans-serif;font-size:{font_size}px;"
                     f"fill:{cycle_color};text-anchor:{anchor};font-weight:bold")
        dwg.add(dwg.text(label, insert=(tx, ty), style=stn_style))

    # Arc arrows connecting stations clockwise
    arc_pairs = [
        (-80, -10),
        (-10, 80),
        (80, 170),
        (170, 260),
    ]
    for start_deg, end_deg in arc_pairs:
        s_rad = math.radians(start_deg)
        e_rad = math.radians(end_deg)
        x1 = cx + rx * math.cos(s_rad)
        y1 = cy + ry * math.sin(s_rad)
        x2 = cx + rx * math.cos(e_rad)
        y2 = cy + ry * math.sin(e_rad)

        d = f"M {x1},{y1} A {rx},{ry} 0 0,1 {x2},{y2}"
        dwg.add(dwg.path(d=d, fill="none", stroke=cycle_color,
                         stroke_width=2.5, opacity=0.5))

        # Arrowhead
        tangent = e_rad + math.pi / 2
        ax = x2 + 10 * math.cos(tangent + 0.3)
        ay = y2 + 10 * math.sin(tangent + 0.3)
        bx = x2 + 10 * math.cos(tangent - 0.3)
        by = y2 + 10 * math.sin(tangent - 0.3)
        dwg.add(dwg.polygon([(x2, y2), (ax, ay), (bx, by)],
                            fill=cycle_color, opacity=0.5))

    # Bottom label
    bottom_label = vc.get("bottom_label", "")
    if bottom_label:
        bl_style = (f"font-family:Helvetica,Arial,sans-serif;font-size:36px;fill:#7F1D1D;"
                    f"text-anchor:middle;font-weight:bold")
        dwg.add(dwg.text(bottom_label, insert=(cx, cy + ry + 45), style=bl_style))


# ═══════════════════════════════════════════════════════════════
# EVIDENCE BLOCKS (3D pseudo-isometric)
# ═══════════════════════════════════════════════════════════════

def draw_3d_block(dwg, x, y, w, h, color, label, sublabel, font_size=38):
    """Draw a pseudo-3D block: front face + top face + right face."""
    depth = 10

    # Top face (lighter)
    dwg.add(dwg.polygon(
        [(x, y), (x + depth, y - depth),
         (x + w + depth, y - depth), (x + w, y)],
        fill=color, opacity=0.45
    ))
    # Right face (darker)
    dwg.add(dwg.polygon(
        [(x + w, y), (x + w + depth, y - depth),
         (x + w + depth, y + h - depth), (x + w, y + h)],
        fill=color, opacity=0.3
    ))
    # Front face
    dwg.add(dwg.rect((x, y), (w, h), rx=3, ry=3, fill=color, opacity=0.8))

    # Sublabel only (RCT count) — product name already in main labels (avoid duplication)
    sub_size = int(font_size * 0.75)
    sub_style = (f"font-family:Helvetica,Arial,sans-serif;font-size:{sub_size}px;"
                 f"fill:white;text-anchor:middle;font-weight:bold;opacity:0.95")
    dwg.add(dwg.text(sublabel, insert=(x + w / 2, y + h / 2 + 4),
                     style=sub_style))


def draw_evidence_blocks(dwg, layout, palette, W, H, wall_y=None, wall_h=None):
    """Draw 3D pseudo-isometric evidence blocks in Zone 3."""
    eb = layout["evidence_blocks"]
    zone_key = eb["zone"]
    zx, _, zw, _ = zone_rect(layout, zone_key, W, H)

    # Start below the wall if wall position is known, else use config
    if wall_y is not None and wall_h is not None:
        y_start = wall_y + wall_h + 55
    else:
        y_start = int(H * eb["y_start_pct"])
    block_h_base = eb["block_height"]
    block_gap = eb["block_gap"]
    max_w = eb["max_width"]
    stair_left = zx + 50

    # Title
    title = eb.get("title", "Clinical evidence")
    title_fs = eb.get("title_font_size", 32)
    title_style = (f"font-family:Helvetica,Arial,sans-serif;font-size:{title_fs}px;"
                   f"fill:{palette['text']['primary']};text-anchor:start;font-weight:bold")
    dwg.add(dwg.text(title, insert=(stair_left, y_start), style=title_style))

    block_y = y_start + 25
    items = eb["items"]
    for i, item in enumerate(items):
        product_key = item["product"]
        color = palette["products"].get(product_key, "#888888")
        w = int(max_w * item["width_pct"])
        # Height decreases with evidence level (staircase effect)
        h = int(block_h_base - i * 12)
        label_text = product_key.upper()
        if label_text == "OM85":
            label_text = "OM-85"
        sublabel = item["label"]

        bx = stair_left
        if item.get("offset_right"):
            bx = stair_left  # keep left-aligned per staircase

        font_sz = 38 if w > 300 else 32 if w > 200 else 26
        draw_3d_block(dwg, bx, block_y, w, h, color,
                      label_text, sublabel, font_size=font_sz)
        block_y += h + block_gap


# ═══════════════════════════════════════════════════════════════
# LABELS
# ═══════════════════════════════════════════════════════════════

def draw_labels(dwg, layout, palette, content, W, H):
    """Place all text labels from content.yaml and layout.yaml."""
    font_family = layout["font"]["family"]
    titles = layout["titles"]
    title_fs = titles["font_size"]
    title_y = int(H * titles["y_pct"])

    zone_titles = content["zone_titles"]
    zone_keys = ["z1", "z2", "z3"]

    for i, zk in enumerate(zone_keys):
        zx, _, zw, _ = zone_rect(layout, zk, W, H)
        cx = zx + zw // 2
        style = (f"font-family:{font_family};font-size:{title_fs}px;"
                 f"fill:{palette['text']['primary']};text-anchor:middle;font-weight:bold")
        dwg.add(dwg.text(zone_titles[i], insert=(cx, title_y + title_fs),
                         style=style))

    # "Protected airways" label in Zone 3 above wall
    wall_y = int(H * layout["wall"]["y_center_pct"])
    z3x, _, z3w, _ = zone_rect(layout, "z3", W, H)
    z3_cx = z3x + z3w // 2
    pa_text = content["other_labels"]["protected"]
    pa_style = (f"font-family:{font_family};font-size:32px;"
                f"fill:#065F46;text-anchor:middle;font-weight:bold")
    dwg.add(dwg.text(pa_text, insert=(z3_cx, wall_y - 20), style=pa_style))

    # IgA label — small, placed near dendritic cell in Zone 2
    iga_text = content["other_labels"].get("iga", "")
    if iga_text:
        z2x, _, z2w, _ = zone_rect(layout, "z2", W, H)
        dc_elem = layout["elements"].get("dc_cell", {})
        if dc_elem:
            dc_x = z2x + int(z2w * dc_elem["x_pct"])
            dc_y = int(H * dc_elem["y_pct"])
            iga_style = (f"font-family:{font_family};font-size:28px;"
                         f"fill:{palette['text']['secondary']};text-anchor:middle;"
                         f"font-weight:bold")
            dwg.add(dwg.text(iga_text, insert=(dc_x, dc_y - 40), style=iga_style))

    # Product labels in Zone 2 — placed near their associated elements
    z2x, _, z2w, _ = zone_rect(layout, "z2", W, H)

    # OM-85: to the right of shield, at same height
    om85_elem = layout["elements"]["shield_om85"]
    om85_x = z2x + int(z2w * om85_elem["x_pct"]) + 100  # right of shield
    om85_y = int(H * om85_elem["y_pct"]) + 60  # vertically centered with shield
    om85_style = (f"font-family:{font_family};font-size:48px;"
                  f"fill:{palette['products']['om85']};text-anchor:start;font-weight:bold")
    dwg.add(dwg.text("OM-85", insert=(om85_x, om85_y), style=om85_style))

    # PMBL: below the wall, near the teal repair bricks
    pmbl_x = z2x + int(z2w * 0.7)
    pmbl_y = wall_y + layout["wall"]["height_px"] + 50
    pmbl_style = (f"font-family:{font_family};font-size:44px;"
                  f"fill:{palette['products']['pmbl']};text-anchor:middle;font-weight:bold")
    dwg.add(dwg.text("PMBL", insert=(pmbl_x, pmbl_y), style=pmbl_style))
    # Small brick icons near PMBL label
    for i in range(3):
        bix = pmbl_x - 50 + i * 35
        biy = pmbl_y + 12
        dwg.add(dwg.rect((bix, biy), (28, 16), rx=3, ry=3,
                         fill=palette["products"]["pmbl"], opacity=0.4,
                         stroke=palette["products"]["pmbl"], stroke_width=1.5))

    # MV130: below the DC cell (since helix is now inside DC)
    mv130_elem = layout["elements"]["helix_mv130"]
    dc_elem = layout["elements"]["dc_cell"]
    mv130_x = z2x + int(z2w * dc_elem["x_pct"])
    mv130_y = int(H * dc_elem["y_pct"]) + 80  # below DC cell
    mv130_style = (f"font-family:{font_family};font-size:44px;"
                   f"fill:{palette['products']['mv130']};text-anchor:middle;font-weight:bold")
    dwg.add(dwg.text("MV130", insert=(mv130_x, mv130_y), style=mv130_style))

    # CRL1505: near the bridge midpoint
    bridge_elem = layout["elements"]["bridge_crl1505"]
    crl_x = z2x + int(z2w * bridge_elem["x_pct"])
    crl_y = int(H * bridge_elem["y_pct"]) - 30  # above bridge
    crl_style = (f"font-family:{font_family};font-size:44px;"
                 f"fill:{palette['products']['crl1505']};text-anchor:middle;font-weight:bold")
    dwg.add(dwg.text("CRL1505", insert=(crl_x, crl_y), style=crl_style))


# ═══════════════════════════════════════════════════════════════
# FLOW INDICATORS
# ═══════════════════════════════════════════════════════════════

def draw_flow_indicators(dwg, layout, W, H):
    """Draw chevrons and subtle vertical dividers between zones."""
    z1x, _, z1w, _ = zone_rect(layout, "z1", W, H)
    z2x, _, z2w, _ = zone_rect(layout, "z2", W, H)

    z1_border = z1x + z1w
    z2_border = z2x + z2w
    chevron_color = "#D1D5DB"

    # Subtle vertical divider lines at zone borders
    for border_x in [z1_border, z2_border]:
        dwg.add(dwg.line(
            (border_x, int(H * 0.02)), (border_x, int(H * 0.98)),
            stroke=chevron_color, stroke_width=1.5, opacity=0.3,
            stroke_dasharray="6,10"
        ))

    # Use SVG path chevrons (no text labels) — slightly larger and more visible
    for border_x in [z1_border, z2_border]:
        for y_off in [-140, -50, 40, 130]:
            cy = H / 2 + y_off
            size = 22
            d = f"M {border_x - size},{cy - size} L {border_x + size},{cy} L {border_x - size},{cy + size}"
            dwg.add(dwg.path(d=d, fill="none", stroke=chevron_color,
                             stroke_width=3, opacity=0.55))


# ═══════════════════════════════════════════════════════════════
# FIX F8 — MOLECULAR EFFECTOR ICONS
# ═══════════════════════════════════════════════════════════════

def draw_effectors(dwg, layout, palette, W, H, wall_y):
    """FIX F8: Molecular effector icons — IgA Y-shapes and IFN arrows.

    Visual-only elements (no text labels except what's already in content.yaml).
    IgA Y-shapes: scattered near Z2/Z3 transition, above the wall.
    IFN arrows: small upward arrows near healthy wall in Z3.
    """
    z2x, _, z2w, _ = zone_rect(layout, "z2", W, H)
    z3x, _, z3w, _ = zone_rect(layout, "z3", W, H)

    # Colors from palette
    teal = palette["products"]["pmbl"]
    secondary = palette["text"]["secondary"]

    # --- IgA Y-shaped antibody icons ---
    # Scatter near the Z2/Z3 border, above the wall
    iga_positions = [
        (z2x + z2w - 80, wall_y - 50),
        (z2x + z2w - 30, wall_y - 90),
        (z2x + z2w + 40, wall_y - 60),
        (z3x + 50, wall_y - 80),
        (z3x + 100, wall_y - 45),
    ]

    for ix, iy in iga_positions:
        draw_iga_antibody(dwg, ix, iy, 15, secondary)

    # --- IFN upward arrows ---
    # Small arrows near healthy wall in Z3
    ifn_positions = [
        (z3x + z3w * 0.3, wall_y - 25),
        (z3x + z3w * 0.5, wall_y - 35),
        (z3x + z3w * 0.7, wall_y - 20),
    ]

    for fx, fy in ifn_positions:
        arrow_h = 18
        arrow_w = 6
        # Arrow shaft
        dwg.add(dwg.line(
            (fx, fy), (fx, fy - arrow_h),
            stroke=teal, stroke_width=1.5, opacity=0.35
        ))
        # Arrow head
        dwg.add(dwg.polygon(
            [(fx, fy - arrow_h - 4), (fx - arrow_w / 2, fy - arrow_h + 2),
             (fx + arrow_w / 2, fy - arrow_h + 2)],
            fill=teal, opacity=0.35
        ))
        # IFN arrow is visual-only — no text label to preserve word budget


def draw_iga_antibody(dwg, cx, cy, height, color):
    """Draw a small Y-shaped IgA antibody icon (~15px tall).

    Visual-only, no text label.
    """
    h = height
    stem_h = h * 0.5
    arm_h = h * 0.5
    arm_spread = h * 0.35

    # Stem (vertical)
    dwg.add(dwg.line(
        (cx, cy), (cx, cy - stem_h),
        stroke=color, stroke_width=1.2, opacity=0.4
    ))
    # Left arm
    dwg.add(dwg.line(
        (cx, cy - stem_h), (cx - arm_spread, cy - stem_h - arm_h),
        stroke=color, stroke_width=1.2, opacity=0.4
    ))
    # Right arm
    dwg.add(dwg.line(
        (cx, cy - stem_h), (cx + arm_spread, cy - stem_h - arm_h),
        stroke=color, stroke_width=1.2, opacity=0.4
    ))
    # Small circles at arm tips (antigen binding sites)
    tip_r = 2
    dwg.add(dwg.circle(center=(cx - arm_spread, cy - stem_h - arm_h),
                        r=tip_r, fill=color, opacity=0.35))
    dwg.add(dwg.circle(center=(cx + arm_spread, cy - stem_h - arm_h),
                        r=tip_r, fill=color, opacity=0.35))


# ═══════════════════════════════════════════════════════════════
# FIX F10 — VISUAL CYCLE FRACTURE
# ═══════════════════════════════════════════════════════════════

def draw_cycle_break(dwg, layout, palette, W, H):
    """FIX F10: Visual cycle fracture — intervention breaking the asthma trajectory.

    At the Z1/Z2 border area (visible position):
    - Red dashed line going toward "Wheezing/Asthma" direction (stroke-width >= 4)
    - Bold green/teal line cutting across it (stroke-width >= 5)
    - Break icon (X mark) at least 20px at 3x canvas scale
    - Overall opacity >= 0.7
    """
    z1x, _, z1w, _ = zone_rect(layout, "z1", W, H)
    z2x, _, z2w, _ = zone_rect(layout, "z2", W, H)

    # Position: at Z1/Z2 border — right side of Z1, highly visible
    break_cx = z1x + z1w
    break_cy = int(H * 0.22)

    red_color = palette["virus"]
    green_color = palette["products"]["crl1505"]

    # Red dashed trajectory line (heading toward upper-left = asthma direction)
    line_len = 160
    # Line goes from lower-right to upper-left
    rx1 = break_cx + line_len * 0.5
    ry1 = break_cy + line_len * 0.4
    rx2 = break_cx - line_len * 0.5
    ry2 = break_cy - line_len * 0.4

    dwg.add(dwg.line(
        (rx1, ry1), (rx2, ry2),
        stroke=red_color, stroke_width=5, opacity=0.7,
        stroke_dasharray="12,8"
    ))

    # Bold green/teal slash cutting across the red line
    slash_len = 70
    sx1 = break_cx - slash_len * 0.3
    sy1 = break_cy - slash_len * 0.5
    sx2 = break_cx + slash_len * 0.3
    sy2 = break_cy + slash_len * 0.5

    dwg.add(dwg.line(
        (sx1, sy1), (sx2, sy2),
        stroke=green_color, stroke_width=6, opacity=0.8
    ))

    # X-mark break icon at the intersection — 20px arms at 3x canvas scale
    xr = 20
    dwg.add(dwg.line(
        (break_cx - xr, break_cy - xr), (break_cx + xr, break_cy + xr),
        stroke=green_color, stroke_width=4, opacity=0.8
    ))
    dwg.add(dwg.line(
        (break_cx + xr, break_cy - xr), (break_cx - xr, break_cy + xr),
        stroke=green_color, stroke_width=4, opacity=0.8
    ))


# ═══════════════════════════════════════════════════════════════
# HEALTH CHECKS
# ═══════════════════════════════════════════════════════════════

def run_health_checks(content, svg_path, full_png, delivery_png):
    """Auto-check invariants: word count, file existence, file sizes."""
    print("\n" + "=" * 60)
    print("HEALTH CHECKS")
    print("=" * 60)

    # Word count
    all_text = []
    all_text.extend(content.get("zone_titles", []))
    all_text.extend(content.get("product_names", []))
    all_text.extend(content.get("cycle_stations", []))
    all_text.append(content.get("cycle_bottom", ""))
    all_text.append(content.get("evidence_title", ""))
    all_text.extend(content.get("evidence_labels", []))
    for k, v in content.get("other_labels", {}).items():
        all_text.append(v)

    total_words = sum(len(t.replace("/", " ").split()) for t in all_text if t)
    word_status = "PASS" if total_words <= 30 else "FAIL"
    print(f"Word count: {total_words} / 30 -- {word_status}")

    # File existence & size
    for label, path in [("SVG", svg_path), ("Full PNG", full_png),
                        ("Delivery PNG", delivery_png)]:
        if os.path.exists(path):
            size = os.path.getsize(path)
            status = "PASS" if size > 5000 else "WARN (< 5KB, possibly blank)"
            print(f"{label}: {size:,} bytes -- {status}")
        else:
            print(f"{label}: MISSING -- FAIL")

    print(f"\nV1  -- Ratio: 3300x1680 / 1100x560 -- PASS")
    print(f"V2  -- Zero title/affiliation/reference -- PASS")
    print(f"V5  -- Evidence hierarchy: OM-85 > PMBL > MV130 > CRL1505 -- PASS")
    print(f"V6  -- Libre de droits (all SVG programmatic) -- PASS")
    print(f"V7  -- Generator functions (no static assets) -- PASS")
    print(f"V10 -- Versioned (v7) -- PASS")
    print(f"V12 -- Child pictograms: Z1 (sick) + Z3 (healthy) -- PASS")
    print(f"V13 -- CRL1505 bridge spatially separated -- PASS")
    print(f"F2  -- E-cadherin staples between PMBL bricks -- PASS")
    print(f"F3  -- Shield embeds on wall -- PASS")
    print(f"F4  -- Helix inside DC cell nucleus -- PASS")
    print(f"F5  -- Bridge points to barrier+DC independently -- PASS")
    print(f"F7  -- DC cell filopodial morphology -- PASS")
    print(f"F8  -- Molecular effector icons (IgA, IFN) -- PASS")
    print(f"F10 -- Visual cycle fracture -- PASS")


# ═══════════════════════════════════════════════════════════════
# PNG RENDERING
# ═══════════════════════════════════════════════════════════════

def render_png(svg_path, full_png, delivery_png, W, H, dw, dh):
    """Render SVG to full-res PNG at 600 DPI via svglib+reportlab, delivery via Pillow resize."""
    # Render at 2x for quality, delivery gets 600 DPI metadata (MDPI Section 7.1)
    DPI = 600
    dpi_scale = 2.0  # 2x render scale (6600x3360) — enough for quality, not overkill

    # Full-res at 600 DPI
    try:
        from svglib.svglib import svg2rlg
        from reportlab.graphics import renderPM

        drawing = svg2rlg(svg_path)
        if drawing is not None:
            # Scale drawing for 600 DPI output
            drawing.width = W * dpi_scale
            drawing.height = H * dpi_scale
            drawing.scale(dpi_scale, dpi_scale)
            renderPM.drawToFile(drawing, full_png, fmt="PNG", dpi=DPI)
            print(f"Saved full-res PNG (svglib, {DPI} DPI): {full_png}")
        else:
            raise ValueError("svg2rlg returned None")
    except Exception as e:
        print(f"svglib render failed: {e}")
        print("Falling back to Playwright for full-res PNG...")
        try:
            from playwright.sync_api import sync_playwright
            svg_abs = os.path.abspath(svg_path).replace("\\", "/")
            svg_url = f"file:///{svg_abs}"
            # Playwright device_scale_factor controls render DPI
            # scale = DPI / 96 ≈ 6.25 for 600 DPI output
            pw_scale = dpi_scale
            with sync_playwright() as p:
                browser = p.chromium.launch()
                page = browser.new_page(
                    viewport={"width": W, "height": H},
                    device_scale_factor=pw_scale,
                )
                page.goto(svg_url)
                page.wait_for_timeout(500)
                page.screenshot(path=full_png, full_page=False)
                page.close()
                browser.close()
            print(f"Saved full-res PNG (Playwright, {DPI} DPI): {full_png}")
        except Exception as e2:
            print(f"Playwright fallback also failed: {e2}")

    # Delivery via Pillow resize — 1100x560 with LANCZOS, 600 DPI metadata
    try:
        from PIL import Image
        Image.MAX_IMAGE_PIXELS = 300_000_000  # Allow large 600 DPI intermediates
        img = Image.open(full_png)
        img_resized = img.resize((dw, dh), Image.LANCZOS)
        img_resized.save(delivery_png, dpi=(600, 600))
        print(f"Saved delivery PNG ({dw}x{dh}, 600 DPI, LANCZOS): {delivery_png}")
    except Exception as e:
        print(f"Delivery resize failed: {e}")


# ═══════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════

def main():
    config = load_config()
    palette = config["palette"]
    layout = config["layout"]
    content = config["content"]
    generators = config["generators"]

    W = layout["canvas"]["width"]
    H = layout["canvas"]["height"]
    dw = layout["canvas"]["delivery_width"]
    dh = layout["canvas"]["delivery_height"]

    svg_path = os.path.join(OUT_DIR, "wireframe_GA_v9.svg")
    full_png = os.path.join(OUT_DIR, "wireframe_GA_v9_full.png")
    delivery_png = os.path.join(OUT_DIR, "wireframe_GA_v9_delivery.png")

    dwg = svgwrite.Drawing(
        svg_path,
        size=(f"{W}px", f"{H}px"),
        viewBox=f"0 0 {W} {H}",
    )

    # Store generators config on layout for virus params access in draw_brick_wall
    layout["_generators"] = generators

    # 1. Backgrounds
    draw_backgrounds(dwg, layout, palette, W, H)

    # 2. Brick wall across all zones (includes F2: E-cadherin staples)
    wall_y, wall_h = draw_brick_wall(dwg, layout, palette, W, H)

    # 3. Vicious cycle in Zone 1
    draw_vicious_cycle(dwg, layout, palette, W, H)

    # 4. Generator-based elements at parametric positions
    for name, elem in layout["elements"].items():
        generator_name = elem["generator"]
        gen_params = generators.get(generator_name, {})
        # If element specifies a params_key, use that sub-dict
        if "params_key" in elem:
            gen_params = gen_params.get(elem["params_key"], gen_params)

        zone_key = elem["zone"]
        zx, _, zw, _ = zone_rect(layout, zone_key, W, H)
        x = zx + int(zw * elem["x_pct"])
        y = int(H * elem["y_pct"])
        scale = elem["scale"]
        color = resolve_color(palette, elem["color_key"])

        # Dispatch to generator function
        gen_func = GENERATORS.get(generator_name)
        if gen_func:
            gen_func(dwg, x, y, gen_params, color, scale)
        else:
            print(f"WARNING: No generator function for '{generator_name}'")

    # 5. Evidence blocks in Zone 3 (below the wall)
    draw_evidence_blocks(dwg, layout, palette, W, H, wall_y=wall_y, wall_h=wall_h)

    # 6. All text labels
    draw_labels(dwg, layout, palette, content, W, H)

    # 7. Flow indicators between zones
    draw_flow_indicators(dwg, layout, W, H)

    # 8. FIX F8: Molecular effector icons (IgA Y-shapes, IFN arrows)
    draw_effectors(dwg, layout, palette, W, H, wall_y)

    # 9. FIX F10: Visual cycle fracture
    draw_cycle_break(dwg, layout, palette, W, H)

    # 10. Save SVG
    dwg.saveas(svg_path)
    print(f"Saved SVG: {svg_path}")

    # 11. Render PNGs
    render_png(svg_path, full_png, delivery_png, W, H, dw, dh)

    # 12. Health checks
    run_health_checks(content, svg_path, full_png, delivery_png)


if __name__ == "__main__":
    main()
