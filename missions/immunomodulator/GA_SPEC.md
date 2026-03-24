# Graphical Abstract — Spec Complète

## 1. Contraintes de Sortie

### 1.1 Contraintes MDPI (non-négociables)

| # | Règle | Implication concrète |
|---|-------|---------------------|
| R1 | Pas de titre, affiliations, ni références | Zéro mention d'auteurs, d'universités, de numéros de citation |
| R2 | Pas identique à une figure du manuscrit | Doit être visuellement ET structurellement différent de la Figure 1 (manufacturing) et de la Figure 2 (quadrants cytokines) |
| R3 | Pas de longs blocs de texte | Budget texte total : ~20 mots max sur toute l'image. Labels courts uniquement |
| R4 | Pas une combinaison Abstract + image | Doit raconter une histoire visuelle autonome, pas illustrer le résumé textuel |
| R5 | Libre de droits | Tout élément visuel doit être original ou sous licence libre. Pas de BioRender sans vérification licence commerciale |
| R6 | Plus petit caractère lisible | Taille minimale de police : 8pt sur le rendu final. Tester à 50% de zoom |
| R7 | PNG, JPEG ou TIFF haute qualité | Livraison en PNG **600 DPI minimum** (MDPI Section 7.1). 300 DPI insuffisant. |
| R8 | Minimum 560 × 1100 px (hauteur × largeur) | Ratio ~1:1.96 (panoramique). Format de travail : 1680 × 3300 px (3x) pour marge de qualité |

### 1.2 Contraintes techniques

