"""Generate PDF for V2 concept proposals using reportlab."""

import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import HexColor, white
from reportlab.lib.units import cm, mm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Preformatted, Table, TableStyle,
    PageBreak, HRFlowable
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT

BASE = r"C:\Users\reyno\scisense\missions\immunomodulator"
OUT = os.path.join(BASE, "artefacts", "proposals", "V2_concept_proposals.pdf")

# Colors
BLUE = HexColor("#2563EB")
TEAL = HexColor("#0D9488")
VIOLET = HexColor("#7C3AED")
GREEN = HexColor("#059669")
DARK = HexColor("#1F2937")
GRAY = HexColor("#6B7280")
LIGHT_GRAY = HexColor("#9CA3AF")
BG_GRAY = HexColor("#F5F5F5")
RED = HexColor("#DC2626")


def build_styles():
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(
        "MainTitle", parent=styles["Title"],
        fontSize=20, textColor=DARK, spaceAfter=2, alignment=TA_CENTER
    ))
    styles.add(ParagraphStyle(
        "Subtitle", parent=styles["Normal"],
        fontSize=12, textColor=GRAY, alignment=TA_CENTER, spaceAfter=4
    ))
    styles.add(ParagraphStyle(
        "Meta", parent=styles["Normal"],
        fontSize=9, textColor=LIGHT_GRAY, alignment=TA_CENTER, spaceAfter=12
    ))
    styles.add(ParagraphStyle(
        "SectionBlue", parent=styles["Heading2"],
        fontSize=13, textColor=BLUE, spaceBefore=16, spaceAfter=6
    ))
    styles.add(ParagraphStyle(
        "SectionTeal", parent=styles["Heading2"],
        fontSize=13, textColor=TEAL, spaceBefore=16, spaceAfter=6
    ))
    styles.add(ParagraphStyle(
        "SectionViolet", parent=styles["Heading2"],
        fontSize=13, textColor=VIOLET, spaceBefore=16, spaceAfter=6
    ))
    styles.add(ParagraphStyle(
        "SectionDark", parent=styles["Heading2"],
        fontSize=13, textColor=DARK, spaceBefore=16, spaceAfter=6
    ))
    styles.add(ParagraphStyle(
        "Body", parent=styles["Normal"],
        fontSize=10, textColor=DARK, spaceAfter=6, leading=14
    ))
    styles.add(ParagraphStyle(
        "Quote", parent=styles["Normal"],
        fontSize=10, textColor=GRAY, fontName="Helvetica-Oblique",
        leftIndent=16, spaceAfter=8, leading=14, borderColor=LIGHT_GRAY,
        borderWidth=0, borderPadding=0
    ))
    styles.add(ParagraphStyle(
        "CodeBlock", parent=styles["Code"],
        fontSize=6.5, fontName="Courier", leading=8.5,
        backColor=BG_GRAY, leftIndent=4, rightIndent=4,
        spaceBefore=4, spaceAfter=4
    ))
    styles.add(ParagraphStyle(
        "CTA", parent=styles["Normal"],
        fontSize=13, fontName="Helvetica-Bold", textColor=DARK,
        alignment=TA_CENTER, spaceBefore=10, spaceAfter=4
    ))
    styles.add(ParagraphStyle(
        "CTASub", parent=styles["Normal"],
        fontSize=10, textColor=GRAY, alignment=TA_CENTER, spaceAfter=8
    ))
    styles.add(ParagraphStyle(
        "Footer", parent=styles["Normal"],
        fontSize=8, textColor=LIGHT_GRAY, alignment=TA_CENTER, spaceBefore=16
    ))
    return styles


def badge(text, color):
    return (f'<font color="white" backColor="{color}" '
            f'size="8">&nbsp;{text}&nbsp;</font>')


