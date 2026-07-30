import unittest
import sqlite3
from tkinter import Tk, Toplevel
from unittest.mock import MagicMock
import sys

class TestMedipayApp(unittest.TestCase):

    def setUp(self):
        
        self.conn = sqlite3.connect(":memory:")
        self.cursor = self.conn.cursor()

        
        self.cursor.execute("CREATE TABLE users (user_id INTEGER PRIMARY KEY, username TEXT)")
        self.cursor.execute("CREATE TABLE Deposit_user (id INTEGER PRIMARY KEY, deposit REAL, time TEXT, date TEXT, user_id INTEGER)")
        self.cursor.execute("CREATE TABLE Whithdraw_user (id INTEGER PRIMARY KEY, withdraw REAL, time TEXT, date TEXT, user_id INTEGER)")
        self.cursor.execute("CREATE TABLE products (product_id INTEGER PRIMARY KEY, name TEXT, price REAL, fee REAL, user_id INTEGER)")

        
        self.cursor.executemany("INSERT INTO users VALUES (?, ?)", [(1, "user1"), (2, "user2")])
        self.cursor.executemany("INSERT INTO Deposit_user VALUES (?, ?, ?, ?, ?)", [(1, 100.0, "10:00", "2025-01-01", 1)])
        self.cursor.executemany("INSERT INTO Whithdraw_user VALUES (?, ?, ?, ?, ?)", [(1, 50.0, "11:00", "2025-01-01", 1)])
        self.cursor.executemany("INSERT INTO products VALUES (?, ?, ?, ?, ?)", [(1, "Product1", 200.0, 20.0, 1)])

        self.conn.commit()

    def tearDown(self):
        self.conn.close()

    def test_show_users(self):
        
        query = '''
        SELECT 
            u.username,
            COALESCE(SUM(d.deposit), 0) - COALESCE(SUM(w.withdraw), 0) AS balance
        FROM users u
        LEFT JOIN Deposit_user d ON u.user_id = d.user_id
        LEFT JOIN Whithdraw_user w ON u.user_id = w.user_id
        GROUP BY u.user_id
        '''
        self.cursor.execute(query)
        users = self.cursor.fetchall()
        self.assertEqual(len(users), 2)
        self.assertEqual(users[0], ("user1", 50.0))
        self.assertEqual(users[1], ("user2", 0.0))

    def test_view_products(self):
        
        self.cursor.execute("SELECT * FROM products")
        products = self.cursor.fetchall()
        self.assertEqual(len(products), 1)
        self.assertEqual(products[0], (1, "Product1", 200.0, 20.0, 1))

    def test_payments(self):
        
        self.cursor.execute("SELECT * FROM Deposit_user")
        deposits = self.cursor.fetchall()
        self.assertEqual(len(deposits), 1)
        self.assertEqual(deposits[0], (1, 100.0, "10:00", "2025-01-01", 1))

        self.cursor.execute("SELECT * FROM Whithdraw_user")
        withdraws = self.cursor.fetchall()
        self.assertEqual(len(withdraws), 1)
        self.assertEqual(withdraws[0], (1, 50.0, "11:00", "2025-01-01", 1))

    def test_factor(self):
        
        product_id = 1
        user_id = 1
        self.cursor.execute("SELECT * FROM products WHERE user_id = ? AND product_id = ?", (user_id, product_id))
        product = self.cursor.fetchone()
        self.assertIsNotNone(product)
        self.assertEqual(product, (1, "Product1", 200.0, 20.0, 1))

    def test_gui(self):
        
        root = Tk()
        root.withdraw()  

        users_window = Toplevel(root)
        self.assertIsNotNone(users_window)
        self.assertEqual(users_window.title(), "tk")

        root.destroy()

if __name__ == "__main__":
    sys.argv = [""]  
    unittest.main(exit=False)