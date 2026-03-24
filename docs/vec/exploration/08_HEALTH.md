# HEALTH — vec/exploration

**Module:** vec/exploration — Agents autonomes paralleles

---

## Guarantee Loop

```
RESULT: Findings actionnables integres, pas de blind spot dans le design
  -> SENSE: Agent results integres ou dismisses avec justification
    -> HEALTH: Aucun probleme identifie par >1 agent reste sans reponse
      -> CARRIER: Silas (sub-agents)
```

---

## Signals

### HE1: Couverture de la taxonomie

| Signal | Description | Methode | Seuil |
|--------|------------|---------|-------|
| HE1a | Angles couverts dans les 2 dernieres iterations | Comptage dans les bilans de cloture | >= 4/6 angles couverts |
| HE1b | Angles jamais couverts depuis le debut du projet | Scan des bilans historiques | 0 (chaque angle doit avoir ete couvert au moins 1 fois) |

**CARRIER:** Silas — verifie au moment de chaque transition de phase (CONCEPT -> COMPILATION -> AUDIT -> VALIDATION).

---

### HE2: Findings resolus

| Signal | Description | Methode | Seuil |
|--------|------------|---------|-------|
| HE2a | Findings identifie par >1 agent sans reponse | Scan du bilan de cloture | 0 (zero tolere) |
| HE2b | Conflits non resolus en fin de cycle | Scan du bilan de cloture | 0 |
| HE2c | Cycles en fuite (pas de bilan de cloture) | Scan des notes de session | 0 |

**CARRIER:** Silas — verifie a la cloture de chaque cycle d'exploration.

**Ce signal est le coeur de la Guarantee Loop.** Si HE2a > 0, le module est en echec. Un probleme identifie par plusieurs agents independants est un signal fort — l'ignorer est une faille architecturale.

---

### HE3: Qualite des prompts

| Signal | Description | Methode | Seuil |
|--------|------------|---------|-------|
| HE3a | Agents qui retournent du bruit (>50% du deliverable non-actionnable) | Evaluation post-integration | 0 |
| HE3b | Agents qui sortent de leur angle | Evaluation post-integration | 0 |
| HE3c | Agents dont le deliverable ne respecte pas le format demande | Evaluation post-integration | 0 |

**CARRIER:** Silas — evalue apres chaque integration (AE2).

Un agent bruyant est un prompt mal calibre. Si HE3a, HE3b, ou HE3c > 0, la correction n'est pas de changer d'agent — c'est de retravailler le prompt (EP3). Le prompt est la variable, pas l'agent.

---

### HE4: Rendements decroissants

| Signal | Description | Methode | Seuil |
|--------|------------|---------|-------|
| HE4a | Findings uniques par agent (non-redondants) | Comptage post-deduplication | >= 1 par agent |
| HE4b | Ratio findings retenus / findings totaux | Comptage post-integration | >= 30% |

**CARRIER:** Silas — evalue apres chaque integration.

Si HE4a < 1 pour un agent, cet agent n'a rien apporte que les autres n'aient deja dit. Si HE4b < 30%, les prompts produisent trop de bruit. Les deux signalent un probleme de calibration des angles ou des prompts, pas un probleme du module.

---

## Dashboard

A chaque cloture de cycle, Silas produit un micro-bilan:

```
EXPLORATION CYCLE [N] — [date]
Declencheur: [EP8 trigger]
Mode: [FG/BG]
Agents: [nombre] ([angles])
Findings extraits: [nombre total] / [nombre retenus]
Conflits: [nombre detectes] / [nombre resolus]
Findings >1 agent non resolus: [nombre] (DOIT ETRE 0)
Cycles en fuite: [nombre] (DOIT ETRE 0)
Statut: PASS / FAIL
```

Ce bilan est la HEALTH du module. S'il dit PASS, la Guarantee Loop est fermee pour ce cycle. S'il dit FAIL, le cycle reste ouvert et les violations sont documentees.
