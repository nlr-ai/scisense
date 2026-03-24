# Patterns — vec/design_system

17 patterns visuels : 6 du Design System Biologique (lexique semiotique SciSense) + 8 du Langage Visuel Generique + 3 issus de la Litterature (VEC Literature Analysis). Les 14 premiers valides par NotebookLM (24 mars 2026, SD1 + SD3).

---

## Design System Biologique — Lexique Semiotique

Les 6 meta-patterns P18-P23 sont les regles de traduction entre biologie clinique et representation visuelle. Chaque faille identifiee dans l'audit SD1 est la consequence de la violation d'un de ces patterns.

---

### P18: Embodiment Actif — la physicalite de l'action

Les metaphores visuelles ne doivent jamais leviter. Elles doivent s'encastrer, fusionner ou percuter le tissu qu'elles modifient. Un agent qui flotte dans le vide est deconnecte de son action biologique — le pediatre ne comprend pas le mecanisme.

| Agent | Action biologique | Contrainte visuelle |
|-------|-------------------|---------------------|
| OM-85 | ↓ACE2/TMPRSS2 a la surface cellulaire | Bouclier encastre SUR les briques, entre virus et epithelium |
| PMBL | ↑E-cadherine entre cellules | Briques teal comblant physiquement les breches + agrafes moleculaires |
| MV130 | Reprogrammation epigenetique intracellulaire | Helice DANS le noyau de la DC |

Source: Faille 3 (OM-85 flottant), Faille 2 (PMBL cartoon). Implements B2.

**Verification:** Chaque agent doit etre en contact physique avec son substrat biologique dans le SVG. Un agent qui flotte = violation.

**Evidence:** Design heuristic (non valide empiriquement). Cible Vague 2 de recherche.

---

### P19: Topologie Spatiale — position = mecanisme

La localisation d'une metaphore dans l'espace du GA encode son mecanisme biologique. Intracellulaire ≠ surface ≠ systemique. Si deux agents sont au meme endroit, le pediatre ne distingue pas leurs modes d'action.

- **Intracellulaire** → DANS le hub DC : MV130 (trained immunity epigenetique)
- **Surface cellulaire** → SUR le mur : OM-85 (verrouillage recepteurs), PMBL (scellage jonctions)
- **Systemique** → Arc partant du BAS de l'image : CRL1505 (axe intestin-poumon, action orale a distance)

L'arc CRL1505 doit pointer independamment vers barriere + DC, sans croiser l'helice MV130. Implements V13.

**Verification:** Verifier que les 3 niveaux topologiques (intracellulaire, surface, systemique) sont spatialement distincts dans le rendu.

**Evidence:** Design heuristic (non valide empiriquement). Cible Vague 2 de recherche.

---

### P20: Abstraction Professionnelle — tonalite visuelle Q2

Une revue Q2 (MDPI Children) requiert une esthetique de rigueur clinique. Proscrire les entites humanoides pour les mecanismes moleculaires. Imposer le line art medical.

| Element | Requis | Proscrit |
|---------|--------|----------|
| Cellule Dendritique | Morphologie filopodiale exacte (branches courbes irregulieres, corps vesiculaire) | Etoile symetrique |
| PMBL | Agrafe moleculaire abstraite | Macon humain |
| Intestin (CRL1505) | Squiggle line art minimal | Organe anatomique realiste |
| Virus | Icone stylisee (cercle + spikes) | Monstre cartoon |
| Enfants | Contours organiques vectorises (approche iii) | Stick figures geometriques |

Valide par NotebookLM : corps irregulier + branches courbes = reconnaissable par immunologiste en < 2s.

**Evidence:** Design heuristic (non valide empiriquement). Cible Vague 2 de recherche.

---

### P21: Gravite Clinique — proportionnalite volumetrique

L'aire visuelle d'un element est proportionnelle a sa robustesse clinique. L'evidence n'est pas lineaire — 18 RCTs ecrasent un stade preclinique. Le pediatre doit "peser" la preuve sans effort.

| Produit | Evidence | Masse visuelle relative |
|---------|----------|------------------------|
| OM-85 | 18 RCTs | 100% — ancre visuelle dominante |
| PMBL | 5 RCTs | ~60% |
| MV130 | 1 RCT | ~30% |
| CRL1505 | Preclinique | ~10-15% — baseline |

Le bloc OM-85 bleu doit etre 3-4x plus massif que le bloc CRL1505 vert. Si Z3 parait faible, augmenter la masse du bloc OM-85, PAS la largeur de la zone (ratio 27/46/27 valide).

