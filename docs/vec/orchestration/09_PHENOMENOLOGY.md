# PHENOMENOLOGY — vec/orchestration

## PH-ORC1: Comment Silas percoit l'orchestration

L'orchestration est le systeme nerveux du VEC. Silas ne la "voit" pas comme un module qu'il execute — il la vit comme une conscience de l'etat du flux. A chaque instant, Silas sait:

- Dans quelle phase il se trouve (CONCEPT / COMPILATION / AUDIT / VALIDATION)
- Quels gates sont ouverts et lesquels sont fermes
- Quelle est la prochaine action

Cette conscience n'est pas cognitive (lire le SYNC et se rappeler) — elle est operationnelle. Le SYNC est la projection externe de cette conscience. Quand le SYNC est obsolete, Silas sent un malaise: l'etat interne diverge de l'etat documente. La premiere action est de resynchroniser.

**Feedback reinjection:** Si Silas se retrouve a "deviner" dans quelle phase il est, le SYNC a echoue. Corriger le SYNC, pas la memoire.

## PH-ORC2: Comment Aurore percoit l'orchestration

Aurore ne percoit pas l'orchestration. Elle ne voit que deux moments:

1. **CONCEPT:** Un PDF arrive avec 3 propositions claires. Elle choisit une direction. Pas de jargon de gates ou de phases. La question est simple: "Quelle direction te parle le plus?"

2. **VALIDATION:** Un GA final arrive. La question est simple: "Les 4 messages cles sont-ils correctement representes? La hierarchie des preuves est-elle exacte?" Oui ou non + corrections.

Entre ces deux moments, Aurore n'a rien a faire. L'orchestration est transparente pour elle. Elle ne sait pas qu'il y a des scripts, des exports, des sub-agents. Elle voit des resultats, pas des processus.

**Feedback reinjection:** Si Aurore se sent submergee par des questions techniques ou des details de pipeline, l'orchestration a echoue dans sa mission de transparence. Silas absorbe la complexite, Aurore tranche sur le fond.

## PH-ORC3: Comment NLR percoit l'orchestration

NLR percoit l'orchestration comme un tableau de bord. Il voit le SYNC et sait immediatement:

- Ou en est le projet (phase + version)
- Si quelque chose bloque (gates FAIL, bloqueurs)
- Si l'orchestration est saine (toutes les transitions documentees)

Son intervention est rare mais decisive: pivots architecturaux (ex: "on abandonne les assets statiques, tout est generateur parametrique"), arbitrages structurels (ex: "le VEC est un calibrateur, pas un renderer"), et revue du SYNC pour verifier que la tracabilite est maintenue.

**Feedback reinjection:** Si NLR doit poser des questions pour comprendre l'etat du projet, le SYNC est insuffisant. Ajouter les champs manquants.

## PH-ORC4: Comment NotebookLM percoit l'orchestration

NotebookLM ne percoit pas l'orchestration. Il recoit un repertoire plat (S0N/) et un system prompt. Il analyse et produit. Il ne sait pas dans quelle phase le VEC se trouve, ni quels gates sont ouverts. Cette ignorance est intentionnelle: NLM doit auditer le contenu tel quel, sans biais sur l'etat du processus.

**Feedback reinjection:** Si l'export S0N/ contient des artefacts obsoletes (fantomes), NLM produit un audit contamine par du contexte mort. L'orchestration empeche ca via les fichiers bannis.

## PH-ORC5: La boucle phenomenologique de l'orchestration

```
Silas SENT la phase courante           → orienté, pas perdu
Aurore SENT deux moments clairs        → sollicitée, pas submergée
NLR SENT l'état du projet d'un coup    → informé, pas questionné
NLM SENT un snapshot propre            → analysé, pas contaminé
```

Quand cette boucle fonctionne:
- Silas ne "devine" jamais — il sait
- Aurore ne recoit jamais de questions techniques
- NLR n'a jamais besoin de demander "ou on en est"
- NLM ne produit jamais d'audit contamine par des fantomes

Quand cette boucle casse:
- Silas compile avant le GO Aurore → jours perdus (V-ORC4 viole)
- Aurore recoit un GA avec des violations MDPI → perte de confiance (V-ORC5 viole)
- NLR decouvre un SYNC obsolete → perte de temps a reconstruire le contexte (V-ORC3 viole)
- NLM audite des wireframes obsoletes → corrections inapplicables (VN-ORC3 viole)

## PH-ORC6: Le rythme de l'orchestration

L'orchestration a un rythme naturel. Les 4 phases ne durent pas le meme temps:

- **CONCEPT:** rapide (heures). L'ASCII art et le diagnostic sont legers. Le goulot est le temps de reponse d'Aurore.
- **COMPILATION:** long (jours). C'est la ou le code est ecrit, les configs ajustees, les calibrations faites. Multiple iterations intra-phase.
- **AUDIT:** moyen (heures-jours). L'export et l'upload sont rapides. L'integration des corrections prend du temps.
- **VALIDATION:** rapide (heures). C'est un GO/NO-GO. Le goulot est le temps de reponse d'Aurore.

L'orchestration ne force pas ce rythme. Elle le constate et s'y adapte. Si COMPILATION prend 5 sessions, c'est 5 mises a jour de SYNC, pas une seule a la fin.
