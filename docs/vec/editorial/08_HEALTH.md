# HEALTH — vec/editorial

**Module:** vec/editorial — Tribunal editorial MDPI

---

## Guarantee Loop

```
RESULT: GA passe 7+ checks MDPI (R1)
  → SENSE: validate_ga.py exit code + rapport (S1a-S1g)
    → HEALTH: H1 — tous les sense signals PASS
      → CARRIER: Silas (script automatique + verification visuelle semi-auto)
```

---

## H1: Conformite editoriale MDPI → validates R1

Le GA passe les 7 checks editoriaux. 5 checks automatises, 2 semi-auto.

### Sense signals

| ID | Signal | Invariant | Checks | Automation | Status |
|----|--------|-----------|--------|------------|--------|
| S1a | Geometry | V1 | viewBox ratio = 3300/1680 = 1.9643. PNG delivery = 1100x560. | Auto — `check_s1a_geometry()`. Pillow pour PNG. | Implemente |
| S1b | Word Budget | V3 | Total mots dans `<text>` <= 30. Comptage semantique (/ = separateur, symboles ignores). | Auto — `check_s1b_word_budget()` | Implemente |
| S1c | No Titles | V2 | 14 regex patterns interdits. Zero match = PASS. | Auto — `check_s1c_no_titles()` | Implemente |
| S1d | Palette | B5, P7 | 4 couleurs produit presentes (#2563EB, #0D9488, #7C3AED, #059669). Couleurs non reconnues → WARN. | Auto — `check_s1d_palette()` | Implemente |
| S1e | No GA Heading | VN1 | Regex `/graphical\s+abstract/i`. Zero match = PASS. | Auto — `check_s1e_no_ga_heading()` | Implemente |
| S1f | Lisibility 50% | V7 | Labels lisibles a 550x280 px. Plus petit caractere >= 8pt a la taille de livraison. | Semi-auto — downscale visuel par Silas | Non automatise |
| S1g | Forbidden Patterns | V2, V6 | Patterns supplementaires (Figure N, Dr., PhD, etc.). Integre dans S1c. | Auto — couvert par `check_s1c_no_titles()` | Implemente |

### Checks supplementaires (pipeline, non editoriaux mais executes dans le meme script)

| ID | Signal | Checks | Automation | Status |
|----|--------|--------|------------|--------|
| S5a | Files Exist | SVG + 2 PNG existent et > 5 KB | Auto — `check_s5a_files()` | Implemente |
| S5h | Content Sync | Word count content.yaml == word count SVG | Auto — `check_s5h_content_sync()` | Implemente |

### Palette sub-check (inclus dans S1d)

Les 4 hex produit dans le SVG correspondent exactement a la palette definie. Extraction via `_extract_colors_from_svg()` (attributs fill/stroke + style inline). Normalisation avant comparaison.

---

## Checker

**Script :** `missions/immunomodulator/scripts/validate_ga.py`

**Protocole d'execution :**
1. Le compositeur (`compose_ga_v10.py`) produit SVG + PNG
2. Silas execute `python validate_ga.py wireframe_GA_vN.svg --config-dir ../config/`
3. Si exit code 0 → PASS → Silas procede aux checks semi-auto (S1f lisibilite, S1e droits)
4. Si exit code 1 → FAIL → Silas lit le rapport, corrige dans le compositeur/config, relance
5. Si tous les checks (auto + semi-auto + manuel) sont PASS → GA autorise pour presentation a Aurore

**Frequence :** A chaque iteration du pipeline, avant toute presentation ou soumission.

---

## Carrier

| Scope | Carrier | Responsabilite |
|-------|---------|---------------|
| Checks auto (S1a-S1e, S1g, S5a, S5h) | Silas (script) | Executer le script, lire le rapport, corriger les echecs |
| Check semi-auto S1f (lisibilite) | Silas (visuel) | Downscaler le PNG a 550x280, verifier que les labels sont lisibles |
| Check semi-auto S1d mission (non-redondance) | Aurore | Confirmer que le GA ne reproduit ni Fig1 ni Fig2 |
| Check manuel S1e mission (droits visuels) | Silas | Verifier PROVENANCE.md : chaque element visuel a une source documentee, libre de droits |

---

## Loops ouvertes

| Loop | Lien manquant | Ce qu'il faut | Qui | Status |
|------|--------------|---------------|-----|--------|
| S1f → V7 | Automatisation lisibilite | Heuristique taille de font minimale dans SVG ou OCR apres downscale | Silas | Ouvert — couteux en faux positifs, reste semi-auto |
| S1e mission → V6 | Verification provenance automatisee | Script qui parse PROVENANCE.md et verifie que chaque fichier SVG reference a une entree | Silas | Ouvert — valeur ajoutee faible vs. effort |
| Palette YAML → script | PRODUCT_COLORS et ALLOWED_COLORS hardcodes | Externaliser dans palette.yaml pour reutilisation multi-mission | Silas | YAGNI — a faire quand 2e mission arrive |

---

## Diagnostic : que faire quand un check echoue

| Check | Cause frequente | Action corrective |
|-------|----------------|-------------------|
| S1a FAIL | viewBox modifie manuellement ou resize incorrect | Verifier layout_v10.yaml dimensions. Regenerer le SVG. |
| S1b FAIL | Trop de labels ajoutes dans content.yaml | Reduire les labels a 1-2 mots. Supprimer les labels redondants avec les icones. |
| S1c FAIL | Texte copie-colle du manuscrit dans le SVG | Supprimer le texte incrimine dans content.yaml. |
| S1d FAIL (missing) | Couleur produit manquante dans le SVG | Verifier compose_ga_v10.py — le produit est-il rendu ? La couleur est-elle correcte dans palette.yaml ? |
| S1d WARN (unknown) | Nouvelle couleur decorative ajoutee | Verifier si la couleur est legitime. Si oui, l'ajouter a ALLOWED_COLORS. Si non, la retirer du SVG. |
| S1e FAIL | Heading "Graphical Abstract" ajoute | Supprimer le heading dans content.yaml ou le compositeur. |
| S5a FAIL | PNG non genere ou corrompu | Relancer le pipeline de rendu (compose_ga_v10.py). Verifier Playwright. |
| S5h FAIL | content.yaml desynchronise du SVG | Le compositeur n'injecte pas tous les labels de content.yaml, ou en ajoute des extras. Synchroniser. |
