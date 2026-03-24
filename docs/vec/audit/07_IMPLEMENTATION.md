# Implementation — vec/audit

## I-AUD1: Fichiers du module

| Fichier | Role | Ref |
|---------|------|-----|
| `scripts/export_notebooklm.py` | Genere le repertoire plat S0N/ pour upload NotebookLM | A-AUD1 step 1 |
| `scripts/transcribe_podcast.py` | Transcription Whisper des podcasts NotebookLM | A-AUD1 step 4 |
| `config/notebooklm_system_prompt.md` | System prompt V2.4 — ton, role, audit silencieux | PA1, V-AUD1 |
| `artefacts/audits/` | Archives des outputs NLM (reports, slides, transcripts) | A-AUD1 step 6 |
| `docs/vec/audit/` | Ce doc chain (10 facets) | — |

## I-AUD2: Script export_notebooklm.py

**Responsabilite :** Creer un repertoire plat S0N/ contenant tous les fichiers necessaires a une session d'audit NotebookLM.

**Contenu de l'export :**

| Categorie | Fichiers | Pourquoi |
|-----------|----------|----------|
| Doc chain mission | `01_RESULTS.md` a `10_SYNC.md` (mission-level) | Contexte scientifique complet |
| Specs | `GA_SPEC.md`, `MISSION.md` | Contraintes et objectifs |
| Configs | `palette.yaml`, `layout_v10.yaml`, `content.yaml` | Parametres courants du compositeur |
| Artefacts courants | `wireframe_GA_v10_delivery.png`, `wireframe_GA_v10.svg` | Le GA a auditer |
| System prompt | `notebooklm_system_prompt.md` | Instructions NLM |
| Doc chain VEC | Fichiers pertinents de `docs/vec/` | Patterns et invariants du moteur |

**Exclusions :**
- Rendus de versions deprecees (wireframe_GA_v7_*, wireframe_GA_v8_*)
- Iterations anciennes (iterations/v1-v8/)
- Concepts IA obsoletes qui ne correspondent plus au design actif
- Fichiers binaires > 5 MB (risque de timeout upload)

**Validation post-export :**
- Comptage fichiers >= 17
- Presence system prompt V2.4 (grep version dans le fichier)
- Pas de fichiers de versions bannies dans S0N/

## I-AUD3: System prompt NotebookLM (V2.4)

Le system prompt vit dans `config/notebooklm_system_prompt.md`. Version courante : 2.4.

**Sections cles :**
1. Role et trinome (P13)
2. Design actif V10 "La Bronche Vivante" — matrice produit-mecanisme
3. Cerveau entier P5 — biologie encode la cognition
4. Ton et style — naturel, direct, auditeur pas directeur
5. Audit silencieux — regles MDPI verifiees en arriere-plan, fail loud si violation
6. Hygiene cognitive P11 — ignore les versions obsoletes

**Invariant V-AUD1 :** La section 4 interdit explicitement a NotebookLM de donner des directives code a Silas. Si ca arrive, c'est un symptome de pollution contextuelle (PA5).

## I-AUD4: Structure artefacts/audits/

```
artefacts/audits/
  S01_output_report.md          <- Report textuel
  S01_output_SD1.pdf            <- Slide deck #1
  S01_output_transcript.md      <- Podcast transcrit
  S02_output_SD2.pdf            <- Slide deck session 2
  S02_output_report.md          <- Report session 2
  ...
```

Chaque session est prefixee par son numero (S01, S02...). Pas d'ecrasement — chaque session est un artefact distinct. Le numero de session correspond au S0N/ de l'export.

## I-AUD5: Dependances

| Outil | Usage | Installe |
|-------|-------|----------|
| `export_notebooklm.py` | Export S0N/ | Script Python dans `scripts/` |
| `transcribe_podcast.py` | STT podcast NLM → texte | Script Python dans `scripts/`, depend de Whisper |
| NotebookLM (Google) | Audit externe multi-sources | Service web, pas de dependance locale |
| Canal communication Aurore | WhatsApp / Telegram / email | Externe, via MCP `send` |

## I-AUD6: Flux de donnees

```
                    +-----------+
                    | Fichiers  |
                    | courants  |
                    +-----+-----+
                          |
                   export_notebooklm.py
                          |
                    +-----v-----+
                    |   S0N/    |  (repertoire plat)
                    +-----+-----+
                          |
                     upload NLM
                          |
                    +-----v-----+
                    | NotebookLM|
                    | (session) |
                    +-----+-----+
                          |
              +-----------+-----------+
              |           |           |
           Report    Slide deck   Podcast
              |           |           |
              +-----+-----+-----+----+
                    |                 |
              transcribe_podcast.py   |
                    |                 |
              +-----v-----------v-----+
              |   Findings integres   |
              +-----------+-----------+
                          |
                  +-------v--------+
                  | Corrections    |    (commit)
                  | Gaps connus    |    (SYNC)
                  | Escalades     |    (A-AUD2 → Aurore)
                  +----------------+
```
