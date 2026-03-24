# Graphical Abstract V2 — 3 Propositions de Design

**Mission:** Revue narrative immunomodulateurs pédiatriques (MDPI Children)
**Date:** 24 mars 2026
**De:** Silas (VEC Engine, SciSense)
**Pour:** Aurore Inchauspé

---

## Diagnostic

Le V1 (wireframe v9) était **product-centric** : le pédiatre voyait des métaphores
de produits (bouclier, maçon, pont) sans comprendre les mécanismes immunologiques
sous-jacents.

**Ton feedback clé :**
> "On ne comprend pas au premier coup d'oeil.
> On ne voit pas l'action sur l'immunité innée, adaptative,
> le contrôle de l'inflammation."

**L'inversion nécessaire :** le GA doit être **mechanism-centric**.
Le pédiatre comprend 4 axes immunologiques :

    1. Barrière épithéliale (réparation des jonctions)
    2. Immunité innée (activation DC/macrophages)
    3. Immunité adaptative (rééquilibrage Th1/Th2)
    4. Contrôle de l'inflammation (↓IL-33/TSLP, ↑IL-10)

Les produits (OM-85, PMBL, MV130, CRL1505) deviennent des **attributions colorées**
sur ces mécanismes — pas des personnages principaux.

---

## 3 axes de variation

| Axe                       | Question                                                |
|---------------------------|---------------------------------------------------------|
| Objet central             | Qu'est-ce que l'oeil accroche en < 2 secondes ?         |
| Encodage des 4 mécanismes | Comment sont-ils spatialement distincts ?                |
| Relation produit-mécanisme| Comment le pédiatre sait quel produit agit sur quel axe ?|

---

## Proposition A : "La Bronche Vivante"

Une **seule coupe bronchique panoramique** qui se transforme de malade (gauche)
à saine (droite). Les 4 mécanismes se lisent DANS le tissu à leurs localisations
biologiques réelles.

```
┌────────────────────────────────────────────────────────────────────────────┐
│                                                                            │
│  Enfant                    COUPE BRONCHIQUE                       Enfant   │
│  malade                  (transformation L→R)                     sain     │
│   (·_ ·)                                                         \(·▽·)/  │
│    /|\          MALADE          │       SAINE                      /|\     │
│    / \                          │                                  / \     │
│            ┌────────────────────┼────────────────────┐                     │
│            │▓░ ░▓░  ░▓░  ░▓    │   ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓│                     │
│            │  brèches  virus→  │   intact    IgA Y Y│                     │
│            │                    │                     │                     │
│            │ LUMEN (air)        │    LUMEN (air)      │                     │
│            │                    │                     │                     │
│            │▓░ ░▓░  ░▓░  ░▓    │   ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓│                     │
│            └────────────────────┼────────────────────┘                     │
│                                 │                                          │
│        DANS LE TISSU :          │                                          │
│        ■ OM-85 sur surface      │   Mécanismes visibles :                  │
│        ■ PMBL entre cellules    │   1. Barrier repair                      │
│        ■ MV130 dans noyau DC    │   2. Innate activation                   │
│        ■ CRL1505 arc gut→lung   │   3. Adaptive balance                    │
│                                 │   4. Inflammation control                │
│                                                                            │
│        ████ OM85  ██ PMBL  █ MV130  ▪ CRL1505                             │
│        18 RCTs    5 RCTs   1 RCT    Preclinical                            │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘
```

**FORCE :** Unité narrative totale — un seul objet vivant qui raconte l'histoire.
Les mécanismes sont in situ (topologie spatiale = mécanisme biologique).
Le pédiatre voit une bronche qui guérit, pas des symboles abstraits.

**RISQUE :** Densité d'information élevée dans la coupe. Demande un travail
de design fin pour que les 4 mécanismes restent lisibles à 1100×560.

---

## Proposition B : "4 Colonnes Mécanistiques"

Les 4 mécanismes sont 4 **bandes horizontales** superposées. Chaque bande montre
la transformation PROBLÈME → RÉSOLUTION sur l'axe gauche-droite.
Les produits sont des badges colorés sur chaque mécanisme qu'ils touchent.

