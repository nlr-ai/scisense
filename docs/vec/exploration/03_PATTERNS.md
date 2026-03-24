# PATTERNS — vec/exploration

**Module:** vec/exploration — Agents autonomes paralleles

---

## EP1: Agents autonomes en parallele (derives de P4)

Chaque sub-agent est un agent Claude Code lance via `/subcall` avec un prompt structure. Il recoit un perimetre, un angle, un deliverable attendu, des contraintes, et un format de retour. Il ne recoit PAS le contexte complet de la session — uniquement ce qui est necessaire a son angle. Cette isolation est intentionnelle: un agent qui voit tout analyse tout, et le gain de la parallelisation disparait.

L'autonomie signifie: l'agent analyse, auto-critique, et produit son deliverable sans feedback intermediaire de Silas. Silas n'intervient qu'a l'integration.

---

## EP2: Taxonomie des angles

L'exploration n'est pas une recherche libre. Chaque agent recoit un angle tire d'une taxonomie finie. Les 6 angles couvrent les dimensions recurrentes d'un Graphical Abstract scientifique:

| Angle | Ce qu'il examine | Question centrale |
|-------|-----------------|-------------------|
| **Immunologie** | Fidelite des mecanismes d'action, hierarchie des preuves, plausibilite biologique | "Les mecanismes representes sont-ils scientifiquement exacts?" |
| **Communication visuelle** | Lisibilite, impact cognitif, flux de lecture, espace negatif, poids visuel | "Un pediatre comprend-il le message en <3 secondes?" |
| **Matrice produit-mecanisme** | Couverture des N produits dans la structure visuelle, coherence des attributions | "Chaque produit a-t-il sa place, sa couleur, son action distincte?" |
| **Lisibilite mobile** | Test de lecture a 50% zoom, taille des labels, contraste sur petit ecran | "Le GA est-il lisible sur un telephone dans la table des matieres MDPI?" |
| **Benchmarking litterature** | Comparaison avec les GA publies dans le meme journal ou domaine | "Notre GA est-il au niveau des meilleures publications du domaine?" |
| **Conformite editoriale** | Regles MDPI, V1-V7, VN1-VN4, droits visuels | "Le GA passe-t-il le tribunal editorial sans modification?" |

La taxonomie est extensible. Un nouveau projet SciSense peut ajouter des angles (ex: reglementation pour un GA pharma, accessibilite daltonisme pour un GA grand public). Mais les 6 angles de base couvrent >90% des cas.

---

## EP3: Prompt engineering structure

Chaque sub-agent recoit un prompt avec 5 sections obligatoires. Un prompt qui omet une section produit un agent qui derive.

```
## SCOPE
Ce que tu examines (ex: "le wireframe GA V2-A immunomodulateur, version v10")

## ANGLE
Ta perspective specifique (ex: "immunologie — validation des mecanismes d'action")

## DELIVERABLE
Ce que tu dois produire (ex: "liste de failles avec severite + correction proposee")

## CONTRAINTES
Ce que tu ne fais PAS (ex: "tu ne codes pas, tu ne modifies aucun fichier, tu analyses uniquement")

## FORMAT DE RETOUR
Structure exacte de la sortie (ex: "tableau markdown: Faille | Severite | Correction | Reference")
```

Le scope borne l'etendue. L'angle borne la perspective. Le deliverable borne la sortie. Les contraintes empechent la derive. Le format de retour permet l'integration automatisee.

---

## EP4: Plafond de 3 agents par sujet

Au-dela de 3 agents sur un meme sujet, les findings deviennent:
- **Redondants:** le 4eme agent repete ce que le 2eme a deja dit
- **Contradictoires sans valeur:** les conflits entre 4+ agents sont plus couteux a resoudre que les insights qu'ils apportent
- **Diluants:** le bruit augmente, le signal ne bouge plus

Le plafond de 3 est empirique. Si 3 agents ne suffisent pas, la reponse n'est pas d'en lancer un 4eme — c'est de redecomposer le probleme en sous-problemes plus fins et de relancer avec des angles mieux calibres.

---

## EP5: Foreground vs. background

Deux modes de lancement:

| Mode | Quand | Comportement de Silas | Risque |
|------|-------|----------------------|--------|
| **Foreground** | Le resultat conditionne la prochaine action | Silas attend la convergence des agents avant de continuer | Blocage si un agent est lent |
| **Background** | Enrichissement, validation secondaire | Silas continue le flux principal et integre les findings quand ils arrivent | Findings obsoletes si la session avance trop |

**Regle par defaut:** foreground. Le background n'est justifie que pour des explorations qui ne conditionnent pas la prochaine etape immediate du pipeline.

**Exemple foreground:** Pendant l'audit V2-A, 3 agents explorent immunologie/visucom/matrice avant que Silas ne commence les corrections. Les findings orientent les corrections.

**Exemple background:** Apres l'audit V2-A, un agent benchmarking compare le GA avec les 5 derniers GA publies dans MDPI Children. Les findings arrivent pendant la phase de correction et enrichissent les prochaines iterations sans les bloquer.

---

## EP6: Integration par extraction des top insights

Quand les agents convergent, Silas ne lit pas l'integralite de chaque rapport. Il extrait les **3 a 5 findings actionnables** de chaque agent et ecarte le bruit. Le protocol:

1. Lire le deliverable de chaque agent
2. Extraire les findings qui passent le test: "est-ce que ca change quelque chose dans le code, le config, ou la doc?"
3. Ecarter les observations generales, les reformulations du brief, et les compliments
4. Fusionner les findings dans une liste unique, dedupliquee
5. Resoudre les conflits (EP7)

---

## EP7: Resolution de conflits par hierarchie fixe

Quand 2 ou 3 agents retournent des findings contradictoires, la resolution suit une hierarchie stricte:

```
1. Precision scientifique   (le mecanisme biologique est-il exact?)
2. Faisabilite visuelle     (le design est-il implementable en SVG/PNG?)
3. Cout d'implementation    (combien de temps/effort pour la correction?)
```

La precision scientifique prime toujours. Un design visuellement elegant mais scientifiquement inexact est un echec. Un design scientifiquement correct mais visuellement difficile est un defi d'ingenierie — pas un compromis sur la science.

**Cas particulier:** Si un conflit oppose deux interpretations scientifiques (ex: positionnement apical vs. basolateral des IgA), il est escalade a Aurore (I1). Les sub-agents ne tranchent pas les questions scientifiques ambigues.

---

## EP8: Declencheurs d'exploration

L'exploration n'est pas systematique. Elle est declenchee par des conditions specifiques:

| Declencheur | Seuil | Exemple |
|-------------|-------|---------|
| Probleme multi-dimensionnel | >3 dimensions identifiees | "Le GA a des failles immunologiques ET visuelles ET editoriales" |
| Blocage sur approche unique | >5 minutes sans progression | "Je tourne en rond sur le placement de l'arc CRL1505" |
| Audit avec failles multiples | >3 failles dans >2 domaines | "NotebookLM a identifie 10 failles touchant 4 patterns differents" |
| Nouvelle phase du pipeline | Transition CONCEPT->COMPILATION ou COMPILATION->AUDIT | Verification que rien n'a ete oublie au moment de la transition |
| Demande explicite NLR/Aurore | Signal humain | "Explore d'autres angles avant de continuer" |

Si aucun declencheur n'est actif, l'exploration n'a pas lieu. Silas continue le flux principal.
