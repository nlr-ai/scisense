"""S2b database — SQLite, zero dependencies beyond stdlib."""

import sqlite3
import os
import json

DB_PATH = os.path.join(os.path.dirname(__file__), "data", "s2b.db")

SCHEMA = """
CREATE TABLE IF NOT EXISTS participants (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    token TEXT UNIQUE NOT NULL,
    clinical_domain TEXT NOT NULL,
    experience_years TEXT,
    data_literacy TEXT NOT NULL,
    grade_familiar INTEGER DEFAULT 0,
    colorblind_status TEXT DEFAULT 'unknown',
    input_mode TEXT DEFAULT 'text'
);

CREATE TABLE IF NOT EXISTS ga_images (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    filename TEXT NOT NULL,
    domain TEXT NOT NULL DEFAULT 'med',
    version TEXT,
    is_control INTEGER DEFAULT 0,
    correct_product TEXT,
    products TEXT,
    title TEXT,
    description TEXT
);

CREATE TABLE IF NOT EXISTS tests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    participant_id INTEGER NOT NULL,
    ga_image_id INTEGER NOT NULL,
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    exposure_ms INTEGER DEFAULT 5000,
    q1_text TEXT,
    q1_time_ms INTEGER,
    q2_choice TEXT,
    q2_time_ms INTEGER,
    q3_choice TEXT,
    q3_time_ms INTEGER,
    s9a_pass INTEGER,
    s9a_score REAL DEFAULT 0.0,
    s9b_pass INTEGER,
    s9c_pass INTEGER,
    s9c_score REAL DEFAULT 0.0,
    s2b_score REAL DEFAULT 0.0,
    speed_accuracy TEXT,
    q4_text TEXT,
    ab_group TEXT,
    tab_switched INTEGER DEFAULT 0,
    exposure_actual_ms INTEGER,
    q1_first_keystroke_ms INTEGER,
    q1_last_keystroke_ms INTEGER,
    exposure_mode TEXT DEFAULT 'spotlight',
    stream_position INTEGER,
    stream_length INTEGER,
    stream_selected_id TEXT,
    s10_hit INTEGER,
    q1_input_mode TEXT DEFAULT 'text',
    q1_raw_transcript TEXT,
    stimulus_condition TEXT DEFAULT 'nude',
    stimulus_text TEXT,
    screen_width INTEGER,
    screen_height INTEGER,
    device_pixel_ratio REAL,
    user_agent TEXT,
    stream_target_dwell_ms INTEGER,
    q1_filtered_text TEXT,
    q1_filter_ratio REAL,
    FOREIGN KEY (participant_id) REFERENCES participants(id),
    FOREIGN KEY (ga_image_id) REFERENCES ga_images(id),
    UNIQUE(participant_id, ga_image_id)
);
"""


def get_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


def init_db():
    conn = get_db()
    conn.executescript(SCHEMA)
    conn.commit()
    conn.close()


def create_participant(token, clinical_domain, experience_years, data_literacy, grade_familiar, colorblind_status, input_mode="text"):
    db = get_db()
    db.execute(
        """INSERT INTO participants
           (token, clinical_domain, experience_years, data_literacy, grade_familiar, colorblind_status, input_mode)
           VALUES (?, ?, ?, ?, ?, ?, ?)""",
        (token, clinical_domain, experience_years, data_literacy, grade_familiar, colorblind_status, input_mode),
    )
    db.commit()
    pid = db.execute("SELECT id FROM participants WHERE token = ?", (token,)).fetchone()["id"]
    db.close()
    return pid


def get_participant_by_token(token):
    db = get_db()
    row = db.execute("SELECT * FROM participants WHERE token = ?", (token,)).fetchone()
    db.close()
    return dict(row) if row else None


