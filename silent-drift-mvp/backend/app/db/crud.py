from app.db.database import get_connection
import datetime

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS prediction_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        amount REAL,
        category TEXT,
        user_type TEXT,
        region TEXT,
        score REAL,
        confidence REAL,
        week INTEGER
    )
    """)
    conn.commit()
    conn.close()

def insert_prediction(amount, category, user_type, region, score, confidence, week):
    conn = get_connection()
    cursor = conn.cursor()
    timestamp = datetime.datetime.utcnow().isoformat()
    cursor.execute("""
    INSERT INTO prediction_logs (timestamp, amount, category, user_type, region, score, confidence, week)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (timestamp, amount, category, user_type, region, score, confidence, week))
    conn.commit()
    conn.close()
    return timestamp

def get_recent_logs(limit=50):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, timestamp, score, confidence, week FROM prediction_logs ORDER BY id DESC LIMIT ?", (limit,))
    rows = cursor.fetchall()
    conn.close()
    return [
        {"id": row[0], "timestamp": row[1], "score": row[2], "confidence": row[3], "week": row[4]}
        for row in rows
    ]
