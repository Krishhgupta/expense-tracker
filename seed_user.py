import sqlite3
import random
from pathlib import Path
from werkzeug.security import generate_password_hash

DATABASE_PATH = Path(__file__).parent / "spendly.db"


def get_db():
    """Opens connection to spendly.db with row_factory and foreign keys enabled."""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


# Common Indian first names (mixed gender for variety)
FIRST_NAMES = [
    "Aarav", "Vivaan", "Aditya", "Arjun", "Rohan", "Aryan", "Reyansh", "Ishaan",
    "Priya", "Ananya", "Diya", "Saanvi", "Aadhya", "Meera", "Kavya", "Riya",
    "Rahul", "Amit", "Vikram", "Sanjay", "Rajesh", "Suresh", "Deepak", "Manoj",
    "Sneha", "Pooja", "Neha", "Swati", "Preeti", "Shruti", "Divya", "Anjali",
    "Arjun", "Karan", "Rohan", "Sameer", "Vikas", "Nitin", "Akash", "Prashant",
    "Lakshmi", "Saraswati", "Usha", "Vinita", "Sangeeta", "Madhuri", "Shilpa"
]

# Common Indian surnames from various regions
LAST_NAMES = [
    "Sharma", "Verma", "Gupta", "Agarwal", "Singh", "Kumar", "Yadav", "Patel",
    "Reddy", "Rao", "Nair", "Iyer", "Iyengar", "Menon", "Pillai", "Das", "Sen",
    "Ganguly", "Banerjee", "Chatterjee", "Mukherjee", "Sengupta", "Bose", "Sarkar",
    "Joshi", "Pandey", "Tiwari", "Mishra", "Shukla", "Srivastava", "Saxena",
    "Desai", "Kulkarni", "Patil", "Shinde", "Jadhav", "Pawar", "Bhosale",
    "Naidu", "Pillai", "Menon", "Reddy", "Gowda", "Rajesh", "Murthy", "Prasad"
]


def generate_indian_name():
    """Generate a realistic Indian name."""
    first_name = random.choice(FIRST_NAMES)
    last_name = random.choice(LAST_NAMES)
    return f"{first_name} {last_name}"


def generate_email_from_name(name, existing_emails):
    """Generate email from name with random 2-3 digit suffix."""
    parts = name.lower().split()
    first = parts[0]
    last = parts[-1] if len(parts) > 1 else parts[0]

    # Try a few variations
    for _ in range(10):
        number = random.randint(10, 999)
        email = f"{first}.{last}{number}@gmail.com"
        if email not in existing_emails:
            return email

    # Fallback with more variations
    for _ in range(10):
        number = random.randint(10, 999)
        email = f"{first}{last}{number}@gmail.com"
        if email not in existing_emails:
            return email

    raise ValueError("Could not generate unique email after multiple attempts")


def get_existing_emails():
    """Get all existing emails from the database."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT email FROM users")
    emails = {row["email"] for row in cursor.fetchall()}
    conn.close()
    return emails


def seed_user():
    """Generate and insert a random Indian user into the database."""
    # Get existing emails to avoid duplicates
    existing_emails = get_existing_emails()

    # Generate unique user
    max_attempts = 10
    for attempt in range(max_attempts):
        name = generate_indian_name()
        email = generate_email_from_name(name, existing_emails)

        if email not in existing_emails:
            break
    else:
        raise ValueError(f"Could not generate unique user after {max_attempts} attempts")

    password = "password123"
    password_hash = generate_password_hash(password)

    # Insert into database
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
        (name, email, password_hash)
    )
    conn.commit()
    user_id = cursor.lastrowid
    conn.close()

    # Add to existing emails set for subsequent runs
    existing_emails.add(email)

    print(f"User seeded successfully!")
    print(f"  id: {user_id}")
    print(f"  name: {name}")
    print(f"  email: {email}")


if __name__ == "__main__":
    seed_user()
