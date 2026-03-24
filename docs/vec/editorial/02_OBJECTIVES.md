# OBJECTIVES — vec/editorial

**Module:** vec/editorial — Tribunal editorial MDPI

---

## Objectif principal

Garantir que le Graphical Abstract est formellement conforme aux regles editoriales MDPI **avant** toute presentation humaine. Le tribunal editorial est un gate automatise — rien ne passe vers la phase d'audit (module `vec/audit`) sans 7/7 PASS.

---

## Goals

### G1: Zero friction editoriale

L'editrice Mindy Ma recoit un fichier qui passe silencieusement toutes les regles editoriales MDPI. Aucune demande de revision formelle. Le manuscrit avance directement vers le peer-review de contenu.

### G2: Detection precoce et bruyante

Toute violation editoriale est detectee au plus tot dans le pipeline (avant que le designer, Aurore, ou NotebookLM investissent du temps sur une version non conforme). Le script echoue bruyamment — exit code 1, rapport detaille.

### G3: Automatisation maximale des checks objectifs

Les checks qui peuvent etre automatises (geometrie, word count, patterns regex, palette) sont automatises. Les checks qui necessitent un jugement humain (lisibilite a 50% zoom, non-redondance structurelle, provenance des visuels) sont documentes comme semi-auto avec un carrier explicite.

### G4: Source de verite unique pour les regles MDPI

Le script `validate_ga.py` est la source de verite executrice. Les constantes (ratio, word budget, forbidden patterns, palette) sont definies une seule fois dans le script. Les fichiers YAML (`palette.yaml`, `content.yaml`) sont des sources de verite pour les donnees parametriques.

---

## Non-goals

### NG1: Validation scientifique

Le module editorial ne juge PAS si la science est correcte. La hierarchie des preuves (V5), la fidelite des mecanismes d'action, le choc cognitif (PH1) — tout ca releve du module `vec/audit` et du carrier Aurore (H2).

### NG2: Validation esthetique

Le module editorial ne juge PAS si le GA est beau, impactant, ou bien compose. La palette est verifiee pour la conformite (couleurs produits presentes, pas de couleurs non autorisees), pas pour l'harmonie chromatique. L'esthetique releve du module `vec/design_system`.

### NG3: Validation du pipeline de rendu

Le module editorial ne verifie PAS que les 3 fichiers (SVG + PNG full + PNG delivery) existent et sont non corrompus. C'est le role de H5 dans le module `vec/pipeline`. Le module editorial presuppose que le SVG et le PNG delivery lui sont fournis intacts.

### NG4: Remplacement du jugement humain

Les checks S1d (non-redondance Fig1/Fig2), S1e (droits visuels), S1f (lisibilite 50%) necessitent un jugement humain. Le module editorial ne pretend pas les automatiser. Il fournit les outils (downscale, checklist provenance) mais le verdict final est humain.

---

## Trade-offs

| Choix fait | Alternative rejetee | Raison |
|-----------|---------------------|--------|
| Script Python standalone | Integration dans le compositeur (compose_ga_v10.py) | Separation des responsabilites. Le compositeur produit, le validateur juge. Jamais le meme acteur. |
| Regex pour patterns interdits | NLP / analyse semantique | Sur-ingenierie. Les patterns MDPI sont des regles syntaxiques, pas semantiques. Regex suffit. |
| WARN pour couleurs inconnues | FAIL strict sur toute couleur non listee | Les couleurs structurelles (decoratives, intermediaires) peuvent etre ajoutees legitimement. WARN alerte sans bloquer. |
| Exit code 0/1 binaire | Score de conformite (70%, 85%) | La conformite MDPI est binaire. Un GA avec 6/7 est rejete exactement comme un GA avec 0/7. Pas de demi-mesure. |
