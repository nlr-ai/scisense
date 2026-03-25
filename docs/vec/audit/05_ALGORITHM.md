# Algorithm — vec/audit

Deux algorithmes principaux : le cycle NotebookLM (A-AUD1) et la presentation Aurore (A-AUD2). Plus le protocole de Hard Reset (A-AUD3).

---

## A-AUD1: Cycle d'audit NotebookLM

```
ENTREE: GA courant (SVG + PNG) + doc chain + configs + artefacts

1. EXPORTER
   - python export_notebooklm.py
   - Genere un repertoire plat S0N/ (N = numero de session : S01, S02, S03...)
   - Contenu : doc chain (01_RESULTS a 10_SYNC), GA_SPEC.md, MISSION.md,
     configs (palette.yaml, layout_v10.yaml, content.yaml),
     artefacts courants (PNG delivery, SVG), system prompt V2.4
   - Exclure : rendus de versions deprecees, iterations anciennes, concepts IA obsoletes
   - Validation : >= 17 fichiers dans S0N/, system prompt V2.4 present (S6a, S6b)

2. UPLOADER dans NotebookLM
   - Charger tous les fichiers S0N/ comme sources
   - Charger config/notebooklm_system_prompt.md comme instruction systeme
   - Verifier que le system prompt V2.4 est bien pris en compte (ton naturel, pas de rapport formate)

3. CHOISIR LE FORMAT D'OUTPUT (PA6)
   - Audit structurel → Slide deck (SD1, SD2, SD3...)
   - Decantation narrative → Podcast
   - Consolidation R1-R4 → Report
   - Calibration P17 → Infographie
   - Plusieurs formats possibles par session

4. LANCER L'AUDIT
   - NotebookLM analyse l'ensemble et retourne :
     a. Problemes identifies (incoherences, gaps, erreurs) — avec reference aux patterns/invariants violes
     b. Patterns applicables (P1-P31, B1-B8) avec justification
     c. Suggestions de resolution — en termes d'intentions fonctionnelles, PAS de directives code
   - Si podcast : transcrire via scripts/transcribe_podcast.py (Whisper)
   - Validation : au moins un output exploitable recu (S6c)

5. INTEGRER
   - Pour chaque finding :
     a. Classifier : scientifique / visuel / editorial / structurel
     b. Lier a un pattern ou invariant (P#, V#, B#)
     c. Lier biologie a cognition (PA2 — cerveau entier obligatoire)
     d. Decider : corriger (commit) | documenter comme gap connu | escalader a Aurore
   - Si correction : modifier code/config, re-rendre (pipeline A5/A7), re-valider (H1/H5)
   - Si gap connu : documenter dans SYNC avec justification
   - Si escalade Aurore : preparer la presentation (A-AUD2) avec le finding en question
   - Validation : tous les problemes traites, aucune ligne "resolution" vide (S6d)

6. ARCHIVER
   - L'output NotebookLM (report/slides/transcript) va dans artefacts/audits/S0N_output.*
   - La table de findings va dans SYNC
   - L'export S0N/ est preserve (ne pas ecraser S01/ quand on cree S02/)

SORTIE: findings integres + corrections appliquees + SYNC mis a jour
```

---

## A-AUD2: Presentation a Aurore

```
ENTREE: GA rendu (PNG delivery) + findings NLM pertinents + points de decision ouverts

1. PREPARER
   - Selectionner les points qui necessitent le jugement d'Aurore :
     a. Choix de metaphore (quand deux options sont egalement defensibles)
     b. Validation hierarchie des preuves (V5)
     c. Impact cognitif (PH1 — "ca marche en 3 secondes?")
     d. Findings NLM que Silas ne peut pas trancher seul
   - Pour CHAQUE point : preparer 2-3 options concretes avec consequences (PA3)
   - Ne PAS inclure les problemes techniques deja resolus — Aurore tranche la science, pas les bugs

2. PRESENTER
   - Envoyer le PNG delivery via le canal de communication (WhatsApp, Telegram, email)
   - Accompagner de :
     a. Ce qui a change depuis la derniere version ("on a encastre le bouclier OM-85 sur les briques")
     b. Les 2-3 points de decision avec options
     c. Ce que NotebookLM a valide (si pertinent — renforce la confiance)
   - Ton : "nous" dans les defis, "tu" dans les succes (PA3)

3. RECEVOIR LE FEEDBACK
   - Attendre une reponse explicite — le silence n'est PAS un accord
   - Si Aurore donne un retour ambigu : reformuler en options concretes, pas en question ouverte
   - Si Aurore ne repond pas dans les 48h : relancer UNE fois avec un rappel leger

4. TRADUIRE LE FEEDBACK (PA4)
   - Chaque retour d'Aurore est traduit en intention fonctionnelle AVANT de coder
   - Documenter dans SYNC : feedback original -> intention -> pattern/invariant concerne
   - Si le feedback contredit un finding NLM : Aurore tranche (P13)

5. DECIDER
   - Si Aurore valide → H2 PASS → proceder a la validation finale (orchestration)
   - Si Aurore donne des corrections → retour a la compilation (A7), puis re-audit (A-AUD1)
   - Si Aurore bloque → proposer de nouvelles options, pas de nouvelle question

SORTIE: H2 PASS ou corrections a integrer + retour boucle
```

---

## A-AUD3: Protocole Hard Reset NotebookLM

