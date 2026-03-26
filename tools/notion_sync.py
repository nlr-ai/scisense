#!/usr/bin/env python3
"""
SciSense - Notion Sync Tool
Synchronise les données prospects et séquences vers Notion

Usage:
    python notion_sync.py --prospects docs/prospects_enriched.md
    python notion_sync.py --posts docs/outreach_strategy.md
    python notion_sync.py --all

Setup:
    1. Créer une intégration Notion: https://www.notion.so/my-integrations
    2. Copier le token dans .env ou variable d'environnement
    3. Partager les databases avec l'intégration
    4. Copier les database IDs

Requirements:
    pip install notion-client python-dotenv
"""

import os
import re
import argparse
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional

try:
    from notion_client import Client
    from dotenv import load_dotenv
except ImportError:
    print("Error: Install dependencies with: pip install notion-client python-dotenv")
    exit(1)

load_dotenv()

# Configuration
NOTION_TOKEN = os.getenv("NOTION_TOKEN")
DATABASE_IDS = {
    "prospects": os.getenv("NOTION_DB_PROSPECTS"),
    "entreprises": os.getenv("NOTION_DB_ENTREPRISES"),
    "sequences": os.getenv("NOTION_DB_SEQUENCES"),
    "posts": os.getenv("NOTION_DB_POSTS"),
}


