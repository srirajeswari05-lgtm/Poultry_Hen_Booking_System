import sqlite3


# -------------------------------
# Database Connection
# -------------------------------
def get_connection():
    connection = sqlite3.connect("poultry.db")
    return connection


# -------------------------------
# Create Bookings Table
# -------------------------------
def create_bookings_table():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_name TEXT NOT NULL,
            mobile_number TEXT NOT NULL,
            village TEXT NOT NULL,
            breed TEXT NOT NULL,
            age TEXT NOT NULL,
            purpose TEXT NOT NULL,
            price INTEGER NOT NULL
        )
        """
    )

    connection.commit()
    connection.close()


# -------------------------------
# Save Booking
# -------------------------------
def save_booking(
    customer_name,
    mobile_number,
    village,
    breed,
    age,
    purpose,
    price
):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO bookings
        (
            customer_name,
            mobile_number,
            village,
            breed,
            age,
            purpose,
            price
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            customer_name,
            mobile_number,
            village,
            breed,
            age,
            purpose,
            price
        )
    )

    connection.commit()
    connection.close()


# -------------------------------
# Run File
# -------------------------------
if __name__ == "__main__":

    create_bookings_table()

    print("✅ Bookings table created successfully.")