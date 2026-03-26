#!/usr/bin/env python3
"""
SciSense - Email Sequences Automation
Remplace Lemlist (économie €60/mois)

Usage:
    # Créer les drafts Gmail pour les emails du jour
    python email_sequences.py --drafts

    # Voir les emails planifiés
    python email_sequences.py --preview

    # Lancer une séquence pour un prospect
    python email_sequences.py --start "Judit Perez Gomez"

    # Marquer un email comme envoyé
    python email_sequences.py --sent <sequence_id>

Prérequis:
    pip install google-auth google-auth-oauthlib google-api-python-client notion-client python-dotenv

Setup Gmail API:
    1. Créer projet Google Cloud Console
    2. Activer Gmail API
    3. Créer credentials OAuth 2.0
    4. Télécharger credentials.json dans tools/
"""

import os
import re
import json
import base64
import argparse
from pathlib import Path
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional

try:
    import requests
    from dotenv import load_dotenv
except ImportError:
    print("Error: pip install requests python-dotenv")
    exit(1)

# Gmail API imports (optional - falls back to SMTP)
GMAIL_API_AVAILABLE = False
try:
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request
    from googleapiclient.discovery import build
    GMAIL_API_AVAILABLE = True
except ImportError:
    pass

load_dotenv(Path(__file__).parent / '.env')

# Configuration
NOTION_TOKEN = os.getenv("NOTION_TOKEN")
NOTION_DB_PROSPECTS = os.getenv("NOTION_DB_PROSPECTS")
NOTION_DB_SEQUENCES = os.getenv("NOTION_DB_SEQUENCES")
SENDER_EMAIL = os.getenv("SENDER_EMAIL", "aurore.inchauspe@scisense.fr")
SENDER_NAME = os.getenv("SENDER_NAME", "Aurore Inchauspé")

# Gmail API scopes
SCOPES = ['https://www.googleapis.com/auth/gmail.compose']


class NotionClient:
    """Simple Notion API client."""

    def __init__(self, token: str):
        self.token = token
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Notion-Version": "2022-06-28",
            "Content-Type": "application/json"
        }
        self.base_url = "https://api.notion.com/v1"

    def query_database(self, database_id: str, filter_obj: dict = None) -> list:
        """Query a Notion database."""
        url = f"{self.base_url}/databases/{database_id}/query"
        body = {}
        if filter_obj:
            body["filter"] = filter_obj

        resp = requests.post(url, headers=self.headers, json=body)
        if resp.status_code != 200:
            print(f"Error querying database: {resp.json()}")
            return []
        return resp.json().get("results", [])

    def create_page(self, database_id: str, properties: dict) -> dict:
        """Create a page in a database."""
        url = f"{self.base_url}/pages"
        body = {
            "parent": {"database_id": database_id},
            "properties": properties
        }
        resp = requests.post(url, headers=self.headers, json=body)
        return resp.json()

    def update_page(self, page_id: str, properties: dict) -> dict:
        """Update a page."""
        url = f"{self.base_url}/pages/{page_id}"
        resp = requests.patch(url, headers=self.headers, json={"properties": properties})
        return resp.json()

    def get_page_content(self, page_id: str) -> str:
        """Get page content (blocks)."""
        url = f"{self.base_url}/blocks/{page_id}/children"
        resp = requests.get(url, headers=self.headers)
        if resp.status_code != 200:
            return ""

        blocks = resp.json().get("results", [])
        content = []
        for block in blocks:
            block_type = block.get("type")
            if block_type == "code":
                texts = block.get("code", {}).get("rich_text", [])
                for t in texts:
                    content.append(t.get("text", {}).get("content", ""))
        return "\n".join(content)


