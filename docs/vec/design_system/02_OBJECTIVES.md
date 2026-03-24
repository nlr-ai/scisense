# Objectives — vec/design_system

## DS-O1: Goal

Definir et appliquer un langage visuel coherent qui traduit la biologie clinique en representation graphique impactante — de maniere a ce que le pediatre comprenne le message en 3 secondes sur ecran mobile, sans lire une seule phrase.

Le design system est le lexique semiotique de SciSense. Il est mission-agnostic dans sa structure (les patterns de couleur, typographie, espace negatif, densite s'appliquent a tout GA) mais parametriquement specialise par mission (la palette, les metaphores, les bandes anatomiques sont injectees par la config).

Delivers DS-R1 a DS-R6.

---

## DS-O2: Non-Goals

**DS-NO1: Pas un guide de style statique.** Le design system n'est pas un PDF de brand guidelines. C'est un ensemble de patterns verifiables implementes dans le code et les configs. Chaque pattern a un sense et un health check.

**DS-NO2: Pas un tutoriel d'anatomie.** Les representations biologiques servent la cognition du pediatre, pas l'exactitude du chercheur. P20 (abstraction professionnelle) impose le line art medical, pas le photorealisme.

**DS-NO3: Pas de decoration.** Chaque element visuel encode de l'information. Un element qui n'encode rien est du bruit (NO3 mission : pas d'illustration decorative).

**DS-NO4: Pas de separation design/science.** Le design EST la science qui encode ses propres mecanismes de transmission (P5). Les patterns visuels ne sont pas des "habillages" appliques apres coup — ils sont les vecteurs de la narration scientifique.

---

## DS-O3: Tradeoffs

**DS-T1: Densite vs lisibilite (extends T1 mission).** On sacrifie la densite d'information moleculaire pour la lisibilite immediate. Pas de listes de cytokines (VN1). Le design system encode cette decision dans P29 (gradient de densite) et P26 (espace negatif).

**DS-T2: Organicite vs reproductibilite.** Les textures organiques (P27) ajoutent du realisme tissu vivant, mais chaque micro-variation doit etre reproductible (seed aleatoire fixe). La texture est une micro-variation, pas un rendu 3D.

**DS-T3: Expressivite vs rigueur Q2.** Les elements visuels doivent declencher l'empathie clinique (enfants, PH1) tout en maintenant l'esthetique de publication Q2 (P20). Le line art medical est le point d'equilibre : expressif et rigoureux.

**DS-T4: Poids visuel vs evidence.** Le poids visuel relatif (P31) doit refleter l'importance clinique ET le niveau de preuve. Un element preclinique ne peut pas peser visuellement autant qu'un element avec 18 RCTs, meme si le mecanisme est fascinant.

---

## DS-O4: Priorites (ranked)

1. **PH1 impact cognitif** — Si le GA ne stoppe pas le scroll en 1s, rien d'autre ne compte. (DS-R2)
2. **Coherence chromatique** — L'identification produit-couleur est le socle de toute la narration. (DS-R1)
3. **Convergence + fracture** — Les deux climax visuels (scientifique et narratif). (DS-R3, DS-R4)
4. **Hierarchie typographique** — Les 30 mots comptent, chacun pese. (DS-R5)
5. **Equilibre spatial** — L'air est aussi important que l'encre. (DS-R6)

---

## DS-O5: Success signals

- Aurore dit "on comprend au premier coup d'oeil" (inverse de son feedback v8.1).
- NotebookLM identifie zero violation de pattern dans l'audit SD.
- Le pediatre non-expert (test informel) identifie "4 produits, 1 objectif" sans explication.
- Tous les DS-H checks PASS.
