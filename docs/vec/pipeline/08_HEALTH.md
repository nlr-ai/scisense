# HEALTH — vec/pipeline

## H5: Pipeline de rendu E2E

Chaque iteration produit 3 fichiers. Si l'un est manquant ou corrompu, Fail Loud.

**Validates :** V8 (rendu complet), V9 (delivery non-blanc), P8 (E2E), P10 (multi-resolution).

---

## Sense Signals

| ID | Signal | Checks | Automation | Invariant |
|----|--------|--------|------------|-----------|
| S5a | SVG non-vide | Fichier > 1 KB, parseable XML (`ET.parse()`) | Auto | V-PIP2 |
| S5b | PNG full res correct | Dimensions ~= (dw*2, dh*2), fichier > 50 KB | Auto | V8, V-PIP1 |
| S5c | PNG delivery correct | Dimensions = (dw, dh), fichier > 5 KB, PAS blanc (mean pixel < 250) | Auto | V8, V9 |
| S5d | Palette presente | Les 4 hex (#2563EB, #0D9488, #7C3AED, #059669) dans le SVG | Auto | V-PIP3 |
| S5e | Archive sans ecrasement | Fichiers vN dans artefacts/wireframes/, pas de vN-1 modifie | Auto | V-PIP5 |
| S5f | Config coherence | Couleurs palette.yaml = couleurs dans le SVG | Auto | — |
| S5g | Asset injection | Tous les assets references dans layout.yaml existent sur disque | Auto | — |
| S5h | Word count from source | Count mots content.yaml = count dans le SVG rendu | Auto | — |

---

## Checker

**Script principal :** `compose_ga_v10.py` integre les checks S5a-S5d en post-generation (A5 steps 4-6).

**Script complementaire :** `validate_ga.py` consolide les checks H1 (editorial) et peut etre etendu pour inclure les checks H5.

**Execution :** Automatique a chaque run de `compose_ga_v10.py`. Les checks sont imprimes dans la console. Pas encore de code de retour non-zero en cas d'echec (amelioration P-PIP3).

---

## Guarantee Loop

```
R-PIP1 (3 fichiers produits)     → S5a + S5b + S5c  → H5 PASS/FAIL  → Silas (console output)
R-PIP2 (palette fidele)          → S5d               → H5 PASS/FAIL  → Silas (console output)
R-PIP3 (archivage non-destructif)→ S5e               → H5 PASS/FAIL  → Silas (console output)
R-PIP4 (coherence config-rendu)  → S5f + S5g + S5h   → H5 PASS/FAIL  → Silas (console output)
```

**Carrier :** Silas (tout automatisable).

---

## Diagnostic par signal

### S5a FAIL — SVG non-vide

| Symptome | Cause probable | Action |
|----------|---------------|--------|
| Fichier 0 octets | `dwg.save()` a echoue silencieusement | Verifier permissions disque, espace disque |
| Fichier < 1 KB | SVG tronque, crash pendant generation | Relancer, verifier les draw_*() pour exceptions |
| XML parse error | SVG corrompu (caracteres speciaux non-echappes dans labels) | Verifier content.yaml pour caracteres speciaux |

### S5b FAIL — Full PNG

| Symptome | Cause probable | Action |
|----------|---------------|--------|
| Fichier absent | Playwright non installe ou pas de Chromium | `playwright install chromium` |
| Dimensions incorrectes | device_scale_factor mal configure | Verifier `new_page(device_scale_factor=2)` |
| Fichier < 50 KB | SVG non charge dans le HTML wrapper | Verifier le chemin file:/// dans _render_v10.html |
| Timeout | SVG trop complexe pour le viewport | Verifier que le viewport est delivery size (1100x560), pas full size |

### S5c FAIL — Delivery non-blanc

| Symptome | Cause probable | Action |
|----------|---------------|--------|
| mean pixel > 250 | Le full PNG etait blanc → le resize l'est aussi | Diagnostiquer S5b d'abord |
| Fichier < 5 KB | Le resize a produit une image vide | Verifier que Pillow a ouvert le full PNG correctement |
| Dimensions != (dw, dh) | Bug dans le resize LANCZOS | Verifier les parametres passes a `img.resize()` |

### S5d FAIL — Palette absente

| Symptome | Cause probable | Action |
|----------|---------------|--------|
| 1 couleur manquante | L'element correspondant n'a pas ete dessine | Verifier la fonction draw_*() correspondante |
| Toutes manquantes | palette.yaml non charge ou chemin incorrect | Verifier load_config() et CONFIG_DIR |

### S5e FAIL — Archive ecrasee

| Symptome | Cause probable | Action |
|----------|---------------|--------|
| Checksum change | Le pipeline ecrit au meme chemin sans versioning | Implementer le suffixe _iterN ou timestamp |

---

## Bug historique resolu

**Probleme :** Le rendu delivery (1100x560) via svglib produisait un fichier de 4 KB, blanc. S5c FAIL systematique.

**Diagnostic :** svglib ne supporte pas correctement les SVGs complexes avec gradients, paths Bezier, et text elements multiples.

**Resolution :** Migration vers Playwright HTML wrapper. Le SVG est enveloppe dans un HTML minimal avec `<img>` et rendu via Chromium headless a la taille delivery avec `device_scale_factor=2`. Le timeout Playwright a 3300x1680 a ete contourne par cette approche (rendre au viewport delivery, pas au viewport full).

**Date :** Resolu entre V9 et V10 du compositeur.

---

## Statut des boucles

| Signal | Statut | Derniere verification |
|--------|--------|----------------------|
| S5a | IMPLEMENTE — check dans compose_ga_v10.py | Console output |
| S5b | IMPLEMENTE — check implicite (Playwright crash = message erreur) | Console output |
| S5c | PARTIEL — le print existe, pas d'assert formel mean pixel | A formaliser |
| S5d | IMPLEMENTE — grep dans A5 step 5 | Console output |
| S5e | PARTIEL — pas de protection explicite contre ecrasement | A formaliser |
| S5f | NON IMPLEMENTE — a ajouter | — |
| S5g | NON IMPLEMENTE — a ajouter | — |
| S5h | NON IMPLEMENTE — a ajouter | — |

---

## Ameliorations identifiees

1. **Code de retour non-zero** — `compose_ga_v10.py` devrait retourner `sys.exit(1)` si un check H5 echoue, pour permettre l'automatisation (CI/CD, scripts appelants).

2. **Formaliser S5c** — Ajouter un assert mean pixel < 250 apres le resize, pas juste un print.

3. **Implementer S5e** — Verifier avant ecriture que le fichier destination n'existe pas deja, ou generer un nom unique.

4. **Implementer S5f-S5h** — Ajouter les checks de coherence config dans une fonction `post_check()` appelee apres le rendu.

5. **Consolider dans validate_ga.py** — Unifier les checks H1 (editorial) et H5 (pipeline) dans un seul script de validation executable independamment.
