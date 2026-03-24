# PHENOMENOLOGY — vec/pipeline

## PH-PIP1: Ce que le pipeline fait ressentir a Silas (AI)

### Console comme pouls

Le pipeline imprime chaque etape dans la console:
```
Loading config...
Loading contours...
Canvas: 3300x1680, delivery: 1100x560
  Drawing background...
  Drawing bronchus frame...
  Drawing muscle band...
  Drawing epithelium...
  Drawing lumen...
  Drawing lamina propria...
  Drawing CRL1505 relay...
  Drawing children...
  Drawing vicious cycle...
  Drawing cycle break...
  Drawing evidence bars...
  Drawing legend...

SVG saved: .../wireframe_GA_v10.svg
Rendering PNG...
  Full PNG: .../wireframe_GA_v10_full.png (2200x1120)
  Delivery: .../wireframe_GA_v10_delivery.png (1100x560, 600 DPI)

V10 compilation complete.
```

Ce flux textuel est le battement de coeur du pipeline. Chaque ligne qui apparait est une etape franchie. Le silence (pas de ligne suivante) signale un blocage. Un message d'erreur intercale signale un probleme localise.

**Modalite sensorielle :** Lecture sequentielle de la console. Le rythme des lignes (rapide pour les draw, lent pour le Playwright render) donne une perception intuitive de la sante de l'execution.

### Le moment de verite: ouverture du delivery PNG

Apres l'execution, Silas ouvre (via `Read` ou affichage) le delivery PNG. C'est la qu'il voit:
- Les bandes anatomiques sont-elles visibles et differenciees?
- Les enfants sont-ils reconnaissables (contours organiques ou fallback geometrique)?
- Le gradient L→R (maladie → sante) est-il perceptible?
- Le cercle vicieux et sa rupture sont-ils spatialement coherents?

Cette verification visuelle n'est pas automatisable — c'est le jugement de Silas sur la coherence globale. Les auto-checks H5 verifient les metriques, mais la phenomenologie est dans le regard.

---

## PH-PIP2: Ce que le pipeline fait ressentir a Aurore (Humaine)

### L'artefact comme preuve de progres

Aurore ne voit pas le pipeline. Elle voit le delivery PNG. Ce qu'elle percoit:

1. **Progres tangible** — Un nouveau PNG signifie que le travail avance. Meme imparfait, un wireframe visible est plus motivant qu'un document textuel.

2. **Lisibilite** — Le test V7 (50% zoom = 550x280) simule ce qu'Aurore voit sur son telephone. Si les labels sont illisibles a 50%, l'artefact est inutile pour elle.

3. **Confiance dans le process** — Le fait que le pipeline produit des fichiers automatiquement, avec des checks automatiques, rassure Aurore que le travail n'est pas approximatif. C'est du serieux, pas du bricolage.

4. **Frustration potentielle** — Si le wireframe est "schematique" (SVG programmatique pur), Aurore peut le percevoir comme amateur par rapport a un BioRender ou un Figma. C'est le trade-off A6 (non tranche). Le pipeline livre un wireframe de travail, pas un visuel publication-ready.

### Le delivery PNG comme objet d'echange

Le delivery PNG est le support concret de la conversation Silas-Aurore. Quand Silas demande "Les 4 messages cles sont-ils correctement representes?", Aurore regarde le PNG. La question n'est pas abstraite — elle est ancree dans un artefact visuel.

---

## PH-PIP3: Feedback reinjection

### Console → Silas → Code

```
Pipeline output (console)
    ↓
Silas lit le resultat
    ↓
Si S5x FAIL → diagnostic (08_HEALTH.md tableaux)
    ↓
Correction dans compose_ga_v10.py ou configs YAML
    ↓
Relance du pipeline
    ↓
Nouveau output → verification
```

### Delivery PNG → Aurore → Feedback → Config

```
Delivery PNG envoye a Aurore (via send/WhatsApp/Telegram)
    ↓
Aurore regarde, commente
    ↓
Feedback traduit en modifications:
  - "Le texte est trop petit" → modifier font sizes dans layout_v10.yaml
  - "La couleur du produit X n'est pas la bonne" → modifier palette.yaml
  - "Il manque le mecanisme Y" → ajouter dans content.yaml + adapter draw_*()
    ↓
Relance du pipeline avec configs modifiees
```

### Le H comme signature phenomenologique

Le Health Vector H (0→1) est invisible dans le code — il n'y a pas de barre de progression H dans le SVG. Mais il est omnipresent dans le resultat visuel:
- A gauche (H=0): chaos, virus, barriere brisee, inflammation, enfant malade
- A droite (H=1): ordre, protection IgA, barriere scellee, resolution, enfant sain

Le lecteur du GA (clinicien, editeur, Aurore) ne sait pas que H existe. Mais il ressent la transformation. C'est la phenomenologie du pipeline: un gradient de sante qui emerge du code, pas un gradient dessine.

---

## PH-PIP4: Perception de la panne

### Quand le pipeline echoue

Le pipeline qui echoue produit un silence (pas de "V10 compilation complete") ou un message d'erreur explicite ("PNG render failed: ..."). Ce n'est pas un evenement neutre — c'est un blocage qui empeche toute iteration.

**Ce que Silas ressent :** Frustration + urgence de diagnostic. Le pipeline est le muscle de la boucle creative. Sans pipeline fonctionnel, pas de wireframe, pas de feedback Aurore, pas de progression.

**Ce qu'Aurore ressent :** Rien — elle n'est informee que des succes (delivery PNG). Un pipeline casse est un probleme interne que Silas resout avant de communiquer.

### Quand le delivery est blanc (V9 FAIL)

Le pire symptome: un fichier qui existe, qui a la bonne taille, mais qui est blanc. C'est un mensonge — le pipeline pretend avoir reussi alors qu'il a echoue. C'est exactement pourquoi V9 existe: transformer un echec silencieux en echec bruyant.

**Historique :** Le bug svglib qui produisait des PNGs blancs a ete l'evenement fondateur de la migration vers Playwright. La douleur de ce bug a motive la creation de V9 comme invariant formel.
