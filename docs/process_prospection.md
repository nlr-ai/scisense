# SciSense - Process de Prospection

> **Workflow complet : Recherche → Analyse → Stratégie → Exécution**
> **Pour les Citoyens (Agents) qui exécutent ce process**

---

## Instructions d'Implémentation pour Agents

### Étape 0 : Lecture du Contexte (OBLIGATOIRE)

Avant toute action, l'agent orchestrateur DOIT lire dans cet ordre :

```
1. docs/scisense.md              → Comprendre l'offre SciSense
2. docs/process_prospection.md   → CE DOCUMENT (comprendre le workflow)
3. docs/prospect_personas_guide.md → Comprendre les cibles
4. docs/prospects_enriched.md    → Base existante (si applicable)
```

### Citoyens Disponibles

| Citoyen | Rôle | Quand l'invoquer |
|---------|------|------------------|
| **Hugo** | Intelligence Gatherer | Recherche prospects, qualification, enrichissement |
| **Sophie** | Scientific Strategist | Analyse pain points, stratégie, positionnement |
| **Léa** | Content Architect | Création contenu (posts, PDFs, docs) |
| **Marie** | Voice to Market | Messages outreach, séquences, campagnes |
| **Thomas** | Project Manager | Coordination, suivi, client |

### Orchestration Parallèle

```
PHASE RECHERCHE (Hugo seul)
     │
     ▼
PHASE ANALYSE (Hugo + Sophie en parallèle)
     │
     ├── Hugo: Enrichissement données prospects
     └── Sophie: Analyse pain points par segment
     │
     ▼
PHASE STRATÉGIE (Sophie + Marie + Léa en parallèle)
     │
     ├── Sophie: Recommandations packages par prospect
     ├── Marie: Rédaction séquences outreach
     └── Léa: Création posts LinkedIn + PDFs
     │
     ▼
PHASE EXÉCUTION (Marie + Thomas)
     │
     ├── Marie: Lancement campagnes
     └── Thomas: Tracking, coordination
```

### Exemple de Lancement Parallèle

```python
# Pseudo-code pour orchestrateur
async def phase_strategie(prospects_enriched):
    # Lancer les 3 citoyens en parallèle
    tasks = [
        invoke_citizen("sophie", {
            "task": "recommend_packages",
            "input": prospects_enriched,
            "output": "docs/recommendations.md"
        }),
        invoke_citizen("marie", {
            "task": "write_sequences",
            "input": prospects_enriched,
            "output": "docs/outreach_strategy.md"
        }),
        invoke_citizen("lea", {
            "task": "create_content",
            "input": "pain_points_from_sophie",
            "output": ["posts_linkedin.md", "pdfs/"]
        })
    ]
    await asyncio.gather(*tasks)
```

### Prompts Types par Citoyen

**Pour Hugo (Recherche) :**
```
Contexte: Tu es Hugo, Intelligence Gatherer de SciSense.
Lis d'abord: docs/scisense.md, docs/prospect_personas_guide.md

Mission: Identifier et qualifier 50 prospects Medical Affairs en France.

Critères:
- Postes: VP/Head/Director Medical Affairs, Product Lead, MSL
- Industries: Pharma, Biotech, Vaccins
- Géo: France prioritaire

Output attendu: docs/prospects.md au format standard
```

**Pour Sophie (Analyse) :**
```
Contexte: Tu es Sophie, Scientific Strategist de SciSense.
Lis d'abord: docs/scisense.md, docs/prospects.md

Mission: Enrichir chaque prospect avec:
- Contexte entreprise (actualités, lancements, défis)
- Pain points identifiés
- Packages SciSense recommandés
- Scoring Tier (1-5)

Output attendu: docs/prospects_enriched.md avec bloc 💰 OPPORTUNITÉ
```

**Pour Marie (Outreach) :**
```
Contexte: Tu es Marie, Voice to Market de SciSense.
Lis d'abord: docs/scisense.md, docs/prospects_enriched.md

Mission: Créer la stratégie outreach:
- Séquence 21 jours par Tier
- Messages personnalisés par prospect
- Templates email et LinkedIn

Output attendu: docs/outreach_strategy.md
```

