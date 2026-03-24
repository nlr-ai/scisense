# V2-A : La Bronche Vivante — Design détaillé

**Date :** 24 mars 2026
**Status :** Concept détaillé, en attente feedback Aurore
**Diagnostic :** Inversion product-centric → mechanism-centric (cf. V2_concept_proposals.pdf)

---

## 1. L'insight fondamental

Les 4 mécanismes immunologiques mappent directement sur les **4 couches anatomiques** d'une bronche pédiatrique. Pas besoin de les séparer artificiellement — la biologie les sépare déjà.

| Couche anatomique | Mécanisme immunologique | Ce qui change (malade → sain) |
|-------------------|------------------------|-------------------------------|
| **LUMEN** (espace aérien) | Agression virale → Protection IgA | Virus RSV/RV entrent → IgA sécrétoires neutralisent |
| **ÉPITHÉLIUM** (couche cellulaire) | Barrière épithéliale | Jonctions ouvertes (brèches) → E-cadhérine intacte |
| **LAMINA PROPRIA** (sous-muqueuse) | Immunité innée + adaptative | DC dormantes, Th2↑ → DC activées, Th1/Th2↔, Treg |
| **MUSCLE LISSE / ADVENTICE** | Contrôle inflammation + remodeling | Paroi épaissie, IL-33↑ → Paroi fine, IL-10↑ |

**Conséquence :** La coupe bronchique N'EST PAS une métaphore. C'est la réalité biologique du manuscrit, rendue lisible par la transformation spatiale L→R.

---

## 2. Choix : coupe longitudinale, pas transversale

Une coupe **transversale** (cercle) ne remplit pas le format panoramique 2:1.
Une coupe **longitudinale** (tube ouvert, vue en cutaway) s'étend naturellement sur toute la largeur.

```
Vue longitudinale d'une bronche (tube coupé en deux) :

  ═══════════════════════════════════════════════════════
  ÉPITHÉLIUM (paroi supérieure)
  - - - - - - - - - - - - - - - - - - - - - - - - - - -
            LUMEN (espace aérien intérieur)
  - - - - - - - - - - - - - - - - - - - - - - - - - - -
  ÉPITHÉLIUM (paroi inférieure)
  ═══════════════════════════════════════════════════════
  LAMINA PROPRIA (cellules immunitaires)
  ───────────────────────────────────────────────────────
  MUSCLE LISSE (remodeling)
```

Les 4 couches deviennent 4 **bandes horizontales naturelles** dans le panorama.

---

## 3. Layout complet (3300×1680 px de travail, 1100×560 livraison)

```
+------+-----------------------------------------------------------+------+
|      |                    BRONCHE VIVANTE                         |      |
| Z1   |              (coupe longitudinale L→R)                     | Z3   |
| ~12% |                      ~76%                                  | ~12% |
|      |                                                            |      |
|      | MALADE ─────────── TRANSITION ──────────── SAIN            |      |
| Enf. |                                                            | Enf. |
| mal. | ┌──────────────────────────────────────────────────────┐   | sain |
|      | │ LUMEN    virus→→  │           │  Y Y Y IgA          │   |      |
| ╭──╮ | │          RSV RV   │           │  (anticorps)         │   | (o)/ |
| │CC│ | ├──────────────────────────────────────────────────────┤   | /|\  |
| │  │ | │ ÉPITH.  ░ ░ ░ ░  │  ░▓░▓░▓   │  ▓▓▓▓▓▓▓▓▓▓        │   | / \  |
| ╰──╯ | │         brèches   │  réparation│  intact             │   |      |
|      | ├──────────────────────────────────────────────────────┤   | EVID |
|      | │ LAMINA  ○ dormant │  ○→✦ activ │  ✦ DC   Th1/Th2↔   │   | ████ |
|      | │ PROPRIA Th2↑↑     │  ■ ■ ■     │  Treg ↑            │   | ██   |
|      | ├──────────────────────────────────────────────────────┤   | █    |
|      | │ MUSCLE  ████ épais│  ███ moyen │  ██ fin  IL-10↑    │   | ▪    |
|      | │ LISSE   inflam.↑  │            │  résolu            │   |      |
|      | └──────────────────────────────────────────────────────┘   |      |
|      |                                                            |      |
|      |   ■OM85  ■PMBL  ■MV130  ■CRL1505  (légende couleur)      |      |
+------+-----------------------------------------------------------+------+
```

### Proportions

