# Objectives — vec/calibration

## O_CAL1: Transformer des images IA en geometrie parametrique

**Ce que le module vise:** Extraire d'une image generee par IA (Ideogram, Gemini, Midjourney) une representation vectorielle native (cubic Bezier SVG path) qui preserve l'organicite de la forme originale tout en etant entierement code — editable, versionnable, parametrisable.

**Ce que le module ne vise PAS:**
- Generer des images IA (c'est le role de I5 — les modeles image)
- Produire des livrables visuels finis (c'est le role de vec/pipeline + vec/design_system)
- Remplacer le jugement esthetique d'Aurore (c'est le role de vec/audit, H2)

**Trade-off:** On sacrifie volontairement la fidelite pixel-perfect au profit de la fluidite organique. Un contour qui capture 85% de la silhouette source mais qui coule comme de l'eau est superieur a un contour qui capture 99% mais qui exhibe des angles parasites.

---

## O_CAL2: Garantir l'empathie clinique

**Ce que le module vise:** Les contours produits ne sont pas des exercices techniques. Ils doivent declencher une reponse emotionnelle specifique chez le pediatre : la projection clinique ("je reconnais mon patient"). Cette reponse est ce qui ancre le GA (B7, PH1) et le distingue d'un schema fonctionnel froid.

**Ce que le module ne vise PAS:**
- Definir ce qu'est l'empathie clinique (c'est le domaine d'Aurore)
- Mesurer l'empathie clinique avec precision psychometrique (c'est hors scope pour un module technique)
- Produire de l'art (c'est de l'ingenierie visuelle au service d'un objectif clinique)

**Trade-off:** L'empathie est qualitative. Le module se dote d'un proxy mesurable (test d'Aurore en <2s, RC2) plutot que de pretendre la quantifier. Le seuil est binaire : ca marche ou pas.

---

## O_CAL3: Parametriser le vecteur de sante H

**Ce que le module vise:** Toute silhouette generee par ce module est une fonction de H (Health Vector, 0.0 -> 1.0). H=0.0 = enfant malade (spine courbe, tete penchee, bras tombants). H=1.0 = enfant sain (spine droit, tete haute, bras ouverts). Toute valeur intermediaire produit une posture coherente. C'est le coeur de P15 et P16.

**Ce que le module ne vise PAS:**
- Definir les transformations des autres elements visuels fonction de H (epithelium, muscle lisse, fond) — c'est vec/design_system
- Gerer l'animation ou le morphing temps-reel — le GA est une image statique

**Trade-off:** On modelise H comme un scalaire unique, pas comme un vecteur multi-dimensionnel. Un enfant reel est malade de multiples facons (fievre, toux, fatigue, douleur). On compresse tout en une seule variable pour garder le pipeline tractable. La perte de granularite est acceptee parce que le GA n'a que 3 zones discrete (H~0, H~0.5 implicite dans la transition, H~1).

---

## O_CAL4: Eliminer tout pixel IA du livrable

**Ce que le module vise:** L'image IA est un calibrateur ephemere. Elle informe. Elle ne persiste pas. Le livrable contient exclusivement des paths SVG generes algorithmiquement. C'est l'enforcement direct de VN4 et V6.

**Ce que le module ne vise PAS:**
- Interdire l'utilisation d'images IA dans le processus (au contraire, P12 les encourage comme accelerateurs)
- Produire des contours qui n'ont aucune trace de l'inspiration IA (c'est impossible et pas souhaitable — on veut l'organicite que l'IA capture)

**Trade-off:** Aucun. C'est un invariant, pas un objectif negociable.

---

## O_CAL5: Calibrer au-dela des contours

**Ce que le module vise:** L'infographie IA (P17 elargi) n'est pas qu'un calibrateur de volumes. C'est un calibrateur integral — volumes, couleurs en contexte, textures, espacements, espaces negatifs, ancrage, hierarchie de lecture, tonalite emotionnelle. Le module extrait tous ces parametres et les traduit en YAML consommable par le compositeur.

**Ce que le module ne vise PAS:**
- Copier l'infographie IA (ce serait VN4 + V6 violation)
- Automatiser entierement l'extraction des parametres non-geometriques (les ratios d'espacement, la densite locale, le poids visuel — ce sont des jugements qui necessitent l'oeil du concepteur)

**Trade-off:** L'extraction de contours (RC1) est automatisable. L'extraction de parametres integraux (RC5) est semi-automatique — le pipeline propose, Silas valide et ajuste. On accepte cette asymetrie.

---

## Success Signals

| Signal | Source | Ce qu'il indique |
|--------|--------|-----------------|
| Aurore dit "je vois un enfant malade" en <2s | Test empathie (RC2) | La calibration depasse le geometrique |
| Le contour SVG est indistinguable en silhouette de la source IA | Comparaison target vs output (RC1) | Le pipeline preserve l'organicite |
| H=0.5 produit une posture credible sans etre explicitee | Strip continuite (RC3) | Le vecteur H est correctement interpole |
| `grep -c "image\|data:image" livrable.svg` = 0 | Check automatique (RC4) | Zero pixel IA |
| Les parametres YAML changent le rendu de maniere perceptible | Injection test (RC5) | La calibration integrale est actionnable |
