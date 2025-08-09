import os
from datetime import datetime
import json
from .utils import load_key, encrypt_data, decrypt_data

DATA_FILE = 'data/budgets.json.enc'

def load_budgets(key):
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, 'rb') as f:
        enc_data = f.read()
    return decrypt_data(enc_data, key)

def save_budgets(budgets, key):
    with open(DATA_FILE, 'wb') as f:
        f.write(encrypt_data(budgets, key))

def export_budgets(budgets):
    with open("budgets_export.json", "w") as f:
        json.dump(budgets, f, indent=4)
    print("Exported to budgets_export.json")

def run_cli():
    key = load_key()
    budgets = load_budgets(key)
    while True:
        print("\nWelcome to Budget Tracker!")
        print("1. View budget")
        print("2. Add expense")
        print("3. Remove expense")
        print("4. Export to JSON")
        print("5. Exit")
        choice = input("Choose an option: ")
        if choice == '1':
            if not budgets:
                print("No expenses found.")
            else:
                print(f"{'ID':>3} | {'Item':<15} | {'Amount':<8} | {'Date'}")
                print("-"*40)
                for b in budgets:
                    print(f"{b['id']:>3} | {b['item']:<15} | ${b['amount']:<7.2f} | {b['date']}")
                total = sum(b['amount'] for b in budgets)
                print(f"\nTotal Spent: ${total:.2f}")
        elif choice == '2':
            item = input("Enter expense name: ").strip()
            if not item:
                print("Expense name cannot be empty.")
                continue
            try:
                amount = float(input("Enter amount: "))
            except ValueError:
                print("Invalid number. Try again.")
                continue
            expense = {
                "id": (budgets[-1]["id"] + 1) if budgets else 1,
                "item": item,
                "amount": amount,
                "date": datetime.now().date().isoformat()
            }
            budgets.append(expense)
            save_budgets(budgets, key)
            print("Expense added!")
        elif choice == '3':
            try:
                eid = int(input("Enter expense id to remove: "))
            except ValueError:
                print("Please enter a valid number.")
                continue
            orig_len = len(budgets)
            budgets = [b for b in budgets if b["id"] != eid]
            if len(budgets) < orig_len:
                save_budgets(budgets, key)
                print("Expense removed!")
            else:
                print("Expense not found.")
        elif choice == '4':
            export_budgets(budgets)
        elif choice == '5':
            break
        else:
            print("Invalid option.")

if __name__ == '__main__':
    run_cli()