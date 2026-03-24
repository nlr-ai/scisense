# Sync — vec/design_system

## Etat actuel: 24 mars 2026

### Phase: COMPLETE — Doc chain 10 facets ecrite

### Module

**vec/design_system** — Langage visuel coherent et impactant. Contient tous les patterns visuels (P7, P18-P31), les behaviors de convergence IgA (B8) et fracture du cycle (B4), et la phenomenologie PH1 (impact cognitif 3 secondes).

C'est le module le plus lourd du VEC : il definit le lexique semiotique complet de SciSense — les regles de traduction entre biologie clinique et representation visuelle.

### Status

| Element | Status | Contenu |
|---------|--------|---------|
| 01_RESULTS | done | 6 resultats mesurables (DS-R1 a DS-R6) + guarantee loop |
| 02_OBJECTIVES | done | 1 goal, 4 non-goals, 4 tradeoffs, 5 priorites ranked |
| 03_PATTERNS | done | 17 patterns : P18-P23 (Design System Biologique) + P7, P26-P31 (Langage Visuel Generique) + P32-P34 (Litterature) |
| 04_BEHAVIORS | done | 3 behaviors (DS-B4 fracture, DS-B5 couleurs, DS-B8 convergence) + relations inter-behaviors |
| 05_ALGORITHM | done | 5 algorithmes (DS-A1 chromatique, DS-A2 PH1, DS-A3 spatial, DS-A4 convergence, DS-A5 fracture) |
| 06_VALIDATION | done | 17 invariants (DS-V1 a DS-V17) en 5 familles + checklist compacte |
| 07_IMPLEMENTATION | done | Fichiers, configs (palette/layout/content YAML), fonctions compose_ga.py, dependances, integration VEC |
| 08_HEALTH | done | 6 health checkers (DS-H1 a DS-H4 + H7 + H8), 18 sense signals, open loops table |
| 09_PHENOMENOLOGY | done | PH1 cascade 3 secondes (detaillee seconde par seconde), perception Aurore, perception Silas, boucle phenomenologique, feedback reinjection |
| 10_SYNC | done | Ce fichier |

### Guarantee Loops

```
DS-R1 (coherence chromatique)     ← DS-H1 ← DS-S1a-c      [partiellement ferme]
DS-R2 (impact cognitif PH1)      ← DS-H2 ← DS-S2a-c      [ouvert — protocole defini]
DS-R3 (convergence IgA)          ← H7    ← S7a-b          [ouvert — a implementer V10.2]
DS-R4 (fracture cycle)           ← H8    ← S8a-b          [ouvert — a implementer V10.2]
DS-R5 (hierarchie typographique) ← DS-H3 ← DS-S3a-d      [partiellement ferme]
DS-R6 (equilibre spatial)        ← DS-H4 ← DS-S4a-d      [ouvert — protocole defini]
```

### Cross-references avec la mission

| Mission ref | Design system ref | Relation |
|-------------|-------------------|----------|
| B4 (cycle brise) | DS-B4, DS-R4, H8, DS-V16, DS-V17, P23 | extends |
| B5 (couleurs constantes) | DS-B5, DS-R1, DS-H1, P7 | extends |
| B8 (convergence IgA) | DS-B8, DS-R3, H7, DS-V14, DS-V15 | extends |
| PH1 (perception pediatre) | DS-R2, DS-H2, DS-PH1, DS-A2 | extends |
| H1 palette sub-check | DS-H1, DS-A1 | integre |
| V3 (30 mots) | DS-V4, DS-R5, DS-H3 | extends |
| V7 (lisibilite 50%) | DS-V6, DS-R5, DS-H3 | extends |
| V12 (enfant obligatoire) | DS-PH1 seconde 2 | reference |
| V13 (CRL1505 separe) | DS-V13, P19 | reference |

### Remarques / Questions

- Les open loops H7 et H8 dependent de l'implementation V10.2 (convergence IgA + fracture cycle). Le design system definit QUOI verifier ; l'implementation est dans vec/pipeline et compose_ga.py.
- DS-H1 est partiellement ferme : le grep des 4 hex est dans validate_ga.py, mais les checks de contexte (rouge exclusif pathologique) et couleurs parasites sont a ajouter.
- DS-H3 est partiellement ferme : word count OK dans validate_ga.py, font-size check et placement check a ajouter.

### Consignes recues

(espace reserve pour les instructions en direct de NLR ou Aurore)

### Handoff

1. Ce module (`docs/vec/design_system/`) est le reference pour tous les patterns visuels du VEC.
2. La palette canonique est dans `config/palette.yaml` (DS-I2).
3. Les algorithmes de verification (DS-A1 a DS-A5) sont les protocoles a executer a chaque iteration.
4. Les open loops sont dans 08_HEALTH.md — prochaine action : implementer convergence IgA + fracture dans compose_ga.py.
5. La cascade PH1 (09_PHENOMENOLOGY.md) est le critere ultime de succes du design system.

### Historique

| Date | Action |
|------|--------|
| 2026-03-24 | Creation du module vec/design_system. Doc chain 10 facets initiee. |
| 2026-03-24 | 10 facets ecrites. 6 results, 14 patterns, 3 behaviors, 5 algorithmes, 17 invariants, 6 health checkers, 18 sense signals, phenomenologie PH1 detaillee. Module complet. |
| 2026-03-24 | VEC Literature Analysis integrated — P32-P34 added to 03_PATTERNS (encodage perceptif hierarchique, frequences naturelles, luminance pour incertitude). V14 (accessibilite daltoniens) et V15 (absence de spin visuel) added to vec/editorial 06_VALIDATION. H9 (Premier Regard — comprehension clinique directe) added to vec/audit 08_HEALTH. Pattern count: 14 → 17. |