**Pour Léa (Contenu) :**
```
Contexte: Tu es Léa, Content Architect de SciSense.
Lis d'abord: docs/scisense.md, docs/prospects_enriched.md (pain points)

Mission: Créer le contenu marketing:
- 10 posts LinkedIn ciblant les pain points
- Outlines pour 6 PDFs lead magnets
- Messages adaptés par persona

Output attendu: Section posts dans outreach_strategy.md + docs/pdfs/
```

---

## Pipeline

```
RECHERCHE          ANALYSE            STRATÉGIE          EXÉCUTION
────────────────────────────────────────────────────────────────────

LinkedIn Export    Enrichissement     Posts LinkedIn     Drafts Gmail
     │             profils                 │             Calendar
     ▼                  │                  ▼                  │
prospects.md       Pain points        Séquences 21j          ▼
     │             identifiés              │             Envois
     ▼                  │                  ▼                  │
50 contacts        Scoring Tier       PDFs support           ▼
qualifiés               │                  │             Tracking
                        ▼                  ▼                  │
                   prospects_         outreach_              ▼
                   enriched.md        strategy.md        Conversion
```

---

## Phase 1 : Recherche

### Sources
| Source | Données | Méthode |
|--------|---------|---------|
| LinkedIn Export | Connexions existantes | Export CSV |
| Sales Navigator | Recherche avancée | Filtres poste/industrie |
| Sites entreprises | Pages équipe | Scraping manuel |
| Congrès | Speakers, participants | Listes publiques |

### Critères de qualification
```
Poste     : Medical Affairs, Scientific Affairs, MSL, Regulatory
Industrie : Pharma, Biotech, Vaccins, Devices
Géo       : France > Belgique > Suisse > UK
Séniorité : Manager+
```

### Output
→ **[`docs/prospects.md`](./prospects.md)** — Liste brute des prospects

---

## Phase 2 : Analyse

### 2.1 Enrichissement par prospect

Pour chaque prospect, rechercher :

| Donnée | Source |
|--------|--------|
| Contexte entreprise | Site web, press releases, actualités |
| Pain points | Poste + contexte marché |
| Parcours | Profil LinkedIn |
| Budget potentiel | Taille entreprise, niveau poste |

### 2.2 Scoring (Tiers)

| Tier | Profil | Budget | Priorité |
|------|--------|--------|----------|
| **1** | VP, Head of | €50k+ | Contact direct, stratégique |
| **2** | Product Lead, Director | €20-50k | Solutions, projets |
| **3** | MSL, Advisor | €10-20k | Collaboratif |
| **4** | Writers, Specialists | €5-10k | Support |
| **5** | Regulatory | €5-15k | Technique |

### 2.3 Opportunité commerciale

Structure par prospect :
```markdown
### 💰 OPPORTUNITÉ COMMERCIALE

| Élément | Détail |
|---------|--------|
| **Packages recommandés** | A3 + B2 + E1 |
| **Offre d'entrée** | A1 - Rapid Review (€3-5k) |
| **Upsell path** | → D2 → E2 retainer |
| **Valeur annuelle** | €XX,XXX |
| **Décideur** | Oui/Non |
| **Cycle vente** | X semaines |
| **Timing** | NOW / Q1 / Attendre |
```

### Packages SciSense (référence)

| Code | Service | Prix |
|------|---------|------|
| A1 | Rapid Review | €3-5k |
| A2 | Systematic Review | €8-12k |
| A3 | Competitive Intelligence | €5-8k |
| B1 | Executive Summary | €1.5-2.5k |
| B2 | White Paper | €3.5-5k |
| C1 | Abstract/Poster | €2-4k |
| C2 | Manuscript | €8-15k |
| D1 | Evidence Gap Analysis | €4-12k |
| D2 | Launch Readiness | €8-18k |
| D3 | MA Strategy | €12-24k |
| E1 | Part-time (2j/sem) | €4-5k/mois |
| E2 | Part-time (3j/sem) | €6-8k/mois |
| F1 | Full-time | €10-15k/mois |

