# VALIDATION — vec/orchestration

## Invariants (MUST)

**V-ORC1: Phases sequentielles.** Le flux DOIT respecter l'ordre CONCEPT -> COMPILATION -> AUDIT -> VALIDATION. Aucune phase ne peut etre sautee. Violation = regression non-detectable.

**V-ORC2: Gate explicite a chaque transition.** Chaque transition DOIT passer par un gate binaire (PASS/FAIL) avec des conditions mesurables. Violation = progression sans verification.

**V-ORC3: SYNC a jour en fin de session.** Le SYNC DOIT refleter l'etat reel du projet en fin de chaque session (phase courante, gates, prochaine action, bloqueurs, version). Violation = fantome cognitif en session suivante.

**V-ORC4: GO Aurore avant compilation.** Aucune ligne de compose_ga_v10.py ne DOIT etre executee avant le GO explicite d'Aurore sur la direction conceptuelle (G1 PASS). Violation = jours de travail potentiellement dans la mauvaise direction.

**V-ORC5: H1 + H5 PASS avant audit.** Le wireframe ne DOIT PAS etre soumis a l'audit NotebookLM tant que validate_ga.py n'a pas retourne PASS (H1) et que le pipeline E2E n'est pas complet (H5). Violation = audit qui revele des problemes deja detectables automatiquement.

**V-ORC6: Zero critique ouvert avant validation.** Aucun probleme identifie comme "critique" dans l'audit NLM ne DOIT rester ouvert au moment du passage en VALIDATION (G3). Violation = Aurore perd son temps sur un GA avec des problemes connus.

**V-ORC7: Diagnostic obligatoire en ITERATE.** Quand VALIDATION echoue (G4 FAIL), le gate echoue ET la cause DOIVENT etre identifies explicitement. "Ca ne marche pas" n'est pas un diagnostic. Violation = boucle infinie sans correction ciblee.

## Invariants (NEVER)

**VN-ORC1: JAMAIS de phase sautee.** Meme si "le GA a l'air bon sans audit" ou "Aurore n'a pas le temps pour le concept". Les gates existent pour attraper ce que l'intuition ne detecte pas.

**VN-ORC2: JAMAIS de gate auto-ferme par timeout.** Si Aurore ne repond pas au GO concept, on attend. On ne se dit pas "pas de reponse = GO implicite". Les gates humains sont explicites ou ils ne sont pas.

**VN-ORC3: JAMAIS de wireframe vN-1 charge dans une session vN sans justification.** Les fantomes des versions precedentes contaminent le contexte. Si un ancien wireframe est necessaire pour comparaison, documenter la raison dans SYNC.

**VN-ORC4: JAMAIS d'ecrasement d'artefact.** Les fichiers wireframe_GA_vN ne sont jamais ecrases par wireframe_GA_vN+1. Le numerotage est monotone croissant. La tracabilite est non-negociable.

## Checklist de transition

| Transition | Conditions | Check |
|------------|-----------|-------|
| CONCEPT -> COMPILATION (G1) | GO explicite Aurore | Document: message Aurore avec GO + direction choisie |
| COMPILATION -> AUDIT (G2) | H1 PASS + H5 PASS + P25 PASS | Script: validate_ga.py PASS + pipeline E2E OK + visuel documente |
| AUDIT -> VALIDATION (G3) | H6 PASS + zero critique ouvert | Document: rapport NLM + checklist problemes tous resolus/documentes |
| VALIDATION -> SHIP (G4) | H2 PASS + R1-R4 fermes | Document: sign-off Aurore + R-status table |
| VALIDATION -> ITERATE (G5) | Gate echoue + diagnostic + phase retour | Document: SYNC mis a jour avec diagnostic et phase de retour |
