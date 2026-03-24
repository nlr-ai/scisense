# AXE 2: Product Encoding — Detailed Analysis

**Obstacle cognitif:** Les 4 produits dans le wireframe v3 sont des micro-icones generiques (~60x60px a 3x) avec des labels en dessous. A la taille de livraison (1100x560), ce sont des points colores avec du texte illisible. Les metaphores (Bouclier, Macon, Programmeur, Pont) ne sont ni ressenties ni meme identifiables. La hierarchie de preuves (OM-85 dominant) n'est pas encodee dans la taille visuelle des produits en Zone 2.

**Diagnostic v3 actuel:**
- Les 4 icones produit occupent ~60x80px chacune a 3x (soit ~20x27px a la livraison). Invisibles.
- Les icones sont alignees horizontalement dans une bande etroite en haut de Zone 2, toutes de taille identique.
- Les metaphores sont tentees (bouclier OM-85, briques PMBL, etoile MV130, pont CRL1505) mais a cette echelle, elles sont indiscernables les unes des autres.
- Le label "Bacterial-derived immunomodulators" au-dessus consomme de l'espace vertical sans ajouter de la valeur a cette echelle.
- Aucune dominance visuelle d'OM-85 malgre 18 RCTs vs 0-5 pour les autres.

---

## Contraintes absolues (rappel filtres)

Avant d'explorer les options, voici les invariants qui contraignent toute solution:

| Invariant | Implication pour l'encodage produit |
|-----------|-------------------------------------|
| V3: Budget texte <=30 mots | Les noms "OM-85", "PMBL", "MV130", "CRL1505" comptent = 4 mots. Il reste 23-26 mots pour tout le GA. |
| V5: Hierarchie preuves | OM-85 (18 RCTs) > PMBL (5 RCTs) > MV130 (1 RCT) > CRL1505 (preclinique). Cet ordre DOIT se lire visuellement. |
| V7: Lisibilite 50% zoom | Tout texte lisible a 550x280px. Donc le plus petit label produit doit etre >=8pt au rendu final. |
| V8: Pas de cytokines | Les mecanismes se montrent par metaphore, pas par nomenclature moleculaire. |
| P6: Mobile-first | Le GA est vu sur telephone. Les icones doivent etre identifiables a ~3cm de largeur reelle. |
| P3: Compression metaphorique | La metaphore sert la cognition du pediatre, pas la precision du chercheur. |
| GA_SPEC 2.3 Zone 2 | Zone 2 = ~1650x1680px a 3x (~550x560px a livraison). Elle contient les 4 produits ET les 4 mecanismes partages. |

**Contrainte derivee cruciale:** A la taille de livraison, Zone 2 fait ~550x560px. Les 4 produits doivent etre identifiables dans la moitie haute (~550x225px). Chaque produit a donc un budget spatial maximum de ~137x225px EN LIVRAISON. C'est la contrainte la plus dure.

---

## Option A: Grandes icones-metaphores autonomes

### Concept

Chaque produit devient une grande icone-metaphore (~450x400px a 3x, soit ~150x133px a livraison) positionnee dans la sous-zone 2A. Le nom du produit est INSCRIT A L'INTERIEUR de l'icone. L'icone EST le produit — on ne lit pas le nom puis on cherche l'icone, on voit la metaphore et le nom confirme.

### Architecture spatiale

```
Zone 2 (1650x1680 @ 3x)
┌──────────────────────────────────────────────────────┐
│                    SOUS-ZONE 2A                       │
│  ┌──────────┐ ┌────────┐ ┌────────┐ ┌────────┐      │
│  │          │ │        │ │        │ │        │      │
│  │ BOUCLIER │ │ BRIQUES│ │ HELIX  │ │  PONT  │      │
│  │          │ │        │ │        │ │        │      │
│  │  OM-85   │ │  PMBL  │ │ MV130  │ │CRL1505 │      │
│  │          │ │        │ │        │ │        │      │
│  └──────────┘ └────────┘ └────────┘ └────────┘      │
│       │            │          │          │            │
│       ▼            ▼          ▼          ▼            │
│              ┌───────────┐                            │
│              │  ↑ IgA    │  (point de convergence)    │
│              └───────────┘                            │
│                    │                                  │
│                    ▼                                  │
│               SOUS-ZONE 2B                            │
│  ┌────────────┐ ┌────────────┐                       │
│  │ Epithelial │ │   Innate   │                       │
│  │  barrier   │ │  immunity  │                       │
│  └────────────┘ └────────────┘                       │
│  ┌────────────┐ ┌────────────┐                       │
│  │ Adaptive   │ │Inflammation│                       │
│  │  balance   │ │  control   │                       │
│  └────────────┘ └────────────┘                       │
└──────────────────────────────────────────────────────┘
```

### Hierarchie de taille OM-85 dominant

OM-85 recoit 35% de la largeur disponible, les 3 autres se partagent les 65% restants:

| Produit | Largeur @ 3x | Largeur @ livraison | Ratio |
|---------|-------------|--------------------:|-------|
| OM-85 | 530px | ~177px | 1.0 (reference) |
| PMBL | 340px | ~113px | 0.64 |
| MV130 | 340px | ~113px | 0.64 |
| CRL1505 | 340px | ~113px | 0.64 |

