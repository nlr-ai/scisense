# IMPLEMENTATION — vec/pipeline

## Architecture des fichiers

```
scisense/
├── missions/immunomodulator/
│   ├── scripts/
│   │   └── compose_ga_v10.py          ← Script principal (compositeur parametrique)
│   ├── config/
│   │   ├── layout_v10.yaml            ← Geometrie, positions, canvas dimensions
│   │   ├── palette.yaml               ← Couleurs (produits, bandes, virus, fond)
│   │   └── content.yaml               ← Labels textuels, budget mots
│   └── artefacts/
│       ├── wireframes/                ← Sortie: SVG + PNGs archives
│       │   ├── wireframe_GA_v10.svg
│       │   ├── wireframe_GA_v10_full.png
│       │   └── wireframe_GA_v10_delivery.png
│       └── contours/                  ← Entree optionnelle (depuis vec/calibration)
│           ├── S3_sick_points.json
│           └── S4_healthy_points.json
├── scripts/
│   └── validate_ga.py                 ← Tribunal editorial (utilise par vec/editorial, inclut des checks H5)
└── docs/vec/pipeline/                 ← Ce module
    ├── 01_RESULTS.md → 10_SYNC.md
```

---

## compose_ga_v10.py — Responsabilites

### Fonctions utilitaires

| Fonction | Role | Lignes |
|----------|------|--------|
| `_lighten_hex(hex, factor)` | Eclaircir une couleur hex | ~6 |
| `_lerp_color(c1, c2, t)` | Interpolation lineaire entre 2 couleurs hex | ~6 |
| `_catmull_rom_to_bezier(points)` | Convertir des points Catmull-Rom en segments Bezier cubiques | ~12 |
| `load_config()` | Charger palette.yaml + content.yaml + layout_v10.yaml | ~10 |
| `resolve_color(palette, key)` | Resoudre une couleur par notation pointee ("products.om85") | ~6 |

### Fonctions de layout

| Fonction | Role |
|----------|------|
| `get_zone_rect(layout, zone_key, W, H)` | Calculer le rectangle d'une zone (margin_left, bronchus, margin_right) |
| `get_bronchus_rect(layout, W, H)` | Calculer le rectangle du bronchus (x, y, w, h) |
| `get_band_rects(layout, W, H)` | Calculer les 4 rectangles de bandes anatomiques |
| `health_at_x(x, bx, bw)` | Calculer la valeur Health Vector H (0→1) selon position X |

### Fonctions de dessin (draw_*)

| Fonction | Element dessine | Bande |
|----------|-----------------|-------|
| `draw_background()` | Gradient de fond L→R | — |
| `draw_bronchus_frame()` | Cadre + separateurs + fills alternees | Toutes |
| `draw_lumen()` | Virus, fleches, convergence IgA, anticorps Y | Lumen |
| `draw_epithelium()` | Cellules epitheliales, gaps, shield, staples | Epithelium |
| `draw_lamina_propria()` | DC, cellules immunitaires, balance Th1/Th2 | Lamina |
| `draw_muscle()` | Muscle lisse epaissi → resolu | Muscle |
| `draw_crl1505_relay()` | Arc de relais gut-lung | Inter-bandes |
| `draw_child_contour()` | Silhouettes enfants (sick / healthy) | Marges |
| `draw_vicious_cycle()` | Cercle vicieux inflammation | Marge gauche |
| `draw_cycle_break()` | Rupture du cycle par CRL1505 | Marge gauche |
| `draw_evidence_bars()` | Barres de preuve par produit | Bas/marge |
| `draw_legend()` | Legende produits-couleurs | Bas |

### Fonctions de dessin d'elements

| Fonction | Element |
|----------|---------|
| `draw_virus_icon(dwg, cx, cy, r, color)` | Icone virus (cercle + spikes) |
| `draw_iga_y(dwg, cx, cy, height, color)` | Anticorps IgA en forme de Y |

### Fonctions de rendu

| Fonction | Role |
|----------|------|
| `render_png(svg_path, full_png, delivery_png, W, H, dw, dh)` | Pipeline complet: HTML wrapper → Playwright → Pillow resize |

### Point d'entree

| Fonction | Role |
|----------|------|
| `main()` | Orchestration: load → draw → save → render → print |

---

## Dependencies

| Package | Version | Role |
|---------|---------|------|
| `svgwrite` | >=1.4 | Generation SVG programmatique |
| `pyyaml` | >=6.0 | Parsing des configs YAML |
| `playwright` | >=1.40 | Rendu SVG → PNG headless |
| `Pillow` | >=10.0 | Resize PNG, injection DPI metadata |

### Dependencies optionnelles (pour auto-checks)

| Package | Version | Role |
|---------|---------|------|
| `numpy` | >=1.24 | Calcul mean pixel pour V9 (delivery non-blanc) |

### Dependencies systeme

| Composant | Requis par |
|-----------|------------|
| Chromium (via Playwright) | `render_png()` — installe via `playwright install chromium` |

---

## Config files — Schema

### layout_v10.yaml

```yaml
canvas:
  width: 3300
  height: 1680
  delivery_width: 1100
  delivery_height: 560
zones:
  margin_left: { x_pct, width_pct }
  bronchus: { x_pct, width_pct }
  margin_right: { x_pct, width_pct }
bronchus:
  y_start_pct: float
  y_end_pct: float
  corner_radius: int
  border_color: hex
  border_width: int
  separator_width: int
  separator_color: hex
  bands:
    lumen: { height_pct }
    epithelium: { height_pct }
    lamina: { height_pct }
    muscle: { height_pct }
band_content:
  lumen: { virus_count, virus_radius, virus_x_range, iga_count, ... }
  # ... per-band element parameters
gradient:
  left_color: hex
  center_color: hex
  right_color: hex
child_sick: { x_pct, y_pct, scale }
child_healthy: { x_pct, y_pct, scale }
```

### palette.yaml

```yaml
background: hex
virus: hex
products:
  om85: "#2563EB"
  pmbl: "#0D9488"
  mv130: "#7C3AED"
  crl1505: "#059669"
bands:
  lumen: hex
  lamina_bg: hex
```

### content.yaml

```yaml
# Labels textuels avec budget mots
# Chaque label est un string, total <= 30 mots (V3)
```

---

## Chemins critiques

| Variable | Valeur |
|----------|--------|
| `BASE` | `C:\Users\reyno\scisense\missions\immunomodulator` |
| `CONFIG_DIR` | `{BASE}/config` |
| `OUT_DIR` | `{BASE}/artefacts/wireframes` |
| Contours | `{BASE}/artefacts/contours/S{3,4}_*_points.json` |
| HTML wrapper temp | `{OUT_DIR}/_render_v10.html` (supprime apres rendu) |

---

## Etat d'implementation

| Composant | Statut | Notes |
|-----------|--------|-------|
| compose_ga_v10.py | IMPLEMENTE | ~1080 lignes, fonctionnel |
| render_png() | IMPLEMENTE | Playwright HTML wrapper, resout le bug svglib |
| Auto-check palette (S5d) | IMPLEMENTE | Grep dans A5 step 5 |
| Auto-check delivery blanc (S5c/V9) | PARTIEL | Le print existe mais pas d'assert formel |
| Archivage versionne (P11) | PARTIEL | Ecriture dans OUT_DIR, mais pas de protection explicite contre ecrasement |
| validate_ga.py integration | PARTIEL | Consolide H1 checks, pas encore tous les H5 checks |
