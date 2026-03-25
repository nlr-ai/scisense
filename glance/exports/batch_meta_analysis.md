# GLANCE Meta-Analysis — 47 GAs across 15 Domains

*Generated: 2026-03-25 05:54*

*Pipeline: batch_analysis.py → recommender.py*


## Distribution

- **N:** 47
- **Mean:** 0.5934 (sigma=0.0787)
- **Median:** 0.6172
- **Min / Max:** 0.5138 / 0.7441
- **Range:** 0.2303

## By Domain (sorted by mean score)

| Domain | N | Mean | sigma | Best GA | Best Score | Worst GA | Worst Score |
|--------|---|------|-------|---------|-----------|----------|------------|
| tech | 2 | 0.6519 | 0.1304 | attention_transformer_2017 | 0.7441 | attention_transformer_2017_pie_cont | 0.5597 |
| policy | 2 | 0.6245 | 0.1513 | oregon_health_experiment_2012 | 0.7314 | oregon_health_experiment_2012_pie_c | 0.5175 |
| transport | 2 | 0.6027 | 0.1098 | modal_emissions_itf_2021 | 0.6803 | modal_emissions_itf_2021_control | 0.5250 |
| education | 2 | 0.5891 | 0.1065 | hattie_visible_learning_2009 | 0.6644 | hattie_visible_learning_2009_bubble | 0.5138 |
| climate | 2 | 0.5891 | 0.1065 | drawdown_climate_2017 | 0.6644 | drawdown_climate_2017_pie_control | 0.5138 |
| psychology | 6 | 0.5891 | 0.0825 | obedience_milgram_1963 | 0.6644 | obedience_milgram_1963_control | 0.5138 |
| economics | 4 | 0.5891 | 0.0870 | minimum_wage_card_krueger_1994 | 0.6644 | minimum_wage_card_krueger_1994_cont | 0.5138 |
| neuroscience | 4 | 0.5891 | 0.0870 | sleep_memory_walker_2009 | 0.6644 | sleep_memory_walker_2009_control | 0.5138 |
| nutrition | 4 | 0.5891 | 0.0870 | predimed_estruch_2018 | 0.6644 | predimed_estruch_2018_control | 0.5138 |
| energy | 4 | 0.5891 | 0.0870 | battery_energy_density_2023 | 0.6644 | battery_energy_density_2023_control | 0.5138 |
| epidemiology | 4 | 0.5891 | 0.0870 | covid_vaccine_polack_2020 | 0.6644 | covid_vaccine_polack_2020_control | 0.5138 |
| ecology | 4 | 0.5891 | 0.0870 | pollinator_decline_potts_2010 | 0.6644 | pollinator_decline_potts_2010_contr | 0.5138 |
| agriculture | 2 | 0.5891 | 0.1065 | crop_yield_ponisio_2015 | 0.6644 | crop_yield_ponisio_2015_control | 0.5138 |
| materials | 2 | 0.5891 | 0.1065 | concrete_co2_alternatives_2023 | 0.6644 | concrete_co2_alternatives_2023_cont | 0.5138 |
| med | 3 | 0.5827 | 0.0598 | immunomod_v10_wireframe | 0.6172 | immunomod_v10_area_control | 0.5138 |

## VEC vs Control

| Type | N | Mean | sigma | Delta from VEC |
|------|---|------|-------|----------------|
| VEC (length, beta=1.0) | 23 | 0.6694 | 0.0241 | baseline |
| Control (area, beta=0.7) | 23 | 0.5164 | 0.0097 | +0.1530 |
| Mixed/calibration | 1 | 0.6172 | 0.0000 | — |

**VEC-Control delta: +0.1530** — VEC outperforms controls by 0.1530 points.
This confirms Stevens power law: beta=1.0 (length) produces higher graph scores than beta=0.7 (area).

## By Encoding Channel

| Channel | N | Mean Score | sigma | Stevens beta |
|---------|---|-----------|-------|-------------|
| length | 23 | 0.6694 | 0.0241 | 1.0 |
| area | 23 | 0.5164 | 0.0097 | 0.7 |
| mixed | 1 | 0.6172 | 0.0000 | varies |

## Top 10 GAs

