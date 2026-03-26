# SciSense - Roadmap Automatisation

> **Principe:** Automatiser progressivement, garder le contrôle humain sur les actions sensibles
> **Créé:** 25 novembre 2025

---

## Philosophie d'Automatisation

```
┌─────────────────────────────────────────────────────────────────┐
│                    NIVEAUX D'AUTOMATISATION                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  NIVEAU 1: PRÉPARATION ASSISTÉE                                │
│  "Je prépare, tu valides et exécutes"                          │
│  → Drafts emails, événements calendar, templates               │
│  → Risque: Zéro | Contrôle: Total                              │
│                                                                 │
│  NIVEAU 2: SEMI-AUTOMATISATION                                 │
│  "J'exécute sur ton approbation"                               │
│  → Envoi après validation, séquences avec review               │
│  → Risque: Faible | Contrôle: Élevé                            │
│                                                                 │
│  NIVEAU 3: AUTOMATISATION CONDITIONNELLE                       │
│  "J'exécute selon des règles définies"                         │
│  → Triggers automatiques, workflows                            │
│  → Risque: Moyen | Contrôle: Modéré                            │
│                                                                 │
│  NIVEAU 4: AUTOMATISATION COMPLÈTE                             │
│  "Je gère de A à Z"                                            │
│  → Full autopilot sur certains process                         │
│  → Risque: Élevé | Contrôle: Supervision                       │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Phase 1: Préparation Assistée (Semaine 1-2)

### 1.1 Gmail - Drafts Emails

**Concept:** Créer des brouillons dans Gmail, Aurore les review et clique "Envoyer"

**Comment:**
```
Option A: Google Apps Script
- Script qui crée des drafts via Gmail API
- Input: CSV ou Google Sheet avec prospects
- Output: Brouillons dans Gmail, prêts à envoyer

Option B: Make.com (ex-Integromat)
- Workflow: Google Sheet → Gmail Draft
- Trigger manuel ou scheduled
- Coût: Gratuit (1000 ops/mois)

