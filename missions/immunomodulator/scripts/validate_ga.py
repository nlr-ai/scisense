#!/usr/bin/env python3
"""
validate_ga.py — Editorial Survival Validator (I6)

Gates the GA pipeline. Implements health checks S1a-S1e, S5a, S5h
from 08_HEALTH.md. Validates MDPI editorial compliance before any
presentation to Aurore.

Usage:
    python validate_ga.py path/to/wireframe.svg [--config-dir path/to/config/]

Exit code 0 = all pass, exit code 1 = any fail.
"""

import argparse
import os
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path


# ---------------------------------------------------------------------------
# Palette — single source of truth loaded from palette.yaml
# Fallback hardcoded if yaml unavailable
# ---------------------------------------------------------------------------

PRODUCT_COLORS = {
    "#2563EB": "OM-85",
    "#0D9488": "PMBL",
    "#7C3AED": "MV130",
    "#059669": "CRL1505",
}

# Colors that are allowed to appear in the SVG without triggering a warning.
# Loaded from palette.yaml + known structural colors.
ALLOWED_COLORS = {
    # Products (required)
    "#2563EB", "#0D9488", "#7C3AED", "#059669",
    # Background
    "#FAFAFA",
    # Zone backgrounds
    "#FEF2F2", "#FFFBEB", "#ECFDF5",
    # Wall — sick
    "#F87171", "#FCA5A5",
    # Wall — transition
    "#D4A574", "#C4956A",
    # Wall — healthy
    "#34D399", "#6EE7B7",
    # Text
    "#1F2937", "#6B7280", "#9CA3AF",
    # Virus
    "#DC2626",
    # Vicious cycle reds
    "#991B1B", "#FEE2E2", "#7F1D1D",
    # Structural / decorative
    "#D1D5DB",  # chevron arrows
    "#065F46",  # "Protected airways" text (dark emerald)
    # Generic
    "white", "black", "none",
    "#FFFFFF", "#000000",
}

# Forbidden patterns in text content (V2 — no titles/affiliations/references)
FORBIDDEN_PATTERNS = [
    re.compile(r"\bet\s+al\.?\b", re.IGNORECASE),
    re.compile(r"\bDOI\b", re.IGNORECASE),
    re.compile(r"\baffiliation", re.IGNORECASE),
    re.compile(r"\buniversit", re.IGNORECASE),
    re.compile(r"\breference", re.IGNORECASE),
    re.compile(r"\bcitation", re.IGNORECASE),
    re.compile(r"\b\d{4};", re.IGNORECASE),         # year; pattern in refs
    re.compile(r"\bFig(?:ure)?\s*\d", re.IGNORECASE),
    re.compile(r"\bDr\.\s", re.IGNORECASE),
    re.compile(r"\bPhD\b", re.IGNORECASE),
    re.compile(r"\bM\.?D\.?\b"),
    re.compile(r"\bInstitut", re.IGNORECASE),
    re.compile(r"\bDepartment\b", re.IGNORECASE),
    re.compile(r"\bHospital\b", re.IGNORECASE),
]

WORD_BUDGET = 30
EXPECTED_RATIO = (3300, 1680)  # viewBox at 3x
DELIVERY_DIMS = (1100, 560)
MIN_FILE_SIZE = 5 * 1024  # 5 KB


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _load_yaml_simple(path: str) -> dict:
    """Minimal YAML loader — handles flat and nested key: value without PyYAML.

    Supports:
      - key: value
      - key: "quoted value"
      - key:  (section header)
      - - "list item"
    """
    result = {}
    current_section = None
    current_list = None

    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            stripped = line.rstrip()
            if not stripped or stripped.startswith("#"):
                continue

            indent = len(line) - len(line.lstrip())

            # List item
            if stripped.lstrip().startswith("- "):
                value = stripped.lstrip()[2:].strip().strip('"').strip("'")
                # Remove inline comments
                if "  #" in value:
                    value = value[:value.index("  #")].strip().strip('"').strip("'")
                elif value.endswith('"') or value.endswith("'"):
                    pass  # already stripped
                if current_list is not None:
                    current_list.append(value)
                continue

            # Key: value
            if ":" in stripped:
                key, _, val = stripped.partition(":")
                key = key.strip()
                val = val.strip()

                # Remove inline comments from val
                if val and "  #" in val:
                    val = val[:val.index("  #")].strip()

                val = val.strip('"').strip("'")

                if not val:
                    # Section header or empty — start a list/dict
                    result[key] = []
                    current_section = key
                    current_list = result[key]
                else:
                    if indent > 0 and current_section:
                        # Nested under a section — convert list to dict if needed
                        if isinstance(result[current_section], list) and len(result[current_section]) == 0:
                            result[current_section] = {}
                        if isinstance(result[current_section], dict):
                            result[current_section][key] = val
                        current_list = None
                    else:
                        result[key] = val
                        current_section = key
                        current_list = None

    return result


