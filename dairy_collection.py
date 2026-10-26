"""Manage dairy milk collection records and generate summaries."""

import hashlib
import sqlite3


def create_database():
    """Create an in-memory database for milk collection records."""
    connection = sqlite3.connect(":memory:")
    connection.execute(
        """
        CREATE TABLE milk (
            id INTEGER PRIMARY KEY,
            farmer TEXT,
            litres REAL,
            fat REAL,
            day TEXT
        )
        """
    )
    return connection


def record_milk(connection, farmer, litres, fat, day):
    """Record a farmer's milk delivery using a parameterized query."""
    connection.execute(
        """
        INSERT INTO milk (farmer, litres, fat, day)
        VALUES (?, ?, ?, ?)
        """,
        (farmer, litres, fat, day),
    )
    connection.commit()


def farmer_token(farmer):
    """Generate a SHA-256 digest for a farmer's identifier."""
    return hashlib.sha256(farmer.encode("utf-8")).hexdigest()


def daily_total(connection, day):
    """Calculate the total litres collected on a given day."""
    rows = connection.execute(
        "SELECT litres FROM milk WHERE day = ?",
        (day,),
    ).fetchall()
    total_litres = sum(row[0] for row in rows)
    return f"Total: {total_litres:.1f} litres"


def top_farmer(connection):
    """Return the farmer who supplied the most milk, or None if empty."""
    rows = connection.execute(
        """
        SELECT farmer, SUM(litres)
        FROM milk
        GROUP BY farmer
        """
    ).fetchall()

    if not rows:
        return None

    top_supplier = max(rows, key=lambda row: row[1])
    return top_supplier[0]


def print_slip(farmer):
    """Print a milk collection slip message."""
    print(f"Printing slip for {farmer}")


def low_fat(connection):
    """Return farmers whose milk fat is missing or below 3.5 percent."""
    rows = connection.execute(
        "SELECT farmer, fat FROM milk"
    ).fetchall()
    return [
        farmer
        for farmer, fat in rows
        if fat is None or fat < 3.5
    ]


def main():
    """Run a demonstration of the dairy collection system."""
    connection = create_database()

    record_milk(connection, "Gopal", 12.5, 4.1, "Mon")
    record_milk(connection, "Lata", 20.0, 3.2, "Mon")

    print(daily_total(connection, "Mon"))
    print("Top farmer:", top_farmer(connection))
    print("Low-fat milk:", low_fat(connection))

    print_slip("Gopal")
    print("Farmer token:", farmer_token("Lata"))

    connection.close()


if __name__ == "__main__":
    main()
