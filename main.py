# main.py

import sqlite3
import os

# Define the path for the database
DATABASE_DIR = "sebo"
DATABASE_PATH = os.path.join(DATABASE_DIR, "database.db")

def initialize_database():
    """Initializes the database and creates necessary tables."""
    # Create the sebo directory if it doesn't exist
    os.makedirs(DATABASE_DIR, exist_ok=True)

    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    # Create a sample table (e.g., 'books')
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS libros (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT NOT NULL,
        autor TEXT NOT NULL
    )
    """)

    # Add some sample data (in Spanish, as requested)
    sample_books = [
        ("Cien años de soledad", "Gabriel García Márquez"),
        ("Don Quijote de la Mancha", "Miguel de Cervantes"),
        ("La sombra del viento", "Carlos Ruiz Zafón")
    ]

    # Check if the table is empty before inserting sample data
    cursor.execute("SELECT COUNT(*) FROM libros")
    if cursor.fetchone()[0] == 0:
        cursor.executemany("INSERT INTO libros (titulo, autor) VALUES (?, ?)", sample_books)

    conn.commit()
    conn.close()
    print(f"Base de datos inicializada en {DATABASE_PATH}")

def view_books():
    """Connects to the database and prints all books."""
    if not os.path.exists(DATABASE_PATH):
        print("La base de datos no existe. Ejecute la inicialización primero.")
        return

    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT titulo, autor FROM libros")
    books = cursor.fetchall()

    if books:
        print("\nLibros en la base de datos:")
        for book in books:
            print(f"- Título: {book[0]}, Autor: {book[1]}")
    else:
        print("No hay libros en la base de datos.")

    conn.close()

if __name__ == "__main__":
    # Initialize the database
    initialize_database()

    # View the books
    view_books()

    # Example of how to add a new book (optional)
    # conn = sqlite3.connect(DATABASE_PATH)
    # cursor = conn.cursor()
    # cursor.execute("INSERT INTO libros (titulo, autor) VALUES (?, ?)", ("El amor en los tiempos del cólera", "Gabriel García Márquez"))
    # conn.commit()
    # conn.close()
    # print("\nNuevo libro añadido.")
    # view_books()
