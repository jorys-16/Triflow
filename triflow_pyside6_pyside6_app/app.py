"""
PySide6 implementation of the TriFlow desktop application.

This simple GUI ports the original Tkinter interface to PySide6.  It
provides three tabs: Tasks, Budget, and Weather.  Tasks and budgets
are stored in encrypted JSON files using Fernet encryption, via
functions in ``data/local_store.py``.

Features:
  - **Tasks tab** – list tasks in a table, add new tasks, mark them
    complete, edit descriptions, and delete tasks.  Each task
    persists to disk.
  - **Budget tab** – list expenses in a table, add a new expense
    (item and amount), delete expenses, and export to a JSON file.
  - **Weather tab** – placeholder for future weather integration.

The code is deliberately kept simple so you can extend it easily.  For
example, you might add theme support, i18n, or hook this GUI up to
Firebase authentication.
"""

import sys
from datetime import datetime
from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLineEdit,
    QTableWidget,
    QTableWidgetItem,
    QLabel,
    QTabWidget,
    QMessageBox,
    QInputDialog,
)

# Ensure we can import our local packages when running as a script.
BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))
if str(BASE_DIR / "data") not in sys.path:
    sys.path.insert(0, str(BASE_DIR / "data"))
if str(BASE_DIR / "core") not in sys.path:
    sys.path.insert(0, str(BASE_DIR / "core"))

from data import local_store


