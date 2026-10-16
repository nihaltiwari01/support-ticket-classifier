"""Step 3: the web app (Flask API + SQLite database)"""
import sqlite3
import joblib
from flask import Flask, jsonify, render_template, request

DB_PATH = "tickets.db"
app = Flask(__name__)

saved = joblib.load("model.joblib")
model = saved["model"]
model_accuracy = saved["accuracy"]


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_db() as conn:
        conn.execute(
            """CREATE TABLE IF NOT EXISTS tickets (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   message TEXT NOT NULL,
                   category TEXT NOT NULL,
                   confidence REAL NOT NULL,
                   created_at TEXT DEFAULT CURRENT_TIMESTAMP
               )"""
        )


init_db()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json(silent=True) or {}
    message = (data.get("message") or "").strip()
    if not message:
        return jsonify({"error": "Message is required"}), 400

    tfidf = model.named_steps["tfidf"]
    clf = model.named_steps["clf"]
    vocab = tfidf.get_feature_names_out()
    vec = tfidf.transform([message])
    probabilities = clf.predict_proba(vec)[0]
    order = probabilities.argsort()[::-1]
    best = order[0]
    best_guess = str(clf.classes_[best])
    confidence = round(float(probabilities[best]) * 100, 1)

    category = best_guess
    if confidence < 50:
        category = "Needs review"

    top = [
        {"category": str(clf.classes_[i]), "probability": round(float(probabilities[i]) * 100, 1)}
        for i in order[:3]
    ]
    columns = vec.nonzero()[1]
    scored = sorted(
        ((vocab[c], float(clf.coef_[best][c] * vec[0, c])) for c in columns),
        key=lambda pair: -pair[1],
    )
    helpful_words = [{"word": w, "score": round(s, 2)} for w, s in scored[:5] if s > 0]

    with get_db() as conn:
        conn.execute(
            "INSERT INTO tickets (message, category, confidence) VALUES (?, ?, ?)",
            (message, category, confidence),
        )
    return jsonify({
        "category": category,
        "confidence": confidence,
        "best_guess": best_guess,
        "top": top,
        "helpful_words": helpful_words,
        "recognised_words": int(len(columns)),
    })


@app.route("/stats")
def stats():
    with get_db() as conn:
        counts = conn.execute(
            "SELECT category, COUNT(*) AS total FROM tickets GROUP BY category ORDER BY total DESC"
        ).fetchall()
        recent = conn.execute(
            "SELECT message, category, confidence FROM tickets ORDER BY id DESC LIMIT 8"
        ).fetchall()
        total = conn.execute("SELECT COUNT(*) FROM tickets").fetchone()[0]
    return jsonify({
        "total": total,
        "accuracy": model_accuracy,
        "counts": [dict(r) for r in counts],
        "recent": [dict(r) for r in recent],
    })


if __name__ == "__main__":
    app.run(debug=True)
