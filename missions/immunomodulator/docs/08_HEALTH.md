# Health — Mission Immunomodulateur GA

8 health checkers: 4 mapping 1:1 avec les 4 results + 4 checkers de processus et comportement.

```
R1 (GA conforme MDPI)     ← H1 (checklist conformité auto)  ← S1a-S1g (7 sense signals)
R2 (validé par Aurore)    ← H2 (sign-off explicite)         ← S2 (question directe Aurore)
R3 (124 refs complètes)   ← H3 (count + format)             ← S3a-S3c (3 sense signals)
R4 (acceptation Mindy Ma) ← H4 (tracking email)             ← S4 (suivi post-soumission)
Pipeline E2E              ← H5 (rendu complet)              ← S5a-S5h (8 sense signals)
Audit NotebookLM          ← H6 (cycle audit)                ← S6a-S6d (4 sense signals)
Convergence IgA (B8)      ← H7 (vérification visuelle)      ← S7a-S7b (2 sense signals)
Cycle fracture (B4)       ← H8 (vérification visuelle)      ← S8a-S8b (2 sense signals)
```

---

## H1: GA conforme MDPI → validates R1

Le GA passe les 8 règles MDPI. Automatisable à 80%.

### Sense signals

| ID | Signal | Checks | Automation |
|----|--------|--------|------------|
| S1a | Dimensions PNG | ≥ 560×1100 px (V1) | Auto — Pillow `Image.open().size` |
| S1b | Word count SVG | ≤ 30 mots dans les `<text>` elements (V3) | Auto — parse SVG, count words |
| S1c | Texte interdit absent | Pas de titres, affiliations, citations (V2) | Auto — regex dans SVG |
| S1d | Non-redondance Fig1/Fig2 | Pas de flux vertical ni quadrants A/B/C/D (V4) | Semi-auto — structure SVG, revue Aurore |
| S1e | Droits visuels | Tout original ou sous licence libre, pas d'IA (V6, VN4) | Manuel — checklist à signer |
| S1f | Lisibilité 50% zoom | Labels lisibles à 550×280 px (V7) | Semi-auto — downscale et vérification visuelle |
| S1g | Pas de heading "Graphical Abstract" | Aucun texte titre/heading dans le rendu (ajouté V10) | Auto — regex dans SVG |

### Palette sub-check (inclus dans H1)

Les 4 couleurs produits dans le SVG correspondent exactement à la palette GA_SPEC.md. Grep dans le SVG pour les hex codes attendus : #2563EB, #0D9488, #7C3AED, #059669 (B5, P7).

**Checker:** Script `validate_ga.py` (IMPLÉMENTÉ). Avant chaque présentation à Aurore, le script valide S1a-S1c + S1g automatiquement. S1d-S1f nécessitent revue humaine. Si un check échoue → Fail Loud, pas de présentation.

**Carrier:** Silas (auto-check S1a-S1c, S1g) + Aurore (revue S1d-S1f).

**Status:** Loop partiellement fermée — script validate_ga.py implémenté et fonctionnel. Checks S1d-S1f restent manuels.

---

## H2: Validation scientifique Aurore → validates R2

Aurore confirme explicitement que le GA encode correctement les 4 messages clés, la hiérarchie des preuves (V5), et que les métaphores (P3) ne trahissent pas la science.

### Sense signal

| ID | Signal | Method |
|----|--------|--------|
| S2 | Sign-off explicite d'Aurore | Question directe : "Les 4 messages clés sont-ils correctement représentés ? La hiérarchie des preuves est-elle exacte ?" Réponse attendue : oui/non + corrections. |

**Checker:** Réponse explicite d'Aurore (pas de silence interprété comme accord). Si corrections → retour à A1 (boucle itération).

**Carrier:** Aurore.

**Status:** Loop ouverte — GA pas encore présenté à Aurore.

---

## H3: Références complètes → validates R3

Les 124 références sont extraites, formatées, complètes et sans doublons.

### Sense signals

| ID | Signal | Checks | Automation |
|----|--------|--------|------------|
| S3a | Count = 124 | `wc -l extracted_references.txt` | Auto |
| S3b | Format MDPI Vancouver | Structure cohérente par ref | Semi-auto — regex pattern match |
| S3c | Pas de doublons | Aucune ref identique ou quasi-identique | Auto — comparaison texte |

**Checker:** Script simple (count + dedup check). Déjà vérifié manuellement.

**Carrier:** Silas.

**Status:** PASS. Fichier `extracted_references.txt` prêt, 124 refs vérifiées.

---

## H4: Acceptation Mindy Ma → validates R4

L'éditrice accepte les livrables sans révision et fait avancer le manuscrit vers le peer-review.

### Sense signal

| ID | Signal | Method |
|----|--------|--------|
| S4 | Email de confirmation | Suivi email post-soumission. Aurore forward ou confirme. |

**Checker:** Email de Mindy Ma (ou absence de demande de révision après 2 semaines).

**Carrier:** Aurore (contact direct avec l'éditrice).

**Status:** Loop ouverte — soumission pas encore effectuée. Dépend de R1+R2+R3 PASS.

---

## H5-H9: VEC Engine Health Checks

These health checkers are now maintained in the VEC module doc chain:
- H5 (Pipeline E2E) → `docs/vec/pipeline/08_HEALTH.md`
- H6 (Audit NotebookLM) → `docs/vec/audit/08_HEALTH.md`
- H7 (Convergence IgA) → `docs/vec/design_system/08_HEALTH.md`
- H8 (Cycle fracture) → `docs/vec/design_system/08_HEALTH.md`
- H9 (Premier Regard) → `docs/vec/audit/08_HEALTH.md`

---

## Open loops / Escalations

| Loop | Missing link | What's needed | Who | Status |
|------|-------------|---------------|-----|--------|
| H1 → R1 | Script `validate_ga.py` | Automatise S1a-S1c + S1g | Silas | **IMPLÉMENTÉ** |
| H1 → R1 | S1d (non-redondance) semi-auto | Revue visuelle par Aurore une fois le GA prêt | Aurore | Ouvert |
| H1 → R1 | S1e (droits visuels) manuel | Checklist de provenance de chaque élément visuel | Silas | Ouvert |
| H1 → R1 | S1f (lisibilité) semi-auto | Vérification à 550×280 (bug svglib résolu, pipeline Playwright ok) | Silas | Ouvert |
| H2 → R2 | GA pas encore présenté | Finaliser wireframe via A2 puis présenter à Aurore | Silas + Aurore | Ouvert |
| H4 → R4 | Soumission non effectuée | Nécessite R1+R2+R3 PASS d'abord | Aurore | Ouvert |
| H6 → A9 | Cycle audit NotebookLM | Export S0N/, upload, audit, intégration corrections | Silas + NotebookLM | Ouvert |
| H7 → B8 | Convergence IgA non vérifiée | 4 lignes colorées + formes Y dans lumen | Silas + NotebookLM | Ouvert |
| H8 → B4 | Cycle fracture non vérifiée | Lance verte brise cycle rouge + marques fracture | Silas + Aurore | Ouvert |

## Bug résolu (anciennement "Bug connu")

~~Le rendu delivery (1100×560) via svglib est cassé dans v3 (fichier de 4 KB, blanc).~~ **Résolu:** Migration de svglib vers Playwright HTML wrapper. Le SVG est enveloppé dans un HTML minimal et rendu via Playwright à la taille de livraison avec 2x device_scale_factor. Le timeout Playwright à 3300x1680 a été contourné par cette approche.
