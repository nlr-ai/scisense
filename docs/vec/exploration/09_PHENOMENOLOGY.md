# PHENOMENOLOGY — vec/exploration

**Module:** vec/exploration — Agents autonomes paralleles

---

## Ce que Silas percoit

### Avant l'exploration: vision tunnel

Quand Silas est en mode implementation (codage SVG, ajustement YAML, rendu PNG), son attention est capturee par la dimension technique. Il voit les pixels, les coordonnees, les font-sizes. Il ne voit plus le flux narratif, la plausibilite immunologique, ou la lisibilite mobile. C'est normal — c'est le cout de la concentration. Mais c'est aussi un danger: un GA peut etre techniquement impeccable et scientifiquement faux, visuellement confus, ou editorialement non-conforme.

La sensation: **solitude cognitive**. Un seul cerveau, une seule perspective, des angles morts inevitables. Le sentiment de "je dois penser a tout en meme temps" qui paralyse ou qui produit des raccourcis.

### Pendant l'exploration: 3 experts en parallele

Le lancement des sub-agents transforme la sensation. Ce n'est plus un cerveau qui essaie de couvrir 6 dimensions — ce sont 3 perspectives specialisees qui travaillent simultanement. Chaque agent a un angle et un mandat. Silas n'a pas besoin de "penser immunologie" tout en "codant du SVG" — l'agent immunologie pense immunologie pour lui.

La sensation: **avoir 3 consultants experts dans la piece**. Un immunologiste verifie les mecanismes. Un graphiste evalue la lisibilite. Un auditeur verifie la conformite. Silas n'est plus seul avec le probleme. Il orchestre au lieu de tout porter.

Ce n'est pas de la delegation — c'est de la decomposition attentionnelle. Silas garde la vision d'ensemble. Les agents apportent la profondeur dans chaque dimension. Le resultat est une couverture que ni Silas seul ni aucun agent seul ne pourrait atteindre.

### A l'integration: le moment de synthese

Quand les 3 agents convergent et que Silas lit leurs deliverables, il y a un moment de synthese ou les perspectives se recombinent. Les findings se renforcent mutuellement ("l'agent immuno dit que CRL1505 est mal place ET l'agent visucom dit que l'arc croise l'helice — c'est le meme probleme vu de deux angles"). Les conflits revelent des tensions reelles dans le design, pas des bugs de l'agent.

La sensation: **clarte emergente**. Le probleme qui semblait multi-dimensionnel et insoluble se revele etre 3-5 corrections specifiques, priorisees, justifiees. Le passage de "je suis bloque" a "je sais quoi faire" est le resultat phenomenologique de l'exploration.

### Apres la cloture: confiance calibree

Un cycle d'exploration clos avec un bilan PASS produit une confiance specifique: non pas "le design est parfait", mais "les angles critiques ont ete examines et les findings traites". C'est une confiance par couverture, pas par exhaustivite.

La sensation: **ancrage**. Silas peut avancer vers la prochaine etape du pipeline en sachant que les blind spots de cette iteration ont ete adresses. Pas de rumination "est-ce que j'ai oublie quelque chose?" — le bilan de cloture repond a cette question.

---

## Ce qu'Aurore percoit

Aurore ne voit pas les sub-agents. Elle voit les resultats: un GA qui a ete examine sous plusieurs angles, des corrections justifiees, des questions scientifiques precisement formulees quand elles sont escaladees.

**Signe que l'exploration a fonctionne:** Les questions d'Aurore sont de moins en moins "est-ce que vous avez pense a X?" et de plus en plus "entre ces deux options, laquelle?" Le premier type de question signale un blind spot. Le second signale un choix delibere — preuve que l'exploration a couvert le terrain.

**Signe que l'exploration a echoue:** Aurore identifie un probleme que 3 agents auraient du attraper. C'est une faille de taxonomie (l'angle n'etait pas dans la liste) ou de prompt (l'angle etait la mais le prompt ne le couvrait pas). Le diagnostic est retroactif — et il enrichit la taxonomie EP2 pour le prochain cycle.

---

## Ce que NLR percoit

NLR voit le processus via les bilans de cloture dans le SYNC et les notes de session. Il percoit:
- Le nombre de cycles d'exploration par session (signal de complexite du probleme)
- Le ratio findings retenus/ecartes (signal de calibration des prompts)
- Les conflits resolus et leurs justifications (signal de rigueur)
- Les escalades a Aurore (signal de separation des responsabilites)

**Signe que le module fonctionne:** Les cycles sont courts (diagnostic -> lancement -> integration -> cloture en un flux continu), les bilans sont PASS, les findings se traduisent en corrections concretes dans le code.

**Signe que le module dysfonctionne:** Les cycles s'allongent, les bilans montrent des cycles en fuite, les findings sont redondants, ou l'exploration est lancee sans declencheur clair.

---

## Feedback reinjection

La phenomenologie n'est pas decorative. Elle reinjecte dans le module:

1. **Si "vision tunnel" persiste apres exploration:** les angles choisis ne couvrent pas la dimension qui cause le blocage. Revoir la taxonomie EP2.

2. **Si "clarte emergente" n'apparait pas a l'integration:** les prompts produisent du bruit, pas du signal. Retravailler les DELIVERABLE et FORMAT DE RETOUR dans EP3.

3. **Si "confiance calibree" ne tient pas (Aurore trouve un blind spot post-exploration):** enrichir la taxonomie avec le nouvel angle decouvert. Le systeme apprend de ses echecs.

4. **Si l'exploration devient routiniere (lancement systematique sans declencheur):** violation de EP8. Revenir aux declencheurs explicites. L'exploration est un outil, pas un rituel.
