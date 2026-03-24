# RESULTS — vec/exploration

**Module:** vec/exploration — Agents autonomes paralleles
**Guarantee Loop:** RESULT -> SENSE -> HEALTH -> CARRIER

---

## R1: Findings actionnables integres dans le design

Chaque cycle d'exploration produit des findings concrets qui modifient le GA ou sa documentation. Un finding qui ne se traduit pas en action (correction code, mise a jour config, nouveau pattern, decision documentee) n'est pas un finding — c'est du bruit.

**Mesure:** Nombre de findings actionnables extraits par cycle d'exploration, rapporte au nombre d'agents lances. Ratio minimum attendu: 3 findings actionnables pour 3 agents (1:1). Un cycle qui retourne moins de 1 finding actionnable par agent est un signal que les prompts etaient mal calibres ou les angles mal choisis.

**Exemple concret (projet immunomodulateur):** Lors de l'audit V2-A, 3 agents ont explore simultanement l'angle immunologie (validation des mecanismes d'action des 4 produits), l'angle communication visuelle (lisibilite mobile, impact cognitif, flux de lecture), et l'angle matrice produit-mecanisme (couverture des 4 produits dans les 4 bandes anatomiques). Les findings ont produit: correction de la topologie spatiale de CRL1505 (faille 4/5), requalification du poids visuel relatif OM-85 vs CRL1505 (faille 9), et identification du besoin de micro-ancres moleculaires IgA (faille 8).

---

## R2: Zero blind spot dans le design

L'exploration existe pour couvrir les angles que l'agent principal (Silas) ne voit pas quand il est en mode implementation. Le cerveau qui code ne voit pas les memes choses que le cerveau qui audite. La parallelisation des angles garantit que chaque dimension du probleme est examinee par un agent dedie.

**Mesure:** Apres un cycle d'exploration, Silas verifie que les 6 angles de la taxonomie (immunologie, communication visuelle, matrice produit-mecanisme, lisibilite mobile, benchmarking litterature, conformite editoriale) ont ete couverts — soit par l'exploration courante, soit par un cycle precedent. Tout angle non couvert depuis >2 iterations est un blind spot actif.

**Exemple concret:** Sans l'agent "benchmarking litterature", la DC (cellule dendritique) aurait garde une morphologie etoile symetrique (violation P20). L'agent dedie a identifie que la morphologie filopodiale exacte (branches courbes irregulieres, corps vesiculaire) etait requise pour la reconnaissance par un immunologiste en <2 secondes. Ce blind spot n'aurait jamais ete attrape par l'agent qui code le SVG.

---

## R3: Conflits resolus par hierarchie explicite

Quand plusieurs agents retournent des findings contradictoires, le conflit est resolu — jamais ignore. La hierarchie de resolution est fixe et documentee (precision scientifique > faisabilite visuelle > cout d'implementation). Chaque resolution de conflit est tracee avec justification.

**Mesure:** Nombre de conflits inter-agents resolus vs. nombre de conflits detectes. Le ratio doit etre 1:1. Un conflit non resolu en fin de cycle est une violation directe de la Guarantee Loop (un probleme identifie par >1 agent reste sans reponse).

**Exemple concret:** L'agent immunologie a demande un arc CRL1505 qui pointe independamment vers barriere + DC (precision scientifique de l'axe intestin-poumon). L'agent communication visuelle a signale que cet arc croisait l'helice MV130, rendant la zone illisible. Resolution: l'arc passe par le BAS de l'image (systémique = position basse, P19), evitant le croisement tout en preservant la precision du mecanisme. Precision scientifique respectee (priorite 1), lisibilite preservee (priorite 2).

---

## R4: Rendements decroissants controles

L'exploration n'est pas illimitee. Au-dela de 3 agents par sujet, les findings deviennent redondants ou contradictoires sans valeur ajoutee. Le module impose un plafond et mesure le retour marginal de chaque agent supplementaire.

**Mesure:** Nombre de findings actionnables uniques (non-redondants) par agent. Si l'agent N+1 produit <1 finding unique par rapport aux N agents precedents, le plafond est atteint. Historiquement, le ratio chute significativement apres le 3eme agent.

---

## R5: Temps d'exploration borne

L'exploration sert l'avancement, pas la procrastination. Chaque cycle a un budget temps implicite. Les agents foreground (bloquants) doivent converger avant que le flux principal ne reprenne. Les agents background (enrichissement) ont un budget plus souple mais sont neanmoins bornes.

**Mesure:** Temps moyen par cycle d'exploration. Foreground: resolution dans la session courante. Background: resolution avant la prochaine phase du pipeline (CONCEPT -> COMPILATION -> AUDIT -> VALIDATION). Un agent background qui traine au-dela d'une transition de phase est un agent mort — ses findings sont probablement obsoletes.
