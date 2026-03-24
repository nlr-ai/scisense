# VALIDATION — vec/editorial

**Module:** vec/editorial — Tribunal editorial MDPI

---

## Invariants (MUST)

**V1: Ratio panoramique exact.**
Le SVG viewBox DOIT avoir un ratio largeur/hauteur de 3300/1680 = 1.9643 (tolerance < 0.001). Le PNG delivery DOIT etre exactement 1100x560 px. Violation = rejet MDPI (regle R8 GA_SPEC.md).
Health: H1 (S1a). Supports R1.

**V2: Zero titre, affiliation, reference dans le rendu.**
Aucun element `<text>` du SVG ne DOIT contenir : noms d'auteurs, institutions, numeros DOI, references bibliographiques, mentions "et al.", titres academiques (Dr., PhD, M.D.), noms de departements ou hopitaux. Violation = rejet MDPI (regle R1 GA_SPEC.md).
Health: H1 (S1c, S1g). Supports R1.

**V3: Budget texte <= 30 mots.**
Le nombre total de mots dans les elements `<text>` du SVG ne DOIT pas depasser 30. Les mots sont comptes par split sur whitespace apres remplacement de "/" par espace. Les symboles purs (fleches, >) ne comptent pas. Violation = rejet MDPI (regle R3 GA_SPEC.md).
Health: H1 (S1b). Supports R1.

**V4: Quatre couleurs produit presentes.**
Le SVG DOIT contenir les 4 hex produit exacts : #2563EB (OM-85), #0D9488 (PMBL), #7C3AED (MV130), #059669 (CRL1505). L'absence d'une couleur produit = FAIL. Violation = incoherence avec le design system (B5, P7).
Health: H1 (S1d palette). Supports R1.

**V6: Libre de droits — zero pixel IA dans le livrable.**
Tout element visuel du GA DOIT etre original (SVG programmatique) ou sous licence libre verifiee. Aucun pixel genere par IA (Midjourney, DALL-E, Ideogram) ne DOIT apparaitre dans le livrable final. Si IA utilisee pour calibration/wireframing, le rendu final DOIT etre redesigne en SVG programmatique. Violation = rejet MDPI (regle R5 GA_SPEC.md).
Health: H1 (S1e droits, semi-auto). Supports R1.

**V7: Lisibilite a 50% zoom.**
Le plus petit caractere du GA (incluant indices comme le gamma de IFN-gamma) DOIT etre lisible quand l'image est affichee a 550x280 px. C'est le cas d'usage reel du pediatre sur mobile. Violation = rejet MDPI (regle R6 GA_SPEC.md).
Health: H1 (S1f, semi-auto). Supports R1, P6.

---

## Invariants (NEVER)

**VN1: JAMAIS de heading "Graphical Abstract" dans le rendu.**
MDPI interdit explicitement d'inclure "Graphical Abstract" comme titre dans l'image. Le script detecte ce pattern par regex case-insensitive. Violation = rejet MDPI.
Health: H1 (S1e no GA heading). Supports R1.

**VN4: JAMAIS d'elements generes par IA dans le livrable final.**
Corollaire de V6. Les contours extraits d'images IA sont acceptes uniquement s'ils sont vectorises (Bezier/Catmull-Rom). Les pixels IA sont interdits. Violation = rejet MDPI + probleme de droits.
Health: H1 (S1e droits, manuel). Supports R1.

---

## Invariants (PROCESS)

**VP1: JAMAIS de presentation sans PASS 7/7.**
Le validateur DOIT etre execute et retourner exit code 0 avant toute presentation du GA a un humain (Aurore, NLR) ou a un systeme d'audit (NotebookLM). Un GA presente sans validation est un GA potentiellement non conforme qui consomme du temps humain inutilement.
Health: Procedure Silas. Supports G2.

**VP2: JAMAIS de modification du validateur pour "faire passer" un check.**
Si un check echoue, la correction se fait dans le SVG (compositeur, config, assets). Le validateur ne DOIT pas etre modifie pour accommoder une violation. Exception unique : ajout d'une couleur dans ALLOWED_COLORS apres verification qu'elle est legitime.
Health: Code review. Supports P2 (separation producteur/validateur).

**VP3: Le rapport DOIT etre archive dans chaque session SYNC.**
Chaque execution du validateur qui precede une decision (presentation, soumission) DOIT avoir son rapport consigne dans le handoff SYNC pour tracabilite. Un verdict sans trace est un verdict invoquable.
Health: Verification SYNC. Supports V10 (archivage versionne).
