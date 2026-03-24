# Validation — Mission Immunomodulateur GA

## Invariants (MUST)

**V1: Ratio panoramique.** Le GA DOIT être ≥ 560×1100 px (h×w). Violation = rejet MDPI. Health: H1. Supports R1.
**Evidence:** MDPI editorial rules (publisher standard).

**V2: Zéro titre/affiliation/référence.** Aucun nom d'auteur, aucune institution, aucun numéro de citation ne peut apparaître sur le GA. Violation = rejet MDPI. Health: H1. Supports R1.
**Evidence:** MDPI editorial rules (publisher standard).

**V3: Budget texte ≤ 30 mots.** Aucun bloc de texte. Labels courts uniquement (1-3 mots). Violation = rejet MDPI (règle MDPI R3). Health: H1. Supports R1.
**Evidence:** MDPI editorial rules (publisher standard).

**V4: Non-redondance.** Le GA ne reproduit NI la Figure 1 (flux manufacturing vertical) NI la Figure 2 (quadrants cytokines). Violation = rejet MDPI (règle MDPI R2). Health: H1. Supports R1.
**Evidence:** MDPI editorial rules (publisher standard).

**V5: Hiérarchie preuves exacte.** OM-85 (18 RCTs) > PMBL (5 RCTs) > MV130 (1 RCT) > CRL1505 (préclinique). Toute inversion = erreur scientifique. Health: H2 (sign-off Aurore). Supports R2.
**Evidence:** Akl 2007 (74% vs 14%, RCT) + Rosenbaum 2010 (93% vs 44%, RCT). Symboles visuels > chiffres pour la compréhension de la certitude.

**V6: Libre de droits.** Tout élément visuel est original ou sous licence libre vérifiée. Pas de filigrane BioRender. Pas d'éléments IA générés dans le livrable final. Violation = rejet MDPI (règle MDPI R5). Health: H1. Supports R1.
**Evidence:** MDPI editorial rules (publisher standard).

**V7: Lisibilité à 50% zoom.** Le plus petit caractère du GA (y compris indices comme le γ de IFN-γ) doit être lisible quand l'image est affichée à 550×280 px. Violation = rejet MDPI (règle MDPI R6). Health: H1. Supports R1, P6.
**Evidence:** MDPI editorial rules (publisher standard).

## Invariants (NEVER)

**VN1:** JAMAIS de listes de cytokines sur le GA. C'est le domaine de la Figure 2. Enforces T1 (densité vs lisibilité), NO4.
**Evidence:** Miller 1956 (7+/-2, fondamental) + Jambor 2024 rule #6 (expert consensus). Limiter les éléments visuels pour ne pas surcharger la mémoire de travail.

**VN2:** JAMAIS de schéma de procédé de fabrication. C'est le domaine de la Figure 1. Enforces V4 (non-redondance), NO4.
**Evidence:** Design heuristic (non validé empiriquement). Cible Vague 2 de recherche.

**VN3:** JAMAIS de version "minimale" ou "brouillon" présentée comme option. Toutes les versions sont qualité maximale. Enforces P2 (framework dynamique).
**Evidence:** Design heuristic (non validé empiriquement). Cible Vague 2 de recherche.

**VN4:** JAMAIS d'éléments générés par IA dans le livrable final. Corollary of V6 (libre de droits). Si IA utilisée pour wireframing, le rendu final doit être redessiné en SVG programmatique.
**Evidence:** Design heuristic (non validé empiriquement). Cible Vague 2 de recherche.

## Invariants (PIPELINE)

**V8: Rendu E2E complet.** Chaque itération produit les 3 fichiers (SVG + PNG full + PNG delivery). Un fichier manquant ou corrompu = pipeline en échec. Fail Loud. Health: H5. Implements P8, P10.
**Evidence:** Design heuristic (non validé empiriquement). Cible Vague 2 de recherche.

**V9: Delivery non-blank.** Le PNG delivery (1100×560) DOIT être un rendu lisible, pas un fichier blanc ou de < 5 KB. Bug v3 = violation de V9. Health: H5.
**Evidence:** Design heuristic (non validé empiriquement). Cible Vague 2 de recherche.

**V10: Archivage versionnée.** Chaque itération est numérotée et préservée. On ne surécrit JAMAIS un artefact précédent. Implements P11.
**Evidence:** Design heuristic (non validé empiriquement). Cible Vague 2 de recherche.

**V11: Provenance traçable.** Chaque élément visuel du livrable final a une source documentée dans `artefacts/PROVENANCE.md`. Implements P9. Health: H1 (S1e).
**Evidence:** Design heuristic (non validé empiriquement). Cible Vague 2 de recherche.

**V12: Pictogramme enfant obligatoire.** Zone 1 DOIT contenir un pictogramme enfant malade. Zone 3 DOIT contenir un pictogramme enfant protégé. La coupe bronchique seule ne suffit PAS pour la projection clinique < 2s (PH1). Violation = le pédiatre ne projette pas son patient. Health: H2 (sign-off Aurore). Supports R2, B7. DECISION feedback Aurore 24 mars 2026.
**Evidence:** Design heuristic (non validé empiriquement). Cible Vague 2 de recherche.

**V13: Pont CRL1505 spatialement séparé.** Le pont CRL1505 (#059669) DOIT être visuellement détaché des 3 agents locaux (OM-85, PMBL, MV130). L'arc DOIT partir du bas de l'image pour signifier l'action systémique via l'axe intestin-poumon. Si trop compact, le pédiatre ne comprend pas que c'est un probiotique oral. Violation = confusion mécanisme d'action. Health: H1. Supports B2, P3. DECISION feedback Aurore 24 mars 2026.
**Evidence:** Design heuristic (non validé empiriquement). Cible Vague 2 de recherche.

## Checklist complète

Voir → `sources/Protocole d'Audit de Pré-Soumission...md` pour la grille d'audit détaillée. Implements A4 (validation pré-soumission).
