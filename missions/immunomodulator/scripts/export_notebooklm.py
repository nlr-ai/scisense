"""
Export files for a NotebookLM session.

Creates exports/notebookLM/{mission}/{session}/  — FLAT (no sub-folders).
All files + MANIFEST.md at the same level.

Usage:
  python export_notebooklm.py                      # auto-increments session
  python export_notebooklm.py --session 3           # explicit session number
  python export_notebooklm.py --mission immunomodulator --session 1
"""

import argparse
import os
import shutil
import glob
from datetime import datetime

BASE = r"C:\Users\reyno\scisense"
MISSION_ROOT = os.path.join(BASE, "missions")
EXPORT_ROOT = os.path.join(BASE, "exports", "notebookLM")


# ── Source registry ──────────────────────────────────────────────────────
# Each mission defines its sources. Add new missions here.

MISSIONS = {
    "immunomodulator": {
        "A_science": {
            "label": "Coeur Biologique et Strategique",
            "files": [
                (r"data\import\missions\immunomodulator-manuscript\Manuscript 06112025.docx",
                 "Manuscrit soumis MDPI Children + 124 references"),
                (r"missions\immunomodulator\sources\Blueprint d'Impact Stratégique  Transformer la Prévention des Infections Respiratoires Pédiatriques.md",
                 "Traduction vulnerabilites -> leviers d'action"),
                (r"missions\immunomodulator\sources\Dossier de Synthèse Éditoriale  Manuscrit MDPI Children.md",
                 "Feuille de route journal Q2"),
            ],
        },
        "B_doc_chain": {
            "label": "Referentiel d'Ingenierie (Doc Chain 10 Facettes)",
            "files": [
                (r"missions\immunomodulator\docs\01_RESULTS.md", "Resultats mesurables R1-R4"),
                (r"missions\immunomodulator\docs\02_OBJECTIVES.md", "Objectifs et non-objectifs"),
                (r"missions\immunomodulator\docs\03_PATTERNS.md", "Design patterns P1-P25"),
                (r"missions\immunomodulator\docs\04_BEHAVIORS.md", "Behaviors observables B1-B7"),
                (r"missions\immunomodulator\docs\05_ALGORITHM.md", "Logique step-by-step"),
                (r"missions\immunomodulator\docs\06_VALIDATION.md", "Invariants V1-V13"),
                (r"missions\immunomodulator\docs\07_IMPLEMENTATION.md", "Architecture code"),
                (r"missions\immunomodulator\docs\08_HEALTH.md", "Diagnostics runtime"),
                (r"missions\immunomodulator\docs\09_PHENOMENOLOGY.md", "Perception et impact"),
                (r"missions\immunomodulator\docs\10_SYNC.md", "Etat actuel et handoff"),
            ],
        },
        "C_anchors": {
            "label": "Ancrage Topologique, Phenomenologique et System Prompt",
            "files": [
                (r"missions\immunomodulator\config\notebooklm_system_prompt.md",
                 "System prompt NotebookLM Moteur Analytique V2"),
                (r"missions\immunomodulator\artefacts\comparisons\target_vs_output_v9.png",
                 "Matrice de reference: extraction organique reussie"),
                (r"missions\immunomodulator\artefacts\comparisons\evolution_v7_v8_v9.png",
                 "Preuve visuelle de progression (anti-regression)"),
                (r"missions\immunomodulator\artefacts\proposals\V2_concept_proposals.pdf",
                 "3 propositions V2 design (Bronche Vivante / Colonnes / Commutateur)"),
                (r"missions\immunomodulator\GA_SPEC.md",
                 "Spec complete GA (contraintes MDPI, pipeline, 3V framework)"),
            ],
        },
        "banned": [
            (r"missions\immunomodulator\artefacts\wireframes\wireframe_GA_v8_delivery.png",
             "Design stick-figures obsolete, elements flottants"),
            (r"missions\immunomodulator\artefacts\podcasts\P1_L_algorithme_qui_calcule_la_santé_pédiatrique_transcript.txt",
             "Debat archive, inutile pour execution clinique"),
        ],
    },
}


