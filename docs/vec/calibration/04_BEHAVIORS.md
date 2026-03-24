# Behaviors — vec/calibration

## BC1: Le contour organique declenche la projection clinique

Quand le compositeur injecte le contour calibre (enfant H=0.0) dans Zone 1 du GA, le pediatre projette son patient. Il ne voit pas une forme — il voit un enfant qu'il a deja vu 50 fois dans son cabinet. L'epine courbee, la tete penchee, les bras serres contre le torse : c'est le langage corporel universel de la maladie chronique chez l'enfant. Ce comportement est le premier maillon de la chaine PH1 (premiere seconde du GA).

**Difference observable:** Un stick figure geometrique (lignes droites, joints circles) encode la meme information semantique (enfant malade) mais ne declenche pas la meme resonance. La courbure organique — les epaules qui s'affaissent avec une rondeur naturelle, le dos qui se voute avec une continuite musculaire — est ce qui transforme l'information en emotion.

**Implements:** B7 (pictogramme enfant obligatoire), PH1 (reconnaissance clinique <2s).
**Valide par:** RC2 (test empathie Aurore).

---

## BC2: Le vecteur H raconte la guerison sans mots

La transformation H=0.0 -> H=1.0 est la narration visuelle du GA comprimee en un seul parametre. Zone 1 montre H~0 (malade). Zone 3 montre H~1 (sain). Le pediatre lit la transition sans legende ni explication — le corps de l'enfant dit tout.

**Difference observable:** Sans le vecteur H, les deux enfants (Z1 et Z3) sont des pictogrammes independants. Le pediatre doit les comparer cognitivement. Avec H parametrise, la transformation est continue — le regard glisse de gauche a droite et SENT la guerison, comme un time-lapse compresse.

**Implements:** P15 (vecteur de sante H), P1 (flux gauche-droite).
**Valide par:** RC3 (continuite H verifiee).

---

## BC3: L'image IA disparait du livrable

A aucun moment l'image IA source n'apparait dans le GA final. Le flux est unidirectionnel :

```
Image IA (pixels) -> Pipeline extraction -> Path SVG (code) -> Compositeur -> GA
                                                                 ^
                                                                 |
                                                         pas de lien retour
```

L'image IA peut etre supprimee apres extraction sans impact sur le livrable. C'est la preuve empirique que VN4 est respecte. L'image a informe la geometrie ; elle n'est pas la geometrie.

**Difference observable:** Si on supprime l'image IA source et qu'on re-rend le GA, le resultat est identique bit-pour-bit. Le SVG est auto-suffisant.

**Implements:** P12 (IA = accelerateur), VN4 (zero pixel IA).
**Valide par:** RC4 (grep raster = 0).

---

## BC4: La calibration integrale modifie le rendu de maniere perceptible

Les parametres extraits de l'infographie IA (P17 elargi) — espacements, densite, poids visuels, tonalite — ne sont pas decoratifs. Leur injection dans le YAML du compositeur produit un changement visible et mesurable dans le GA. L'espace negatif s'agrandit ou se comprime. Les proportions entre elements changent. La hierarchie de lecture se reordonne.

**Difference observable:** Deux rendus du meme GA, l'un avec les parametres calibres par IA, l'autre avec des valeurs par defaut — la difference doit etre perceptible en <3s par un observateur non-expert.

**Implements:** P17 (calibration integrale), P26-P31 (design system spatial).
**Valide par:** RC5 (parametres YAML injectes et actionnes).

---

## BC5: La Contour Matrix explore avant de converger

Le module ne produit pas un seul contour. Il produit une **grille** (age x H) de contours, les compare, et choisit le plus expressif. La selection n'est pas le premier essai — c'est le meilleur d'une exploration systematique.

**Difference observable:** Le repertoire `artefacts/contours/` contient plusieurs paires (sick/healthy) pour differentes tranches d'age. Un seul couple est selectionne pour le GA. Les autres sont archives comme alternatives documentees, pas comme brouillons abandonnes.

**Implements:** P_CAL2 (Contour Matrix), P2 (framework dynamique 3V adapte).
**Valide par:** RC1 (contours organiques exploitables) sur le couple selectionne.