def _extract_text_elements(tree: ET.ElementTree) -> list[tuple[str, str]]:
    """Extract all <text> elements from SVG. Returns list of (text_content, raw_xml)."""
    ns = {"svg": "http://www.w3.org/2000/svg"}
    root = tree.getroot()
    results = []

    # Handle both namespaced and non-namespaced SVGs
    for text_el in root.iter():
        tag = text_el.tag
        # Strip namespace
        if "}" in tag:
            tag = tag.split("}")[1]
        if tag != "text":
            continue

        # Get all text content including tspan children
        content = "".join(text_el.itertext()).strip()
        raw = ET.tostring(text_el, encoding="unicode")
        results.append((content, raw))

    return results


def _count_words(text: str) -> int:
    """Count words by splitting on whitespace. '/' is a separator, not a word."""
    # Replace / with space for "Wheezing / Asthma" = 3 words not 2
    text = text.replace("/", " ")
    words = text.split()
    # Filter out pure punctuation or single symbols like '>'
    words = [w for w in words if re.search(r"[a-zA-Z0-9]", w)]
    return len(words)


def _extract_colors_from_svg(tree: ET.ElementTree) -> set[str]:
    """Extract all fill and stroke color values from SVG attributes and style."""
    colors = set()
    root = tree.getroot()

    for el in root.iter():
        # From attributes
        for attr in ("fill", "stroke"):
            val = el.get(attr)
            if val:
                colors.add(val.strip())

        # From style attribute
        style = el.get("style", "")
        if style:
            for match in re.findall(r"(?:fill|stroke)\s*:\s*([^;\"]+)", style):
                colors.add(match.strip())

    return colors


def _normalize_color(c: str) -> str:
    """Normalize color to uppercase hex or lowercase keyword."""
    c = c.strip()
    if c.startswith("#"):
        return c.upper()
    return c.lower()


# ---------------------------------------------------------------------------
# Check implementations
# ---------------------------------------------------------------------------

