#!/usr/bin/env python3
"""
SciSense - Markdown to PDF Converter
Generates professional PDFs with SciSense brand colors (mauve/purple)

Usage:
    python markdown_to_pdf.py input.md [output.pdf]
    python markdown_to_pdf.py input.md --output output.pdf
    python markdown_to_pdf.py ../docs/automation_onepager.md

Requirements:
    pip install markdown weasyprint pygments
"""

import argparse
import sys
from pathlib import Path
from datetime import datetime

try:
    import markdown
    from markdown.extensions.tables import TableExtension
    from markdown.extensions.fenced_code import FencedCodeExtension
    from markdown.extensions.codehilite import CodeHiliteExtension
except ImportError:
    print("Error: markdown not installed. Run: pip install markdown")
    sys.exit(1)

try:
    from weasyprint import HTML, CSS
except ImportError:
    print("Error: weasyprint not installed. Run: pip install weasyprint")
    sys.exit(1)


# SciSense Brand Colors - Mauve + Rose
COLORS = {
    # Mauve (couleur principale)
    'primary': '#7B5B9A',        # Mauve principal
    'primary_dark': '#5D4375',   # Mauve foncé
    'primary_light': '#9B7BB8',  # Mauve clair
    # Rose (couleur secondaire)
    'rose': '#E8A5B3',           # Rose principal
    'rose_dark': '#D4899A',      # Rose foncé
    'rose_light': '#F5D0D8',     # Rose clair
    'rose_pale': '#FDF2F4',      # Rose très pâle (fond)
    # Neutres
    'background': '#FAF8FB',     # Fond légèrement mauve
    'background_alt': '#F5F0F7', # Fond alternatif
    'text': '#2D2D2D',           # Texte principal
    'text_light': '#6B6B6B',     # Texte secondaire
    'white': '#FFFFFF',
    'border': '#E8DDF0',         # Bordures (plus légères)
    'border_light': '#F0E8F5',   # Bordures très légères
    'code_bg': '#FAF7FC',        # Fond code
    'table_row_alt': '#FDF9FE',  # Ligne alternée tableau
}