### Output
→ **[`docs/prospects_enriched.md`](./prospects_enriched.md)** — 50 prospects avec contexte, pain points, opportunité commerciale

---

## Phase 3 : Stratégie

### 3.1 Personas

Documenter les archétypes pour adapter le ton :

| Persona | Exemples titres | Approche |
|---------|-----------------|----------|
| MA Head | VP, Head of, Director | ROI, stratégie, partenariat |
| Product Lead | Global Medical Lead | Solutions concrètes, délais |
| MSL | MSL Lead, Medical Advisor | Expertise terrain, HCPs |
| Writer | Medical Writer | Support, qualité |
| Regulatory | RA Director | Compliance, rigueur |

→ **[`docs/prospect_personas_guide.md`](./prospect_personas_guide.md)**

### 3.2 Séquence 21 jours

```
J-7   LinkedIn   Post avec mention prospect
J-5   LinkedIn   Liker/commenter ses posts
J0    LinkedIn   Demande connexion + note
J+2   LinkedIn   Message remerciement
J+5   Email      Introduction + PDF
J+10  Email      Cas client pertinent
J+14  Téléphone  Appel (Tier 1-2)
J+17  Email      Offre concrète + Calendly
J+21  LinkedIn   Message final
```

### 3.3 Contenu à produire

| Type | Volume | Lien pain point |
|------|--------|-----------------|
| Posts LinkedIn | 10 | 1 par pain point majeur |
| Messages connexion | Templates/persona | Personnalisés |
| Emails | 4-5/séquence | Valeur + CTA |
| PDFs | 6 outlines | Lead magnets |

### Pain points → Contenu

| Pain Point | Prospects | Post/PDF |
|------------|-----------|----------|
| Crise sécurité produit | Valneva (1,3), Boiron (7) | Post #1 + PDF Crisis |
| Lancement FDA/EMA | OM Pharma (2,8), Alnylam (9) | Post #2 |
| Scaling équipes MA | Sanofi (11,12,15) | Post #3 |
| Maladies rares | Ipsen (22), Théa (4) | Post #4 |
| Cannabis médical | Boiron (7,10,28-30) | Post #6 + PDF |
| Formation MSL | Alnylam (9), argenx (26) | Post #8 + PDF RNAi |

### Output
→ **[`docs/outreach_strategy.md`](./outreach_strategy.md)** — Séquences, posts, templates, PDFs

---

## Phase 4 : Exécution

### 4.1 Automatisation

| Niveau | Outils | Coût |
|--------|--------|------|
| **Basic** | Google Sheets + Apps Script | €0 |
| **Intermédiaire** | + Lemlist + Calendly | €70/mois |
| **Avancé** | + Make.com + HubSpot | €150+/mois |

### Scripts disponibles

→ **[`tools/markdown_to_pdf.py`](../tools/markdown_to_pdf.py)** — Conversion MD → PDF pro

```bash
# Usage
python3 tools/markdown_to_pdf.py docs/outreach_strategy.md
```

→ **[`docs/automation_roadmap.md`](./automation_roadmap.md)** — Scripts Google Apps Script :
- `createAllDrafts()` — Drafts Gmail depuis Sheet
- `createAllEvents()` — Events Calendar
- `generateWeeklyReport()` — Rapport hebdo

### 4.2 Workflow quotidien

```
MATIN (15-20 min)
├── Gmail : Review + envoi des drafts
├── Calendar : Actions du jour
└── LinkedIn : Messages préparés

HEBDO (1h)
├── Analyser métriques
├── Ajuster messages si besoin
└── Planifier semaine suivante
```

### Output
→ **[`docs/automation_roadmap.md`](./automation_roadmap.md)**
→ **[`docs/automation_onepager.md`](./automation_onepager.md)**

---

## Phase 5 : Export

### Génération PDFs

```bash
# Tous les docs
python3 tools/markdown_to_pdf.py docs/outreach_strategy.md
python3 tools/markdown_to_pdf.py docs/prospects_enriched.md
python3 tools/markdown_to_pdf.py docs/prospect_personas_guide.md
python3 tools/markdown_to_pdf.py docs/automation_onepager.md
```