class NotionSync:
    def __init__(self, token: str):
        self.client = Client(auth=token)

    # =========================================================================
    # PROSPECTS
    # =========================================================================

    def parse_prospects_md(self, filepath: str) -> list[dict]:
        """Parse prospects_enriched.md into structured data."""
        content = Path(filepath).read_text(encoding='utf-8')
        prospects = []

        # Find all TIER sections and their prospect ranges
        tier_sections = re.findall(r'## TIER (\d+):', content)

        # Split by prospect (### N. Prénom NOM)
        prospect_pattern = r'\n### (\d+)\.'
        matches = list(re.finditer(prospect_pattern, content))

        for i, match in enumerate(matches):
            prospect_num = int(match.group(1))
            start = match.end()
            end = matches[i + 1].start() if i + 1 < len(matches) else len(content)
            block = content[start:end]

            # Determine tier based on prospect number
            tier = self._get_tier_by_number(prospect_num)

            prospect = self._parse_prospect_block(block, prospect_num, tier)
            if prospect:
                prospects.append(prospect)

        return prospects

    def _get_tier_by_number(self, num: int) -> int:
        """Determine tier based on prospect number."""
        if num <= 10:
            return 1
        elif num <= 22:
            return 2
        elif num <= 32:
            return 3
        elif num <= 40:
            return 4
        else:
            return 5

    def _parse_prospect_block(self, block: str, index: int, tier: int = 3) -> Optional[dict]:
        """Parse a single prospect block."""
        lines = block.strip().split('\n')
        if not lines:
            return None

        # Extract name from first line
        name = lines[0].strip()

        # Extract fields - handle table format: | **Field** | Value |
        prospect = {
            "index": index,
            "name": name,
            "position": self._extract_table_field(block, "Position"),
            "company": self._extract_table_field(block, "Company") or
                       self._extract_table_field(block, "Entreprise"),
            "linkedin": self._extract_linkedin(block),
            "email": self._extract_field(block, r'\*\*Email\*\*[:\|]\s*([^\s\|]+@[^\s\|]+)'),
            "priority": self._extract_stars(block),
            "tier": tier,
            "pain_points": self._extract_pain_points(block),
            "packages": self._extract_packages(block),
            "estimated_value": self._extract_value(block),
            "message": self._extract_message(block),
        }

        return prospect

    def _extract_field(self, text: str, pattern: str) -> Optional[str]:
        """Extract a field using regex."""
        match = re.search(pattern, text, re.IGNORECASE)
        return match.group(1).strip() if match else None

    def _extract_table_field(self, text: str, field_name: str) -> Optional[str]:
        """Extract field from markdown table format: | **Field** | Value |"""
        pattern = rf'\|\s*\*\*{field_name}\*\*\s*\|\s*([^|]+)\s*\|'
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            value = match.group(1).strip()
            # Clean up any trailing whitespace or newlines
            return value if value else None
        return None

    def _extract_linkedin(self, text: str) -> Optional[str]:
        """Extract LinkedIn URL from various formats."""
        # Try markdown link format: [Profile](url)
        match = re.search(r'\*\*LinkedIn\*\*\s*\|\s*\[.*?\]\(([^)]+)\)', text)
        if match:
            return match.group(1).strip()
        # Try direct URL format
        match = re.search(r'\*\*LinkedIn\*\*[:\|]\s*(https?://[^\s\|\)]+)', text)
        if match:
            return match.group(1).strip()
        return None

    def _extract_stars(self, text: str) -> int:
        """Extract priority from stars (★)."""
        match = re.search(r'(★+)', text)
        return len(match.group(1)) if match else 3

    def _extract_tier(self, text: str) -> int:
        """Extract tier number."""
        match = re.search(r'TIER\s*(\d)', text, re.IGNORECASE)
        return int(match.group(1)) if match else 3

    def _extract_pain_points(self, text: str) -> list[str]:
        """Extract pain points list."""
        pain_points = []
        match = re.search(r'\*\*Pain Points.*?\*\*:?\s*([\s\S]*?)(?=\n\*\*|\n###|\n\||\Z)', text)
        if match:
            items = re.findall(r'[-•]\s*(.+)', match.group(1))
            pain_points = [item.strip() for item in items[:5]]
        return pain_points

    def _extract_packages(self, text: str) -> list[str]:
        """Extract recommended packages from table format."""
        # Try table format first: | **Recommended Packages** | ... |
        match = re.search(r'\*\*Recommended Packages?\*\*\s*\|\s*([^|]+)', text, re.IGNORECASE)
        if match:
            packages = re.findall(r'[A-Z]\d', match.group(1))
            return packages
        # Fallback to old format
        match = re.search(r'\*\*(?:Recommended )?Packages?\*\*[:\|]\s*([A-Z0-9,\s\+\-\(\)]+)', text, re.IGNORECASE)
        if match:
            packages = re.findall(r'[A-Z]\d', match.group(1))
            return packages
        return []

    def _extract_value(self, text: str) -> Optional[int]:
        """Extract estimated annual value - takes the midpoint of range."""
        # Try to find: €40,000 - €80,000 format
        match = re.search(r'Estimated Annual Value\*\*\s*\|\s*€?([\d,\.]+)\s*-?\s*€?([\d,\.]+)?', text, re.IGNORECASE)
        if match:
            low_str = match.group(1).replace(',', '').replace('.', '')
            high_str = match.group(2).replace(',', '').replace('.', '') if match.group(2) else low_str
            try:
                low = int(low_str)
                high = int(high_str)
                return (low + high) // 2  # Return midpoint
            except ValueError:
                pass
        # Fallback: any €XX,XXX format
        match = re.search(r'€\s*([\d,\.]+)', text, re.IGNORECASE)
        if match:
            value_str = match.group(1).replace(',', '').replace('.', '')
            try:
                return int(value_str)
            except ValueError:
                pass
        return None

    def _extract_message(self, text: str) -> Optional[str]:
        """Extract personalized message."""
        match = re.search(r'```\n(Bonjour.*?)```', text, re.DOTALL)
        return match.group(1).strip() if match else None

    def sync_prospects(self, prospects: list[dict], database_id: str):
        """Sync prospects to Notion database."""
        print(f"Syncing {len(prospects)} prospects to Notion...")

        for prospect in prospects:
            self._create_or_update_prospect(prospect, database_id)
            print(f"  ✓ {prospect['name']}")

        print(f"Done! {len(prospects)} prospects synced.")

    def _create_or_update_prospect(self, prospect: dict, database_id: str):
        """Create or update a prospect in Notion."""
        # Match existing Notion database schema
        properties = {
            "Name": {"title": [{"text": {"content": prospect["name"]}}]},
            "Poste": {"rich_text": [{"text": {"content": prospect["position"] or ""}}]},
            "Entreprise": {"rich_text": [{"text": {"content": prospect["company"] or ""}}]},
            "Tier": {"select": {"name": f"Tier {prospect['tier']}"}},
            "Statut": {"select": {"name": "Not Started"}},
        }

        if prospect["linkedin"]:
            properties["LinkedIn"] = {"url": prospect["linkedin"]}

        if prospect["estimated_value"]:
            properties["Valeur"] = {"number": prospect["estimated_value"]}

        # Create page with enriched content
        children = []

        # Add metadata section
        meta_lines = []
        if prospect.get("email"):
            meta_lines.append(f"📧 Email: {prospect['email']}")
        if prospect.get("priority"):
            meta_lines.append(f"⭐ Priorité: {'★' * prospect['priority']}")
        if prospect.get("packages"):
            meta_lines.append(f"📦 Packages: {', '.join(prospect['packages'])}")

        if meta_lines:
            children.append({
                "object": "block",
                "type": "callout",
                "callout": {
                    "rich_text": [{"text": {"content": "\n".join(meta_lines)}}],
                    "icon": {"emoji": "📋"}
                }
            })

        # Add pain points
        if prospect.get("pain_points"):
            children.append({
                "object": "block",
                "type": "heading_3",
                "heading_3": {
                    "rich_text": [{"text": {"content": "Pain Points identifiés"}}]
                }
            })
            for pp in prospect["pain_points"]:
                children.append({
                    "object": "block",
                    "type": "bulleted_list_item",
                    "bulleted_list_item": {
                        "rich_text": [{"text": {"content": pp}}]
                    }
                })

        # Add personalized message
        if prospect["message"]:
            children.append({
                "object": "block",
                "type": "heading_3",
                "heading_3": {
                    "rich_text": [{"text": {"content": "Message personnalisé"}}]
                }
            })
            children.append({
                "object": "block",
                "type": "code",
                "code": {
                    "rich_text": [{"text": {"content": prospect["message"]}}],
                    "language": "plain text"
                }
            })

        self.client.pages.create(
            parent={"database_id": database_id},
            properties=properties,
            children=children
        )

    # =========================================================================
    # SEQUENCES
    # =========================================================================

    def create_sequences_for_prospect(self, prospect_page_id: str, prospect_name: str,
                                       tier: int, database_id: str):
        """Create sequence actions for a prospect."""

        # Sequence based on tier
        sequences = {
            1: [  # Tier 1: 10 touches
                (0, "LinkedIn", "Demande connexion"),
                (2, "LinkedIn", "Message remerciement"),
                (5, "Email", "Introduction + PDF"),
                (7, "LinkedIn", "Commenter post"),
                (10, "Email", "Cas client"),
                (12, "LinkedIn", "Partager contenu"),
                (14, "Téléphone", "Appel"),
                (17, "Email", "Offre concrète"),
                (19, "LinkedIn", "Relance"),
                (21, "LinkedIn", "Message final"),
            ],
            2: [  # Tier 2: 8 touches
                (0, "LinkedIn", "Demande connexion"),
                (2, "LinkedIn", "Message remerciement"),
                (5, "Email", "Introduction + PDF"),
                (10, "Email", "Cas client"),
                (14, "Téléphone", "Appel"),
                (17, "Email", "Offre concrète"),
                (21, "LinkedIn", "Message final"),
            ],
            3: [  # Tier 3: 6 touches
                (0, "LinkedIn", "Demande connexion"),
                (3, "LinkedIn", "Message"),
                (7, "Email", "Introduction"),
                (14, "Email", "Relance"),
                (21, "Email", "Offre"),
            ],
        }

        tier_sequence = sequences.get(tier, sequences[3])
        start_date = datetime.now()

        for day_offset, channel, action in tier_sequence:
            due_date = start_date + timedelta(days=day_offset)

            self.client.pages.create(
                parent={"database_id": database_id},
                properties={
                    "Action": {"title": [{"text": {"content": f"{action} - {prospect_name}"}}]},
                    "Prospect": {"relation": [{"id": prospect_page_id}]},
                    "Canal": {"select": {"name": channel}},
                    "Date prévue": {"date": {"start": due_date.strftime("%Y-%m-%d")}},
                    "Statut": {"select": {"name": "À faire"}},
                    "Jour": {"number": day_offset},
                }
            )

    # =========================================================================
    # POSTS LINKEDIN
    # =========================================================================

    def parse_posts_md(self, filepath: str) -> list[dict]:
        """Parse LinkedIn posts from outreach_strategy.md."""
        content = Path(filepath).read_text(encoding='utf-8')
        posts = []

        # Find post blocks with target (updated pattern to capture Sources and Commentaire if present)
        post_pattern = r'### Post #(\d+)[:\s]+(.+?)\n+\*\*Cible:\*\*\s*(.+?)\n+```\n([\s\S]*?)```'
        post_blocks = re.findall(post_pattern, content)

        for num, title, target, text in post_blocks:
            # Extract theme from title (e.g., "Gestion de Crise Sécurité Produit" -> "Crise")
            title_clean = title.strip()
            theme = self._extract_theme(title_clean)

            posts.append({
                "number": int(num),
                "title": title_clean,
                "theme": theme,
                "target": target.strip()[:100],  # Limit to 100 chars for rich_text
                "content": text.strip(),
                "sources": "",  # To be filled manually in Notion
                "commentaire": "",  # To be filled manually in Notion
            })

        return posts

    def _extract_theme(self, title: str) -> str:
        """Extract theme from post title."""
        theme_map = {
            "crise": "Crise",
            "launch": "Launch",
            "lancement": "Launch",
            "ia": "IA",
            "ai": "IA",
            "msl": "MSL",
            "kol": "KOL",
            "publication": "Publication",
            "evidence": "Evidence",
            "team": "Équipe",
            "équipe": "Équipe",
            "communication": "Communication",
            "strateg": "Stratégie",
        }
        title_lower = title.lower()
        for key, theme in theme_map.items():
            if key in title_lower:
                return theme
        return "Général"

    def sync_posts(self, posts: list[dict], database_id: str):
        """Sync LinkedIn posts to Notion."""
        print(f"Syncing {len(posts)} posts to Notion...")

        start_date = datetime.now()

        for i, post in enumerate(posts):
            # Schedule posts every 2-3 days
            pub_date = start_date + timedelta(days=i * 3)

            self.client.pages.create(
                parent={"database_id": database_id},
                properties={
                    "Post": {"title": [{"text": {"content": f"#{post['number']} - {post['title']}"}}]},
                    "Date prévue": {"date": {"start": pub_date.strftime("%Y-%m-%d")}},
                    "Statut": {"select": {"name": "À publier"}},
                    "Thème": {"select": {"name": post.get('theme', 'Général')}},
                    "Cible": {"rich_text": [{"text": {"content": post.get('target', '')}}]},
                    "Sources": {"rich_text": [{"text": {"content": post.get('sources', '')}}]},
                    "Commentaire": {"rich_text": [{"text": {"content": post.get('commentaire', '')}}]},
                },
                children=[
                    {
                        "object": "block",
                        "type": "paragraph",
                        "paragraph": {
                            "rich_text": [{"text": {"content": post["content"][:2000]}}]
                        }
                    }
                ]
            )
            print(f"  ✓ Post #{post['number']}")

        print(f"Done! {len(posts)} posts synced.")