```
ENTREE: session NLM polluee (references obsoletes, contradictions, boucle sterile)

1. DIAGNOSTIQUER
   - Identifier les symptomes :
     a. NLM reference des versions anterieures (V7, V8) qui n'existent plus
     b. Les suggestions contredisent des suggestions de la meme session
     c. Le dialogue repete les memes findings sans progression
     d. NLM donne des directives code au lieu de lister des problemes

2. DECIDER : HARD RESET ou CORRECTION DOUCE
   - Si symptomes (a) ou (b) : Hard Reset obligatoire
   - Si symptome (c) : essayer une correction douce d'abord ("concentre-toi sur X, ignore Y")
   - Si symptome (d) : rappeler le role (system prompt V2.4 section 4) avant de reset

3. EXECUTER LE HARD RESET
   - Incrementer le numero de session (S01 → S02 → S03...)
   - Re-executer export_notebooklm.py → nouveau S0N/
   - Exclure les fichiers bannis (rendus obsoletes, iterations mortes)
   - Creer une nouvelle session NotebookLM (pas re-utiliser l'ancienne)
   - Charger le system prompt V2.4 dans la nouvelle session
   - Premier message : etat courant du design (V10), objectif de cette session, ce qui a ete resolu

4. DOCUMENTER
   - Noter dans SYNC : "Hard Reset S0N → S0(N+1), raison : [symptome]"
   - Conserver l'ancien export S0N/ comme archive (ne pas supprimer)

SORTIE: session NLM propre, contexte frais, prete a auditer
```

---

## A-AUD4: Protocole GLANCE "Premier Regard" — Test de Compréhension Clinique

Deux modes d'exécution : MANUEL (pour la mission courante) et WEB (infrastructure scalable future).

### Mode MANUEL (Gate G4 — mission immunomodulator)

```
ENTREE: GA delivery PNG (1100x560) + 3-5 pédiatres naïfs

1. RECRUTER
   - Aurore identifie 3-5 pédiatres qui n'ont PAS lu le manuscrit
   - Critère : clinicien actif, pédiatrie générale ou pneumo pédiatrique
   - Aucun lien avec les auteurs du manuscrit

2. EXPOSER (5 secondes)
   - Montrer le GA sur smartphone (format mobile = usage réel MDPI)
   - Chronomètre strict : 5000ms d'exposition puis retrait
   - Pas de contexte verbal, pas de titre, pas d'explication

3. INTERROGER (3 questions canoniques)
   Q1: "Que venez-vous de voir ?" (rappel libre → valide B1, B4)
   Q2: "Quel produit vous a semblé le mieux documenté ?" (→ valide B3, V5, P32)
   Q3: "Cela modifierait-il votre prise en charge RTIs récurrentes 0-5 ans ?" (→ actionnabilité)

4. SCORER
   - S9a: ≥3/5 identifient le sujet (immunomodulateurs + RTIs) → PASS
   - S9b: ≥4/5 identifient OM-85 comme le mieux documenté → PASS
   - S9c: ≥2/5 expriment un changement de perception → PASS

5. DÉCIDER
   - Si S9a + S9b PASS → GA validé pour compréhension, libérer soumission MDPI
   - Si FAIL → identifier quel pattern visuel échoue, itérer V10.N+1

SORTIE: scores S9a-S9c + verbatims + décision GO/NO-GO
```

### Mode WEB (infrastructure scisense.fr — post-MDPI, scalable)

**Décision architecturale (24 mars 2026, proposition NotebookLM validée NLR) :**
Le test GLANCE sera déployé sur scisense.fr comme plateforme de validation cognitive permanente.

```
SPÉCIFICATIONS (à implémenter post-soumission MDPI) :

1. AUTHENTIFICATION
   - Profils médecins authentifiés (DB scisense.fr)
   - Vérification : clinicien actif, spécialité, jamais exposé à CE GA
   - Verrou anti-apprentissage : 1 test par compte par image

2. CHRONOMÈTRE IMPLACABLE
   - GA affiché format mobile (560px largeur) pendant exactement 5000ms
   - Aucun bouton retour, aucun téléchargement, aucun screenshot possible
   - Simulation biologique du scroll MDPI table des matières

3. ENTONNOIR GLANCE (3 questions canoniques)
   - Q1 rappel libre (champ texte)
   - Q2 hiérarchie évidence (choix parmi les 4 produits)
   - Q3 changement de pratique (échelle Likert 1-5)

4. DONNÉES
   - Réponses liées à l'ID médecin + l'ID du GA testé
   - Scoring automatique S9a/S9b/S9c
   - Dashboard de résultats par version du GA
   - Base de preuves pour démontrer la supériorité du VEC vs GA standard

VALEUR STRATÉGIQUE :
- Première base de données de compréhension clinique pour des GA paramétriques
- Preuve quantitative que le VEC détruit le spin visuel (V15)
- Actif SciSense différenciant vs BioRender/Mind the Graph
```

**Chronologie décidée :**
- Phase 1 (maintenant) : Mode MANUEL pour valider la V10 et libérer la soumission MDPI
- Phase 2 (post-MDPI) : Mode WEB sur scisense.fr pour les missions futures

**Evidence:** Bredbenner & Simon 2019 (RCT, N=538) — le fossé engagement-compréhension. Garcia-Retamero & Cokely 2017 (revue systématique, 27885 participants) — les aides visuelles transparentes améliorent la compréhension. Jambor & Bornhäuser 2024, rule #10 — feedback structuré recommandé.
