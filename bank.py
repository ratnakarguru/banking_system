import os
import csv
import customtkinter as ctk
from customtkinter import CTkLabel, CTkEntry, CTkButton, CTkSwitch, CTkOptionMenu, CTkTextbox, CTkFrame, CTkImage
import tkinter.messagebox as messagebox
from tkinter import filedialog
from PIL import Image, ImageTk
from datetime import datetime

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class Account:
    def __init__(self, name, account_number, initial_balance=0):
        self.name = name
        self.account_number = account_number
        self.balance = initial_balance
        # self.update_account_menus()

        self.history = []
        self.history.append((datetime.now(), "OPEN", initial_balance, initial_balance))

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            self.history.append((datetime.now(), "DEPOSIT", amount, self.balance))
            return f"₹{amount} deposited. New balance: ₹{self.balance}"
        else:
            return "Deposit amount must be greater than zero."

    def withdraw(self, amount):
        if 0 < amount <= self.balance:
            self.balance -= amount
            self.history.append((datetime.now(), "WITHDRAW", amount, self.balance))
            return f"₹{amount} withdrawn. New balance: ₹{self.balance}"
        else:
            return "Insufficient balance or invalid amount."

    def get_balance(self):
        return self.balance

    def get_history(self):
        lines = []
        for dt, typ, amt, bal in self.history:
            ts = dt.strftime("%Y-%m-%d %H:%M:%S")
            lines.append(f"{ts} | {typ:<8} | ₹{amt:<10} | Bal: ₹{bal}")
        return lines

class BankingSystem:
    def __init__(self):
        self.accounts = {}

    def create_account(self, name, account_number, initial_balance=0):
        if account_number in self.accounts:
            return "Account number already exists."
        new_acct = Account(name, account_number, initial_balance)
        self.accounts[account_number] = new_acct
        return f"Account created for {name}. Account Number: {account_number}, Balance: ₹{initial_balance}"

    def deposit_to_account(self, account_number, amount):
        acct = self.accounts.get(account_number)
        if acct:
            return acct.deposit(amount)
        return "Account number not found."

    def withdraw_from_account(self, account_number, amount):
        acct = self.accounts.get(account_number)
        if acct:
            return acct.withdraw(amount)
        return "Account number not found."

    def check_balance(self, account_number):
        acct = self.accounts.get(account_number)
        if acct:
            return f"Balance for Account {account_number} ({acct.name}): ₹{acct.get_balance()}"
        return "Account number not found."

    def delete_account(self, account_number):
        if account_number in self.accounts:
            del self.accounts[account_number]
            return f"Account {account_number} deleted."
        return "Account number not found."

    def get_account_list(self):
        return list(self.accounts.keys())

    def filter_accounts(self, substring):
        return [acc for acc in self.accounts.keys() if substring in acc]

class AdvancedBankingApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.bank_system = BankingSystem()
        self.title("Advanced Banking System")
        self.geometry("900x650")
        self.minsize(650, 500)

        # Top frame
        top = CTkFrame(self)
        top.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=10, pady=5)
        top.grid_columnconfigure(0, weight=1)
        top.grid_columnconfigure(1, weight=0)

        header = CTkLabel(top, text="Advanced Banking System", font=("Arial", 24, "bold"))
        header.grid(row=0, column=0, sticky="w")

        self.mode_switch = CTkSwitch(top, text="", command=self.toggle_mode)
        self.mode_switch.grid(row=0, column=1, sticky="e")
        self.mode_switch.select()

        # Left: Tabs
        from customtkinter import CTkTabview
        self.tabview = CTkTabview(self)
        self.tabview.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)
        self.tabview.grid_rowconfigure(0, weight=1)
        self.tabview.grid_columnconfigure(0, weight=1)

        for name in ["Create", "Deposit", "Withdraw", "Check / History", "Search / Delete"]:
            self.tabview.add(name)

        self._build_create_tab(self.tabview.tab("Create"))
        self._build_deposit_tab(self.tabview.tab("Deposit"))
        self._build_withdraw_tab(self.tabview.tab("Withdraw"))
        self._build_check_tab(self.tabview.tab("Check / History"))
        self._build_search_delete_tab(self.tabview.tab("Search / Delete"))

        # Right: optional side panel (for small screens or info)
        side = CTkFrame(self)
        side.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)
        side.grid_rowconfigure(0, weight=1)
        self.info_label = CTkLabel(side, text="Select a tab to perform actions", wraplength=200, justify="left")
        self.info_label.grid(row=0, column=0, sticky="nw")

        # Bottom: log
        bottom = CTkFrame(self)
        bottom.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=10, pady=5)
        bottom.grid_columnconfigure(0, weight=1)
        bottom.grid_rowconfigure(0, weight=1)

        self.log_text = CTkTextbox(bottom, wrap="word")
        self.log_text.grid(row=0, column=0, sticky="nsew")

        clear_btn = CTkButton(bottom, text="Clear Log", command=self.clear_log)
        clear_btn.grid(row=1, column=0, pady=5, sticky="e")

        # Configure root grid
        self.grid_columnconfigure(0, weight=3)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.update_account_menus()

    def toggle_mode(self):
        cur = ctk.get_appearance_mode()
        ctk.set_appearance_mode("Dark" if cur == "Light" else "Light")

    def log_message(self, msg):
        self.log_text.insert("end", msg + "\n")
        self.log_text.see("end")

    def clear_log(self):
        self.log_text.delete("0.0", "end")

    def update_account_menus(self):
        accts = self.bank_system.get_account_list()
        vals = accts if accts else ["No accounts yet"]
        self.deposit_acc_menu.configure(values=vals)
        self.withdraw_acc_menu.configure(values=vals)
        self.check_acc_menu.configure(values=vals)
        self.search_delete_menu.configure(values=vals)

        state = "normal" if accts else "disabled"
        self.deposit_btn.configure(state=state)
        self.withdraw_btn.configure(state=state)
        self.check_btn.configure(state=state)
        self.delete_btn.configure(state=state)

    def _build_create_tab(self, frame):
        frame.grid_columnconfigure(1, weight=1)
        CTkLabel(frame, text="Name:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.create_name_entry = CTkEntry(frame)
        self.create_name_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        CTkLabel(frame, text="Account Number:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.create_acc_entry = CTkEntry(frame)
        self.create_acc_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        CTkLabel(frame, text="Initial Balance (₹):").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.create_bal_entry = CTkEntry(frame)
        self.create_bal_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        self.create_error_lbl = CTkLabel(frame, text="", text_color="red")
        self.create_error_lbl.grid(row=3, column=0, columnspan=2, sticky="w", padx=5)

        btn = CTkButton(frame, text="Create Account", command=self.create_account)
        btn.grid(row=4, column=0, columnspan=2, pady=10)

    def _build_deposit_tab(self, frame):
        frame.grid_columnconfigure(1, weight=1)
        CTkLabel(frame, text="Select Account:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.deposit_acc_menu = CTkOptionMenu(frame, values=["No accounts yet"])
        self.deposit_acc_menu.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        CTkLabel(frame, text="Amount (₹):").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.deposit_amt_entry = CTkEntry(frame)
        self.deposit_amt_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        self.deposit_error_lbl = CTkLabel(frame, text="", text_color="red")
        self.deposit_error_lbl.grid(row=2, column=0, columnspan=2, sticky="w", padx=5)

        self.deposit_btn = CTkButton(frame, text="Deposit", command=self.deposit_money)
        self.deposit_btn.grid(row=3, column=0, columnspan=2, pady=10)

    def _build_withdraw_tab(self, frame):
        frame.grid_columnconfigure(1, weight=1)
        CTkLabel(frame, text="Select Account:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.withdraw_acc_menu = CTkOptionMenu(frame, values=["No accounts yet"])
        self.withdraw_acc_menu.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        CTkLabel(frame, text="Amount (₹):").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.withdraw_amt_entry = CTkEntry(frame)
        self.withdraw_amt_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        self.withdraw_error_lbl = CTkLabel(frame, text="", text_color="red")
        self.withdraw_error_lbl.grid(row=2, column=0, columnspan=2, sticky="w", padx=5)

        self.withdraw_btn = CTkButton(frame, text="Withdraw", command=self.withdraw_money)
        self.withdraw_btn.grid(row=3, column=0, columnspan=2, pady=10)

    def _build_check_tab(self, frame):
        frame.grid_columnconfigure(1, weight=1)
        CTkLabel(frame, text="Select Account:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.check_acc_menu = CTkOptionMenu(frame, values=["No accounts yet"])
        self.check_acc_menu.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        self.check_btn = CTkButton(frame, text="Check Balance / History", command=self.show_history_and_export)
        self.check_btn.grid(row=1, column=0, columnspan=2, pady=10)

        self.history_text = CTkTextbox(frame, height=10, wrap="word")
        self.history_text.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)
        frame.grid_rowconfigure(2, weight=1)

        # Button to export history
        self.export_btn = CTkButton(frame, text="Export History", command=self.export_history)
        self.export_btn.grid(row=3, column=0, columnspan=2, pady=5)

    def _build_search_delete_tab(self, frame):
        frame.grid_columnconfigure(1, weight=1)
        
        CTkLabel(frame, text="Search / Filter by Account #:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.search_entry = CTkEntry(frame)
        self.search_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        self.search_btn = CTkButton(frame, text="Search", command=self.search_accounts)
        self.search_btn.grid(row=1, column=0, columnspan=2, pady=5)

        self.search_results_text = CTkTextbox(frame, height=8, wrap="word")
        self.search_results_text.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)
        frame.grid_rowconfigure(2, weight=1)

        # ✅ Add this dropdown for deletion
        CTkLabel(frame, text="Select Account to Delete:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.search_delete_menu = CTkOptionMenu(frame, values=["No accounts yet"])
        self.search_delete_menu.grid(row=3, column=1, padx=5, pady=5, sticky="ew")

        self.delete_btn = CTkButton(frame, text="Delete Selected Account", command=self.delete_account)
        self.delete_btn.grid(row=4, column=0, columnspan=2, pady=10)


    def create_account(self):
        name = self.create_name_entry.get().strip()
        acc = self.create_acc_entry.get().strip()
        bal_text = self.create_bal_entry.get().strip()
        self.create_error_lbl.configure(text="")

        if not name or not acc:
            self.create_error_lbl.configure(text="Name & Account Number required.")
            return

        try:
            bal = float(bal_text)
            if bal < 0:
                raise ValueError
        except ValueError:
            self.create_error_lbl.configure(text="Invalid balance.")
            return

        result = self.bank_system.create_account(name, acc, bal)
        self.log_message(result)
        messagebox.showinfo("Result", result)
        self.create_name_entry.delete(0, "end")
        self.create_acc_entry.delete(0, "end")
        self.create_bal_entry.delete(0, "end")
        self.update_account_menus()

    def deposit_money(self):
        acc = self.deposit_acc_menu.get()
        self.deposit_error_lbl.configure(text="")
        if not self.bank_system.get_account_list():
            return
        try:
            amt = float(self.deposit_amt_entry.get())
            if amt <= 0:
                raise ValueError
        except:
            self.deposit_error_lbl.configure(text="Enter a valid amount.")
            return

        result = self.bank_system.deposit_to_account(acc, amt)
        self.log_message(result)
        messagebox.showinfo("Result", result)
        # Low balance alert
        if self.bank_system.accounts[acc].get_balance() < 50:  # threshold
            messagebox.showwarning("Low Balance", "Your balance is low!")
        self.deposit_amt_entry.delete(0, "end")
        self.update_account_menus()

    def withdraw_money(self):
        acc = self.withdraw_acc_menu.get()
        self.withdraw_error_lbl.configure(text="")
        if not self.bank_system.get_account_list():
            return
        try:
            amt = float(self.withdraw_amt_entry.get())
            if amt <= 0:
                raise ValueError
        except:
            self.withdraw_error_lbl.configure(text="Enter a valid amount.")
            return

        result = self.bank_system.withdraw_from_account(acc, amt)
        self.log_message(result)
        messagebox.showinfo("Result", result)
        if acc in self.bank_system.accounts and self.bank_system.accounts[acc].get_balance() < 50:
            messagebox.showwarning("Low Balance", "Your balance is low!")
        self.withdraw_amt_entry.delete(0, "end")
        self.update_account_menus()

    def show_history_and_export(self):
        acc = self.check_acc_menu.get()
        if not self.bank_system.get_account_list():
            return
        # Show balance + history
        result = self.bank_system.check_balance(acc)
        hist = self.bank_system.accounts[acc].get_history()
        self.history_text.delete("0.0", "end")
        self.history_text.insert("end", result + "\n\nTransaction History:\n")
        for line in hist:
            self.history_text.insert("end", line + "\n")
        self.log_message(result)

    def export_history(self):
        acc = self.check_acc_menu.get()
        if acc not in self.bank_system.accounts:
            messagebox.showerror("Error", "No valid account selected.")
            return
        # Ask for filename
        fpath = filedialog.asksaveasfilename(defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("Text files", "*.txt")])
        if not fpath:
            return
        try:
            with open(fpath, mode="w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["Timestamp", "Type", "Amount", "Balance"])
                for dt, typ, amt, bal in self.bank_system.accounts[acc].history:
                    writer.writerow([dt.strftime("%Y-%m-%d %H:%M:%S"), typ, amt, bal])
            messagebox.showinfo("Export", f"History exported to {fpath}")
        except Exception as e:
            messagebox.showerror("Export Failed", str(e))

    def search_accounts(self):
        q = self.search_entry.get().strip()
        self.search_results_text.delete("0.0", "end")
        if not q:
            self.search_results_text.insert("end", "Enter part of account number to search.")
            return
        results = self.bank_system.filter_accounts(q)
        if not results:
            self.search_results_text.insert("end", "No matches found.")
        else:
            self.search_results_text.insert("end", "Matches:\n")
            for acc in results:
                name = self.bank_system.accounts[acc].name
                bal = self.bank_system.accounts[acc].get_balance()
                self.search_results_text.insert("end", f"{acc} — {name} — ₹{bal}\n")

    def delete_account(self):
        acc = self.search_delete_menu.get() if hasattr(self, "search_delete_menu") else None
        # Alternatively, you can allow entering a number to delete
        acc = self.deposit_acc_menu.get()  # or some menu to pick
        confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete account {acc}?")
        if not confirm:
            return
        result = self.bank_system.delete_account(acc)
        self.log_message(result)
        messagebox.showinfo("Result", result)
        self.update_account_menus()

if __name__ == "__main__":
    app = AdvancedBankingApp()
    app.mainloop()
