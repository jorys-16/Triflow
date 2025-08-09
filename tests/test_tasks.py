import unittest
import os
from core import task_tracker
from core.utils import load_key, encrypt_data, decrypt_data

class TestTaskTracker(unittest.TestCase):
    def setUp(self):
        self.key = load_key()
        self.test_file = "data/test_tasks.json.enc"
        self.original_data_file = task_tracker.DATA_FILE
        task_tracker.DATA_FILE = self.test_file
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
        task_tracker.DATA_FILE = self.original_data_file

    def test_add_and_load_task(self):
        tasks = []
        new_task = {
            "id": 1,
            "description": "Test Task",
            "completed": False,
            "created_at": "2025-01-01T00:00:00"
        }
        tasks.append(new_task)
        task_tracker.save_tasks(tasks, self.key)
        loaded = task_tracker.load_tasks(self.key)
        self.assertEqual(loaded[0]["description"], "Test Task")
        self.assertFalse(loaded[0]["completed"])

if __name__ == "__main__":
    unittest.main()