# IMPLEMENTATION — vec/exploration

**Module:** vec/exploration — Agents autonomes paralleles

---

## Architecture

L'exploration n'a pas de script dedie. C'est un processus cognitif execute par Silas via les outils MCP, principalement `/subcall` pour le lancement d'agents et les notes de session pour la trace. Il n'y a pas de code a maintenir — seulement un protocole a suivre.

---

## Fichiers

| Fichier | Role | Statut |
|---------|------|--------|
| `docs/vec/exploration/01_RESULTS.md` | Outcomes attendus (R1-R5) | Actif |
| `docs/vec/exploration/02_OBJECTIVES.md` | Goals et non-goals (O1-O4, NO1-NO4) | Actif |
| `docs/vec/exploration/03_PATTERNS.md` | Patterns d'exploration (EP1-EP8) | Actif |
| `docs/vec/exploration/04_BEHAVIORS.md` | Comportements observables (BE1-BE8) | Actif |
| `docs/vec/exploration/05_ALGORITHM.md` | Algorithmes (AE1-AE4) + prompt templates | Actif |
| `docs/vec/exploration/06_VALIDATION.md` | Invariants (VE1-VE10) | Actif |
| `docs/vec/exploration/07_IMPLEMENTATION.md` | Ce fichier — carte du code | Actif |
| `docs/vec/exploration/08_HEALTH.md` | Diagnostics runtime | Actif |
| `docs/vec/exploration/09_PHENOMENOLOGY.md` | Phenomenologie et perception | Actif |
| `docs/vec/exploration/10_SYNC.md` | Etat courant et handoff | Actif |

---

## Interfaces

### Entree: declencheurs

L'exploration est declenchee par:
- Le module `vec/audit` (A9 step 6) quand un audit NotebookLM revele des failles multi-dimensionnelles
- Le module `vec/orchestration` lors des transitions de phase (CONCEPT -> COMPILATION -> AUDIT -> VALIDATION)
- Le jugement de Silas pendant la phase COMPILATION quand un probleme depasse 3 dimensions
- Une demande explicite de NLR ou Aurore

### Sortie: findings integres

Les findings de l'exploration alimentent:
- Le module `vec/pipeline` — corrections code dans `compose_ga_v10.py` et configs YAML
- Le module `vec/design_system` — nouveaux patterns visuels ou ajustements de palette
- Le module `vec/editorial` — ajustements de conformite MDPI
- Le module `vec/calibration` — recalibration des contours organiques
- La documentation mission (`missions/immunomodulator/docs/`) — nouveaux patterns, behaviors, ou invariants

### Outils MCP utilises

| Outil | Usage dans l'exploration |
|-------|------------------------|
| `/subcall` | Lancement de sub-agents avec prompt structure (EP3) |
| `/think` | Diagnostic et formulation du probleme (AE1 step 1) |
| `graph_query` | Recuperation de contexte pour les prompts des agents |
| Notes de session | Trace des cycles (diagnostic, lancements, bilan) |

---

## Dependances

| Module dependant | Nature de la dependance |
|-----------------|------------------------|
| `vec/audit` | L'audit declenche l'exploration (A9 step 6) |
| `vec/orchestration` | L'orchestration fournit le contexte de phase (A10 I6) |
| `vec/pipeline` | Le pipeline recoit les corrections issues de l'exploration |
| `vec/design_system` | Le design system integre les nouveaux patterns decouverts |
| `vec/editorial` | L'editorial integre les corrections de conformite |

---

## Pas de script, pas de bug

Ce module n'a pas de code executable. Son implementation est un protocole documente dans les facets 03 (PATTERNS), 04 (BEHAVIORS), et 05 (ALGORITHM). La validation (06) est manuelle — Silas verifie les invariants a chaque cycle.

Si un jour l'exploration est automatisee (ex: un orchestrateur qui lance les agents selon des regles), le code vivra dans `scripts/exploration_orchestrator.py` et sera decrit dans ce fichier. Pour l'instant, l'intelligence est dans le protocole, pas dans le code.