Option C: Zapier
- Même principe que Make
- Plus simple mais moins flexible
- Coût: Gratuit (100 tasks/mois)
```

**Template de données (Google Sheet):**
| Prospect | Email | Objet | Corps | Statut Draft | Date Envoi |
|----------|-------|-------|-------|--------------|------------|
| Judit Perez Gomez | judit@valneva.com | Communication de crise... | Bonjour Judit... | ☐ Créé | |
| Christophe GREGOIRE | christophe.gregoire@sanofi.com | Différenciation vaccins... | Bonjour Christophe... | ☐ Créé | |

**Script Google Apps Script (exemple):**
```javascript
function createDrafts() {
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('Prospects');
  const data = sheet.getDataRange().getValues();

  // Skip header row
  for (let i = 1; i < data.length; i++) {
    const [prospect, email, subject, body, status] = data[i];

    if (status !== 'Créé' && email) {
      // Créer le draft
      GmailApp.createDraft(email, subject, body);

      // Marquer comme créé
      sheet.getRange(i + 1, 5).setValue('Créé');
      sheet.getRange(i + 1, 6).setValue(new Date());
    }
  }
}
```

**Workflow:**
```
1. Aurore remplit le Google Sheet avec les prospects du jour
2. Lance le script (bouton ou menu custom)
3. Drafts créés dans Gmail
4. Aurore ouvre Gmail, review chaque draft
5. Personnalise si besoin, puis "Envoyer"
6. Met à jour le Sheet (envoyé ✓)
```

---

### 1.2 Google Calendar - Événements de Suivi

**Concept:** Créer automatiquement des rappels/tâches dans le calendrier

**Types d'événements:**
| Type | Quand | Durée | Description |
|------|-------|-------|-------------|
| **Relance LinkedIn** | J+3 après connexion | 15min | "Envoyer DM suivi à [Prospect]" |
| **Relance Email** | J+5 après email | 15min | "Vérifier réponse [Prospect], relancer si besoin" |
| **Call prévu** | Date choisie | 30min | "Call découverte [Prospect] - [Entreprise]" |
| **Review séquence** | Hebdo (vendredi) | 30min | "Analyser KPIs semaine, ajuster séquences" |

**Script Google Apps Script:**
```javascript
function createFollowUpEvents() {
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('Séquences');
  const calendar = CalendarApp.getDefaultCalendar();
  const data = sheet.getDataRange().getValues();

  for (let i = 1; i < data.length; i++) {
    const [prospect, company, action, dueDate, eventCreated] = data[i];

    if (!eventCreated && dueDate) {
      const title = `${action} - ${prospect} (${company})`;
      const startTime = new Date(dueDate);
      startTime.setHours(9, 0, 0); // 9h du matin

      const endTime = new Date(startTime);
      endTime.setMinutes(endTime.getMinutes() + 15);

      calendar.createEvent(title, startTime, endTime, {
        description: `Prospect: ${prospect}\nEntreprise: ${company}\nAction: ${action}`,
        reminders: {useDefault: false, overrides: [{method: 'popup', minutes: 30}]}
      });

      // Marquer comme créé
      sheet.getRange(i + 1, 5).setValue('✓');
    }
  }
}
```

**Google Sheet "Séquences":**
| Prospect | Company | Action | Due Date | Event ✓ |
|----------|---------|--------|----------|---------|
| Judit Perez Gomez | Valneva | Envoyer DM LinkedIn | 2025-12-01 | |
| Judit Perez Gomez | Valneva | Email + PDF | 2025-12-05 | |
| Judit Perez Gomez | Valneva | Appel téléphonique | 2025-12-14 | |

---

### 1.3 LinkedIn - Préparation Messages

**Concept:** Préparer les messages, copier-coller manuellement (LinkedIn n'a pas d'API publique pour les messages)

**Google Sheet "LinkedIn Messages":**
| Prospect | LinkedIn URL | Type | Message | Copié ✓ | Envoyé ✓ |
|----------|--------------|------|---------|---------|----------|
| Judit Perez Gomez | linkedin.com/in/... | Connexion | Judit, suite à notre échange... | ☐ | ☐ |
| Judit Perez Gomez | linkedin.com/in/... | DM J+2 | Merci pour la connexion !... | ☐ | ☐ |

**Extension Chrome (concept):**
```
- Bouton "Copier message" qui copie dans le presse-papier
- Ouvre automatiquement le profil LinkedIn
- Aurore colle et envoie
- Marque comme envoyé dans le Sheet (via extension)
```

**Outils existants (attention ToS):**
- **Dux-Soup**: Semi-auto, risque moyen
- **Expandi**: Full auto, risque élevé
- **Recommandation**: Rester manuel pour LinkedIn

---

### 1.4 Notion/Airtable - CRM Simple

**Structure Notion:**
```
📁 SciSense Prospection
├── 📋 Prospects (Database)
│   ├── Nom
│   ├── Entreprise
│   ├── Poste
│   ├── Tier (1-5)
│   ├── LinkedIn URL
│   ├── Email
│   ├── Statut (Not Started, In Sequence, Call Booked, Proposal, Won, Lost)
│   ├── Dernière action
│   ├── Prochaine action
│   └── Notes
│
├── 📋 Séquences (Database)
│   ├── Prospect (Relation)
│   ├── Étape (1-10)
│   ├── Canal (LinkedIn/Email/Phone)
│   ├── Action
│   ├── Date prévue
│   ├── Date faite
│   └── Résultat
│
├── 📋 Posts LinkedIn (Database)
│   ├── Thème
│   ├── Contenu
│   ├── Prospects mentionnés
│   ├── Date publication prévue
│   ├── Publié ✓
│   └── Engagement (likes, comments)
│
└── 📊 Dashboard
    ├── Prospects par statut
    ├── Actions cette semaine
    └── KPIs
```

**Airtable alternative:**
- Plus puissant pour automations
- Intégrations natives Make/Zapier
- Vues Kanban, Calendar, Gallery

---

## Phase 2: Semi-Automatisation (Semaine 3-6)

### 2.1 Séquences Email Automatisées

**Outil recommandé:** Lemlist ou Instantly

**Concept:**
```
Créer la séquence une fois → Les emails partent automatiquement
MAIS: Review avant chaque envoi OU envoi auto avec possibilité de pause
```

**Séquence type dans Lemlist:**
```
SÉQUENCE: Tier 2 - Product Leads

