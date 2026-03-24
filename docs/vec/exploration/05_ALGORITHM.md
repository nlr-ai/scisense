# ALGORITHM — vec/exploration

**Module:** vec/exploration — Agents autonomes paralleles

---

## AE1: Cycle d'exploration complet

```
ENTREE: Declencheur identifie (EP8) + contexte courant (wireframe, configs, audit)

1. DIAGNOSTIC
   - Formuler le probleme en une phrase
   - Identifier les dimensions en jeu (>3 = exploration justifiee)
   - Si <=3 dimensions → resoudre sequentiellement, pas d'exploration
   - Si blocage >5 minutes sur une approche → forcer l'exploration

2. SELECTION DES ANGLES
   - Choisir 1 a 3 angles dans la taxonomie EP2
   - Chaque angle doit couvrir une dimension distincte du probleme
   - Si le probleme a plus de 3 dimensions, prioriser les 3 plus critiques
     (criticite = impact sur precision scientifique > faisabilite visuelle > cout)

3. DECLARATION DU MODE
   - Foreground [FG]: si le resultat conditionne la prochaine action
   - Background [BG]: si enrichissement non-bloquant
   - Documenter la declaration dans les notes de session

4. CONSTRUCTION DES PROMPTS (un par agent)
   Pour chaque angle:
   a. SCOPE: decrire l'artefact examine (version, fichier, etat courant)
   b. ANGLE: nommer la perspective et sa question centrale
   c. DELIVERABLE: specifier la sortie attendue (tableau de failles, propositions, etc.)
   d. CONTRAINTES: specifier ce que l'agent ne fait PAS
      - Ne code jamais
      - Ne modifie aucun fichier
      - Ne sort pas de son angle
      - Ne produit pas de prose libre
   e. FORMAT DE RETOUR: structure exacte (colonnes du tableau, sections du rapport)

5. LANCEMENT
   - /subcall pour chaque agent avec son prompt
   - Mode foreground: attendre la convergence des 3 agents
   - Mode background: continuer le flux principal

6. CONVERGENCE (foreground uniquement)
   - Attendre que les 3 agents aient produit leur deliverable
   - Si un agent ne converge pas → timeout apres un delai raisonnable,
     noter le timeout et integrer avec les agents restants

7. INTEGRATION (AE2)

8. CLOTURE
   - Documenter le bilan du cycle dans les notes de session
   - Mettre a jour le SYNC du module concerne
   - Verifier la Guarantee Loop: aucun probleme identifie par >1 agent
     reste sans reponse

SORTIE: Liste de findings actionnables + conflits resolus + questions escaladees
```

---

## AE2: Protocole d'integration (merge)

```
ENTREE: Deliverables des N agents (1 <= N <= 3)

1. EXTRACTION
   Pour chaque agent:
   - Lire le deliverable structure
   - Extraire les findings qui passent le test actionnable:
     "Est-ce que ca change quelque chose dans le code, le config, ou la doc?"
   - Limiter a 3-5 findings par agent (au-dela = bruit probable)
   - Ecarter:
     * Reformulations du brief
     * Observations generales sans correction proposee
     * Compliments ou validations ("le design est bon dans l'ensemble")

2. DEDUPLICATION
   - Fusionner les findings identiques ou equivalents entre agents
   - Un finding deduplique conserve la formulation la plus precise
   - Compter le nombre d'agents qui l'ont identifie (>1 = signal fort)

3. DETECTION DE CONFLITS
   - Scanner les findings pour les contradictions:
     * Agent A dit "augmenter X" et Agent B dit "diminuer X"
     * Agent A dit "ajouter element Y" et Agent C dit "supprimer element Y"
   - Marquer chaque conflit detecte

4. RESOLUTION DE CONFLITS (AE3)

5. PRIORISATION
   Classer les findings par:
   a. Nombre d'agents concordants (>1 = haute priorite)
   b. Dimension impactee (precision scientifique > faisabilite visuelle > cout)
   c. Severite estimee (bloquant > degradant > amelioration)

6. LISTE FINALE
   - Produire une liste ordonnee de corrections/actions
   - Chaque entree: Finding | Source(s) | Priorite | Action proposee

SORTIE: Liste d'actions priorisees + trace d'integration (findings retenus, ecartes, conflits)
```

---

## AE3: Resolution de conflits

```
ENTREE: Conflit detecte entre 2+ agents

1. IDENTIFIER LA NATURE DU CONFLIT
   a. Conflit scientifique: deux interpretations d'un mecanisme biologique
      → Escalade a Aurore (I1). Les sub-agents ne tranchent pas.
        Question formulee: precise, binaire, avec contexte minimal.
   b. Conflit visuel: deux approches de design incompatibles
      → Appliquer la hierarchie EP7:
        Precision scientifique > Faisabilite visuelle > Cout d'implementation
   c. Conflit de priorite: deux agents priorisent des corrections differentes
      → Le finding identifie par plus d'agents prime.
        A egalite, la dimension la plus critique (precision scientifique) prime.

2. DOCUMENTER LA RESOLUTION
   - Les deux positions
   - La regle de hierarchie appliquee (ou l'escalade)
   - La decision finale
   - La justification en une phrase

3. INTEGRER
   - Le finding resolu rejoint la liste finale (AE2 step 5)
   - Le finding rejete est note avec sa justification dans la trace

SORTIE: Decision + trace
```

