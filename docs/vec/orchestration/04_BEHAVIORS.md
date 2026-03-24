# BEHAVIORS — vec/orchestration

## B-ORC1: Le flux avance d'une phase a la suivante sans saut

Le comportement observable: le GA passe par les 4 phases dans l'ordre exact CONCEPT -> COMPILATION -> AUDIT -> VALIDATION. Un observateur peut verifier dans le SYNC que chaque phase a ete completee et que chaque gate a ete franchi avant la suivante.

Implemente P-ORC1 (phases sequentielles). Valide par R-ORC1 (concept GO), R-ORC2 (compilation valide), R-ORC3 (audit complet), R-ORC4 (validation ferme).

## B-ORC2: Un gate FAIL bloque la progression

Le comportement observable: quand un gate retourne FAIL, la phase suivante n'est PAS entamee. L'agent documente l'echec dans SYNC, identifie la cause, et corrige dans la phase courante ou retourne a une phase anterieure.

Pas de contournement. Un "H1 FAIL mais on continue parce qu'on va corriger apres" est une violation. On corrige D'ABORD, on passe le gate ENSUITE.

Implemente P-ORC2 (gate explicite). Valide par R-ORC2 (compilation valide avant audit).

## B-ORC3: Chaque session commence par la lecture du SYNC

Le comportement observable: la premiere action de chaque session est `Read 10_SYNC.md`. L'agent ne commence pas par "ou en etait-on?" — il sait ou on en est parce que le SYNC le dit. Si le SYNC est obsolete, sa mise a jour est la premiere action.

Implemente P-ORC3 (SYNC comme memoire). Valide par R-ORC5 (sessions propres).

## B-ORC4: Le SYNC est mis a jour en fin de chaque session

Le comportement observable: la derniere action significative de chaque session est la mise a jour du SYNC avec: phase courante, gates ouverts, prochaine action, bloqueurs, numero de version. Un agent qui quitte une session sans mettre a jour le SYNC cree un fantome pour la session suivante.

Implemente P-ORC3 (SYNC comme memoire). Valide par R-ORC5 (sessions propres).

## B-ORC5: Les artefacts precedents ne sont jamais ecrases

Le comportement observable: apres la production de la version vN, les fichiers de la version vN-1 existent toujours et n'ont pas ete modifies. Le numerotage est monotone croissant. Un agent qui ecrase v8 avec v9 detruit la tracabilite et empeche la comparaison.

Implemente P-ORC5 (hard reset) + P11 (version archival). Valide par R-ORC6 (pas de regression).

## B-ORC6: Les fichiers bannis sont exclus des exports

Le comportement observable: le repertoire S0N/ genere par export_notebooklm.py ne contient AUCUN fichier de la liste de fichiers bannis. Les fantomes des versions precedentes ne sont pas charges dans NotebookLM.

Implemente P-ORC4 (export S0N/) + P-ORC5 (hard reset). Valide par R-ORC6 (pas de regression).

## B-ORC7: Iterate identifie le gate et la phase de retour

Le comportement observable: quand un GA est rejete en VALIDATION, l'agent ne retourne pas systematiquement au debut. Il identifie le gate specifique qui echoue (H1? H2? H5? H6?), documente le diagnostic, et retourne a la phase correspondante. Le SYNC reflete le retour: "Phase: COMPILATION (retour depuis VALIDATION, H1 FAIL: word count 33 > 30)".

Implemente P-ORC7 (iterate retourne a la phase pertinente). Valide par R-ORC4 (validation ferme).

## B-ORC8: La bonne intelligence est mobilisee a la bonne phase

Le comportement observable: Aurore est sollicitee en CONCEPT et VALIDATION, pas en COMPILATION. NotebookLM est sollicite en AUDIT, pas en CONCEPT. Les scripts sont executes en COMPILATION et AUDIT, pas en CONCEPT.

Violation typique: "Aurore, peux-tu verifier que le pipeline SVG fonctionne?" — ce n'est pas son domaine. "NotebookLM, valide la science du GA" — ce n'est pas son role, c'est celui d'Aurore.

Implemente P-ORC6 (7 intelligences assignees). Valide par R-ORC2 (compilation valide) + R-ORC3 (audit complet) + R-ORC4 (validation ferme).
