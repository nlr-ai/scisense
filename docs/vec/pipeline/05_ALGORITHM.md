# ALGORITHM — vec/pipeline

## A-PIP1: Pipeline de rendu E2E

Reproduit A5 de la mission immunomodulateur, specialise pour le module pipeline.

```
ENTREE: compose_ga_v10.py + 3 YAML configs + contours JSON (optionnels)

1. CHARGER
   load_config() → dict { palette, layout, content }
   _load_contours() → _CONTOUR_SICK, _CONTOUR_HEALTHY (ou None)

   Chemins:
     CONFIG_DIR = missions/immunomodulator/config/
     palette    = CONFIG_DIR/palette.yaml
     content    = CONFIG_DIR/content.yaml
     layout     = CONFIG_DIR/layout_v10.yaml
     contours   = missions/immunomodulator/artefacts/contours/S{3,4}_*_points.json

2. INITIALISER CANVAS
   W = layout.canvas.width       (3300)
   H = layout.canvas.height      (1680)
   dw = layout.canvas.delivery_width   (1100)
   dh = layout.canvas.delivery_height  (560)
   dwg = svgwrite.Drawing(svg_path, size=(W,H), viewBox="0 0 W H")

3. DESSINER (12 etapes sequentielles)
   Chaque etape appelle une fonction draw_*() qui lit layout + palette.
   L'ordre determine le z-order SVG.

   Sequence:
     background → bronchus_frame → muscle → epithelium → lumen →
     lamina_propria → crl1505_relay → child_contour(sick) →
     child_contour(healthy) → vicious_cycle → cycle_break →
     evidence_bars → legend

   Chaque element dans le bronchus utilise health_at_x() pour
   sa transformation parametrique L→R.

4. SAUVER SVG
   dwg.save() → wireframe_GA_v10.svg
   Validation: fichier existe, > 1 KB, parseable XML

5. RENDRE FULL RES
   a. Creer _render_v10.html:
      <img src="file:///absolute/path/wireframe_GA_v10.svg"
           style="width:{dw}px; height:{dh}px">
   b. Playwright:
      - launch chromium headless
      - new_page(viewport={width:dw, height:dh}, device_scale_factor=2)
      - goto file:///.../_render_v10.html
      - wait_for_timeout(2000)
      - screenshot(path=full_png, full_page=True, timeout=30000)
      - close browser
   c. Supprimer _render_v10.html
   Validation: fichier existe, dimensions ~= (dw*2, dh*2), > 50 KB

6. RENDRE DELIVERY
   a. Pillow: img = Image.open(full_png)
   b. delivery = img.resize((dw, dh), Image.LANCZOS)
   c. delivery.save(delivery_png, dpi=(600, 600))
   Validation: fichier existe, dimensions = (dw, dh), > 5 KB, PAS blanc

SORTIE: wireframe_GA_v10.svg + wireframe_GA_v10_full.png + wireframe_GA_v10_delivery.png
```

---

## A-PIP2: Transformation parametrique (Health Vector)

```
ENTREE: position X d'un element dans le bronchus

1. CALCULER H
   H = (x - bx) / bw
   Clampe a [0.0, 1.0]

2. APPLIQUER H
   Chaque famille d'elements utilise H differemment:

   - Virus (lumen):
     Densite = max quand H ≈ 0, zero quand H > 0.5
     Opacite = 0.85 * (1 - H)

   - Epithelium:
     H ≈ 0: cellules disjointes, gaps visibles (barriere brisee)
     H ≈ 1: cellules jointes, shield OM-85 + staples PMBL

   - Lamina propria:
     H ≈ 0: DC dormantes (gris), desequilibre Th2
     H ≈ 1: DC activees (couleur produit), balance Th1-Th2

   - Muscle lisse:
     H ≈ 0: epaissi, contraction inflammatoire
     H ≈ 1: fin, resolu

3. INTERPOLATION COULEUR
   _lerp_color(c_sick, c_healthy, H) pour les transitions graduelles
   Les couleurs sick et healthy viennent de palette.yaml

SORTIE: parametres visuels (opacite, taille, couleur, position)
        appliques a l'element SVG
```

