# BEHAVIORS — vec/exploration

**Module:** vec/exploration — Agents autonomes paralleles

---

## BE1: Lancement cible sur declencheur

Silas ne lance pas d'exploration "au cas ou". Il identifie un declencheur (EP8), formule le probleme en une phrase, choisit les angles pertinents dans la taxonomie (EP2), et lance 1 a 3 agents avec des prompts structures (EP3).

**Observable:** Chaque cycle d'exploration est precede d'un diagnostic explicite dans les notes de session. Le diagnostic contient: le probleme identifie, les dimensions en jeu, les angles choisis, et la justification du mode (foreground/background).

---

## BE2: Production de findings structures

Chaque sub-agent retourne son deliverable dans le format demande (EP3). Les findings sont structures, pas narratifs. Un agent qui retourne un paragraphe de prose au lieu d'un tableau de failles n'a pas respecte son prompt — son output est rejete et l'agent est relance avec un prompt corrige.

**Observable:** Les deliverables des agents sont des tableaux markdown ou des listes structurees. Jamais de prose libre. Le format permet l'extraction automatisee (EP6).

---

## BE3: Integration selective

Silas ne copie pas les findings en bloc. Il extrait les 3 a 5 insights actionnables par agent (EP6), ecarte le bruit, deduplique, et fusionne. L'integration produit une liste unique de corrections classees par priorite.

**Observable:** Apres chaque cycle d'exploration, un bloc d'integration apparait dans les notes de session ou dans le SYNC du module concerne. Ce bloc contient: les findings retenus, les findings ecartes avec justification, et les conflits resolus.

---

## BE4: Resolution de conflits tracee

Quand des findings sont contradictoires, Silas applique la hierarchie EP7 et documente la resolution. La trace contient: les deux positions, la regle de hierarchie appliquee, et la decision finale.

**Observable:** Chaque conflit resolu est documente dans le bloc d'integration (BE3). Aucun conflit n'est resolu silencieusement.

---

## BE5: Escalade des ambiguites scientifiques

Les sub-agents ne tranchent pas les questions scientifiques ambigues. Quand un finding touche a l'interpretation d'un mecanisme biologique, il est marque NEEDS_FEEDBACK et escalade a Aurore.

**Observable:** Les questions escaladees sont formulees de maniere precise et binaire ("Les IgA secretoires sont-elles positionnees en apical ou en basolateral dans ce contexte?"), pas vagues ("Qu'en penses-tu?"). L'escalade inclut le contexte minimal necessaire a la decision.

---

## BE6: Respect du plafond de 3 agents

Silas ne lance jamais plus de 3 agents sur le meme sujet dans le meme cycle. Si les 3 agents ne suffisent pas, le probleme est redecompose avec des angles plus fins et un nouveau cycle est lance.

**Observable:** Les notes de session montrent au maximum 3 lancements par sujet. Toute tentative de lancer un 4eme est accompagnee d'une redecomposition explicite du probleme.

---

## BE7: Distinction foreground/background explicite

Au moment du lancement, Silas declare si l'exploration est foreground (bloquante) ou background (enrichissement). Cette declaration conditionne le comportement: foreground = attente de convergence, background = continuation du flux principal.

**Observable:** Chaque lancement porte la mention "[FG]" ou "[BG]" dans les notes de session. Pas d'ambiguite.

---

## BE8: Clot du cycle avec bilan

Un cycle d'exploration ne reste pas ouvert indefiniment. Il se termine par un bilan: findings integres, findings ecartes, conflits resolus, questions escaladees. Le bilan ferme le cycle et met a jour le SYNC du module concerne.

**Observable:** Chaque cycle a une entree de cloture dans les notes de session ou le SYNC. Un cycle sans cloture est un cycle en fuite — Silas le detecte et le ferme au debut de la session suivante.
