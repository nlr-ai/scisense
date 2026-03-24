# ALGORITHM — vec/orchestration

## A-ORC1: Boucle principale — les 4 phases

```
ENTREE: mission YAML (manuscrit, specs, contraintes MDPI) + doc chain mission

1. PHASE CONCEPT (P24)
   a. DIAGNOSTIC — identifier l'obstacle cognitif principal du lecteur cible
   b. AXES DE VARIATION — definir 3 variables independantes (P2)
   c. 3 PROPOSITIONS ASCII — structure spatiale + parcours visuel, pas de code
   d. PDF GENERATION — generate_proposal_pdf.py (reportlab)
   e. VERIFICATION VISUELLE (P25) — Read le PDF, verifier lisibilite
   f. ENVOI AURORE — send via MCP, question explicite: "Quelle direction?"
   g. GATE G1: Aurore GO explicite?
      - Si GO → passer a COMPILATION
      - Si NO → re-diagnostiquer avec le feedback (retour a 1a)
      - Si pivot architectural → mobiliser I2 (NLR) avant de continuer
   h. DOCUMENTER dans SYNC: direction validee, axe choisi, feedback Aurore

2. PHASE COMPILATION (A5/A7)
   a. CONFIGURER — editer layout_v10.yaml, palette.yaml, content.yaml selon le concept valide
   b. COMPILER — python compose_ga_v10.py (A7)
   c. VALIDER EDITORIAL — python validate_ga.py (H1: S1a-S1g)
   d. VALIDER PIPELINE — verifier S5a-S5h (3 fichiers, palette, archivage, coherence)
   e. VERIFICATION VISUELLE (P25) — Read le PNG delivery, verifier equilibre spatial
   f. Si CALIBRATION necessaire (elements organiques):
      - Generer images IA de reference (I5)
      - Extraire contours (scikit-image + Douglas-Peucker)
      - Integrer dans compose_ga_v10.py
      - Re-compiler (retour a 2b)
   g. Si exploration necessaire:
      - Lancer sub-agents (I6) avec angle + deliverable
      - Integrer findings (retour a 2a ou 2b)
   h. GATE G2: H1 PASS + H5 PASS + P25 PASS?
      - Si tous PASS → passer a AUDIT
      - Si FAIL → corriger et retour a 2b (si technique) ou 2a (si config)
   i. DOCUMENTER dans SYNC: version produite, checks PASS/FAIL, corrections appliquees

3. PHASE AUDIT (A9)
   a. EXPORT — python export_notebooklm.py → S0N/
      - Verifier que les fichiers bannis sont exclus
      - Verifier que le system prompt V2.4 est inclus
   b. UPLOAD — charger S0N/ dans NotebookLM (I3)
   c. AUDIT REQUEST — NLM analyse et retourne:
      - Problemes identifies (incoherences, gaps, erreurs)
      - Patterns applicables avec justification
      - Suggestions concretes
   d. OUTPUT FORMS — NLM peut produire: report, slide deck, podcast, infographic
   e. INTEGRATION — Silas traduit en:
      - Corrections code (compose_ga_v10.py, configs)
      - Mises a jour documentation (doc chain)
      - Nouveaux patterns ou behaviors si decouverte
   f. SUB-AGENTS (optionnel) — lancer agents specialises (I6):
      - Angle immunologie (validation mecanismes)
      - Angle communication visuelle (lisibilite, impact)
      - Matrice produit-mecanisme (couverture)
      - Max 3 agents par sujet (rendements decroissants)
   g. GATE G3: H6 PASS (S6a-S6d) + zero probleme critique ouvert?
      - Si PASS → passer a VALIDATION
      - Si FAIL → integrer corrections et retour a 3e (si fixable dans l'audit)
                   ou retour a 2b (si correction necessite recompilation)
   h. DOCUMENTER dans SYNC: rapport d'audit resume, problemes resolus, gaps connus

4. PHASE VALIDATION
   a. ENVOYER A AURORE — GA final (PDF ou PNG) via MCP
      - Question explicite: "Les 4 messages cles sont-ils correctement representes?
        La hierarchie des preuves est-elle exacte?"
   b. REVUE CLINIQUE — Aurore examine et repond:
      - GO → H2 PASS
      - Corrections → retour a la phase pertinente (2 ou 3)
   c. GATE G4: H2 PASS + R1-R4 tous fermes?
      - Si PASS → SHIP (soumission a l'editeur)
      - Si FAIL → ITERATE (voir A-ORC2)
   d. DOCUMENTER dans SYNC: outcome (SHIP ou ITERATE), feedback Aurore, version finale

SORTIE: GA pret a soumettre (SHIP) ou diagnostic de retour (ITERATE)
```

