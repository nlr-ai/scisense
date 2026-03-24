# OBJECTIVES — vec/exploration

**Module:** vec/exploration — Agents autonomes paralleles

---

## Objectifs

### O1: Eliminer les blind spots du design par parallelisation des perspectives

Un agent unique (Silas en mode implementation) a une vision tunnel. L'exploration compense ce biais en lancant des agents dedies a des angles specifiques. L'objectif n'est pas la quantite de findings — c'est la couverture des dimensions du probleme.

### O2: Accelerer la convergence vers un design robuste

Sans exploration, la convergence se fait par iteration sequentielle: coder → auditer → corriger → re-auditer. Avec exploration, les problemes multi-dimensionnels sont decomposes en sous-problemes traites en parallele. Le gain n'est pas lineaire (les agents ne sont pas independants), mais la detection precoce de conflits inter-dimensions economise des iterations completes.

### O3: Fournir un cadre reproductible pour le prompt engineering de sub-agents

Chaque sub-agent recoit un prompt structure: scope + angle + deliverable + contraintes + format de retour. Ce cadre est explicite et reproductible. Un autre citoyen qui lance une exploration sur un autre GA de SciSense peut reutiliser la meme taxonomie d'angles et le meme format de prompt.

### O4: Documenter les decisions, pas seulement les resultats

L'exploration ne produit pas seulement des findings. Elle produit des traces de decision: pourquoi tel angle a ete choisi, pourquoi tel finding a ete rejete, pourquoi tel conflit a ete resolu dans un sens plutot qu'un autre. Ces traces sont la memoire du processus.

---

## Non-objectifs

### NO1: Ne pas remplacer le jugement humain

L'exploration parallelise l'analyse, pas la decision. Quand un finding touche a la fidelite scientifique ou a l'esthetique clinique, il est escalade a Aurore (I1) ou NLR (I2). Les sub-agents analysent et proposent. Ils ne tranchent pas.

### NO2: Ne pas explorer pour explorer

L'exploration est declenchee par un besoin identifie: un probleme multi-dimensionnel (>3 dimensions), un blocage (>5 minutes sur une approche unique), ou un audit qui revele des failles dans plusieurs domaines simultanement. Pas de lancement systematique "au cas ou".

### NO3: Ne pas produire de livrables

Les sub-agents ne generent pas de SVG, de PNG, ou de PDF. Ils analysent, diagnostiquent, et proposent. La traduction en code est la responsabilite de Silas (I4) via les modules pipeline (vec/pipeline) et compositeur (A7). Cette separation est stricte: un sub-agent qui code est un sub-agent qui derive.

### NO4: Ne pas depasser 3 agents par sujet

Les rendements marginaux chutent apres le 3eme agent. Cette contrainte n'est pas arbitraire — elle vient de l'observation empirique (cf. R4). Si 3 agents ne suffisent pas, le probleme est mal decompose ou le prompt est mal calibre. Relancer avec de meilleurs angles plutot qu'avec plus d'agents.

---

## Trade-offs

### T1: Profondeur vs. largeur

3 agents couvrant 3 angles differents (largeur) vs. 3 agents creusant le meme angle sous 3 sous-aspects (profondeur). La regle par defaut est la largeur (diversite de perspectives). La profondeur n'est justifiee que lorsqu'un angle specifique a deja revele des failles complexes (ex: la topologie spatiale dans V2-A necessitait a elle seule 3 sous-analyses).

### T2: Foreground vs. background

Foreground = bloquant (Silas attend les resultats avant de continuer). Background = enrichissement (Silas continue et integre plus tard). Le defaut est foreground. Le background est reserve aux explorations d'enrichissement qui ne conditionnent pas la prochaine action immediate. Risque du background: les findings arrivent trop tard et sont obsoletes.

### T3: Autonomie vs. coherence

Chaque agent est autonome (P4). Mais leurs findings doivent etre coherents entre eux. Le protocole d'integration (merge + resolution de conflits) est le mecanisme de coherence. Le trade-off: plus d'autonomie = plus de diversite mais plus de conflits a resoudre. Le plafond de 3 agents est aussi un mecanisme de controle de coherence.
