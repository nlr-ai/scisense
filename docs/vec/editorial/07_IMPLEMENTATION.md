# IMPLEMENTATION — vec/editorial

**Module:** vec/editorial — Tribunal editorial MDPI

---

## Carte des fichiers

| Fichier | Role | Lignes | Dependances |
|---------|------|--------|-------------|
| `missions/immunomodulator/scripts/validate_ga.py` | Script principal — tribunal editorial | ~620 | Python 3.10+ stdlib (xml, re, argparse, pathlib, os, sys). Pillow optionnel (S1a PNG dims). |
| `missions/immunomodulator/config/palette.yaml` | Source de verite pour la palette couleurs | ~30 | Lu par validate_ga.py via _load_yaml_simple |
| `missions/immunomodulator/config/content.yaml` | Source de verite pour le budget texte et les labels | ~40 | Lu par validate_ga.py pour S5h (content sync) |
| `missions/immunomodulator/artefacts/PROVENANCE.md` | Registre de provenance des elements visuels | variable | Consulte manuellement pour S1e (droits visuels) |

---

## Architecture du script

### Constantes (hardcodees — regles MDPI universelles)

```python
WORD_BUDGET = 30                  # Regle MDPI R3
EXPECTED_RATIO = (3300, 1680)     # viewBox a 3x (regle MDPI R8)
DELIVERY_DIMS = (1100, 560)       # Dimensions de livraison
MIN_FILE_SIZE = 5 * 1024          # 5 KB minimum par fichier
```

### Constantes (hardcodees — specifiques mission immunomodulateur)

```python
PRODUCT_COLORS = {                # Les 4 produits et leurs hex
    "#2563EB": "OM-85",
    "#0D9488": "PMBL",
    "#7C3AED": "MV130",
    "#059669": "CRL1505",
}

ALLOWED_COLORS = { ... }          # 25+ couleurs autorisees (produits, fonds, texte, virus, etc.)

FORBIDDEN_PATTERNS = [ ... ]      # 14 regex patterns (et al., DOI, affiliations, etc.)
```

**Note pour la reutilisation VEC :** Pour une autre mission, les `PRODUCT_COLORS` et `ALLOWED_COLORS` devront etre externalises dans un YAML mission-specifique. Les `FORBIDDEN_PATTERNS` et le `WORD_BUDGET` sont universels MDPI et restent hardcodes.

### Fonctions

| Fonction | Responsabilite | Entree | Sortie |
|----------|---------------|--------|--------|
| `validate()` | Orchestrateur — execute tous les checks | svg_path, [png paths], [config_dir] | `(bool, str)` |
| `check_s1a_geometry()` | Ratio viewBox + dimensions PNG | tree, delivery_png_path | `(status, detail)` |
| `check_s1b_word_budget()` | Comptage de mots SVG | text_elements | `(status, detail, word_count)` |
| `check_s1c_no_titles()` | Patterns interdits (V2) | text_elements | `(status, detail)` |
| `check_s1d_palette()` | Couleurs produit + couleurs non autorisees | tree, config_dir | `(status, detail)` |
| `check_s1e_no_ga_heading()` | Heading "Graphical Abstract" interdit | text_elements | `(status, detail)` |
| `check_s5a_files()` | Existence et taille des 3 fichiers | svg_path, png paths | `(status, detail)` |
| `check_s5h_content_sync()` | Coherence content.yaml vs SVG | text_elements, word_count, config_dir | `(status, detail)` |
| `_extract_text_elements()` | Parse SVG, extrait tous les <text> | tree | `list[(content, raw)]` |
| `_extract_colors_from_svg()` | Parse SVG, extrait fill/stroke/style colors | tree | `set[str]` |
| `_count_words()` | Comptage semantique de mots | text | `int` |
| `_normalize_color()` | Normalise hex/noms CSS | color | `str` |
| `_load_yaml_simple()` | Parseur YAML minimal sans PyYAML | path | `dict` |
| `_format_report()` | Mise en forme du rapport tribunal | results dict | `str` |
| `main()` | CLI entry point, argparse | argv | exit 0/1 |

---

## Dependances

### Runtime

| Dependance | Version | Usage | Obligatoire |
|-----------|---------|-------|-------------|
| Python | >= 3.10 | Type hints `str \| None`, standard lib | Oui |
| xml.etree.ElementTree | stdlib | Parse SVG | Oui |
| re | stdlib | Forbidden patterns, color extraction | Oui |
| Pillow (PIL) | >= 9.0 | Verification dimensions PNG (S1a) | Non — si absent, S1a PNG check est FAIL avec message explicite |

### Pas de dependance a

- PyYAML (remplace par `_load_yaml_simple`)
- lxml (remplace par `xml.etree.ElementTree`)
- svglib (etait utilise dans le pipeline de rendu, pas dans le validateur)
- Playwright (utilise dans le pipeline de rendu, pas dans le validateur)

---

## Points d'integration

### Avec vec/pipeline (compose_ga_v10.py)

Le pipeline produit les 3 fichiers. Le validateur les consomme. Pas de couplage code — le contrat est le filesystem :

```
artefacts/wireframes/wireframe_GA_v{N}.svg
artefacts/wireframes/wireframe_GA_v{N}_full.png
artefacts/wireframes/wireframe_GA_v{N}_delivery.png
```

### Avec vec/audit (export_notebooklm.py)

L'export NotebookLM n'est autorise qu'apres un PASS editorial. Pas de couplage code — c'est une procedure Silas (VP1).

### Avec vec/design_system

La palette de reference vit dans `config/palette.yaml`. Le validateur la charge pour la coherence. Le design system definit les couleurs ; le validateur les verifie.

---

## Extension pour d'autres missions

Pour reutiliser `validate_ga.py` sur un futur GA SciSense :

1. Creer un `config/palette.yaml` specifique a la mission
2. Creer un `config/content.yaml` specifique
3. Externaliser `PRODUCT_COLORS` et `ALLOWED_COLORS` dans un YAML charge au runtime
4. Les `FORBIDDEN_PATTERNS`, `WORD_BUDGET`, `EXPECTED_RATIO`, `DELIVERY_DIMS` restent hardcodes (regles MDPI)
5. Ajouter un argument CLI `--mission-config` pour pointer vers le YAML mission

Ce refactoring n'est pas fait aujourd'hui — YAGNI. Il sera fait quand la deuxieme mission GA arrivera.
