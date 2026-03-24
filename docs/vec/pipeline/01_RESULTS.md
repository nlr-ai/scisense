# RESULTS — vec/pipeline

## R-PIP1: 3 fichiers produits a chaque iteration

Chaque execution du pipeline produit exactement 3 fichiers:

| Fichier | Format | Dimensions | Seuil taille |
|---------|--------|------------|--------------|
| `wireframe_GA_v10.svg` | SVG vectoriel | 3300x1680 viewBox | > 1 KB, XML parseable |
| `wireframe_GA_v10_full.png` | PNG raster | 2x delivery (2200x1120 pixels effectifs via device_scale_factor=2) | > 50 KB |
| `wireframe_GA_v10_delivery.png` | PNG raster | 1100x560 px, 600 DPI metadata | > 5 KB, PAS blanc |

**Mesure :** Les 3 fichiers existent, passent les seuils de taille, et les PNGs ont les dimensions attendues.

**Signal :** S5a (SVG non-vide) + S5b (full res correct) + S5c (delivery correct).

---

## R-PIP2: Palette fidele a la config

Le SVG genere contient les 4 couleurs produit exactes definies dans `palette.yaml`:

| Produit | Hex attendu |
|---------|-------------|
| OM-85 | #2563EB |
| PMBL | #0D9488 |
| MV130 | #7C3AED |
| CRL1505 | #059669 |

**Mesure :** Grep des 4 hex codes dans le SVG — tous presents.

**Signal :** S5d (palette presente).

---

## R-PIP3: Archivage sans ecrasement

Chaque version est archivee dans `artefacts/wireframes/` avec un numero de version. Aucun artefact existant n'est ecrase.

**Mesure :** Apres archivage, l'artefact vN-1 existe toujours et n'a pas ete modifie (checksum stable).

**Signal :** S5e (archive sans ecrasement).

---

## R-PIP4: Coherence config-rendu

Le rendu reflète fidelement les configs sources:
- Les couleurs dans le SVG correspondent a `palette.yaml`
- Les labels dans le SVG correspondent a `content.yaml` (meme word count)
- Les assets references dans `layout_v10.yaml` existent sur disque

**Mesure :** Comparaison automatique config vs SVG.

**Signal :** S5f (config coherence) + S5g (asset injection) + S5h (word count from source).

---

## Guarantee Loop

```
R-PIP1 (3 fichiers)        → S5a + S5b + S5c  → H5  → Silas (auto)
R-PIP2 (palette fidele)    → S5d              → H5  → Silas (auto)
R-PIP3 (archivage)         → S5e              → H5  → Silas (auto)
R-PIP4 (coherence config)  → S5f + S5g + S5h  → H5  → Silas (auto)
```

Tous les liens sont fermes. Carrier unique : Silas (execution automatique dans compose_ga_v10.py + validate_ga.py).