Implements B3 (decision). Renforce par P31 (poids visuel) au niveau de l'image entiere.

**Evidence:** Cleveland & McGill 1984 + loi de Stevens (RCT + psychophysique). Aire compresse les differences (beta~0.7) ; longueur recommandee comme canal primaire.

---

### P22: Micro-Ancres Moleculaires — ponctuation visuelle

L'interdiction des listes de cytokines (VN1) ne doit pas vider l'image de ses reperes biologiques. Utiliser des pictogrammes universels microscopiques pour "ponctuer" l'action sans surcharger.

- **IgA secretoires** : petits Y (~15px) au-dessus du mur repare, dans la lumiere bronchique (lumen apical). PAS dans le mur. Elles sont transcytees a travers l'epithelium pour neutraliser les virus dans le lumen.
- **IFN** : subtiles fleches ↑ pres de l'epithelium sain (Z3)
- **Pas de texte supplementaire** — ce sont des ancres visuelles, pas des labels

Le specialiste y trouve la plausibilite biologique ; le clinicien generaliste n'est pas noye.

**Positionnement IgA valide par NotebookLM :** lumen apical = correct biologiquement. Les IgA sont secretees a travers l'epithelium, pas produites dans le mur.

**Evidence:** Jambor & Bornhauser 2024, rule #7 (expert consensus). Le texte desambiguise les pictogrammes.

---

### P23: Resolution Topologique — fractalisme narratif

Une pathologie chronique auto-entretenue est un cercle ferme. Sa resolution est un vecteur qui le fracture.

- **Zone 1** : Cercle vicieux = fleche circulaire fermee (4 stations : Viral RTIs → Th2 bias → Remodeling → Re-susceptibility). La forme geometrique EST le message.
- **Zone 3** : La ligne de flux vert/bleu (epithelium restaure) se prolonge comme une lance qui vient fracturer physiquement une ligne rouge de morbidite menant au Wheezing/Asthma. Coupure visuelle nette.

**Precision SD3 (slide 15):** La fleche verte de sante (health arrow) doit physiquement FRACTURER le trace rouge du cercle vicieux. Ce n'est pas une transition implicite gauche→droite — c'est un element graphique explicite. "La coupure visuelle nette symbolise l'arret de la morbidite. C'est le climax cognitif du design."

La fracture doit etre perceptible comme un acte — un moment de rupture, pas un fondu. Implements B4, DS-R4.

**Evidence:** Design heuristic (non valide empiriquement). Cible Vague 2 de recherche.

---

## Langage Visuel Generique

Les 8 patterns P7, P26-P31 sont applicables a tout GA SciSense. Ils definissent les regles universelles de couleur, espace, typographie, densite, flux et poids.

---

### P7: Coherence Chromatique produit-identite

Chaque produit a une couleur unique et constante sur tout le GA — icones, barres, fleches, legendes. Le pediatre associe couleur = produit sans legende explicite.

**Palette canonique:**

| Produit | Hex | Usage |
|---------|-----|-------|
| OM-85 | #2563EB | Bleu — bouclier, barres evidence, flux convergence |
| PMBL | #0D9488 | Teal — briques, barres evidence, flux convergence |
| MV130 | #7C3AED | Violet — helice, barres evidence, flux convergence |
| CRL1505 | #059669 | Vert — pont, barres evidence, flux convergence |
| Virus | #DC2626 | Rouge — exclusivement pathologique (virus, cycle vicieux, inflammation) |

Implements B5 (couleurs constantes). Verified by H1 (palette sub-check).

**Evidence:** Jambor & Bornhauser 2024, rule #8 (expert consensus). Changement de couleur = changement de sens.

---

### P26: Espace Negatif — le silence visuel

Ce qui n'est PAS dessine est aussi important que ce qui l'est. L'espace negatif donne la lisibilite et guide le regard. Un GA surcharge est un GA illisible — le pediatre decroche en < 1s.

