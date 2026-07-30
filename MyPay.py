import sqlite3
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from datetime import datetime
from tkinter.messagebox import showinfo, showerror
def main_window():
    def show_users():
        
        users_window = Toplevel()
        users_window.title("users")
        users_window.iconbitmap("tklogo.ico")

        conn = sqlite3.connect("Medipay_app.db")
        cursor = conn.cursor()

        try:
            
            query = '''
            SELECT 
                u.username,
                COALESCE(SUM(d.deposit), 0) - COALESCE(SUM(w.withdraw), 0) AS balance
            FROM users u
            LEFT JOIN Deposit_user d ON u.user_id = d.user_id
            LEFT JOIN Whithdraw_user w ON u.user_id = w.user_id
            GROUP BY u.user_id
            '''
            
            cursor.execute(query)
            users = cursor.fetchall()

            
            

            
            tree = ttk.Treeview(users_window, columns=("Username", "Balance"), show="headings", height=15)
            tree.heading("Username", text="Username")
            tree.heading("Balance", text="Balance")
            tree.column("Username", width=200, anchor="center")
            tree.column("Balance", width=100, anchor="center")

            
            for user in users:
                username, balance = user
                tree.insert("", "end", values=(username, f"{balance:.2f}"))

           
            tree.pack(fill="both", expand=True)

        except sqlite3.Error as e:
            print(f"Database error: {e}")
        finally:
            
            conn.close()

    def payments():
        payment_window = Toplevel()
        payment_window.title("Payments")
        payment_window.iconbitmap("tklogo.ico")


        tree = ttk.Treeview(payment_window, columns=('ID', 'Amount', 'Time', 'Date', 'user ID'), show='headings')
        tree.heading('ID', text='ID')
        tree.heading('Amount', text='Amount')
        tree.heading('Time', text='Time')
        tree.heading('Date', text='Date')
        tree.heading('user ID', text='user ID')
        tree.pack(fill='both', expand=True) 

        conn = sqlite3.connect("Medipay_app.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Deposit_user")
        tree_deposits = cursor.fetchall()

        for deposits in tree_deposits:
            tree.insert("", "end", values=(deposits[0], deposits[1], deposits[2], deposits[3], deposits[4]))

        cursor.execute("SELECT * FROM Whithdraw_user")
        tree_deposits = cursor.fetchall()

        for withdraws in tree_deposits:
            tree.insert("", "end", values=(withdraws[0], withdraws[1], withdraws[2], withdraws[3], deposits[4]))

    def view_products():
        product_window = Toplevel()
        product_window.title("Products")
        product_window.iconbitmap("tklogo.ico")

        tree = ttk.Treeview(product_window, columns=('product ID', 'Name', 'Price', 'Fee', 'userID'), show='headings')
        tree.heading('product ID', text='product ID')
        tree.heading('Name', text='Name')
        tree.heading('Price', text='Price')
        tree.heading('Fee', text='Fee')
        tree.heading('userID', text='userID')
        tree.pack(fill='both', expand=True)

        cursor.execute("SELECT * FROM products")
        tree_products = cursor.fetchall()

        for product in tree_products:
            tree.insert("", "end", values=(product[0], product[1], product[2], product[3], product[4])) 

    
    def factor():
        print_window = Toplevel()
        print_window.title("Deposit")
        print_window.iconbitmap("tklogo.ico")
        print_window.configure(bg='black')

        Label(print_window, text="enter user ID: ", bg='black', fg='white', font='MSSerif').pack(padx=5, pady=5, side='left')
        user_ID_entery = Entry(print_window)
        user_ID_entery.pack(pady=5, padx=5, side='left')

        Label(print_window, text="enter product ID: ", bg='black', fg='white', font='MSSerif').pack(padx=5, pady=5, side='left')
        product_ID_entery = Entry(print_window)
        product_ID_entery.pack(pady=5, padx=5, side='left')

        def get_factor():
            productid = product_ID_entery.get()
            userid = user_ID_entery.get()
            try:
                productid = int(productid)
                cursor.execute("SELECT * FROM products WHERE user_id = ? AND product_id = ?", (userid, productid))
                product = cursor.fetchone()

                if product:
                    with open(f"D:/me/uni/semester 7/app test/project/mypay/product_{productid}.txt", "w") as f:
                        f.write(f"Product ID: {product[0]}\n")
                        f.write(f"Product Name: {product[1]}\n")
                        f.write(f"Product Price: {product[2]}\n")
                        f.write(f"User ID: {product[3]}")
                    messagebox.showinfo("Saved", f"Product {product[0]} saved to file.")
                else:
                    messagebox.showwarning("Not Found", "No product found with this ID.")

            except ValueError:
                messagebox.showerror("Error", "Please enter a valid ID!")

        Button(print_window, text="print", command=get_factor, bg='#0000b3', fg='white', font='MSSerif').pack(padx=6, pady=6, side='top')  





    mypay_window = Tk()
    mypay_window.title("Dashboard") 
    mypay_window.iconbitmap("tklogo.ico")
    mypay_window.configure(bg='black')
    mypay_window.geometry('500x300')


    conn = sqlite3.connect("Medipay_app.db")
    cursor = conn.cursor()
    cursor.execute("SELECT COALESCE(SUM(fee), 0) FROM products")
    all_fee = cursor.fetchall()[0][0]
    rounded_fee = round(all_fee, 2)


    Label(mypay_window, text= f"all the profits till now: {rounded_fee}", bg='black', fg='white', font='MSSerif').pack(pady=10, padx=5)
    Button(mypay_window, text="users", command=show_users, bg='#0000b3', fg='white', font='MSSerif').pack(pady=10, padx=5)
    Button(mypay_window, text="Payments", command=payments, bg='#0000b3', fg='white', font='MSSerif').pack(pady=10, padx=5)
    Button(mypay_window, text="products", command=view_products, bg='#0000b3', fg='white', font='MSSerif').pack(pady=10, padx=5)
    Button(mypay_window, text="get factor for product", command=factor, bg='#0000b3', fg='white', font='MSSerif').pack(pady=10, padx=5)





    mypay_window.mainloop()

if __name__ == "__main__":
    main_window()