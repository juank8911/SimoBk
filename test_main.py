import unittest
import os
import sqlite3
from main import initialize_database, view_books, DATABASE_PATH, DATABASE_DIR

class TestMain(unittest.TestCase):

    def setUp(self):
        # Ensure a clean database for each test
        if os.path.exists(DATABASE_PATH):
            os.remove(DATABASE_PATH)
        # Ensure the directory exists for creating the DB
        os.makedirs(DATABASE_DIR, exist_ok=True)

    def tearDown(self):
        # Clean up the database file after tests
        if os.path.exists(DATABASE_PATH):
            os.remove(DATABASE_PATH)
        if os.path.exists(DATABASE_DIR) and not os.listdir(DATABASE_DIR):
            os.rmdir(DATABASE_DIR)

    def test_initialize_database_creates_db_and_table(self):
        initialize_database()
        self.assertTrue(os.path.exists(DATABASE_PATH))

        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='libros'")
        self.assertIsNotNone(cursor.fetchone(), "La tabla 'libros' no fue creada.")
        conn.close()

    def test_initialize_database_populates_data(self):
        initialize_database()
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM libros")
        self.assertEqual(cursor.fetchone()[0], 3, "La base de datos no contiene los 3 libros de muestra.")
        conn.close()

    def test_view_books_empty_db(self):
        # Don't initialize, so DB is empty (or non-existent)
        import io
        import sys
        captured_output = io.StringIO()
        sys.stdout = captured_output
        view_books()
        sys.stdout = sys.__stdout__  # Reset redirect.
        self.assertIn("La base de datos no existe", captured_output.getvalue())

    def test_view_books_with_data(self):
        initialize_database()
        import io
        import sys
        captured_output = io.StringIO()
        sys.stdout = captured_output
        view_books()
        sys.stdout = sys.__stdout__  # Reset redirect.
        output = captured_output.getvalue()
        self.assertIn("Libros en la base de datos:", output)
        self.assertIn("Cien años de soledad", output)
        self.assertIn("Gabriel García Márquez", output)
        self.assertIn("Don Quijote de la Mancha", output)
        self.assertIn("Miguel de Cervantes", output)
        self.assertIn("La sombra del viento", output)
        self.assertIn("Carlos Ruiz Zafón", output)

    def test_initialize_database_idempotent_data_insertion(self):
        initialize_database() # First initialization
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM libros")
        count_after_first_init = cursor.fetchone()[0]
        conn.close()
        self.assertEqual(count_after_first_init, 3)

        initialize_database() # Second initialization
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM libros")
        count_after_second_init = cursor.fetchone()[0]
        conn.close()
        # Data should not be duplicated
        self.assertEqual(count_after_second_init, 3, "La inicialización de la base de datos no es idempotente para los datos.")

if __name__ == "__main__":
    unittest.main()
