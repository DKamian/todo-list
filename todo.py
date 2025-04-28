import json
from enum import Enum

class Priority(Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"

#Task class definition
class Task:
    #Class variable for id numeration
    _id_counter = 1

    def __init__(self, description: str, priority: Priority, done=False):
        self.id = Task._id_counter
        Task._id_counter += 1

        self.description = description
        self.priority = priority
        self.done = done

    #Get status for print
    def get_status(self):
        return "Yes" if self.done else "No"
    
    #Get task for print
    def __str__(self):
        return f"{self.id}. Task: '{self.description}', Priority: {self.priority.value}, Done: {self.get_status()}"

#To-Do list class definition
class ToDoList:
    def __init__(self):
        self.tasks = []
        self.load_from_file()

    #List tasks
    def list_tasks(self):
        print("List of your tasks:")
        for task in self.tasks:
            print(task)
    
    #Add task
    def add_task(self, description: str, priority: Priority):
        self.tasks.append(Task(description, priority))
        self.save_to_file()

    #Remove task
    def remove_task(self, task_id: int):
        self.tasks = [task for task in self.tasks if task.id != task_id]
        self.reset_ids()
        self.save_to_file()

    #Mark a task as done
    def get_done(self, task_id: int):
        for task in self.tasks:
            if task.id == task_id:
                if task.done: print("This task is already done!")
                else: 
                    task.done = True
                    print("Task done, good job!")
        self.save_to_file()

    #IDs reset
    def reset_ids(self):
        for i, task in enumerate(self.tasks, start=1):
            task.id = i
        Task._id_counter = len(self.tasks) + 1

    #Check if task ID exists
    def task_exists(self, task_id: int):
        return any(task.id == task_id for task in self.tasks)
    
    #Change task's description
    def change_task(self, task_id: int, description: str):
        for task in self.tasks:
            if task.id == task_id: task.description = description
            break
        self.save_to_file()

    #Save data to JSON file
    def save_to_file(self, filename="tasks.json"):
        with open(filename, "w") as file:
            #Convert Task objects to dictionaries
            tasks_data = [{"id": task.id, "task": task.description, "priority": task.priority.value, "done": task.done} for task in self.tasks]
            json.dump(tasks_data, file, indent=4)

    #Load data from JSON file
    def load_from_file(self, filename="tasks.json"):
        try:
            with open(filename, "r") as file:
                tasks_data = json.load(file)
                self.tasks = []
                for task_data in tasks_data:
                    priority = Priority[task_data["priority"].upper()]
                    task = Task(task_data["task"], priority, task_data["done"])
                    task.id = task_data["id"]
                    self.tasks.append(task)
                Task._id_counter = self.tasks[-1].id + 1 if self.tasks else 1
        except FileNotFoundError:
            print(f"File {filename} doesn't exist")

if __name__ == "__main__":
    to_do_list = ToDoList()
    choice = 0

    while choice != 6:
        print("Welcome to your To-Do list, what are you up to?")
        print("1. See all tasks.")
        print("2. Add a new task.")
        print("3. Remove a task.")
        print("4. Mark task as done.")
        print("5. Edit task's description.")
        print("6. Leave")
        choice = int(input("Enter your choice: "))

        match choice:
            case 1:
                print("")
                to_do_list.list_tasks()
            case 2:
                task = input("Enter task's description: ")

                print("Choose priority:")
                print("1. Low")
                print("2. Medium")
                print("3. High")
                try:
                    choice = int(input("Your choice: "))
                except ValueError:
                    print("Input is not a number.")
                    continue
                if choice == 1:
                    priority = Priority.LOW
                elif choice == 2:
                    priority = Priority.MEDIUM
                elif choice == 3:
                    priority = Priority.HIGH

                to_do_list.add_task(task, priority)
                print("New task created!")
            case 3:
                try:
                    task = int(input("Enter ID of the task which will be deleted: "))
                except ValueError:
                    print("Input is not a number.")
                    continue
                to_do_list.remove_task(task)
                print("Task removed!")
            case 4:
                try:
                    task = int(input("Which task have you done? Enter ID: "))
                except ValueError:
                    print("Input is not a number.")
                    continue
                to_do_list.get_done(task)
            case 5:
                try:
                    task = int(input("Enter ID of the task you want to change: "))
                except ValueError:
                    print("Input is not a number.")
                    continue
                if to_do_list.task_exists(task):
                    description = input("New description: ")
                    to_do_list.change_task(task, description)
                    print("Task changed!")
                else: print("Task not found.")
            case 6:
                print("Goodbye! See you next time!")
                pass
            case _:
                print("Invalid input")

        print("")