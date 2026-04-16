#!/usr/bin/env python3
"""Seed dummy expenses for a specific user."""

import random
from datetime import datetime, timedelta
from database.db import get_db

# Arguments
USER_ID = 2
COUNT = 5
MONTHS = 3

# Categories with Indian context and amount ranges (₹)
CATEGORIES = {
    "Food": (50, 800),
    "Transport": (20, 500),
    "Bills": (200, 3000),
    "Health": (100, 2000),
    "Entertainment": (100, 1500),
    "Shopping": (200, 5000),
    "Other": (50, 1000),
}

# Distribution weights (Food most common, Health/Entertainment least)
CATEGORY_WEIGHTS = {
    "Food": 25,
    "Transport": 18,
    "Bills": 15,
    "Shopping": 15,
    "Other": 12,
    "Entertainment": 8,
    "Health": 7,
}

# Indian-style descriptions per category
DESCRIPTIONS = {
    "Food": [
        "Lunch at office canteen", "Dinner at Biryani House", "Street food",
        "Groceries from Big Bazaar", "Coffee at Cafe Coffee Day", "Tiffin service",
        "Family dinner at restaurant", "Breakfast at Udupi", "Pizza delivery",
        "South Indian thali", "North Indian meal", "Snacks from roadside vendor"
    ],
    "Transport": [
        "Metro card recharge", "Bus pass", "Auto fare", "Ola/Uber ride",
        "Fuel at petrol pump", "Train ticket", "Bike service", "Taxi to airport"
    ],
    "Bills": [
        "Electricity bill", "Water bill", "Internet bill", "Mobile recharge",
        "Cooking gas refill", "Maintenance charges", "Rent payment", "DTH subscription"
    ],
    "Health": [
        "Doctor consultation", "Medicines from pharmacy", "Health checkup",
        "Gym membership", "Yoga class fee", "Medical test", "Physiotherapy session"
    ],
    "Entertainment": [
        "Movie tickets at PVR", "OTT subscription", "Concert tickets",
        "Game purchase", "Bowling night", "Amusement park entry"
    ],
    "Shopping": [
        "Clothes from Reliance Trends", "Electronics from Croma", "Footwear",
        "Watch", "Bag", "Home decor", "Kitchen appliances", "Furniture"
    ],
    "Other": [
        "Stationery", "Gift for friend", "Donation", "Pet supplies",
        "Car wash", "Laundry service", "Salon visit", "Miscellaneous"
    ],
}


def generate_expenses(user_id, count, months):
    """Generate random expenses across past months."""
    expenses = []
    today = datetime.now()

    for _ in range(count):
        # Pick category based on weights
        category = random.choices(
            list(CATEGORY_WEIGHTS.keys()),
            weights=list(CATEGORY_WEIGHTS.values())
        )[0]

        # Generate amount in range
        min_amt, max_amt = CATEGORIES[category]
        amount = round(random.uniform(min_amt, max_amt), 2)

        # Generate date within past months
        days_ago = random.randint(0, months * 30)
        expense_date = (today - timedelta(days=days_ago)).strftime("%Y-%m-%d")

        # Pick description
        description = random.choice(DESCRIPTIONS[category])

        expenses.append((user_id, amount, category, expense_date, description))

    return expenses


def main():
    expenses = generate_expenses(USER_ID, COUNT, MONTHS)

    conn = get_db()
    cursor = conn.cursor()

    try:
        cursor.executemany(
            """INSERT INTO expenses
               (user_id, amount, category, date, description)
               VALUES (?, ?, ?, ?, ?)""",
            expenses
        )
        conn.commit()
    except Exception as e:
        conn.rollback()
        print(f"Error inserting expenses: {e}")
        raise
    finally:
        conn.close()

    # Report
    dates = [e[3] for e in expenses]
    print(f"\n✅ Inserted {len(expenses)} expenses for user {USER_ID}")
    print(f"📅 Date range: {min(dates)} to {max(dates)}")

    print("\n📋 Sample records (first 5):")
    print(f"{'ID':<6} {'Amount':<10} {'Category':<15} {'Date':<12} {'Description'}")
    print("-" * 70)

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, amount, category, date, description FROM expenses "
        "WHERE user_id = ? ORDER BY date DESC LIMIT 5",
        (USER_ID,)
    )
    for row in cursor.fetchall():
        print(f"{row[0]:<6} ₹{row[1]:<9.2f} {row[2]:<15} {row[3]:<12} {row[4]}")
    conn.close()


if __name__ == "__main__":
    main()