---

## AE4: Prompt templates par angle

Templates concrets pour les 6 angles de la taxonomie EP2. Chaque template est une base — a adapter au contexte specifique de la mission.

### Angle: Immunologie

```
## SCOPE
Wireframe GA [version] pour la mission [mission]. Fichiers: [liste].

## ANGLE
Immunologie — validation des mecanismes d'action representes visuellement.

## DELIVERABLE
Tableau des failles immunologiques:
| Faille | Element concerne | Probleme | Correction | Reference (paper/manual) |

## CONTRAINTES
- Ne code pas, ne modifie aucun fichier
- Ne juge pas l'esthetique — concentre-toi sur la precision biologique
- Chaque faille doit citer une reference (paper ou consensus immunologique)

## FORMAT DE RETOUR
Tableau markdown strict. Max 5 failles. Si zero faille, dire explicitement "PASS — aucune faille immunologique detectee".
```

### Angle: Communication visuelle

```
## SCOPE
Wireframe GA [version] — PNG delivery [resolution]. Fichiers: [liste].

## ANGLE
Communication visuelle — lisibilite, impact cognitif, flux de lecture.

## DELIVERABLE
Tableau des problemes visuels:
| Probleme | Zone | Impact cognitif | Correction proposee |

## CONTRAINTES
- Ne juge pas la science — concentre-toi sur ce que le lecteur VOIT
- Teste mentalement le flux de lecture L→R (P1) et le scan vertical (P30)
- Evalue l'espace negatif (P26), la hierarchie typo (P28), le poids visuel (P31)

## FORMAT DE RETOUR
Tableau markdown strict. Max 5 problemes. Inclure une evaluation du "aha moment" en <3 secondes (oui/non + justification).
```

### Angle: Matrice produit-mecanisme

```
## SCOPE
Wireframe GA [version] — [N] produits, [M] bandes/zones. Fichiers: [liste].

## ANGLE
Matrice produit-mecanisme — couverture, coherence, et distinction des produits.

## DELIVERABLE
Matrice de couverture:
| Produit | Couleur | Zone/Bande | Mecanisme represente | Visible? | Distinct? |

+ Liste des gaps (produit present mais mecanisme absent, ou mecanisme present mais non attribue).

## CONTRAINTES
- Ne code pas. Analyse uniquement la representation visuelle des produits.
- Verifie que chaque produit a sa couleur constante (P7), sa position topologique (P19), et sa masse visuelle proportionnelle a son evidence (P21).

## FORMAT DE RETOUR
Matrice markdown + liste de gaps. Si couverture complete, dire "PASS — matrice complete".
```

### Angle: Lisibilite mobile

```
## SCOPE
PNG delivery [resolution] du GA [version]. A evaluer a 50% zoom (= [resolution_50%]).

## ANGLE
Lisibilite mobile — test de lecture a taille reduite, simulation ecran telephone.

## DELIVERABLE
Tableau des labels illisibles:
| Label | Niveau typo (1/2/3) | Taille actuelle | Lisible a 50%? | Action |

## CONTRAINTES
- Le test est a 50% du format delivery, pas du format full.
- Un label de Niveau 3 (P28) illisible a 50% doit etre supprime, pas reduit.
- Un label de Niveau 1 ou 2 illisible a 50% est un FAIL bloquant.

## FORMAT DE RETOUR
Tableau markdown. Verdict global: PASS / FAIL (+ nombre de labels en echec).
```

### Angle: Benchmarking litterature

```
## SCOPE
GA [version] pour la mission [mission], destine a [journal] (facteur d'impact: [IF]).

## ANGLE
Benchmarking — comparaison avec les GA publies dans le meme journal ou domaine.

## DELIVERABLE
Analyse comparative:
| Critere | Notre GA | Benchmark (top 3 GA du journal) | Gap | Recommendation |

## CONTRAINTES
- Compare sur des criteres objectifs: densite d'information, nombre de couleurs, ratio texte/image, lisibilite, originalite du format.
- Ne juge pas la science (elle est mission-specifique).
- Cite les GA de reference si possible (DOI ou description).

## FORMAT DE RETOUR
Tableau markdown + verdict: "Au niveau" / "En dessous" / "Au-dessus" + justification en 2 phrases.
```

### Angle: Conformite editoriale

```
## SCOPE
GA [version] — SVG + PNG delivery. Fichiers: [liste]. Journal cible: [journal].

## ANGLE
Conformite editoriale — regles du journal, invariants V1-V7, VN1-VN4.

## DELIVERABLE
Checklist de conformite:
| Regle | Statut (PASS/FAIL) | Detail |

## CONTRAINTES
- Verifie chaque invariant explicitement (V1: ratio, V2: zero titre, V3: <=30 mots, V4: non-redondance, V5: hierarchie preuves, V6: droits, V7: lisibilite 50%).
- Verifie chaque negative (VN1: zero cytokines, VN2: zero schema fabrication, VN3: zero brouillon, VN4: zero pixel IA).

## FORMAT DE RETOUR
Checklist markdown. Verdict global: PASS (tout vert) / FAIL (nombre de regles en echec).
```
