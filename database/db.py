import sqlite3
from pathlib import Path
from werkzeug.security import generate_password_hash

DATABASE_PATH = Path(__file__).parent.parent / "spendly.db"


def get_db():
    """
    Opens connection to spendly.db with row_factory and foreign keys enabled.
    Returns the connection.
    """
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    """
    Creates all tables using CREATE TABLE IF NOT EXISTS.
    Safe to call multiple times.
    """
    conn = get_db()
    cursor = conn.cursor()

    # Users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Expenses table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            date TEXT NOT NULL,
            description TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
        )
    """)

    conn.commit()
    conn.close()


def seed_db():
    """
    Inserts demo data only once. Does not duplicate records on multiple runs.
    """
    conn = get_db()
    cursor = conn.cursor()

    # Check if users table already contains data
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] > 0:
        conn.close()
        return  # Already seeded

    # Insert demo user
    demo_password_hash = generate_password_hash("demo123")
    cursor.execute(
        "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
        ("Demo User", "demo@spendly.com", demo_password_hash)
    )

    # Insert 8 sample expenses across all 7 categories
    sample_expenses = [
        (1, 45.50, "Food", "2026-04-01", "Lunch at cafe"),
        (1, 15.00, "Transport", "2026-04-02", "Bus pass"),
        (1, 120.00, "Bills", "2026-04-03", "Electricity bill"),
        (1, 25.00, "Health", "2026-04-05", "Pharmacy"),
        (1, 35.00, "Entertainment", "2026-04-07", "Movie tickets"),
        (1, 89.99, "Shopping", "2026-04-10", "New shoes"),
        (1, 50.00, "Other", "2026-04-12", "Miscellaneous"),
        (1, 12.50, "Food", "2026-04-13", "Coffee and snacks"),
    ]

    cursor.executemany(
        "INSERT INTO expenses (user_id, amount, category, date, description) VALUES (?, ?, ?, ?, ?)",
        sample_expenses
    )

    conn.commit()
    conn.close()