def build():
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    styles = build_styles()

    doc = SimpleDocTemplate(
        OUT, pagesize=A4,
        topMargin=2*cm, bottomMargin=2*cm,
        leftMargin=2.5*cm, rightMargin=2.5*cm,
        title="Graphical Abstract V2 - 3 Propositions",
        author="Silas - SciSense VEC"
    )

    story = []

    # Title block
    story.append(Paragraph("Graphical Abstract V2", styles["MainTitle"]))
    story.append(Paragraph("3 Propositions de Design", styles["Subtitle"]))
    story.append(Paragraph(
        "Mission : Revue narrative immunomodulateurs p\u00e9diatriques (MDPI Children)<br/>"
        "24 mars 2026 \u2014 De : Silas | Pour : Aurore Inchausp\u00e9",
        styles["Meta"]
    ))
    story.append(HRFlowable(width="100%", color=HexColor("#DDDDDD")))
    story.append(Spacer(1, 8))

    # Diagnostic
    story.append(Paragraph("Diagnostic", styles["SectionDark"]))
    story.append(Paragraph(
        "Le V1 (wireframe v9) \u00e9tait <b>product-centric</b> : le p\u00e9diatre voyait des "
        "m\u00e9taphores de produits (bouclier, ma\u00e7on, pont) sans comprendre les m\u00e9canismes "
        "immunologiques sous-jacents.",
        styles["Body"]
    ))
    story.append(Paragraph(
        "\u00ab On ne comprend pas au premier coup d\u2019\u0153il. "
        "On ne voit pas l\u2019action sur l\u2019immunit\u00e9 inn\u00e9e, adaptative, "
        "le contr\u00f4le de l\u2019inflammation. \u00bb \u2014 Aurore",
        styles["Quote"]
    ))
    story.append(Paragraph(
        "<b>L\u2019inversion n\u00e9cessaire :</b> le GA doit \u00eatre <b>mechanism-centric</b>. "
        "Le p\u00e9diatre comprend 4 axes immunologiques :",
        styles["Body"]
    ))
    for mech in [
        "1. Barri\u00e8re \u00e9pith\u00e9liale (r\u00e9paration des jonctions)",
        "2. Immunit\u00e9 inn\u00e9e (activation DC/macrophages)",
        "3. Immunit\u00e9 adaptative (r\u00e9\u00e9quilibrage Th1/Th2)",
        "4. Contr\u00f4le de l\u2019inflammation (\u2193IL-33/TSLP, \u2191IL-10)",
    ]:
        story.append(Paragraph(f"&nbsp;&nbsp;&nbsp;&nbsp;{mech}", styles["Body"]))
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        "Les produits (OM-85, PMBL, MV130, CRL1505) deviennent des "
        "<b>attributions color\u00e9es</b> sur ces m\u00e9canismes \u2014 "
        "pas des personnages principaux.",
        styles["Body"]
    ))

    # Axes table
    story.append(Paragraph("3 Axes de variation", styles["SectionDark"]))
    axes_data = [
        ["Axe", "Question"],
        ["Objet central", "Qu\u2019est-ce que l\u2019\u0153il accroche en < 2s ?"],
        ["Encodage 4 m\u00e9canismes", "Comment sont-ils spatialement distincts ?"],
        ["Produit-m\u00e9canisme", "Comment sait-on quel produit agit sur quoi ?"],
    ]
    t = Table(axes_data, colWidths=[4.5*cm, 11*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), HexColor("#F3F4F6")),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("TEXTCOLOR", (0, 0), (-1, -1), DARK),
        ("GRID", (0, 0), (-1, -1), 0.5, HexColor("#DDDDDD")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    story.append(t)

    # Proposition A
    story.append(PageBreak())
    story.append(Paragraph(
        'Proposition A : \u00ab La Bronche Vivante \u00bb', styles["SectionBlue"]
    ))
    story.append(Paragraph(
        "Une <b>seule coupe bronchique panoramique</b> qui se transforme de malade (gauche) "
        "\u00e0 saine (droite). Les 4 m\u00e9canismes se lisent <b>DANS le tissu</b> \u00e0 "
        "leurs localisations biologiques r\u00e9elles.",
        styles["Body"]
    ))
    story.append(Preformatted(
        "+----------------------------------------------------------------------------+\n"
        "|                                                                            |\n"
        "|  Enfant                    COUPE BRONCHIQUE                       Enfant   |\n"
        "|  malade                  (transformation L->R)                    sain     |\n"
        "|                                                                            |\n"
        "|            +--------------------+--------------------+                     |\n"
        "|            | breches  virus->   |   intact    IgA Y Y|                     |\n"
        "|            |                    |                     |                     |\n"
        "|            |    LUMEN (air)     |    LUMEN (air)      |                     |\n"
        "|            |                    |                     |                     |\n"
        "|            | breches            |   intact            |                     |\n"
        "|            +--------------------+--------------------+                     |\n"
        "|                                                                            |\n"
        "|        DANS LE TISSU :             Mecanismes visibles :                   |\n"
        "|        # OM-85 sur surface         1. Barrier repair                       |\n"
        "|        # PMBL entre cellules       2. Innate activation                    |\n"
        "|        # MV130 dans noyau DC       3. Adaptive balance                     |\n"
        "|        # CRL1505 arc gut->lung     4. Inflammation control                 |\n"
        "|                                                                            |\n"
        "|        #### OM85  ## PMBL  # MV130  . CRL1505                             |\n"
        "|        18 RCTs    5 RCTs   1 RCT    Preclinical                            |\n"
        "+----------------------------------------------------------------------------+",
        styles["CodeBlock"]
    ))
    story.append(Paragraph(
        '<font color="#059669"><b>FORCE :</b></font> '
        "Unit\u00e9 narrative totale. Un seul objet vivant qui raconte l\u2019histoire. "
        "Les m\u00e9canismes sont <i>in situ</i> (topologie spatiale = m\u00e9canisme biologique). "
        "Le p\u00e9diatre voit une bronche qui gu\u00e9rit, pas des symboles abstraits.",
        styles["Body"]
    ))
    story.append(Paragraph(
        '<font color="#DC2626"><b>RISQUE :</b></font> '
        "Densit\u00e9 d\u2019information \u00e9lev\u00e9e dans la coupe. "
        "Demande un travail de design fin pour que les 4 m\u00e9canismes restent lisibles "
        "\u00e0 1100\u00d7560.",
        styles["Body"]
    ))

    # Proposition B
    story.append(Spacer(1, 12))
    story.append(HRFlowable(width="100%", color=HexColor("#DDDDDD")))
    story.append(Paragraph(
        'Proposition B : \u00ab 4 Colonnes M\u00e9canistiques \u00bb', styles["SectionTeal"]
    ))
    story.append(Paragraph(
        "Les 4 m\u00e9canismes sont 4 <b>bandes horizontales</b> superpos\u00e9es. Chaque bande "
        "montre PROBL\u00c8ME \u2192 R\u00c9SOLUTION. Les produits sont des badges color\u00e9s "
        "sur chaque m\u00e9canisme qu\u2019ils touchent.",
        styles["Body"]
    ))
    story.append(Preformatted(
        "+----------------------------------------------------------------------------+\n"
        "|                                                                            |\n"
        "|  Enfant           PROBLEME    ------>    RESOLUTION              Enfant    |\n"
        "|  malade                                                          sain     |\n"
        "|            +------------------------------------------------------+       |\n"
        "|            |  BARRIER     breches       ===>  intact               |       |\n"
        "|            |              [#OM85] [#PMBL]                          |       |\n"
        "|            |------------------------------------------------------|       |\n"
        "|            |  INNATE      DC dormante   ===>  DC active            |       |\n"
        "|            |              [#OM85] [#MV130] [#CRL]                  |       |\n"
        "|            |------------------------------------------------------|       |\n"
        "|            |  ADAPTIVE    Th2 bias      ===>  Th1/Th2 balance      |       |\n"
        "|            |              [#OM85] [#MV130]                          |       |\n"
        "|            |------------------------------------------------------|       |\n"
        "|            |  INFLAMMATION  elevee      ===>  controlee            |       |\n"
        "|            |              [#OM85] [#PMBL] [#CRL]                   |       |\n"
        "|            +------------------------------------------------------+       |\n"
        "|                                                                            |\n"
        "|            #### OM85   ## PMBL   # MV130   . CRL1505                      |\n"
        "|            18 RCTs     5 RCTs    1 RCT     Preclinical                     |\n"
        "+----------------------------------------------------------------------------+",
        styles["CodeBlock"]
    ))
    story.append(Paragraph(
        '<font color="#059669"><b>FORCE :</b></font> '
        "Les 4 m\u00e9canismes sont imm\u00e9diatement visibles et s\u00e9par\u00e9s. "
        "Le mapping produit \u2192 m\u00e9canisme est explicite.",
        styles["Body"]
    ))
    story.append(Paragraph(
        '<font color="#DC2626"><b>RISQUE :</b></font> '
        "Plus \u00ab tableau \u00bb que \u00ab r\u00e9cit \u00bb. "
        "Risque de ressembler \u00e0 la Figure 2 du manuscrit. Moins d\u2019\u00e9motion clinique.",
        styles["Body"]
    ))

    # Proposition C
    story.append(PageBreak())
    story.append(Paragraph(
        'Proposition C : \u00ab Le Commutateur Immunologique \u00bb', styles["SectionViolet"]
    ))
    story.append(Paragraph(
        "Garde la structure 3 zones gauche \u2192 droite mais <b>INVERSE la "
        "hi\u00e9rarchie</b> : les 4 m\u00e9canismes sont les stars de la Zone 2, "
        "les produits sont des attributions.",
        styles["Body"]
    ))
    story.append(Preformatted(
        "+------------------+--------------------------------+------------------+\n"
        "|                  |                                |                  |\n"
        "|    ZONE 1        |         ZONE 2                 |     ZONE 3       |\n"
        "|    VULNERABILITE |     4 MECANISMES               |     RESOLUTION   |\n"
        "|                  |                                |                  |\n"
        "|   Enfant malade  |  +------------------------+    |   Enfant sain    |\n"
        "|                  |  | Barrier    ===> intact  |   |                  |\n"
        "|   Mini-bronche   |  | [#OM85][#PMBL]          |   |   Mini-bronche   |\n"
        "|   malade:        |  |                         |   |   saine:         |\n"
        "|   . breches      |  | Innate     ===> active  |   |   . intacte      |\n"
        "|   . virus RSV/RV |  | [#OM85][#MV130][#CRL]   |   |   . IgA          |\n"
        "|   . inflammation |  |                         |   |   . equilibre    |\n"
        "|                  |  | Adaptive   ===> balance |   |                  |\n"
        "|   +--------+    |  | [#OM85][#MV130]          |   |   EVIDENCE       |\n"
        "|   | Cercle |    |  |                         |   |   #### 18 RCTs   |\n"
        "|   | vicieux|    |  | Inflammation => ctrl    |   |   ##   5 RCTs    |\n"
        "|   | RTIs-> |    |  | [#OM85][#PMBL][#CRL]    |   |   #    1 RCT     |\n"
        "|   | Th2->  |    |  +------------------------+    |   .    Preclin   |\n"
        "|   +--------+    |                                |                  |\n"
        "+------------------+--------------------------------+------------------+",
        styles["CodeBlock"]
    ))
    story.append(Paragraph(
        '<font color="#059669"><b>FORCE :</b></font> '
        "Flux L\u2192R conserv\u00e9 (familier pour le p\u00e9diatre). "
        "Int\u00e8gre les 4 m\u00e9canismes manquants. Enfants + bronches toujours "
        "pr\u00e9sents pour le choc cognitif.",
        styles["Body"]
    ))
    story.append(Paragraph(
        '<font color="#DC2626"><b>RISQUE :</b></font> '
        "Moins audacieux \u2014 on am\u00e9liore V1 plut\u00f4t qu\u2019on r\u00e9invente. "
        "La Zone 2 pourrait para\u00eetre dense.",
        styles["Body"]
    ))

    # Recommendation
    story.append(Spacer(1, 12))
    story.append(HRFlowable(width="100%", color=HexColor("#DDDDDD")))
    story.append(Paragraph("Recommandation de Silas", styles["SectionDark"]))
    story.append(Paragraph(
        "<b>V2-A</b> est la plus coh\u00e9rente scientifiquement : une bronche qui "
        "gu\u00e9rit EST le message de l\u2019article.",
        styles["Body"]
    ))
    story.append(Paragraph(
        "<b>V2-C</b> est le chemin le plus court pour int\u00e9grer ton feedback et livrer.",
        styles["Body"]
    ))
    story.append(Paragraph(
        "<b>V2-B</b> est la plus claire structurellement mais risque de para\u00eetre "
        "trop \u00ab tableau \u00bb.",
        styles["Body"]
    ))
    story.append(Paragraph(
        "On peut aussi <b>fusionner</b> : par exemple A+C (bronche centrale dans le format 3 zones).",
        styles["Body"]
    ))
    story.append(Paragraph(
        "Aurore, qu\u2019est-ce qui te parle ?", styles["CTA"]
    ))
    story.append(Paragraph(
        "Tu peux choisir, fusionner, ou rejeter les trois \u2014 on it\u00e8re.",
        styles["CTASub"]
    ))
    story.append(Spacer(1, 20))
    story.append(HRFlowable(width="100%", color=HexColor("#EEEEEE")))
    story.append(Paragraph(
        "SciSense \u2014 Visual Evidence Compiler (VEC)<br/>"
        "Silas \u00d7 Aurore \u2014 Compagnons de cord\u00e9e",
        styles["Footer"]
    ))

    doc.build(story)
    size_kb = os.path.getsize(OUT) / 1024
    print(f"PDF saved: {OUT}")
    print(f"Size: {size_kb:.0f} KB")


if __name__ == "__main__":
    build()
