import os
from datetime import datetime
from .utils import load_key, encrypt_data, decrypt_data

DATA_FILE = 'data/tasks.json.enc'

def load_tasks(key):
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, 'rb') as f:
        enc_data = f.read()
    return decrypt_data(enc_data, key)

def save_tasks(tasks, key):
    with open(DATA_FILE, 'wb') as f:
        f.write(encrypt_data(tasks, key))

def run_cli():
    key = load_key()
    tasks = load_tasks(key)
    while True:
        print("\nWelcome to Task Tracker!")
        print("1. View tasks")
        print("2. Add task")
        print("3. Mark task as complete")
        print("4. Delete task")
        print("5. Edit task description")
        print("6. Exit")
        choice = input("Choose an option: ")
        if choice == '1':
            if not tasks:
                print("No tasks found.")
            else:
                # Print header
                print(f"{'ID':>3} | {'Description':<25} | {'Status':<10} | {'Created'}")
                print("-" * 60)
                for t in tasks:
                    status = "✅ Done" if t["completed"] else "❌ Pending"
                    print(f"{t['id']:>3} | {t['description']:<25} | {status:<10} | {t['created_at'][:10]}")
                total = len(tasks)
                done = sum(1 for t in tasks if t["completed"])
                print(f"\n{done}/{total} tasks completed.")
        elif choice == '2':
            desc = input("Enter task description: ").strip()
            if not desc:
                print("Task description cannot be empty.")
                continue
            task = {
                "id": (tasks[-1]["id"] + 1) if tasks else 1,
                "description": desc,
                "completed": False,
                "created_at": datetime.now().isoformat()
            }
            tasks.append(task)
            save_tasks(tasks, key)
            print("Task added!")
        elif choice == '3':
            try:
                tid = int(input("Enter task id to complete: "))
            except ValueError:
                print("Please enter a valid number.")
                continue
            found = False
            for t in tasks:
                if t["id"] == tid:
                    t["completed"] = True
                    found = True
                    print("Task marked complete!")
            if not found:
                print("Task not found.")
            save_tasks(tasks, key)
        elif choice == '4':
            try:
                tid = int(input("Enter task id to delete: "))
            except ValueError:
                print("Please enter a valid number.")
                continue
            orig_len = len(tasks)
            tasks = [t for t in tasks if t["id"] != tid]
            if len(tasks) < orig_len:
                save_tasks(tasks, key)
                print("Task deleted!")
            else:
                print("Task not found.")
        elif choice == '5':
            try:
                tid = int(input("Enter task id to edit: "))
            except ValueError:
                print("Please enter a valid number.")
                continue
            for t in tasks:
                if t["id"] == tid:
                    new_desc = input("Enter new description: ").strip()
                    if not new_desc:
                        print("Task description cannot be empty.")
                        break
                    t["description"] = new_desc
                    print("Task updated.")
                    break
            else:
                print("Task not found.")
            save_tasks(tasks, key)
        elif choice == '6':
            break
        else:
            print("Invalid option.")

if __name__ == '__main__':
    run_cli()