# PATTERNS — vec/pipeline

## P8: End-to-End (E2E) Pipeline

**Principe :** Chaque iteration execute la chaine complete, sans exception. Pas de rendu partiel. Pas de "je ferai le PNG apres".

**Raison :** Un SVG sans PNG ne peut pas etre valide visuellement. Un PNG sans SVG source n'est pas reproductible. Les 3 fichiers forment un triplet atomique.

**Application :** `compose_ga_v10.py` genere le SVG puis appelle `render_png()` dans le meme run. Si le rendu echoue, le message d'erreur est affiche mais le SVG reste disponible pour debug (fail loud, pas fail silent).

**Sequence E2E :**
```
load_config() → svgwrite.Drawing() → draw_*() series → dwg.save() → render_png()
                                                                        ├── Playwright HTML wrapper → full_png
                                                                        └── Pillow resize LANCZOS → delivery_png
```

---

## P10: Multi-resolution

**Principe :** Le meme contenu est rendu a plusieurs resolutions pour differents usages, depuis une source vectorielle unique.

**Raison :** Le SVG est la source de verite (scalable, editable, versionnable). Le full-res PNG est le rendu de reference. Le delivery PNG est le livrable final, dimensionne et marque 600 DPI pour la soumission MDPI.

**Resolutions :**

| Artefact | Dimensions | Usage |
|----------|------------|-------|
| SVG | 3300x1680 viewBox | Source de verite, edition |
| Full PNG | ~2200x1120 effectif (device_scale_factor=2 sur 1100x560 viewport) | Reference visuelle haute-res |
| Delivery PNG | 1100x560 px, 600 DPI metadata | Soumission MDPI |

**Flux :** SVG → Playwright (viewport=delivery, scale=2x) → full PNG → Pillow LANCZOS resize → delivery PNG. Le delivery est TOUJOURS derive du full, jamais directement du SVG.

---

## P11: Archivage versionne (Versioned Archival)

**Principe :** Ne jamais ecraser un artefact existant. Chaque iteration est archivee avec un identifiant de version.

**Raison :** Pouvoir revenir a n'importe quelle iteration pour comparer, diagnostiquer une regression, ou presenter l'evolution a Aurore. L'historique visuel est aussi important que l'historique de code.

**Application :** Les 3 fichiers du triplet sont copies dans `artefacts/wireframes/` apres chaque iteration reussie. Si un fichier vN existe deja, le pipeline ne l'ecrase pas — il cree vN+1.

**Hygiene :** Le nommage actuel utilise `wireframe_GA_v10.*`. Pour des iterations au sein de V10, le suffixe `_iterN` ou un timestamp peut etre ajoute. L'important est l'invariant: apres une execution, les fichiers precedents sont toujours la.

---

## P-PIP1: Playwright HTML Wrapper

**Principe :** Le rendu SVG → PNG passe par un fichier HTML intermediaire qui enveloppe le SVG dans un `<img>` avec des dimensions CSS explicites.

**Raison :** Le rendu SVG direct dans Playwright timeout a 3300x1680 (trop grand). La solution est de rendre a la taille delivery (1100x560) avec `device_scale_factor=2`, ce qui donne un PNG de ~2200x1120 pixels effectifs — equivalent a un rendu full-res sans le timeout.

**Implementation :**
```
1. Creer _render_v10.html avec <img src="file:///...svg" width=dw height=dh>
2. Playwright lance Chromium headless
3. Viewport = 1100x560, device_scale_factor = 2
4. Screenshot → full_png (~2200x1120)
5. Supprimer _render_v10.html
```

**Bug historique :** svglib (la methode precedente) produisait des PNGs blancs de 4 KB. L'approche Playwright HTML wrapper a resolu ce probleme definitivement.

---

## P-PIP2: Config-Driven Generation

**Principe :** Tout parametre visuel est lu depuis les 3 YAML configs. Aucune valeur hard-codee dans le script de generation (sauf `random.seed(42)`).

**Raison :** Permet de modifier la palette, le layout, ou le contenu textuel sans toucher au code. Rend le pipeline reutilisable pour d'autres missions SciSense.

**Configs :**
- `palette.yaml` — couleurs (produits, bandes, virus, fond, gradient)
- `layout_v10.yaml` — geometrie (canvas, bronchus, bands, zones, positions)
- `content.yaml` — texte (labels, budget mots)

**Contrainte :** Si une couleur, une position, ou un label est visible dans le SVG, il DOIT venir d'un YAML. Si on le trouve hard-code dans le script, c'est un bug.

---

## P-PIP3: Fail Loud sur Rendu

**Principe :** Si le rendu PNG echoue, le pipeline affiche le message d'erreur complet et ne pretend pas que tout va bien. Le SVG reste disponible pour diagnostic.

**Raison :** Un fichier PNG blanc ou absent est pire qu'une erreur visible. L'erreur silencieuse est le pire ennemi d'un pipeline iteratif — on continue a iterer sur un rendu casse sans le savoir.

**Implementation actuelle :** Le `try/except` dans `render_png()` catch l'exception et print le message. Le SVG est deja sauve avant l'appel a `render_png()`. C'est un compromis: on ne crash pas le pipeline entier, mais on signale clairement l'echec du rendu.

**Amelioration possible :** Retourner un code de sortie non-zero si le rendu echoue, pour que les scripts appelants puissent detecter l'echec automatiquement.
