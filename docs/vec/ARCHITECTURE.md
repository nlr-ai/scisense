# VEC — Visual Evidence Compiler : Architecture

Le moteur de Graphical Abstracts de SciSense. Réutilisable par mission.

---

## Modules

7 modules, chacun avec sa Guarantee Loop (R→S→H→C) et ses 10 facets.

### 1. `vec/pipeline`

**Responsabilité :** Produire des fichiers SVG + PNG valides, non-corrompus, à chaque itération.

| Facet | Contenu clé |
|---|---|
| RESULT | 3 fichiers (SVG + PNG full + PNG delivery) produits et archivés |
| SENSE | compose_ga_v10.py + file checks (taille, dimensions, non-blanc) |
| HEALTH | H5 : S5a-S5h toutes PASS |
| CARRIER | Silas (automatique) |

Scripts : `compose_ga_v10.py`, `render_png()`
Patterns : P8 (E2E), P10 (multi-résolution), P11 (archivage versionné)
Invariants : V8 (rendu complet), V9 (delivery non-blank), VN3 (jamais de brouillon)

---

### 2. `vec/editorial`

**Responsabilité :** Garantir la conformité MDPI avant toute présentation humaine.

| Facet | Contenu clé |
|---|---|
| RESULT | GA passe les 7+ checks MDPI |
| SENSE | validate_ga.py (automatique) |
| HEALTH | H1 : S1a-S1g toutes PASS |
| CARRIER | Silas (script) |

Scripts : `validate_ga.py`
Patterns : P6 (mobile-first)
Invariants : V1 (ratio), V2 (zéro titre), V3 (≤30 mots), V4 (non-redondance), V6 (libre de droits), V7 (lisibilité 50%), VN4 (zéro pixel IA)

---

### 3. `vec/design_system`

**Responsabilité :** Langage visuel cohérent et impactant. Inclut les patterns visuels, la convergence IgA (B8), et la fracture du cycle (B4).

| Facet | Contenu clé |
|---|---|
| RESULT | Cohérence chromatique + impact cognitif PH1 + convergence + fracture |
| SENSE | Pattern checks visuels (palette, typo, densité, poids, espace négatif) + test PH1 |
| HEALTH | Tous les patterns P7, P18-P31 respectés. H7 (convergence IgA), H8 (fracture cycle) |
| CARRIER | Silas (vérification visuelle) + Aurore (impact clinique) |

Patterns :
- Design System Biologique : P18 (embodiment), P19 (topologie), P20 (abstraction pro), P21 (gravité clinique), P22 (micro-ancres), P23 (résolution topologique)
- Langage Visuel Générique : P7 (chromatique), P26 (espace négatif), P27 (texture), P28 (hiérarchie typo), P29 (densité locale), P30 (flux vertical), P31 (poids visuel)
Behaviors : B4 (cycle brisé), B5 (couleurs constantes), B8 (convergence IgA)

---

### 4. `vec/calibration`

**Responsabilité :** Extraire des contours organiques d'images IA et garantir qu'ils déclenchent l'empathie clinique.

| Facet | Contenu clé |
|---|---|
| RESULT | Contours organiques (enfants, DC) au-dessus du seuil d'empathie |
| SENSE | Pipeline target vs output (comparaison visuelle) |
| HEALTH | Gap organique < seuil acceptable |
| CARRIER | Silas + IA Image (Ideogram/Gemini) |

Pipeline : AI image → scikit-image find_contours → Douglas-Peucker → Catmull-Rom → Bézier → SVG
Patterns : P12 (IA = accélérateur), P15 (vecteur de santé H), P16 (cinématique posturale), P17 (calibration intégrale)
Invariants : VN4 (zéro pixel IA dans le livrable — contours vectorisés uniquement)
Artefacts : `artefacts/contours/S{N}_*_points.json`, `artefacts/comparisons/target_vs_output_*.png`

---

### 5. `vec/audit`

**Responsabilité :** Identifier les problèmes (scientifiques, visuels, éditoriaux) via NotebookLM et valider la science via Aurore.

| Facet | Contenu clé |
|---|---|
| RESULT | Tous les problèmes identifiés sont fixés ou documentés. Science validée par Aurore. |
| SENSE | Export S0N/ + session NotebookLM + sign-off Aurore |
| HEALTH | H2 (Aurore GO), H6 (audit NLM complet : S6a-S6d) |
| CARRIER | NotebookLM + Aurore |