## A-ORC2: Boucle ITERATE — retour a la phase pertinente

```
ENTREE: gate G4 FAIL avec diagnostic

1. IDENTIFIER LE GATE QUI ECHOUE
   - H1 FAIL → violation MDPI non detectee
   - H2 FAIL → erreur scientifique ou metaphore trahissant la science
   - H5 FAIL → rendu corrompu ou incomplet
   - H6 FAIL → probleme NLM non resolu

2. DIAGNOSTIQUER LA CAUSE
   - Erreur d'implementation (config, code) → COMPILATION
   - Erreur de direction (concept, architecture visuelle) → CONCEPT
   - Erreur d'integration (correction NLM mal appliquee) → AUDIT
   - Pas de diagnostic vague. "Ca ne marche pas" est interdit.
     "H2 FAIL: hierarchie preuves inversee OM-85/PMBL" est un diagnostic.

3. RETOURNER A LA PHASE CORRESPONDANTE
   - Mettre a jour SYNC: "Phase: [PHASE] (retour depuis VALIDATION, [GATE] FAIL: [DIAGNOSTIC])"
   - Re-executer la phase depuis le debut de ses steps
   - Quand le gate de sortie de la phase est PASS, reprendre le flux normal

SORTIE: GA re-entre dans le flux a la phase pertinente
```

## A-ORC3: Demarrage de session

```
ENTREE: nouvelle session humaine

1. LIRE SYNC (10_SYNC.md)
   - Phase courante
   - Gates ouverts
   - Prochaine action
   - Bloqueurs
   - Numero de version

2. HARD RESET (P11) si nouvelle version majeure
   - Ne PAS charger les wireframes des versions precedentes
   - Ne PAS re-ouvrir les debats resolus
   - Se fier au SYNC, pas a la memoire residuelle

3. VERIFIER les health checks de la phase courante
   - Si phase = COMPILATION → verifier H1, H5
   - Si phase = AUDIT → verifier H6
   - Si phase = VALIDATION → verifier H2

4. REPRENDRE a la prochaine action documentee dans SYNC

SORTIE: session orientee, prete a produire
```

## A-ORC4: Fin de session

```
ENTREE: fin de session humaine (temps ecoule ou objectif atteint)

1. METTRE A JOUR SYNC
   - Phase courante
   - Gates ouverts (G1-G5 avec status PASS/FAIL/OPEN)
   - Prochaine action (une seule, actionnable)
   - Bloqueurs (le cas echeant)
   - Numero de version courant

2. SI prochaine session = audit NLM
   - Regenerer S0N/ via export_notebooklm.py
   - Verifier exclusion des fichiers bannis

3. ARCHIVER les artefacts produits dans la session
   - Wireframes dans artefacts/wireframes/ avec numero de version
   - Ne jamais ecraser un artefact existant

SORTIE: SYNC a jour, session proprement fermee
```

## A-ORC5: Verification de gate

```
ENTREE: transition entre phases (ex: COMPILATION → AUDIT)

1. LISTER les conditions du gate (voir P-ORC2 pour la table)

2. EVALUER chaque condition
   - Automatisable → executer le script (validate_ga.py, file checks)
   - Semi-auto → executer le script + revue visuelle
   - Manuel → verifier le document (sign-off Aurore, rapport NLM)

3. AGGREGER
   - Toutes PASS → gate PASS, documenter dans SYNC, passer a la phase suivante
   - Au moins une FAIL → gate FAIL, documenter le FAIL dans SYNC, rester dans la phase courante

SORTIE: PASS (progression) ou FAIL (blocage documente)
```
