import sqlite3
from tkinter import *
from tkinter import messagebox
from tkinter import ttk, PhotoImage
from datetime import datetime
from tkinter.messagebox import showinfo, showerror


conn = sqlite3.connect("Medipay_app.db")
cursor = conn.cursor()


cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT
)''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS products (
    product_id INTEGER PRIMARY KEY AUTOINCREMENT,
    productname TEXT,
    price REAL,
    fee REAL,
    user_id INTEGER,
    FOREIGN KEY(user_id) REFERENCES users(user_id)
)''')


cursor.execute('''
CREATE TABLE IF NOT EXISTS Deposit_user (
    transac_id INTEGER PRIMARY KEY AUTOINCREMENT,
    deposit REAL,
    date TEXT,
    time TEXT,
    user_id INTEGER,
    FOREIGN KEY(user_id) REFERENCES users(user_id)
)''')


cursor.execute('''
CREATE TABLE IF NOT EXISTS Whithdraw_user (
    transac_id INTEGER PRIMARY KEY AUTOINCREMENT,
    withdraw REAL,
    date TEXT,
    time TEXT,
    user_id INTEGER,
    FOREIGN KEY(user_id) REFERENCES users(user_id)
)''')


conn.commit()


def main_window():
    def login():
        username = username_entry.get()
        password = password_entry.get()


        
        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user = cursor.fetchone()
        
        if user:
            messagebox.showinfo("Login", "Login successful!")
            dashboard(user[0])
        else:
            assert user is not None, "User should be found in the database"
            showerror("Error", "Invalid username or password")
        

    def register():
        username = username_entry.get()
        password = password_entry.get()
        
        try:
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            showinfo("Register", "Account created successfully!")
        except sqlite3.IntegrityError: #IntegrityError --> when we are overwriting an information in DB
            showerror("Error", "Username already exists")

    root = Tk()
    root.title("Medipay")

    Label(root, text="Username: ", bg='black', fg='white', font='MSSerif').grid(row=17, column=1, padx=5, pady=5, sticky="w")
    username_entry = Entry(root)
    username_entry.grid(row=17, column=2, padx=5, pady=5, sticky="w")

    Label(root, text="Password: ", bg='black', fg='white', font='MSSerif').grid(row=18, column=1, padx=5, pady=5, sticky="w")
    password_entry = Entry(root)
    password_entry.grid(row=18, column=2, padx=5, pady=5, sticky="w")

    Button(root, text="Login", command=login, bg='#0000b3', fg='white', font='MSSerif').grid(row=19, column=1, padx=15, pady=10)
    Button(root, text="Register", command=register, bg='#0000b3', fg='white', font='MSSerif').grid(row=19, column=2, padx=15, pady=10, sticky="w")

    root.geometry("380x480")
    root.configure(bg='black')

    root.iconbitmap("tklogo.ico")
    rootphoto = PhotoImage(file="minifylogo.png")
    Label(root, image=rootphoto, bd=0, highlightthickness=0).grid(row=1, column=1, padx=0, pady=0, columnspan=2)


    root.mainloop()
#####################################################################################

def dashboard(user_id):
    def view_products():
        product_window = Toplevel()
        product_window.title("Products")
        product_window.iconbitmap("tklogo.ico")

        tree = ttk.Treeview(product_window, columns=('ID', 'Name', 'Price', 'Fee', 'userID'), show='headings')
        tree.heading('ID', text='ID')
        tree.heading('Name', text='Name')
        tree.heading('Price', text='Price')
        tree.heading('Fee', text='Fee')
        tree.heading('userID', text='userID')
        tree.pack(fill='both', expand=True)

        cursor.execute("SELECT * FROM products WHERE user_id = ?", (user_id,))
        tree_products = cursor.fetchall()

        for product in tree_products:
            tree.insert("", "end", values=(product[0], product[1], product[2], product[3], product[4])) 

    def view_payments():
        payment_window = Toplevel()
        payment_window.title("Payments")
        payment_window.iconbitmap("tklogo.ico")


        tree = ttk.Treeview(payment_window, columns=('ID', 'Amount', 'Time', 'Date'), show='headings')
        tree.heading('ID', text='ID')
        tree.heading('Amount', text='Amount')
        tree.heading('Time', text='Time')
        tree.heading('Date', text='Date')
        tree.pack(fill='both', expand=True) 

        conn = sqlite3.connect("Medipay_app.db")
        cursor = conn.cursor()
        cursor.execute("SELECT COALESCE(SUM(deposit), 0) AS deposit_sum FROM Deposit_user WHERE user_id = ?", (user_id,))
        deposit_sum = cursor.fetchone()[0]

        cursor.execute("SELECT COALESCE(SUM(withdraw), 0) AS withdraw_sum FROM Whithdraw_user WHERE user_id = ?", (user_id,))
        withdraw_sum = cursor.fetchone()[0]

        balance = deposit_sum - withdraw_sum
        print(balance)
        if (balance<0):
            Label(payment_window, text="We kindly request that you proceed with settling your outstanding balance at your earliest convenience.", font='MSSerif'). pack(pady=10)

        Label(payment_window, text=f"Credit: {balance}", font='MSSerif').pack(side='top', pady=10)

        cursor.execute("SELECT * FROM Deposit_user WHERE user_id = ?", (user_id,))
        tree_deposits = cursor.fetchall()

        for deposits in tree_deposits:
            tree.insert("", "end", values=(deposits[0], deposits[1], deposits[2], deposits[3]))

        cursor.execute("SELECT * FROM Whithdraw_user WHERE user_id = ?", (user_id,))
        tree_deposits = cursor.fetchall()

        for withdraws in tree_deposits:
            tree.insert("", "end", values=(withdraws[0], withdraws[1], withdraws[2], withdraws[3]))




    def Deposit_it():
        deposit_window = Toplevel()
        deposit_window.title("Deposit")
        deposit_window.iconbitmap("tklogo.ico")
        deposit_window.configure(bg='black')

        Label(deposit_window, text="please double check the amount you want to deposit", bg='black', fg='white', font='MSSerif').pack(padx=5, pady=5, side='top')
        Label(deposit_window, text="Enter the amount you want to deposit: ", bg='black', fg='white', font='MSSerif').pack(padx=5, pady=5, side='left')
        amount_entry = Entry(deposit_window)
        amount_entry.pack(pady=5, padx=5, side='left')

        def confirm_deposit():
            money_amount = amount_entry.get()
            try:
                money_amount = float(money_amount)
                assert money_amount > 0 , "money amount is less than zero" #★
                if (money_amount>0):
                    showinfo("Deposit Successful",f"you deposit {money_amount}$")

                    current_time = datetime.now()
                    date_pay = current_time.strftime("%Y-%m-%d")  # فقط تاریخ به‌صورت رشته
                    time_pay = current_time.strftime("%H:%M:%S")
                    
                    conn = sqlite3.connect('Medipay_app.db')  
                    cursor = conn.cursor()

                    cursor.execute('SELECT user_id FROM users WHERE user_id = ?', (user_id,))
                    user = cursor.fetchone()
                    if user:
                        cursor.execute('INSERT INTO Deposit_user (deposit, date, time, user_id) VALUES (?,?,?,?)',(money_amount, date_pay, time_pay, user_id))
                    conn.commit()
                    conn.close()
                else:
                    showerror ("Invalid Amount", "You can't deposit less than 1$!")
                    raise TypeError("Invalid Amount", "You can't deposit less than 1$!") #★
                
            except ValueError:
                showinfo("Error", "Please enter a valid number!")

        Button(deposit_window, text="confirm", command=confirm_deposit , bg='#0000b3', fg='white', font='MSSerif').pack(padx=6, pady=6, side='top')


    def add_product():
        add_window = Toplevel()
        add_window.title("Deposit")
        add_window.iconbitmap("tklogo.ico")
        add_window.configure(bg='black')

        Label(add_window, text="Each purchase includes a 10% tax", bg='black', fg='white', font='MSSerif').pack(padx=5, pady=5, side='top')


        Label(add_window, text="product name: ", bg='black', fg='white', font='MSSerif').pack(padx=5, pady=5, side='left')
        product_name_entery = Entry(add_window)
        product_name_entery.pack(pady=5, padx=5, side='left')

        Label(add_window, text="Enter the price of procuct: ", bg='black', fg='white', font='MSSerif').pack(padx=6, pady=6, side='left')
        product_price_entery = Entry(add_window)
        product_price_entery.pack(pady=6, padx=6, side='left')

        def confirm_product():
            product_name = product_name_entery.get()
            product_price = product_price_entery.get()
            product_price = float(product_price)
            product_name = product_name.capitalize()
            if (product_price > 0):
                fee_for = product_price * 0.10
                fee_for = round(fee_for, 2)
                price_and_fee = fee_for + product_price

                current_time = datetime.now()
                date_withdraw = current_time.strftime("%Y-%m-%d")
                time_withdraw = current_time.strftime("%H:%M:%S")

                showinfo("added succefully", f"price with fee: {price_and_fee}")

                conn = sqlite3.connect('Medipay_app.db')  
                cursor = conn.cursor()

                cursor.execute('SELECT user_id FROM users WHERE user_id = ?', (user_id,))
                user = cursor.fetchone()

                if user:
                    conn = sqlite3.connect('Medipay_app.db')  
                    cursor = conn.cursor()
                    cursor.execute('INSERT INTO products (productname, price, fee, user_id) VALUES (?,?,?,?)',(product_name, price_and_fee, fee_for, user_id))
                    cursor.execute('INSERT INTO Whithdraw_user (withdraw, date, time, user_id) VALUES (?,?,?,?)',(price_and_fee, date_withdraw, time_withdraw, user_id))
                    conn.commit()
                conn.close()

            else:
                showinfo("Invalid Amount", "You can't buy less than 1$!")


        Button(add_window, text="add", command=confirm_product, bg='#0000b3', fg='white', font='MSSerif').pack(padx=6, pady=6, side='top')
    
    def print_factor():
        print_window = Toplevel()
        print_window.title("Deposit")
        print_window.iconbitmap("tklogo.ico")
        print_window.configure(bg='black')

        Label(print_window, text="enter product ID to get the factor: ", bg='black', fg='white', font='MSSerif').pack(padx=5, pady=5, side='left')
        product_ID_entery = Entry(print_window)
        product_ID_entery.pack(pady=5, padx=5, side='left')

        def get_factor():
            productid = product_ID_entery.get()
            try:
                productid = int(productid)
                cursor.execute("SELECT * FROM products WHERE user_id = ? AND product_id = ?", (user_id, productid))
                product = cursor.fetchone()

                if product:
                    with open(f"D:/me/uni/semester 7/app test/project/products/product_{productid}.txt", "w") as f:
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

    dashboard_window = Tk()
    dashboard_window.title("Dashboard") 
    
    dashboard_window.iconbitmap("tklogo.ico")


    Button(dashboard_window, text="Products", command=view_products, bg='#0000b3', fg='white', font='MSSerif').pack(pady=10, padx=5)
    Button(dashboard_window, text="Payments", command=view_payments, bg='#0000b3', fg='white', font='MSSerif').pack(pady=10, padx=5)
    Button(dashboard_window, text="Deposit", command=Deposit_it, bg='#0000b3', fg='white', font='MSSerif').pack(pady=10, padx=5)
    Button(dashboard_window, text="add products", command=add_product, bg='#0000b3', fg='white', font='MSSerif').pack(pady=10, padx=5)
    Button(dashboard_window, text="get factor for product", command=print_factor, bg='#0000b3', fg='white', font='MSSerif').pack(pady=10, padx=5)

    dashboard_window.configure(bg='black')
    dashboard_window.geometry('500x400')

    dashboard_logo = PhotoImage(file="sublogo.png")
    label = Label(dashboard, image=dashboard_logo, bd=0, highlightthickness=0)
    label.image = dashboard_logo
    label.pack(side='top', pady=10)


    dashboard_window.mainloop()

if __name__ == "__main__":
    main_window()