def check_s1a_geometry(tree: ET.ElementTree, delivery_png_path: str | None) -> tuple[str, str]:
    """S1a — Verify SVG ratio is 1100:560 and delivery PNG is 1100x560."""
    root = tree.getroot()
    details = []
    passed = True

    # Check viewBox
    viewbox = root.get("viewBox")
    width_attr = root.get("width", "").replace("px", "")
    height_attr = root.get("height", "").replace("px", "")

    if viewbox:
        parts = viewbox.split()
        if len(parts) == 4:
            vb_w, vb_h = float(parts[2]), float(parts[3])
            expected_ratio = EXPECTED_RATIO[0] / EXPECTED_RATIO[1]
            actual_ratio = vb_w / vb_h

            # Check ratio matches 1100:560 (= 55:28)
            if abs(actual_ratio - expected_ratio) < 0.001:
                details.append(f"viewBox {vb_w:.0f}x{vb_h:.0f} ratio OK ({actual_ratio:.4f})")
            else:
                details.append(f"viewBox {vb_w:.0f}x{vb_h:.0f} ratio {actual_ratio:.4f} != expected {expected_ratio:.4f}")
                passed = False
        else:
            details.append(f"viewBox malformed: {viewbox}")
            passed = False
    else:
        # Fall back to width/height
        if width_attr and height_attr:
            w, h = float(width_attr), float(height_attr)
            expected_ratio = EXPECTED_RATIO[0] / EXPECTED_RATIO[1]
            actual_ratio = w / h
            if abs(actual_ratio - expected_ratio) < 0.001:
                details.append(f"width/height {w:.0f}x{h:.0f} ratio OK")
            else:
                details.append(f"width/height ratio {actual_ratio:.4f} != expected {expected_ratio:.4f}")
                passed = False
        else:
            details.append("No viewBox or width/height found")
            passed = False

    # Check delivery PNG dimensions
    if delivery_png_path and os.path.isfile(delivery_png_path):
        try:
            from PIL import Image
            with Image.open(delivery_png_path) as img:
                w, h = img.size
                if (w, h) == DELIVERY_DIMS:
                    details.append(f"delivery PNG {w}x{h} OK")
                else:
                    details.append(f"delivery PNG {w}x{h} != expected {DELIVERY_DIMS[0]}x{DELIVERY_DIMS[1]}")
                    passed = False
        except ImportError:
            details.append("Pillow not installed — cannot check PNG dimensions")
            passed = False
        except Exception as e:
            details.append(f"PNG read error: {e}")
            passed = False
    elif delivery_png_path:
        details.append(f"delivery PNG not found: {delivery_png_path}")
        passed = False
    else:
        details.append("no delivery PNG path provided — skipping PNG dim check")

    status = "PASS" if passed else "FAIL"
    return status, "; ".join(details)


def check_s1b_word_budget(text_elements: list[tuple[str, str]]) -> tuple[str, str, int]:
    """S1b — Total words in all <text> elements must be <= 30."""
    total = 0
    breakdown = []

    for content, _raw in text_elements:
        wc = _count_words(content)
        if wc > 0:
            total += wc
            breakdown.append(f"  '{content}' = {wc}w")

    passed = total <= WORD_BUDGET
    status = "PASS" if passed else "FAIL"
    detail = f"{total}/{WORD_BUDGET} words"
    if not passed:
        detail += " — OVER BUDGET"

    return status, detail, total


def check_s1c_no_titles(text_elements: list[tuple[str, str]]) -> tuple[str, str]:
    """S1c — No author names, affiliations, DOI, references, 'et al'."""
    violations = []

    for content, _raw in text_elements:
        for pat in FORBIDDEN_PATTERNS:
            match = pat.search(content)
            if match:
                violations.append(f"'{content}' matches forbidden pattern: {pat.pattern}")

    if violations:
        return "FAIL", "; ".join(violations)
    return "PASS", "no forbidden patterns found"


def check_s1d_palette(tree: ET.ElementTree, config_dir: str | None) -> tuple[str, str]:
    """S1d — All 4 product colors present; no unauthorized colors."""
    colors_found = _extract_colors_from_svg(tree)
    normalized = {_normalize_color(c) for c in colors_found}

    details = []
    passed = True
    has_warning = False

    # Check required product colors
    missing_products = []
    for hex_code, name in PRODUCT_COLORS.items():
        if hex_code.upper() not in normalized:
            missing_products.append(f"{name} ({hex_code})")

    if missing_products:
        details.append(f"MISSING product colors: {', '.join(missing_products)}")
        passed = False
    else:
        details.append("all 4 product colors present")

    # Check for unauthorized colors
    allowed_normalized = {_normalize_color(c) for c in ALLOWED_COLORS}
    unauthorized = []
    for c in normalized:
        if c.lower() in ("none", ""):
            continue
        if c not in allowed_normalized:
            unauthorized.append(c)

    if unauthorized:
        details.append(f"WARN unrecognized colors: {', '.join(sorted(unauthorized))}")
        has_warning = True

    if not passed:
        status = "FAIL"
    elif has_warning:
        status = "WARN"
    else:
        status = "PASS"

    return status, "; ".join(details)


