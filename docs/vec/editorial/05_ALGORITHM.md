# ALGORITHM — vec/editorial

**Module:** vec/editorial — Tribunal editorial MDPI

---

## A1: Flux principal — validate_ga.py

```
ENTREE: svg_path, [full_png_path], [delivery_png_path], [config_dir]
        │
        ├─ Resoudre les chemins absolus
        ├─ Auto-detecter les PNG si non fournis (nom_svg + _full.png / _delivery.png)
        ├─ Auto-detecter config_dir si non fourni (../config/ relatif au script)
        │
        ▼
PARSE SVG
        │
        ├─ xml.etree.ElementTree.parse(svg_path)
        ├─ Si ParseError → tous les checks = FAIL, rapport SVG parse error, exit 1
        │
        ▼
EXTRAIRE textes (une seule fois)
        │
        ├─ Parcourir tous les elements de l'arbre
        ├─ Filtrer sur tag == "text" (avec ou sans namespace SVG)
        ├─ Pour chaque <text> : collecter itertext() + tostring()
        ├─ Resultat : list[(content: str, raw_xml: str)]
        │
        ▼
EXECUTER 7 CHECKS (sequentiels, pas de court-circuit)
        │
        ├─ S1a: check_s1a_geometry(tree, delivery_png_path)
        │     ├─ Lire viewBox ou width/height du SVG
        │     ├─ Calculer ratio, comparer a 3300/1680 = 1.9643
        │     ├─ Si delivery_png_path fourni et existant :
        │     │     ├─ Pillow Image.open().size
        │     │     └─ Comparer a (1100, 560)
        │     └─ Resultat: PASS/FAIL + detail
        │
        ├─ S1b: check_s1b_word_budget(text_elements)
        │     ├─ Pour chaque texte : remplacer "/" par espace, split, filtrer symboles purs
        │     ├─ Sommer les mots
        │     ├─ Comparer a WORD_BUDGET (30)
        │     └─ Resultat: PASS/FAIL + total/budget + svg_word_count (pour S5h)
        │
        ├─ S1c: check_s1c_no_titles(text_elements)
        │     ├─ Pour chaque texte : tester contre 14 FORBIDDEN_PATTERNS (regex)
        │     │     Patterns: et al., DOI, affiliation, universit*, reference,
        │     │     citation, annee;, Figure N, Dr., PhD, M.D., Institut*,
        │     │     Department, Hospital
        │     ├─ Collecter toutes les violations
        │     └─ Resultat: PASS/FAIL + liste des violations
        │
        ├─ S1d: check_s1d_palette(tree, config_dir)
        │     ├─ Extraire toutes les couleurs du SVG (fill, stroke, style)
        │     ├─ Normaliser (hex majuscules, noms minuscules)
        │     ├─ Verifier que les 4 couleurs produit sont presentes
        │     ├─ Verifier qu'aucune couleur n'est hors de la liste ALLOWED_COLORS
        │     ├─ Couleurs non reconnues → WARN (pas FAIL)
        │     └─ Resultat: PASS/WARN/FAIL + detail
        │
        ├─ S1e: check_s1e_no_ga_heading(text_elements)
        │     ├─ Regex: /graphical\s+abstract/i
        │     ├─ Scanner tous les textes
        │     └─ Resultat: PASS/FAIL + detail
        │
        ├─ S1f: (non implemente dans le script — semi-auto)
        │     └─ Verification visuelle par Silas : downscale a 550x280, lire a l'oeil
        │
        ├─ S1g: (couvert par S1c — les forbidden patterns incluent Figure N, Dr., etc.)
        │     └─ Pas de fonction separee, integre dans check_s1c_no_titles
        │
        ├─ S5a: check_s5a_files(svg_path, full_png_path, delivery_png_path)
        │     ├─ Pour chaque fichier : existe? > 5 KB?
        │     └─ Resultat: PASS/FAIL + tailles
        │
        └─ S5h: check_s5h_content_sync(text_elements, svg_word_count, config_dir)
              ├─ Charger content.yaml avec _load_yaml_simple
              ├─ Compter les mots dans le YAML
              ├─ Comparer au word count SVG (de S1b)
              └─ Resultat: PASS/FAIL + yaml_words vs svg_words

        │
        ▼
FORMATER RAPPORT
        │
        ├─ Header: "VALIDATE_GA -- Editorial Tribunal"
        ├─ Pour chaque check : label aligné + PASS/WARN/FAIL + detail
        ├─ Footer: VERDICT PASS (N/N) ou VERDICT FAIL (N/N)
        │
        ▼
RETOUR
        │
        ├─ all_passed = aucun FAIL (WARN acceptable)
        ├─ print(rapport) sur stdout
        └─ sys.exit(0 si passed, 1 sinon)
```

---

## A2: Parseur YAML minimal (_load_yaml_simple)

```
ENTREE: chemin fichier YAML
        │
        ├─ Pour chaque ligne :
        │     ├─ Ignorer lignes vides et commentaires (#)
        │     ├─ Calculer l'indentation
        │     ├─ Si commence par "- " → element de liste → ajouter a current_list
        │     ├─ Si contient ":" :
        │     │     ├─ Separer key: value
        │     │     ├─ Retirer commentaires inline (  #)
        │     │     ├─ Retirer quotes
        │     │     ├─ Si value vide → section header → creer liste/dict
        │     │     └─ Si value non vide :
        │     │           ├─ Si indent > 0 et section courante → nested → dict[key] = val
        │     │           └─ Sinon → top-level → result[key] = val
        │
        └─ Retour: dict
```

---

## A3: Extraction des couleurs SVG

```
ENTREE: arbre SVG (ElementTree)
        │
        ├─ Pour chaque element de l'arbre :
        │     ├─ Lire attributs "fill" et "stroke" → ajouter au set
        │     ├─ Lire attribut "style" → regex pour fill:/stroke: → ajouter au set
        │
        └─ Retour: set[str] de couleurs brutes
```

---

## A4: Invocation en ligne de commande

```bash
# Usage minimal (SVG seul, PNG auto-detectes)
python validate_ga.py path/to/wireframe.svg

# Usage complet
python validate_ga.py path/to/wireframe.svg \
    --full-png path/to/wireframe_full.png \
    --delivery-png path/to/wireframe_delivery.png \
    --config-dir path/to/config/

# Usage programmatique (depuis un autre script)
from validate_ga import validate
passed, report = validate("wireframe.svg", config_dir="config/")
```

---

## A5: Sequence d'integration dans le pipeline VEC

```
compose_ga_v10.py produit SVG + PNG
        │
        ▼
validate_ga.py juge les artefacts     ◄── CE MODULE
        │
        ├─ FAIL → retour au compositeur, corriger
        │
        ├─ PASS → avancer vers l'audit
        │           │
        │           ├─ Checks semi-auto (S1d non-redondance, S1f lisibilite)
        │           │     par Silas (verification visuelle)
        │           │
        │           ├─ Check manuel (S1e provenance / droits)
        │           │     par Silas (checklist PROVENANCE.md)
        │           │
        │           └─ Si tout OK → export_notebooklm.py → audit NLM → Aurore
        │
        └─ Le validateur ne touche JAMAIS les artefacts
```