CSS_TEMPLATE = f"""
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

@page {{
    size: A4;
    margin: 2cm 2.5cm;

    @top-center {{
        content: "SciSense";
        font-family: 'Inter', sans-serif;
        font-size: 9pt;
        color: {COLORS['text_light']};
        padding-bottom: 0.5cm;
    }}

    @bottom-center {{
        content: counter(page) " / " counter(pages);
        font-family: 'Inter', sans-serif;
        font-size: 9pt;
        color: {COLORS['text_light']};
    }}

    @bottom-right {{
        content: "scisense.fr";
        font-family: 'Inter', sans-serif;
        font-size: 8pt;
        color: {COLORS['rose_dark']};
    }}
}}

@page:first {{
    @top-center {{
        content: none;
    }}
}}

* {{
    box-sizing: border-box;
}}

body {{
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    font-size: 10pt;
    line-height: 1.6;
    color: {COLORS['text']};
    background: {COLORS['white']};
    margin: 0;
    padding: 0;
}}

/* Titres */
h1 {{
    font-size: 24pt;
    font-weight: 700;
    color: {COLORS['primary_dark']};
    margin: 0 0 0.5cm 0;
    padding-bottom: 0.3cm;
    border-bottom: 1.5px solid {COLORS['primary']};
    page-break-after: avoid;
}}

h2 {{
    font-size: 16pt;
    font-weight: 600;
    color: {COLORS['primary']};
    margin: 1cm 0 0.4cm 0;
    padding-bottom: 0.2cm;
    border-bottom: 0.5px solid {COLORS['rose']};
    page-break-after: avoid;
}}

h3 {{
    font-size: 12pt;
    font-weight: 600;
    color: {COLORS['rose_dark']};
    margin: 0.8cm 0 0.3cm 0;
    page-break-after: avoid;
}}

h4 {{
    font-size: 11pt;
    font-weight: 500;
    color: {COLORS['primary']};
    margin: 0.6cm 0 0.2cm 0;
    page-break-after: avoid;
}}

/* Paragraphes */
p {{
    margin: 0 0 0.4cm 0;
    text-align: justify;
}}

/* Blockquotes - Style callout */
blockquote {{
    background: linear-gradient(135deg, {COLORS['rose_pale']} 0%, {COLORS['background']} 100%);
    border-left: 2px solid {COLORS['rose']};
    border-radius: 0 6px 6px 0;
    margin: 0.5cm 0;
    padding: 0.4cm 0.7cm;
    font-style: italic;
    color: {COLORS['text_light']};
}}

blockquote p {{
    margin: 0;
}}

blockquote strong {{
    color: {COLORS['primary_dark']};
    font-style: normal;
}}

/* Listes */
ul, ol {{
    margin: 0 0 0.4cm 0;
    padding-left: 0.8cm;
}}

li {{
    margin-bottom: 0.15cm;
}}

li::marker {{
    color: {COLORS['rose_dark']};
    font-weight: 500;
}}

/* Tableaux */
table {{
    width: 100%;
    border-collapse: collapse;
    margin: 0.5cm 0;
    font-size: 9pt;
    page-break-inside: avoid;
}}

thead {{
    background: linear-gradient(135deg, {COLORS['primary']} 0%, {COLORS['rose_dark']} 100%);
}}

th {{
    color: {COLORS['white']};
    font-weight: 500;
    text-align: left;
    padding: 0.25cm 0.35cm;
    border: none;
}}

th:first-child {{
    border-radius: 4px 0 0 0;
}}

th:last-child {{
    border-radius: 0 4px 0 0;
}}

td {{
    padding: 0.2cm 0.35cm;
    border-bottom: 0.5px solid {COLORS['border_light']};
    vertical-align: top;
}}

tr:nth-child(even) {{
    background: {COLORS['table_row_alt']};
}}

tr:last-child td:first-child {{
    border-radius: 0 0 0 4px;
}}

tr:last-child td:last-child {{
    border-radius: 0 0 4px 0;
}}

/* Code inline */
code {{
    font-family: 'JetBrains Mono', 'Fira Code', monospace;
    font-size: 9pt;
    background: {COLORS['code_bg']};
    color: {COLORS['primary_dark']};
    padding: 0.08cm 0.15cm;
    border-radius: 3px;
    border: 0.5px solid {COLORS['border_light']};
}}

/* Blocs de code */
pre {{
    background: linear-gradient(180deg, {COLORS['code_bg']} 0%, {COLORS['background']} 100%);
    border: 0.5px solid {COLORS['border']};
    border-left: 2px solid {COLORS['rose']};
    border-radius: 0 5px 5px 0;
    padding: 0.4cm;
    margin: 0.5cm 0;
    overflow-x: auto;
    font-size: 8.5pt;
    line-height: 1.5;
    page-break-inside: avoid;
}}

pre code {{
    background: none;
    border: none;
    padding: 0;
    color: {COLORS['text']};
}}

/* Liens */
a {{
    color: {COLORS['rose_dark']};
    text-decoration: none;
    border-bottom: 0.5px dotted {COLORS['rose']};
}}

/* Ligne horizontale */
hr {{
    border: none;
    height: 1px;
    background: linear-gradient(90deg, {COLORS['rose']} 0%, {COLORS['primary_light']} 50%, transparent 100%);
    margin: 0.6cm 0;
}}

/* Strong & Em */
strong {{
    font-weight: 600;
    color: {COLORS['primary_dark']};
}}

em {{
    font-style: italic;
    color: {COLORS['text_light']};
}}

/* Checkboxes dans les listes */
li input[type="checkbox"] {{
    margin-right: 0.2cm;
    accent-color: {COLORS['rose']};
}}

/* Images */
img {{
    max-width: 100%;
    height: auto;
    border-radius: 5px;
    margin: 0.5cm 0;
}}

/* Emojis - Ensure proper display */
.emoji {{
    font-family: "Apple Color Emoji", "Segoe UI Emoji", "Noto Color Emoji", sans-serif;
}}

/* Header custom pour SciSense */
.scisense-header {{
    text-align: center;
    margin-bottom: 1cm;
    padding: 0.5cm;
    background: linear-gradient(135deg, {COLORS['primary']} 0%, {COLORS['rose_dark']} 100%);
    border-radius: 5px;
    color: {COLORS['white']};
}}

.scisense-header h1 {{
    color: {COLORS['white']};
    border: none;
    margin: 0;
    padding: 0;
}}

/* Footer info */
.doc-info {{
    font-size: 8pt;
    color: {COLORS['text_light']};
    text-align: right;
    margin-top: 1cm;
    padding-top: 0.3cm;
    border-top: 0.5px solid {COLORS['rose_light']};
}}

/* Boxes spéciales */
.info-box {{
    background: {COLORS['rose_pale']};
    border: 0.5px solid {COLORS['rose_light']};
    border-radius: 5px;
    padding: 0.4cm;
    margin: 0.5cm 0;
}}

.highlight-box {{
    background: linear-gradient(135deg, {COLORS['primary']} 0%, {COLORS['rose_dark']} 100%);
    color: {COLORS['white']};
    border-radius: 5px;
    padding: 0.4cm;
    margin: 0.5cm 0;
}}

.highlight-box strong {{
    color: {COLORS['white']};
}}
"""


HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
</head>
<body>
{content}
<div class="doc-info">
    Document généré le {date} | SciSense - Making Science Make Sense
</div>
</body>
</html>
"""


def convert_markdown_to_html(md_content: str) -> str:
    """Convert markdown content to HTML with extensions."""
    md = markdown.Markdown(
        extensions=[
            'tables',
            'fenced_code',
            'codehilite',
            'toc',
            'nl2br',
            'sane_lists',
            'smarty',
        ],
        extension_configs={
            'codehilite': {
                'css_class': 'highlight',
                'guess_lang': False,
            }
        }
    )
    return md.convert(md_content)


def create_pdf(input_path: str, output_path: str = None) -> str:
    """
    Convert markdown file to professionally styled PDF.

    Args:
        input_path: Path to markdown file
        output_path: Optional path for output PDF (defaults to same name as input)

    Returns:
        Path to generated PDF
    """
    input_file = Path(input_path)

    if not input_file.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    if not input_file.suffix.lower() in ['.md', '.markdown']:
        print(f"Warning: Input file may not be markdown: {input_file.suffix}")

    # Determine output path
    if output_path is None:
        output_file = input_file.with_suffix('.pdf')
    else:
        output_file = Path(output_path)

    # Read markdown content
    md_content = input_file.read_text(encoding='utf-8')

    # Extract title from first H1 or filename
    title = input_file.stem.replace('_', ' ').replace('-', ' ').title()
    for line in md_content.split('\n'):
        if line.startswith('# '):
            title = line[2:].strip()
            break

    # Convert to HTML
    html_content = convert_markdown_to_html(md_content)

    # Create full HTML document
    full_html = HTML_TEMPLATE.format(
        title=title,
        content=html_content,
        date=datetime.now().strftime('%d/%m/%Y')
    )

    # Generate PDF
    html_doc = HTML(string=full_html, base_url=str(input_file.parent))
    css = CSS(string=CSS_TEMPLATE)

    html_doc.write_pdf(
        str(output_file),
        stylesheets=[css],
    )

    return str(output_file)


def main():
    parser = argparse.ArgumentParser(
        description='Convert Markdown to professionally styled PDF with SciSense branding',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python markdown_to_pdf.py document.md
    python markdown_to_pdf.py document.md output.pdf
    python markdown_to_pdf.py ../docs/automation_onepager.md

The generated PDF will use SciSense brand colors (mauve/purple)
and include professional formatting with headers, footers, and page numbers.
        """
    )

    parser.add_argument(
        'input',
        help='Path to input markdown file'
    )

    parser.add_argument(
        'output',
        nargs='?',
        help='Path to output PDF file (optional, defaults to input name with .pdf)'
    )

    parser.add_argument(
        '-o', '--output-dir',
        help='Output directory for PDF (uses input filename)'
    )

    args = parser.parse_args()

    # Handle output path
    output_path = args.output
    if args.output_dir:
        input_file = Path(args.input)
        output_path = Path(args.output_dir) / input_file.with_suffix('.pdf').name

    try:
        result = create_pdf(args.input, output_path)
        print(f"✓ PDF generated: {result}")
    except FileNotFoundError as e:
        print(f"✗ Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"✗ Error generating PDF: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
