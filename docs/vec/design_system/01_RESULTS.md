# Results — vec/design_system

6 resultats mesurables. Chacun avec sa Guarantee Loop (R→S→H→C).

---

## DS-R1: Coherence chromatique produit-identite

Les 4 immunomodulateurs sont instantanement identifiables par leur couleur, partout dans le GA — icones, barres d'evidence, fleches, legende, flux de convergence. Le pediatre associe couleur = produit sans lire de legende.

**Palette canonique:**

| Produit | Hex | Couleur | Evidence |
|---------|-----|---------|----------|
| OM-85 | #2563EB | Bleu | 18 RCTs (ancre dominante) |
| PMBL | #0D9488 | Teal | 5 RCTs |
| MV130 | #7C3AED | Violet | 1 RCT |
| CRL1505 | #059669 | Vert | Preclinique |
| Virus (RSV/RV) | #DC2626 | Rouge | Antagoniste visuel |

Chaque couleur est constante sur tout le GA. Aucune substitution, aucun degrade qui brouille l'identite. Le rouge #DC2626 est reserve exclusivement aux elements pathologiques (virus, cycle vicieux, inflammation).

**Sense:** Grep automatique des hex codes dans le SVG source. Les 5 hex doivent etre presents. Aucune couleur produit ne doit apparaitre sur un element qui ne lui appartient pas.
**Health:** Inclus dans H1 (palette sub-check) + DS-H1 (coherence chromatique design system).
**Carrier:** Silas (auto-check script).
**Implements:** P7 (coherence chromatique), B5 (couleurs constantes).

---

## DS-R2: Impact cognitif PH1 — 3 secondes

Le GA declenche la sequence perceptive complete en 3 secondes sur ecran mobile :

- **Seconde 1 (scan):** Transition chromatique rouge→vert perceptible. Signal immediat : mauvais (gauche) → bon (droite). Curiosite activee.
- **Seconde 2 (identification):** Elements familiers reconnus — virus, voie respiratoire, "Wheezing/Asthma", enfant malade. Le pediatre projette son patient. Ancrage emotionnel.
- **Seconde 3 (comprehension):** 4 agents colores convergent vers des mecanismes partages. Gradient de preuves cliniques visible. Message clair : strategie preventive comparee, OM-85 mieux documente. Il clique.

Ce resultat est le plus critique du module. Un GA qui ne stoppe pas le scroll en 1s est un GA qui echoue. Un GA ou le pediatre ne projette pas son patient en 2s ne cree pas d'ancrage emotionnel. Un GA ou le message n'est pas clair en 3s ne genere pas de citation.

**Sense:** Test PH1 = verification visuelle de la sequence 3 secondes sur PNG delivery (1100x560) affiche a 50% zoom (550x280 = ecran mobile). Chaque seconde est un gate.
**Health:** DS-H2 (test PH1). Depend aussi de H2 (sign-off Aurore).
**Carrier:** Silas (verification visuelle) + Aurore (impact clinique).
**Implements:** PH1 (perception pediatre), B1 (reconnaissance clinique Z1), B3 (decision Z3).

---

## DS-R3: Convergence visuelle IgA

Les 4 flux-produits (OM-85 bleu, PMBL teal, MV130 violet, CRL1505 vert) convergent visuellement vers un point focal unique dans le lumen : le site de synthese des IgA muqueuses. Ce point de convergence encode le fait que l'objectif tissulaire est unique — production d'IgA muqueuses et restauration de la barriere — quel que soit le mecanisme d'action en amont.

La convergence est le climax scientifique du GA : "4 agents, 1 resultat". Les 4 couleurs se rejoignent physiquement dans l'espace du GA, formant un noeud visuel que le pediatre lit sans effort.

**Criteres de reussite:**
- 4 lignes de flux colorees visibles dans la bande lumen, chacune d'une couleur produit distincte
- Les lignes convergent vers un point focal identifiable
- Formes Y (IgA secretoires, ~15px) regroupees au point de convergence
- Le point de convergence est dans le lumen apical (pas dans le mur, pas dans la lamina propria)
- Les flux sont distinguables (pas de superposition qui brouille les couleurs)

**Sense:** Verification visuelle S7a (4 lignes colorees) + S7b (formes Y au point focal).
**Health:** H7 (convergence IgA).
**Carrier:** Silas (verification visuelle) + NotebookLM (audit).
**Implements:** B8 (convergence visuelle IgA), P19 (topologie spatiale), P3 (compression metaphorique).

---

