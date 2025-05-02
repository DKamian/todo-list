from task import Task, Priority
from datetime import date
import json
import shutil
import os

#To-Do list class definition
class ToDoList:
    def __init__(self):
        self.tasks = []
        self.load_from_file()

    #Check if task ID exists
    def task_exists(self, task_id: int):
        return any(task.id == task_id for task in self.tasks)
    
    #IDs reset
    def reset_ids(self):
        for i, task in enumerate(self.tasks, start=1):
            task.id = i
        Task._id_counter = len(self.tasks) + 1
    
    #Add task
    def add_task(self, description: str, priority: Priority, deadline: date | None = None):
        self.tasks.append(Task(description = description, priority = priority, deadline = deadline))
        self.save_to_file()

    #Change task's description
    def change_task(self, task_id: int, description: str):
        for task in self.tasks:
            if task.id == task_id: 
                task.description = description
                self.save_to_file()
                break

    #Change task priority
    def change_priority(self, task_id: int, priority: Priority):
        for task in self.tasks:
            if task.id == task_id:
                task.priority = priority
                self.save_to_file()
                break

    #Change task deadline
    def change_deadline(self, task_id: int, deadline: date | None):
        for task in self.tasks:
            if task.id == task_id:
                task.deadline = deadline
                self.save_to_file()
                break

    #Remove task
    def remove_task(self, task_id: int):
        self.tasks = [task for task in self.tasks if task.id != task_id]
        self.reset_ids()
        self.save_to_file()

    #Mark a task as done
    def get_done(self, task_id: int):
        for task in self.tasks:
            if task.id == task_id: 
                if not task.done:
                    task.done = True
                    self.save_to_file()
                    return "marked_done"
                else:
                    return "already_done" 

    #Get tasks view
    def get_tasks_view(self, filter_by: str, value: any) -> list[Task]:
        tasks_view = []
        today = date.today()

        match filter_by:
            case "none":
                tasks_view = self.tasks
            case "name":
                tasks_view = sorted(self.tasks, key=lambda task: task.description, reverse=value)
            case "status":
                tasks_view = [task for task in self.tasks if task.done == value]
            case "priority":
                tasks_view = [task for task in self.tasks if task.priority == value]
            case "deadline":
                match value:
                    case "today":
                        tasks_view = [task for task in self.tasks if task.deadline == today and task.done == False]
                    case "overdue":
                        tasks_view = [task for task in self.tasks if task.deadline and task.deadline < today and task.done == False]
                    case "none":
                        tasks_view = [task for task in self.tasks if task.deadline is None]
                    case "asc":
                        tasks_view = sorted(self.tasks, key=lambda task: task.deadline or date.max)
                    case "desc":
                        tasks_view = sorted(self.tasks, key=lambda task: task.deadline or date.min, reverse=True)

        return tasks_view

    #Save data to JSON file
    def save_to_file(self, filename="tasks.json"):
        with open(filename, "w") as file:
            #Convert Task objects to dictionaries
            tasks_data = [
                {
                    "id": task.id, 
                    "task": task.description, 
                    "priority": task.priority.value, 
                    "done": task.done, 
                    "deadline": task.deadline.isoformat() if task.deadline else None
                } 
                for task in self.tasks
            ]

            #Add to json file
            json.dump(tasks_data, file, indent=4)

    #Load data from JSON file
    def load_from_file(self, filename="tasks.json"):
        backup_filename = filename + ".bak"

        #Backup file
        if os.path.exists(filename):
            try:
                shutil.copyfile(filename, backup_filename)
            except Exception as e:
                print(f"Could not create backup file: {e}")

        #Read from file
        try:
            with open(filename, "r") as file:
                tasks_data = json.load(file)
                self.tasks = []
                for task_data in tasks_data:
                    priority = Priority[task_data["priority"].upper()]
                    deadline_str = task_data.get("deadline")
                    deadline = date.fromisoformat(deadline_str) if deadline_str else None
                    task = Task(task_data["task"], priority, task_data["done"], deadline)
                    task.id = task_data["id"]
                    self.tasks.append(task)
                if self.tasks:
                    Task._id_counter = max(task.id for task in self.tasks) + 1  
                else:
                    Task._id_counter = 1
        except FileNotFoundError:
            print(f"File {filename} doesn't exist. Starting with an empty list.")
        except json.JSONDecodeError:
            print(f"Error reading {filename}. It might be corrupted.")
            print(f"A backup might be available at {backup_filename}.")
            print("Starting with an empty list.")
            self.tasks = []
            Task._id_counter = 1
        except KeyError as e:
            print(f"Error reading task data from {filename}. Missing key: {e}.")
            print(f"A backup might be available at {backup_filename}.")
            print("Starting with an empty list.")
            self.tasks = []
            Task._id_counter = 1
        except Exception as e:
             print(f"An unexpected error occurred while loading {filename}: {e}")
             print(f"A backup might be available at {backup_filename}.")
             print("Starting with an empty list.")
             self.tasks = []
             Task._id_counter = 1
