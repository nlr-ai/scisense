# Health — vec/audit

3 health checkers. H2 et H6 mapping 1:1 avec les 2 results. H9 (Premier Regard) valide la comprehension clinique directe.

```
R-AUD1 (science validee Aurore)   <- H2 (sign-off explicite)   <- S2 (question directe)
R-AUD2 (audit NLM integre)       <- H6 (cycle audit)          <- S6a-S6d (4 sense signals)
comprehension clinique directe    <- H9 (Premier Regard)       <- S9a-S9c (3 sense signals)
```

---

## H2: Validation scientifique Aurore -> validates R-AUD1

Aurore confirme explicitement que le GA encode correctement les 4 messages cles, la hierarchie des preuves (V5), et que les metaphores (P3) ne trahissent pas la science.

### Sense signal

| ID | Signal | Method |
|----|--------|--------|
| S2 | Sign-off explicite d'Aurore | Question directe avec options concretes (PA3). Presentation du PNG delivery + 2-3 points de decision. Reponse attendue : OUI ou corrections specifiques. |

**Checker:** Reponse explicite d'Aurore. Pas d'interpretation du silence. Pas de lecture d'emojis comme validation. Si corrections : retour a la compilation (A7), re-audit (A-AUD1), re-presentation (A-AUD2). La boucle tourne jusqu'au OUI.

**Carrier:** Aurore.

**Gate:** Sans H2 PASS, le GA ne progresse pas vers la soumission (H4/R4). C'est le gate le plus dur du processus — il ne depend d'aucun script, d'aucune automatisation. Il depend d'une humaine qui a un travail, des enfants doudous, et des journees chargees.

**Comment ne PAS bloquer le gate :**
- Presenter des options, pas des questions ouvertes (PA3)
- Inclure les findings NLM pertinents pour renforcer la confiance (B-AUD4)
- Un message clair, scannable en 30 secondes, avec les points de decision en gras
- Si pas de reponse 48h : relance legere UNE fois

**Status:** Loop ouverte — GA pas encore presente a Aurore.

---

## H6: Audit NotebookLM cycle -> validates R-AUD2

Chaque cycle d'audit NotebookLM produit un rapport exploitable et les corrections sont integrees.

### Sense signals

| ID | Signal | Checks | Automation |
|----|--------|--------|------------|
| S6a | Export S0N/ cree | Repertoire S0N/ contient >= 17 fichiers, pas de versions bannies | Auto — file count + filename check |
| S6b | System prompt V2.4 charge | `config/notebooklm_system_prompt.md` present dans S0N/ et version = 2.4 | Auto — file exists + version grep |
| S6c | Reponse audit recue | NotebookLM a retourne au moins un output (report, slide deck, podcast, ou infographie) | Manuel — verification Silas |
| S6d | Problemes traites | Tous les problemes identifies soit corriges (commit), soit documentes (gap connu), soit escalades (Aurore). Aucune ligne "resolution" vide dans la table de findings SYNC. | Semi-auto — checklist SYNC |

**Checker:** S6a et S6b sont automatisables dans `export_notebooklm.py` (validation post-export). S6c et S6d necessitent le jugement de Silas.

**Carrier:** Silas + NotebookLM.

**Interaction H6 → H2 :** Les findings de H6 alimentent la presentation H2. NotebookLM identifie les problemes, Silas les corrige ou les escalade, Aurore tranche ce qui reste. Le cycle ne s'arrete pas apres un seul passage — il boucle tant que des problemes non-resolus subsistent.

**Hard Reset (PA5) :** Si les sense signals S6c/S6d deviennent de plus en plus bruites (findings contradictoires, references obsoletes), c'est un signe de pollution contextuelle. Declencher A-AUD3 (Hard Reset) avant de continuer.

**Status:** Loop ouverte — processus defini, premiere execution a lancer.

---

## H9: Comprehension clinique directe (Premier Regard) -> validates comprehension, not just engagement

Le fossile engagement-comprehension (VEC Literature Analysis, section 2.2) montre que les GA captent l'attention mais ne transferent pas la comprehension. Ce health checker valide la comprehension directe.

### Protocole "Premier Regard" (Naive Comprehension Test)

**Sujets:** 3-5 pediatres qui n'ont PAS lu le manuscrit.

**Protocole:**
1. Exposition au GA pendant 5 secondes (simule le scan mobile, PH1).
2. Retrait du GA.
3. Trois questions :
   - "Que voyez-vous ?" (valide B1, B4)
   - "Quel produit est le mieux documente ?" (valide B3, V5, P21)
   - "Feriez-vous quelque chose differemment dans votre pratique ?" (valide l'impact decisionnel)

### Sense signals

| ID | Signal | Critere de succes |
|----|--------|-------------------|
| S9a | Test conduit avec >= 3 pediatres naifs | Minimum 3 sujets recrutes et testes |
| S9b | Identification correcte du sujet | >= 60% identifient correctement le sujet (immunomodulateurs + RTIs) |
| S9c | Identification correcte du produit le mieux documente | >= 80% identifient OM-85 comme le mieux documente |

**Checker:** Resultats du test. Donnees quantitatives (N correct / N total) pour chaque question.

**Carrier:** Aurore (recrute les pediatres).

**Ce que ca prouve:** Ce protocole mesure la *comprehension*, pas l'engagement. Aucune etude GA existante n'a mesure la comprehension dans un format aussi contraint (5 secondes, audience clinique naive). Un PASS produirait les PREMIERES donnees de comprehension clinique pour un GA parametrique.

**Status:** OPEN — pas encore conduit.

Source: VEC_Literature_Analysis section 4.4, Jambor & Bornhauser 2024 rule #10.

---

## Open loops / Escalations

| Loop | Missing link | What's needed | Who | Status |
|------|-------------|---------------|-----|--------|
| H2 -> R-AUD1 | GA pas encore presente | Finaliser wireframe V10, auditer (H6), puis presenter a Aurore | Silas + Aurore | Ouvert |
| H6 -> R-AUD2 | Premier cycle NLM pas lance | Executer export_notebooklm.py, upload, lancer l'audit | Silas + NLM | Ouvert |
| H9 -> comprehension | Test pas encore conduit | Recruter 3-5 pediatres naifs, executer protocole Premier Regard | Aurore + Silas | Ouvert |