class DocumentSync:
    """Sync markdown documents to Notion pages."""

    def __init__(self, token: str, parent_page_id: str):
        self.client = Client(auth=token)
        self.parent_page_id = parent_page_id

    def markdown_to_blocks(self, content: str) -> list[dict]:
        """Convert markdown content to Notion blocks."""
        blocks = []
        lines = content.split('\n')
        i = 0

        while i < len(lines):
            line = lines[i]

            # Skip empty lines
            if not line.strip():
                i += 1
                continue

            # Headers
            if line.startswith('# '):
                blocks.append(self._heading_block(1, line[2:].strip()))
            elif line.startswith('## '):
                blocks.append(self._heading_block(2, line[3:].strip()))
            elif line.startswith('### '):
                blocks.append(self._heading_block(3, line[4:].strip()))

            # Code blocks
            elif line.startswith('```'):
                code_lines = []
                lang = line[3:].strip() or "plain text"
                i += 1
                while i < len(lines) and not lines[i].startswith('```'):
                    code_lines.append(lines[i])
                    i += 1
                blocks.append(self._code_block('\n'.join(code_lines), lang))

            # Blockquotes
            elif line.startswith('> '):
                quote_text = line[2:].strip()
                blocks.append(self._quote_block(quote_text))

            # Bullet lists
            elif line.startswith('- ') or line.startswith('* '):
                blocks.append(self._bullet_block(line[2:].strip()))

            # Numbered lists
            elif re.match(r'^\d+\.\s', line):
                text = re.sub(r'^\d+\.\s', '', line).strip()
                blocks.append(self._numbered_block(text))

            # Tables (simplified - as callout)
            elif line.startswith('|'):
                table_lines = [line]
                i += 1
                while i < len(lines) and lines[i].startswith('|'):
                    table_lines.append(lines[i])
                    i += 1
                i -= 1  # Adjust for the outer loop increment
                # Convert table to text
                table_text = '\n'.join(table_lines)
                blocks.append(self._callout_block(table_text, "📊"))

            # Horizontal rule
            elif line.strip() in ['---', '***', '___']:
                blocks.append({"object": "block", "type": "divider", "divider": {}})

            # Regular paragraph
            else:
                # Combine consecutive paragraph lines
                para_lines = [line]
                while i + 1 < len(lines) and lines[i + 1].strip() and \
                      not lines[i + 1].startswith(('#', '-', '*', '>', '|', '```', '1.')):
                    i += 1
                    para_lines.append(lines[i])
                text = ' '.join(para_lines)
                if text.strip():
                    blocks.append(self._paragraph_block(text.strip()))

            i += 1

        return blocks[:100]  # Notion limit per request

    def _heading_block(self, level: int, text: str) -> dict:
        block_type = f"heading_{level}"
        return {
            "object": "block",
            "type": block_type,
            block_type: {
                "rich_text": [{"type": "text", "text": {"content": text[:2000]}}]
            }
        }

    def _paragraph_block(self, text: str) -> dict:
        return {
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [{"type": "text", "text": {"content": text[:2000]}}]
            }
        }

    def _bullet_block(self, text: str) -> dict:
        return {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{"type": "text", "text": {"content": text[:2000]}}]
            }
        }

    def _numbered_block(self, text: str) -> dict:
        return {
            "object": "block",
            "type": "numbered_list_item",
            "numbered_list_item": {
                "rich_text": [{"type": "text", "text": {"content": text[:2000]}}]
            }
        }

    def _code_block(self, code: str, language: str = "plain text") -> dict:
        return {
            "object": "block",
            "type": "code",
            "code": {
                "rich_text": [{"type": "text", "text": {"content": code[:2000]}}],
                "language": language if language in ["javascript", "python", "bash", "markdown"] else "plain text"
            }
        }

    def _quote_block(self, text: str) -> dict:
        return {
            "object": "block",
            "type": "quote",
            "quote": {
                "rich_text": [{"type": "text", "text": {"content": text[:2000]}}]
            }
        }

    def _callout_block(self, text: str, emoji: str = "📋") -> dict:
        return {
            "object": "block",
            "type": "callout",
            "callout": {
                "rich_text": [{"type": "text", "text": {"content": text[:2000]}}],
                "icon": {"emoji": emoji}
            }
        }

    def sync_document(self, filepath: str, title: str = None, icon: str = "📄") -> str:
        """Sync a markdown document to Notion as a page."""
        content = Path(filepath).read_text(encoding='utf-8')

        # Extract title from first H1 if not provided
        if not title:
            match = re.search(r'^# (.+)$', content, re.MULTILINE)
            title = match.group(1) if match else Path(filepath).stem

        # Convert markdown to blocks
        blocks = self.markdown_to_blocks(content)

        # Create page
        page = self.client.pages.create(
            parent={"page_id": self.parent_page_id},
            icon={"emoji": icon},
            properties={
                "title": {"title": [{"text": {"content": title}}]}
            },
            children=blocks
        )

        return page["id"]

    def sync_all_documents(self, docs_dir: str = "docs") -> dict:
        """Sync all markdown documents from a directory."""
        results = {}
        doc_configs = {
            "scisense.md": ("SciSense - Documentation", "🏢"),
            "strategie_q1_q2_2026.md": ("Stratégie Q1-Q2 2026", "🎯"),
            "prospect_personas_guide.md": ("Guide Personas Prospects", "👥"),
            "outreach_strategy.md": ("Stratégie Outreach Multi-Canal", "📣"),
            "automation_roadmap.md": ("Roadmap Automatisation", "⚙️"),
            "next_steps_roadmap.md": ("Next Steps & Roadmap", "🗺️"),
            "process_prospection.md": ("Process Prospection", "🔄"),
        }

        for filename, (title, icon) in doc_configs.items():
            filepath = Path(docs_dir) / filename
            if filepath.exists():
                try:
                    page_id = self.sync_document(str(filepath), title, icon)
                    results[filename] = {"status": "success", "page_id": page_id}
                    print(f"  ✓ {title}")
                except Exception as e:
                    results[filename] = {"status": "error", "error": str(e)}
                    print(f"  ✗ {title}: {e}")
            else:
                results[filename] = {"status": "not_found"}
                print(f"  - {filename} not found")

        return results