## DS-R4: Fracture du cercle vicieux

La transition visuelle gauche→droite montre que l'intervention brise la boucle pathologique. L'element memorable : une lance verte (health arrow) qui fracture physiquement le trace rouge du cercle vicieux. Ce n'est pas un fondu ni une transition implicite — c'est un acte graphique explicite, le climax cognitif du design.

**Criteres de reussite:**
- Cercle vicieux rouge visible en Zone 1 (4 stations : Viral RTIs → Th2 bias → Remodeling → Re-susceptibility)
- Fleche/lance verte qui traverse physiquement le cercle rouge
- Marques de fracture au point d'impact (eclats ou lignes de rupture)
- La coupure est perceptible comme un acte — un moment de rupture, pas un fondu
- Le cercle est ferme (boucle auto-entretenue) et la lance l'ouvre (resolution)

**Sense:** Verification visuelle S8a (lance verte brise cycle rouge) + S8b (marques de fracture).
**Health:** H8 (cycle fracture).
**Carrier:** Silas (verification visuelle) + Aurore.
**Implements:** B4 (cercle vicieux brise), P23 (resolution topologique).

---

## DS-R5: Hierarchie typographique respectee

Les 30 mots maximum (V3) sont distribues en 3 niveaux typographiques qui encodent l'importance par le poids visuel :

- **Niveau 1 (ancre):** Mots lus en premier. Font-size >= 32 au format 3x. Plus grands, plus gras. Ex: "Wheezing/Asthma", "Clinical evidence". Places HORS de la bronche (marges ou legende).
- **Niveau 2 (contexte):** Labels de mecanismes et produits. Font-size 24-30 au format 3x. Ex: "OM-85", "Viral RTIs", "18 RCTs". Dans ou pres de leurs elements.
- **Niveau 3 (ponctuation):** Micro-labels optionnels. Font-size 18-22 au format 3x. Ex: "Th1", "Th2", "gut". Colles a leur objet. Supprimes si le budget est serre.

Tous les niveaux passent le test de lisibilite V7 (50% zoom = 550x280). Si le Niveau 3 ne passe pas, il est supprime plutot que reduit.

**Sense:** Mesure des font-size dans le SVG source (parse XML). Verification V7 sur PNG reduit.
**Health:** DS-H3 (hierarchie typographique).
**Carrier:** Silas (auto-check SVG) + verification visuelle.
**Implements:** P28 (hierarchie typographique), V3 (budget 30 mots), V7 (lisibilite 50%).

---

## DS-R6: Equilibre spatial et densite controlee

L'espace du GA respecte simultanement :

- **Densite locale (P29):** Gradient d'information Z1 faible → Z2 haute → Z3 moyenne. Le gradient suit le flux de lecture L→R : accroche simple → complexite justifiee → conclusion actionable.
- **Espace negatif (P26):** Chaque element majeur a 5%+ de respiration autour de lui. Le lumen reste majoritairement vide (c'est de l'air). Les marges ne collent pas au cadre.
- **Poids visuel relatif (P31):** Enfants > Bronche > Evidence bars > Cercle vicieux > Legende > Arc CRL1505. Le preclinique ne pese pas comme 18 RCTs.
- **Flux vertical (P30):** L'axe horizontal L→R (temps/intervention) coexiste avec l'axe vertical haut→bas (surface→profondeur tissulaire). Le regard fait un L inverse.

**Sense:** Verification visuelle multi-critere (densite, espacement, poids, flux).
**Health:** DS-H4 (equilibre spatial).
**Carrier:** Silas (verification visuelle) + NotebookLM (audit).
**Implements:** P26, P29, P30, P31, P1 (flux L→R).

---

## Guarantee Loop

```
DS-R1 (coherence chromatique)    ← DS-H1 (palette check)         ← grep hex codes dans SVG
DS-R2 (impact cognitif PH1)     ← DS-H2 (test PH1 3 secondes)   ← verification visuelle PNG 50%
DS-R3 (convergence IgA)         ← H7   (convergence)             ← S7a + S7b (lignes + formes Y)
DS-R4 (fracture cycle)          ← H8   (cycle fracture)          ← S8a + S8b (lance + marques)
DS-R5 (hierarchie typographique)← DS-H3 (typo check)             ← parse SVG font-sizes + V7
DS-R6 (equilibre spatial)       ← DS-H4 (spatial check)          ← verification visuelle multi-critere
```

Tous les carriers sont Silas (auto-check + verification visuelle) + Aurore (impact clinique pour DS-R2, DS-R4).
