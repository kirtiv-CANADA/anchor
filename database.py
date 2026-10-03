import sqlite3
from datetime import datetime
from pathlib import Path

DB_PATH = Path(__file__).parent / "data" / "anchor.db"


def init_db():
    """Create the database and table if they don't exist."""
    DB_PATH.parent.mkdir(exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT NOT NULL,
            answer TEXT NOT NULL,
            created_at TEXT NOT NULL,
            feedback TEXT
        )
    """)
    # Migration for old DBs that don't have the feedback column yet
    cursor.execute("PRAGMA table_info(history)")
    columns = [row[1] for row in cursor.fetchall()]
    if "feedback" not in columns:
        cursor.execute("ALTER TABLE history ADD COLUMN feedback TEXT")
    conn.commit()
    conn.close()


def save_qa(question, answer):
    """Save a question and answer to the database. Returns the new row id."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO history (question, answer, created_at, feedback) VALUES (?, ?, ?, ?)",
        (question, answer, datetime.now().isoformat(), None)
    )
    new_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return new_id


def get_all_history():
    """Return all saved Q&As, newest first."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, question, answer, created_at, feedback FROM history ORDER BY id DESC"
    )
    rows = cursor.fetchall()
    conn.close()
    return rows


def get_latest():
    """Return the most recently saved row, or None."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, question, answer, created_at, feedback FROM history ORDER BY id DESC LIMIT 1"
    )
    row = cursor.fetchone()
    conn.close()
    return row


def set_feedback(qid, value):
    """Set feedback ('up' or 'down') for a given row id."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("UPDATE history SET feedback = ? WHERE id = ?", (value, qid))
    conn.commit()
    conn.close()


def clear_history():
    """Delete all history."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM history")
    conn.commit()
    conn.close()


def find_similar(question, top_n=3):
    """Find past questions similar to the given question."""
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity

    history = get_all_history()
    if not history:
        return []

    past_questions = [row[1] for row in history]
    past_answers = [row[2] for row in history]
    past_dates = [row[3][:10] for row in history]
    past_ids = [row[0] for row in history]

    all_texts = past_questions + [question]

    try:
        vectorizer = TfidfVectorizer(stop_words="english")
        matrix = vectorizer.fit_transform(all_texts)
        similarities = cosine_similarity(matrix[-1], matrix[:-1]).flatten()
    except ValueError:
        return []

    results = []
    indices = similarities.argsort()[::-1][:top_n]
    for idx in indices:
        score = similarities[idx]
        if score > 0.15:
            results.append({
                "id": past_ids[idx],
                "question": past_questions[idx],
                "answer": past_answers[idx],
                "date": past_dates[idx],
                "score": round(float(score), 2),
            })
    return results


# Simple keyword-based theme detection
THEMES = {
    "Sleep": ["sleep", "bed", "bedtime", "night", "nap", "tired"],
    "Behavior": ["tantrum", "meltdown", "behavior", "behaviour", "anger", "cry", "crying"],
    "Food": ["eat", "eating", "food", "meal", "dinner", "lunch", "breakfast", "hungry"],
    "School": ["school", "class", "teacher", "homework", "study", "learn"],
    "Routine": ["routine", "schedule", "plan", "structure", "habit"],
    "Communication": ["talk", "speak", "language", "word", "communicate", "nonverbal"],
    "Anxiety": ["anxious", "anxiety", "worried", "fear", "scared", "stress"],
    "Focus": ["focus", "attention", "concentrate", "distracted", "hyperactive"],
}


def detect_themes():
    """Return a dict: theme -> {count, worked, not_worked}."""
    history = get_all_history()
    themes = {name: {"count": 0, "worked": 0, "not_worked": 0} for name in THEMES}

    for row in history:
        qid, q, a, ts, fb = row
        q_lower = q.lower()
        for theme_name, keywords in THEMES.items():
            if any(k in q_lower for k in keywords):
                themes[theme_name]["count"] += 1
                if fb == "up":
                    themes[theme_name]["worked"] += 1
                elif fb == "down":
                    themes[theme_name]["not_worked"] += 1

    return {name: data for name, data in themes.items() if data["count"] > 0}