# HEALTH — vec/orchestration

6 health checkers mapping 1:1 avec les 6 results.

```
R-ORC1 (concept GO)         ← H-ORC1 (GO Aurore archive)       ← S-ORC1
R-ORC2 (compilation valide) ← H-ORC2 (H1+H5+P25 PASS)         ← S-ORC2a/b/c
R-ORC3 (audit complet)      ← H-ORC3 (H6 PASS + zero crit)    ← S-ORC3
R-ORC4 (validation ferme)   ← H-ORC4 (H2 PASS + R fermes)     ← S-ORC4a/b/c
R-ORC5 (sessions propres)   ← H-ORC5 (SYNC a jour)            ← S-ORC5a/b
R-ORC6 (pas de regression)  ← H-ORC6 (artefacts intacts)       ← S-ORC6a/b
```

---

## H-ORC1: GO Aurore archive — validates R-ORC1

Le GO d'Aurore sur la direction conceptuelle est explicitement documente avant toute compilation.

### Sense signals

| ID | Signal | Check | Automation |
|----|--------|-------|------------|
| S-ORC1 | GO Aurore archive | Message Aurore avec GO + direction choisie documente dans SYNC mission | Manuel — verification Silas |

**Checker:** Verifier que le SYNC mission contient une entree "Aurore GO" avec: date, direction choisie, feedback eventuel. Un silence n'est pas un GO (VN-ORC2).

**Carrier:** Aurore (decision) + Silas (documentation).

**Status:** Loop fermee — mecanisme defini.

---

## H-ORC2: Compilation valide — validates R-ORC2

Le wireframe passe les checks editoriaux, pipeline, et visuels AVANT d'etre soumis a l'audit.

### Sense signals

| ID | Signal | Check | Automation |
|----|--------|-------|------------|
| S-ORC2a | H1 PASS | validate_ga.py retourne PASS sur S1a-S1g | Auto — script |
| S-ORC2b | H5 PASS | 3 fichiers produits, palette, archivage, coherence (S5a-S5h) | Auto — pipeline |
| S-ORC2c | P25 PASS | Verification visuelle documentee (Read du PNG delivery) | Semi-auto — Silas documente |

**Checker:** S-ORC2a et S-ORC2b sont automatisables (scripts). S-ORC2c est semi-automatique: Silas lit le PNG delivery et documente "P25 PASS: equilibre spatial OK, labels lisibles, pas de chevauchement" ou "P25 FAIL: [raison]" dans le SYNC.

**Carrier:** Silas (auto + visuel).

**Status:** Loop fermee — scripts implementes, processus visuel defini.

---

## H-ORC3: Audit complet — validates R-ORC3

L'audit NotebookLM est termine et tous les problemes critiques sont resolus.

### Sense signals

| ID | Signal | Check | Automation |
|----|--------|-------|------------|
| S-ORC3a | S6a PASS | Export S0N/ cree avec tous les fichiers requis | Auto — file count |
| S-ORC3b | S6b PASS | System prompt V2.4 charge | Auto — file exists + version |
| S-ORC3c | S6c PASS | Reponse audit recue (report ou slide deck) | Manuel — verification Silas |
| S-ORC3d | S6d PASS | Tous les problemes traites (corriges ou documentes) | Semi-auto — checklist |
| S-ORC3e | Zero critique ouvert | Aucun probleme marque "critique" n'est en status "ouvert" | Semi-auto — checklist |

**Checker:** S-ORC3a et S-ORC3b sont automatisables. S-ORC3c-e necessitent la revue de Silas apres reception de l'output NLM. La checklist de problemes est dans le rapport d'audit, chaque probleme doit avoir un status: RESOLU, DOCUMENTE, ou OUVERT. Si un OUVERT est marque critique → H-ORC3 FAIL.

**Carrier:** Silas + NotebookLM.

**Status:** Loop fermee — mecanisme defini.

---

## H-ORC4: Validation ferme — validates R-ORC4

Le GA est soit pret a SHIP, soit renvoye en ITERATE avec diagnostic.

### Sense signals

| ID | Signal | Check | Automation |
|----|--------|-------|------------|
| S-ORC4a | H2 PASS | Sign-off scientifique explicite d'Aurore | Manuel — message Aurore |
| S-ORC4b | R1-R4 tous fermes | Tous les resultats mission sont PASS | Semi-auto — verification table R-status |
| S-ORC4c | (si ITERATE) Gate echoue identifie | Le gate specifique qui echoue est nomme + diagnostic + phase de retour | Manuel — Silas documente |

**Checker:** SHIP = S-ORC4a PASS + S-ORC4b PASS. ITERATE = S-ORC4c documente (V-ORC7: diagnostic obligatoire). Il n'existe pas d'etat intermediaire.

**Carrier:** Aurore (sign-off) + Silas (coordination).

**Status:** Loop fermee — mecanisme defini.

---

## H-ORC5: Sessions propres — validates R-ORC5

Chaque session demarre avec un etat cognitif propre via SYNC.

### Sense signals

| ID | Signal | Check | Automation |
|----|--------|-------|------------|
| S-ORC5a | SYNC a jour | SYNC contient: phase courante, gates, prochaine action, bloqueurs, version | Semi-auto — verification structure |
| S-ORC5b | S0N/ regenere | Si session NLM imminente: export_notebooklm.py execute, fichiers bannis exclus | Auto — script + file check |

**Checker:** En debut de session, lire SYNC. Si les champs obligatoires sont absents ou obsoletes (date anterieure a la derniere session), H-ORC5 FAIL. Premiere action: mettre a jour le SYNC.

**Carrier:** Silas + NLR.

**Status:** Loop fermee — mecanisme defini.

---

## H-ORC6: Pas de regression — validates R-ORC6

Les versions precedentes sont intactes et les fantomes sont exclus des exports.

### Sense signals

| ID | Signal | Check | Automation |
|----|--------|-------|------------|
| S-ORC6a | Artefacts vN-1 intacts | Fichiers wireframe_GA_vN-1 existent et checksums stables apres production vN | Auto — file exists + checksum |
| S-ORC6b | Fichiers bannis absents de S0N/ | Aucun fichier de la liste de fichiers bannis n'est present dans S0N/ | Auto — file check apres export |

**Checker:** S-ORC6a est verifiable par comparaison de checksums avant/apres compilation. S-ORC6b est verifiable par scan du repertoire S0N/ contre la liste de fichiers bannis dans export_notebooklm.py.

**Carrier:** Silas (auto).

**Status:** Loop fermee — mecanisme defini.

---

## Open loops / Escalations

| Loop | Missing link | What's needed | Who | Status |
|------|-------------|---------------|-----|--------|
| Tous | Instance concrete | Les H-ORC checks sont definis mais pas encore executes sur une mission reelle | Silas | Premier run = mission immunomodulateur |
| H-ORC1 | Pas de GO Aurore enregistre | La mission immunomodulateur est en phase COMPILATION, le GO concept a ete implicite (feedback v8.1) mais pas formellement gate | Silas + Aurore | A regulariser |
| H-ORC6 | Checksums pas automatises | Le check S-ORC6a (checksums stables) n'a pas de script dedie. Verification manuelle pour l'instant. | Silas | Ouvert |
