# Algorithm — vec/design_system

3 algorithmes : verification chromatique, test d'impact cognitif, et validation spatiale.

---

## DS-A1: Verification chromatique automatique

Verifie que la palette canonique est respectee dans le SVG source. Execute automatiquement dans le pipeline (A5/A7).

```
ENTREE: fichier SVG source (.svg)

1. PARSER LE SVG
   - xml.etree.ElementTree.parse(svg_path)
   - Extraire tous les attributs fill, stroke, stop-color, color

2. VERIFIER PRESENCE PALETTE
   Pour chaque hex produit dans la palette canonique:
     #2563EB (OM-85), #0D9488 (PMBL), #7C3AED (MV130),
     #059669 (CRL1505), #DC2626 (virus)
   - Grep hex dans le SVG (case-insensitive)
   - Si un hex produit est absent → WARN (peut etre legitimate si l'element n'est pas encore dessine)
   - Si un hex produit est present mais utilise sur un element qui ne lui appartient pas → FAIL

3. VERIFIER ABSENCE COULEURS PARASITES
   - Extraire toutes les couleurs uniques du SVG
   - Comparer avec la palette autorisee (produits + neutres + fond)
   - Si une couleur saturee non-autorisee apparait → WARN + documenter

4. VERIFIER COHERENCE FOND/PRODUIT
   - Les couleurs de fond (bandes anatomiques, background) ne doivent pas
     avoir de saturation > 30% dans le meme canal qu'une couleur produit
   - Si conflit → WARN (risque de confusion visuelle)

SORTIE: PASS/FAIL/WARN + liste des anomalies
```

**Implements:** P7, B5, DS-R1.
**Health:** DS-H1 (coherence chromatique).

---

## DS-A2: Test d'impact cognitif PH1 (3 secondes)

Protocole de verification du choc cognitif sur le PNG delivery. Semi-automatique : la verification elle-meme est humaine, mais les criteres sont stricts.

```
ENTREE: fichier PNG delivery (1100x560) + fichier PNG 50% (550x280)

1. PREPARER LE TEST
   - Charger le PNG delivery (1100x560)
   - Generer le PNG 50% zoom (550x280) via Pillow resize LANCZOS
   - Ouvrir le PNG 50% dans une fenetre isolee (pas de contexte environnant)

2. SECONDE 1 — SCAN (gate 1)
   Question: "En 1 seconde de regard, est-ce que je percois une transition
   chromatique rouge→vert (gauche→droite)?"
   - OUI → passer au gate 2
   - NON → FAIL. Diagnostic: les couleurs de fond ne creent pas
     le gradient perceptible. Verifier P7 (palette) et P29 (densite Z1).

3. SECONDE 2 — IDENTIFICATION (gate 2)
   Question: "En 2 secondes, est-ce que je reconnais : des virus,
   une voie respiratoire, un enfant, le mot 'Wheezing' ou 'Asthma'?"
   - OUI (≥3 elements reconnus) → passer au gate 3
   - NON → FAIL. Diagnostic: la hierarchie typographique P28 n'est pas
     respectee (Niveau 1 absent ou trop petit) OU V12 viole
     (pictogramme enfant absent) OU V7 echoue (lisibilite 50% zoom).

4. SECONDE 3 — COMPREHENSION (gate 3)
   Question: "En 3 secondes, est-ce que je comprends : 4 agents colores,
   convergence vers un objectif commun, gradient de preuves (un agent
   dominant)?"
   - OUI → PASS
   - NON → FAIL. Diagnostic: B8 (convergence) ou B3 (barres evidence)
     ou P21 (gravite clinique) defaillants.

5. DOCUMENTER LE RESULTAT
   - Gate atteint (1/2/3 ou PASS)
   - Elements reconnus a chaque gate
   - Temps reel vs. temps cible
   - Si FAIL: quel pattern est en cause

SORTIE: PASS (3 gates passes) / FAIL (gate N echoue) + diagnostic
```

**Implements:** PH1, DS-R2.
**Health:** DS-H2 (test PH1).
**Carrier:** Silas (execution du protocole) + Aurore (test independant sur son expertise).

---

## DS-A3: Validation spatiale multi-critere

Verifie l'equilibre spatial, la densite, l'espace negatif, le poids visuel et les flux de lecture. Semi-automatique.