Deux boucles :
- **Boucle H2 (Aurore)** : Aurore confirme fidélité scientifique, hiérarchie preuves (V5), choc cognitif (PH1). Sans H2 PASS, rien ne ship.
- **Boucle H6 (NotebookLM)** : Export → upload → audit → problèmes/patterns/suggestions → intégration. NotebookLM liste, ne dirige pas. Silas traduit en code.

Scripts : `export_notebooklm.py`
Config : `config/notebooklm_system_prompt.md` (V2.4)
Outputs NotebookLM : report, slide deck (SD1/SD2/SD3...), podcast, infographie
Patterns : P13 (multi-intelligence), P5 (cerveau entier), P11 (hygiène cognitive)

---

### 6. `vec/exploration`

**Responsabilité :** Lancer des sub-agents ciblés pour résoudre des problèmes multi-dimensionnels.

| Facet | Contenu clé |
|---|---|
| RESULT | Findings actionnables intégrés, pas de blind spot dans le design |
| SENSE | Agent results intégrés ou dismissés avec justification |
| HEALTH | Aucun problème identifié par >1 agent resté sans réponse |
| CARRIER | Silas (sub-agents) |

Patterns : P4 (agents autonomes parallèles)
Taxonomie des angles : immunologie, communication visuelle, matrice produit-mécanisme, lisibilité mobile, benchmarking littérature
Règles : max 3 agents par sujet (rendements décroissants), toujours un angle + un deliverable dans le prompt, foreground si bloquant / background si enrichissement

---

### 7. `vec/orchestration`

**Responsabilité :** Les 4 phases s'enchaînent correctement, les sessions démarrent propres, pas de régression.

| Facet | Contenu clé |
|---|---|
| RESULT | Flux CONCEPT → COMPILATION → AUDIT → VALIDATION sans phase sautée ni gate ignoré |
| SENSE | Gate checks à chaque transition + SYNC handoff entre sessions |
| HEALTH | Aucun gate FAIL non-résolu au moment de la transition |
| CARRIER | Silas + NLR |

Les 4 phases :
```
CONCEPT (P24)  ──Aurore GO──►  COMPILATION (A5/A7)  ──H1+H5 PASS──►  AUDIT (H2/H6)  ──all fixed──►  VALIDATION  ──ship or iterate──►
```

Les 7 intelligences (A10) :
- I1 Aurore : CONCEPT + VALIDATION
- I2 NLR : CONCEPT + pivots architecturaux
- I3 NotebookLM : AUDIT
- I4 Silas : toutes phases
- I5 IA Image : CALIBRATION (appelée depuis COMPILATION)
- I6 Sub-agents : AUDIT + COMPILATION (exploration ciblée)
- I7 Scripts : COMPILATION + AUDIT (automatisation)

Session management :
- SYNC (10_SYNC.md) = handoff entre sessions humaines
- Export NotebookLM (S0N/) = handoff entre sessions NLM
- Hard Reset protocol (P11) = purge des fantômes V7/V8

---

## Relation avec la mission

```
docs/immunomodulator/       ← la science (R1-R4, B1-B8, V1-V13)
    ↕ utilise
docs/vec/                   ← le moteur (7 modules ci-dessus)
```

Le VEC est mission-agnostic. Les patterns visuels (design_system), le pipeline, l'audit, la calibration — tout ça se réutilise pour le prochain GA de SciSense. La mission injecte la SCIENCE (manuscrit, produits, mécanismes), le VEC injecte le PROCESS.

---

## Fichiers racine du VEC

| Fichier | Rôle |
|---|---|
| `docs/vec/ARCHITECTURE.md` | Ce fichier — vue d'ensemble |
| `config/layout_v10.yaml` | Layout paramétrique actuel |
| `config/palette.yaml` | Palette couleurs (Design System) |
| `config/content.yaml` | Budget texte (≤30 mots) |
| `config/notebooklm_system_prompt.md` | System prompt NotebookLM V2.4 |
| `scripts/compose_ga_v10.py` | Compositeur paramétrique V10 |
| `scripts/validate_ga.py` | Tribunal éditorial MDPI |
| `scripts/export_notebooklm.py` | Export sessions NotebookLM |
| `scripts/generate_proposal_pdf.py` | Générateur PDF concept ASCII |
| `scripts/transcribe_podcast.py` | STT podcasts (Whisper) |