def check_s1e_no_ga_heading(text_elements: list[tuple[str, str]]) -> tuple[str, str]:
    """S1e — No 'Graphical Abstract' heading in the image.

    MDPI explicitly says: 'Do not include Graphical Abstract as a heading in the image.'
    Scans all text elements for the words 'Graphical Abstract' (case-insensitive). FAIL if found.
    """
    ga_pattern = re.compile(r"graphical\s+abstract", re.IGNORECASE)
    violations = []

    for content, _raw in text_elements:
        match = ga_pattern.search(content)
        if match:
            violations.append(f"'{content}' contains forbidden heading 'Graphical Abstract'")

    if violations:
        return "FAIL", "; ".join(violations)
    return "PASS", "no 'Graphical Abstract' heading found"


def check_s5a_files(svg_path: str, full_png_path: str | None, delivery_png_path: str | None) -> tuple[str, str]:
    """S5a — SVG, full PNG, delivery PNG all exist and are > 5KB."""
    details = []
    passed = True

    files = {"SVG": svg_path, "full PNG": full_png_path, "delivery PNG": delivery_png_path}

    for label, fpath in files.items():
        if fpath is None:
            details.append(f"{label}: path not provided")
            passed = False
            continue
        if not os.path.isfile(fpath):
            details.append(f"{label}: NOT FOUND at {fpath}")
            passed = False
            continue
        size = os.path.getsize(fpath)
        if size < MIN_FILE_SIZE:
            details.append(f"{label}: {size}B < {MIN_FILE_SIZE}B minimum")
            passed = False
        else:
            details.append(f"{label}: {size}B OK")

    status = "PASS" if passed else "FAIL"
    return status, "; ".join(details)


def check_s5h_content_sync(text_elements: list[tuple[str, str]], svg_word_count: int, config_dir: str | None) -> tuple[str, str]:
    """S5h — Word count from content.yaml matches SVG text count."""
    if config_dir is None:
        return "FAIL", "no config_dir provided"

    content_path = os.path.join(config_dir, "content.yaml")
    if not os.path.isfile(content_path):
        return "FAIL", f"content.yaml not found at {content_path}"

    try:
        data = _load_yaml_simple(content_path)
    except Exception as e:
        return "FAIL", f"failed to parse content.yaml: {e}"

    # Count all words declared in content.yaml
    yaml_words = 0

    # Gather all text values from the yaml
    all_text_values = []

    for key, val in data.items():
        if key.startswith("#") or key == "TOTAL":
            continue
        if isinstance(val, list):
            for item in val:
                if isinstance(item, str):
                    all_text_values.append(item)
        elif isinstance(val, dict):
            for subkey, subval in val.items():
                if isinstance(subval, str):
                    all_text_values.append(subval)
        elif isinstance(val, str):
            all_text_values.append(val)

    for text in all_text_values:
        yaml_words += _count_words(text)

    if yaml_words == svg_word_count:
        return "PASS", f"content.yaml={yaml_words}w == SVG={svg_word_count}w"
    else:
        return "FAIL", f"content.yaml={yaml_words}w != SVG={svg_word_count}w"


# ---------------------------------------------------------------------------
# Main validator
# ---------------------------------------------------------------------------