| Zone | Largeur | Contenu |
|------|---------|---------|
| Marge gauche (Z1) | ~12% (~396px) | Enfant malade + cercle vicieux compact |
| Bronche centrale | ~76% (~2508px) | Coupe longitudinale 4 couches, transformation L→R |
| Marge droite (Z3) | ~12% (~396px) | Enfant sain + barres d'évidence |

**Pourquoi 76% pour la bronche ?** C'est le sujet. Les enfants et l'évidence sont des cadres narratifs, pas le contenu central. V1 donnait 46% au centre — trop peu pour 4 mécanismes.

---

## 4. Les 4 bandes détaillées

### Bande 1 : LUMEN (espace aérien)

**Gauche (malade):** 2-3 virus stylisés (cercle rouge + spikes) entrant par les brèches de l'épithélium. Mouvement L→R avec des flèches rouges.

**Droite (sain):** Petits Y d'IgA sécrétoires (P22 micro-ancres) patrouillant dans la lumière. Les Y sont **multi-colorés** (un Y bleu OM-85, un Y teal PMBL, un Y vert CRL1505) pour montrer que les 3 produits convergent vers ↑IgA.

**Transition:** Les virus s'estompent, les Y apparaissent. Gradient de rouge → blanc → vert-bleu pâle.

### Bande 2 : ÉPITHÉLIUM (barrière cellulaire)

**Gauche (malade):** Cellules épithéliales dessinées comme des blocs rectangulaires avec des **brèches** (gaps entre les blocs). Le tissu est poreux — les virus traversent.

**Droite (sain):** Blocs serrés, jonctions fermées. Petites agrafes teal (PMBL) entre les blocs = E-cadhérine restaurée. Bouclier bleu (OM-85) sur la surface = récepteurs viraux verrouillés.

**Attribution couleur (sans mots):**
- Points/halos **bleus** sur les cellules côté droit = OM-85 (↓ACE2/TMPRSS2)
- Agrafes **teal** entre les cellules = PMBL (↑E-cadhérine)

### Bande 3 : LAMINA PROPRIA (cellules immunitaires)

C'est la bande la plus riche. Deux sous-systèmes :

**Immunité innée :**
- Gauche : cellule dendritique (DC) dormante — corps irrégulier gris, branches courtes
- Droite : DC activée — branches étendues, halo lumineux, couleur violet/bleu

**Immunité adaptative :**
- Gauche : déséquilibre Th2 (symbolisé par une balance penchée, ou simplement Th2↑ en petit)
- Droite : balance Th1/Th2 rééquilibrée (balance droite), Treg visible

**Attribution couleur :**
- Halo **bleu** sur DC = OM-85 (activation)
- Hélice **violet** dans le noyau DC = MV130 (trained immunity, reprogrammation épigénétique)
- Arc **vert** arrivant du bas = CRL1505 (axe intestin-poumon, action à distance)
- Points **bleu** sur la balance = OM-85 (modulation Th1/Th2)

### Bande 4 : MUSCLE LISSE / ADVENTICE (inflammation + remodeling)

**Gauche (malade):** Bande épaisse, teinte rouge/orangé = inflammation active, remodeling (paroi épaissie, fibrose, mucus).

**Droite (sain):** Bande fine, teinte verte pâle = inflammation contrôlée, paroi normalisée.

**Attribution couleur :**
- Toute cette bande montre la conséquence des 4 mécanismes au-dessus. Pas d'attribution directe d'un seul produit — c'est le résultat convergent.
- Optionnel : gradient de rouge→vert avec les 4 couleurs mélangées.

---

## 5. Éléments annexes

### Enfant malade (marge gauche)

Silhouette organique (contour extrait S3, approche iii). Posture affaissée, dos courbé, bras vers la bouche (toux). Petites marques de détresse. Couleur rouge/gris.

Taille : ~250px de haut dans le format de travail. Position verticale centrée sur la bronche.

### Cercle vicieux (marge gauche, sous l'enfant)

Version **compacte** — 4 stations en cercle fermé, taille réduite (~180px diamètre). C'est un élément de contexte, pas le centre du design.

```
    ╭───→ Viral RTIs ───╮
    │                    │
Re-suscept.          Th2 bias
    │                    │
    ╰── Remodeling ←────╯
        Wheezing/Asthma
```

### Enfant sain (marge droite)

Silhouette organique (contour extrait S4). Posture droite, bras ouverts. Couleur verte/bleue.

### Barres d'évidence (marge droite, sous l'enfant)

4 barres horizontales empilées verticalement, largeur proportionnelle à l'évidence :

```
████████████████  OM-85    18 RCTs
██████████        PMBL     5 RCTs
█████             MV130    1 RCT
██                CRL1505  Preclinical
```

