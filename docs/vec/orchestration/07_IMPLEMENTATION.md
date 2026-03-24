# IMPLEMENTATION — vec/orchestration

## I-ORC1: Fichiers du module

L'orchestration ne possede pas de code propre. Elle coordonne les scripts des autres modules VEC et s'appuie sur des documents pour le handoff.

| Fichier | Role | Module proprietaire |
|---------|------|---------------------|
| `docs/vec/orchestration/10_SYNC.md` | Handoff inter-sessions (etat, gates, prochaine action) | orchestration |
| `docs/vec/ARCHITECTURE.md` | Vue d'ensemble des 7 modules et du flux | orchestration (meta) |
| `scripts/compose_ga_v10.py` | Compositeur parametrique (phase COMPILATION) | pipeline |
| `scripts/validate_ga.py` | Tribunal editorial MDPI (gate G2: H1) | editorial |
| `scripts/export_notebooklm.py` | Export sessions NLM (phase AUDIT) | audit |
| `scripts/generate_proposal_pdf.py` | Generateur PDF concept ASCII (phase CONCEPT) | orchestration |
| `config/notebooklm_system_prompt.md` | System prompt NLM V2.4 (phase AUDIT) | audit |
| `config/layout_v10.yaml` | Layout parametrique (phase COMPILATION) | pipeline |
| `config/palette.yaml` | Palette couleurs (phase COMPILATION) | design_system |
| `config/content.yaml` | Budget texte (phase COMPILATION) | editorial |

## I-ORC2: Dependances inter-modules

L'orchestration depend des RESULTATS des autres modules, pas de leurs mecanismes internes:

```
orchestration
├── utilise: pipeline.H5 (PASS/FAIL)         — gate G2
├── utilise: editorial.H1 (PASS/FAIL)        — gate G2
├── utilise: audit.H6 (PASS/FAIL)            — gate G3
├── utilise: calibration (si elements organiques) — phase COMPILATION
├── utilise: exploration (sub-agents)         — phases COMPILATION + AUDIT
├── utilise: design_system (palette, patterns) — phase COMPILATION
└── produit: SYNC state pour tous les modules
```

L'orchestration ne micro-manage pas les modules. Elle verifie leurs outputs via les health checks.

## I-ORC3: Outils MCP utilises

| Outil MCP | Phase | Usage |
|-----------|-------|-------|
| `send` | CONCEPT + VALIDATION | Envoyer PDF concept / GA final a Aurore |
| `subcall` | AUDIT + COMPILATION | Lancer sub-agents specialises |
| `think` | Toutes | Reflexion interne sur l'etat du flux |
| `sense` | Toutes | Lecture etat cognitif (drives, WM) |
| `task` | Toutes | Gestion des taches VEC |

## I-ORC4: Structure du SYNC

Le SYNC est structure en sections obligatoires:

```
# SYNC — vec/orchestration

## Statut actuel
Phase: [CONCEPT | COMPILATION | AUDIT | VALIDATION]
Version: vN
Gates:
  G1 (concept GO):        [PASS | FAIL | OPEN]
  G2 (compilation valid): [PASS | FAIL | OPEN]
  G3 (audit complet):     [PASS | FAIL | OPEN]
  G4 (validation ship):   [PASS | FAIL | OPEN]
Prochaine action: [une seule action actionnable]
Bloqueurs: [le cas echeant]

## Historique
[table date | auteur | action]

## Remarques / Questions
[renseigne au fur et a mesure]

## Consignes recues
[instructions en cours de session]

## Handoff
[contexte requis pour le prochain agent]
```

## I-ORC5: Fichiers bannis (export_notebooklm.py)

La liste de fichiers bannis dans export_notebooklm.py empeche les fantomes de versions precedentes de contaminer l'audit NotebookLM. L'orchestration est responsable de maintenir cette liste a jour quand de nouveaux artefacts obsoletes apparaissent.

Le mecanisme est dans le script lui-meme (`scripts/export_notebooklm.py`), pas dans l'orchestration. L'orchestration verifie que le mecanisme fonctionne (S-ORC6b).

## I-ORC6: Flux de fichiers par phase

```
CONCEPT:
  IN:  mission docs + science data
  OUT: concept_proposal.pdf → Aurore
       SYNC update (direction validee)

COMPILATION:
  IN:  config/*.yaml + concept valide
  OUT: wireframe_GA_vN.svg + _full.png + _delivery.png
       validate_ga.py output (PASS/FAIL)
       SYNC update (version, checks)

AUDIT:
  IN:  S0N/ (export) + NLM system prompt
  OUT: rapport NLM + corrections integrees
       SYNC update (audit resume, gaps)

VALIDATION:
  IN:  GA final (PNG/PDF) → Aurore
  OUT: SHIP (soumission) ou ITERATE (diagnostic + retour)
       SYNC update (outcome, feedback Aurore)
```