Email 1 (J0):
  Subject: {{customIntro}} - SciSense
  Body: Template avec variables
  Delay: Envoi immédiat après ajout

Email 2 (J+5):
  Subject: Re: {{previousSubject}}
  Body: Suivi avec PDF attaché
  Condition: Si pas de réponse à Email 1
  Delay: 5 jours

Email 3 (J+12):
  Subject: Cas client {{theirIndustry}}
  Body: Partage de cas pertinent
  Condition: Si pas de réponse à Email 2
  Delay: 7 jours

Email 4 (J+17):
  Subject: Proposition concrète
  Body: Offre avec pricing
  Condition: Si pas de réponse à Email 3
  Delay: 5 jours
```

**Variables personnalisées:**
| Variable | Exemple |
|----------|---------|
| `{{firstName}}` | Judit |
| `{{company}}` | Valneva |
| `{{customIntro}}` | La gestion IXCHIQ |
| `{{painPoint}}` | communication de crise |
| `{{offer}}` | A3 - Competitive Intelligence (€6-8k) |

**Workflow:**
```
1. Importer prospects dans Lemlist (CSV)
2. Assigner à la séquence appropriée
3. Lemlist envoie selon le schedule
4. Aurore reçoit notifications de réponses
5. Réponses = sortie auto de la séquence
6. Review hebdo des métriques
```

---

### 2.2 Calendrier Automatique (Calendly)

**Setup Calendly:**
```
Types de meetings:
├── "Découverte SciSense" (30 min)
│   └── Dispo: Mar-Jeu, 10h-12h et 14h-17h
├── "Suivi projet" (15 min)
│   └── Dispo: Lun-Ven, 9h-18h
└── "Call approfondi" (45 min)
    └── Dispo: Sur demande
```

**Intégrations:**
- Google Calendar (sync auto)
- Gmail (lien dans signature)
- Zoom/Google Meet (création auto)
- Notion (création fiche contact)

**Lien dans emails:**
```
Seriez-vous disponible pour un échange de 30 minutes ?
→ Réservez un créneau ici: calendly.com/aurore-scisense/decouverte
```

---

### 2.3 Notifications & Alertes

**Google Alerts:**
```
Alertes configurées:
- "Valneva" + "Medical Affairs"
- "Sanofi" + "vaccins" + "lancement"
- "Boiron" + "cannabis médical"
- "OM Pharma" + "FDA"
- Chaque prospect Tier 1 (nom)
```

**LinkedIn Sales Navigator Alerts:**
- Changements de poste des prospects
- Nouvelles de leurs entreprises
- Posts des prospects (pour commenter)

**Slack/Email digest:**
```
Digest quotidien 8h:
- Prospects qui ont changé de poste
- News des entreprises cibles
- Rappel: actions du jour
```

---

## Phase 3: Automatisation Conditionnelle (Mois 2-3)

### 3.1 Workflows Make.com

**Workflow 1: Nouveau prospect → Setup complet**
```
Trigger: Nouvelle ligne dans Google Sheet "Prospects"
    ↓
Action 1: Créer fiche dans Notion
    ↓
Action 2: Créer draft email intro dans Gmail
    ↓
Action 3: Créer événements calendar (séquence 21j)
    ↓
Action 4: Ajouter à Lemlist (si email connu)
    ↓
Action 5: Notification Slack "Nouveau prospect ajouté"
```

**Workflow 2: Réponse email → Actions**
```
Trigger: Email reçu de domaine prospect
    ↓
Condition: Sentiment positif?
    ├── OUI → Créer event "Call à booker"
    │         Notification prioritaire
    │         Pause séquence Lemlist
    │
    └── NON → Notification standard
              Marquer "Réponse négative"
```

**Workflow 3: Post LinkedIn → Tracking**
```
Trigger: Heure de publication prévue
    ↓
Action 1: Notification "Publier post #X maintenant"
    ↓