### PDFs générés
| Fichier | Usage |
|---------|-------|
| `outreach_strategy.pdf` | Référence séquences et contenu |
| `prospects_enriched.pdf` | Base prospects complète |
| `prospect_personas_guide.pdf` | Formation, onboarding |
| `automation_onepager.pdf` | Présentation process |

---

## Arborescence

```
scisense/citizens/
├── docs/
│   ├── scisense.md                  # Docu entreprise
│   ├── prospects.md                 # Liste brute
│   ├── prospects_enriched.md        # Prospects enrichis ⭐
│   ├── prospect_personas_guide.md   # Guide personas
│   ├── outreach_strategy.md         # Stratégie outreach ⭐
│   ├── automation_roadmap.md        # Roadmap auto
│   ├── automation_onepager.md       # Résumé auto
│   ├── next_steps_roadmap.md        # Prochaines étapes
│   ├── process_prospection.md       # CE DOCUMENT
│   └── *.pdf                        # Exports
│
└── tools/
    ├── markdown_to_pdf.py           # Script PDF ⭐
    └── requirements.txt             # Dépendances
```

---

## Métriques

| KPI | Cible | Formule |
|-----|-------|---------|
| Taux connexion LinkedIn | >40% | Acceptées / Demandes |
| Taux réponse | >20% | Réponses / Messages |
| Calls bookés | >8% | Calls / Prospects contactés |
| Conversion | >20% | Clients / Propositions |
| Deal moyen | €15-25k | Valeur / Client |

---

## Quick Start

```bash
# 1. Lire la stratégie
cat docs/outreach_strategy.md

# 2. Générer les PDFs
pip3 install markdown weasyprint pygments
python3 tools/markdown_to_pdf.py docs/outreach_strategy.md

# 3. Configurer l'automatisation
# → Voir docs/automation_roadmap.md pour les scripts
```

---

---

## Implémentation Détaillée par Phase

### Phase 1 : Recherche (Hugo)

**Déclencheur:** Nouvelle campagne prospection demandée

**Étapes Hugo :**
```
1. LIRE docs/scisense.md (comprendre l'offre)
2. LIRE docs/prospect_personas_guide.md (comprendre les cibles)
3. RECHERCHER prospects via:
   - LinkedIn (export connexions ou Sales Navigator)
   - Sites entreprises pharma/biotech
   - Listes congrès (SNIP, DIA, AFCROS)
4. QUALIFIER chaque prospect (critères Tier 1-5)
5. ÉCRIRE docs/prospects.md au format standard
6. NOTIFIER "Phase 1 complète, X prospects qualifiés"
```

**Format output Hugo :**
```markdown
## 1. Prénom NOM
- **Poste:** Titre exact
- **Entreprise:** Nom
- **LinkedIn:** URL
- **Email:** (si disponible)
- **Tier:** X (justification)
```

**Handoff → Sophie + Hugo (parallèle)**

---

### Phase 2 : Analyse (Hugo + Sophie en parallèle)

**Tâche Hugo (enrichissement) :**
```
1. LIRE docs/prospects.md
2. POUR CHAQUE prospect:
   - Rechercher actualités entreprise
   - Identifier lancements/projets récents
   - Noter contexte marché
3. ENRICHIR avec données collectées
```

**Tâche Sophie (analyse stratégique) :**
```
1. LIRE docs/scisense.md (packages disponibles)
2. LIRE docs/prospects.md
3. POUR CHAQUE prospect:
   - Identifier pain points depuis contexte
   - Recommander packages SciSense adaptés
   - Estimer valeur annuelle potentielle
   - Définir stratégie d'approche
4. ÉCRIRE bloc 💰 OPPORTUNITÉ COMMERCIALE
```

**Synchronisation :**
```
Hugo termine enrichissement contexte
        +
Sophie termine analyse packages
        ↓
MERGE → docs/prospects_enriched.md
```

**Handoff → Marie + Léa + Sophie (parallèle)**

---

### Phase 3 : Stratégie (Marie + Léa + Sophie en parallèle)

