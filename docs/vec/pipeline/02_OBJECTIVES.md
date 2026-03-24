# OBJECTIVES — vec/pipeline

## O1: Ce que le module fait

Le pipeline transforme 3 fichiers YAML de configuration en 3 artefacts visuels (SVG + 2 PNGs) de maniere deterministe, reproductible et verifiable.

**Entree :**
- `config/layout_v10.yaml` — geometrie, positions, tailles
- `config/palette.yaml` — couleurs (bandes, produits, fond, virus)
- `config/content.yaml` — labels textuels, budget mots

**Sortie :**
- `wireframe_GA_v10.svg` — source vectorielle, editable
- `wireframe_GA_v10_full.png` — raster haute resolution (rendu Playwright 2x)
- `wireframe_GA_v10_delivery.png` — raster livrable (1100x560, 600 DPI)

---

## O2: Objectifs

### O2a: Zero fichier corrompu

Chaque execution produit des fichiers valides ou echoue bruyamment. Pas de fichier blanc, pas de PNG de 4 KB, pas de SVG tronque. Le pipeline Fail Loud: si une etape echoue, l'erreur est remontee, pas avalee.

### O2b: Reproductibilite parfaite

Pour les memes configs YAML + les memes contours JSON, le pipeline produit le meme SVG (aux coordonnees aleatoires pres, fixees par `random.seed(42)`). Pas de dependance a l'etat global, pas d'effet de bord entre executions.

### O2c: Pipeline E2E, pas de rendu partiel

Chaque iteration execute la chaine complete: SVG generation → Playwright render → Pillow resize → archivage. Pas de shortcut, pas de "je genere juste le SVG et le PNG plus tard". La raison: un SVG sans son rendu PNG ne peut pas etre valide visuellement.

### O2d: Autonomie du rendu

Le pipeline ne depend pas de logiciels exterieurs manuels (pas de Inkscape CLI, pas de GIMP, pas de navigateur ouvert par l'utilisateur). Playwright est le moteur de rendu, lance programmatiquement. L'intervention humaine est zero pour la production des 3 fichiers.

### O2e: Mission-agnostic

Le pipeline est reutilisable pour tout futur GA SciSense. La mission (immunomodulateur) injecte sa science via les 3 YAML configs. Le pipeline injecte le process. Aucune logique scientifique hard-codee dans le pipeline — tout passe par les configs.

---

## O3: Non-objectifs (ce que le module ne fait PAS)

### O3a: Pas de validation editoriale

Le pipeline produit des fichiers. Il ne juge pas leur conformite MDPI (c'est `vec/editorial`, H1). Il verifie seulement que les fichiers sont non-corrompus et fideles aux configs.

### O3b: Pas de validation scientifique

Le pipeline ne verifie pas que le contenu est scientifiquement correct. C'est le role d'Aurore (H2) et de NotebookLM (H6).

### O3c: Pas de calibration organique

Le pipeline consomme des contours JSON pre-extraits. Il ne fait pas l'extraction de contours depuis des images IA — c'est `vec/calibration`.

### O3d: Pas de finition publication

Le pipeline produit des wireframes de travail. La finition publication (si necessaire via Inkscape/Figma) est hors scope — c'est une decision a prendre (A6, non tranchee).

---

## O4: Trade-offs explicites

| Choix | Alternative rejetee | Justification |
|-------|---------------------|---------------|
| Playwright HTML wrapper | svglib / cairosvg / rendu SVG direct Playwright | svglib produit des blancs; le rendu direct Playwright timeout a 3300x1680; le HTML wrapper avec device_scale_factor=2 resout les deux |
| Pillow resize depuis full res | Rendu direct a 1100x560 | Le resize LANCZOS depuis 2x donne un rendu net; rendre directement a la taille delivery perd en qualite |
| random.seed(42) | Pas de seed | La reproductibilite est plus importante que la variation aleatoire pour le debug et la regression |
| 600 DPI metadata | 300 DPI / pas de metadata | MDPI exige une qualite publication; 600 DPI est le standard medical imaging |
