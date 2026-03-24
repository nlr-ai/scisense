# Health — Mission Immunomodulateur GA

4 health checkers, mapping 1:1 avec les 4 results.

```
R1 (GA conforme MDPI)     ← H1 (checklist conformité auto)  ← S1a-S1f (6 sense signals)
R2 (validé par Aurore)    ← H2 (sign-off explicite)         ← S2 (question directe Aurore)
R3 (124 refs complètes)   ← H3 (count + format)             ← S3a-S3c (3 sense signals)
R4 (acceptation Mindy Ma) ← H4 (tracking email)             ← S4 (suivi post-soumission)
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

### Palette sub-check (inclus dans H1)

Les 4 couleurs produits dans le SVG correspondent exactement à la palette GA_SPEC.md. Grep dans le SVG pour les hex codes attendus : #2563EB, #0D9488, #7C3AED, #059669 (B5, P7).

**Checker:** Script `validate_ga.py` (I6, à implémenter). Avant chaque présentation à Aurore, le script valide S1a-S1c automatiquement. S1d-S1f nécessitent revue humaine. Si un check échoue → Fail Loud, pas de présentation.

**Carrier:** Silas (auto-check S1a-S1c) + Aurore (revue S1d-S1f).

**Status:** Loop partiellement ouverte — script non implémenté. Checks manuels pour l'instant.

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

## H5: Pipeline de rendu E2E → validates V8, V9, P8, P10

Chaque itération produit 3 fichiers. Si l'un est manquant ou corrompu, Fail Loud.

### Sense signals

| ID | Signal | Checks | Automation |
|----|--------|--------|------------|
| S5a | SVG non-vide | Fichier > 1 KB, parseable XML | Auto — `xml.etree.ElementTree.parse()` |
| S5b | PNG full res correct | Dimensions = 3300×1680, fichier > 50 KB | Auto — Pillow `Image.open().size` |
| S5c | PNG delivery correct | Dimensions = 1100×560, fichier > 5 KB, PAS blanc | Auto — Pillow size + mean pixel > 10 |
| S5d | Palette présente | Les 4 hex (#2563EB, #0D9488, #7C3AED, #059669) dans le SVG | Auto — grep |
| S5e | Archivé sans écrasement | Fichiers vN dans artefacts/wireframes/, pas de vN-1 modifié | Auto — file exists check |
| S5f | Config coherence | palette.yaml colors match GA_SPEC.md palette section | Auto — yaml parse + compare |
| S5g | Asset injection | All assets referenced in layout.yaml exist in assets/ | Auto — file exists check |
| S5h | Word count from source | Count words in content.yaml = same as count in rendered SVG | Auto — yaml parse |

**Checker:** Intégré dans A5 (pipeline de rendu). Chaque step valide le précédent. Si S5c fail → utiliser Pillow resize au lieu de svglib (workaround bug v3).

**Carrier:** Silas (tout automatisable).

**Status:** Partiellement implémenté dans A5. Script `validate_ga.py` (I6) consolidera tous les checks.

---

## Open loops / Escalations

| Loop | Missing link | What's needed | Who |
|------|-------------|---------------|-----|
| H1 → R1 | Script `validate_ga.py` non implémenté (I6) | Écrire le script qui automatise S1a-S1c | Silas |
| H1 → R1 | S1d (non-redondance) semi-auto | Revue visuelle par Aurore une fois le GA prêt | Aurore |
| H1 → R1 | S1e (droits visuels) manuel | Checklist de provenance de chaque élément visuel | Silas |
| H1 → R1 | S1f (lisibilité) semi-auto | Fix du rendu delivery 1100×560 (bug connu svglib) | Silas |
| H2 → R2 | GA pas encore présenté | Finaliser wireframe via A2 puis présenter à Aurore | Silas + Aurore |
| H4 → R4 | Soumission non effectuée | Nécessite R1+R2+R3 PASS d'abord | Aurore |

## Bug connu

Le rendu delivery (1100×560) via svglib est cassé dans v3 (fichier de 4 KB, blanc). Cause probable : svglib ne scale pas correctement certains éléments SVG. Bloque S1f. À investiguer avant de lancer la boucle A2.
