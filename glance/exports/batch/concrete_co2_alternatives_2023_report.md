# GLANCE GA Analysis Report

**Overall Score:** 0.70
**Nodes:** 8 | **Links:** 13

## Recommendations (prioritized)

## Strengths

- **encoding_channel** — Length encoding (beta=1.0) — optimal quantitative channel. Perceived magnitude matches actual magnitude with no compression.
- **semantic_depth** — Rich semantic references (0.83/1.0) — supports accurate S9a comprehension measurement.
- **space:concrete_co2_alternatives_2023_domain** — Solide (w=0.7825833333333333, s=0.8300000000000001) — bien établi dans la littérature ou le design.
- **thing:concrete_co2_alternatives_2023_geopolymer** — Solide (w=0.95, s=0.958) — bien établi dans la littérature ou le design.
- **thing:concrete_co2_alternatives_2023_lc3** — Solide (w=0.64, s=0.9) — bien établi dans la littérature ou le design.
- **narrative:concrete_co2_alternatives_2023_comparison** — Solide (w=0.9325833333333333, s=0.94) — bien établi dans la littérature ou le design.
- **moment:concrete_co2_alternatives_2023_source** — Solide (w=0.9, s=0.95) — bien établi dans la littérature ou le design.
- **thing:concrete_co2_alternatives_2023_length_channel** — Solide (w=0.8, s=0.95) — bien établi dans la littérature ou le design.

## Accessibility Warnings

- **color_pair_close:** Les paires de couleurs sont-elles distinguables pour les daltoniens ?
  - Fix: Utilisez des couleurs séparées d'au moins 30° sur la roue chromatique, ou ajoutez des motifs/textures
  - Ref: 8% des hommes sont daltoniens (deutéranopie/protanopie)

- **text_density:** Le GA contient-il plus de 30 mots ?
  - Fix: Réduisez à 30 mots max. Chaque mot supplémentaire active le Système 2 et augmente le temps de décodage
  - Ref: V3 — Budget 30 mots

- **small_details:** Tous les éléments sont-ils lisibles à 50% de la taille originale ?
  - Fix: Agrandissez les éléments critiques. Le GA sera vu en thumbnail 200px dans une TOC — si c'est illisible à 50%, c'est mort
  - Ref: V7 — Lisibilité 50%

## Channel Upgrade Paths

| Current Channel | Upgrade To | Reason | Expected S9b Improvement |
|----------------|-----------|--------|------------------------|
| area | length | Stevens β passe de 0.7 à 1.0 — les différences sont perçues ... | +20-30% sur S9b |
| volume | length | Stevens β passe de 0.6 à 1.0... | +30-40% sur S9b |
| color_saturation | luminance | La luminance est intuitive pour l'incertitude (MacEachren 20... | +15-25% sur la perception de l'incertitude |
| color_hue | length + color_hue | La teinte seule encode des catégories, pas des magnitudes. A... | +10-20% sur S9b |
| no_channel | length | L'information n'est encodée dans aucun canal visuel pré-atte... | De 0% à 60-80% de perception |