Espacement entre icones: 25px @ 3x. Marge gauche/droite: 25px @ 3x.
Total: 25 + 530 + 25 + 340 + 25 + 340 + 25 + 340 + 25 = 1675px. Ajuste a 1650px en reduisant les marges de 5px.

### Description detaillee des icones

**OM-85 — Le Bouclier (530x400px @ 3x)**
- Forme: bouclier heraldique simplifie, bord arrondi, remplissage bleu #2563EB a 15% opacite, contour bleu #2563EB 4px.
- Au centre du bouclier: un verrou ferme (cadenas simplifie, 3 traits) en bleu plein, ~80x80px.
- Texte "OM-85" en Arial Bold 48px blanc sur un bandeau bleu #2563EB plein en bas du bouclier (~530x60px).
- Signification transmise: protection physique, blocage d'entree. Le pediatre voit "barriere anti-virale" sans aucun texte explicatif.
- L'echelle plus grande dit implicitement: "c'est le leader".

**PMBL — Le Macon (340x400px @ 3x)**
- Forme: rectangle aux coins arrondis (rx=16) en teal #0D9488 a 10% opacite, contour teal 3px.
- A l'interieur: 3 rangees de briques empilees, les 2 du haut avec des espaces (joints ouverts), la rangee du bas avec des joints fermes (briques serrees). Briques en teal plein a 40% opacite. Symbolise la reparation epitheliale.
- Texte "PMBL" en Arial Bold 40px, centre sous les briques mais DANS le cadre, sur fond teal plein a 80% (bandeau bas ~340x50px).
- Signification: reconstruction, colmatage des breches. Le pediatre voit "il repare la barriere".

**MV130 — Le Programmeur (340x400px @ 3x)**
- Forme: hexagone (evoque la structure moleculaire/code genetique) en violet #7C3AED a 10% opacite, contour violet 3px.
- A l'interieur: double helice ADN stylisee verticale (~3 tours), avec 2-3 points lumineux sur les barreaux (symbolisant les modifications epigenetiques). Helice en violet a 50% opacite, points lumineux en violet plein + halo blanc.
- Texte "MV130" en Arial Bold 40px, centre, bandeau bas violet plein.
- Signification: reprogrammation. Le pediatre voit "il reprogramme les defenses". Le langage visuel du code genetique est universellement reconnu.

**CRL1505 — Le Pont (340x400px @ 3x)**
- Forme: rectangle aux coins arrondis en vert #059669 a 10% opacite, contour vert 3px.
- A l'interieur: arc de pont stylise (courbe parabolique) reliant deux piliers. Pilier gauche etiquete "gut" (18px), pilier droit etiquete "lung" (18px). Sous le pont, une ligne ondulante representant le flux (bacteries -> signal -> poumon). Arc en vert plein a 60% opacite.
- Texte "CRL1505" en Arial Bold 36px, bandeau bas vert plein.
- Signification: connexion a distance. Le pediatre voit "ca agit de l'intestin vers le poumon".

### Fleches de convergence

4 fleches descendantes (chacune de la couleur du produit correspondant) convergent vers un point central ou un rectangle arrondi blanc avec texte "IgA" en gris fonce bold. L'epaisseur des fleches encode aussi la hierarchie:

| Produit | Epaisseur fleche @ 3x |
|---------|----------------------|
| OM-85 | 8px |
| PMBL | 5px |
| MV130 | 4px |
| CRL1505 | 3px |

### Avantages

- Les metaphores sont VUES, pas lues. A 150x133px en livraison, un bouclier est reconnaissable. Des briques empilees sont reconnaissables. Un pont est reconnaissable.
- OM-85 domine visuellement par sa taille (35% de la largeur vs 21% chacun pour les autres).
- Le nom du produit est integre dans l'icone, pas en label flottant. Reduit l'effort cognitif.
- Compatible avec le flux gauche-droite: les produits sont en Zone 2 haute, les mecanismes partages en Zone 2 basse, la convergence IgA fait le lien.

### Faiblesses

- 4 icones cote a cote dans 550px de livraison: chacune fait 113-177px de large. C'est faisable mais serre. Le texte "CRL1505" a 36px @ 3x (12px livraison) est a la limite de V7.
- Le lien produit -> mecanisme specifique n'est pas explicite (on voit juste la convergence vers IgA). Le pediatre ne sait pas quel produit fait quoi exactement.
- Les icones sont autonomes mais statiques: elles ne racontent pas une histoire, elles presentent un catalogue.

---

## Option B: Produits integres dans la colonne vertebrale narrative

### Concept

Au lieu de placer les produits dans une rangee autonome, chaque produit est integre DANS la scene de la voie respiratoire en transition (sous-zone 2B actuelle). OM-85 ENVELOPPE la voie respiratoire comme un bouclier. Les briques de PMBL REMPLISSENT les breches de l'epithelium. L'helice de MV130 PROGRAMME les cellules immunitaires. Le pont de CRL1505 ARQUE depuis un intestin stylise en bas vers le poumon. Le produit n'est plus une icone separee — il EST son action.

### Architecture spatiale