| Paramètre | Valeur |
|-----------|--------|
| Dimensions de travail | 3300 × 1680 px (3x du minimum, ratio conservé) |
| Dimensions de livraison | 1100 × 560 px minimum (downscale propre) |
| Format de livraison | PNG 600 DPI minimum (MDPI Section 7.1) |
| Espace couleur | sRGB (publication web + print) |
| Fond | Blanc ou très légèrement gris (#FAFAFA) — standard journal |
| Polices | MDPI recommande: Times, Arial, Courier, Helvetica, Ubuntu, Calibri. Force `font-family: "Helvetica", "Arial", sans-serif` dans le SVG. PAS Inter. |
| Taille min police | 8pt sur le rendu final (= 24pt sur le fichier 3x) |
| Nombre de couleurs | Palette de 6-8 couleurs max pour cohérence visuelle |

### 1.3 Contraintes de différenciation

| Figure existante | Ce qu'elle montre | Ce que le GA NE DOIT PAS faire |
|-----------------|-------------------|-------------------------------|
| Figure 1 | Flux vertical : souches → fermentation → 4 procédés de lyse → formulation | Pas de schéma de procédé de fabrication. Pas de boîtes de Petri. Pas de flux vertical industriel |
| Figure 2 | 4 quadrants A/B/C/D avec listes de cytokines par produit | Pas de quadrants. Pas de listes de cytokines. Pas de bullet points. Pas de code couleur identique (orange/bleu/vert/jaune) |

---

## 2. Contenu Exact

### 2.1 Architecture : 3 zones dans le cadre panoramique

```
┌─────────────────────────────────────────────────────────────────────┐
│                         3300 × 1680 px                              │
│  ┌──────────┐  ┌─────────────────────────────┐  ┌──────────────┐   │
│  │  ZONE 1  │  │          ZONE 2              │  │   ZONE 3     │   │
│  │ ~25%     │  │          ~50%                │  │   ~25%       │   │
│  │ largeur  │  │          largeur             │  │   largeur    │   │
│  │          │  │                               │  │              │   │
│  │ PROBLÈME │  │  INTERVENTION + MÉCANISMES   │  │  ÉVIDENCE    │   │
│  │          │  │                               │  │  CLINIQUE    │   │
│  └──────────┘  └─────────────────────────────┘  └──────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
```

### 2.2 Zone 1 — LE PROBLÈME (~825 × 1680 px)

**Message :** Les infections virales respiratoires récurrentes chez l'enfant 0-5 ans créent un cercle vicieux menant au wheezing/asthme.

**Éléments visuels :**

| Élément | Description | Position |
|---------|------------|----------|
| Voie respiratoire malade | Coupe transversale stylisée d'une bronche pédiatrique. Épithélium poreux (jonctions ouvertes, représentées par des briques disjointes). Paroi épaissie. Mucus excessif (gouttelettes). | Centre de la zone |
| Virus | 2-3 icônes de virus (VRS, RV) pénétrant par les brèches de l'épithélium. Style simplifié, pas photoréaliste. | Entrant par le haut/gauche |
| Cercle vicieux | Flèche circulaire (sens horaire) reliant 4 étapes. La flèche revient au début (boucle fermée). | Autour de la voie respiratoire |
| Fond | Teinte rouge-orangé pâle, signifiant danger/inflammation | Fond de zone |

**Cercle vicieux — 4 étapes :**
1. **Viral aggression** — RSV/RV → nucleolin/ICAM-1 binding
2. **Dysregulated inflammation** — IL-33/TSLP/IL-25 → Th2 bias → ILC2 → IL-4/IL-5/IL-13
3. **Airway remodeling** — wall thickening, smooth muscle, fibrosis, mucus hypersecretion
4. **Re-susceptibility** — reduced caliber → compromised elasticity → vulnerable to next infection → loop closes

**Labels texte (Zone 1) :**
- "Viral aggression" (sur le cercle)
- "Dysregulated inflammation" (sur le cercle)
- "Airway remodeling" (sur le cercle)
- "Re-susceptibility" (sur le cercle)
- "Wheezing / Asthma" (sous la voie respiratoire, en gras)

**Total mots Zone 1 : 9**

### 2.3 Zone 2 — INTERVENTION + MÉCANISMES (~1650 × 1680 px)

**Message :** 4 immunomodulateurs bactériens convergent vers 4 mécanismes d'action partagés qui restaurent l'homéostasie immunitaire.

**Sous-zone 2A — Les 4 agents (partie haute, ~40% de la hauteur)**

| Élément | Description |
|---------|------------|
| 4 icônes produit | 4 symboles distincts alignés horizontalement, chacun avec sa couleur propre. Pas les mêmes icônes que la Figure 1. |
| OM-85 | Icône capsule. Couleur : bleu profond (#2563EB) |
| PMBL | Icône comprimé sublingual. Couleur : teal (#0D9488) |
| MV130 | Icône spray sublingual. Couleur : violet (#7C3AED) |
| CRL1505 | Icône probiotique (bactérie stylisée vivante). Couleur : vert (#059669) |
| Flèches convergentes | 4 flèches descendantes qui convergent vers un point central (la voie respiratoire saine) |

**Labels texte (2A) :** "OM-85", "PMBL", "MV130", "CRL1505" (sous chaque icône)

**Sous-zone 2B — Les 4 mécanismes convergents (partie basse, ~60% de la hauteur)**

Au point de convergence des 4 flèches, une voie respiratoire en transition (mi-malade, mi-saine) avec 4 transformations visibles :

| Mécanisme | Représentation visuelle | Label |
|-----------|------------------------|-------|
| Renforcement barrière épithéliale | Les briques de l'épithélium se resserrent, les jonctions se ferment. Flèche "↑" sur les briques. | "Epithelial barrier" |
| Activation immunité innée | Une cellule dendritique/macrophage qui "s'allume" (halo lumineux). | "Innate immunity" |
| Modulation immunité adaptative | Balance Th1/Th2 qui se rééquilibre (le plateau Th1 remonte, Th2 descend). | "Adaptive balance" |
| Contrôle inflammation | Thermomètre/cadran qui descend du rouge vers le vert. | "Inflammation control" |

**Labels texte (2B) :** "Epithelial barrier", "Innate immunity", "Adaptive balance", "Inflammation control" (4 × 2 mots = 8 mots)

**Total mots Zone 2 : 12** (4 noms produits + 8 mots mécanismes)

#### Métaphores visuelles par produit

Les 4 produits ne sont plus des pilules génériques. Chaque icône incarne son mécanisme d'action :

| Produit | Métaphore | Icône visuelle | Justification scientifique |
|---------|-----------|----------------|---------------------------|
| OM-85 (Bleu #2563EB) | Bouclier/Verrou | Icône de bouclier avec verrou | ↓ACE2/TMPRSS2/ICAM-1 — bloque physiquement l'arrimage viral |
| PMBL (Teal #0D9488) | Maçon | Briques scellées | ↑E-cadhérine, axe IL-23/IL-22 — répare les brèches épithéliales |
| MV130 (Rouge/Violet #7C3AED) | Programmeur | Hélice ADN / icône engrenage | Immunité entraînée — reprogrammation épigénétique & métabolique |
| CRL1505 (Vert #059669) | Pont Intestin-Poumon | Arc/pont reliant intestin et poumon | Axe intestin-poumon — action à distance de l'intestin vers les voies aériennes |

**Convergence visuelle :** Les 4 convergent vers un output partagé : ↑IgA mucosal antibodies (élément visuel unificateur au point de jonction des 4 flèches descendantes).

### 2.4 Zone 3 — ÉVIDENCE CLINIQUE (~825 × 1680 px)

**Message :** Ces 4 produits ont des niveaux de preuves cliniques pédiatriques très différents, de robuste (OM-85) à préclinique (CRL1505).

**Éléments visuels :**

| Élément | Description |
|---------|------------|
| Voie respiratoire saine | Même style que Zone 1, mais épithélium intact, pas de virus, paroi normale. Couleur verte/bleue. |
| Gradient d'évidence | Barre verticale ou échelle à 4 niveaux, avec les 4 produits positionnés selon leur maturité. Chaque produit garde sa couleur de la Zone 2. |

**Le gradient (de haut en bas = plus vers moins de preuves) :**

| Position | Produit | Indicateur visuel | Label |
|----------|---------|-------------------|-------|
| Haut | OM-85 (bleu) | Barre pleine + icône stéthoscope | "18 RCTs" |
| Milieu-haut | PMBL (teal) | Barre ~60% | "5 RCTs" |
| Milieu-bas | MV130 (violet) | Barre ~30% | "1 RCT" |
| Bas | CRL1505 (vert) | Barre ~10% + icône fiole labo | "Preclinical" |

**Fond :** Teinte bleu-vert pâle, signifiant protection/résolution.

**Labels texte (Zone 3) :** "18 RCTs", "5 RCTs", "1 RCT", "Preclinical", + "Clinical evidence" en titre de la barre.

**Total mots Zone 3 : 7**

### 2.5 Budget texte total

| Zone | Mots |
|------|------|
| Zone 1 | 8 |
| Zone 2 | 12 |
| Zone 3 | 7 |
| **Total** | **27** |

C'est au-dessus de mon budget initial de 20 mots. Options :
- Acceptable si chaque label fait 1-2 mots et qu'il n'y a aucun paragraphe → conforme à la règle R3
- Si trop : supprimer les labels des 4 mécanismes et les remplacer par des icônes pures avec légende intégrée au flux visuel

### 2.6 Palette de couleurs

| Usage | Couleur | Hex |
|-------|---------|-----|
| Fond général | Blanc/gris très clair | #FAFAFA |
| Zone 1 - Problème | Rouge-orangé pâle | #FEE2E2 |
| Zone 3 - Résolution | Bleu-vert pâle | #ECFDF5 |
| Virus | Rouge vif | #DC2626 |
| OM-85 | Bleu profond | #2563EB |
| PMBL | Teal | #0D9488 |
| MV130 | Violet | #7C3AED |
| CRL1505 | Vert émeraude | #059669 |
| Texte principal | Gris foncé | #1F2937 |
| Flèches/liaisons | Gris moyen | #6B7280 |

### 2.6bis Impact Chain

Le GA sert de détonateur d'une chaîne d'impact clinique en 4 étapes :

1. **Visual Trigger** — arrête le scroll du pédiatre sur la table des matières (mobile-first)
2. **Cognitive Shock** — changement de paradigme : du traitement aigu vers l'immunomodulation préventive
3. **Actionability** — outil d'aide à la décision (hiérarchie comparative d'évidence)
4. **Loop Closure** — changement de pratique → citation → autorité pour SciSense

**Implication design :** la lisibilité à PETITE taille (téléphone mobile) est encore plus critique qu'en format desktop. Chaque élément doit rester lisible et identifiable à 1100×560 px et en-dessous.

---

## 3. Pipeline de Création

### 3.1 Étapes

```
ÉTAPE 1 — WIREFRAME (Silas)
    Génération d'un wireframe SVG annoté avec positions exactes,
    proportions et labels. Validation par Aurore.
    Outil : Python (svgwrite) ou HTML/CSS
    Livrable : wireframe.svg + wireframe.png

         ↓ validation Aurore

ÉTAPE 2 — ÉLÉMENTS VISUELS UNITAIRES
    Création/sourcing de chaque élément :

    2a. Voie respiratoire (malade + saine)
        → Option A : Dessin vectoriel simplifié (Illustrator/Inkscape)
        → Option B : IA générative (prompt Midjourney/DALL-E) + vectorisation
        → Option C : Élément BioRender (vérifier licence MDPI)

    2b. Icônes virus (VRS, RV)
        → Icônes vectorielles libres de droits (Flaticon, Bioicons.com)
        → Ou : génération simple SVG (cercle + spikes)

    2c. Icônes produits (capsule, comprimé, spray, bactérie)
        → Icônes vectorielles médicales/pharma libres de droits

    2d. Icônes mécanismes (briques, cellule, balance, thermomètre)
        → Icônes vectorielles ou dessin SVG programmatique

    2e. Gradient d'évidence
        → Barres SVG programmatiques (facile, 100% contrôle)

    2f. Cercle vicieux + flèches
        → SVG programmatique (arcs + pointes de flèches)

         ↓ éléments prêts

ÉTAPE 3 — ASSEMBLAGE
    Composition de tous les éléments dans le cadre 3300×1680.
    Outil : Python (Pillow/Cairo) ou Figma ou Illustrator
    Ajustement espacement, alignement, équilibre visuel.
    Livrable : GA_draft_v1.png

         ↓ review Aurore

ÉTAPE 4 — ITÉRATION
    Corrections basées sur le feedback :
    - Ajustement couleurs/contraste
    - Modification labels
    - Rééquilibrage zones
    Livrable : GA_draft_v2.png, v3...

         ↓ validation Aurore

ÉTAPE 5 — FINALISATION
    - Export final 3300×1680 px PNG 300 DPI
    - Downscale test à 1100×560 → vérification lisibilité R6
    - Vérification des 8 règles MDPI une par une (checklist)
    Livrable : GA_FINAL.png + GA_FINAL_lowres.png

         ↓ livré

ÉTAPE 6 — SOUMISSION
    Aurore envoie le GA + la bibliographie reformatée à Mindy Ma.
```

### 3.2 Évaluation des outils de génération

| Outil | Forces | Faiblesses | Verdict |
|-------|--------|------------|---------|
| **Python (svgwrite/Pillow)** | 100% contrôle, reproductible, libre de droits garanti, modifiable par code | Rendu moins "organique", limité pour les éléments anatomiques | Wireframe + gradient + flèches + assemblage |
| **BioRender** | Éléments biomédicaux prêts, style publication | Licence commerciale floue pour MDPI, coût, moins flexible | Éléments anatomiques SI licence vérifiée |
| **Midjourney/DALL-E** | Visuels frappants, rapide | Copyright ambigu (R5), contrôle faible sur le détail scientifique, hallucinations visuelles | Inspiration/concept uniquement, PAS pour le livrable final |
| **Inkscape/Illustrator** | Précision vectorielle totale, export parfait | Manuel, plus lent | Finition finale si nécessaire |
| **Figma** | Collaboratif, bon pour le layout | Moins bon pour les éléments biomédicaux | Alternative pour l'assemblage |

### 3.3 Pipeline recommandé

```
Silas (code)          →  wireframe SVG + gradient + flèches + labels
                      →  icônes virus/produits (SVG programmatique simple)
Aurore (validation)   →  choix d'angle, ajustements contenu
Bioicons.com (libre)  →  éléments anatomiques vectoriels si disponibles
Inkscape (finition)   →  assemblage final et polish
```

**Première action concrète :** Je génère le wireframe SVG annoté maintenant. C'est la base sur laquelle tout le reste se construit. Aurore voit le layout, valide les proportions, et on itère.

### 3.4 Checklist de livraison finale

- [ ] R1 : Aucun titre, affiliation, référence
- [ ] R2 : Différent de Figure 1 ET Figure 2
- [ ] R3 : Aucun bloc de texte > 3 mots
- [ ] R4 : Pas une simple illustration de l'abstract
- [ ] R5 : Tous les éléments libres de droits (traçabilité documentée)
- [ ] R6 : Plus petit caractère lisible à 1100×560
- [ ] R7 : PNG haute qualité
- [ ] R8 : Dimensions ≥ 560 × 1100 px, ratio conservé
- [ ] Scientifiquement exact (review Aurore)
- [ ] Cohérent avec le manuscrit soumis

---

## 4. Système des 3 Versions — Framework Dynamique

### 4.1 Principe fondamental

Les 3 versions sont **toutes à 100% de qualité**, 100% conformes MDPI, scientifiquement rigoureuses au même degré. Il n'y a pas de version "minimale" — accepter une baisse de standard n'est pas une option.

La différence entre les 3 versions est **l'hypothèse d'encodage** — le pattern visuel/cognitif choisi pour transmettre la science au pédiatre.

### 4.2 Framework dynamique (pas d'axes statiques)

Les axes de variation ne sont **PAS prédéfinis**. Ils changent à chaque itération en fonction du feedback et de l'obstacle cognitif à résoudre. Le process à chaque boucle :

```
1. DIAGNOSTIC — Quel est l'obstacle cognitif actuel ?
2. DÉCLARATION DES AXES — Silas définit 3 variables pertinentes et justifie
3. 3 VERSIONS — toutes qualité max, 3 approches de l'obstacle
4. FEEDBACK AURORE — elle choisit, fusionne, ou rejette
5. BOUCLE — les axes mutent, on recommence
```

### 4.3 Critères de sélection

Aurore tranche entre les 3 versions selon :

| Critère | Question |
|---------|----------|
| **Charge cognitive** | Laquelle encode le plus d'information en un seul regard, sans effort ? |
| **Émotion clinique** | Laquelle crée le déclic — "ça, c'est mon patient" ? |
| **Esthétique éditoriale** | Laquelle atteint le standard visuel Q2 ? |

### 4.4 Ce que cela implique

- Chaque itération commence par la **Déclaration des Axes** (pas de design avant)
- Les 3 versions respectent les mêmes contraintes MDPI et le même budget texte
- Aurore valide avant l'étape suivante du pipeline
- Les axes évoluent : ce qui était un axe à l'itération N peut être une constante à N+1
