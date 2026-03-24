# VALIDATION — vec/exploration

**Module:** vec/exploration — Agents autonomes paralleles

---

## Invariants

### VE1: Plafond de 3 agents par sujet

Jamais plus de 3 sub-agents lances sur le meme sujet dans le meme cycle d'exploration. Si 3 agents ne suffisent pas, redecomposer le probleme avant de relancer.

**Test:** Compter les lancements par sujet dans les notes de session. >3 = violation.

---

### VE2: Prompt complet a 5 sections

Chaque sub-agent recoit un prompt contenant les 5 sections obligatoires: SCOPE, ANGLE, DELIVERABLE, CONTRAINTES, FORMAT DE RETOUR. Un prompt incomplet produit un agent qui derive.

**Test:** Avant chaque lancement, verifier que le prompt contient les 5 sections. Une section manquante = lancement interdit.

---

### VE3: Aucun finding non-resolu

A la cloture d'un cycle d'exploration, aucun probleme identifie par >1 agent ne peut rester sans reponse. Un probleme non-resolu est soit integre (correction planifiee), soit ecarte avec justification, soit escalade a Aurore.

**Test:** Scanner le bilan de cloture. Tout finding marque par >1 agent doit avoir un statut: INTEGRE, ECARTE (+ justification), ou ESCALADE.

---

### VE4: Conflits resolus avec trace

Tout conflit entre agents est resolu avec une trace documentee: les deux positions, la regle de hierarchie appliquee, la decision finale. Pas de resolution silencieuse.

**Test:** Chaque conflit dans le bilan de cloture doit avoir sa trace. Un conflit sans trace = violation.

---

### VE5: Mode declare (FG/BG)

Chaque cycle d'exploration est declare foreground ou background au moment du lancement. Cette declaration est irrevocable pour le cycle en cours.

**Test:** Chaque lancement dans les notes de session porte la mention [FG] ou [BG]. Absence = violation.

---

### VE6: Sub-agents ne codent pas

Les sub-agents analysent, diagnostiquent, et proposent. Ils ne modifient aucun fichier. Ils ne generent pas de SVG, PNG, PDF, ou code Python. La traduction en code est la responsabilite exclusive de Silas (I4).

**Test:** Le prompt de chaque sub-agent contient explicitement dans ses CONTRAINTES: "Ne code pas, ne modifie aucun fichier." Si un agent retourne du code, son output est rejete.

---

### VE7: Declencheur documente

Chaque cycle d'exploration est precede d'un declencheur documente (EP8). Pas d'exploration sans raison identifiee.

**Test:** Le diagnostic (AE1 step 1) doit citer le declencheur. Absence de declencheur = exploration non justifiee.

---

### VE8: Cycle clos avec bilan

Tout cycle d'exploration se termine par un bilan de cloture (BE8). Un cycle sans cloture est un cycle en fuite.

**Test:** Chaque cycle dans les notes de session ou le SYNC a une entree de cloture. Absence = cycle en fuite, a fermer au debut de la session suivante.

---

### VE9: Hierarchie de resolution respectee

Les conflits sont resolus dans l'ordre: precision scientifique > faisabilite visuelle > cout d'implementation. Aucun conflit ne peut etre resolu en inversant cette hierarchie.

**Test:** Chaque trace de conflit (VE4) cite la regle de hierarchie appliquee. Si la faisabilite visuelle a prime sur la precision scientifique, c'est une violation — sauf si Aurore a explicitement tranche.

---

### VE10: Extraction bornee a 3-5 findings par agent

L'integration ne retient pas plus de 5 findings par agent. Au-dela, le bruit l'emporte sur le signal.

**Test:** Le bilan d'integration montre au maximum 5 findings par agent. >5 = filtrage insuffisant.