def setup_notion_databases(client: Client, parent_page_id: str) -> dict:
    """Create the required Notion databases."""

    print("Creating Notion databases...")

    # Database: Prospects
    prospects_db = client.databases.create(
        parent={"page_id": parent_page_id},
        title=[{"text": {"content": "👥 Prospects"}}],
        properties={
            "Nom": {"title": {}},
            "Poste": {"rich_text": {}},
            "Entreprise": {"rich_text": {}},
            "Tier": {"select": {"options": [
                {"name": "Tier 1", "color": "red"},
                {"name": "Tier 2", "color": "orange"},
                {"name": "Tier 3", "color": "yellow"},
                {"name": "Tier 4", "color": "green"},
                {"name": "Tier 5", "color": "blue"},
            ]}},
            "Statut": {"select": {"options": [
                {"name": "Not Started", "color": "gray"},
                {"name": "In Sequence", "color": "blue"},
                {"name": "Responded", "color": "yellow"},
                {"name": "Call Booked", "color": "orange"},
                {"name": "Proposal", "color": "purple"},
                {"name": "Won", "color": "green"},
                {"name": "Lost", "color": "red"},
            ]}},
            "LinkedIn": {"url": {}},
            "Email": {"email": {}},
            "Priorité": {"number": {}},
            "Valeur estimée": {"number": {"format": "euro"}},
            "Pain Points": {"multi_select": {}},
            "Packages": {"multi_select": {"options": [
                {"name": "A1"}, {"name": "A2"}, {"name": "A3"},
                {"name": "B1"}, {"name": "B2"}, {"name": "B3"}, {"name": "B4"},
                {"name": "C1"}, {"name": "C2"}, {"name": "C3"},
                {"name": "D1"}, {"name": "D2"}, {"name": "D3"},
                {"name": "E1"}, {"name": "E2"}, {"name": "F1"},
            ]}},
            "Dernière action": {"date": {}},
            "Prochaine action": {"date": {}},
        }
    )
    print(f"  ✓ Prospects: {prospects_db['id']}")

    # Database: Séquences
    sequences_db = client.databases.create(
        parent={"page_id": parent_page_id},
        title=[{"text": {"content": "📧 Séquences"}}],
        properties={
            "Action": {"title": {}},
            "Prospect": {"relation": {"database_id": prospects_db["id"]}},
            "Canal": {"select": {"options": [
                {"name": "LinkedIn", "color": "blue"},
                {"name": "Email", "color": "green"},
                {"name": "Téléphone", "color": "orange"},
            ]}},
            "Date prévue": {"date": {}},
            "Date faite": {"date": {}},
            "Statut": {"select": {"options": [
                {"name": "À faire", "color": "gray"},
                {"name": "Fait", "color": "green"},
                {"name": "Réponse", "color": "blue"},
                {"name": "Annulé", "color": "red"},
            ]}},
            "Jour": {"number": {}},
            "Notes": {"rich_text": {}},
        }
    )
    print(f"  ✓ Séquences: {sequences_db['id']}")

    # Database: Posts LinkedIn
    posts_db = client.databases.create(
        parent={"page_id": parent_page_id},
        title=[{"text": {"content": "📝 Posts LinkedIn"}}],
        properties={
            "Post": {"title": {}},
            "Date prévue": {"date": {}},
            "Date publiée": {"date": {}},
            "Statut": {"select": {"options": [
                {"name": "Brouillon", "color": "gray"},
                {"name": "À publier", "color": "yellow"},
                {"name": "Publié", "color": "green"},
            ]}},
            "Likes": {"number": {}},
            "Commentaires": {"number": {}},
            "Impressions": {"number": {}},
        }
    )
    print(f"  ✓ Posts: {posts_db['id']}")

    return {
        "prospects": prospects_db["id"],
        "sequences": sequences_db["id"],
        "posts": posts_db["id"],
    }