Chaque barre dans la couleur du produit. Labels à droite des barres (2 mots chacun).

### Légende produit-couleur (sous la bronche)

4 petits carrés colorés avec le nom du produit. Positionnés sous la bronche, centrés.

```
■ OM-85    ■ PMBL    ■ MV130    ■ CRL1505
```

### Arc CRL1505 (axe intestin-poumon)

Un arc vert (#059669) partant du **bas de l'image** (petit pictogramme intestin = squiggle line art) et montant vers la bande LAMINA PROPRIA côté droit. Cet arc est spatialement séparé pour marquer l'action systémique à distance (V13).

```
                    BRONCHE
                ┌──────────────────┐
                │  lamina propria  │ ←── arc vert arrive ici
                └──────────────────┘
                         ↑
                         │  arc vert
                         │
                    (intestin)
```

---

## 6. Budget mots

| Élément | Mots | Comptage |
|---------|------|----------|
| Cercle vicieux : Viral RTIs, Th2 bias, Remodeling, Re-susceptibility | 6 |
| Wheezing / Asthma | 2 |
| OM-85, PMBL, MV130, CRL1505 (légende) | 4 |
| 18 RCTs, 5 RCTs, 1 RCT, Preclinical (évidence) | 7 |
| Barrier, Innate, Adaptive, Inflammation (labels bandes, optionnel) | 4 |
| Protected airways (Z3) | 2 |
| Clinical evidence (titre barres) | 2 |
| **TOTAL** | **27** |

Budget respecté (27/30). 3 mots de marge.

**Option sans labels de bandes** (si trop dense) : 23 mots, 7 de marge.

---

## 7. Palette

| Élément | Hex | Usage |
|---------|-----|-------|
| OM-85 | #2563EB | Halos sur épithélium + DC + balance |
| PMBL | #0D9488 | Agrafes entre cellules épithéliales |
| MV130 | #7C3AED | Hélice dans noyau DC |
| CRL1505 | #059669 | Arc gut→lung + points sur DC |
| Virus | #DC2626 | Icônes virus |
| Fond malade | #FEE2E2 | Gradient gauche (rouge pâle) |
| Fond sain | #ECFDF5 | Gradient droite (vert pâle) |
| Lumen | #FFFFFF | Espace aérien blanc |
| Paroi épaisse | #FBBF24 | Muscle lisse enflammé (ambre) |
| Texte | #1F2937 | Labels |

---

## 8. Justification Pattern par Pattern

| Pattern | Comment V2-A l'implémente |
|---------|--------------------------|
| P1 (flux L→R) | La bronche SE TRANSFORME de gauche à droite |
| P3 (compression métaphorique) | Les métaphores sont IN SITU — pas de symboles flottants |
| P5 (la science s'encode) | Les 4 couches anatomiques SONT les 4 mécanismes |
| P6 (mobile-first) | 4 bandes horizontales lisibles même à petite taille |
| P7 (cohérence chromatique) | Couleur = produit, visible dans chaque bande |
| P18 (embodiment actif) | Chaque agent est ENCASTRÉ dans sa couche biologique |
| P19 (topologie spatiale) | Position verticale = localisation anatomique réelle |
| P20 (abstraction pro) | Line art médical, pas de cartoon |
| P21 (gravité clinique) | Barres d'évidence proportionnelles |
| P22 (micro-ancres) | IgA Y dans le lumen, agrafes E-cadhérine |
| P23 (résolution topologique) | Cercle vicieux fermé → transformation linéaire qui le brise |
| P24 (concept ASCII avant wireframe) | Ce document |
| P25 (vérification visuelle) | PDF vérifié avant envoi |
| V12 (enfants obligatoires) | Enfant malade Z1 + enfant sain Z3 |
| V13 (CRL1505 séparé) | Arc gut→lung spatialement séparé en bas |

---

## 9. Risques identifiés et mitigations

| Risque | Mitigation |
|--------|-----------|
| 4 bandes = trop dense à 560px | Tester lisibilité mobile dès le premier wireframe. Si trop dense : fusionner bandes 3+4 (lamina + muscle = "sous-muqueuse") |
| Attribution couleur ambiguë sans légende | Légende explicite sous la bronche (4 carrés + noms) |
| Arc CRL1505 croise les bandes | L'arc part du BAS, arrive par le côté DROIT. Ne traverse pas les bandes mais les rejoint latéralement |
| Cercle vicieux trop petit pour être lisible | Agrandir la marge gauche à 15% si besoin. Ou simplifier à 3 stations |

---

## 10. Prochaine étape

1. **Attendre feedback Aurore** sur les 3 propositions
2. **Si V2-A validée** → wireframe SVG (Étape 1 du pipeline)
3. **Si fusion demandée** → adapter ce layout selon ses retours
4. **Générer contours organiques** pour les enfants (pipeline contour extraction S3/S4)

---

## 11. Audit multi-agent — corrections intégrées (24 mars 2026)

3 agents d'exploration ont audité ce design depuis 3 angles : immunologie, communication visuelle, et matrice produit-mécanisme. Voici les corrections.

### 11.1 Trained immunity ≠ Adaptive classique (CORRECTION CRITIQUE)

Le design initial compressait trained immunity (MV130) et rééquilibrage Th1/Th2 (OM-85) dans la même bande "lamina propria". Ce sont deux processus fondamentalement différents :

- **Adaptive classique** (OM-85) : antigen-spécifique, réversible, balance Th1/Th2
- **Trained immunity** (MV130) : non-spécifique, reprogrammation épigénétique permanente, innée

**Solution : séparation verticale dans la bande lamina propria**
- Partie haute : balance Th1/Th2 (seesaw/oscillation) — OM-85 bleu
- Partie basse : macrophage/DC avec glow doré + hélice violet — MV130 (état "verrouillé", pas oscillant)
- La distinction mouvement (balance) vs. stase (glow permanent) encode la différence sans texte

### 11.2 PMBL sous-représenté (CORRECTION)

PMBL n'apparaissait que dans la bande épithélium (agrafes teal). Or PMBL active aussi l'axe IL-22/IL-23 (immunité innée/Th17) et contribue au contrôle inflammatoire.

**Solution :** Ajouter une marque teal secondaire en lamina propria (petit point teal près du compartiment Th17/innée). PMBL reste dominé par son rôle barrière mais n'est plus un "joueur unique".

### 11.3 CRL1505 : du "arc" au "relais métabolique" (AMÉLIORATION)

L'arc générique gut→lung n'explique pas COMMENT un probiotique oral affecte l'immunité pulmonaire. Un pédiatre ne comprend pas "pourquoi ce pont existe".

**Solution : chaîne d'icônes en 3 étapes**
```
[Bactérie vivante] → [Métabolites (SCFA)] → [Poumon]
  (ovale vert)         (bulles/vial)           (bronche)
```
Le vial/bulles de fermentation encode immédiatement "processus métabolique microbien". Compacte (~150px), plus explicite que l'arc.

### 11.4 Risque d'indistinguabilité des 4 bandes à 560px (ATTÉNUATION)

100px par bande à la livraison = marginal. Atténuations :

1. **Séparateurs forts** : lignes horizontales grises 1-2px entre chaque bande
2. **Alternance épaisseur** : LUMEN fin (60px) / ÉPITHÉLIUM épais (120px) / LAMINA épais (140px) / MUSCLE fin (80px)
3. **Gradient très subtil** : réduire à #FFF0F0 (gauche) → #F0FFFB (droite) pour éviter le masquage chromatique
4. **Outlines sur tous les éléments colorés** : 1-2px gris foncé, surtout CRL1505 vert sur fond vert
5. **Fallback si échec test mobile** : fusionner lamina + muscle en 3 bandes

### 11.5 Micro-ancres IgA à 560px (ATTÉNUATION)

Les Y d'IgA (P22) passent à ~5px à la livraison = invisible.

**Solution :** Grossir les Y à 25px dans le format de travail (→ ~8px livraison = limite de lisibilité). Réduire le nombre de Y (3 au lieu de 6). Les Y restent des "ponctuation visuelle" que le spécialiste reconnaît sans que le généraliste soit perdu.

### 11.6 Blue dominance = scientifiquement correct

OM-85 dans 3/4 bandes crée une dominance bleue. C'est CORRECT : 18 RCTs = le produit le plus robuste. Les barres d'évidence Z3 confirment cette hiérarchie. Ne pas atténuer artificiellement.

---

## 12. Questions ouvertes pour NotebookLM

À transmettre au Moteur Analytique pour arbitrage :

1. **Le relais métabolique CRL1505** (bactérie → SCFA → poumon) est-il trop spéculatif pour un stade préclinique ? Faut-il rester à l'arc simple par prudence ?
2. **La séparation trained immunity / adaptive** dans la lamina propria ajoute de la complexité visuelle. Est-ce que le pédiatre cible comprend cette distinction ou est-ce un surplus pour immunologiste ?
3. **Faut-il un label de bande ?** ("Barrier", "Innate", "Adaptive", "Inflammation") = 4 mots (budget 27→23 restants). Gain en lisibilité vs. perte en espace.
4. **Le cercle vicieux Z1** peut-il être réduit à 3 stations (au lieu de 4) pour gagner de l'espace en marge ?

---

---

## 13. SD3 Audit Insights (NotebookLM slide deck, 24 mars 2026)

L'analyse du slide deck SD3 (19 slides) produit par NotebookLM confirme 3 choix de design V2-A et identifie 3 gaps à corriger.

### 13.1 Validations (design déjà aligné)

| Slide | Insight SD3 | Pattern/Behavior validé | Statut |
|-------|-------------|------------------------|--------|
| **Slide 11** — Topologie Spatiale = V2-A | "La Position = Le Mécanisme" : Surface (OM-85+PMBL), Intracellulaire (MV130 in DC), Systémique (CRL1505). L'architecture V2-A avec ses 4 bandes anatomiques est exactement cette topologie. | **P19** (position = mécanisme) | CONFIRMÉ |
| **Slide 9** — Compression Métaphorique | "Sacrifier le bruit moléculaire pour révéler la fonction tissulaire. Passer du laboratoire au chevet du patient." La stratégie V2-A de métaphores in situ (bouclier, briques, hélice, pont) plutôt que de listes de cytokines est validée. | **P3** (compression métaphorique) | CONFIRMÉ |
| **Slide 15** — Fractalisme Narratif | "La coupure visuelle nette symbolise l'arrêt de la morbidité. C'est le climax cognitif du design." La lance verte doit physiquement FRACTURER le cycle rouge du cercle vicieux. V2-A avait déjà P23 (résolution topologique) mais SD3 renforce l'exigence de coupure physique nette. | **P23** + **B4** (cycle brisé) | RENFORCÉ |

### 13.2 Confirmations additionnelles

| Slide | Insight SD3 | Référence existante |
|-------|-------------|---------------------|
| **Slide 5** — Choc Cognitif | Coupe bronchique seule = "froide". Pictogrammes enfants obligatoires pour projection clinique < 2s. | **V12**, **B7** — déjà intégré post-feedback Aurore |
| **Slide 19** — Effet Domino | Cascade cognitive 4 étapes : Scroll stop → Reconnaissance clinique < 2s → Aide à la décision → Changement de paradigme. | **GA_SPEC 2.6bis** — Impact Chain déjà documentée |

### 13.3 Gaps identifiés (corrections requises)

| Slide | Gap | Impact sur V2-A | Action |
|-------|-----|-----------------|--------|
| **Slide 13** — IgA Convergence | Les 4 flux-produits doivent converger visuellement au point de synthèse IgA dans le lumen. V2-A actuel montre les Y d'IgA mais sans convergence explicite des 4 couleurs vers ce point focal. | **Nouveau B8** ajouté (04_BEHAVIORS). Les 4 flux colorés doivent se rejoindre physiquement au site IgA. | V10.2 : redessiner le lumen côté sain pour que les 4 couleurs convergent vers un noeud IgA unique |
| **Slide 18** — Blueprint Clinique | Overlay anatomique : système respiratoire visible à travers le corps de l'enfant. V10 actuel = silhouettes solides sans anatomie interne. | Les pictogrammes enfants (B7) sont nécessaires mais insuffisants si opaques. L'anatomie interne renforce la connexion bronche → patient. | V10.2 : remplacer silhouettes solides par overlay semi-transparent avec arbre bronchique visible |
| **Slide 15** — Fracture du cycle (renforcement) | La lance verte doit physiquement fracturer le cycle rouge. V2-A section 8 mentionne P23 mais le wireframe actuel ne montre pas une coupure nette. | B4 + P23 renforcés. La fracture doit être un élément graphique explicite, pas implicite dans la transition L→R. | V10.2 : ajouter une flèche verte qui coupe net le tracé rouge du cercle vicieux |

### 13.4 Synthèse

Le slide deck SD3 valide l'architecture fondamentale de V2-A (topologie spatiale, compression métaphorique, fractalisme narratif). Les gaps sont des **raffinements de rendu**, pas des remises en question structurelles. La convergence IgA (B8) est le seul nouveau behavior à documenter. Les deux autres gaps (anatomie enfants, fracture cycle) sont des améliorations de l'implémentation de patterns et behaviors existants (B7, B4, P23).

---

*Ce document est une itération. Il deviendra GA_SPEC v2 section 2 après validation Aurore.*