| Rank | GA | Domain | Type | Score | N Products |
|------|-----|--------|------|-------|-----------|
| 1 | attention_transformer_2017 | tech | VEC | 0.7441 | 4 |
| 2 | oregon_health_experiment_2012 | policy | VEC | 0.7314 | 4 |
| 3 | modal_emissions_itf_2021 | transport | VEC | 0.6803 | 4 |
| 4 | hattie_visible_learning_2009 | education | VEC | 0.6644 | 4 |
| 5 | drawdown_climate_2017 | climate | VEC | 0.6644 | 4 |
| 6 | obedience_milgram_1963 | psychology | VEC | 0.6644 | 4 |
| 7 | marshmallow_watts_2018 | psychology | VEC | 0.6644 | 4 |
| 8 | cbt_depression_cuijpers_2020 | psychology | VEC | 0.6644 | 4 |
| 9 | minimum_wage_card_krueger_1994 | economics | VEC | 0.6644 | 4 |
| 10 | microfinance_banerjee_2015 | economics | VEC | 0.6644 | 4 |

## Bottom 10 GAs

| Rank | GA | Domain | Type | Score | N Products |
|------|-----|--------|------|-------|-----------|
| 38 | predimed_estruch_2018_control | nutrition | CTRL | 0.5138 | 4 |
| 39 | sugar_tax_teng_2019_control | nutrition | CTRL | 0.5138 | 4 |
| 40 | battery_energy_density_2023_control | energy | CTRL | 0.5138 | 4 |
| 41 | renewable_lcoe_lazard_2023_control | energy | CTRL | 0.5138 | 4 |
| 42 | covid_vaccine_polack_2020_control | epidemiology | CTRL | 0.5138 | 4 |
| 43 | handwashing_aiello_2008_control | epidemiology | CTRL | 0.5138 | 4 |
| 44 | pollinator_decline_potts_2010_control | ecology | CTRL | 0.5138 | 4 |
| 45 | coral_recovery_interventions_2020_contro | ecology | CTRL | 0.5138 | 4 |
| 46 | crop_yield_ponisio_2015_control | agriculture | CTRL | 0.5138 | 4 |
| 47 | concrete_co2_alternatives_2023_control | materials | CTRL | 0.5138 | 4 |

## Most Common Recommendations (frequency table)

| Recommendation | Count | % of GAs |
|---------------|-------|---------|

## Cross-Domain Insights

### Which domains produce better GAs?
- **Best domain:** tech (mean=0.6519, N=2)
- **Worst domain:** med (mean=0.5827, N=3)
- **Domain spread:** 0.0691 between best and worst

### Is there a correlation between N products and score?
- **4 products:** mean=0.5934 (N=47)

### Do controls consistently score lower?
| Domain | VEC Mean | Control Mean | Delta | Consistent? |
|--------|----------|-------------|-------|-------------|
| med | 0.6172 | 0.5138 | +0.1035 | YES |
| tech | 0.7441 | 0.5597 | +0.1844 | YES |
| policy | 0.7314 | 0.5175 | +0.2139 | YES |
| education | 0.6644 | 0.5138 | +0.1506 | YES |
| climate | 0.6644 | 0.5138 | +0.1506 | YES |
| psychology | 0.6644 | 0.5138 | +0.1506 | YES |
| economics | 0.6644 | 0.5138 | +0.1506 | YES |
| neuroscience | 0.6644 | 0.5138 | +0.1506 | YES |
| nutrition | 0.6644 | 0.5138 | +0.1506 | YES |
| energy | 0.6644 | 0.5138 | +0.1506 | YES |
| epidemiology | 0.6644 | 0.5138 | +0.1506 | YES |
| ecology | 0.6644 | 0.5138 | +0.1506 | YES |
| transport | 0.6803 | 0.5250 | +0.1553 | YES |
| agriculture | 0.6644 | 0.5138 | +0.1506 | YES |
| materials | 0.6644 | 0.5138 | +0.1506 | YES |

**Result:** Controls score lower in 15/15 domains (100%).
**Stevens power law confirmed across ALL testable domains.**

---
*Generated by batch_analysis.py — 2026-03-25 05:54*