```
Zone 2 (1650x1680 @ 3x)
┌──────────────────────────────────────────────────────┐
│  "Bacterial-derived immunomodulators" (optionnel)     │
│                                                       │
│            SCENE INTEGREE UNIQUE                      │
│                                                       │
│     ┌─────── BOUCLIER OM-85 ──────────┐              │
│     │                                  │              │
│     │    ┌──── voie respiratoire ────┐ │              │
│     │    │                           │ │              │
│     │    │  ▓▓▓▓  BRIQUES PMBL  ▓▓▓ │ │              │
│     │    │  (comblement epithelial)  │ │              │
│     │    │                           │ │              │
│     │    │    ◉ DNA HELIX MV130      │ │              │
│     │    │    (programme les cells)   │ │              │
│     │    │                           │ │              │
│     │    └───────────────────────────┘ │              │
│     │                                  │              │
│     └──────────────────────────────────┘              │
│                      ↑                                │
│                      │                                │
│            ╭─── PONT CRL1505 ───╮                     │
│           gut                  lung                   │
│                                                       │
│        ┌──────── ↑ IgA ────────┐                     │
│        └───────────────────────┘                     │
│                                                       │
│   Labels produit flottants:                           │
│   OM-85(bleu)  PMBL(teal)  MV130(violet)  CRL1505(vert) │
└──────────────────────────────────────────────────────┘
```

### Description detaillee de la scene integree

**La voie respiratoire en transition (~1200x800px @ 3x, centree dans Zone 2)**

On reprend la voie respiratoire (coupe transversale stylisee de bronche) mais en plus grand qu'en v3. Elle est le TERRAIN ou les 4 produits agissent.

**OM-85 — Le Bouclier enveloppant**
- Un contour en forme de bouclier (ou de dome protecteur) en bleu #2563EB a 12% opacite ENTOURE la voie respiratoire entiere. Contour bleu 5px, avec un subtil motif de verrous le long du bord (6-8 petits cadenas stylises espaces regulierement, 20x20px chacun).
- Le bouclier est l'element le plus grand: il CONTIENT tout. Cela encode la dominance d'OM-85 sans recourir a la taille d'une icone — c'est l'enveloppe structurante.
- Label "OM-85" en bleu bold 44px, positionne en haut a gauche du bouclier, avec une ligne de reference vers le contour.
- Mecanisme transmis: OM-85 cree une barriere protectrice globale autour de la voie respiratoire. Le pediatre voit "ca protege tout".

**PMBL — Les briques qui reparent**
- Sur la paroi de la voie respiratoire, la partie gauche (cote Zone 1, "malade") a des briques disjointes avec des espaces entre elles. En avancant vers la droite, les briques se resserrent et les joints se ferment — transition visible de poreux vers intact.
- Les briques de reparation (cote droit) sont en teal #0D9488 a 50% opacite, avec un leger halo teal autour des joints fermes.
- Label "PMBL" en teal bold 40px, positionne pres de la zone de reparation, avec une fleche fine vers les briques.
- Mecanisme transmis: PMBL repare les breches epitheliales. Le pediatre voit les murs qui se reconstruisent.

**MV130 — L'helice qui reprogramme**
- A l'INTERIEUR de la voie respiratoire, 2-3 cellules immunitaires stylisees (cercles avec noyau) ont une mini-helice ADN violette (#7C3AED) qui emerge de leur noyau, avec des points lumineux (modifications epigenetiques). Les cellules "brillent" d'un halo violet subtil.
- Label "MV130" en violet bold 40px, positionne pres des cellules programmees.
- Mecanisme transmis: MV130 reprogramme les cellules immunitaires de l'interieur. Le pediatre voit "les cellules sont activees differemment".