class TaskTab(QWidget):
    """Tab for managing tasks."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.tasks = local_store.load_tasks()
        self._build_ui()
        self.refresh_table()

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)

        # Table to display tasks
        self.table = QTableWidget(0, 3)
        self.table.setHorizontalHeaderLabels(["Description", "Status", "Created"])
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        self.table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.table)

        # Entry and buttons
        form_layout = QHBoxLayout()
        self.new_entry = QLineEdit()
        self.new_entry.setPlaceholderText("New task description…")
        form_layout.addWidget(self.new_entry)
        add_btn = QPushButton("Add Task")
        comp_btn = QPushButton("Mark Complete")
        edit_btn = QPushButton("Edit Task")
        del_btn = QPushButton("Delete Task")
        form_layout.addWidget(add_btn)
        form_layout.addWidget(comp_btn)
        form_layout.addWidget(edit_btn)
        form_layout.addWidget(del_btn)
        layout.addLayout(form_layout)

        # Button handlers
        add_btn.clicked.connect(self.add_task)
        comp_btn.clicked.connect(self.mark_complete)
        edit_btn.clicked.connect(self.edit_task)
        del_btn.clicked.connect(self.delete_task)

    def refresh_table(self) -> None:
        """Reload tasks from storage and update the table."""
        self.tasks = local_store.load_tasks()
        self.table.setRowCount(len(self.tasks))
        for row, task in enumerate(self.tasks):
            desc_item = QTableWidgetItem(task["description"])
            status_text = "✅ Done" if task["completed"] else "❌ Pending"
            status_item = QTableWidgetItem(status_text)
            created_item = QTableWidgetItem(task["created_at"][:10])
            desc_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            status_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            created_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.table.setItem(row, 0, desc_item)
            self.table.setItem(row, 1, status_item)
            self.table.setItem(row, 2, created_item)

    def add_task(self) -> None:
        desc = self.new_entry.text().strip()
        if not desc:
            QMessageBox.warning(self, "Input Error", "Task description cannot be empty.")
            return
        new_task = {
            "id": (self.tasks[-1]["id"] + 1) if self.tasks else 1,
            "description": desc,
            "completed": False,
            "created_at": datetime.now().isoformat(),
        }
        self.tasks.append(new_task)
        local_store.save_tasks(self.tasks)
        self.new_entry.clear()
        self.refresh_table()

    def _selected_task(self) -> tuple[int, dict] | None:
        idxs = self.table.selectionModel().selectedRows()
        if not idxs:
            return None
        row = idxs[0].row()
        return row, self.tasks[row]

    def mark_complete(self) -> None:
        sel = self._selected_task()
        if not sel:
            QMessageBox.warning(self, "Selection Error", "Please select a task to mark complete.")
            return
        row, task = sel
        task["completed"] = True
        local_store.save_tasks(self.tasks)
        self.refresh_table()

    def edit_task(self) -> None:
        sel = self._selected_task()
        if not sel:
            QMessageBox.warning(self, "Selection Error", "Please select a task to edit.")
            return
        row, task = sel
        new_desc, ok = QInputDialog.getText(self, "Edit Task", "Enter new description:", text=task["description"])
        if ok:
            new_desc = new_desc.strip()
            if not new_desc:
                QMessageBox.warning(self, "Input Error", "Task description cannot be empty.")
                return
            task["description"] = new_desc
            local_store.save_tasks(self.tasks)
            self.refresh_table()

    def delete_task(self) -> None:
        sel = self._selected_task()
        if not sel:
            QMessageBox.warning(self, "Selection Error", "Please select a task to delete.")
            return
        row, task = sel
        self.tasks.pop(row)
        local_store.save_tasks(self.tasks)
        self.refresh_table()


class BudgetTab(QWidget):
    """Tab for managing budgets/expenses."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.budgets = local_store.load_budgets()
        self._build_ui()
        self.refresh_table()

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)
        self.table = QTableWidget(0, 3)
        self.table.setHorizontalHeaderLabels(["Item", "Amount", "Date"])
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        self.table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.table)

        form_layout = QHBoxLayout()
        add_btn = QPushButton("Add Expense")
        del_btn = QPushButton("Delete")
        export_btn = QPushButton("Export")
        form_layout.addWidget(add_btn)
        form_layout.addWidget(del_btn)
        form_layout.addWidget(export_btn)
        layout.addLayout(form_layout)

        add_btn.clicked.connect(self.add_expense)
        del_btn.clicked.connect(self.delete_expense)
        export_btn.clicked.connect(self.export_expenses)

    def refresh_table(self) -> None:
        self.budgets = local_store.load_budgets()
        self.table.setRowCount(len(self.budgets))
        for row, exp in enumerate(self.budgets):
            item_item = QTableWidgetItem(exp["item"])
            amt_item = QTableWidgetItem(f"${exp['amount']:.2f}")
            date_item = QTableWidgetItem(exp["date"])
            item_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            amt_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            date_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.table.setItem(row, 0, item_item)
            self.table.setItem(row, 1, amt_item)
            self.table.setItem(row, 2, date_item)

    def add_expense(self) -> None:
        item, ok_item = QInputDialog.getText(self, "Add Expense", "Item:")
        if not ok_item or not item.strip():
            return
        amount_text, ok_amt = QInputDialog.getText(self, "Add Expense", "Amount (e.g., 3.50):")
        if not ok_amt:
            return
        try:
            amount = float(amount_text)
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Amount must be a valid number.")
            return
        exp = {
            "id": (self.budgets[-1]["id"] + 1) if self.budgets else 1,
            "item": item.strip(),
            "amount": amount,
            "date": datetime.now().date().isoformat(),
        }
        self.budgets.append(exp)
        local_store.save_budgets(self.budgets)
        self.refresh_table()

    def _selected_expense_row(self) -> int | None:
        idxs = self.table.selectionModel().selectedRows()
        if not idxs:
            return None
        return idxs[0].row()

    def delete_expense(self) -> None:
        row = self._selected_expense_row()
        if row is None:
            QMessageBox.warning(self, "Selection Error", "Please select an expense to delete.")
            return
        self.budgets.pop(row)
        local_store.save_budgets(self.budgets)
        self.refresh_table()

    def export_expenses(self) -> None:
        if not self.budgets:
            QMessageBox.information(self, "Export", "No expenses to export.")
            return
        local_store.export_budgets(self.budgets)
        QMessageBox.information(self, "Export", "Expenses exported to budgets_export.json.")


class WeatherTab(QWidget):
    """Placeholder tab for future weather integration."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        layout = QVBoxLayout(self)
        msg = QLabel("Weather feature coming soon!")
        msg.setAlignment(Qt.AlignCenter)
        layout.addWidget(msg)


class MainWindow(QMainWindow):
    """Main window hosting the tabbed interface."""

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("TriFlow (PySide6)")
        tabs = QTabWidget()
        tabs.addTab(TaskTab(), "Tasks")
        tabs.addTab(BudgetTab(), "Budget")
        tabs.addTab(WeatherTab(), "Weather")
        self.setCentralWidget(tabs)


def main() -> None:
    app = QApplication(sys.argv)
    win = MainWindow()
    win.resize(800, 600)
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()