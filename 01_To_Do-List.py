import json
import os
from datetime import datetime, date

TASK_FILE = "tasks.json"

# load and save the task
def load_tasks():
    if os.path.exists(TASK_FILE):
        try:
            with open(TASK_FILE, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []
    return []

def save_tasks(tasks):
    with open(TASK_FILE, "w") as f:
        json.dump(tasks, f, indent=4)

# Add tasks
def add_task(tasks, next_id):
    while True:
        task_name = input("Enter task: ")

        if task_name == "":
            print("Task cannot be empty! Please enter a valid task.")
            continue

        if not any(char.isalpha() for char in task_name):
            print("Task must contain at least one alphabet character!")
            continue

        break  # Valid task name, exit the loop

    while True:
        deadline_input = input("Enter deadline (YYYY-MM-DD): ")

        if deadline_input == "":
            print("Deadline cannot be empty! Please enter a valid deadline.")
            continue

        try:
            datetime.strptime(deadline_input, "%Y-%m-%d")
            break  # Valid format, exit the loop
        except ValueError:
            print("Invalid date format! Please enter in YYYY-MM-DD format.")

    priority = input("Enter priority (low/medium/high): ").lower()

    if priority not in ['low', 'medium', 'high']:
        print("Invalid priority! Defaulting to low.")
        priority = "low"
        
    tasks.append({
        "id": next_id,
        "task": task_name,
        "done": False,
        "deadline": deadline_input,
        "priority": priority
    })

    save_tasks(tasks)
    print("Task added successfully!")

    return next_id + 1

# view + sort tasks 
def sort_tasks(tasks):
    priority_map = {"high": 3, "medium": 2, "low": 1}

    def sort_key(task):
        deadline = datetime.strptime(task["deadline"], "%Y-%m-%d")
        priority = priority_map.get(task["priority"], 1)
        return (-priority, deadline)
    tasks.sort(key=sort_key)

def view_tasks(tasks):
    if not tasks:
        print("No tasks found!")
        return
    
    sort_tasks(tasks)
    
    print("=== Task List ===")
    for task in tasks:
        status = "✔" if task['done'] else "❌"
        print(f"{task['id']}. {task['task']} [{status}] "
              f"| Priority: {task['priority']} | Deadline: {task['deadline']}")

# Deadline Dashboard
def show_deadline_dashboard(tasks):
    today = date.today()

    print("Deadline Dashboard")

    for task in tasks:
        if task['done']:
            print(f"{task['id']}. {task['task']} ✔ DONE")
            continue

        deadline = datetime.strptime(task["deadline"], "%Y-%m-%d").date()
        days_left = (deadline - today).days

        if days_left < 0:
            status = f"Overdue ({abs(days_left)} days late!)"
        elif days_left == 0:
            status = "Due Today!"
        elif days_left == 1:
            status = "Due Tomorrow"
        else:
            status = f"{days_left} days left!"

        print(f"{task['id']}. {task['task']} [{status}]")

# Mark complete
def mark_completed(tasks):
    try:
        task_id = int(input("Enter task ID to mark completed: "))

        for task in tasks:
            if task["id"] == task_id:
                task['done'] = True
                save_tasks(tasks)
                print("Task marked as completed ✔!")
                return

        print("Task not found")
    except ValueError:
        print("Invalid input!")

# Edit task
def edit_task(tasks):
    try:
        task_id = int(input("Enter task ID to edit: "))

        for task in tasks:
            if task["id"] == task_id:
                task["task"] = input("Enter new task: ")
                save_tasks(tasks)
                print("Task updated!")
                return
        
        print("Task not found!")

    except ValueError:
        print("Invalid input!")

# Clear all tasks
def clear_tasks(tasks):
    confirm = input("Are your sure? (Y/N): ").strip().lower()

    if confirm.lower() == "y":
        tasks.clear()
        save_tasks(tasks)
        print("All tasks cleared!")

# Weekly summary
def weekly_summary(tasks):
    today = date.today()

    completed = 0
    pending = 0
    overdue = 0

    for task in tasks:
        deadline = datetime.strptime(task["deadline"], "%Y-%m-%d").date()

        if task['done']:
            completed += 1
        else:
            if deadline < today:
                overdue += 1
            else:
                pending += 1

    print("Weekly Summary!")
    print(f"Completed: {completed}")
    print(f"Pending: {pending}")
    print(f"Overdue: {overdue}")


# Main Menu
def main():
    tasks = load_tasks()

    if tasks:
        next_id = max(task["id"] for task in tasks) + 1
    else:
        next_id = 1

    while True:
        print("=====TO-DO List=====")
        print("1. Add Task")
        print("2. View Tasks")
        print("3. Deadline Dashboard")
        print("4. Mark Completed")
        print("5. Edit Task")
        print("6. Weekly Summary")
        print("7. Clear All Tasks")
        print("8. Exit")

        while True:
            try:
                choice = int(input("Enter your choice: "))
                break
            except ValueError:
                print("Input digit only!")

        if choice == 1:
            next_id = add_task(tasks, next_id)
            
        elif choice == 2:
            view_tasks(tasks)

        elif choice == 3:
            show_deadline_dashboard(tasks)

        elif choice == 4:
            mark_completed(tasks)

        elif choice == 5:
            edit_task(tasks)

        elif choice == 6:
            weekly_summary(tasks)

        elif choice == 7:
            clear_tasks(tasks)

        elif choice == 8:
            save_tasks(tasks)
            print("Goodbye!")
            break

        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()