**Tâche Marie (séquences outreach) :**
```
1. LIRE docs/prospects_enriched.md
2. CRÉER framework séquence 21 jours
3. POUR CHAQUE Tier:
   - Adapter nombre de touches
   - Définir canaux prioritaires
   - Écrire templates messages
4. POUR CHAQUE prospect Tier 1-2:
   - Personnaliser message connexion
   - Personnaliser premier email
5. ÉCRIRE docs/outreach_strategy.md (section séquences)
```

**Tâche Léa (contenu) :**
```
1. LIRE docs/prospects_enriched.md (extraire pain points)
2. GROUPER pain points par thème
3. CRÉER 10 posts LinkedIn:
   - 1 post par pain point majeur
   - Inclure mentions prospects concernés
4. CRÉER outlines PDFs:
   - 1 PDF par thème majeur
   - Structure: problème → solution → CTA
5. ÉCRIRE docs/outreach_strategy.md (section posts + PDFs)
```

**Tâche Sophie (validation) :**
```
1. RELIRE contenu Marie + Léa
2. VALIDER précision scientifique
3. SUGGÉRER ajustements si nécessaire
```

**Merge final → docs/outreach_strategy.md complet**

---

### Phase 4 : Exécution (Marie + Thomas)

**Tâche Marie (lancement) :**
```
1. PRÉPARER Google Sheets avec prospects
2. CONFIGURER séquences (manuel ou Lemlist)
3. PLANIFIER posts LinkedIn (calendrier)
4. LANCER premières séquences (Tier 1 d'abord)
```

**Tâche Thomas (coordination) :**
```
1. TRACKER réponses et engagement
2. METTRE À JOUR statuts prospects
3. COORDONNER calls avec Aurore
4. REPORTER métriques hebdo
```

---

## Gestion des Erreurs

| Situation | Action |
|-----------|--------|
| Prospect sans email | Hugo cherche via Hunter.io ou Apollo |
| Pain point non identifié | Sophie utilise contexte industrie générique |
| Message trop long LinkedIn | Marie coupe à 300 caractères |
| Prospect déjà contacté | Thomas vérifie CRM avant lancement |
| Pas de réponse après séquence | Marie passe au Tier suivant |

---

## Checklist Orchestrateur

```
□ Lecture contexte complète (4 docs)
□ Hugo lancé sur recherche
□ Hugo + Sophie lancés en parallèle (enrichissement)
□ Marie + Léa + Sophie lancés en parallèle (stratégie)
□ Merge des outputs vérifié
□ PDFs générés (tools/markdown_to_pdf.py)
□ Marie + Thomas lancés (exécution)
□ Métriques trackées
```

---

## Fichiers de Référence

| Fichier | Rôle | Citoyens concernés |
|---------|------|-------------------|
| [`scisense.md`](./scisense.md) | Contexte entreprise | Tous |
| [`prospect_personas_guide.md`](./prospect_personas_guide.md) | Définition cibles | Hugo, Marie |
| [`prospects.md`](./prospects.md) | Liste brute | Hugo → Sophie |
| [`prospects_enriched.md`](./prospects_enriched.md) | Prospects complets | Sophie → Marie, Léa |
| [`outreach_strategy.md`](./outreach_strategy.md) | Stratégie finale | Marie, Léa → Thomas |
| [`automation_roadmap.md`](./automation_roadmap.md) | Scripts auto | Thomas, Marie |
| [`markdown_to_pdf.py`](../tools/markdown_to_pdf.py) | Export PDF | Léa |

---

## Liens Citoyens

| Citoyen | CLAUDE.md |
|---------|-----------|
| Hugo | [`citizens/hugo/CLAUDE.md`](../citizens/hugo/CLAUDE.md) |
| Sophie | [`citizens/sophie/CLAUDE.md`](../citizens/sophie/CLAUDE.md) |
| Léa | [`citizens/lea/CLAUDE.md`](../citizens/lea/CLAUDE.md) |
| Marie | [`citizens/marie/CLAUDE.md`](../citizens/marie/CLAUDE.md) |
| Thomas | [`citizens/thomas/CLAUDE.md`](../citizens/thomas/CLAUDE.md) |

---

*SciSense - Making Science Make Sense*
