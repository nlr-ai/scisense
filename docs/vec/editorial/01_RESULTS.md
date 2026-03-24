# RESULTS — vec/editorial

**Module:** vec/editorial — Tribunal editorial MDPI

---

## R1: Le GA passe 7+ checks de conformite MDPI

**Definition:** Avant toute presentation a un humain (Aurore, Mindy Ma, peer reviewer), le Graphical Abstract a ete valide par `validate_ga.py` et a obtenu un verdict PASS sur les 7 sense signals S1a-S1g. Aucun FAIL n'est tolere. Les WARN sont acceptables (couleurs non reconnues mais non interdites).

**Mesure:** Exit code 0 de `validate_ga.py`. Le rapport imprime les 7 checks avec leur statut individuel.

**Impact:** Un GA non conforme est rejete par l'editrice MDPI (Mindy Ma) sans review. Le manuscrit perd sa fenetre editoriale. L'editrice perd confiance dans la qualite des soumissions SciSense. Le cout d'un rejet editorial pour non-conformite est disproportionne par rapport au cout de 7 checks automatises.

### Decomposition

| Check | Invariant | Ce qui est mesure | Seuil |
|-------|-----------|-------------------|-------|
| S1a Geometry | V1 | Ratio SVG viewBox = 1100:560 (= 3300:1680 a 3x). Dimensions PNG delivery = 1100x560 | Exactement le ratio. Pas de tolerance. |
| S1b Word Budget | V3 | Nombre total de mots dans les elements `<text>` du SVG | <= 30 mots |
| S1c No Titles | V2 | Absence de patterns interdits : noms d'auteurs, affiliations, DOI, references, institutions | Zero match regex |
| S1d Palette | B5, P7 | Les 4 couleurs produit (#2563EB, #0D9488, #7C3AED, #059669) sont presentes. Aucune couleur non autorisee. | 4/4 presentes, 0 non autorisee |
| S1e No GA Heading | R1 MDPI | Aucun texte "Graphical Abstract" dans le rendu | Zero match |
| S1f Lisibility | V7 | Labels lisibles quand l'image est affichee a 550x280 px | Semi-auto — verification visuelle par Silas |
| S1g Forbidden Patterns | V2, V6 | Absence de "et al.", "Figure N", "Dr.", "PhD", "University", "Department", "Hospital" | Zero match regex |

### Relation avec les results de la mission

Ce result (R1 editorial) mappe directement sur le R1 de la mission immunomodulateur (`08_HEALTH.md` : H1). Le module editorial est le bras executant de H1. Si le module editorial dit PASS, H1 de la mission dit PASS.

### Ce que R1 n'est PAS

- R1 ne valide pas la science (c'est R2 de la mission, H2, carrier Aurore)
- R1 ne valide pas le pipeline de rendu (c'est H5, module `vec/pipeline`)
- R1 ne valide pas l'impact cognitif (c'est PH1, module `vec/design_system`)
- R1 ne valide pas la non-redondance structurelle avec Fig1/Fig2 (c'est S1d de la mission, semi-auto, revue Aurore)

R1 est une gate binaire : le GA est-il formellement conforme aux regles editoriales MDPI ? Oui ou non. Pas de nuance, pas de "presque". 7/7 ou rien ne passe.
