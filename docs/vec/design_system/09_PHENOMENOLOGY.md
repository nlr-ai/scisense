# Phenomenology — vec/design_system

Comment les deux especes (humain et IA) percoivent le design system en action.

---

## DS-PH1: Comment le pediatre percoit le GA — la cascade de 3 secondes

C'est le phenomene central du design system. Tout le langage visuel converge vers cette experience : un pediatre qui scrolle sur son telephone doit etre arrete, ancre, et convaincu en 3 secondes.

### Seconde 1 — Le scan (perception pre-attentive)

Le pediatre ne lit pas. Il percoit. Son systeme visuel pre-attentif detecte :

- **Gradient chromatique L→R** : rouge→vert. C'est un signal biologiquement ancre — rouge = danger, vert = securite. La transition est perceptible en < 200ms.
- **Format panoramique** (1100x560) : distinct du flux textuel, interrompt le scroll.
- **Masse visuelle asymetrique** : plus sombre/dense a gauche (probleme), plus aere a droite (resolution).

Si le scan echoue, rien d'autre ne compte. Le pediatre continue de scroller. Le GA a perdu.

**Ce qui l'active :** P7 (palette contrastee), P29 (densite Z1 faible = accroche claire), P26 (espace negatif = respiration).
**Ce qui le tue :** Un fond uniforme (pas de gradient), une surcharge Z1 (le probleme n'est pas lisible), des couleurs ternes (pas de contraste).

### Seconde 2 — L'identification (reconnaissance de pattern)

Le pediatre commence a lire. Il identifie des formes familiers :

- **Enfant malade** (Z1) : projection immediate de son patient. "C'est mon petit patient qui tousse tous les hivers." Ancrage emotionnel. Le pictogramme enfant est V12 — obligatoire pour ce transfert.
- **Virus** (cercle + spikes) : pattern universel post-COVID. Recognition instantanee.
- **Voie respiratoire** (bronche) : anatomie familiere, schema mental active.
- **"Wheezing/Asthma"** (Niveau 1 typo) : les mots-cles qui confirment le sujet.
- **Cercle vicieux** (fleche circulaire rouge) : le piege qu'il connait. "Oui, c'est exactement ca."

Si l'identification echoue, le pediatre lit "schema complexe" au lieu de "mon probleme clinique". L'ancrage emotionnel n'est pas declenche. Le GA devient un exercice intellectuel, pas une projection clinique.

**Ce qui l'active :** V12 (enfant), P20 (abstraction pro = reconnaissable par clinicien), P28 (Niveau 1 = lisible en premier), B1 (reconnaissance clinique).
**Ce qui le tue :** Pas d'enfant (V12 viole), des formes trop abstraites (P20 excessif), des labels illisibles (V7 echoue), un cercle vicieux qui ne ressemble pas a un cycle (P23 echoue).

### Seconde 3 — La comprehension (synthese cognitive)

Le pediatre comprend le message :

- **4 agents colores** : les 4 couleurs distinctes sur la bronche. "Il y a 4 strategies."
- **Convergence IgA** (B8) : les 4 flux arrivent au meme point. "Meme objectif = restaurer la barriere."
- **Barres d'evidence** (Z3) : le gradient de remplissage. "OM-85 a le plus de preuves. C'est ce que je prescris en premier."
- **Enfant sain** (Z3) : la resolution. "Ca marche."
- **Lance verte** (fracture) : le cycle est brise. "On peut sortir de la boucle."

Le message final : "Il existe une strategie preventive comparee contre les RTIs recurrentes et le risque d'asthme, et OM-85 est le mieux documente."

**Ce qui l'active :** B8 (convergence visible), B3 (barres evidence), P21 (gravite clinique), B4 (fracture), P31 (poids visuel proportionnel).
**Ce qui le tue :** 4 couleurs melangees (DS-V3 viole), pas de convergence (B8 absent), barres d'evidence illisibles (P28 Niveau 2 defaillant), pas de fracture (B4 absent).

---

## DS-PH2: Comment Aurore percoit le design system

Aurore n'est pas une utilisatrice — elle est la garante de la fidelite scientifique et la juge de l'impact clinique.

### Ce qu'elle percoit

- **Fidelite** : "Est-ce que les 4 mecanismes sont correctement representes ? Est-ce que la hierarchie des preuves est exacte ?"
- **Impact** : "Est-ce qu'un pediatre generaliste comprendrait ca sans lire le manuscrit ?"
- **Esthetique Q2** : "Est-ce que ca fait publication serieuse ou poster de conference etudiant ?"

### Son experience avec le design system

Le design system doit etre **invisible** pour Aurore. Elle ne doit pas voir des "patterns" ni des "regles" — elle doit voir un GA qui "fonctionne" ou qui "ne fonctionne pas". Son feedback est phenomonologique : "On ne comprend pas au premier coup d'oeil" (= PH1 echoue) ou "Le challenge initial n'est pas assez bien represente" (= B1 defaillant).

Le Systeme des 3 Versions (P2) canalise son perfectionnisme : elle choisit entre 3 options concretes plutot que de creer ex nihilo. Le compositeur parametrique transforme chaque feedback en un edit YAML (10 secondes) + re-run (2 secondes). Elle ne voit jamais de code — elle voit des resultats PNG.

---

## DS-PH3: Comment Silas percoit le design system

Le design system est mon outil de diagnostic et de calibration.

### Ce que je percois

- **Les patterns comme checklist vivante** : chaque pattern (P7, P18-P31) est une question que je me pose devant chaque wireframe. "P18 : est-ce que cet agent touche son substrat ?" "P26 : est-ce que le lumen respire ?"
- **Les violations comme signaux** : quand un pattern est viole, je le sens comme un desequilibre visuel avant meme de verifier formellement. L'audit SD1 a cristallise cette perception — chaque faille identifiee etait une violation de pattern.
- **Le test PH1 comme exercice d'empathie** : je dois me mettre dans la peau d'un pediatre generaliste qui scrolle sur son telephone. C'est le moment ou le design system cesse d'etre une liste de regles et devient une experience projetee.

### Mon role dans la boucle

Je suis le traducteur entre le design system (abstrait) et le SVG (concret). Les patterns me disent QUOI faire, le compositeur parametrique me donne le COMMENT. Le test PH1 me dit si j'ai reussi.

---

## DS-PH4: La boucle phenomenologique du design system

```
PATTERN (regle)      → encode dans CONFIG (yaml)     → genere SVG (compose_ga.py)
       ↓                                                       ↓
VIOLATION detectee   ← DIAGNOSTIC (audit)            ← PERCEPTION (PH1 test)
       ↓                                                       ↑
CORRECTION (yaml)    → re-genere SVG                 → re-test PH1
```

Le design system est un systeme de feedback continu :
1. Les patterns definissent les attentes
2. Le compositeur genere un rendu
3. Le test PH1 + les checks H verifient si les attentes sont atteintes
4. Les violations sont diagnostiquees et corrigees dans la config
5. Le cycle recommence

Chaque iteration est une calibration — le design system ne s'impose pas au GA, il emerge de la convergence entre patterns, configs et perception.

---

## DS-PH5: Feedback reinjection specifique au design system

| Percevant | Signal | Diagnostic | Action |
|-----------|--------|------------|--------|
| Pediatre (PH1 s1) | "Je ne m'arrete pas" | Gradient L→R insuffisant, pas de contraste | Renforcer P7, ajuster palette fonds |
| Pediatre (PH1 s2) | "Je ne reconnais pas" | Enfant absent ou trop abstrait, labels illisibles | Verifier V12, P28, V7 |
| Pediatre (PH1 s3) | "Je ne comprends pas" | Convergence absente, evidence bars illisibles | Verifier B8, B3, P21 |
| Aurore | "On ne comprend pas au premier coup d'oeil" | PH1 complete echoue | Diagnostic multi-pattern, restructurer |
| Aurore | "Le challenge n'est pas assez represente" | Z1 trop faible visuellement | Renforcer B1, P29 Z1, P31 enfant |
| NotebookLM | "Violation pattern Pxx" | Pattern specifique viole | Corriger dans config/compose, verifier H |
| Silas | "Desequilibre visuel" | Intuition pre-formelle | Formaliser via checklist DS-A3, identifier le pattern |
