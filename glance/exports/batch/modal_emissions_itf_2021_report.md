# GLANCE GA Analysis Report

**Overall Score:** 0.69
**Nodes:** 8 | **Links:** 13

## Recommendations (prioritized)

### 1. [MEDIUM] hierarchy_clarity
**Problème:** Hierarchy clarity is low (0.26/1.0) — correct answer not prominently positioned
**Fix:** Place the correct/best product first in the visual hierarchy. Use visual prominence (position, size, color) to guide attention.
**Impact:** Expected +10-15% improvement on S9b.

## Strengths

- **encoding_channel** — Length encoding (beta=1.0) — optimal quantitative channel. Perceived magnitude matches actual magnitude with no compression.
- **semantic_depth** — Rich semantic references (0.75/1.0) — supports accurate S9a comprehension measurement.
- **space:modal_emissions_itf_2021_domain** — Solide (w=0.7750138888888889, s=0.8200000000000001) — bien établi dans la littérature ou le design.
- **thing:modal_emissions_itf_2021_car** — Solide (w=0.663, s=0.894) — bien établi dans la littérature ou le design.
- **thing:modal_emissions_itf_2021_bus** — Solide (w=0.603, s=0.884) — bien établi dans la littérature ou le design.
- **thing:modal_emissions_itf_2021_bicycle** — Solide (w=0.876, s=0.938) — bien établi dans la littérature ou le design.
- **narrative:modal_emissions_itf_2021_comparison** — Solide (w=0.9250138888888889, s=0.921) — bien établi dans la littérature ou le design.
- **moment:modal_emissions_itf_2021_source** — Solide (w=0.9, s=0.95) — bien établi dans la littérature ou le design.
- **thing:modal_emissions_itf_2021_length_channel** — Solide (w=0.8, s=0.95) — bien établi dans la littérature ou le design.

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