# PATTERNS — vec/orchestration

## P-ORC1: Phases sequentielles, parallelisme intra-phase

Les 4 phases (CONCEPT, COMPILATION, AUDIT, VALIDATION) s'executent strictement en sequence. Aucun raccourci. Aucune phase sautee.

```
CONCEPT ──gate──> COMPILATION ──gate──> AUDIT ──gate──> VALIDATION ──outcome──>
```

La parallelisation est reservee a l'INTERIEUR des phases:
- CONCEPT: 3 agents paralleles explorent 3 axes (A2)
- COMPILATION: sub-agents paralleles pour exploration ciblee (A9 step 6)
- AUDIT: NotebookLM + sub-agents en parallele (A9 steps 3-6)

Ce pattern empeche le scenario ou "on code avant d'avoir le GO d'Aurore" ou "on envoie a Aurore sans avoir audite". Ces raccourcis sont les premiers vecteurs de regression.

## P-ORC2: Gate explicite a chaque transition

Chaque transition entre phases est un gate binaire: PASS ou FAIL. Pas de "en cours", pas de "presque", pas de "on continue en parallele". Le gate est defini par des conditions mesurables (health checks), pas par un jugement subjectif.

| Transition | Gate | Conditions |
|------------|------|------------|
| CONCEPT -> COMPILATION | G1 | Aurore GO explicite sur la direction conceptuelle |
| COMPILATION -> AUDIT | G2 | H1 PASS (editorial) + H5 PASS (pipeline) + P25 PASS (visual check) |
| AUDIT -> VALIDATION | G3 | H6 PASS (audit NLM complet) + zero probleme critique ouvert |
| VALIDATION -> SHIP | G4 | H2 PASS (Aurore science sign-off) + R1-R4 tous fermes |
| VALIDATION -> ITERATE | G5 | Gate echoue identifie + phase de retour documentee |

Si un gate est FAIL, la progression est bloquee. Pas de negociation.

## P-ORC3: SYNC comme memoire inter-sessions

Le fichier SYNC (10_SYNC.md) est le SEUL mecanisme de handoff entre sessions humaines. Il contient l'etat necessaire et suffisant pour qu'un agent demarre une session sans contexte residuel:

- Phase courante (CONCEPT / COMPILATION / AUDIT / VALIDATION)
- Gates ouverts (G1-G5 avec status)
- Prochaine action (une seule, actionnable)
- Bloqueurs (le cas echeant)
- Numero de version courant (vN)

Le SYNC n'est PAS un log exhaustif. L'historique detaille est dans la section Historique du SYNC de la mission (`missions/immunomodulator/docs/10_SYNC.md`). Le SYNC du module orchestration pointe vers l'instance concrete.

## P-ORC4: Export S0N/ comme memoire inter-sessions NLM

L'export NotebookLM (`S0N/`) est le handoff entre sessions NotebookLM. Il est regenere par `export_notebooklm.py` avant chaque nouvelle session NLM. Le script inclut une liste de fichiers bannis qui empeche les artefacts obsoletes de contaminer l'audit.

Difference avec SYNC: SYNC est pour les humains et les agents. S0N/ est pour NotebookLM specifiquement — un repertoire plat de fichiers sources que NLM peut ingerer.

## P-ORC5: Hard Reset (P11) — purge des fantomes

Avant une nouvelle session sur une nouvelle version majeure, le Hard Reset purge les fantomes cognitifs:

1. Les wireframes des versions precedentes ne sont PAS charges dans le contexte
2. Les debats resolus ne sont PAS re-ouverts
3. Les exports S0N/ sont regeneres sans les fichiers bannis
4. Le SYNC est relu en premier — c'est la source de verite, pas la memoire de l'agent

Le Hard Reset n'est PAS une perte d'information. Les artefacts sont archives (P11 version archival). Les decisions sont documentees dans SYNC. La purge concerne le CONTEXTE ACTIF, pas le stockage.

## P-ORC6: Les 7 intelligences ont des phases assignees

Chaque intelligence (A10) intervient dans des phases specifiques. L'orchestration verifie que la bonne intelligence est mobilisee au bon moment:

| Intelligence | Phase(s) assignee(s) | Role |
|-------------|---------------------|------|
| I1 Aurore | CONCEPT + VALIDATION | GO/NO-GO conceptuel + sign-off scientifique |
| I2 NLR | CONCEPT + tout pivot architectural | Direction strategique + arbitrage structurel |
| I3 NotebookLM | AUDIT | Analyse multi-sources, generation rapport/podcast/infographic |
| I4 Silas | Toutes phases | Code, documentation, orchestration, sub-agents |
| I5 AI Image | COMPILATION (via calibration) | Extraction contours organiques |
| I6 Sub-agents | AUDIT + COMPILATION | Exploration specialisee (angles specifiques) |
| I7 Scripts | COMPILATION + AUDIT | Validation automatisee (validate_ga.py, export_notebooklm.py) |

Violation: demander a NotebookLM de valider la science (c'est Aurore). Demander a Aurore de debugger le pipeline (c'est Silas). Chaque intelligence a un perimetre, l'orchestration le fait respecter.

## P-ORC7: Iterate retourne a la phase pertinente

Quand VALIDATION echoue (G4 FAIL), le retour n'est pas systematiquement au debut. L'orchestration identifie le gate qui echoue et retourne a la phase correspondante:

| Gate echoue | Diagnostic | Retour a |
|-------------|-----------|----------|
| H1 FAIL (editorial) | Violation MDPI non detectee en COMPILATION | COMPILATION (re-run validate_ga.py) |
| H2 FAIL (science) | Aurore identifie une erreur scientifique | CONCEPT (si direction fausse) ou COMPILATION (si erreur d'implementation) |
| H5 FAIL (pipeline) | Rendu corrompu ou incomplet | COMPILATION (fix pipeline) |
| H6 FAIL (audit) | Probleme identifie par NLM non resolu | AUDIT (re-integrer les corrections) |

Le diagnostic est obligatoire. "Ca ne marche pas" n'est pas un diagnostic. "H2 FAIL parce que la hierarchie des preuves OM-85 > PMBL est inversee visuellement" est un diagnostic.
