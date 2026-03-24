# VALIDATION — vec/pipeline

## Invariants strictement verifies

Ces invariants doivent etre vrais a chaque execution du pipeline. Une violation est un bug, pas un warning.

---

### V8: Rendu complet (Complete Render)

**Enonce :** Chaque execution produit exactement 3 fichiers: SVG + full PNG + delivery PNG. Si un fichier manque ou est corrompu, l'execution est consideree en echec.

**Verification :**
```python
assert os.path.exists(svg_path) and os.path.getsize(svg_path) > 1024
assert os.path.exists(full_png) and os.path.getsize(full_png) > 50_000
assert os.path.exists(delivery_png) and os.path.getsize(delivery_png) > 5_000
```

**Consequence en cas de violation :** Fail Loud. Le pipeline affiche l'erreur. Aucun artefact n'est archive.

---

### V9: Delivery non-blanc (Non-Blank Delivery)

**Enonce :** Le PNG delivery ne doit jamais etre un fichier blanc ou quasi-blanc. C'est le symptome d'un rendu echoue (historiquement cause par svglib).

**Verification :**
```python
from PIL import Image
import numpy as np
img = Image.open(delivery_png)
mean_pixel = np.array(img).mean()
assert mean_pixel < 250, f"Delivery is blank (mean pixel = {mean_pixel})"
```

**Seuil :** mean pixel > 250 sur une image RGB signifie que l'image est quasi-blanche. Pour un GA riche en couleurs, le mean pixel attendu est entre 100 et 200.

**Consequence en cas de violation :** Fail Loud. Le rendu Playwright a probablement echoue silencieusement (SVG non charge, timeout, etc.). Verifier le HTML wrapper et le chemin file:/// du SVG.

---

### VN3: Jamais de brouillon (Never Ship Drafts)

**Enonce :** Un fichier produit par le pipeline ne porte jamais le label "draft" ou "WIP". Soit il passe les auto-checks, soit il est explicitement marque en echec.

**Verification :** Pas de fichier nomme `*_draft.*` ou `*_wip.*` dans `artefacts/wireframes/`. Le nommage est strict: `wireframe_GA_v10.*` ou `wireframe_GA_v10_iterN.*`.

**Consequence en cas de violation :** Renommer ou supprimer le fichier. Chaque artefact archive est une iteration complete, pas un brouillon.

---

## Invariants derives (verifiables mais non bloquants seuls)

### V-PIP1: Dimensions full PNG coherentes avec device_scale_factor

**Enonce :** Le full PNG doit avoir des dimensions proches de `(dw * device_scale_factor, dh * device_scale_factor)` — soit ~(2200, 1120) avec scale=2.

**Verification :**
```python
img = Image.open(full_png)
w, h = img.size
assert abs(w - dw * 2) < 10 and abs(h - dh * 2) < 10
```

**Note :** Playwright peut produire des dimensions legerement differentes selon le contenu de la page. La tolerance de 10px absorbe ces variations.

---

### V-PIP2: SVG parseable XML

**Enonce :** Le fichier SVG produit est un document XML valide, parseable par `xml.etree.ElementTree`.

**Verification :**
```python
import xml.etree.ElementTree as ET
ET.parse(svg_path)  # leve ParseError si invalide
```

---

### V-PIP3: Palette 4-couleurs presente dans le SVG

**Enonce :** Les 4 hex codes produit (#2563EB, #0D9488, #7C3AED, #059669) doivent etre presents dans le fichier SVG.

**Verification :**
```python
svg_text = open(svg_path).read().lower()
for hex_code in ["#2563eb", "#0d9488", "#7c3aed", "#059669"]:
    assert hex_code in svg_text, f"Missing {hex_code}"
```

**Raison :** Si une couleur produit manque, c'est que le dessin correspondant a ete omis ou que la palette.yaml a ete modifiee sans mise a jour du script.

---

### V-PIP4: Delivery DPI = 600

**Enonce :** Le PNG delivery doit contenir la metadata DPI = 600 dans ses chunks PNG.

**Verification :**
```python
img = Image.open(delivery_png)
dpi = img.info.get("dpi", (72, 72))
assert dpi == (600, 600), f"DPI = {dpi}, expected (600, 600)"
```

---

### V-PIP5: Archivage non-destructif

**Enonce :** Apres archivage, tout artefact vN-1 existant dans `artefacts/wireframes/` a conserve son checksum d'origine.

**Verification :** Avant archivage, calculer MD5 des fichiers existants. Apres archivage, verifier que les MD5 sont identiques.

---

## Resume des invariants

| ID | Invariant | Automatisable | Bloquant |
|----|-----------|---------------|----------|
| V8 | Rendu complet (3 fichiers) | Oui | Oui |
| V9 | Delivery non-blanc | Oui | Oui |
| VN3 | Jamais de brouillon | Oui | Oui |
| V-PIP1 | Dimensions full PNG | Oui | Non |
| V-PIP2 | SVG parseable XML | Oui | Non |
| V-PIP3 | Palette 4-couleurs | Oui | Non |
| V-PIP4 | Delivery DPI 600 | Oui | Non |
| V-PIP5 | Archivage non-destructif | Oui | Non |