class EmailSequencer:
    """Manages email sequences for prospects."""

    # Email sequence templates by tier
    SEQUENCES = {
        1: [  # Tier 1: VP/Head level - 5 emails
            {"day": 0, "subject": "Introduction - {pain_point}", "template": "tier1_intro"},
            {"day": 5, "subject": "Re: {previous_subject} - Cas client", "template": "tier1_case"},
            {"day": 10, "subject": "Ressource: {pdf_title}", "template": "tier1_pdf"},
            {"day": 15, "subject": "Proposition concrète", "template": "tier1_offer"},
            {"day": 21, "subject": "Dernier message - {company}", "template": "tier1_final"},
        ],
        2: [  # Tier 2: Director level - 4 emails
            {"day": 0, "subject": "Introduction - SciSense", "template": "tier2_intro"},
            {"day": 5, "subject": "Re: Ressource utile", "template": "tier2_resource"},
            {"day": 12, "subject": "Cas client pertinent", "template": "tier2_case"},
            {"day": 18, "subject": "Proposition", "template": "tier2_offer"},
        ],
        3: [  # Tier 3-5: 3 emails
            {"day": 0, "subject": "Introduction - SciSense", "template": "tier3_intro"},
            {"day": 7, "subject": "Re: Ressource", "template": "tier3_resource"},
            {"day": 14, "subject": "Proposition", "template": "tier3_offer"},
        ],
    }

    # Email templates
    TEMPLATES = {
        "tier1_intro": """Bonjour {first_name},

{personalized_hook}

Chez SciSense, nous accompagnons les équipes Medical Affairs sur des enjeux similaires :
• Synthèse rapide de données complexes
• Communication scientifique adaptée par audience
• Support publications et congrès

Seriez-vous disponible pour un échange de 20 minutes cette semaine ou la suivante ?

Bien cordialement,
{sender_name}

---
Aurore Inchauspé, PhD
SciSense - Making Science Make Sense
aurore.inchauspe@scisense.fr | 06.29.89.49.16""",

        "tier1_case": """Bonjour {first_name},

Je me permets de revenir vers vous suite à mon précédent message.

Un cas qui pourrait vous intéresser : nous avons récemment accompagné une équipe Medical Affairs sur {relevant_case}.

Le résultat : {case_result}.

Si cela résonne avec vos enjeux actuels, je serais ravie d'en discuter.

Bien cordialement,
{sender_name}""",

        "tier1_pdf": """Bonjour {first_name},

Je vous partage une ressource qui pourrait vous être utile : {pdf_description}.

[Lien vers le PDF]

N'hésitez pas si vous avez des questions ou si vous souhaitez approfondir certains points.

Bien cordialement,
{sender_name}""",

        "tier1_offer": """Bonjour {first_name},

Suite à mes précédents messages, je souhaitais vous proposer quelque chose de concret.

Pour répondre à {pain_point}, nous proposons :

{offer_description}

Investissement : {price}
Délai : {timeline}

Seriez-vous disponible pour un call de 30 minutes pour en discuter ?
→ Réservez un créneau : calendly.com/aurore-scisense/discovery

Bien cordialement,
{sender_name}""",

        "tier1_final": """Bonjour {first_name},

Je ne souhaite pas encombrer votre boîte mail, ce sera donc mon dernier message.

Si le timing n'est pas le bon actuellement, je comprends parfaitement. N'hésitez pas à revenir vers moi quand le moment sera plus opportun.

En attendant, je reste disponible si vous avez des questions.

Bien cordialement,
{sender_name}""",

        "tier2_intro": """Bonjour {first_name},

Je découvre votre parcours chez {company} et vos responsabilités en {role_area}.

SciSense accompagne les équipes Medical Affairs sur la communication scientifique et la synthèse de données complexes.

Seriez-vous ouvert(e) à un échange de 15 minutes pour explorer d'éventuelles synergies ?

Bien cordialement,
{sender_name}

---
SciSense - Making Science Make Sense""",

        "tier2_resource": """Bonjour {first_name},

Je vous partage une ressource sur {topic} qui pourrait vous intéresser.

{resource_description}

N'hésitez pas si vous avez des questions.

Bien cordialement,
{sender_name}""",

        "tier2_case": """Bonjour {first_name},

Un exemple concret de notre accompagnement : {case_description}.

Si cela correspond à vos besoins, je serais ravie d'en discuter.

Bien cordialement,
{sender_name}""",

        "tier2_offer": """Bonjour {first_name},

Pour répondre aux enjeux de {pain_point}, nous proposons :

{offer_summary}

Disponible pour un call de 20 minutes ?
→ calendly.com/aurore-scisense/discovery

Bien cordialement,
{sender_name}""",

        "tier3_intro": """Bonjour {first_name},

Je me permets de vous contacter suite à votre profil chez {company}.

SciSense accompagne les équipes Medical Affairs sur leurs enjeux de communication scientifique.

Seriez-vous disponible pour un bref échange ?

Bien cordialement,
{sender_name}""",

        "tier3_resource": """Bonjour {first_name},

Je vous partage une ressource qui pourrait vous être utile : {resource}.

N'hésitez pas si vous avez des questions.

Bien cordialement,
{sender_name}""",

        "tier3_offer": """Bonjour {first_name},

Je souhaitais vous proposer un échange pour discuter de vos besoins en Medical Affairs.

Disponible pour un call de 15 minutes ?
→ calendly.com/aurore-scisense/discovery

Bien cordialement,
{sender_name}""",
    }

    def __init__(self):
        self.notion = NotionClient(NOTION_TOKEN)
        self.gmail_service = None
        if GMAIL_API_AVAILABLE:
            self._init_gmail()

    def _init_gmail(self):
        """Initialize Gmail API service."""
        creds = None
        token_path = Path(__file__).parent / 'token.json'
        creds_path = Path(__file__).parent / 'credentials.json'

        if token_path.exists():
            creds = Credentials.from_authorized_user_file(str(token_path), SCOPES)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            elif creds_path.exists():
                flow = InstalledAppFlow.from_client_secrets_file(str(creds_path), SCOPES)
                creds = flow.run_local_server(port=0)
                with open(token_path, 'w') as token:
                    token.write(creds.to_json())
            else:
                print("⚠️  Gmail API: credentials.json not found. Using draft mode only.")
                return

        self.gmail_service = build('gmail', 'v1', credentials=creds)

    def get_prospects(self, tier: int = None, include_content: bool = False) -> list:
        """Get prospects from Notion.

        Args:
            tier: Filter by tier number (1-5)
            include_content: If True, fetch page content (slow, +1 API call per prospect)
        """
        filter_obj = None
        if tier:
            filter_obj = {
                "property": "Tier",
                "select": {"equals": f"Tier {tier}"}
            }

        pages = self.notion.query_database(NOTION_DB_PROSPECTS, filter_obj)
        prospects = []

        for page in pages:
            props = page.get("properties", {})

            # Extract name
            name_prop = props.get("Name", {}).get("title", [])
            name = name_prop[0].get("text", {}).get("content", "") if name_prop else ""

            # Extract other fields
            prospect = {
                "id": page["id"],
                "name": name,
                "first_name": name.split()[0] if name else "",
                "company": self._get_rich_text(props.get("Entreprise", {})),
                "position": self._get_rich_text(props.get("Poste", {})),
                "email": props.get("Email", {}).get("email", ""),
                "linkedin": props.get("LinkedIn", {}).get("url", ""),
                "tier": self._get_select(props.get("Tier", {})),
                "status": self._get_select(props.get("Statut", {})),
                "value": props.get("Valeur", {}).get("number", 0),
            }

            # Get personalized message from page content (optional, slow)
            if include_content:
                prospect["message"] = self.notion.get_page_content(page["id"])
            else:
                prospect["message"] = ""

            prospects.append(prospect)

        return prospects

    def _get_rich_text(self, prop: dict) -> str:
        """Extract rich text value."""
        texts = prop.get("rich_text", [])
        return texts[0].get("text", {}).get("content", "") if texts else ""

    def _get_select(self, prop: dict) -> str:
        """Extract select value."""
        select = prop.get("select", {})
        return select.get("name", "") if select else ""

    def get_pending_sequences(self) -> list:
        """Get sequences that need to be sent today."""
        today = datetime.now().strftime("%Y-%m-%d")

        filter_obj = {
            "and": [
                {"property": "Date prévue", "date": {"on_or_before": today}},
                {"property": "Statut", "select": {"equals": "À faire"}},
                {"property": "Canal", "select": {"equals": "Email"}}
            ]
        }

        return self.notion.query_database(NOTION_DB_SEQUENCES, filter_obj)

    def start_sequence(self, prospect_name: str) -> bool:
        """Start email sequence for a prospect."""
        # Find prospect (with content for personalization)
        prospects = self.get_prospects(include_content=True)
        prospect = next((p for p in prospects if prospect_name.lower() in p["name"].lower()), None)

        if not prospect:
            print(f"❌ Prospect '{prospect_name}' not found")
            return False

        if not prospect.get("email"):
            print(f"❌ No email for {prospect['name']}")
            return False

        # Determine sequence based on tier
        tier_num = int(prospect["tier"].replace("Tier ", "")) if prospect["tier"] else 3
        sequence = self.SEQUENCES.get(tier_num, self.SEQUENCES[3])

        # Create sequence entries in Notion
        start_date = datetime.now()

        for i, step in enumerate(sequence):
            due_date = start_date + timedelta(days=step["day"])

            self.notion.create_page(NOTION_DB_SEQUENCES, {
                "Action": {"title": [{"text": {"content": f"Email {i+1} - {prospect['name']}"}}]},
                "Canal": {"select": {"name": "Email"}},
                "Date prévue": {"date": {"start": due_date.strftime("%Y-%m-%d")}},
                "Statut": {"select": {"name": "À faire"}},
                "Jour": {"number": step["day"]},
                "Notes": {"rich_text": [{"text": {"content": f"Template: {step['template']}\nSubject: {step['subject']}"}}]},
            })

        # Update prospect status
        self.notion.update_page(prospect["id"], {
            "Statut": {"select": {"name": "In Sequence"}}
        })

        print(f"✓ Séquence démarrée pour {prospect['name']} ({len(sequence)} emails)")
        return True

    def render_template(self, template_name: str, prospect: dict, **kwargs) -> str:
        """Render email template with prospect data."""
        template = self.TEMPLATES.get(template_name, "")

        # Default values
        values = {
            "first_name": prospect.get("first_name", ""),
            "company": prospect.get("company", ""),
            "position": prospect.get("position", ""),
            "sender_name": SENDER_NAME,
            "personalized_hook": prospect.get("message", "")[:500] if prospect.get("message") else "",
            "pain_point": "vos enjeux Medical Affairs",
            "role_area": prospect.get("position", "Medical Affairs"),
            "relevant_case": "un projet similaire",
            "case_result": "gain de temps significatif",
            "pdf_description": "notre guide sur la communication scientifique",
            "offer_description": "Un accompagnement personnalisé",
            "price": "Sur devis",
            "timeline": "2-4 semaines",
            "topic": "Medical Affairs",
            "resource_description": "Un document utile",
            "case_description": "un accompagnement réussi",
            "offer_summary": "Notre offre",
            "resource": "une ressource utile",
            **kwargs
        }

        # Replace placeholders
        for key, value in values.items():
            template = template.replace(f"{{{key}}}", str(value))

        return template

    def create_draft(self, to: str, subject: str, body: str) -> Optional[str]:
        """Create Gmail draft."""
        if not self.gmail_service:
            print(f"📧 [DRAFT MODE] To: {to}")
            print(f"   Subject: {subject}")
            print(f"   Body preview: {body[:100]}...")
            return "draft_mode"

        message = MIMEMultipart()
        message['to'] = to
        message['from'] = f"{SENDER_NAME} <{SENDER_EMAIL}>"
        message['subject'] = subject
        message.attach(MIMEText(body, 'plain'))

        raw = base64.urlsafe_b64encode(message.as_bytes()).decode()

        try:
            draft = self.gmail_service.users().drafts().create(
                userId='me',
                body={'message': {'raw': raw}}
            ).execute()
            return draft['id']
        except Exception as e:
            print(f"❌ Error creating draft: {e}")
            return None

    def preview_pending(self):
        """Preview pending emails."""
        sequences = self.get_pending_sequences()

        if not sequences:
            print("✓ Aucun email à envoyer aujourd'hui")
            return

        print(f"\n📧 {len(sequences)} emails à envoyer aujourd'hui:\n")

        for seq in sequences:
            props = seq.get("properties", {})
            action = props.get("Action", {}).get("title", [{}])[0].get("text", {}).get("content", "")
            date = props.get("Date prévue", {}).get("date", {}).get("start", "")
            notes = self._get_rich_text(props.get("Notes", {}))

            print(f"  • {action}")
            print(f"    Date: {date}")
            if notes:
                print(f"    Notes: {notes[:80]}...")
            print()

    def create_today_drafts(self):
        """Create Gmail drafts for today's emails."""
        sequences = self.get_pending_sequences()
        prospects = {p["name"]: p for p in self.get_prospects()}

        if not sequences:
            print("✓ Aucun email à préparer aujourd'hui")
            return

        print(f"\n📧 Création de {len(sequences)} drafts...\n")

        for seq in sequences:
            props = seq.get("properties", {})
            action = props.get("Action", {}).get("title", [{}])[0].get("text", {}).get("content", "")
            notes = self._get_rich_text(props.get("Notes", {}))

            # Extract prospect name from action
            prospect_name = action.replace("Email", "").strip()
            for i in range(1, 6):
                prospect_name = prospect_name.replace(f"{i} -", "").strip()

            prospect = prospects.get(prospect_name, {})

            if not prospect.get("email"):
                print(f"⚠️  Pas d'email pour: {prospect_name}")
                continue

            # Parse template info from notes
            template_name = "tier3_intro"
            subject = "SciSense - Introduction"

            if notes:
                if "Template:" in notes:
                    template_match = re.search(r"Template:\s*(\w+)", notes)
                    if template_match:
                        template_name = template_match.group(1)
                if "Subject:" in notes:
                    subject_match = re.search(r"Subject:\s*(.+?)(?:\n|$)", notes)
                    if subject_match:
                        subject = subject_match.group(1)

            # Render template
            body = self.render_template(template_name, prospect)

            # Personalize subject
            subject = subject.replace("{first_name}", prospect.get("first_name", ""))
            subject = subject.replace("{company}", prospect.get("company", ""))
            subject = subject.replace("{pain_point}", "Medical Affairs")
            subject = subject.replace("{previous_subject}", "SciSense")
            subject = subject.replace("{pdf_title}", "Guide Communication Scientifique")

            # Create draft
            draft_id = self.create_draft(prospect["email"], subject, body)

            if draft_id:
                print(f"✓ Draft créé: {prospect_name} ({prospect['email']})")

                # Update sequence status
                self.notion.update_page(seq["id"], {
                    "Statut": {"select": {"name": "Draft créé"}},
                    "Notes": {"rich_text": [{"text": {"content": f"{notes}\nDraft ID: {draft_id}"}}]}
                })

    def mark_sent(self, sequence_id: str):
        """Mark a sequence email as sent."""
        self.notion.update_page(sequence_id, {
            "Statut": {"select": {"name": "Fait"}},
            "Date faite": {"date": {"start": datetime.now().strftime("%Y-%m-%d")}}
        })
        print(f"✓ Marqué comme envoyé: {sequence_id}")


def main():
    parser = argparse.ArgumentParser(description='SciSense Email Sequences')
    parser.add_argument('--preview', action='store_true', help='Preview pending emails')
    parser.add_argument('--drafts', action='store_true', help='Create Gmail drafts for today')
    parser.add_argument('--start', help='Start sequence for a prospect')
    parser.add_argument('--sent', help='Mark sequence as sent')
    parser.add_argument('--list-prospects', action='store_true', help='List all prospects')

    args = parser.parse_args()

    if not NOTION_TOKEN:
        print("Error: NOTION_TOKEN not set")
        return

    sequencer = EmailSequencer()

    if args.preview:
        sequencer.preview_pending()
    elif args.drafts:
        sequencer.create_today_drafts()
    elif args.start:
        sequencer.start_sequence(args.start)
    elif args.sent:
        sequencer.mark_sent(args.sent)
    elif args.list_prospects:
        prospects = sequencer.get_prospects()
        print(f"\n📋 {len(prospects)} prospects:\n")
        for p in prospects:
            email_status = "✓" if p.get("email") else "✗"
            print(f"  {email_status} {p['name']} ({p['tier']}) - {p['company']}")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
