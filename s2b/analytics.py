"""S2b analytics — aggregate statistics per S2b_Mathematics.md.

All formulas from sections 2-7 of the mathematical model.
"""

from scoring import classify_speed_accuracy, classify_rt2, score_s2b_composite
from config_loader import get_constant

# ── Configurable constants ────────────────────────────────────────────────
MCNEMAR_MIN_PAIRS = get_constant("mcnemar_min_pairs", 10)

try:
    import numpy as np
    def _median(values):
        if not values:
            return 0.0
        return float(np.median(values))
except ImportError:
    from statistics import median as _stats_median
    def _median(values):
        if not values:
            return 0.0
        return float(_stats_median(values))


def compute_aggregate_stats(tests: list[dict]) -> dict:
    """Compute aggregate metrics across a list of test dicts.

    Each test dict must have: s9a_pass, s9b_pass, s9c_score, q2_time_ms, s2b_score.

    Returns:
        {
            "Taux_S9a": float,      # proportion S9a correct
            "Taux_S9b": float,      # proportion S9b correct
            "Score_S9c": float,     # mean graduated S9c
            "Mediane_RT2": float,   # median q2_time_ms
            "RT2_class": str,       # fluent/hesitant/lost
            "Score_S2b": float,     # mean composite score
            "N": int,
        }
    """
    n = len(tests)
    if n == 0:
        return {
            "Taux_S9a": 0.0,
            "Taux_S9b": 0.0,
            "Score_S9c": 0.0,
            "Mediane_RT2": 0.0,
            "RT2_class": "lost",
            "Score_S2b": 0.0,
            "N": 0,
        }

    taux_s9a = sum(1 for t in tests if t.get("s9a_pass")) / n
    taux_s9b = sum(1 for t in tests if t.get("s9b_pass")) / n
    score_s9c = sum(t.get("s9c_score", 0.0) or 0.0 for t in tests) / n

    rt2_values = [t["q2_time_ms"] for t in tests if t.get("q2_time_ms")]
    mediane_rt2 = _median(rt2_values)
    rt2_class = classify_rt2(mediane_rt2)

    score_s2b = sum(t.get("s2b_score", 0.0) or 0.0 for t in tests) / n

    return {
        "Taux_S9a": round(taux_s9a, 4),
        "Taux_S9b": round(taux_s9b, 4),
        "Score_S9c": round(score_s9c, 4),
        "Mediane_RT2": round(mediane_rt2, 1),
        "RT2_class": rt2_class,
        "Score_S2b": round(score_s2b, 4),
        "N": n,
    }


def compute_profile_quadrant(clinical_domain: str, data_literacy: str) -> str:
    """Map participant profile to one of 4 quadrants per S2b_Mathematics.md section 4.

    Axes:
        - Clinical expertise: high if clinical_domain in {pediatrician, gp, researcher_bio,
          Pédiatre, Médecin Généraliste, Chercheur Bio/Médical}
        - Data literacy: high if data_literacy in {published_author, tech_data,
          Auteur publié (peer-review), Profil Tech/Data}

    Returns one of: "Q1_public_naif", "Q2_tech", "Q3_clinicien", "Q4_clinicien_chercheur"
    """
    clinical_high_values = {
        "pediatrician", "gp", "researcher_bio",
        "pédiatre", "médecin généraliste", "chercheur bio/médical",
    }
    data_high_values = {
        "published_author", "tech_data",
        "auteur publié (peer-review)", "profil tech/data",
    }

    cd = (clinical_domain or "").strip().lower()
    dl = (data_literacy or "").strip().lower()

    clinical_high = cd in clinical_high_values
    data_high = dl in data_high_values

    if clinical_high and data_high:
        return "Q4_clinicien_chercheur"
    if clinical_high and not data_high:
        return "Q3_clinicien"
    if not clinical_high and data_high:
        return "Q2_tech"
    return "Q1_public_naif"


def compute_stats_by_quadrant(tests: list[dict], participants: list[dict] = None) -> dict:
    """Compute aggregate stats grouped by profile quadrant.

    Each test dict must have clinical_domain and data_literacy fields
    (from JOIN with participants).

    Returns: dict mapping quadrant string -> stats dict (same shape as compute_aggregate_stats).
    """
    buckets = {}
    for t in tests:
        q = compute_profile_quadrant(t.get("clinical_domain", ""), t.get("data_literacy", ""))
        buckets.setdefault(q, []).append(t)

    return {q: compute_aggregate_stats(ts) for q, ts in buckets.items()}


