# OBJECTIVES — vec/orchestration

## O-ORC1: Goal

Garantir que le flux CONCEPT -> COMPILATION -> AUDIT -> VALIDATION s'execute sans phase sautee, sans gate ignore, et sans regression entre sessions. L'orchestration est le systeme nerveux du VEC — il ne produit rien lui-meme, mais il garantit que les 6 autres modules (pipeline, editorial, design_system, calibration, audit, exploration) s'enchainent dans le bon ordre avec les bonnes conditions de transition.

Delivers R-ORC1 through R-ORC6.

## Non-Goals

- **NO-ORC1: Pas d'automatisation du jugement humain.** L'orchestration gere les gates, pas les decisions. Le GO d'Aurore (CONCEPT), le sign-off scientifique (VALIDATION), et les pivots architecturaux (NLR) restent des actes humains explicites. Aucun gate humain ne peut etre auto-ferme par timeout ou inference.

- **NO-ORC2: Pas de parallelisation des phases.** Les 4 phases sont sequentielles par design. CONCEPT avant COMPILATION, COMPILATION avant AUDIT, AUDIT avant VALIDATION. Les raccourcis sont le premier vecteur de regression. La seule parallelisation permise est INTRA-phase (ex: 3 agents paralleles en CONCEPT via A2, sub-agents paralleles en AUDIT via A9).

- **NO-ORC3: Pas de gestion de contenu.** L'orchestration ne sait pas ce que contient le GA. Elle sait seulement si les gates sont ouverts ou fermes. Le contenu scientifique est le domaine de la mission (docs/immunomodulator/), le contenu visuel est le domaine du design_system et de la calibration.

- **NO-ORC4: Pas de scheduling temporel.** L'orchestration ne planifie pas de deadlines ni d'horaires de session. Elle gere l'etat (quelle phase, quels gates, quels bloqueurs), pas le calendrier.

## Priorites (ranked)

1. **Integrite des transitions** — Aucune phase n'est sautee, aucun gate n'est ignore. (R-ORC1, R-ORC2, R-ORC3, R-ORC4)
2. **Proprete des sessions** — Chaque session demarre avec un etat cognitif propre. (R-ORC5)
3. **Anti-regression** — Les versions precedentes ne contaminent pas les nouvelles. (R-ORC6)
4. **Tracabilite** — Chaque transition est documentee avec raison et timestamp. (SYNC)

## Tradeoffs

- **T-ORC1: Rigueur vs vitesse.** Les gates ralentissent le flux. Un GA pourrait etre soumis plus vite sans audit NotebookLM. Mais un GA soumis avec des erreurs scientifiques (H2 FAIL) ou des violations MDPI (H1 FAIL) coute plus cher en revision que le temps de l'audit. L'orchestration privilegie la certitude sur la rapidite.

- **T-ORC2: Exhaustivite SYNC vs lisibilite.** Un SYNC trop detaille devient illisible. Un SYNC trop concis perd le contexte inter-sessions. L'equilibre: phase courante + gates ouverts + prochaine action + bloqueurs + numero de version. Pas plus, pas moins.

- **T-ORC3: Autonomie des modules vs controle central.** Chaque module VEC (pipeline, editorial, etc.) a sa propre doc chain et ses propres health checks. L'orchestration ne les micro-manage pas — elle verifie les RESULTATS des modules (H1 PASS? H5 PASS?) sans se substituer a leurs mecanismes internes.
