# BEHAVIORS — vec/pipeline

## B-PIP1: Chargement et validation des configs

**Declencheur :** Debut de chaque execution de `compose_ga_v10.py`.

**Comportement observable :**
1. `load_config()` ouvre `palette.yaml`, `content.yaml`, `layout_v10.yaml`
2. Chaque fichier est parse via `yaml.safe_load()`
3. Si un fichier manque → `FileNotFoundError` (fail loud)
4. Si un YAML est malformed → `yaml.YAMLError` (fail loud)
5. Les valeurs sont accessibles via `resolve_color(palette, "products.om85")` — notation pointee

**Sortie :** Dictionnaire `config` avec 3 cles: `palette`, `layout`, `content`.

**Verification :** Le print `"Loading config..."` apparait dans la console. Si ce message n'apparait pas, le script n'a pas demarre.

---

## B-PIP2: Generation SVG sequentielle

**Declencheur :** Configs chargees et contours optionnellement charges.

**Comportement observable :**
Le script dessine les elements dans un ordre strict. L'ordre de dessin determine le z-order SVG (dernier dessine = au-dessus).

```
1. draw_background()          — gradient de fond L→R
2. draw_bronchus_frame()      — cadre + separateurs de bandes + fills alternees
3. draw_muscle()              — bande 4 (la plus basse, dessinee en premier)
4. draw_epithelium()          — bande 2
5. draw_lumen()               — bande 1 (virus, IgA convergence, fleches)
6. draw_lamina_propria()      — bande 3 (DC, cellules immunitaires)
7. draw_crl1505_relay()       — arc de relais gut-lung
8. draw_child_contour() x2    — silhouettes enfant malade (gauche) / sain (droite)
9. draw_vicious_cycle()       — cercle vicieux inflammation
10. draw_cycle_break()        — rupture du cycle par CRL1505
11. draw_evidence_bars()      — barres de preuve par produit
12. draw_legend()             — legende des produits avec couleurs
```

Chaque etape imprime son nom dans la console (`"  Drawing background..."`, etc.).

**Sortie :** `dwg.save()` ecrit le fichier SVG sur disque.

---

## B-PIP3: Rendu PNG via Playwright

**Declencheur :** SVG sauve sur disque.

**Comportement observable :**
1. Creation d'un fichier HTML wrapper temporaire (`_render_v10.html`)
   - Contient un `<img>` pointant vers le SVG via `file:///` protocol
   - CSS: `body { margin:0; padding:0; }`, `img { width:1100px; height:560px; }`
2. Lancement de Chromium headless via Playwright
3. Navigation vers le HTML wrapper
4. Attente de 2000ms (rendu du SVG par le navigateur)
5. Screenshot full page → `full_png`
6. Fermeture du navigateur
7. Suppression du HTML wrapper temporaire

**Sortie :** `wireframe_GA_v10_full.png` sur disque.

**Fallback :** Si Playwright echoue (timeout, pas installe, etc.), le message d'erreur est affiche mais le SVG reste disponible.

---

## B-PIP4: Resize et injection DPI

**Declencheur :** Full PNG produit avec succes.

**Comportement observable :**
1. Pillow ouvre le full PNG
2. Resize via `Image.LANCZOS` a 1100x560 (delivery dimensions)
3. Sauvegarde avec `dpi=(600, 600)` dans les metadata PNG
4. Print des dimensions et DPI pour verification humaine

**Sortie :** `wireframe_GA_v10_delivery.png` — fichier livrable, 1100x560, 600 DPI.

**Pourquoi LANCZOS :** Filtre de downscale le plus net. Preserve les details typographiques mieux que BILINEAR ou BICUBIC. Essentiel quand le texte doit rester lisible a 50% zoom (V7).

---

## B-PIP5: Chargement des contours organiques

**Declencheur :** Debut de `main()`, apres chargement des configs.

**Comportement observable :**
1. `_load_contours()` cherche `S3_sick_points.json` et `S4_healthy_points.json` dans `artefacts/contours/`
2. Si presents → charge les points en memoire (variables globales `_CONTOUR_SICK`, `_CONTOUR_HEALTHY`)
3. Si absents → les variables restent `None`, les silhouettes enfants utilisent un fallback geometrique

**Tolerance :** Les contours sont optionnels. Le pipeline fonctionne sans eux — les enfants sont dessines avec des formes basiques. Ce n'est pas une erreur, c'est un mode degrade accepte (les contours organiques viennent de `vec/calibration`, un module separe).

---

## B-PIP6: Transformation parametrique L→R (Health Vector)

**Declencheur :** Chaque element dessine dans le bronchus.

**Comportement observable :**
La fonction `health_at_x(x, bx, bw)` retourne une valeur H entre 0 et 1 selon la position horizontale dans le bronchus:
- `x = bx` (bord gauche) → H = 0 (maladie)
- `x = bx + bw` (bord droit) → H = 1 (sante)

Cette valeur H pilote parametriquement:
- L'opacite et la densite des virus (H bas = beaucoup de virus)
- L'integrite de l'epithelium (H bas = brise, H haut = scelle)
- L'activation des cellules immunitaires (H bas = dormantes, H haut = activees)
- L'epaisseur du muscle lisse (H bas = epaissi/inflamme, H haut = fin/resolu)

**Principe :** Le gradient de sante n'est pas dessine — il EMERGE de la transformation parametrique de chaque element en fonction de sa position X. C'est la signature architecturale du VEC.