Action 2: (Manuel) Aurore publie
    ↓
Action 3: (24h après) Rappel "Vérifier engagement post #X"
    ↓
Action 4: Aurore entre les stats dans Sheet
```

---

### 3.2 Scoring Automatique des Prospects

**Critères de scoring:**
| Critère | Points |
|---------|--------|
| Tier 1 (VP/Head) | +30 |
| Tier 2 (Product Lead) | +20 |
| Tier 3 (MSL) | +10 |
| A répondu à un email | +25 |
| A accepté connexion LinkedIn | +15 |
| A liké/commenté un post | +20 |
| Entreprise en croissance | +10 |
| Pain point urgent identifié | +15 |
| Budget confirmé | +30 |

**Actions selon score:**
| Score | Statut | Action |
|-------|--------|--------|
| 0-30 | Froid | Séquence standard |
| 31-50 | Tiède | Accélérer séquence |
| 51-70 | Chaud | Priorité appel |
| 71+ | Très chaud | Action immédiate |

---

### 3.3 Templates Dynamiques

**Google Docs + Mail Merge:**
```
Template: Proposition commerciale

Proposition pour {{Company}}
Préparé pour: {{FirstName}} {{LastName}}
Date: {{Date}}

Suite à notre échange du {{CallDate}}, voici ma proposition pour {{PainPoint}}:

Package recommandé: {{Package}}
- {{Service1}}
- {{Service2}}
- {{Service3}}

Investissement: {{Price}}
Délai: {{Timeline}}

[Signature]
```

**Automatisation:**
```
1. Call terminé → Aurore remplit formulaire post-call
2. Make.com génère la proposition (Google Docs)
3. Convertit en PDF
4. Crée draft email avec PDF attaché
5. Notification "Proposition prête à envoyer"
```

---

## Phase 4: Automatisation Avancée (Mois 4+)

### 4.1 CRM Complet (HubSpot Free)

**Pipeline de vente:**
```
[Prospect] → [Contacté] → [Qualifié] → [Call fait] → [Proposition] → [Négociation] → [Gagné/Perdu]
```

**Automations HubSpot:**
- Contact créé → Email de bienvenue
- Pas d'activité 14j → Alerte relance
- Deal gagné → Email onboarding
- Deal perdu → Enquête feedback

### 4.2 Reporting Automatisé

**Dashboard Google Data Studio:**
```
Sources:
- Google Sheets (données prospects)
- Gmail (emails envoyés/reçus)
- Calendar (calls bookés)
- Lemlist (métriques email)

