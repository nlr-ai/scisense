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

**Checker:** Intégré dans A5 (pipeline de rendu via compose_ga_v10.py). Chaque step valide le précédent. Le rendu full res utilise Playwright HTML wrapper (SVG enveloppé dans HTML, rendu à la taille de livraison avec 2x device_scale_factor). Delivery via Pillow resize depuis le full res.

**Bug résolu:** Playwright timeout à 3300x1680 → résolu par HTML wrapper qui rend à la taille de livraison avec 2x device_scale_factor au lieu de rendre directement à la taille full.

**Carrier:** Silas (tout automatisable).

**Status:** Implémenté dans A5/A7 (compose_ga_v10.py). Script `validate_ga.py` consolidera tous les checks.

---

## H6: Audit NotebookLM cycle → validates A9

Chaque cycle d'audit NotebookLM produit un rapport exploitable et les corrections sont intégrées.

### Sense signals

| ID | Signal | Checks | Automation |
|----|--------|--------|------------|
| S6a | Export S0N/ créé | Répertoire S0N/ contient tous les fichiers requis (17+ fichiers) | Auto — file count check |
| S6b | System prompt V2.4 chargé | config/notebooklm_system_prompt.md présent et version = 2.4 | Auto — file exists + version grep |
| S6c | Réponse audit reçue | NotebookLM a retourné un report ou slide deck | Manuel — vérification Silas |
| S6d | Problèmes traités | Tous les problèmes identifiés soit corrigés, soit documentés comme gaps connus | Semi-auto — checklist |

**Carrier:** Silas + NotebookLM.

**Status:** Loop ouverte — processus défini, première exécution à lancer.

---

## H7: Convergence IgA → validates B8

La convergence IgA est visible dans la bande lumen du GA.

### Sense signals

| ID | Signal | Checks | Automation |
|----|--------|--------|------------|
| S7a | 4 lignes de convergence colorées | 4 lignes de convergence visibles dans la bande lumen, chacune d'une couleur produit distincte | Semi-auto — vérification visuelle |
| S7b | Formes Y IgA au point focal | Formes Y (IgA) regroupées au point de convergence | Semi-auto — vérification visuelle |

**Carrier:** Silas (vérification visuelle) + NotebookLM (audit).

**Status:** Loop ouverte — à vérifier sur wireframe_GA_v10.

---

## H8: Cycle fracture → validates B4 (renforcé par SD3)

La rupture du cercle vicieux par CRL1505 est visuellement explicite.

### Sense signals

| ID | Signal | Checks | Automation |
|----|--------|--------|------------|
| S8a | Flèche/lance verte brise le cycle rouge | L'élément vert (CRL1505) traverse visuellement le cercle vicieux rouge | Semi-auto — vérification visuelle |
| S8b | Marques de fracture au point d'impact | Éclats ou lignes de rupture visibles à l'endroit où la lance traverse le cycle | Semi-auto — vérification visuelle |

**Carrier:** Silas (vérification visuelle) + Aurore.

**Status:** Loop ouverte — à vérifier sur wireframe_GA_v10.

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
