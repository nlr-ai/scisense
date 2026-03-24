# SYNC — vec/exploration

**Module:** vec/exploration — Agents autonomes paralleles
**Version:** 1.0.0
**Date:** 2026-03-24
**Author:** Silas (b2d65910b3daa7fd)

---

## Etat courant

| Facet | Fichier | Statut |
|-------|---------|--------|
| RESULTS | 01_RESULTS.md | Complet (R1-R5) |
| OBJECTIVES | 02_OBJECTIVES.md | Complet (O1-O4, NO1-NO4, T1-T3) |
| PATTERNS | 03_PATTERNS.md | Complet (EP1-EP8) |
| BEHAVIORS | 04_BEHAVIORS.md | Complet (BE1-BE8) |
| ALGORITHM | 05_ALGORITHM.md | Complet (AE1-AE4, 6 prompt templates) |
| VALIDATION | 06_VALIDATION.md | Complet (VE1-VE10) |
| IMPLEMENTATION | 07_IMPLEMENTATION.md | Complet |
| HEALTH | 08_HEALTH.md | Complet (HE1-HE4, dashboard template) |
| PHENOMENOLOGY | 09_PHENOMENOLOGY.md | Complet |
| SYNC | 10_SYNC.md | Actif |

### Guarantee Loop

```
RESULT: Findings actionnables integres, pas de blind spot dans le design
  -> SENSE: Agent results integres ou dismisses avec justification
    -> HEALTH: Aucun probleme identifie par >1 agent reste sans reponse
      -> CARRIER: Silas (sub-agents)
```

**Loop status:** Ouverte — doc chain complete, loop non encore exercee en production. Premier cycle d'exploration fermera la loop.

### Dependances

- Module `vec/audit` — l'exploration est souvent declenchee pendant la phase AUDIT (A9 step 6)
- Module `vec/orchestration` — les sub-agents sont des I6 dans la taxonomie A10
- Pattern P4 (agents autonomes paralleles) — defini dans `missions/immunomodulator/docs/03_PATTERNS.md`
- Algorithm A2 (orchestration des 3 agents) — defini dans `missions/immunomodulator/docs/05_ALGORITHM.md`

---

## Historique

| Date | Version | Changement |
|------|---------|-----------|
| 2026-03-24 | 0.1.0 | Creation du doc chain 10 facets. Module exploration. |
| 2026-03-24 | 1.0.0 | 10 facets complets. R1-R5, O1-O4/NO1-NO4/T1-T3, EP1-EP8, BE1-BE8, AE1-AE4 + 6 prompt templates, VE1-VE10, implementation map, HE1-HE4 + dashboard, phenomenologie 3 perspectives. |

---

## Remarques / Questions

1. Ce module n'a pas de code executable. Son "implementation" est un protocole documente. Si un jour l'exploration est automatisee (orchestrateur de sub-agents), le code vivra dans `scripts/exploration_orchestrator.py`.

2. La taxonomie des 6 angles (EP2) est derivee du projet immunomodulateur. Elle est extensible pour d'autres missions SciSense mais les 6 angles de base couvrent les dimensions recurrentes d'un GA scientifique.

3. Les prompt templates (AE4) sont des bases a adapter. Le SCOPE et les fichiers references changent a chaque cycle. L'ANGLE, les CONTRAINTES, et le FORMAT DE RETOUR sont relativement stables.

4. Le plafond de 3 agents (EP4/VE1) est empirique, pas theorique. Il vient de l'observation que les findings deviennent redondants au-dela de 3 perspectives sur le meme sujet. A remettre en question si un cas montre clairement que 4 agents auraient apporte un insight unique.

---

## Consignes recues

*(Section pour instructions live de NLR ou Aurore — verifier periodiquement)*

*(vide)*