def find_next_session(mission_export_dir):
    """Find the next session number by scanning existing directories."""
    if not os.path.exists(mission_export_dir):
        return 1
    existing = []
    for d in os.listdir(mission_export_dir):
        if d.startswith("S") and d[1:].isdigit():
            existing.append(int(d[1:]))
    return max(existing, default=0) + 1


def export(mission_name, session_num=None):
    if mission_name not in MISSIONS:
        print(f"Unknown mission: {mission_name}")
        print(f"Available: {', '.join(MISSIONS.keys())}")
        return

    config = MISSIONS[mission_name]
    mission_export_dir = os.path.join(EXPORT_ROOT, mission_name)

    if session_num is None:
        session_num = find_next_session(mission_export_dir)

    session_dir = os.path.join(mission_export_dir, f"S{session_num:02d}")

    if os.path.exists(session_dir):
        print(f"Session directory already exists: {session_dir}")
        print("Use --session N to specify a different session number.")
        return

    print(f"Exporting: {mission_name} / S{session_num:02d}")
    print(f"Target: {session_dir}")
    print()

    manifest_lines = []
    manifest_lines.append(f"# NotebookLM Session S{session_num:02d} — {mission_name}")
    manifest_lines.append(f"")
    manifest_lines.append(f"**Exported:** {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    manifest_lines.append(f"**Mission:** {mission_name}")
    manifest_lines.append(f"**Purpose:** Hard Reset — clean context for V10 compilation")
    manifest_lines.append(f"")
    manifest_lines.append(f"---")
    manifest_lines.append(f"")

    os.makedirs(session_dir, exist_ok=True)

    total_copied = 0
    total_missing = 0
    total_size = 0

    for section_key in ["A_science", "B_doc_chain", "C_anchors"]:
        section = config[section_key]
        section_label = section["label"]

        manifest_lines.append(f"## {section_key}: {section_label}")
        manifest_lines.append(f"")

        for rel_path, description in section["files"]:
            src = os.path.join(BASE, rel_path)
            filename = os.path.basename(src)
            dst = os.path.join(session_dir, filename)

            if os.path.exists(src):
                shutil.copy2(src, dst)
                size_kb = os.path.getsize(dst) / 1024
                total_size += size_kb
                total_copied += 1
                status = f"{size_kb:.0f} KB"
                print(f"  [OK] {filename} ({status})")
                manifest_lines.append(f"- **{filename}** ({status}) — {description}")
            else:
                total_missing += 1
                print(f"  [!!] MISSING: {src}")
                manifest_lines.append(f"- **{filename}** (MISSING) — {description}")

        manifest_lines.append(f"")

    # Banned files section
    manifest_lines.append(f"## BANNED (do NOT import)")
    manifest_lines.append(f"")
    for rel_path, reason in config.get("banned", []):
        filename = os.path.basename(rel_path)
        manifest_lines.append(f"- ~~{filename}~~ — {reason}")
    manifest_lines.append(f"")

    # Summary
    manifest_lines.append(f"---")
    manifest_lines.append(f"")
    manifest_lines.append(f"**Total:** {total_copied} files, {total_size:.0f} KB")
    if total_missing:
        manifest_lines.append(f"**Missing:** {total_missing} files")
    manifest_lines.append(f"")
    manifest_lines.append(f"*SciSense — Visual Evidence Compiler (VEC)*")

    # Write manifest
    manifest_path = os.path.join(session_dir, "MANIFEST.md")
    with open(manifest_path, "w", encoding="utf-8") as f:
        f.write("\n".join(manifest_lines))

    print()
    print(f"Manifest: {manifest_path}")
    print(f"Total: {total_copied} files copied, {total_size:.0f} KB")
    if total_missing:
        print(f"WARNING: {total_missing} files missing!")
    print(f"Done: {session_dir}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Export files for NotebookLM session")
    parser.add_argument("--mission", default="immunomodulator",
                        help="Mission name (default: immunomodulator)")
    parser.add_argument("--session", type=int, default=None,
                        help="Session number (auto-increments if omitted)")
    args = parser.parse_args()
    export(args.mission, args.session)