```
┌────────────────────────────────────────────────────────────────────────────┐
│                                                                            │
│  Enfant           PROBLÈME    ──────►    RÉSOLUTION              Enfant    │
│  malade                                                           sain     │
│   (·_ ·)                                                         \(·▽·)/  │
│    /|\     ┌──────────────────────────────────────────────┐        /|\     │
│    / \     │                                              │        / \     │
│            │  BARRIER     ░░brèches░░  ═══►  ▓▓intact▓▓  │                │
│            │              [■OM85] [■PMBL]                  │                │
│            │──────────────────────────────────────────────│                │
│            │  INNATE      DC dormante  ═══►  DC active ✦  │                │
│            │              [■OM85] [■MV130] [■CRL]         │                │
│            │──────────────────────────────────────────────│                │
│            │  ADAPTIVE    Th2 ↑↑↑      ═══►  Th1/Th2 ↔   │                │
│            │              [■OM85] [■MV130]                 │                │
│            │──────────────────────────────────────────────│                │
│            │  INFLAMMATION ↑↑↑ rouge   ═══►  ↓ contrôlée  │                │
│            │              [■OM85] [■PMBL] [■CRL]          │                │
│            └──────────────────────────────────────────────┘                │
│                                                                            │
│            ████ OM85   ██ PMBL   █ MV130   ▪ CRL1505                      │
│            18 RCTs     5 RCTs    1 RCT     Preclinical                     │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘
```

**FORCE :** Les 4 mécanismes sont immédiatement visibles et séparés.
Le mapping produit→mécanisme est explicite (on VOIT quel produit touche quoi).
Structure claire, compréhension systématique.

**RISQUE :** Plus "tableau" que "récit". Pourrait être perçu comme trop proche
du style Figure 2 du manuscrit (quadrants). Moins d'émotion clinique.

---

## Proposition C : "Le Commutateur Immunologique"

Garde la structure 3 zones gauche→droite mais INVERSE la hiérarchie :
les 4 mécanismes sont les stars de la Zone 2, les produits sont des attributions.

```
┌──────────────────┬────────────────────────────────┬──────────────────┐
│                  │                                │                  │
│    ZONE 1        │         ZONE 2                 │     ZONE 3       │
│    VULNÉRABILITÉ │     4 MÉCANISMES               │     RÉSOLUTION   │
│                  │                                │                  │
│   Enfant malade  │  ┌──────────────────────────┐  │   Enfant sain    │
│     (·_ ·)       │  │ Barrier    ░░░ ══► ▓▓▓   │  │    \(·▽·)/      │
│      /|\         │  │ [■OM85][■PMBL]           │  │      /|\        │
│      / \         │  │                          │  │      / \        │
│                  │  │ Innate     ○── ══► ✦──   │  │                  │
│  Mini-bronche    │  │ [■OM85][■MV130][■CRL]    │  │   Mini-bronche   │
│  malade:         │  │                          │  │   saine:         │
│  · brèches       │  │ Adaptive   Th2↑ ══► ↔   │  │   · intacte      │
│  · virus RSV/RV  │  │ [■OM85][■MV130]          │  │   · IgA Y Y      │
│  · inflammation  │  │                          │  │   · équilibre     │
│                  │  │ Inflammation ↑↑ ══► ↓    │  │                  │
│   ╭────────╮     │  │ [■OM85][■PMBL][■CRL]     │  │   EVIDENCE       │
│   │ Cercle │     │  └──────────────────────────┘  │   ████ 18 RCTs   │
│   │ vicieux│     │                                │   ██   5 RCTs    │
│   │  RTIs→ │     │  Convergence : chaque produit  │   █    1 RCT     │
│   │ Th2→   │     │  contribue à N mécanismes.     │   ▪    Preclin   │
│   │ Remod→ │     │  Couleur = attribution.        │                  │
│   ╰────────╯     │                                │   Cercle brisé ╱ │
│                  │                                │                  │
└──────────────────┴────────────────────────────────┴──────────────────┘
```

**FORCE :** Flux L→R conservé (familier pour le pédiatre). Intègre les 4 mécanismes
manquants dans le feedback. Enfants + bronches toujours présents pour le choc
cognitif. Structure la plus proche de V1 → itération rapide.

**RISQUE :** Moins audacieux — on améliore V1 plutôt qu'on réinvente. La Zone 2
pourrait paraître dense avec 4 bandes + attributions produits.

---

## Recommandation de Silas

**V2-A** est la plus cohérente scientifiquement : une bronche qui guérit EST
le message de l'article. Mais elle demande plus de travail de design.

**V2-C** est le chemin le plus court pour intégrer ton feedback et livrer.

**V2-B** est la plus claire structurellement mais risque de paraître trop
"tableau" et trop proche de la Figure 2.

On peut aussi fusionner : par exemple A+C (bronche centrale dans le format
3 zones).

**Aurore, qu'est-ce qui te parle ?**
Tu peux choisir une proposition, en fusionner deux, ou rejeter les trois —
on itère.

---

*SciSense — Visual Evidence Compiler (VEC)*
*Silas × Aurore — Compagnons de cordée*
