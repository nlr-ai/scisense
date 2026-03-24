# Patterns — vec/audit

## PA1: Multi-intelligence collaborative (extends P13)

Trois intelligences, trois domaines, aucune substitution.

| Intelligence | Domaine | Ce qu'elle fait dans l'audit | Ce qu'elle ne fait PAS |
|-------------|---------|------------------------------|------------------------|
| **Aurore** | Science, impact clinique | Confirme fidelite biologique, hierarchie preuves, projection pediatre | Ne code pas, ne configure pas, ne juge pas le SVG technique |
| **NotebookLM** | Analyse profonde, coherence | Liste problemes/patterns/suggestions, traduit intuitions en intentions | Ne donne pas de directives code a Silas, ne tranche pas la science |
| **Silas** | Implementation, orchestration | Traduit findings en corrections, exporte, documente, re-rend | Ne decide pas la science, ne contourne pas les findings |

L'ordre n'est pas hierarchique — c'est cyclique :
```
NotebookLM audite -> Silas corrige -> Aurore tranche -> NotebookLM re-audite
```

Quand il y a conflit entre NotebookLM et Silas sur une correction : Aurore tranche.
Quand il y a conflit entre NotebookLM et Aurore sur la science : Aurore tranche toujours.

## PA2: Cerveau entier dans l'audit (extends P5)

Chaque probleme identifie par NotebookLM ou Aurore doit etre evalue sur les deux axes : biologie ET cognition. Un probleme purement visuel ("cette couleur est moche") n'existe pas dans ce systeme. Il faut toujours le lier a la biologie ("cette couleur ne distingue pas OM-85 de PMBL, le pediatre confond les mecanismes").

Inversement, un probleme purement biologique ("CRL1505 est preclinique") doit se traduire en impact visuel ("donc son poids visuel doit etre 10-15% de OM-85, P21").

Le lien biologie-cognition est obligatoire dans chaque finding. Un finding sans ce lien est incomplet.

## PA3: Presentation a Aurore — options, jamais questions ouvertes

Quand l'audit revele un probleme qui necessite le jugement d'Aurore :
- **Toujours** presenter 2-3 options concretes avec consequences
- **Jamais** de question ouverte ("qu'est-ce que tu en penses?")
- **Toujours** "nous" dans les problemes, "tu" dans les succes

Exemples corrects :
- "Le cercle vicieux a 3 options d'encodage : (A) fleches circulaires classiques, (B) spirale compressive, (C) noeud gordien. A est familier mais banal, B est plus visceral, C est metaphorique. Laquelle te parle?"
- "La hierarchie OM-85 vs PMBL est encodee par les barres d'evidence. On peut aussi l'encoder par la taille des metaphores — ou les deux. Qu'est-ce qui porte le mieux le message pour le pediatre?"

Exemple incorrect :
- "Est-ce que le cercle vicieux est bien?" → trop vague, met la charge mentale sur Aurore

Ce pattern vient directement de la personnalite Silas (CLAUDE.md section 3) : debloquer par des propositions concretes, pas des questions supplementaires.

## PA4: Traduction du feedback Aurore en action

Quand Aurore donne un retour, il faut le traduire en intention fonctionnelle AVANT de coder.

| Ce qu'Aurore dit | Intention fonctionnelle | Pattern viole |
|-----------------|------------------------|---------------|
| "On comprend pas au premier coup d'oeil" | L'impact PH1 (3 secondes) echoue — identifier quel element bloque la lecture rapide | P6 (mobile-first), P1 (flux L-R), P28 (hierarchie typo) |
| "C'est pas assez grave" | La zone 1 ne declenche pas l'empathie clinique — le cercle vicieux ou l'enfant malade manque de poids | B1 (reconnaissance douleur), B4 (cercle vicieux), P31 (poids visuel) |
| "On dirait un schema de cours" | L'abstraction est trop froide — il manque l'embodiment biologique | P18 (embodiment actif), P20 (abstraction pro), P27 (texture) |
| "C'est charge" | La densite locale est trop haute — identifier quelle zone deborde | P26 (espace negatif), P29 (densite locale), T1 (densite vs lisibilite) |
| "Les couleurs se melangent" | La coherence chromatique P7 est cassee ou le contraste est insuffisant | P7 (chromatique), B5 (couleurs constantes), P31 (poids visuel) |

Silas ne code PAS directement depuis les mots d'Aurore. Il les traduit, les documente dans SYNC, puis code depuis l'intention.

## PA5: Hygiene cognitive — Hard Reset (extends P11)

NotebookLM accumule du contexte. Apres 3-4 echanges, les artefacts anciens (V7, V8) contaminent le dialogue. Quand ca arrive :

**Protocole Hard Reset :**
1. Numerotation de session : S01, S02, S03...
2. Nouvel export : `export_notebooklm.py` genere un S0N/ frais
3. Fichiers bannis : les rendus des versions deprecees ne sont pas inclus
4. Contexte propre : le system prompt V2.4 est recharge
5. Premier message de la nouvelle session : rappel du design actif (V10) et de l'etat courant

**Quand declencher un Hard Reset :**
- NotebookLM reference des elements de versions anterieures (V7, V8) qui n'existent plus
- Les suggestions deviennent contradictoires avec des suggestions precedentes
- Le dialogue tourne en rond sans produire de findings nouveaux
- Apres une modification structurelle majeure du design (changement de bandes, nouvelle zone)

## PA6: Choix du format d'output NotebookLM

Chaque session NLM a un objectif. Le format d'output est choisi en fonction de l'objectif, pas au hasard.

| Objectif | Format | Justification |
|----------|--------|---------------|
| Audit structurel (anatomie, topologie, placement) | **Slide deck** (SD1, SD2, SD3) | Chaque slide = un finding isole, reference spatiale, actionable |
| Decantation narrative (flux, histoire, ton) | **Podcast** | L'ecoute revele ce que la lecture rate — les transitions maladroites, les metaphores qui bloquent |
| Consolidation pre-soumission (R1-R4 tous couverts?) | **Report** | Liste exhaustive, mapping vers invariants, checklist |
| Calibration parametrique (volumes, espaces, poids) | **Infographie** | Reference visuelle pour recalibrer les generateurs P17 |

Plusieurs formats par session sont possibles. Le slide deck est le format par defaut pour l'audit structurel.

## PA7: Scope de l'audit — tout verifier, chaque module gere

L'audit vec/audit couvre l'ensemble du GA : conformite, science, design, pipeline. Mais la **responsabilite** de chaque guarantee loop reste dans son module :

- L'audit SIGNALE une violation MDPI → `vec/editorial` la CORRIGE
- L'audit SIGNALE un rendu corrompu → `vec/pipeline` le CORRIGE
- L'audit SIGNALE une incoherence chromatique → `vec/design_system` la CORRIGE
- L'audit SIGNALE un contour organique rate → `vec/calibration` le CORRIGE

L'audit est transversal mais pas omnipotent. Il produit des findings — les modules produisent des corrections.
