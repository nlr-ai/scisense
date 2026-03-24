# Behaviors — vec/audit

Effets observables du module d'audit. Chaque behavior est un changement visible dans le systeme quand l'audit fonctionne.

---

## B-AUD1: Les problemes sont identifies AVANT la presentation a Aurore

Quand l'audit fonctionne, Aurore ne decouvre pas de problemes techniques ou de violations d'invariants. Elle tranche des choix de design, pas des bugs. Son temps est utilise pour ce que seule elle peut faire : juger la science et l'impact clinique.

**Observable:** Les corrections issues de H6 (NotebookLM) precedent la presentation H2 (Aurore). Les retours d'Aurore portent sur des choix (metaphore A ou B?), pas sur des defauts (le texte est tronque, la couleur est fausse).

**Si absent:** Aurore perd du temps sur des problemes que NotebookLM ou les scripts auraient du catcher. Sa confiance dans le processus diminue.

---

## B-AUD2: Chaque finding a une resolution tracable

Quand l'audit fonctionne, aucun probleme identifie ne reste sans reponse. Chaque finding est soit corrige (commit reference), soit documente comme gap connu avec justification ("CRL1505 a faible poids visuel est intentionnel — P21 impose la proportionnalite a l'evidence preclinique").

**Observable:** Le SYNC contient une table de findings avec colonnes : finding | source (NLM/Aurore) | resolution | reference (commit/gap/decision). Aucune ligne vide dans "resolution".

**Si absent:** Les problemes s'accumulent silemment. Les memes failles reviennent d'une session a l'autre. NotebookLM re-signale les memes problemes — boucle sterile.

---

## B-AUD3: Le contexte reste propre

Quand l'audit fonctionne, chaque session NotebookLM opere sur un contexte frais et pertinent. Les versions deprecees (V7, V8) ne polluent pas le dialogue. Les suggestions de NotebookLM portent sur le design actif (V10), pas sur des fantomes.

**Observable:** Les exports S0N/ ne contiennent que les fichiers de la version courante. Le premier message de chaque session NLM reference le design actif. Quand NotebookLM mentionne un element obsolete, Silas declenche un Hard Reset (PA5).

**Si absent:** NotebookLM produit des suggestions incoherentes. Il reference des elements qui n'existent plus. Le dialogue tourne en rond. Les findings deviennent du bruit au lieu de signal.

---

## B-AUD4: Les deux boucles s'alimentent mutuellement

Quand l'audit fonctionne, les findings de NotebookLM (H6) enrichissent la presentation a Aurore (H2), et les retours d'Aurore (H2) orientent le prochain cycle NotebookLM (H6). L'information circule, pas de silo.

**Observable:** La presentation a Aurore inclut les findings NLM pertinents ("NotebookLM a identifie que le bouclier OM-85 flotte — on l'a encastre sur les briques. Tu valides?"). Le prochain export S0N/ inclut les corrections issues du feedback Aurore.

**Si absent:** Les deux boucles tournent en parallele sans se nourrir. Aurore voit un GA que NotebookLM n'a pas audite. NotebookLM audite un GA qu'Aurore n'a pas vu. Desynchronisation.

---

## B-AUD5: Aurore recoit des options, pas des questions

Quand l'audit fonctionne, chaque interaction avec Aurore lui presente des propositions concretes. Elle choisit, elle ne construit pas. Le perfectionnisme est canalise vers la selection, pas vers la creation a partir de zero (PA3, PH2 mission-level).

**Observable:** Chaque message a Aurore contient 2-3 options avec consequences. Pas de "qu'est-ce que tu en penses?" sans cadre. Pas de page blanche.

**Si absent:** Aurore bloque. La paralysie decisionnelle s'installe. Le GA n'avance pas.