```
ENTREE: fichier SVG source + fichier PNG delivery (1100x560)

1. VERIFIER DENSITE LOCALE (P29)
   - Diviser l'image en 3 zones (27/46/27)
   - Compter les elements visuels par zone (approximation via groupes SVG)
   - Zone 1: attendu FAIBLE (3-5 elements: enfant, cercle vicieux, virus, label)
   - Zone 2: attendu HAUTE (8-15 elements: 4 bandes, 4 agents, convergence, DC, IgA)
   - Zone 3: attendu MOYENNE (4-7 elements: enfant, barres evidence, labels, fleche sante)
   - Si une zone depasse son budget d'elements → WARN

2. VERIFIER ESPACE NEGATIF (P26)
   - Lumen: verifier que le lumen est > 60% vide (fond visible)
     Methode: dans le SVG, calculer l'aire des elements dans la bande lumen
     vs. l'aire totale de la bande
   - Marges: verifier que les enfants (Z1/Z3) ont > 5% de padding
     par rapport au bord du canvas et au bord de la bronche
   - Si un element majeur touche un bord → FAIL

3. VERIFIER POIDS VISUEL RELATIF (P31)
   - Pour chaque element principal, estimer le poids:
     poids = aire_bbox * opacite_moyenne * saturation_couleur
   - Verifier la hierarchie:
     enfants > bronche > evidence_bars > cercle_vicieux > legende > arc_crl1505
   - Si inversion → WARN + identifier les elements a ajuster

4. VERIFIER FLUX DE LECTURE (P30)
   - Axe horizontal: le gradient chromatique L→R est-il perceptible?
     (rouge dominant a gauche, vert dominant a droite)
   - Axe vertical: les 4 bandes sont-elles empilees lisiblement?
     (lumen en haut, muscle lisse en bas)
   - L inverse: le scan horizontal mene-t-il naturellement a un scan
     vertical dans la zone d'interet?

5. VERIFIER HIERARCHIE TYPOGRAPHIQUE (P28)
   - Parser les <text> elements du SVG
   - Extraire font-size pour chaque label
   - Verifier: Niveau 1 >= 32, Niveau 2 in [24-30], Niveau 3 in [18-22]
   - Verifier: word count total ≤ 30 (V3)
   - Verifier: Niveau 1 place hors de la bronche
   - Generer PNG 550x280 et verifier lisibilite de chaque niveau

SORTIE: rapport multi-critere (PASS/WARN/FAIL par sous-check) + recommandations
```

**Implements:** P26, P28, P29, P30, P31, DS-R5, DS-R6.
**Health:** DS-H3 (hierarchie typographique) + DS-H4 (equilibre spatial).

---

## DS-A4: Verification convergence IgA

Protocole de verification visuelle de la convergence IgA (B8).

```
ENTREE: fichier SVG source + fichier PNG delivery

1. VERIFIER 4 FLUX COLORES (S7a)
   - Dans le SVG, identifier les paths/lines de convergence
   - Chaque flux doit porter une couleur produit distincte:
     #2563EB, #0D9488, #7C3AED, #059669
   - Les 4 flux doivent etre presents
   - Aucun flux ne doit etre masque par un autre (verifier z-order)

2. VERIFIER POINT FOCAL (S7b)
   - Les 4 flux convergent vers un point identifiable
   - Le point est dans la bande lumen (pas dans le mur, pas dans la lamina propria)
   - Des formes Y (IgA) sont presentes au point de convergence
   - Les formes Y sont de taille ~15px (micro-ancres, P22)

3. VERIFIER LISIBILITE DE LA CONVERGENCE
   - Sur PNG 50% zoom: les 4 couleurs sont-elles distinguables?
   - Le point de convergence est-il identifiable?
   - Si non → augmenter l'epaisseur des flux ou l'espacement

SORTIE: PASS/FAIL + diagnostic
```

**Implements:** B8, DS-R3.
**Health:** H7.

---

## DS-A5: Verification fracture du cycle

Protocole de verification visuelle de la fracture du cercle vicieux (B4).

```
ENTREE: fichier SVG source + fichier PNG delivery

1. VERIFIER CERCLE VICIEUX (structure)
   - Cercle ferme present en Zone 1
   - 4 stations identifiables (Viral RTIs → Th2 bias → Remodeling → Re-susceptibility)
   - Couleur rouge (#DC2626 ou derive)
   - Fleches circulaires connectant les 4 stations

2. VERIFIER LANCE VERTE (S8a)
   - Element vert (path/line) qui traverse physiquement le cercle rouge
   - La lance part de Zone 2/3 (cote sain) vers Zone 1 (cote malade)
   - La lance est visuellement assertive (epaisseur suffisante, contraste avec le fond)

3. VERIFIER MARQUES DE FRACTURE (S8b)
   - Au point d'intersection lance/cercle:
     des eclats, des lignes de rupture, ou des fragments visuels
   - L'impression est celle d'un ACTE (rupture), pas d'un fondu

4. VERIFIER PERCEPTION
   - Sur PNG 50% zoom: la fracture est-elle perceptible?
   - Le cercle semble-t-il "brise" et non "intact"?

SORTIE: PASS/FAIL + diagnostic
```

**Implements:** P23, B4, DS-R4.
**Health:** H8.
