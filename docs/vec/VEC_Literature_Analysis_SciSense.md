# Visual Evidence Compiler — Analyse de la Littérature

**SciSense × Mind Protocol — Mars 2026**
**Auteurs : Marco (analyse), Silas (implémentation), Aurore (validation scientifique)**

---

## 1. Position du Problème

SciSense construit le premier **compilateur paramétrique d'évidence visuelle** (VEC) : un système qui transforme de l'évidence scientifique structurée — niveaux de preuve, mécanismes d'action, hiérarchie de certitude — en représentations visuelles où chaque propriété graphique est traçable à une justification scientifique et perceptive.

Le premier cas d'usage est un Graphical Abstract (GA) pour un manuscrit de revue sur 4 immunomodulateurs pédiatriques, soumis à MDPI *Children*. Mais la méthodologie vise la généralisation : tout manuscrit, toute discipline, tout format visuel.

Cette analyse synthétise la littérature scientifique sur deux axes fondamentaux et en extrait des spécifications de design concrètes, des gaps identifiés, et des protocoles de validation.

---

## 2. Axe A — L'Engagement ne Transfère pas en Compréhension

### 2.1 Ce que disent les données

Six études expérimentales (RCT ou crossover prospectif) mesurent l'effet des visual abstracts sur l'engagement :

| Étude | Design | N | Canal primaire | Effet |
|-------|--------|---|----------------|-------|
| Ibrahim et al. 2017, *Ann Surg* | Crossover prospectif | 44 articles | Twitter | ×7.7 impressions, ×8.4 retweets, ×2.7 visites |
| Oska et al. 2020, *JMIR* | Triple crossover | 40 articles | Twitter | ×5 engagements vs texte, ×3.5 vs figure-clé |
| Chapman et al. 2019, *BJS* | RCT 3 bras | 41 articles | Twitter | +57% engagement professionnel (45.3 vs 28.8) |
| Hoffberg et al. 2020, *Frontiers* | Crossover randomisé | 50 articles | Twitter | P<.001 impressions et retweets |
| Chisari et al. 2021, *J Arthroplasty* | Crossover randomisé | 20 articles | Twitter | d=1.68, P=.016 engagement composite |
| Trueger et al. 2023, *JAMA Network* | Crossover simultané | 205 RCTs, 12 journaux | Twitter + Facebook | Médiane 18 vs 9 clics (P<.001, Twitter only) |

Deux études observationnelles rapportent des effets nuls ou négatifs :

| Étude | Design | N | Résultat |
|-------|--------|---|----------|
| Pferschy-Wenzig et al. 2016, *Molecules* | Rétrospectif | 1 326 articles | Sans GA > avec GA (downloads, vues, citations) |
| Aggarwal 2021, *HILJ* | Rétrospectif | 307 articles (NEJM, BMJ, JAMA) | Aucune différence significative (Altmetric P=.37, citations P=.44) |

**Résolution de la contradiction apparente :** Les études expérimentales mesurent l'effet de la *dissémination active* (tweet avec VA vs tweet sans VA). Les études observationnelles mesurent l'effet de la *présence passive* sur le site du journal. L'effet engagement est réel mais conditionné par la stratégie de diffusion, pas par le format seul. De plus, les études rétrospectives souffrent d'un biais de sélection : les auteurs plus établis (dont les articles sont plus cités par défaut) créent moins souvent des GA.

### 2.2 Le fossé engagement-compréhension

C'est la découverte la plus conséquente pour SciSense.