Visualisations:
- Funnel conversion
- Activité par semaine
- Top prospects engagés
- ROI par canal
```

**Rapport hebdo automatique:**
```
Chaque vendredi 17h:
- Génération auto du rapport
- Email à Aurore avec PDF
- Archivage dans Drive
```

### 4.3 IA & Personnalisation

**Concepts futurs:**
| Fonction | Outil | Complexité |
|----------|-------|------------|
| Génération emails personnalisés | GPT-4 API | Moyenne |
| Analyse sentiment réponses | GPT-4 API | Moyenne |
| Suggestion meilleur moment envoi | ML custom | Haute |
| Prédiction probabilité conversion | ML custom | Haute |
| Chatbot qualification leads | Intercom/Drift | Moyenne |

---

## Outils & Coûts

### Stack Recommandé par Phase

**Phase 1 (€0-20/mois):**
| Outil | Usage | Coût |
|-------|-------|------|
| Google Sheets | Base de données | Gratuit |
| Google Apps Script | Automatisations simples | Gratuit |
| Google Calendar | Rappels | Gratuit |
| Gmail | Drafts et envois | Gratuit |
| Notion | CRM simple | Gratuit |

**Phase 2 (€100-150/mois):**
| Outil | Usage | Coût |
|-------|-------|------|
| Lemlist | Séquences email | €60/mois |
| Calendly | Booking | €10/mois |
| LinkedIn Sales Nav | Recherche prospects | €80/mois |
| Make.com | Workflows | Gratuit (1000 ops) |

**Phase 3 (€200-300/mois):**
| Outil | Usage | Coût |
|-------|-------|------|
| Stack Phase 2 | - | €150/mois |
| Make.com Pro | Plus d'automations | €10/mois |
| Slack | Notifications | Gratuit |
| Google Data Studio | Reporting | Gratuit |
| Apollo.io | Enrichissement | €50/mois |

**Phase 4 (€400-600/mois):**
| Outil | Usage | Coût |
|-------|-------|------|
| HubSpot Starter | CRM complet | €20/mois |
| OpenAI API | Personnalisation IA | €50-100/mois |
| Zapier Pro | Automations avancées | €20/mois |
| Reste du stack | - | €200/mois |

---

## Implementation Checklist

### Semaine 1: Setup de base
- [ ] Créer Google Sheet "Prospects Master"
- [ ] Créer Google Sheet "Séquences"
- [ ] Créer Google Sheet "LinkedIn Messages"
- [ ] Écrire script createDrafts()
- [ ] Écrire script createFollowUpEvents()
- [ ] Tester sur 3 prospects

### Semaine 2: Notion + Process
- [ ] Setup Notion workspace
- [ ] Créer database Prospects
- [ ] Créer database Séquences
- [ ] Créer dashboard
- [ ] Importer les 50 prospects
- [ ] Documenter le process

### Semaine 3-4: Email automation
- [ ] Créer compte Lemlist
- [ ] Setup domaine email (SPF, DKIM)
- [ ] Créer séquence Tier 1
- [ ] Créer séquence Tier 2
- [ ] Importer 10 prospects test
- [ ] Analyser résultats

### Semaine 5-6: Workflows
- [ ] Créer compte Make.com
- [ ] Workflow: nouveau prospect
- [ ] Workflow: réponse reçue
- [ ] Setup Calendly
- [ ] Intégrer Calendly + Calendar
- [ ] Setup Google Alerts

### Mois 2+: Optimisation
- [ ] Analyser métriques
- [ ] A/B test messages
- [ ] Ajuster séquences
- [ ] Ajouter scoring
- [ ] Setup reporting
- [ ] Documenter learnings

---

## Scripts Prêts à l'Emploi

### Script 1: Créer tous les drafts Gmail

```javascript
/**
 * SciSense - Création de drafts Gmail
 * À exécuter depuis Google Sheets
 */

function createAllDrafts() {
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('Emails');
  const data = sheet.getDataRange().getValues();
  const headers = data[0];

  // Trouver les indices des colonnes
  const emailCol = headers.indexOf('Email');
  const subjectCol = headers.indexOf('Objet');
  const bodyCol = headers.indexOf('Corps');
  const statusCol = headers.indexOf('Statut');

  let draftsCreated = 0;

  for (let i = 1; i < data.length; i++) {
    const row = data[i];
    const email = row[emailCol];
    const subject = row[subjectCol];
    const body = row[bodyCol];
    const status = row[statusCol];

    // Ne créer que si pas déjà fait et email valide
    if (status !== 'Draft créé' && status !== 'Envoyé' && email && email.includes('@')) {
      try {
        GmailApp.createDraft(email, subject, body);
        sheet.getRange(i + 1, statusCol + 1).setValue('Draft créé');
        sheet.getRange(i + 1, statusCol + 2).setValue(new Date());
        draftsCreated++;
      } catch (e) {
        sheet.getRange(i + 1, statusCol + 1).setValue('Erreur: ' + e.message);
      }
    }
  }

  SpreadsheetApp.getUi().alert(draftsCreated + ' drafts créés dans Gmail !');
}

// Ajouter au menu
function onOpen() {
  SpreadsheetApp.getUi()
    .createMenu('SciSense')
    .addItem('Créer les drafts Gmail', 'createAllDrafts')
    .addItem('Créer les événements Calendar', 'createAllEvents')
    .addToUi();
}
```

### Script 2: Créer les événements Calendar

```javascript
/**
 * SciSense - Création d'événements de suivi
 */