def validate(svg_path: str, full_png_path: str | None = None,
             delivery_png_path: str | None = None,
             config_dir: str | None = None) -> tuple[bool, str]:
    """Run all checks. Returns (passed: bool, report: str)."""

    # Resolve paths
    svg_path = os.path.abspath(svg_path)
    if config_dir:
        config_dir = os.path.abspath(config_dir)

    # Auto-detect PNG paths if not provided
    if full_png_path is None or delivery_png_path is None:
        svg_dir = os.path.dirname(svg_path)
        svg_stem = Path(svg_path).stem  # e.g. wireframe_GA_v6
        if full_png_path is None:
            candidate = os.path.join(svg_dir, svg_stem + "_full.png")
            if os.path.isfile(candidate):
                full_png_path = candidate
        if delivery_png_path is None:
            candidate = os.path.join(svg_dir, svg_stem + "_delivery.png")
            if os.path.isfile(candidate):
                delivery_png_path = candidate

    if full_png_path:
        full_png_path = os.path.abspath(full_png_path)
    if delivery_png_path:
        delivery_png_path = os.path.abspath(delivery_png_path)

    # Parse SVG
    try:
        tree = ET.parse(svg_path)
    except ET.ParseError as e:
        report = _format_report({
            "S1a Geometry": ("FAIL", f"SVG parse error: {e}"),
            "S1b Word Budget": ("FAIL", "SVG parse error"),
            "S1c No Titles": ("FAIL", "SVG parse error"),
            "S1d Palette": ("FAIL", "SVG parse error"),
            "S1e No GA Heading": ("FAIL", "SVG parse error"),
            "S5a Files": ("FAIL", "SVG parse error"),
            "S5h Content Sync": ("FAIL", "SVG parse error"),
        })
        return False, report

    # Extract text elements once
    text_elements = _extract_text_elements(tree)

    # Run checks
    results = {}

    s1a_status, s1a_detail = check_s1a_geometry(tree, delivery_png_path)
    results["S1a Geometry"] = (s1a_status, s1a_detail)

    s1b_status, s1b_detail, svg_word_count = check_s1b_word_budget(text_elements)
    results["S1b Word Budget"] = (s1b_status, s1b_detail)

    s1c_status, s1c_detail = check_s1c_no_titles(text_elements)
    results["S1c No Titles"] = (s1c_status, s1c_detail)

    s1d_status, s1d_detail = check_s1d_palette(tree, config_dir)
    results["S1d Palette"] = (s1d_status, s1d_detail)

    s1e_status, s1e_detail = check_s1e_no_ga_heading(text_elements)
    results["S1e No GA Heading"] = (s1e_status, s1e_detail)

    s5a_status, s5a_detail = check_s5a_files(svg_path, full_png_path, delivery_png_path)
    results["S5a Files"] = (s5a_status, s5a_detail)

    s5h_status, s5h_detail = check_s5h_content_sync(text_elements, svg_word_count, config_dir)
    results["S5h Content Sync"] = (s5h_status, s5h_detail)

    report = _format_report(results)

    # Overall pass = no FAIL (WARN is acceptable)
    all_passed = all(status != "FAIL" for status, _ in results.values())

    return all_passed, report


def _format_report(results: dict[str, tuple[str, str]]) -> str:
    """Format the tribunal report."""
    lines = []
    lines.append("")
    lines.append("=" * 55)
    lines.append(" VALIDATE_GA -- Editorial Tribunal")
    lines.append("=" * 55)

    pass_count = 0
    total = len(results)

    for label, (status, detail) in results.items():
        # Pad label to align
        padded = f"{label:<16s}"
        if status == "FAIL":
            marker = "FAIL"
        elif status == "WARN":
            marker = "WARN"
            pass_count += 1  # WARN counts as pass
        else:
            marker = "PASS"
            pass_count += 1

        lines.append(f"{padded}: {marker} ({detail})")

    lines.append("")
    lines.append("-" * 55)

    if pass_count == total:
        lines.append(f"VERDICT: PASS ({pass_count}/{total})")
    else:
        lines.append(f"VERDICT: FAIL ({pass_count}/{total})")

    lines.append("-" * 55)
    lines.append("")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Editorial Survival Validator — gates GA pipeline (I6)")
    parser.add_argument("svg_path", help="Path to wireframe SVG file")
    parser.add_argument("--full-png", default=None,
                        help="Path to full-resolution PNG (auto-detected if omitted)")
    parser.add_argument("--delivery-png", default=None,
                        help="Path to delivery PNG (auto-detected if omitted)")
    parser.add_argument("--config-dir", default=None,
                        help="Path to config/ directory (default: ../config/ relative to script)")

    args = parser.parse_args()

    # Default config dir
    config_dir = args.config_dir
    if config_dir is None:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        config_dir = os.path.join(script_dir, "..", "config")
        if not os.path.isdir(config_dir):
            config_dir = None

    passed, report = validate(
        svg_path=args.svg_path,
        full_png_path=args.full_png,
        delivery_png_path=args.delivery_png,
        config_dir=config_dir,
    )

    print(report)
    sys.exit(0 if passed else 1)


if __name__ == "__main__":
    main()
