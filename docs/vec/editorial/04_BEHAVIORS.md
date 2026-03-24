# BEHAVIORS — vec/editorial

**Module:** vec/editorial — Tribunal editorial MDPI

---

## B1: Bloquer la presentation sur echec

Quand `validate_ga.py` retourne exit code 1 (FAIL), aucune presentation du GA n'est faite a Aurore, a NotebookLM, ou a Mindy Ma. Le pipeline est bloque a la gate editoriale. Le rapport du tribunal est lu, les violations sont corrigees dans le compositeur ou la config, et le validateur est relance.

**Declencheur :** Exit code 1.
**Effet observable :** Pas de message envoye, pas d'export NotebookLM, pas de soumission. Le rapport FAIL est affiche dans la console.

---

## B2: Laisser passer sur PASS complet

Quand `validate_ga.py` retourne exit code 0 (PASS, possiblement avec des WARN), le GA est autorise a avancer vers la phase d'audit. Les WARN sont consignes mais ne bloquent pas. Le rapport est archive dans la session SYNC pour tracabilite.

**Declencheur :** Exit code 0.
**Effet observable :** Le GA peut etre presente a Aurore. L'export NotebookLM peut etre genere. Les WARN sont lus et evalues humainement (une couleur non reconnue peut etre un ajout legitime ou une erreur).

---

## B3: Rapport detaille a chaque execution

Chaque execution du script produit un rapport formate qui affiche :
- Le nom de chaque check (S1a, S1b, etc.)
- Le statut (PASS / WARN / FAIL)
- Le detail (valeurs mesurees, violations trouvees)
- Le verdict global (PASS N/N ou FAIL N/N)

Le rapport est imprime sur stdout. Le format est lisible a l'oeil, pas un JSON machine. Le destinataire est Silas (ou NLR en debug) — un humain ou un citoyen IA qui lit un terminal.

---

## B4: Auto-detection des fichiers PNG

Quand les chemins PNG (full resolution et delivery) ne sont pas fournis explicitement en arguments, le script les infere a partir du nom du SVG :
- `wireframe_GA_v10.svg` → cherche `wireframe_GA_v10_full.png` et `wireframe_GA_v10_delivery.png` dans le meme repertoire.

Si les fichiers inferres n'existent pas, le check S1a (geometry PNG) et S5a (files exist) reportent l'absence sans crash. Le script continue les autres checks.

**Raison :** Pendant le developpement, on peut vouloir valider un SVG seul avant de lancer le pipeline de rendu PNG. Le validateur ne doit pas bloquer artificiellement.

---

## B5: Normalisation des couleurs avant comparaison

Toutes les couleurs extraites du SVG sont normalisees avant comparaison :
- Hex en majuscules (`#2563eb` → `#2563EB`)
- Noms CSS en minuscules (`White` → `white`)
- `none` et chaines vides sont ignores

**Raison :** Les compositeurs SVG (svgwrite, navigateurs, Inkscape) ecrivent les couleurs dans des formats differents. La normalisation evite les faux positifs.

---

## B6: Comptage de mots semantique

Le comptage de mots (S1b) utilise une heuristique specifique au contexte GA :
- Le `/` est traite comme un separateur de mots (`Wheezing / Asthma` = 3 mots, pas 2)
- Les symboles purs (>, ↑, →) ne comptent pas comme des mots
- Seuls les tokens contenant au moins un caractere alphanumerique comptent

**Raison :** La regle MDPI R3 parle de "mots" au sens humain, pas de tokens. Un symbole fleche n'est pas un mot. "IFN-gamma" est un mot (1 token avec trait d'union).

---

## B7: Chargement YAML sans dependance externe

Le script charge les fichiers YAML (`palette.yaml`, `content.yaml`) avec un parseur minimal interne (`_load_yaml_simple`), sans dependance a PyYAML. Cela permet l'execution du validateur dans n'importe quel environnement Python 3.10+ sans installation de packages.

**Limitation connue :** Le parseur ne supporte que les structures plates et les listes simples. Les structures YAML complexes (ancres, multi-documents, types explicites) ne sont pas supportees. Si `content.yaml` evolue vers une structure complexe, migrer vers PyYAML et ajouter la dependance.

---

## B8: Extraction exhaustive des textes SVG

L'extraction des elements `<text>` parcourt l'arbre SVG complet, incluant :
- Les elements `<text>` directs
- Les elements `<tspan>` imbriques (via `itertext()`)
- Les elements avec namespace SVG (`{http://www.w3.org/2000/svg}text`) et sans namespace

Tout texte invisible dans le SVG (opacity 0, display none, hors viewport) est quand meme extrait et valide. Le validateur est paranoiaque : si le texte existe dans le DOM SVG, il est soumis aux checks, meme s'il n'est pas rendu visuellement.