**Bredbenner & Simon (2019, *PLOS ONE*, N=538)** ont directement comparé quatre formats sur la compréhension mesurée (pas l'engagement) :

| Format | Compréhension mesurée (rang) | Préférence déclarée |
|--------|------------------------------|---------------------|
| Video abstract | 1er | Variable |
| Plain language summary | 2ème | Variable |
| **Graphical abstract** | **3ème** | Variable |
| Published abstract | 4ème | Variable |

Conclusion clé : *"la préférence pour différents types de résumés n'était généralement pas corrélée à la compréhension"* — un fossé préférence-performance direct.

**Bennett & Slattery (2023, *Scientometrics*, N=562 articles)** quantifient la dissociation engagement/impact :
- GA → Altmetric score **×1.89** (IRR, P=.003)
- GA → citations : **aucune différence** (IRR 0.97, P=.829)

**Zong, Huang & Deng (2023, *Learned Publishing*)** confirment par propensity score matching : les GA augmentent les clics sur l'abstract mais n'ont *"aucun avantage pour les vues full-text et les citations."*

**Vorland et al. (2024, *J Clin Epidemiol*, N=253 VA de RCTs)** ajoutent un signal d'alarme : les visual abstracts contiennent un *"taux élevé de spin"* par rapport aux abstracts textuels. Le format visuel peut amplifier la distorsion, pas la clarifier.

### 2.3 Implications pour SciSense

**Implication 1 — Les métriques d'engagement ne sont pas des métriques de valeur.** Le GA immunomodulateur ne doit pas être évalué uniquement par l'acceptation de Mindy Ma (R4) ou le partage sur Twitter. Ces signaux mesurent la visibilité, pas l'impact cognitif. SciSense doit développer un protocole de validation par compréhension directe.

**Implication 2 — Le GA comme format est nécessaire mais insuffisant.** Il capture l'attention (prouvé) mais ne transfère pas la compréhension (prouvé aussi). La valeur ajoutée de SciSense doit résider dans la *qualité du design perceptif* — pas dans le fait de produire un GA, mais dans la façon dont l'évidence est encodée visuellement. C'est ce qui distingue un GA SciSense d'un GA BioRender.

**Implication 3 — Le spin est un risque systémique.** La compression visuelle peut trahir la science (exactement ce que VN1 et P3 cherchent à éviter). Le protocole de validation d'Aurore (H2) doit explicitement vérifier l'absence de spin — pas seulement la fidélité des 4 messages clés, mais aussi l'absence de distorsion hiérarchique.

---

## 3. Axe B — L'Encodage Visuel de la Force de l'Évidence

### 3.1 L'état de l'art : GRADE et ses limites

Le framework GRADE utilise un système de cercles remplis (⊕⊕⊕⊕ High → ⊕⊖⊖⊖ Very Low) qui est le seul encodage visuel de la certitude testé expérimentalement :

**Akl et al. (2007, *J Clin Epidemiol*, RCT, N=84) :**
- Symboles → **74% compréhension correcte**
- Chiffres → **14% compréhension correcte**
- P<.001, avec supériorité en facilité de compréhension (md=1.5, P=.001) et clarté (md=1.5, P<.001)

**Schünemann et al. (2003, *CMAJ*)** : les auteurs du système GRADE ont consulté des psychologues, experts marketing et designers graphiques, et n'ont trouvé *"aucune recherche existante en santé"* sur la représentation visuelle optimale des grades d'évidence — un gap qui persiste 20+ ans plus tard.

**Rosenbaum et al. (2010, *J Clin Epidemiol*, RCT, N=33) :** Les tables Summary of Findings (SoF) de Cochrane avec symboles GRADE → **93% compréhension correcte** vs 44% sans (P=.003).

**Limites de GRADE pour le VEC :**
- Canal unique : remplissage seulement (pas de position, longueur, luminance)
- Format unique : tableau exclusivement (jamais testé dans un contexte narratif visuel)
- Granularité limitée : 4 niveaux seulement
- Non paramétrique : pas de mapping continu entre données et propriétés visuelles

### 3.2 La hiérarchie perceptive de Cleveland & McGill

Cleveland & McGill (1984, *JASA* ; 1985, *Science*) ont établi la hiérarchie de précision perceptive pour l'encodage de données quantitatives, validée expérimentalement et répliquée par Stewart & Best (2010) :

| Rang | Canal visuel | Précision perceptive | Usage recommandé pour l'évidence |
|------|-------------|---------------------|----------------------------------|
| 1 | Position sur échelle commune | Très haute | **Signal primaire** : barres d'évidence alignées |
| 2 | Position sur échelles non-alignées | Haute | Comparaison inter-zones |
| 3 | Longueur | Haute (β≈1.0) | **Signal secondaire** : remplissage proportionnel |
| 4 | Direction / Angle | Moyenne | Flèches directionnelles |
| 5 | Aire | Basse (β≈0.7) | **À utiliser avec prudence** : masse visuelle |
| 6 | Volume | Très basse | Non recommandé |
| 7 | Saturation / Teinte | Très basse | Catégorisation uniquement |

**Impact critique sur P21 (Gravité Clinique) :** Le pattern actuel utilise l'aire visuelle comme encodage principal de la robustesse clinique (OM-85 = bloc 3-4× plus massif que CRL1505). La loi de Stevens (β≈0.7 pour l'aire) prédit qu'une différence réelle de 10× sera perçue comme ~5×. La littérature recommande d'utiliser la **longueur** (β≈1.0, quasi-linéaire) comme canal primaire.