---

## A-PIP3: Rendu des contours organiques (enfants)

```
ENTREE: points JSON (liste de [x, y]) + position cible + scale + palette

1. CHARGER POINTS
   Si _CONTOUR_{SICK,HEALTHY} est None → fallback geometrique (cercle + rectangle)
   Sinon → liste de points normalises

2. CONSTRUIRE CHEMIN SVG
   a. Points bruts → Catmull-Rom spline (4+ points requis)
   b. _catmull_rom_to_bezier(points) → segments Bezier cubiques
   c. Chaque segment = (cp1, cp2, end_point)

3. DESSINER
   a. Commencer par M (move to) premier point
   b. Pour chaque segment Bezier: C cp1x,cp1y cp2x,cp2y ex,ey
   c. Fermer le path (Z)
   d. Fill avec couleur produit (opacite 0.15-0.25)
   e. Stroke avec couleur plus soutenue

4. DETAILS CONTEXTUELS
   - Enfant sick: rouge/virus, posture affaissee (contour S3)
   - Enfant healthy: vert/CRL1505, posture droite (contour S4)

SORTIE: element <path> SVG avec courbes organiques
```

---

## A-PIP4: Auto-check post-generation

```
ENTREE: 3 fichiers produits + configs

1. S5a: SVG NON-VIDE
   xml.etree.ElementTree.parse(svg_path)
   Si echec → FAIL "SVG corrompu ou vide"

2. S5b: FULL PNG CORRECT
   img = Image.open(full_png)
   width, height = img.size
   Si width < dw ou height < dh → FAIL "Full PNG sous-dimensionne"
   Si os.path.getsize(full_png) < 50000 → FAIL "Full PNG trop petit"

3. S5c: DELIVERY CORRECT
   img = Image.open(delivery_png)
   Si img.size != (dw, dh) → FAIL "Delivery dimensions incorrectes"
   Si os.path.getsize(delivery_png) < 5000 → FAIL "Delivery trop petit"
   mean_pixel = numpy.array(img).mean()
   Si mean_pixel > 250 → FAIL "Delivery est blanc"

4. S5d: PALETTE PRESENTE
   svg_text = open(svg_path).read()
   Pour chaque hex in [#2563EB, #0D9488, #7C3AED, #059669]:
     Si hex.lower() not in svg_text.lower() → FAIL f"Couleur {hex} absente"

5. S5e: ARCHIVE INTACTE
   Pour chaque fichier dans artefacts/wireframes/ avec version precedente:
     Si checksum a change → FAIL "Artefact vN-1 ecrase"

6. S5f: CONFIG COHERENCE
   palette_yaml_colors = extract_product_colors(palette.yaml)
   svg_colors = extract_colors_from_svg(svg_path)
   Si mismatch → FAIL "Couleur palette.yaml non utilisee"

7. S5g: ASSETS EXISTANTS
   Pour chaque asset reference dans layout_v10.yaml:
     Si not os.path.exists(asset_path) → FAIL f"Asset manquant: {asset_path}"

8. S5h: WORD COUNT COHERENT
   content_words = count_words(content.yaml)
   svg_words = count_text_elements(svg_path)
   Si content_words != svg_words → WARN "Word count diverge"

SORTIE: 8 signals (PASS/FAIL) → H5
```

---

## A-PIP5: Sequence d'execution main()

```
1. print("Loading config...")
2. config = load_config()                    # palette + content + layout_v10
3. W, H, dw, dh = canvas dimensions
4. _load_contours()                          # optional, no fail if absent
5. Creer svgwrite.Drawing
6. 12 draw_*() calls (voir B-PIP2)
7. dwg.save()                                # SVG sur disque
8. render_png(svg_path, full_png, delivery_png, W, H, dw, dh)
9. print("V10 compilation complete.")

Duree typique: ~3-8 secondes (Playwright domine le temps)
```
