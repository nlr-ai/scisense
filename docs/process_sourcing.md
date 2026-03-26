# SciSense - Process de Sourcing

> **Workflow complet : Identification → Recherche → Validation → Intégration**
> **Pour les Citoyens (Agents) qui sourcent le contenu**

---

## Objectif

Sourcer = Trouver et vérifier les références qui appuient les affirmations dans nos contenus (posts LinkedIn, articles, PDFs).

**Pourquoi sourcer ?**
- Crédibilité scientifique (SciSense = expertise PhD)
- Différenciation vs concurrents (on prouve ce qu'on dit)
- LinkedIn : sources en commentaire = engagement + autorité
- Éviter les affirmations "dans le vide"

---

## Instructions d'Implémentation pour Agents

### Étape 0 : Lecture du Contexte (OBLIGATOIRE)

Avant toute action, l'agent orchestrateur DOIT lire :

```
1. docs/scisense.md              → Comprendre l'offre SciSense
2. docs/process_sourcing.md      → CE DOCUMENT (comprendre le workflow)
3. Le contenu à sourcer          → Post LinkedIn ou article concerné
```

### Citoyens Disponibles

| Citoyen | Rôle | Quand l'invoquer |
|---------|------|------------------|
| **Sophie** | Scientific Strategist | Recherche sources scientifiques (PubMed, études) |
| **Hugo** | Intelligence Gatherer | Recherche sources business (rapports, press releases) |
| **Léa** | Content Architect | Intégration sources dans le contenu |
| **Marie** | Voice to Market | Rédaction du commentaire LinkedIn avec sources |

### Orchestration Parallèle

```
PHASE IDENTIFICATION (Léa)
     │
     ▼
PHASE RECHERCHE (Sophie + Hugo en parallèle)
     │
     ├── Sophie: Sources scientifiques (PubMed, études cliniques, reviews)
     └── Hugo: Sources business (rapports annuels, press releases, news)
     │
     ▼
PHASE VALIDATION (Sophie)
     │
     └── Vérification qualité et pertinence des sources
     │
     ▼
PHASE INTÉGRATION (Marie + Léa en parallèle)
     │
     ├── Marie: Rédaction commentaire LinkedIn formaté
     └── Léa: Mise à jour du contenu si nécessaire
     │
     ▼
PHASE SYNC (Lucas)
     │
     └── Mise à jour Notion (champs Sources + Commentaire)
```

---

## Types de Sources par Catégorie

### Sources Scientifiques (Sophie)

| Type | Exemples | Crédibilité |
|------|----------|-------------|
| **Publications peer-reviewed** | NEJM, Lancet, JAMA, Nature | ⭐⭐⭐⭐⭐ |
| **Systematic Reviews** | Cochrane, meta-analyses | ⭐⭐⭐⭐⭐ |
| **Guidelines** | FDA, EMA, sociétés savantes | ⭐⭐⭐⭐⭐ |
| **Clinical Trials** | ClinicalTrials.gov, EudraCT | ⭐⭐⭐⭐ |
| **Congrès** | ASCO, ESMO, AACR abstracts | ⭐⭐⭐⭐ |
| **Preprints** | medRxiv, bioRxiv | ⭐⭐⭐ (mentionner "preprint") |

### Sources Business (Hugo)

| Type | Exemples | Crédibilité |
|------|----------|-------------|
| **Rapports annuels** | SEC filings, rapports annuels | ⭐⭐⭐⭐⭐ |
| **Press releases** | PRNewswire, Business Wire | ⭐⭐⭐⭐ |
| **Analystes** | McKinsey, BCG, IQVIA | ⭐⭐⭐⭐ |
| **News pharma** | Endpoints, STAT News, BioPharma Dive | ⭐⭐⭐⭐ |
| **LinkedIn** | Posts officiels entreprises | ⭐⭐⭐ |
| **Communiqués** | Sites corporate des entreprises | ⭐⭐⭐⭐ |

### Sources à Éviter

| Type | Pourquoi |
|------|----------|
| Wikipedia | Pas une source primaire |
| Blogs non-experts | Pas vérifiable |
| Sources sans date | Impossible de vérifier actualité |
| Études < 2020 | Sauf si historique pertinent |
| Sources en accès payant sans abstract | Impossible à vérifier pour le lecteur |

---

## Phase 1 : Identification des Affirmations

### Tâche Léa

Pour chaque contenu à sourcer :

```
1. LIRE le post/article complet
2. IDENTIFIER chaque affirmation factuelle:
   - Chiffres ("40% des...", "€2.2B de ventes")
   - Faits spécifiques ("FDA a approuvé", "essai Phase 3 positif")
   - Tendances ("croissance de +130%")
   - Citations indirectes ("les experts estiment")
3. LISTER les affirmations dans un tableau
4. CATÉGORISER: Scientifique vs Business
```

### Format Output Identification

```markdown
## Post: [Titre du post]

### Affirmations à sourcer

| # | Affirmation | Type | Priorité |
|---|-------------|------|----------|
| 1 | "argenx atteint $2.2B de ventes avec VYVGART" | Business | Haute |
| 2 | "UCB résultats Phase 3 positifs dapirolizumab pegol lupus" | Scientifique | Haute |
| 3 | "42% réduction amyloid-PET SUV" | Scientifique | Haute |
| 4 | "15 indications auto-immunes ciblées" | Business | Moyenne |

### Affirmations OK (opinion/généralité)
- "Les maladies auto-immunes représentent une aire dynamique" → Opinion, pas besoin de source
- "La documentation peut faire ou défaire ces approbations" → Statement général
```

---

## Phase 2 : Recherche (Sophie + Hugo en parallèle)

### Tâche Sophie (Sources Scientifiques)

```
1. LIRE la liste des affirmations scientifiques
2. POUR CHAQUE affirmation:
   a. Rechercher sur PubMed (termes clés + année récente)
   b. Vérifier ClinicalTrials.gov si essai mentionné
   c. Chercher sur sites FDA/EMA si approbation
   d. Vérifier abstracts congrès si récent
3. DOCUMENTER chaque source trouvée:
   - URL complète
   - Titre
   - Auteurs (si pertinent)
   - Date
   - Citation exacte qui confirme l'affirmation
```

### Tâche Hugo (Sources Business)

```
1. LIRE la liste des affirmations business
2. POUR CHAQUE affirmation:
   a. Rechercher rapport annuel/SEC filing de l'entreprise
   b. Chercher press release officielle
   c. Vérifier sur sites news pharma (Endpoints, STAT)
   d. Chercher communiqués sur site corporate
3. DOCUMENTER chaque source trouvée:
   - URL complète
   - Titre
   - Date
   - Citation exacte qui confirme l'affirmation
```

### Format Output Recherche

```markdown
## Sources trouvées - Post #X

### Affirmation 1: "argenx atteint $2.2B de ventes avec VYVGART"
**Type:** Business
**Source trouvée:** ✅
**URL:** https://www.argenx.com/investors/press-releases/...
**Titre:** "argenx Reports Full Year 2024 Financial Results"
**Date:** Février 2025
**Citation:** "VYVGART net product sales reached $2.2 billion for full year 2024"
**Qualité:** ⭐⭐⭐⭐⭐ (Source primaire - rapport officiel)

### Affirmation 2: "UCB résultats Phase 3 positifs dapirolizumab pegol"
**Type:** Scientifique
**Source trouvée:** ✅
**URL:** https://clinicaltrials.gov/study/NCT04294667
**Titre:** "Phase 3 Study of Dapirolizumab Pegol in SLE (PHOENYCS GO)"
**Date:** Résultats 2024
**Publication:** [Si publiée - ajouter référence NEJM/Lancet]
**Citation:** "Primary endpoint met: significant reduction in disease activity"
**Qualité:** ⭐⭐⭐⭐⭐

### Affirmation 3: "[Affirmation]"
**Type:** [Scientifique/Business]
**Source trouvée:** ❌
**Notes:** Impossible de vérifier. Recommandation: reformuler ou supprimer.
```

---

## Phase 3 : Validation (Sophie)

### Checklist Qualité Sources

```
□ Source primaire (pas de citation de citation)
□ Date récente (< 2 ans sauf historique)
□ URL fonctionnelle et accessible
□ Citation exacte vérifiée
□ Source crédible (voir tableau crédibilité)
□ Pas de conflit d'intérêt évident
```

### Classification Finale

| Statut | Action |
|--------|--------|
| ✅ Sourcé | Prêt pour intégration |
| ⚠️ Partiellement sourcé | Reformuler l'affirmation |
| ❌ Non sourcé | Supprimer ou généraliser |

---

## Phase 4 : Intégration (Marie + Léa)

### Tâche Marie (Commentaire LinkedIn)

Format standard du commentaire à poster :

```
📚 Sources de ce post :

• [Affirmation courte 1] : [Nom source] ([année]) - [URL courte ou "lien en réponse"]
• [Affirmation courte 2] : [Nom source] ([année])
• [Affirmation courte 3] : Rapport annuel [Entreprise] 2024

💡 Données vérifiables = crédibilité. N'hésitez pas à checker !
```

**Exemple concret :**

```
📚 Sources de ce post :

• Ventes VYVGART $2.2B : Rapport annuel argenx 2024
• Phase 3 dapirolizumab UCB : ClinicalTrials.gov NCT04294667
• 15 indications VYVGART : Pipeline argenx Q4 2024

Les données citées sont publiques et vérifiables. Questions ? Je réponds en commentaire.
```

### Tâche Léa (Mise à jour contenu)

Si une affirmation n'est pas sourcable :

```
1. Option A: Reformuler en termes plus généraux
   AVANT: "40% des antibiotiques échouent au remboursement"
   APRÈS: "Une proportion significative d'antibiotiques échouent au remboursement"

2. Option B: Supprimer l'affirmation si non essentielle

3. Option C: Ajouter une nuance
   AVANT: "La FDA a approuvé..."
   APRÈS: "Selon les communiqués de [Entreprise], la FDA a approuvé..."
```

---

## Phase 5 : Sync Notion (Lucas)

### Mise à jour des champs

```python
# Pseudo-code pour mise à jour Notion
def update_post_sources(post_id: str, sources: str, commentaire: str):
    notion.pages.update(
        page_id=post_id,
        properties={
            "Sources": {"rich_text": [{"text": {"content": sources}}]},
            "Commentaire": {"rich_text": [{"text": {"content": commentaire}}]}
        }
    )
```

### Format champ "Sources" dans Notion

```
[1] argenx Annual Report 2024 - https://...
[2] ClinicalTrials.gov NCT04294667 - https://...
[3] FDA Press Release Nov 2024 - https://...
```

### Format champ "Commentaire" dans Notion

Le texte exact à copier-coller en premier commentaire LinkedIn.

---

## Workflow Complet - Exemple

### Input : Post B2B #5 "Maladies Auto-Immunes"

**Étape 1 - Léa identifie :**
```
Affirmations à sourcer:
1. "UCB résultats Phase 3 positifs dapirolizumab pegol lupus" → Scientifique
2. "argenx atteint $2.2B de ventes avec VYVGART" → Business
3. "argenx cible 15 indications auto-immunes" → Business
4. "Roche développe evidence generation plans en nephropathie lupique" → Business
```

**Étape 2 - Sophie + Hugo en parallèle :**

Sophie cherche :
- PubMed: "dapirolizumab pegol phase 3 lupus"
- ClinicalTrials.gov: NCT04294667

Hugo cherche :
- argenx investor relations → Q4 2024 earnings
- argenx pipeline page
- Roche annual report 2024

**Étape 3 - Sophie valide :**
```
✅ Affirmation 1: Source trouvée (ClinicalTrials.gov + UCB press release)
✅ Affirmation 2: Source trouvée (argenx earnings report)
✅ Affirmation 3: Source trouvée (argenx pipeline)
⚠️ Affirmation 4: Partiellement sourcé → Reformuler
```

**Étape 4 - Marie rédige commentaire :**
```
📚 Sources de ce post :

• Phase 3 dapirolizumab UCB : ClinicalTrials.gov NCT04294667 + communiqué UCB Nov 2024
• Ventes VYVGART $2.2B : Rapport financier argenx FY2024
• 15 indications VYVGART : Pipeline argenx mis à jour Q4 2024

Toutes les données sont publiques. Questions sur les sources ? 👇
```

**Étape 5 - Lucas sync Notion :**
- Champ Sources ← Liste des URLs
- Champ Commentaire ← Texte du commentaire

---

## Prompts Types par Citoyen

### Pour Léa (Identification)

```
Contexte: Tu es Léa, Content Architect de SciSense.

Mission: Analyser le post LinkedIn suivant et identifier toutes les affirmations
factuelles qui nécessitent une source.

Post à analyser:
[CONTENU DU POST]

Output attendu:
- Tableau des affirmations (numéro, affirmation, type Scientifique/Business, priorité)
- Liste des affirmations qui sont des opinions/généralités (pas besoin de source)
```

### Pour Sophie (Recherche Scientifique)

```
Contexte: Tu es Sophie, Scientific Strategist de SciSense.

Mission: Trouver des sources scientifiques crédibles pour les affirmations suivantes.

Affirmations à sourcer:
[LISTE DES AFFIRMATIONS SCIENTIFIQUES]

Pour chaque affirmation, fournir:
- URL de la source
- Titre complet
- Date de publication
- Citation exacte qui confirme l'affirmation
- Note de qualité (⭐ à ⭐⭐⭐⭐⭐)

Sources prioritaires: PubMed, ClinicalTrials.gov, FDA/EMA, Congrès (ASCO, ESMO, etc.)
```

### Pour Hugo (Recherche Business)

```
Contexte: Tu es Hugo, Intelligence Gatherer de SciSense.

Mission: Trouver des sources business crédibles pour les affirmations suivantes.

Affirmations à sourcer:
[LISTE DES AFFIRMATIONS BUSINESS]

Pour chaque affirmation, fournir:
- URL de la source
- Titre complet
- Date de publication
- Citation exacte qui confirme l'affirmation
- Note de qualité

Sources prioritaires: Rapports annuels, SEC filings, Press releases officielles,
Sites corporate, News pharma (Endpoints, STAT News)
```

### Pour Marie (Commentaire)

```
Contexte: Tu es Marie, Voice to Market de SciSense.

Mission: Rédiger le commentaire LinkedIn qui listera les sources du post.

Sources validées:
[LISTE DES SOURCES AVEC URLs]

Format attendu:
- Emoji 📚 en intro
- Liste à puces des sources (affirmation courte : source + année)
- Phrase de clôture engageante
- Ton: professionnel mais accessible, pas académique
- Longueur: max 500 caractères
```

---

## Métriques

| KPI | Cible | Mesure |
|-----|-------|--------|
| Taux de sourçage | >90% | Affirmations sourcées / Total affirmations |
| Qualité sources | >80% ⭐⭐⭐⭐+ | Sources haute qualité / Total sources |
| Temps par post | <30 min | Temps identification + recherche + intégration |
| Engagement commentaire | +20% vs sans | Likes/réponses sur commentaire sources |

---

## Checklist Orchestrateur

```
□ Contenu à sourcer identifié
□ Léa lancée sur identification des affirmations
□ Sophie + Hugo lancés en parallèle (recherche)
□ Sophie valide la qualité des sources
□ Marie rédige le commentaire LinkedIn
□ Léa met à jour le contenu si nécessaire
□ Lucas sync vers Notion (Sources + Commentaire)
□ Post prêt à publier avec sources
```

---

## Fichiers de Référence

| Fichier | Rôle | Citoyens concernés |
|---------|------|-------------------|
| [`process_sourcing.md`](./process_sourcing.md) | CE DOCUMENT | Tous |
| Posts Notion DB | Contenu à sourcer | Léa, Marie |
| [`notion_sync.py`](../tools/notion_sync.py) | Sync Notion | Lucas |

---

## Quick Reference - Outils de Recherche

### Sophie (Scientifique)

| Outil | URL | Usage |
|-------|-----|-------|
| PubMed | pubmed.ncbi.nlm.nih.gov | Publications médicales |
| ClinicalTrials.gov | clinicaltrials.gov | Essais cliniques |
| FDA Drugs | fda.gov/drugs | Approbations FDA |
| EMA | ema.europa.eu | Approbations EMA |
| Cochrane | cochranelibrary.com | Systematic reviews |

### Hugo (Business)

| Outil | URL | Usage |
|-------|-----|-------|
| SEC EDGAR | sec.gov/edgar | Filings entreprises US |
| Endpoints News | endpts.com | News biotech/pharma |
| STAT News | statnews.com | News santé |
| BioPharma Dive | biopharmadive.com | News industrie |
| Company IR pages | [company].com/investors | Rapports officiels |

---

*SciSense - Making Science Make Sense*
*"Chaque affirmation mérite sa source"*