**L'"illusion de la moyenne pondérée" (2021, *IEEE TVCG*) :** Dans les bubble charts, les points plus grands et plus foncés reçoivent un poids cognitif disproportionné dans l'estimation moyenne (P<.0001). Cet effet peut être exploité délibérément : si OM-85 (forte évidence) est à la fois plus grand ET plus saturé, le biais perceptif s'aligne avec la réalité scientifique.

### 3.3 Visualisation de l'incertitude

**Hullman — Hypothetical Outcome Plots (HOPs) :** Kale et al. (2019, *IEEE TVCG*) ont montré que les observateurs utilisant des HOPs (animations montrant des tirages possibles) *"inféraient correctement les tendances sous-jacentes à des seuils d'évidence plus bas"* que les utilisateurs de barres d'erreur ou d'ensembles de lignes statiques. Les HOPs exploitent le traitement d'ensemble du système visuel (~200ms pour extraire des statistiques sommaires).

**Padilla — Erreur de construal déterministe :** Les observateurs interprètent systématiquement l'information d'incertitude comme déterministe. Les frontières visuelles nettes (comme le cône d'incertitude des ouragans) forcent la pensée catégorielle sur des données continues.

**MacEachren et al. (2012, *IEEE TVCG*) — Ranking d'intuitivité pour l'encodage d'incertitude :**

| Propriété visuelle | Intuitivité | Quantifiable ? | Recommandation VEC |
|-------------------|-------------|----------------|---------------------|
| Flou (blur) | Très haute | NON (binaire seulement) | Signal certain/incertain uniquement |
| Luminance (clair/foncé) | Haute | OUI (gradué) | **Encodage gradué de la certitude** |
| Taille | Moyenne-haute | OUI (avec biais β≈0.7) | Secondaire, avec labels |
| Transparence (opacité) | Moyenne-haute | OUI (forte variance individuelle) | Possible en superposition |
| Saturation | **Basse** (contre-intuitif) | OUI | **NON recommandé** malgré les hypothèses des designers |

**Kinkeldey, MacEachren & Schiewe (2017), revue systématique :** Recommandent teinte, luminance et transparence. **Déconseillent explicitement** la saturation pour représenter l'incertitude.

### 3.4 Communication des risques : fréquences naturelles et icon arrays

**Gigerenzer — Fréquences naturelles :** Quand des conseillers VIH reçoivent des probabilités conditionnelles, ~50% produisent des inférences bayésiennes correctes (avec des erreurs quasi-toutes catastrophiques). Avec des fréquences naturelles ("10 sur 1 000"), la bonne réponse devient transparente. Confirmé par McDowell & Jacobs (2017, *Psychological Bulletin*, méta-analyse).

**Garcia-Retamero & Cokely (2017, *Human Factors*, revue systématique, 36 publications, 27 885 participants, 60 pays) :** *"Les aides visuelles transparentes améliorent robustement la compréhension des risques chez des individus divers."* Les icon arrays sont particulièrement efficaces pour les individus à faible numératie.

**Zikmund-Fisher et al. (2014, *Medical Decision Making*, N=1 504) :** Le type d'icône affecte significativement la perception du risque. Les icônes en forme de personne augmentent le risque perçu par rapport aux blocs ou ovales — un effet à considérer pour B7 (pictogramme enfant).

**Implication directe pour le VEC :** Les barres d'évidence (B3) devraient utiliser des fréquences naturelles plutôt que des catégories abstraites. Au lieu de "Niveau A" ou "Fort", écrire "18 essais" ou "5 RCTs". La littérature montre que ce format est compris par >80% des publics vs <50% pour les formats probabilistes.

### 3.5 Le gap que SciSense comble

Aucun outil existant ne fait le mapping paramétrique entre certitude de l'évidence et propriétés visuelles :

| Outil | Ce qu'il fait | Ce qu'il ne fait pas |
|-------|---------------|---------------------|
| GRADEpro | Symboles ⊕ dans tableaux | Mapping multi-canal, format narratif |
| iSoF (Cochrane) | Disclosure progressive | Extension au-delà des SoF tables |
| MAGICapp | Multi-couches pour audiences | Encodage perceptif paramétrique |
| Evidence Gap Maps | Taille de bulle + couleur | Intégration narrative, mécanismes d'action |
| BioRender / Mind the Graph | Éléments visuels biomédicaux | Aucun encodage de l'évidence |
| **VEC (SciSense)** | — | **Premier système combinant position + luminance + longueur + fréquence discrète dans une grammaire visuelle cohérente pour l'évidence** |

---

## 4. Principes de Design Validés — Mapping vers la Doc Chain

### 4.1 Patterns validés par la littérature

Chaque pattern est lié dans le graph L3 à ses sources via des links `narrative:vec:* → moment:study:*`. Le weight du lien encode la force de l'évidence (1.0 RCT, 0.8 revue systématique, 0.6 loi psychophysique, 0.4 consensus expert, 0.2 observationnel).

| Pattern VEC | Principe littérature | Source | Statut | Graph link |
|------------|---------------------|--------|--------|------------|
| P1 (flux gauche→droite) | Direction de lecture naturelle, début/fin clairs | Jambor & Bornhäuser 2024, Elsevier guidelines | ✅ Validé | `→ moment:study:jambor_2024` (w=0.4) |
| P3 (compression métaphorique) | Intégration fluide texte+visuels > exhaustivité | Jambor & Bornhäuser 2024, rule #3 | ✅ Validé | `→ moment:study:jambor_2024` (w=0.4) |
| P6 (mobile-first) | 87% des sens = vision, GA vus en TOC mobile | Lee & Yoo 2023 | ✅ Validé | `→ moment:study:lee_yoo_2023` (w=0.4) |
| P7 (cohérence chromatique) | Changement de couleur = changement de sens | Jambor & Bornhäuser 2024, rule #8 | ✅ Validé | `→ moment:study:jambor_2024` (w=0.4) |
| P21 (proportionnalité volumétrique) | Aire compresse les différences (β≈0.7) | Cleveland & McGill 1984, Stevens' law | ⚠️ **À corriger** : longueur comme canal primaire | `→ moment:study:cleveland_mcgill_1984` (w=0.6) |
| P22 (micro-ancres moléculaires) | Le texte désambiguïse les pictogrammes | Jambor & Bornhäuser 2024, rule #7 | ✅ Validé | `→ moment:study:jambor_2024` (w=0.4) |
| VN1 (pas de cytokines) | Limiter à ~7 éléments (Miller) + chunks Gestalt | Miller 1956, Jambor 2024 rule #6 | ✅ Validé | `→ moment:study:miller_1956` (w=0.6) |
| B3 (gradient d'évidence) | Longueur = canal le plus précis pour le quantitatif | Cleveland & McGill 1984 | ✅ Validé (barres de remplissage = longueur) | `→ moment:study:cleveland_mcgill_1984` (w=0.6) |
| B7 (pictogramme enfant) | Icônes-personnes augmentent le risque perçu et l'ancrage | Zikmund-Fisher et al. 2014 | ✅ Validé | `→ moment:study:zikmund_fisher_2014` (w=1.0) |
| V5 (hiérarchie preuves) | Symboles > chiffres (74% vs 14%) pour la certitude | Akl et al. 2007 | ✅ Validé | `→ moment:study:akl_2007` (w=1.0) |

### 4.2 Patterns à ajouter (issus de la littérature)

**P32 — Encodage Perceptif Hiérarchique de l'Évidence**
*Intégré dans : `03_PATTERNS.md` (Design System Biologique). Cross-ref : B3, P21, V5.*
*Graph : `narrative:vec:P32` → links vers `moment:study:cleveland_mcgill_1984`, `moment:study:maceachren_2012`*

Chaque produit est encodé sur 3 canaux simultanés, du plus au moins précis :

| Canal | Propriété visuelle | Mapping évidence | Justification |
|-------|-------------------|------------------|---------------|
| Primaire | Longueur (barre de remplissage) | Proportionnelle au nombre de RCTs | β≈1.0, Cleveland & McGill rang 3 |
| Secondaire | Luminance (clair→foncé) | Plus foncé = évidence plus forte | MacEachren 2012 : haute intuitivité, quantifiable |
| Tertiaire | Aire (masse visuelle du bloc) | Plus grand = évidence plus robuste | β≈0.7, renforce le signal mais ne le porte pas seul |

Les 3 canaux sont **redondants** (encodent la même information) pour maximiser la compréhension en scan rapide. Si le lecteur ne perçoit que l'un des trois, le message passe quand même.

**P33 — Fréquences Naturelles, Pas de Catégories Abstraites**
*Intégré dans : `03_PATTERNS.md` (Design System Biologique). Cross-ref : V3, B3, content.yaml.*
*Graph : `narrative:vec:P33` → links vers `moment:study:gigerenzer_2003`, `moment:study:mcdowell_jacobs_2017`*

Les labels d'évidence utilisent des fréquences naturelles :
- OM-85 : "18 essais cliniques"
- PMBL : "5 essais cliniques"
- MV130 : "1 essai clinique"
- CRL1505 : "Études précliniques"

Pas de : "Niveau A", "Fort", "Modéré". La littérature montre que les fréquences naturelles améliorent la compréhension de 50%→80%+ chez les cliniciens (Gigerenzer, McDowell & Jacobs 2017).

Contrainte V3 (≤30 mots) : ces labels consomment ~12 mots. Budget restant : 18 mots pour les autres labels du GA.

**P34 — Encodage de l'Incertitude par Luminance, Pas par Saturation**
*Intégré dans : `03_PATTERNS.md` (Design System Biologique). Cross-ref : P7, P32, palette.yaml.*
*Graph : `narrative:vec:P34` → links vers `moment:study:maceachren_2012`, `moment:study:kinkeldey_2017`*

Contre-intuitivement, la saturation de couleur n'est **pas** perçue comme un marqueur d'incertitude par les non-spécialistes (MacEachren 2012, classée en bas d'intuitivité ; Kinkeldey 2017, explicitement déconseillée). La luminance (clair/foncé) est le canal recommandé.

Application : les blocs d'évidence CRL1505 (préclinique) devraient être visuellement plus clairs (pas juste plus petits) que les blocs OM-85. La teinte reste constante (#059669 pour CRL1505), mais à luminance réduite (ex: opacity 60%).

### 4.3 Validation à ajouter

**V14 — Accessibilité Daltoniens**
*Intégré dans : `06_VALIDATION.md` (Invariants PIPELINE). Cross-ref : P7, B5, H1.*
*Graph : `narrative:vec:V14` → links vers `moment:study:jambor_2024` (rule #8), `thing:standard:wcag_2_1`*

~8% des hommes sont daltoniens (deutéranopie et protanopie principalement). La palette actuelle teal (#0D9488) / vert (#059669) est potentiellement confuse pour cette population.

Test : passer chaque rendu dans un simulateur Coblis ou sim-daltonism. Les 4 couleurs produits doivent rester distinguables sous les 3 types de daltonisme (deutéranopie, protanopie, tritanopie).

Automation : intégrable dans validate_ga.py (conversion de l'espace couleur et mesure de la distance perceptive CIEDE2000 entre les 4 paires sous chaque simulation).

**V15 — Absence de Spin Visuel**
*Intégré dans : `06_VALIDATION.md` (Invariants PIPELINE). Cross-ref : P3, P21, R2, H2.*
*Graph : `narrative:vec:V15` → links vers `moment:study:vorland_2024`*

Vorland et al. (2024) montrent que les visual abstracts ont un taux élevé de spin. Le VEC doit vérifier que la représentation visuelle n'amplifie pas les résultats au-delà de ce que le manuscrit supporte.

Test spécifique : la masse visuelle relative des 4 produits correspond-elle à la hiérarchie d'évidence du manuscrit ? Si le bloc MV130 (1 RCT) paraît visuellement aussi imposant que le bloc PMBL (5 RCTs), c'est du spin.

### 4.4 Protocole de validation par compréhension

**GLANCE — Test "Premier Regard" (Naive Comprehension Test)**
*Intégré dans : `08_HEALTH.md` comme H9. Cross-ref : PH1, B1, B3, B4, V5.*
*Graph : `narrative:vec:GLANCE` → links vers `moment:study:jambor_2024` (rule #10), `moment:study:bredbenner_simon_2019`, `moment:study:garcia_retamero_cokely_2017`*

La littérature (Jambor & Bornhäuser 2024, rule #10 ; feedback structuré) recommande un protocole de test formel :

**Sujets :** 3-5 pédiatres qui n'ont PAS lu le manuscrit.

**Protocole :**
1. Exposition au GA pendant 5 secondes (simule le scan mobile, PH1).
2. Retrait du GA.
3. Trois questions :
   - *"Que voyez-vous ?"* (rappel libre — valide B1, B4)
   - *"Quel produit est le mieux documenté ?"* (valide B3, V5, P21)
   - *"Feriez-vous quelque chose différemment dans votre pratique ?"* (valide l'impact décisionnel)

**Critères de succès :**
- ≥3/5 pédiatres identifient correctement le sujet (immunomodulateurs + RTIs)
- ≥4/5 identifient OM-85 comme le mieux documenté
- ≥2/5 expriment un changement de perception ou d'intention

**Ce que ça prouve :** Ce protocole mesure la *compréhension*, pas l'engagement. C'est ce qui différencie SciSense du champ existant. Aucune étude GA n'a jamais mesuré la compréhension dans un format aussi contraint (5 secondes, audience clinique naïve).

---

## 5. Le Gap que SciSense Comble — Positionnement

### 5.1 Le problème (documenté)

La littérature converge sur un diagnostic en 3 points :

1. Les graphical abstracts captent l'attention (×2-8 engagement) mais ne transfèrent pas la compréhension.
2. Le seul encodage visuel de certitude testé expérimentalement (GRADE ⊕) utilise un canal unique dans un format unique.
3. Aucun outil n'existe pour traduire systématiquement le niveau de certitude scientifique en propriétés visuelles multi-canaux.

### 5.2 La solution SciSense

Le Visual Evidence Compiler (VEC) est le premier système qui :

- **Encode l'évidence sur 3 canaux perceptifs simultanés** (longueur, luminance, aire) au lieu d'un seul (remplissage GRADE), suivant la hiérarchie validée de Cleveland & McGill.
- **Utilise des fréquences naturelles** ("18 essais") au lieu de catégories abstraites ("Niveau A"), conformément aux recommandations de Gigerenzer sur la transparence des risques.
- **Intègre l'encodage dans un format narratif visuel** (flux gauche→droite, compression métaphorique) au lieu de le confiner à un tableau.
- **Paramétrise le design** (YAML-driven, générateurs) pour que chaque itération soit traçable à ses justifications perceptives et scientifiques.
- **Valide par compréhension directe** (protocole GLANCE) au lieu de se contenter de métriques d'engagement.

### 5.3 Ce que ça signifie

Si SciSense démontre qu'un GA produit par le VEC améliore la *compréhension clinique* (pas juste l'engagement), c'est une contribution originale au champ. Aucune étude existante n'a fait cette démonstration pour un graphical abstract. Le protocole GLANCE, aussi modeste soit-il (3-5 pédiatres), produirait les premières données de compréhension clinique pour un GA paramétrique.

---

## 6. Traçabilité par le Graph — Architecture

### 6.1 Principe

Chaque item de la doc chain (P, B, V, VN) est un node `narrative:vec:*` dans le graph L3. Chaque étude est un node `moment:study:*`. Les liens entre les deux portent la traçabilité.

```
[narrative:vec:P21]  ──link(weight=0.6)──►  [moment:study:cleveland_mcgill_1984]
    "Gravité clinique"                        assertion: "β≈0.7 pour l'aire"
                                              force: "loi psychophysique"

[narrative:vec:B7]   ──link(weight=1.0)──►  [moment:study:zikmund_fisher_2014]
    "Pictogramme enfant"                      assertion: "icônes-personnes ↑ risque perçu"
                                              force: "RCT, N=1504"

[narrative:vec:V5]   ──link(weight=1.0)──►  [moment:study:akl_2007]
    "Hiérarchie preuves"                      assertion: "symboles 74% vs chiffres 14%"
                                              force: "RCT, N=84"
```

### 6.2 Taxonomie des forces (weight sur le lien)

| Weight | Force | Définition | Exemples |
|--------|-------|-----------|----------|
| 1.0 | RCT | Étude contrôlée randomisée mesurant directement l'effet | Akl 2007, Ibrahim 2017, Bredbenner 2019 |
| 0.8 | Revue systématique | Synthèse avec méthodologie explicite | Garcia-Retamero & Cokely 2017 (27 885 participants) |
| 0.6 | Loi psychophysique | Principe perceptif validé et répliqué | Cleveland & McGill 1984, Stevens' law, Miller 1956 |
| 0.4 | Consensus expert | Recommandation basée sur l'expérience | Jambor & Bornhäuser 2024, Elsevier guidelines |
| 0.2 | Observationnel | Étude rétrospective ou corrélative | Bennett & Slattery 2023, Pferschy-Wenzig 2016 |

### 6.3 Audit de couverture

Items avec source RCT (w=1.0) : V5, B7
Items avec source psychophysique (w=0.6) : P21, B3, VN1
Items avec consensus expert uniquement (w=0.4) : P1, P3, P6, P7, P22
Items non sourcés (w=0) : **à identifier par requête graph** — tout node `narrative:vec:*` sans lien sortant vers `moment:study:*`

Les items non sourcés deviennent les cibles prioritaires de la **Vague 2** de recherche (Axe 1 : perception cognitive, Axe 5 : métriques de validation).

### 6.4 Avantage graph vs matrice centralisée

La traçabilité vit dans le graph, pas dans un fichier séparé :
- **Requêtable** : `graph_query "P21" expand_depth=1` → montre ses sources directement
- **Distribué** : pas de fichier unique qui se désynchronise avec la doc chain
- **Évolutif** : ajouter une source = ajouter un lien, pas éditer un tableau
- **Auditable** : les nodes `narrative:vec:*` sans lien vers `moment:study:*` = trous visibles

---

## 7. Bibliographie Structurée

### Efficacité des Visual Abstracts (Axe A)

*Chaque entrée correspond à un node `moment:study:*` dans le graph L3.*

- Ibrahim AM et al. (2017). Visual abstracts to disseminate research on social media. *Ann Surg* 266(6):e46-e48. — *Crossover prospectif, N=44, ×7.7 impressions* `→ moment:study:ibrahim_2017`
- Oska S, Lerma E, Topf J. (2020). A picture is worth a thousand views. *JMIR* 22(12):e22327. — *Triple crossover, N=40, ×5 engagements* `→ moment:study:oska_2020`
- Trueger NS et al. (2023). RCT visual abstract display and social media–driven website traffic. *JAMA*. — *Crossover simultané, N=205 RCTs, 12 journaux JAMA* `→ moment:study:trueger_2023`
- Chapman SJ et al. (2019). Randomized controlled trial of plain English and visual abstracts. *BJS* 106(12):1611-1616. — *RCT 3 bras, N=41* `→ moment:study:chapman_2019`
- Hoffberg AS et al. (2020). Beyond journals — visual abstracts promote wider dissemination. *Front Res Metr Anal* 5:564193. — *Crossover, N=50, P<.001* `→ moment:study:hoffberg_2020`
- Pferschy-Wenzig EM et al. (2016). Does a graphical abstract bring more visibility? *Molecules* 21(9):1247. — *Rétrospectif, N=1326, effet négatif* `→ moment:study:pferschy_wenzig_2016`
- Aggarwal R. (2021). Visual abstracts do not increase impact scores. *Health Info Libr J*. — *Rétrospectif, N=307, P>.37* `→ moment:study:aggarwal_2021`
- Bredbenner K, Simon SM. (2019). Video abstracts and plain language summaries are more effective than graphical abstracts. *PLOS ONE* 14(11):e0224697. — *RCT, N=538, GA = 3ème/4 en compréhension* `→ moment:study:bredbenner_simon_2019`
- Bennett H, Slattery F. (2023). Graphical abstracts: Altmetric scores but not citations. *Scientometrics* 128:3793-3804. — *N=562, IRR Altmetric 1.89 P=.003, citations IRR 0.97 P=.829* `→ moment:study:bennett_slattery_2023`
- Zong Q, Huang Z, Deng Z. (2023). Effect of GAs on usage and citations. *Learned Publishing* 36(2):266-274. `→ moment:study:zong_2023`
- Vorland CJ et al. (2024). Visual abstracts of RCTs: inadequate reporting and high spin. *J Clin Epidemiol*. `→ moment:study:vorland_2024`
- Egan M et al. (2021). COVID-19 infographic effectiveness. *BMC Public Health*. — *RCT, N=4099, rappel P<.001* `→ moment:study:egan_2021`

### Sémiotique de l'Évidence (Axe B)

- Akl EA et al. (2007). Symbols superior to numbers for strength of recommendations. *J Clin Epidemiol*. — *RCT, N=84, 74% vs 14% P<.001* `→ moment:study:akl_2007`
- Schünemann HJ et al. (2003). Letters, numbers, symbols and words: communicating grades. *CMAJ* 169(7):677-680. — *Fondation du système GRADE visuel* `→ moment:study:schunemann_2003`
- Rosenbaum SE et al. (2010). Summary-of-findings tables improved understanding. *J Clin Epidemiol*. — *RCT, N=33, 93% vs 44% P=.003* `→ moment:study:rosenbaum_2010`
- Cleveland WS, McGill R. (1984). Graphical perception: theory, experimentation. *JASA* 79:531-554. — *Hiérarchie perceptive fondatrice* `→ moment:study:cleveland_mcgill_1984`
- Cleveland WS, McGill R. (1985). Graphical perception and graphical methods. *Science* 229:828-833. `→ moment:study:cleveland_mcgill_1985`
- MacEachren AM et al. (2012). Visual semiotics & uncertainty visualization. *IEEE TVCG*. — *Ranking d'intuitivité pour l'incertitude* `→ moment:study:maceachren_2012`
- Kinkeldey C, MacEachren AM, Schiewe J. (2017). How to assess visual communication of uncertainty? Systematic review. — *Recommandent luminance, déconseillent saturation* `→ moment:study:kinkeldey_2017`
- Kale A et al. (2019). Hypothetical outcome plots. *IEEE TVCG*. — *HOPs > barres d'erreur pour inférence* `→ moment:study:kale_2019`
- Padilla L et al. (2018). Uncertainty visualization. *Cogn Res: Princ Implic*. — *Erreur de construal déterministe* `→ moment:study:padilla_2018`
- Garcia-Retamero R, Cokely ET. (2017). Designing visual aids that promote risk literacy. *Human Factors*. — *Revue systématique, 36 pub, 27 885 participants* `→ moment:study:garcia_retamero_cokely_2017`
- Gigerenzer G. (2003). Reckoning with risk. — *Fréquences naturelles* `→ moment:study:gigerenzer_2003`
- McDowell M, Jacobs P. (2017). Meta-analysis of the effect of natural frequencies on Bayesian reasoning. *Psychological Bulletin*. `→ moment:study:mcdowell_jacobs_2017`
- Zikmund-Fisher BJ et al. (2014). Blocks, ovals, or people? Icon type affects risk perceptions. *Med Decis Making*. — *N=1504* `→ moment:study:zikmund_fisher_2014`
- Jambor HK, Bornhäuser M. (2024). Ten simple rules for designing graphical abstracts. *PLOS Comput Biol* 20(2):e1011789. — *10 règles validées par la pratique* `→ moment:study:jambor_2024`
- Lee J, Yoo JJ. (2023). Current state of graphical abstracts. *Science Editing*. — *Vision = 87% des sens* `→ moment:study:lee_yoo_2023`
- Miller GA. (1956). The magical number seven, plus or minus two. *Psychological Review* 63(2):81-97. `→ moment:study:miller_1956`

---

*Document généré le 2026-03-24, mis à jour le 2026-03-24 (renumérotation P32-P34, ajout V14/V15/GLANCE, section traçabilité graph)*
*SciSense × Mind Protocol — Visual Evidence Compiler, Vague 1*
*Prochaine étape : Vague 2 (Axe 1 : perception cognitive + Axe 5 : métriques de validation)*