"""
Main GUI interface for the TriFlow desktop app using Tkinter.

Features:
- ttk.Notebook for tabbed layout: Tasks, Budget, Weather (placeholder).
- TaskTab: Treeview with all tasks, add/mark/edit/delete tasks, persistent (encrypted) storage.
- BudgetTab: Treeview with expenses, add/delete/export, show total spent, persistent (encrypted) storage.
- WeatherTab: Placeholder for future extension.
- Messagebox used for error and validation alerts.

Tabs are implemented as their own classes, instantiated in the notebook.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

from core import task_tracker, budget_tracker
from core.utils import load_key

class TaskTab(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.key = load_key()
        self.tasks = task_tracker.load_tasks(self.key)
        self._create_widgets()
        self.refresh_tasks()

    def _create_widgets(self):
        # Treeview for tasks
        columns = ("Description", "Status", "Created")
        self.tree = ttk.Treeview(self, columns=columns, show="headings", selectmode="browse", height=12)
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120)
        self.tree.grid(row=0, column=0, columnspan=4, sticky="nsew", padx=10, pady=10)
        
        # Add new task Entry & Button
        self.new_task_var = tk.StringVar()
        ttk.Entry(self, textvariable=self.new_task_var, width=30).grid(row=1, column=0, padx=10, pady=2, sticky="w")
        ttk.Button(self, text="Add Task", command=self.add_task).grid(row=1, column=1, padx=2, pady=2, sticky="w")
        ttk.Button(self, text="Mark Complete", command=self.mark_complete).grid(row=1, column=2, padx=2, pady=2)
        ttk.Button(self, text="Edit Task", command=self.edit_task).grid(row=1, column=3, padx=2, pady=2)
        ttk.Button(self, text="Delete Task", command=self.delete_task).grid(row=1, column=4, padx=2, pady=2)

        # Configure resizing
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def refresh_tasks(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        self.tasks = task_tracker.load_tasks(self.key)
        for t in self.tasks:
            status = "✅ Done" if t["completed"] else "❌ Pending"
            self.tree.insert("", "end", iid=t["id"], values=(t["description"], status, t["created_at"][:10]))

    def add_task(self):
        desc = self.new_task_var.get().strip()
        if not desc:
            messagebox.showerror("Input Error", "Task description cannot be empty.")
            return
        task = {
            "id": (self.tasks[-1]["id"] + 1) if self.tasks else 1,
            "description": desc,
            "completed": False,
            "created_at": datetime.now().isoformat()
        }
        self.tasks.append(task)
        task_tracker.save_tasks(self.tasks, self.key)
        self.new_task_var.set("")
        self.refresh_tasks()

    def mark_complete(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Selection Error", "Please select a task to mark complete.")
            return
        tid = int(selected[0])
        found = False
        for t in self.tasks:
            if t["id"] == tid:
                t["completed"] = True
                found = True
                break
        if found:
            task_tracker.save_tasks(self.tasks, self.key)
            self.refresh_tasks()
        else:
            messagebox.showerror("Error", "Task not found.")

    def edit_task(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Selection Error", "Please select a task to edit.")
            return
        tid = int(selected[0])
        for t in self.tasks:
            if t["id"] == tid:
                new_desc = tk.simpledialog.askstring("Edit Task", "Enter new description:", initialvalue=t["description"])
                if new_desc is not None:
                    new_desc = new_desc.strip()
                    if not new_desc:
                        messagebox.showerror("Input Error", "Task description cannot be empty.")
                        return
                    t["description"] = new_desc
                    task_tracker.save_tasks(self.tasks, self.key)
                    self.refresh_tasks()
                return
        messagebox.showerror("Error", "Task not found.")

    def delete_task(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Selection Error", "Please select a task to delete.")
            return
        tid = int(selected[0])
        orig_len = len(self.tasks)
        self.tasks = [t for t in self.tasks if t["id"] != tid]
        if len(self.tasks) < orig_len:
            task_tracker.save_tasks(self.tasks, self.key)
            self.refresh_tasks()
        else:
            messagebox.showerror("Error", "Task not found.")

class BudgetTab(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.key = load_key()
        self.budgets = budget_tracker.load_budgets(self.key)
        self._create_widgets()
        self.refresh_budgets()

    def _create_widgets(self):
        columns = ("Item", "Amount", "Date")
        self.tree = ttk.Treeview(self, columns=columns, show="headings", selectmode="browse", height=12)
        for col in columns:
            self.tree.heading(col, text=col)
            if col == "Amount":
                self.tree.column(col, width=80, anchor="e")
            else:
                self.tree.column(col, width=120)
        self.tree.grid(row=0, column=0, columnspan=4, sticky="nsew", padx=10, pady=10)

        # Add new expense Entry & Button
        self.item_var = tk.StringVar()
        self.amount_var = tk.StringVar()
        ttk.Entry(self, textvariable=self.item_var, width=18).grid(row=1, column=0, padx=10, pady=2, sticky="w")
        ttk.Entry(self, textvariable=self.amount_var, width=10).grid(row=1, column=1, padx=2, pady=2, sticky="w")
        ttk.Button(self, text="Add Expense", command=self.add_expense).grid(row=1, column=2, padx=2, pady=2)
        ttk.Button(self, text="Delete", command=self.delete_expense).grid(row=1, column=3, padx=2, pady=2)
        ttk.Button(self, text="Export", command=self.export_expenses).grid(row=1, column=4, padx=2, pady=2)

        # Total spent label
        self.total_label = ttk.Label(self, text="Total Spent: $0.00", font=("Arial", 11, "bold"))
        self.total_label.grid(row=2, column=0, columnspan=3, sticky="w", padx=10, pady=6)

        # Configure resizing
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def refresh_budgets(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        self.budgets = budget_tracker.load_budgets(self.key)
        for b in self.budgets:
            self.tree.insert("", "end", iid=b["id"], values=(b["item"], f"${b['amount']:.2f}", b["date"]))
        total = sum(b["amount"] for b in self.budgets)
        self.total_label.config(text=f"Total Spent: ${total:.2f}")

    def add_expense(self):
        item = self.item_var.get().strip()
        if not item:
            messagebox.showerror("Input Error", "Expense name cannot be empty.")
            return
        try:
            amount = float(self.amount_var.get())
        except ValueError:
            messagebox.showerror("Input Error", "Amount must be a valid number.")
            return
        expense = {
            "id": (self.budgets[-1]["id"] + 1) if self.budgets else 1,
            "item": item,
            "amount": amount,
            "date": datetime.now().date().isoformat()
        }
        self.budgets.append(expense)
        budget_tracker.save_budgets(self.budgets, self.key)
        self.item_var.set("")
        self.amount_var.set("")
        self.refresh_budgets()

    def delete_expense(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Selection Error", "Please select an expense to delete.")
            return
        eid = int(selected[0])
        orig_len = len(self.budgets)
        self.budgets = [b for b in self.budgets if b["id"] != eid]
        if len(self.budgets) < orig_len:
            budget_tracker.save_budgets(self.budgets, self.key)
            self.refresh_budgets()
        else:
            messagebox.showerror("Error", "Expense not found.")

    def export_expenses(self):
        if not self.budgets:
            messagebox.showinfo("Export", "No expenses to export.")
            return
        budget_tracker.export_budgets(self.budgets)
        messagebox.showinfo("Export", "Expenses exported to budgets_export.json.")

class WeatherTab(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        ttk.Label(self, text="Weather feature coming soon!", font=("Arial", 14, "italic")).pack(pady=50)

class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("TriFlow")
        self.geometry("750x500")
        self._create_widgets()

    def _create_widgets(self):
        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True)

        self.task_tab = TaskTab(notebook)
        self.budget_tab = BudgetTab(notebook)
        self.weather_tab = WeatherTab(notebook)

        notebook.add(self.task_tab, text="Tasks")
        notebook.add(self.budget_tab, text="Budget")
        notebook.add(self.weather_tab, text="Weather")

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()