def add_ga_image(filename, domain="med", version=None, is_control=False,
                 correct_product=None, products=None, title=None, description=None):
    db = get_db()
    db.execute(
        """INSERT INTO ga_images (filename, domain, version, is_control, correct_product, products, title, description)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
        (filename, domain, version, int(is_control), correct_product,
         json.dumps(products) if products else None, title, description),
    )
    db.commit()
    db.close()


def get_next_image(participant_id):
    """Pick next unseen image for this participant."""
    db = get_db()
    seen = db.execute(
        "SELECT ga_image_id FROM tests WHERE participant_id = ?", (participant_id,)
    ).fetchall()
    seen_ids = [r["ga_image_id"] for r in seen]

    if seen_ids:
        placeholders = ",".join("?" * len(seen_ids))
        row = db.execute(
            f"SELECT * FROM ga_images WHERE id NOT IN ({placeholders}) ORDER BY RANDOM() LIMIT 1",
            seen_ids,
        ).fetchone()
    else:
        row = db.execute("SELECT * FROM ga_images ORDER BY RANDOM() LIMIT 1").fetchone()

    db.close()
    return dict(row) if row else None


def save_test(participant_id, ga_image_id, q1_text, q1_time_ms,
              q2_choice, q2_time_ms, q3_choice, q3_time_ms,
              s9a_pass, s9b_pass, s9c_pass, q4_text="", ab_group=None,
              s9c_score=0.0, s2b_score=0.0, speed_accuracy=None,
              s9a_score=0.0,
              tab_switched=0, exposure_actual_ms=None,
              q1_first_keystroke_ms=None, q1_last_keystroke_ms=None,
              exposure_mode="spotlight", stream_position=None,
              stream_length=None, stream_selected_id=None, s10_hit=None,
              q1_input_mode="text", q1_raw_transcript=None,
              screen_width=None, screen_height=None,
              device_pixel_ratio=None, user_agent=None,
              stream_target_dwell_ms=None,
              q1_filtered_text=None, q1_filter_ratio=None):
    db = get_db()
    cursor = db.execute(
        """INSERT INTO tests
           (participant_id, ga_image_id, q1_text, q1_time_ms,
            q2_choice, q2_time_ms, q3_choice, q3_time_ms,
            s9a_pass, s9a_score, s9b_pass, s9c_pass, s9c_score, s2b_score,
            speed_accuracy, q4_text, ab_group,
            tab_switched, exposure_actual_ms,
            q1_first_keystroke_ms, q1_last_keystroke_ms,
            exposure_mode, stream_position, stream_length,
            stream_selected_id, s10_hit,
            q1_input_mode, q1_raw_transcript,
            screen_width, screen_height, device_pixel_ratio,
            user_agent, stream_target_dwell_ms,
            q1_filtered_text, q1_filter_ratio)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (participant_id, ga_image_id, q1_text, q1_time_ms,
         q2_choice, q2_time_ms, q3_choice, q3_time_ms,
         int(s9a_pass), float(s9a_score), int(s9b_pass), int(s9c_pass),
         s9c_score, s2b_score, speed_accuracy, q4_text, ab_group,
         int(tab_switched), exposure_actual_ms,
         q1_first_keystroke_ms, q1_last_keystroke_ms,
         exposure_mode, stream_position, stream_length,
         stream_selected_id, s10_hit,
         q1_input_mode, q1_raw_transcript,
         screen_width, screen_height, device_pixel_ratio,
         user_agent, stream_target_dwell_ms,
         q1_filtered_text, q1_filter_ratio),
    )
    test_id = cursor.lastrowid
    db.commit()
    db.close()
    return test_id


def get_test(test_id):
    db = get_db()
    row = db.execute(
        """SELECT t.*, g.filename, g.domain, g.correct_product, g.title,
                  g.description, g.products, g.is_control, g.version
           FROM tests t JOIN ga_images g ON t.ga_image_id = g.id
           WHERE t.id = ?""",
        (test_id,),
    ).fetchone()
    db.close()
    return dict(row) if row else None


def get_stats(ga_image_id=None):
    db = get_db()
    if ga_image_id:
        row = db.execute(
            """SELECT COUNT(*) as total, AVG(s9a_pass)*100 as pct_s9a,
                      AVG(s9b_pass)*100 as pct_s9b, AVG(s9c_pass)*100 as pct_s9c,
                      AVG(q2_time_ms) as avg_q2_time
               FROM tests WHERE ga_image_id = ?""",
            (ga_image_id,),
        ).fetchone()
    else:
        row = db.execute(
            """SELECT COUNT(*) as total, AVG(s9a_pass)*100 as pct_s9a,
                      AVG(s9b_pass)*100 as pct_s9b, AVG(s9c_pass)*100 as pct_s9c,
                      AVG(q2_time_ms) as avg_q2_time
               FROM tests""",
        ).fetchone()
    db.close()
    return dict(row) if row else {}


def get_all_tests():
    db = get_db()
    rows = db.execute(
        """SELECT t.id, t.created_at, t.s9a_pass, t.s9a_score,
                  t.s9b_pass, t.s9c_pass,
                  t.s9c_score, t.s2b_score, t.speed_accuracy,
                  t.q1_text, t.q2_choice, t.q3_choice,
                  t.q1_time_ms, t.q2_time_ms, t.q3_time_ms,
                  t.participant_id, t.ab_group,
                  t.tab_switched, t.exposure_actual_ms,
                  t.q1_first_keystroke_ms, t.q1_last_keystroke_ms,
                  t.exposure_mode, t.stream_position, t.stream_length,
                  t.stream_selected_id, t.s10_hit,
                  t.q1_input_mode, t.q1_raw_transcript,
                  p.clinical_domain, p.data_literacy,
                  g.title, g.domain, g.version, g.correct_product, g.is_control
           FROM tests t
           JOIN participants p ON t.participant_id = p.id
           JOIN ga_images g ON t.ga_image_id = g.id
           ORDER BY t.created_at DESC""",
    ).fetchall()
    db.close()
    return [dict(r) for r in rows]


def get_image_count():
    db = get_db()
    row = db.execute("SELECT COUNT(*) as c FROM ga_images").fetchone()
    db.close()
    return row["c"]


def get_all_images():
    db = get_db()
    rows = db.execute("SELECT * FROM ga_images ORDER BY id").fetchall()
    db.close()
    return [dict(r) for r in rows]


def get_tests_by_quadrant(quadrant_fn):
    """Group all tests by profile quadrant.

    Args:
        quadrant_fn: callable(clinical_domain, data_literacy) -> quadrant string

    Returns: dict mapping quadrant -> list of test dicts
    """
    tests = get_all_tests()
    buckets = {}
    for t in tests:
        q = quadrant_fn(t.get("clinical_domain", ""), t.get("data_literacy", ""))
        buckets.setdefault(q, []).append(t)
    return buckets
