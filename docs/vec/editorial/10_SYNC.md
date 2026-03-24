# SYNC — vec/editorial

**Module:** vec/editorial — Tribunal editorial MDPI
**Version:** 1.0.0
**Date:** 2026-03-24
**Author:** Silas (b2d65910b3daa7fd)

---

## Etat courant

| Facet | Fichier | Statut |
|-------|---------|--------|
| RESULTS | 01_RESULTS.md | Complet |
| OBJECTIVES | 02_OBJECTIVES.md | Complet |
| PATTERNS | 03_PATTERNS.md | Complet |
| BEHAVIORS | 04_BEHAVIORS.md | Complet |
| ALGORITHM | 05_ALGORITHM.md | Complet |
| VALIDATION | 06_VALIDATION.md | Complet |
| IMPLEMENTATION | 07_IMPLEMENTATION.md | Complet |
| HEALTH | 08_HEALTH.md | Complet |
| PHENOMENOLOGY | 09_PHENOMENOLOGY.md | Complet |
| SYNC | 10_SYNC.md | Actif |

### Guarantee Loop

```
RESULT: GA passe 7+ checks MDPI (S1a-S1g all PASS)
  → SENSE: validate_ga.py (automatique, exit code 0/1)
    → HEALTH: H1 — S1a-S1g toutes PASS
      → CARRIER: Silas (script exécuté avant toute présentation à Aurore)
```

**Loop status:** Fermée pour S1a, S1b, S1c, S1d (palette), S1e (no GA heading), S1g. Ouverte pour S1d (non-redondance Fig1/Fig2, semi-auto), S1e (droits visuels, manuel), S1f (lisibilité 50%, semi-auto).

### Script

| Script | Chemin | Statut |
|--------|--------|--------|
| validate_ga.py | `missions/immunomodulator/scripts/validate_ga.py` | Implémenté, fonctionnel |

### Dépendances

- Module `vec/pipeline` fournit les fichiers SVG + PNG à valider
- Module `vec/design_system` fournit la palette de référence
- `config/palette.yaml`, `config/content.yaml` — sources de vérité pour palette et budget texte

---

## Historique

| Date | Version | Changement |
|------|---------|-----------|
| 2026-03-24 | 0.1.0 | Création initiale du doc chain (10_SYNC.md en premier). |
| 2026-03-24 | 1.0.0 | Doc chain complet — 10/10 facets écrits. Script validate_ga.py déjà implémenté et documenté. Guarantee Loop fermée pour 5/7 checks auto, ouverte pour 2 checks semi-auto (S1f lisibilité, S1e droits). |

---

## Remarques / Questions

*(Section de travail — observations, questions ouvertes, points à clarifier)*

1. Le mapping S1d dans HEALTH.md de la mission (08_HEALTH.md) désigne "non-redondance Fig1/Fig2" mais dans validate_ga.py le check S1d est implémenté comme "palette check". L'architecture actuelle est correcte : la palette est automatisable, la non-redondance est un jugement humain (Aurore). La numérotation diverge entre le doc mission et le script — le doc mission est la référence canonique, le script a renuméroté pour regrouper les checks auto.

2. Le check S1f (lisibilité 50% zoom) n'a pas d'automatisation dans validate_ga.py. Une heuristique serait possible (downscale à 550x280 + OCR ou taille de font minimale dans le SVG) mais le coût de faux positifs dépasse le bénéfice. Reste semi-auto : Silas vérifie visuellement.

3. Le check S1e (droits visuels / provenance) ne peut jamais être automatisé — il nécessite un jugement sur la source de chaque élément visuel. Le fichier `artefacts/PROVENANCE.md` est la source de vérité.

---

## Consignes recues

*(Section pour instructions live de NLR ou Aurore — vérifier périodiquement)*

*(vide)*