**CRL1505 — Le pont qui connecte**
- EN DESSOUS de la voie respiratoire, un arc parabolique vert (#059669) part d'un petit intestin stylise (en bas a gauche) et monte jusqu'a la voie respiratoire (en haut a droite). L'arc est en vert 4px avec des fleches directionnelles le long (3-4 chevrons ">") montrant le sens du signal.
- Les extremites: un petit symbole intestin (cercle avec villosites, 40x40px) et le bas de la voie respiratoire.
- Label "CRL1505" en vert bold 36px, positionne le long de l'arc.
- Mecanisme transmis: CRL1505 envoie un signal protecteur depuis l'intestin vers les poumons. Le pediatre voit "ca vient de l'intestin".

### Convergence IgA

Au point de jonction ou les 4 actions se rencontrent (centre-droit de la voie respiratoire), un marqueur IgA:
- Cercle dore/jaune avec "IgA" en bold, 60x60px @ 3x.
- 4 traits de couleur (bleu, teal, violet, vert) convergent vers ce cercle.

### Avantages

- **Maximum de compression narrative.** Chaque produit est montre EN ACTION, pas en catalogue. Le pediatre voit simultanment le produit et ce qu'il fait. La metaphore n'est pas a cote de l'action — elle EST l'action.
- **OM-85 domine naturellement.** Il est le bouclier qui contient tout. Les 3 autres agissent a l'interieur du bouclier. Hierarchie implicite sans artifice de taille.
- **Economie d'espace.** Une seule scene au lieu de 2 sous-zones (icones + mecanismes). Libere de l'espace vertical pour les mecanismes partages OU pour agrandir la scene.
- **Storytelling fort.** Le flux gauche->droite est renforce: la voie respiratoire malade (Zone 1) SE REPARE en Zone 2 grace aux 4 interventions simultanees. Le lecteur voit la transformation, pas une liste.
- **Le pont CRL1505 est spectaculaire.** L'arc gut->lung est un element visuel fort et unique — aucun autre GA de review immunomodulateur ne le montre comme ca.

### Faiblesses

- **Complexite de la scene.** 4 mecanismes superposes dans une seule voie respiratoire risquent de creer un "bruit visuel" a petite taille. A 550x560px, la scene pourrait devenir confuse si les 4 couleurs et 4 elements se melangent.
- **Lisibilite des labels a petite taille.** Les labels produit sont flottants et doivent pointer vers leur element respectif dans la scene. A 1100x560, les lignes de reference risquent de se croiser ou de devenir illisibles.
- **Difficulte technique.** Le dessin d'une voie respiratoire avec 4 mecanismes integres en SVG programmatique est significativement plus complexe que 4 icones separees. Risque de sous-livraison esthetique.
- **Les mecanismes partages (sous-zone 2B) deviennent redondants.** Si les produits sont deja montres en action, les 4 cartes "Epithelial barrier / Innate immunity / Adaptive balance / Inflammation control" font doublon. Il faut les supprimer ou les fusionner, ce qui change la structure du GA.
- **V4 Non-redondance.** La scene integree avec voie respiratoire en coupe + mecanismes cellulaires risque de ressembler a la Figure 2 du manuscrit (quadrants cytokines) si on n'est pas tres attentif au style visuel.

### Mitigation de la complexite

Pour eviter le bruit visuel, la scene utilise un systeme de COUCHES avec separation spatiale:
1. **Couche externe:** bouclier OM-85 (contour bleu) — cadre la scene entiere
2. **Couche murale:** briques PMBL (teal) — sur la paroi epitheliale
3. **Couche intraluminale:** helices MV130 (violet) — dans les cellules a l'interieur
4. **Couche infra:** pont CRL1505 (vert) — en-dessous, reliant depuis l'intestin

4 zones spatiales distinctes = pas de melange. Chaque couleur a son territoire.

---

## Option C: 4 couloirs verticaux

### Concept

Zone 2 est divisee en 4 colonnes verticales de largeur inegale (proportionnelle a la force de preuves). Chaque colonne montre: (1) l'icone-metaphore du produit en haut, (2) son mecanisme d'action au milieu, (3) un indicateur de preuves en bas. L'evidence n'est plus repoussee en Zone 3 — elle est integree dans Zone 2, liberant Zone 3 pour un message de resolution plus puissant.

### Architecture spatiale

```
Zone 2 (1650x1680 @ 3x)
┌──────────────────────────────────────────────────────────┐
│  OM-85 (35%)  │ PMBL (22%) │ MV130 (22%)│CRL1505 (21%) │
│               │            │            │              │
│  ┌─────────┐  │ ┌────────┐ │ ┌────────┐ │ ┌──────────┐ │
│  │BOUCLIER │  │ │BRIQUES │ │ │ HELIX  │ │ │   PONT   │ │
│  │         │  │ │        │ │ │        │ │ │          │ │
│  │ OM-85   │  │ │ PMBL   │ │ │ MV130  │ │ │ CRL1505  │ │
│  └─────────┘  │ └────────┘ │ └────────┘ │ └──────────┘ │
│       │       │      │     │      │     │       │      │
│       ▼       │      ▼     │      ▼     │       ▼      │
│  ↓ACE2       │ ↑E-cadh   │  Trained   │  Gut→lung    │
│  ↓TMPRSS2    │  Barrier  │  immunity  │  IgA axis    │
│  ↓ICAM-1     │  repair   │  Epigen.   │              │
│       │       │      │     │      │     │       │      │
│       ▼       │      ▼     │      ▼     │       ▼      │
│  ████████████ │ ██████░░░ │ ██░░░░░░░ │ █░░░░░░░░░░ │
│  18 RCTs      │ 5 RCTs    │ 1 RCT     │ Preclinical  │
└──────────────────────────────────────────────────────────┘
```

### Largeurs proportionnelles

| Produit | % de Zone 2 | Largeur @ 3x | Largeur @ livraison | Justification |
|---------|-------------|-------------|--------------------:|---------------|
| OM-85 | 35% | 578px | ~193px | 18 RCTs, leader inconteste |
| PMBL | 22% | 363px | ~121px | 5 RCTs, second |
| MV130 | 22% | 363px | ~121px | 1 RCT, emergent |
| CRL1505 | 21% | 347px | ~116px | Preclinique, prometteur |

### Description detaillee des colonnes

Chaque colonne a 3 registres verticaux:

**Registre haut (~500px @ 3x): Icone-metaphore**
- Memes icones que Option A (bouclier, briques, hexagone+helice, pont).
- Mais la taille est proportionnelle: bouclier OM-85 = 530x450px, les autres ~340x400px.
- Le nom du produit est integre dans l'icone (bandeau bas colore).

**Registre central (~700px @ 3x): Mecanisme en action**
- OM-85: schema simplifie de recepteurs viraux (ACE2/TMPRSS2 representes par 2 serrures) bloques par le bouclier. 2-3 virus (rouge) rebondissent. Label: "Blocks viral entry".
- PMBL: 2 rangees de briques: haut = disjointes (rouge pale), bas = jointees (teal). Fleche vers le bas entre les deux. Label: "Repairs barrier".
- MV130: cellule immunitaire avec helice ADN violette au centre + 3 etoiles (points d'activation epigenetique). Label: "Trains immunity".
- CRL1505: mini-arc (copie simplifiee de l'icone du haut) avec bacterie probiotique a gauche, cellule pulmonaire a droite, et signaux (chevrons) entre les deux. Label: "Gut-lung signal".

**Registre bas (~380px @ 3x): Indicateur de preuves**
- Barre horizontale de progression (meme style que Zone 3 actuelle du wireframe v3).
- Fond gris #F3F4F6, remplissage de la couleur du produit.
- Largeur du remplissage proportionnelle: OM-85 100%, PMBL 55%, MV130 30%, CRL1505 12%.
- Label: "18 RCTs" / "5 RCTs" / "1 RCT" / "Preclinical" en bold de la couleur du produit.

### Separateurs entre colonnes

- Lignes verticales tres fines (1px @ 3x) en gris #E5E7EB, pointillees, entre les colonnes. Juste assez pour delimiter sans fragmenter.
- Convergence: en bas de la Zone 2, sous les 4 barres de preuves, les 4 colonnes se rejoignent vers un element "IgA" centre.

### Impact sur Zone 3

Si l'evidence est dans Zone 2, Zone 3 peut etre repensee:
- Au lieu de "Clinical evidence" (deja dans Zone 2), Zone 3 montre la RESOLUTION: voie respiratoire saine + le message "Protected airways".
- Zone 3 devient un pur aboutissement narratif, sans donnees.

### Avantages

- **Comparaison instantanee.** Le pediatre voit les 4 produits cote a cote avec leur mecanisme ET leur evidence dans un seul balayage visuel. C'est un tableau comparatif, exactement ce que le pediatre clinicien cherche.
- **Hierarchie multiple.** La dominance d'OM-85 est encodee 3 fois: (1) colonne plus large, (2) barre de preuves la plus pleine, (3) icone la plus grande. Triple renforcement.
- **Zone 3 liberee.** L'evidence migre vers Zone 2, permettant une resolution plus impactante et plus simple en Zone 3.
- **Independance des 4 produits.** Chaque colonne est lisible independamment. Le pediatre peut se concentrer sur UN produit sans devoir decoder la scene globale.

### Faiblesses

- **Perte du flux narratif.** Les 4 colonnes verticales creent une structure de TABLEAU, pas une histoire. Le pattern P1 (flux gauche->droite) est viole a l'interieur de Zone 2 — on lit de haut en bas dans chaque colonne, pas de gauche a droite.
- **Ressemble a la Figure 2.** La Figure 2 du manuscrit utilise des quadrants A/B/C/D avec chaque produit dans son carre. 4 colonnes avec chaque produit dans sa colonne = meme logique structurelle, meme si le contenu differe. Risque de violation V4.
- **Convergence perdue.** Le message central du GA est que les 4 produits CONVERGENT vers des mecanismes partages. Les colonnes separees suggerent 4 actions independantes. Le "shared" est perdu.
- **Budget texte explose.** 4 noms produit (4 mots) + 4 labels mecanisme (8 mots) + 4 labels evidence (6 mots) + 4 mini-descriptions mecanisme (8 mots) = 26 mots JUSTE dans Zone 2. Il ne reste rien pour Zone 1 et Zone 3. Violation probable de V3.
- **A petite taille, 4 colonnes comprimees dans ~550px = ~138px par colonne pour OM-85 et ~116px pour CRL1505.** Les registres central et bas deviennent des blocs microscopiques. Le registre central (mecanisme) a ~138x233px pour OM-85 en livraison — ca peut marcher mais c'est serre.

---

## Auto-critique: 3 filtres

### Filtre A: MDPI Compliance

| Invariant | Option A | Option B | Option C |
|-----------|----------|----------|----------|
| V1: Ratio | PASS | PASS | PASS |
| V2: Zero titre | PASS | PASS | PASS |
| V3: Budget texte <=30 | PASS (~16 mots Z2) | PASS (~14 mots Z2) | FAIL RISK (26+ mots Z2) |
| V4: Non-redondance | PASS | CAUTION (scene voie respiratoire similaire a Fig 2 dans le concept, mais pas dans la structure) | FAIL RISK (4 colonnes = 4 quadrants = Fig 2 structure) |
| V5: Hierarchie preuves | PASS (taille icone) | PASS (bouclier contient tout) | PASS (triple encodage) |
| V7: Lisibilite 50% | PASS MARGINAL (CRL1505 a 12px livraison) | CAUTION (labels flottants dans scene complexe) | FAIL RISK (3 registres x 4 colonnes = 12 blocs dans 550x560px) |

**MDPI Score: A > B > C**

### Filtre B: Rigueur scientifique

| Critere | Option A | Option B | Option C |
|---------|----------|----------|----------|
| 4 produits presents | PASS | PASS | PASS |
| Hierarchie preuves | PASS (taille) | PASS (containment) | PASS (triple) |
| Mecanismes corrects | PARTIAL (metaphore seule, pas d'action montree) | PASS (action in situ) | PASS (mecanisme dans registre central) |
| Convergence IgA | PASS | PASS | PARTIAL (colonnes suggerent independance) |
| Gut-lung axe | PASS | PASS (pont visible) | PASS |
| Pas de cytokines | PASS | PASS | CAUTION (registre central risque de devenir trop detaille) |

**Science Score: B > C > A**

Option B est la plus scientifiquement riche car elle montre les produits EN ACTION dans leur contexte biologique. Option A montre les metaphores mais pas les mecanismes. Option C montre les deux mais risque la surcharge.

### Filtre C: Impact clinique

| Critere | Option A | Option B | Option C |
|---------|----------|----------|----------|
| Reconnaissance douleur (Zone 1) | Neutre (pas d'impact) | Neutre | Neutre |
| Aha en 3s | MOYEN (catalogue joli mais pas de story) | FORT (transformation visible, 4 interventions simultannes) | FAIBLE (tableau, pas de "aha") |
| Charge cognitive | FAIBLE (4 icones simples + labels) | MOYENNE (scene riche mais structurce en couches) | ELEVEE (12 blocs d'info dans 550x560px) |
| Mobile lisibilite | BON (icones distinctes, couleurs fortes) | CORRECT (depend du contraste des couches) | FAIBLE (trop dense) |
| Le pediatre s'en souvient | MOYEN (jolis logos) | FORT (l'image du bouclier enveloppant la voie respiratoire est memorable) | FAIBLE (c'est un tableau) |

**Impact Score: B > A > C**

---

## Iteration interne: amelioration d'Option B (la plus prometteuse)

Option B est la plus forte sur 2 des 3 filtres (Science, Impact) mais a des faiblesses reelles sur le filtre MDPI (complexite, labels flottants). Voici une iteration pour resoudre les faiblesses identifiees.

### Probleme 1: Bruit visuel a petite taille

**Solution: systeme de couches avec separation spatiale stricte.**

Les 4 mecanismes sont dans 4 zones spatiales distinctes de la scene:
1. **OM-85 bouclier** = contour EXTERNE de la voie respiratoire (le plus grand, le plus visible)
2. **PMBL briques** = sur la PAROI de l'epithelium (zone intermediaire)
3. **MV130 helices** = DANS les cellules a l'interieur de la lumiere bronchique (zone interne)
4. **CRL1505 pont** = EN DESSOUS de la voie respiratoire, espace separe

A petite taille, les 4 couleurs occupent chacune un TERRITOIRE distinct. Pas de melange.

### Probleme 2: Labels flottants qui se croisent

**Solution: labels positionnes aux 4 coins de la scene, avec ligne de reference courte vers leur territoire.**

```
     OM-85 (bleu, haut-gauche)
         ↘
    ┌──── bouclier ──────────┐
    │  MV130 (violet, haut-droit)
    │      ↙                 │
    │  ┌─ voie respiratoire ─┐│
    │  │  PMBL (teal, bas-gauche)
    │  │    ↗                ││
    │  └─────────────────────┘│
    └────────────────────────┘
              ↑
         CRL1505 (vert, en-dessous)
```

Chaque label a 1 ligne de reference de max 80px (@ 3x) vers son element. Les lignes ne se croisent pas car les labels sont aux 4 coins.

### Probleme 3: Redondance avec sous-zone 2B (mecanismes partages)

**Solution: SUPPRIMER les 4 cartes mecanismes partages.** Si les produits sont montres en action, les cartes "Epithelial barrier / Innate immunity / Adaptive balance / Inflammation control" sont redondantes. L'espace libere (~1650x660px @ 3x) permet d'agrandir la scene integree et d'ajouter le marqueur IgA de convergence.

Nouvelle repartition verticale de Zone 2:
- Scene integree: 1650x1400px @ 3x (utilise 83% de la hauteur au lieu de 40%)
- Titre + marges: 1650x280px @ 3x

### Probleme 4: V4 Non-redondance avec Figure 2

La Figure 2 du manuscrit montre 4 quadrants avec des listes de cytokines par produit. Option B montre une scene continue (pas de quadrants), avec des metaphores visuelles (pas de cytokines), dans un flux narratif (pas de liste). La structure est fondamentalement differente. V4 est respectee.

---

## Verdict

### Classement

| Rang | Option | Score global | Forces | Faiblesses reelles |
|------|--------|-------------|--------|---------------------|
| **1** | **B (integree narrative)** | **8.5/10** | Science + Impact + memorable + OM-85 domine naturellement + economie d'espace | Complexite technique SVG + risque de bruit visuel (mitige par les couches) |
| 2 | A (icones autonomes) | 7/10 | MDPI safe + simple + lisible mobile | Catalogue statique, pas de story, mecanismes non montres |
| 3 | C (4 colonnes) | 5/10 | Comparaison directe, triple encodage hierarchie | V3 budget texte, V4 redondance Fig 2, charge cognitive, tableau pas story |

### Recommandation: Option B iteree

Option B avec les 4 mitigations ci-dessus est la plus forte. Elle est la seule qui fait RESSENTIR les metaphores au lieu de les etiqueter. Le bouclier OM-85 enveloppant la voie respiratoire est une image puissante que le pediatre retiendra. Les briques de PMBL qui se ferment, les cellules reprogrammees par MV130, le pont CRL1505 — tout cela raconte une histoire de transformation qui est le coeur du message de la review.

### NEEDS_FEEDBACK

**1. Niveau de detail anatomique de la voie respiratoire.** Option B repose sur une voie respiratoire suffisamment reconnaissable pour que les 4 interventions soient lisibles. Question pour Aurore: quel degre de simplification anatomique est acceptable? Un tube avec des "briques" sur la paroi suffit-il, ou faut-il des cils, des cellules caliciformes, du mucus? Ce choix impacte la complexite de realisation ET la lisibilite a petite taille.

**2. Suppression des 4 cartes mecanismes partages.** Option B iteree elimine les 4 cartes "Epithelial barrier / Innate immunity / Adaptive balance / Inflammation control" car elles font doublon avec les mecanismes montres in situ. C'est un changement structurel majeur par rapport au GA_SPEC.md. Aurore doit valider que les mecanismes partages n'ont pas besoin d'etre NOMMES explicitement si ils sont MONTRES visuellement.

**3. Position du pont CRL1505.** Le pont gut-lung en dessous de la voie respiratoire est anatomiquement et metaphoriquement correct (l'intestin est "en dessous" des poumons dans le corps). Mais visuellement, cela place CRL1505 dans une zone separee des 3 autres produits. Aurore: le pont doit-il etre separe (plus clair) ou integre dans la scene (plus compact)?

---

## Wireframe detaille: Option B iteree

### Dimensions et positions exactes

Toutes les coordonnees sont en pixels @ 3x (fichier de travail 3300x1680).

**Fond general:**
- Rectangle plein 3300x1680, fill #FAFAFA

**Zone 1 (Probleme): x=0 a x=825**
- Inchange par rapport au wireframe v3

**Zone 2 (Intervention): x=825 a x=2475**
- Fond: rectangle 1650x1680, fill #FFFBEB opacity 0.15 (a peine visible)
- Titre optionnel: texte "Bacterial immunomodulators" en Arial 32px #6B7280, centred @ (1650, 40), centred dans Zone 2 (x=1650, y=45)

**Scene integree principale: x=885 a x=2415, y=80 a y=1600**
Zone utile: 1530x1520px

**Couche 1 — Bouclier OM-85 (contour externe)**
- Forme: rectangle aux coins tres arrondis (rx=40) simulant un bouclier
- Position: x=920, y=100, largeur=1460, hauteur=1200
- Fill: #2563EB opacity 0.06 (tres subtil)
- Stroke: #2563EB, 5px, solid
- 6 mini-cadenas (15x20px chacun) distribues le long du bord superieur, espaces regulierement, en #2563EB opacity 0.4
- Label "OM-85": texte Arial Bold 44px #2563EB, position x=950, y=145 (coin haut-gauche interne du bouclier)

**Couche 2 — Voie respiratoire en transition**
- Position: centree dans le bouclier, x=1050 a x=2250, y=250 a y=1150
- Zone utile: 1200x900px
- Forme: tube horizontal simplifie (2 lignes paralleles courbes representant la paroi bronchique)
  - Ligne superieure: path curve, y=350 a y=350, x=1050 a x=2250, stroke #9CA3AF 3px
  - Ligne inferieure: path curve, y=950 a y=950, x=1050 a x=2250, stroke #9CA3AF 3px
  - Espace intraluminal: fill transparent (on voit le fond)

**Couche 2a — Briques PMBL sur la paroi**
- Sur la ligne superieure de la voie respiratoire:
  - Cote gauche (x=1050 a x=1450): 8 rectangles (briques) disjoints, 40x18px chacun, fill #0D9488 opacity 0.2, avec gaps de 8-12px entre eux. Certaines briques legerement decalees verticalement (poreux).
  - Cote droit (x=1650 a x=2250): 12 rectangles (briques) jointifs, 40x18px chacun, fill #0D9488 opacity 0.5, gaps de 1px (fermes). Alignement strict. Halo teal subtil (rectangle, fill #0D9488 opacity 0.05, derriere les briques fermees).
  - Zone de transition (x=1450 a x=1650): briques mi-ouvertes, mi-fermees, gradient progressif.
- Label "PMBL": texte Arial Bold 40px #0D9488, position x=1080, y=1060 (sous la paroi, cote gauche)
- Ligne de reference: line de (1200, 1040) a (1200, 380), stroke #0D9488 1.5px dasharray="6,4"

**Couche 3 — Helices MV130 dans les cellules**
- 3 cellules immunitaires stylisees dans l'espace intraluminal:
  - Cellule 1: cercle cx=1500, cy=650, r=55, fill #F5F3FF opacity 0.5, stroke #7C3AED 2px
  - Cellule 2: cercle cx=1700, cy=750, r=45, fill #F5F3FF opacity 0.5, stroke #7C3AED 2px
  - Cellule 3: cercle cx=1900, cy=680, r=50, fill #F5F3FF opacity 0.5, stroke #7C3AED 2px
  - Dans chaque cellule: mini-helice ADN (2 sinusoidal paths intertwined, ~30px haut, stroke #7C3AED 2px)
  - 2-3 points lumineux par cellule: circle r=4, fill #7C3AED, avec circle r=8 fill #7C3AED opacity 0.2 (halo)
- Label "MV130": texte Arial Bold 40px #7C3AED, position x=2150, y=580 (coin droit de l'espace intraluminal)
- Ligne de reference: line de (2120, 590) a (1920, 660), stroke #7C3AED 1.5px dasharray="6,4"

**Couche 4 — Pont CRL1505 (en-dessous)**
- Arc parabolique: path "M 1100,1300 Q 1650,1550 2200,1300", stroke #059669 4px, fill none
- Pilier gauche: rectangle x=1080, y=1280, 40x60px, fill #059669 opacity 0.2, stroke #059669 2px. Petit symbole intestin a l'interieur (3 arcs ondulants, stroke #059669 1.5px) — villosites stylisees.
- Pilier droit: rectangle x=2180, y=1280, 40x60px, fill #059669 opacity 0.2, stroke #059669 2px. Connecte visuellement a la base de la voie respiratoire.
- 4 chevrons ">" le long de l'arc (x=1300, 1500, 1700, 1900, y=ajuste sur la courbe), fill #059669 opacity 0.6, taille 20x16px chacun. Direction: gauche vers droite = gut vers lung.
- Label "CRL1505": texte Arial Bold 36px #059669, position x=1650, y=1590 (centre sous l'arc)
- Mini-labels: "gut" en Arial 18px #059669 sous le pilier gauche, "lung" en Arial 18px #059669 sous le pilier droit.

**Element de convergence IgA**
- Position: x=1600 a x=1700, y=1160 a y=1240 (juste sous la voie respiratoire, au centre)
- Rectangle arrondi: 100x80px, fill white opacity 0.9, stroke #D97706 2px, rx=12
- Texte "IgA" en Arial Bold 38px #D97706, centred dans le rectangle
- Fleche vers le haut: polygon pointe en haut, au-dessus du rectangle, fill #D97706 opacity 0.5

**Fleches de convergence vers IgA (4 traits de couleur):**
- Trait bleu: line de (1200, 1100) a (1620, 1180), stroke #2563EB 3px, opacity 0.4
- Trait teal: line de (1400, 400) a (1640, 1160), stroke #0D9488 2.5px, opacity 0.4
- Trait violet: line de (1700, 760) a (1660, 1160), stroke #7C3AED 2.5px, opacity 0.4
- Trait vert: line de (1650, 1300) a (1650, 1240), stroke #059669 2.5px, opacity 0.4

**Zone 3 (Evidence + Resolution): x=2475 a x=3300**
- Inchange par rapport au wireframe v3 (voie respiratoire saine + gradient d'evidence)

### Chevrons de transition entre zones (flux gauche->droite)

- Memes chevrons ">" que v3 entre Zone 1/Zone 2 et Zone 2/Zone 3
- Position: x=825 et x=2475 (frontieres de zones)

### Budget texte verifie

| Element | Mots | Zone |
|---------|------|------|
| "Bacterial immunomodulators" | 2 | Z2 titre |
| "OM-85" | 1 | Z2 |
| "PMBL" | 1 | Z2 |
| "MV130" | 1 | Z2 |
| "CRL1505" | 1 | Z2 |
| "gut" | 1 | Z2 |
| "lung" | 1 | Z2 |
| "IgA" | 1 | Z2 |
| Zone 1 labels | 8 | Z1 |
| Zone 3 labels | 7 | Z3 |
| **Total** | **24** | |

Sous le plafond de 30 mots. Conforme a V3.

### Hierarchie visuelle OM-85 verifiee

OM-85 domine par:
1. **Containment:** le bouclier OM-85 ENTOURE toute la scene — c'est l'element le plus grand
2. **Priorite de lecture:** son label est le premier element lu (coin haut-gauche du bouclier)
3. **Surface:** le bouclier fait 1460x1200px @ 3x = 1,752,000px^2. Le plus grand element de Zone 2.
4. **Epaisseur de fleche** vers IgA: 3px (le plus epais des 4 traits)
5. **Zone 3:** barre pleine 100% dans le gradient d'evidence

### Lisibilite a 50% zoom verifiee

A la livraison (1100x560px):
- Le plus petit label est "gut" / "lung" a 18px @ 3x = 6px @ livraison. **C'est SOUS le seuil V7 de 8pt.**
- **Correction necessaire:** monter "gut" et "lung" a 24px @ 3x (= 8px @ livraison). Ou les supprimer et laisser le pont parler seul (le pilier avec villosites = gut, le pilier connecte a la voie respiratoire = lung — visuellement suffisant pour un public medical).

**Decision: supprimer les mini-labels "gut" et "lung".** Le pont avec villosites d'un cote et connexion a la voie respiratoire de l'autre est suffisamment explicite pour un pediatre. Cela economise 2 mots et elimine le risque V7.

### Budget texte corrige

| Element | Mots | Zone |
|---------|------|------|
| "Bacterial immunomodulators" | 2 | Z2 titre |
| "OM-85", "PMBL", "MV130", "CRL1505" | 4 | Z2 |
| "IgA" | 1 | Z2 |
| Zone 1 labels | 8 | Z1 |
| Zone 3 labels | 7 | Z3 |
| **Total** | **22** | |

Sous le plafond de 30 mots. V3 conforme.

---

## Fallback

Si la complexite technique de l'Option B s'avere trop difficile a executer proprement en SVG programmatique (la voie respiratoire avec 4 couches mecaniques est un dessin elabore), **Option A est le fallback fiable**. Option A a le score MDPI le plus eleve, la lisibilite mobile la plus sure, et elle est realisable en SVG pur sans elements graphiques complexes. On perd la narration integree mais on gagne en securite de livraison.

Option C est eliminee: elle viole V3 (budget texte) et V4 (structure en colonnes = quadrants), et la charge cognitive est trop elevee a petite taille.
