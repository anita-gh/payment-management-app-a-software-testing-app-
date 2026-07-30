import sqlite3
from tkinter import Tk, messagebox
from unittest import TestCase, main
from unittest.mock import patch


def register(username, password):
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        messagebox.showinfo("Register", "Account created successfully!")
        return "Account created successfully!"
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Username already exists")
        return "Username already exists"

def login(username, password):
    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    user = cursor.fetchone()
    if user:
        messagebox.showinfo("Login", "Login successful!")
        return "Login successful!"
    else:
        messagebox.showerror("Error", "Invalid username or password")
        return "Invalid username or password"


class TestMediPay(TestCase):
    def setUp(self):
        
        self.conn = sqlite3.connect(":memory:")
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE,
                password TEXT
            )
        ''')
        self.conn.commit()

        
        global conn, cursor
        conn = self.conn
        cursor = self.cursor

    def tearDown(self):
        self.conn.close()

    def test_register_success(self):
        username = "testuser"
        password = "testpass"
        result = register(username, password)
        self.cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = self.cursor.fetchone()
        self.assertIsNotNone(user)
        self.assertEqual(user[1], username)
        self.assertEqual(result, "Account created successfully!")

    def test_register_username_exists(self):
        username = "testuser"
        password = "testpass"
        self.cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        self.conn.commit()

        result = register(username, password)
        self.assertEqual(result, "Username already exists")

    def test_login_success(self):
        username = "testuser"
        password = "testpass"
        self.cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        self.conn.commit()

        result = login(username, password)
        self.assertEqual(result, "Login successful!")

    def test_login_failure(self):
        username = "wronguser"
        password = "wrongpass"

        result = login(username, password)
        self.assertEqual(result, "Invalid username or password")

if __name__ == "__main__":
    main()