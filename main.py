import tkinter as tk
from tkinter import ttk  # Import ttk for Treeview
from tkinter import messagebox
from datetime import datetime
import mysql.connector as mysql

# Global MySQL Connection
conn = mysql.connect(host='localhost', user='root', password='manager', database='bank')
rec = conn.cursor()

# Main Application Window
class BankApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Bank Management System")
        self.create_main_menu()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def create_main_menu(self):
        self.clear_window()
        tk.Label(self.root, text="____M A I N   M E N U____", font=("Arial", 16)).pack(pady=20)
        tk.Button(self.root, text="Bank Services", command=self.bank_services, width=20).pack(pady=5)
        tk.Button(self.root, text="Transaction", command=self.transaction, width=20).pack(pady=5)
        tk.Button(self.root, text="Reports", command=self.reports, width=20).pack(pady=5)
        tk.Button(self.root, text="Exit", command=self.exit_application, width=20).pack(pady=5)

    def bank_services(self):
        self.clear_window()
        tk.Label(self.root, text="B A N K   S E R V I C E S", font=("Arial", 16)).pack(pady=20)
        tk.Button(self.root, text="Create an Account", command=self.create_account, width=20).pack(pady=5)
        tk.Button(self.root, text="Display an Account", command=self.display_account, width=20).pack(pady=5)
        tk.Button(self.root, text="Delete an Account", command=self.delete_account, width=20).pack(pady=5)
        tk.Button(self.root, text="Return to Main Menu", command=self.create_main_menu, width=20).pack(pady=5)

    def create_account(self):
        self.clear_window()
        tk.Label(self.root, text="Create Account", font=("Arial", 16)).pack(pady=20)
        labels = ["Account No:", "Name:", "Account Type (Saving/Current):", "Address 1:", "Address 2:", "City:", "Opening Balance:"]
        self.entries = {}
        for label in labels:
            tk.Label(self.root, text=label).pack()
            entry = tk.Entry(self.root)
            entry.pack(pady=5)
            self.entries[label] = entry
        tk.Button(self.root, text="Submit", command=self.save_account).pack(pady=20)
        tk.Button(self.root, text="Back", command=self.bank_services).pack(pady=5)

    def save_account(self):
        try:
            a = int(self.entries["Account No:"].get())
            b = self.entries["Name:"].get()
            c = self.entries["Account Type (Saving/Current):"].get()
            d = datetime.now().date()
            e = self.entries["Address 1:"].get()
            f = self.entries["Address 2:"].get()
            g = self.entries["City:"].get()
            h = int(self.entries["Opening Balance:"].get())

            sql = """CREATE TABLE IF NOT EXISTS accountmaster (
                Account_Number INTEGER PRIMARY KEY, 
                name CHAR(40), 
                Account_Type CHAR(40), 
                DateOfOpening DATE, 
                Address_1 CHAR(100), 
                Address_2 CHAR(100), 
                City CHAR(20), 
                Opening_Balance INTEGER
            )"""
            rec.execute(sql)
            conn.commit()

            sql_insert = "INSERT INTO accountmaster VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            rec.execute(sql_insert, (a, b, c, d, e, f, g, h))
            conn.commit()
            messagebox.showinfo("Success", "Account created successfully!")
            self.bank_services()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def display_account(self):
        self.clear_window()
        tk.Label(self.root, text="Display Account", font=("Arial", 16)).pack(pady=20)
        tk.Label(self.root, text="Enter Account No:").pack()
        account_entry = tk.Entry(self.root)
        account_entry.pack(pady=5)

        def show_account():
            try:
                a = int(account_entry.get())
                sql = "SELECT * FROM accountmaster WHERE Account_Number = %s"
                rec.execute(sql, (a,))
                data = rec.fetchall()
                if data:
                    self.show_table(data, ["Account Number", "Name", "Account Type", "Date of Opening", 
                                           "Address 1", "Address 2", "City", "Opening Balance"])
                else:
                    tk.Label(self.root, text="Account not found.", fg="red").pack(pady=10)
            except Exception as e:
                tk.Label(self.root, text=f"Error: {e}", fg="red").pack(pady=10)

        tk.Button(self.root, text="Search", command=show_account).pack(pady=20)
        tk.Button(self.root, text="Back", command=self.bank_services).pack(pady=5)

    def delete_account(self):
        self.clear_window()
        tk.Label(self.root, text="Delete Account", font=("Arial", 16)).pack(pady=20)
        tk.Label(self.root, text="Enter Account No:").pack()
        account_entry = tk.Entry(self.root)
        account_entry.pack(pady=5)

        def remove_account():
            try:
                a = int(account_entry.get())
                sql_check = "SELECT * FROM accountmaster WHERE Account_Number = %s"
                rec.execute(sql_check, (a,))
                no = rec.fetchone()
                if no is None:
                    tk.Label(self.root, text="Account not found.", fg="red").pack(pady=10)
                else:
                    sql_delete = "DELETE FROM accountmaster WHERE Account_Number = %s"
                    rec.execute(sql_delete, (a,))
                    conn.commit()
                    tk.Label(self.root, text="Account deleted successfully!", fg="green").pack(pady=10)
            except Exception as e:
                tk.Label(self.root, text=f"Error: {e}", fg="red").pack(pady=10)

        tk.Button(self.root, text="Delete", command=remove_account).pack(pady=20)
        tk.Button(self.root, text="Back", command=self.bank_services).pack(pady=5)

    def transaction(self):
        self.clear_window()
        tk.Label(self.root, text="Transaction", font=("Arial", 16)).pack(pady=20)

        tk.Label(self.root, text="Enter Account No:").pack()
        account_entry = tk.Entry(self.root)
        account_entry.pack(pady=5)

        tk.Label(self.root, text="Enter ('W' for Withdrawal / 'D' for Deposit):").pack()
        type_entry = tk.Entry(self.root)
        type_entry.pack(pady=5)

        tk.Label(self.root, text="Enter Amount:").pack()
        amount_entry = tk.Entry(self.root)
        amount_entry.pack(pady=5)

        def process_transaction():
            try:
                a = int(account_entry.get())
                t_type = type_entry.get().upper()
                amt = int(amount_entry.get())
                d = datetime.now().date()

                if t_type not in ['W', 'D']:
                    raise ValueError("Invalid transaction type.")

                sql_check = "SELECT Opening_Balance FROM accountmaster WHERE Account_Number = %s"
                rec.execute(sql_check, (a,))
                bal = rec.fetchone()

                if bal is None:
                    raise ValueError("Account not found.")

                bal = bal[0]

                if t_type == 'W':
                    if amt > bal:
                        raise ValueError("Insufficient balance.")
                    new_balance = bal - amt
                elif t_type == 'D':
                    new_balance = bal + amt

                sql_update = "UPDATE accountmaster SET Opening_Balance = %s WHERE Account_Number = %s"
                rec.execute(sql_update, (new_balance, a))

                sql_trans = """CREATE TABLE IF NOT EXISTS Transaction (
                    Account_Number INTEGER,
                    Date DATE,
                    Transaction_Type CHAR(1),
                    Amount INTEGER
                )"""
                rec.execute(sql_trans)

                sql_insert_trans = "INSERT INTO Transaction VALUES (%s, %s, %s, %s)"
                rec.execute(sql_insert_trans, (a, d, t_type, amt))

                conn.commit()
                messagebox.showinfo("Success", "Transaction successful!")
                self.create_main_menu()
            except Exception as e:
                messagebox.showerror("Error", str(e))

        tk.Button(self.root, text="Submit", command=process_transaction).pack(pady=20)
        tk.Button(self.root, text="Back", command=self.create_main_menu).pack(pady=5)


    def reports(self):
        self.clear_window()
        tk.Label(self.root, text="Reports", font=("Arial", 16)).pack(pady=20)
        tk.Button(self.root, text="Account List", command=self.account_list, width=20).pack(pady=5)
        tk.Button(self.root, text="Back to Main Menu", command=self.create_main_menu, width=20).pack(pady=5)

    def reports(self):
        self.clear_window()
        tk.Label(self.root, text="Reports", font=("Arial", 16)).pack(pady=20)
        tk.Button(self.root, text="Account List", command=self.account_list, width=20).pack(pady=5)
        tk.Button(self.root, text="Individual Account List", command=self.individual_list, width=20).pack(pady=5)
        tk.Button(self.root, text="Back to Main Menu", command=self.create_main_menu, width=20).pack(pady=5)

    def account_list(self):
        self.clear_window()
        tk.Label(self.root, text="Account List", font=("Arial", 16)).pack(pady=20)
        try:
            sql = "SELECT * FROM accountmaster"
            rec.execute(sql)
            data = rec.fetchall()
            if not data:
                messagebox.showinfo("Info", "No accounts found.")
                self.reports()
                return
            self.show_table(data, ["Account Number", "Name", "Account Type", "Date of Opening", 
                                   "Address 1", "Address 2", "City", "Opening Balance"])
        except Exception as e:
            messagebox.showerror("Error", str(e))
        tk.Button(self.root, text="Back", command=self.reports).pack(pady=20)

    def individual_list(self):
        self.clear_window()
        tk.Label(self.root, text="Individual Account List", font=("Arial", 16)).pack(pady=20)
        tk.Button(self.root, text="Current Statement", command=self.current_list, width=20).pack(pady=5)
        tk.Button(self.root, text="Mini Statement", command=self.mini_list, width=20).pack(pady=5)
        tk.Button(self.root, text="Back to Reports", command=self.reports, width=20).pack(pady=5)

    def current_list(self):
        self.clear_window()
        tk.Label(self.root, text="Current Statement", font=("Arial", 16)).pack(pady=20)
        tk.Label(self.root, text="Enter Account No:").pack()
        account_entry = tk.Entry(self.root)
        account_entry.pack(pady=5)

        def show_current():
            try:
                a = int(account_entry.get())
                sql = "SELECT DISTINCT name, Account_Type, Opening_Balance FROM accountmaster WHERE Account_Number = %s"
                rec.execute(sql, (a,))
                data = rec.fetchall()
                if not data:
                    messagebox.showinfo("Not Found", "Account not found.")
                    return
                # Show data in a Treeview
                self.show_table(data, ["Name", "Account Type", "Opening Balance"])
            except Exception as e:
                messagebox.showerror("Error", str(e))

        tk.Button(self.root, text="Search", command=show_current).pack(pady=20)
        tk.Button(self.root, text="Back", command=self.individual_list).pack(pady=5)

    def mini_list(self):
        self.clear_window()
        tk.Label(self.root, text="Mini Statement", font=("Arial", 16)).pack(pady=20)
        tk.Label(self.root, text="Enter Account No:").pack()
        account_entry = tk.Entry(self.root)
        account_entry.pack(pady=5)

        def show_mini():
            try:
                account_number = int(account_entry.get())
                # Correct SQL query with the actual column names
                sql = "SELECT Date_Of_Transaction, Transaction_Type, Amount FROM Transaction WHERE Account_Number = %s"
                rec.execute(sql, (account_number,))
                data = rec.fetchall()

                if not data:
                    messagebox.showinfo("Not Found", "No transactions found.")
                    return

                # Show data in a Treeview using the helper function
                self.show_table(data, ["Date", "Type", "Amount"])
            except Exception as e:
                messagebox.showerror("Error", str(e))

        tk.Button(self.root, text="Search", command=show_mini).pack(pady=20)
        tk.Button(self.root, text="Back", command=self.individual_list).pack(pady=5)



    def show_table(self, data, columns):
        tree = ttk.Treeview(self.root, columns=columns, show="headings")
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150, anchor='center')
        for row in data:
            tree.insert("", tk.END, values=row)
        tree.pack(fill=tk.BOTH, expand=True, pady=10)

    def exit_application(self):
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = BankApp(root)
    root.mainloop()