def main():
    parser = argparse.ArgumentParser(description='Sync SciSense data to Notion')
    parser.add_argument('--prospects', help='Path to prospects_enriched.md')
    parser.add_argument('--posts', help='Path to outreach_strategy.md')
    parser.add_argument('--docs', action='store_true', help='Sync all documents to Notion')
    parser.add_argument('--doc', help='Sync a specific document to Notion')
    parser.add_argument('--setup', help='Parent page ID to create databases')
    parser.add_argument('--all', action='store_true', help='Sync all data (prospects, posts, docs)')

    args = parser.parse_args()

    if not NOTION_TOKEN:
        print("Error: NOTION_TOKEN not set")
        print("Set it in .env file or environment variable")
        print("\nExample .env:")
        print("  NOTION_TOKEN=secret_xxxxx")
        print("  NOTION_DB_PROSPECTS=xxxxx")
        print("  NOTION_DB_SEQUENCES=xxxxx")
        print("  NOTION_DB_POSTS=xxxxx")
        return

    sync = NotionSync(NOTION_TOKEN)

    if args.setup:
        db_ids = setup_notion_databases(sync.client, args.setup)
        print("\nAdd these to your .env:")
        for name, id in db_ids.items():
            print(f"  NOTION_DB_{name.upper()}={id}")
        return

    if args.prospects or args.all:
        filepath = args.prospects or "docs/prospects_enriched.md"
        db_id = DATABASE_IDS.get("prospects")
        if not db_id:
            print("Error: NOTION_DB_PROSPECTS not set")
            return
        prospects = sync.parse_prospects_md(filepath)
        sync.sync_prospects(prospects, db_id)

    if args.posts or args.all:
        filepath = args.posts or "docs/outreach_strategy.md"
        db_id = DATABASE_IDS.get("posts")
        if not db_id:
            print("Error: NOTION_DB_POSTS not set")
            return
        posts = sync.parse_posts_md(filepath)
        sync.sync_posts(posts, db_id)

    # Document sync
    parent_page_id = os.getenv("NOTION_PARENT_PAGE")
    if args.docs or args.all:
        if not parent_page_id:
            print("Error: NOTION_PARENT_PAGE not set")
            print("Add to .env: NOTION_PARENT_PAGE=your_page_id")
            return
        print("Syncing documents to Notion...")
        doc_sync = DocumentSync(NOTION_TOKEN, parent_page_id)
        doc_sync.sync_all_documents("docs")
        print("Done!")

    if args.doc:
        if not parent_page_id:
            print("Error: NOTION_PARENT_PAGE not set")
            return
        doc_sync = DocumentSync(NOTION_TOKEN, parent_page_id)
        page_id = doc_sync.sync_document(args.doc)
        print(f"✓ Document synced: {page_id}")


if __name__ == "__main__":
    main()
