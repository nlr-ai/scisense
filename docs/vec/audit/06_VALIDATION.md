# Validation — vec/audit

## Invariants (MUST)

**V-AUD1: Separation des roles.** NotebookLM LISTE des problemes/patterns/suggestions. Il ne DONNE PAS de directives code a Silas ("configure tel YAML", "ajuste telle coordonnee"). Si NotebookLM derive vers le code, rappeler le system prompt V2.4 section 4. Violation = bruit dans le processus, Silas perd du temps a filtrer.

**V-AUD2: Sign-off explicite.** Le silence d'Aurore n'est PAS un accord. H2 PASS necessite une reponse explicite (oui, ou corrections). Pas d'interpretation, pas de "elle a reagi avec un emoji donc c'est valide". Violation = GA potentiellement incorrect livre.

**V-AUD3: Options concretes obligatoires.** Chaque interaction avec Aurore contient 2-3 options avec consequences. Pas de question ouverte sans cadre. Violation = paralysie decisionnelle d'Aurore, blocage du processus.

**V-AUD4: Lien biologie-cognition obligatoire.** Chaque finding identifie par NotebookLM ou Aurore doit etre exprime sur les deux axes : ce que ca change biologiquement ET ce que ca change cognitivement pour le pediatre. Un finding sur un seul axe est incomplet. Violation = correction cosmetique sans valeur scientifique, ou correction scientifique invisible.

**V-AUD5: Export propre.** L'export S0N/ ne contient que les fichiers de la version courante. Les rendus de versions deprecees (V7, V8) sont EXCLUS. Violation = NotebookLM audite un fantome, findings inutiles.

**V-AUD6: Resolution tracable.** Chaque probleme identifie a une resolution dans SYNC : commit, gap connu justifie, ou escalade. Aucun finding sans resolution. Violation = problemes qui s'accumulent, memes failles reviennent.

## Invariants (NEVER)

**VN-AUD1: JAMAIS de presentation a Aurore sans audit NLM prealable.** L'exception : phase CONCEPT (A8/P24) ou les propositions ASCII n'ont pas encore de contenu auditable. Des que le premier wireframe E2E existe, NotebookLM passe avant Aurore.

**VN-AUD2: JAMAIS de Hard Reset sans documentation.** Chaque Hard Reset est note dans SYNC avec le numero de session et la raison. Pas de reset silencieux.

**VN-AUD3: JAMAIS de rejet silencieux d'un finding NLM.** Si Silas decide qu'un finding NotebookLM n'est pas pertinent, il le documente avec justification dans SYNC. Pas de suppression discrete.