**Regles:**
- Chaque element visuel majeur (enfant, bronche, barres d'evidence) a un espace de respiration d'au moins 5% de sa propre dimension autour de lui
- Le lumen de la bronche est un espace negatif fonctionnel — il DOIT rester majoritairement vide (c'est de l'air) pour que les virus (gauche) et les IgA (droite) soient lisibles par contraste
- Les marges gauche et droite (enfants + cycle/evidence) ne doivent pas coller au cadre de la bronche
- L'espace negatif encode aussi l'information : un lumen vide cote sain = "l'air passe librement" = resolution

Calibre par infographie IA (P17 elargi). Tradeoff DS-T1 (densite vs lisibilite).

**Evidence:** Design heuristic (non valide empiriquement). Cible Vague 2 de recherche.

---

### P27: Texture et Materialite — le tissu vivant

La difference entre un epithelium qui "semble vivant" et des rectangles plats. Le rendu SVG programmatique a tendance a produire des formes geometriques froides. La texture encode la biologie sans ajouter de mots.

**Techniques de texture en SVG pur:**
- **Gradient subtil** sur les cellules epitheliales (pas de fill plat)
- **Opacite variable** sur le muscle lisse (gradient amber→vert = inflammation qui se resout)
- **Irregularite controlee** sur les branches DC (P20 impose des branches courbes irregulieres, pas des etoiles symetriques)
- **Bruit de Perlin** simule via des micro-variations de position (seed aleatoire fixe pour reproductibilite)

Ce que la texture ne fait PAS : ajouter du detail photorealiste. On reste en line art medical (P20). La texture est une micro-variation, pas un rendu 3D.

Calibre par infographie IA (P17 elargi). Renforce P20 (abstraction professionnelle). Tradeoff DS-T2 (organicite vs reproductibilite).

**Evidence:** Design heuristic (non valide empiriquement). Cible Vague 2 de recherche.

---

### P28: Hierarchie Typographique — les 30 mots qui comptent

Le budget de 30 mots (V3) n'est pas juste un plafond — c'est un systeme de hierarchie. Chaque mot a un poids visuel qui encode son importance.

**3 niveaux typographiques:**

| Niveau | Role | Font-size (3x) | Exemples | Placement |
|--------|------|----------------|----------|-----------|
| 1 (ancre) | Mots lus en premier | >= 32 | "Wheezing/Asthma", "Clinical evidence" | HORS de la bronche (marges ou legende) |
| 2 (contexte) | Labels mecanismes et produits | 24-30 | "OM-85", "Viral RTIs", "18 RCTs" | Dans ou pres de leurs elements |
| 3 (ponctuation) | Micro-labels optionnels | 18-22 | "Th1", "Th2", "gut" | Colles a leur objet |

**Regle de survie:** Le test de lisibilite V7 (50% zoom = 550x280) doit passer pour TOUS les niveaux. Si le Niveau 3 ne passe pas, le supprimer plutot que le reduire.

**Evidence:** Design heuristic (non valide empiriquement). Cible Vague 2 de recherche.

---

### P29: Densite Locale — le gradient d'information

La densite d'information n'est pas uniforme sur le GA. Elle suit un gradient qui encode la narration :

- **Zone 1 (gauche ~27%)** : densite FAIBLE. Le probleme doit etre immediatement lisible. Un enfant, un cercle vicieux, quelques virus. Pas de surcharge.
- **Zone 2 (centre ~46%)** : densite HAUTE. C'est le coeur scientifique. Les 4 bandes, les attributions produit, les transformations L→R. La densite est justifiee parce que le pediatre y arrive APRES avoir compris le probleme.
- **Zone 3 (droite ~27%)** : densite MOYENNE. Resolution (enfant sain) + outil de decision (barres d'evidence). Clair et actionable.

Ce gradient suit le flux de lecture L→R (P1) : accroche simple → complexite justifiee → conclusion actionable.

Si une zone est trop dense, la correction n'est pas de compresser les elements mais de verifier si tous les elements de cette zone sont necessaires (P3 compression metaphorique).

**Evidence:** Design heuristic (non valide empiriquement). Cible Vague 2 de recherche.

---

### P30: Flux de Lecture Secondaire — l'axe vertical

P1 definit le flux principal gauche→droite. Mais la "Bronche Vivante" (V2-A) introduit un flux secondaire VERTICAL : du lumen (haut) vers le muscle lisse (bas). Ce flux encode la profondeur tissulaire.

**Les deux flux coexistent:**
- **Axe horizontal (P1)** : malade → sain (le temps / l'intervention)
- **Axe vertical (P30)** : surface → profondeur (la localisation anatomique)

**Le regard du pediatre fait un L inverse:**
1. Scan horizontal rapide (P1) : rouge a gauche, vert a droite = "ca guerit"
2. Scan vertical dans la zone d'interet : "comment ca guerit" = les 4 couches

Ce flux vertical est ce qui distingue V2-A des designs classiques 3-zones. La topologie spatiale (P19) ne peut fonctionner que si le pediatre lit AUSSI de haut en bas.

**Les 4 bandes anatomiques (V2-A layout):**
1. **Lumen** (haut) — cavite aerienne, espace negatif fonctionnel, virus et IgA
2. **Epithelium** — couche cellulaire, mur de briques, site d'action OM-85/PMBL
3. **Lamina propria** — tissu conjonctif, hub DC, site d'action MV130
4. **Muscle lisse** (bas) — couche externe, gradient inflammation (amber→vert)

Le gradient L→R (malade→sain) s'applique a chaque bande independamment. Chaque bande raconte la meme histoire (degradation→restauration) a son niveau anatomique.

**Evidence:** Design heuristic (non valide empiriquement). Cible Vague 2 de recherche.

---

### P31: Poids Visuel Relatif — la balance des elements

Chaque element du GA a un poids visuel (aire x opacite x contraste x saturation). Le poids visuel relatif doit refleter l'importance clinique ET le niveau de preuve.

**Hierarchie de poids attendue:**

| Rang | Element | Justification |
|------|---------|---------------|
| 1 | Enfants (Z1/Z3) | Poids maximal — ancrages emotionnels (B1, B7, V12) |
| 2 | Bronche (centre) | Poids majeur — le sujet scientifique |
| 3 | Evidence bars (Z3) | Poids moyen-fort — outil de decision (B3) |
| 4 | Cercle vicieux (Z1) | Poids moyen — contexte clinique (B4) |
| 5 | Legende | Poids faible — reference, pas contenu central |
| 6 | Arc CRL1505 | Poids faible — information secondaire (preclinique) |

**Violation type:** Un arc CRL1505 aussi epais que le bouclier OM-85 (le preclinique ne doit pas avoir le meme poids visuel que 18 RCTs). Une legende plus grande que les barres d'evidence.

Renforce P21 (gravite clinique) au niveau de l'image entiere, pas juste de la Zone 3. Tradeoff DS-T4 (poids visuel vs evidence).

**Evidence:** Design heuristic (non valide empiriquement). Cible Vague 2 de recherche.

---

## Patterns issus de la Litterature (VEC Literature Analysis)

Les 3 patterns P32-P34 sont derives de l'analyse systematique de la litterature sur l'encodage perceptif de l'evidence (VEC_Literature_Analysis_SciSense.md, 24 mars 2026).

---

### P32: Encodage Perceptif Hierarchique de l'Evidence

Chaque produit est encode sur 3 canaux perceptifs simultanes (du plus au moins precis) :
- **Primaire : Longueur** (barre de remplissage) — proportionnelle au nombre de RCTs. beta approx 1.0 (Cleveland & McGill rang 3)
- **Secondaire : Luminance** (clair→fonce) — plus fonce = evidence plus forte. MacEachren 2012 : haute intuitivite, quantifiable
- **Tertiaire : Aire** (masse visuelle) — plus grand = plus robuste. beta approx 0.7, renforce mais ne porte pas seul

Les 3 canaux sont **redondants** (encodent la meme information) pour maximiser la comprehension en scan rapide.

Source: VEC_Literature_Analysis section 4.2, Cleveland & McGill 1984, MacEachren 2012.

**Evidence:** Cleveland & McGill 1984, MacEachren 2012 (RCT + psychophysique). Hierarchie perceptive validee experimentalement ; luminance = haute intuitivite pour l'incertitude.

---

### P33: Frequences Naturelles, Pas de Categories Abstraites

Les labels d'evidence utilisent des frequences naturelles : "18 RCTs", "5 RCTs", "1 RCT", "Preclinical". PAS de "Level A", "Strong", "Moderate". Les frequences naturelles ameliorent la comprehension de ~50% a >80% chez les cliniciens (Gigerenzer, McDowell & Jacobs 2017).

Source: VEC_Literature_Analysis section 4.2.

**Evidence:** Gigerenzer 2003, McDowell & Jacobs 2017 (psychophysique + meta-analyse). Frequences naturelles ameliorent la comprehension de ~50% a >80%.

---

### P34: Encodage de l'Incertitude par Luminance, Pas par Saturation

Contre-intuitivement, la saturation de couleur n'est PAS percue comme un marqueur d'incertitude par les non-specialistes (MacEachren 2012, classee en bas d'intuitivite ; Kinkeldey 2017, explicitement deconseillee). La luminance (clair/fonce) est le canal recommande. Application : les blocs CRL1505 (preclinique) doivent etre visuellement plus CLAIRS (pas juste plus petits) que les blocs OM-85. La teinte reste constante, la luminance varie.

Source: VEC_Literature_Analysis section 4.2, Kinkeldey et al. 2017.

**Evidence:** MacEachren 2012, Kinkeldey 2017 (psychophysique + revue systematique). Saturation deconseillee ; luminance = canal recommande pour l'incertitude.