def compute_speed_accuracy_distribution(tests: list[dict]) -> dict:
    """Count tests in each speed-accuracy quadrant per S2b_Mathematics.md section 3.

    Returns: {"fast_right": int, "slow_right": int, "fast_wrong": int, "slow_wrong": int}
    """
    counts = {"fast_right": 0, "slow_right": 0, "fast_wrong": 0, "slow_wrong": 0}
    for t in tests:
        sa = t.get("speed_accuracy")
        if not sa:
            # Compute on the fly if not stored
            sa = classify_speed_accuracy(t.get("s9b_pass", False), t.get("q2_time_ms", 0))
        if sa in counts:
            counts[sa] += 1
    return counts


def compute_s10_rate(tests: list[dict]) -> dict:
    """Compute S10 saillance rate per S2b_Mathematics.md section 8.

    S10 = P(participant selects the GA cible among 3 thumbnails).
    Only applies to stream-mode tests where s10_hit is recorded.

    Chance level = 1/3 = 0.33. Threshold for scroll-stopping = >0.70.

    Returns:
        {
            "s10_rate": float,        # proportion of hits
            "n_stream": int,          # total stream tests with s10 data
            "n_hits": int,            # number of correct selections
            "s10_label": str,         # interpretation label
            "s10_x_s9b": float | None,  # S10 x S9b product (chain metric)
        }
    """
    stream_tests = [
        t for t in tests
        if t.get("exposure_mode") == "stream" and t.get("s10_hit") is not None
    ]
    n = len(stream_tests)
    if n == 0:
        return {
            "s10_rate": 0.0,
            "n_stream": 0,
            "n_hits": 0,
            "s10_label": "Pas de données stream",
            "s10_x_s9b": None,
        }

    n_hits = sum(1 for t in stream_tests if t.get("s10_hit"))
    s10_rate = n_hits / n

    if s10_rate > 0.70:
        label = "Scroll-stopping validé"
    elif s10_rate >= 0.33:
        label = "Pas plus mémorable que les distracteurs"
    else:
        label = "Activement ignoré (pire que le hasard)"

    # Compute S10 x S9b chain metric
    taux_s9b = sum(1 for t in stream_tests if t.get("s9b_pass")) / n
    s10_x_s9b = round(s10_rate * taux_s9b, 4)

    return {
        "s10_rate": round(s10_rate, 4),
        "n_stream": n,
        "n_hits": n_hits,
        "s10_label": label,
        "s10_x_s9b": s10_x_s9b,
    }


def compute_ab_delta(tests_control: list[dict], tests_vec: list[dict]) -> dict:
    """Compute A/B delta per S2b_Mathematics.md section 5.

    Delta_S9b = Taux_S9b(VEC) - Taux_S9b(control)

    Optional McNemar chi-squared if sufficient paired data.

    Returns:
        {
            "delta_s9b": float,
            "taux_s9b_control": float,
            "taux_s9b_vec": float,
            "n_control": int,
            "n_vec": int,
            "mcnemar_chi2": float | None,
            "mcnemar_significant": bool | None,  # at p=0.05 (chi2 > 3.84)
        }
    """
    n_ctrl = len(tests_control)
    n_vec = len(tests_vec)

    taux_ctrl = sum(1 for t in tests_control if t.get("s9b_pass")) / n_ctrl if n_ctrl else 0.0
    taux_vec = sum(1 for t in tests_vec if t.get("s9b_pass")) / n_vec if n_vec else 0.0
    delta = taux_vec - taux_ctrl

    result = {
        "delta_s9b": round(delta, 4),
        "taux_s9b_control": round(taux_ctrl, 4),
        "taux_s9b_vec": round(taux_vec, 4),
        "n_control": n_ctrl,
        "n_vec": n_vec,
        "mcnemar_chi2": None,
        "mcnemar_significant": None,
    }

    # McNemar requires paired data — match by participant_id
    ctrl_by_pid = {t["participant_id"]: bool(t.get("s9b_pass")) for t in tests_control if "participant_id" in t}
    vec_by_pid = {t["participant_id"]: bool(t.get("s9b_pass")) for t in tests_vec if "participant_id" in t}

    paired_pids = set(ctrl_by_pid.keys()) & set(vec_by_pid.keys())
    if len(paired_pids) >= MCNEMAR_MIN_PAIRS:
        # b = control correct, VEC incorrect
        # c = control incorrect, VEC correct
        b = sum(1 for pid in paired_pids if ctrl_by_pid[pid] and not vec_by_pid[pid])
        c = sum(1 for pid in paired_pids if not ctrl_by_pid[pid] and vec_by_pid[pid])

        if (b + c) > 0:
            chi2 = ((b - c) ** 2) / (b + c)
            result["mcnemar_chi2"] = round(chi2, 4)
            # Phenomenon: chi2 critical value 3.84 = chi-squared distribution
            # at p=0.05 with 1 degree of freedom (standard statistical threshold)
            result["mcnemar_significant"] = chi2 > 3.84

    return result
