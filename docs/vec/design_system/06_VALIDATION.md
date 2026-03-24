# Validation — vec/design_system

Invariants du design system. Regles absolues qui doivent toujours etre vraies.

---

## Invariants chromatiques

**DS-V1: Palette canonique immuable.** Les 5 hex codes de la palette canonique ne changent JAMAIS dans un GA donne : OM-85=#2563EB, PMBL=#0D9488, MV130=#7C3AED, CRL1505=#059669, virus=#DC2626. Ils sont definis dans palette.yaml et c'est la single source of truth. Toute modification de palette passe par un changement de config, jamais par un hardcode dans le script. Violation = coherence chromatique brisee (DS-R1 echoue). Health: DS-H1.

**DS-V2: Rouge exclusivement pathologique.** Le rouge #DC2626 ne peut JAMAIS etre utilise pour un produit therapeutique, un element positif, ou une information neutre. Il est reserve aux virus, au cercle vicieux, a l'inflammation, et aux elements pathologiques. Violation = confusion semantique. Health: DS-H1.

**DS-V3: Pas de degrade inter-produit.** Aucun gradient ne doit melanger deux couleurs-produit (ex: bleu→teal). Chaque couleur reste pure sur son element. Les degrades sont autorises uniquement pour les fonds (neutres desatures) et les transitions anatomiques (amber→vert sur le muscle lisse). Violation = identite produit brouille. Health: DS-H1.

---

## Invariants typographiques

**DS-V4: Budget 30 mots (extends V3 mission).** Le GA contient au maximum 30 mots. Ce sont des labels courts (1-3 mots), pas des phrases. Aucun bloc de texte. Violation = rejet MDPI. Health: DS-H3.

**DS-V5: 3 niveaux typographiques distincts.** Chaque label du GA appartient a exactement un des 3 niveaux (ancre >= 32, contexte 24-30, ponctuation 18-22 au format 3x). Il n'existe pas de "niveau intermediaire". Si un label ne rentre dans aucun niveau, il doit etre reclasse ou supprime. Health: DS-H3.

**DS-V6: Lisibilite V7 pour tous les niveaux.** Tous les niveaux typographiques presents dans le GA doivent etre lisibles a 50% zoom (550x280). Le Niveau 3 est supprime (pas reduit) si il ne passe pas V7. Health: DS-H3.

**DS-V7: Niveau 1 hors bronche.** Les labels de Niveau 1 (ancre) sont toujours places HORS de la bronche (dans les marges ou la legende). Ils sont les premiers elements lus et ne doivent pas etre noyes dans la complexite anatomique. Health: DS-H3.

---

## Invariants spatiaux

**DS-V8: Respiration 5%.** Chaque element visuel majeur (enfant, bronche, barres d'evidence, cercle vicieux) a un espace de respiration d'au moins 5% de sa propre dimension autour de lui. Un element qui touche un bord ou un voisin sans air = violation. Health: DS-H4.

**DS-V9: Lumen majoritairement vide.** Le lumen de la bronche est un espace negatif fonctionnel. Au moins 60% de sa surface doit etre du fond visible (air). Les virus (gauche) et les IgA (droite) sont les seuls elements autorises dans le lumen, et ils n'occupent qu'une fraction de l'espace. Violation = lumen surcharge, le pediatre ne lit pas "air qui passe". Health: DS-H4.

**DS-V10: Hierarchie de poids visuel respectee.** La hierarchie suivante doit etre respectee :
```
enfants > bronche > evidence_bars > cercle_vicieux > legende > arc_crl1505
```
Un element de rang inferieur ne peut pas avoir un poids visuel (aire x opacite x contraste x saturation) superieur a un element de rang superieur. Health: DS-H4.

**DS-V11: Gradient de densite L→R.** Zone 1 est la moins dense (faible), Zone 2 la plus dense (haute), Zone 3 est intermediaire (moyenne). Si Z1 devient plus dense que Z3, le flux de lecture est compromis (P1 + P29). Health: DS-H4.

---

## Invariants biologiques

**DS-V12: Embodiment obligatoire.** Chaque agent therapeutique (OM-85, PMBL, MV130, CRL1505) est en contact physique avec son substrat biologique dans le SVG. Aucun agent ne flotte dans le vide. Violation = le mecanisme d'action est invisible (P18). Health: verification visuelle.

**DS-V13: Topologie 3 niveaux.** Les 3 niveaux topologiques (intracellulaire = MV130 dans DC, surface = OM-85/PMBL sur mur, systemique = CRL1505 arc du bas) sont spatialement distincts. Deux agents de niveaux differents ne peuvent pas etre au meme endroit. Violation = confusion mecanisme d'action (P19, V13 mission). Health: verification visuelle.

**DS-V14: IgA dans le lumen apical.** Les formes Y (IgA secretoires) sont positionnees dans le lumen, au-dessus du mur repare. PAS dans le mur. PAS dans la lamina propria. Elles sont transcytees a travers l'epithelium pour neutraliser les virus dans le lumen. Violation = erreur biologique (P22). Health: H7.

**DS-V15: Point de convergence IgA unique.** Les 4 flux-produits convergent vers un seul point focal dans le lumen. Pas 2 points. Pas 4 points separes. Un point = un resultat (B8). Health: H7.

---

## Invariants de fracture

**DS-V16: Cercle vicieux ferme.** Le cercle vicieux en Zone 1 est une boucle fermee (4 stations connectees circulairement). Si le cercle n'est pas ferme, le message "piege auto-entretenu" est perdu. Health: H8.

**DS-V17: Fracture explicite.** La lance verte doit physiquement traverser le cercle rouge. Pas le contourner, pas le fondre, pas le faire disparaitre progressivement. La fracture est un acte graphique — une rupture visible. Health: H8.

---

## Checklist compacte

```
CHROMATIQUES     DS-V1  palette canonique immuable
                 DS-V2  rouge exclusivement pathologique
                 DS-V3  pas de degrade inter-produit

TYPOGRAPHIQUES   DS-V4  budget 30 mots
                 DS-V5  3 niveaux distincts
                 DS-V6  lisibilite V7 tous niveaux
                 DS-V7  Niveau 1 hors bronche

SPATIAUX         DS-V8  respiration 5%
                 DS-V9  lumen majoritairement vide
                 DS-V10 hierarchie poids visuel
                 DS-V11 gradient densite L→R

BIOLOGIQUES      DS-V12 embodiment obligatoire
                 DS-V13 topologie 3 niveaux
                 DS-V14 IgA dans lumen apical
                 DS-V15 convergence IgA unique

FRACTURE         DS-V16 cercle vicieux ferme
                 DS-V17 fracture explicite
```
