import unittest
import os
from core import budget_tracker
from core.utils import load_key, encrypt_data, decrypt_data

class TestBudgetTracker(unittest.TestCase):
    def setUp(self):
        self.key = load_key()
        self.test_file = "data/test_budgets.json.enc"
        self.original_data_file = budget_tracker.DATA_FILE
        budget_tracker.DATA_FILE = self.test_file
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
        budget_tracker.DATA_FILE = self.original_data_file

    def test_add_and_load_expense(self):
        budgets = []
        new_expense = {
            "id": 1,
            "item": "Coffee",
            "amount": 2.5,
            "date": "2025-01-01"
        }
        budgets.append(new_expense)
        budget_tracker.save_budgets(budgets, self.key)
        loaded = budget_tracker.load_budgets(self.key)
        self.assertEqual(loaded[0]["item"], "Coffee")
        self.assertEqual(loaded[0]["amount"], 2.5)

if __name__ == "__main__":
    unittest.main()