function createAllEvents() {
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('Séquences');
  const calendar = CalendarApp.getDefaultCalendar();
  const data = sheet.getDataRange().getValues();

  let eventsCreated = 0;

  for (let i = 1; i < data.length; i++) {
    const [prospect, company, action, dateStr, created] = data[i];

    if (!created && dateStr) {
      const eventDate = new Date(dateStr);

      // Event à 9h
      eventDate.setHours(9, 0, 0, 0);
      const endDate = new Date(eventDate);
      endDate.setMinutes(15);

      const title = `📋 ${action} - ${prospect}`;
      const description = `
Prospect: ${prospect}
Entreprise: ${company}
Action: ${action}

---
Lien LinkedIn: [À ajouter]
Voir Google Sheet pour détails
      `.trim();

      calendar.createEvent(title, eventDate, endDate, {
        description: description,
        reminders: {
          useDefault: false,
          overrides: [
            {method: 'popup', minutes: 60},
            {method: 'email', minutes: 1440} // 24h avant
          ]
        }
      });

      sheet.getRange(i + 1, 5).setValue('✓');
      eventsCreated++;
    }
  }

  SpreadsheetApp.getUi().alert(eventsCreated + ' événements créés dans Calendar !');
}
```

### Script 3: Générer rapport hebdomadaire

```javascript
/**
 * SciSense - Rapport hebdomadaire automatique
 */

function generateWeeklyReport() {
  const prospectsSheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('Prospects');
  const data = prospectsSheet.getDataRange().getValues();

  // Compter par statut
  const stats = {
    total: data.length - 1,
    notStarted: 0,
    inSequence: 0,
    responded: 0,
    callBooked: 0,
    proposal: 0,
    won: 0,
    lost: 0
  };

  for (let i = 1; i < data.length; i++) {
    const status = data[i][5]; // Colonne Statut
    switch(status) {
      case 'Not Started': stats.notStarted++; break;
      case 'In Sequence': stats.inSequence++; break;
      case 'Responded': stats.responded++; break;
      case 'Call Booked': stats.callBooked++; break;
      case 'Proposal': stats.proposal++; break;
      case 'Won': stats.won++; break;
      case 'Lost': stats.lost++; break;
    }
  }

  // Créer le rapport
  const report = `
📊 RAPPORT HEBDOMADAIRE SCISENSE
${new Date().toLocaleDateString('fr-FR')}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PIPELINE:
• Total prospects: ${stats.total}
• Non démarrés: ${stats.notStarted}
• En séquence: ${stats.inSequence}
• Ont répondu: ${stats.responded}
• Calls bookés: ${stats.callBooked}
• Propositions: ${stats.proposal}
• Gagnés: ${stats.won}
• Perdus: ${stats.lost}

TAUX DE CONVERSION:
• Réponse: ${((stats.responded / stats.inSequence) * 100).toFixed(1)}%
• Call: ${((stats.callBooked / stats.responded) * 100).toFixed(1)}%
• Win: ${((stats.won / stats.proposal) * 100).toFixed(1)}%

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  `.trim();

  // Envoyer par email
  GmailApp.sendEmail(
    'aurore.inchauspe@scisense.fr',
    '📊 Rapport Hebdo SciSense - ' + new Date().toLocaleDateString('fr-FR'),
    report
  );

  return report;
}

// Trigger hebdomadaire (à configurer)
function setupWeeklyTrigger() {
  ScriptApp.newTrigger('generateWeeklyReport')
    .timeBased()
    .everyWeeks(1)
    .onWeekDay(ScriptApp.WeekDay.FRIDAY)
    .atHour(17)
    .create();
}
```

---

## Prochaines Actions

### Immédiat (aujourd'hui)
1. [ ] Créer le Google Sheet "Prospects Master" avec les 50 prospects
2. [ ] Copier les scripts ci-dessus
3. [ ] Tester createDrafts() sur 3 prospects

### Cette semaine
4. [ ] Setup complet Phase 1
5. [ ] Créer le Notion workspace
6. [ ] Lancer premières séquences manuelles

### Semaine prochaine
7. [ ] Analyser résultats
8. [ ] Décider si passer à Lemlist
9. [ ] Setup Make.com si pertinent

---

*Document évolutif - À mettre à jour selon les résultats*
