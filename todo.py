import json

#Task class definition
class Task:
    #Class variable for id numeration
    _id_counter = 1

    def __init__(self, description: str, done=False):
        self.id = Task._id_counter
        Task._id_counter += 1

        self.description = description
        self.done = done

    #Get status for print
    def get_status(self):
        return "Yes" if self.done else "No"
    
    #Get task for print
    def __str__(self):
        return f"{self.id}. Task: '{self.description}', Done: {self.get_status()}"

class ToDoList:
    def __init__(self):
        self.tasks = []
        self.load_from_file()
    
    #Add task
    def add_task(self, description: str):
        self.tasks.append(Task(description))
        self.save_to_file()

    #List tasks
    def list_tasks(self):
        for task in self.tasks:
            print(task)

    #Remove task
    def remove_task(self, task_id: int):
        self.tasks = [task for task in self.tasks if task.id != task_id]
        self.reset_ids()
        self.save_to_file()

    #IDs reset
    def reset_ids(self):
        for i, task in enumerate(self.tasks, start=1):
            task.id = i
        Task._id_counter = len(self.tasks) + 1

    #Save data to JSON file
    def save_to_file(self, filename="tasks.json"):
        with open(filename, "w") as file:
            #Convert Task objects to dictionaries
            tasks_data = [{"id": task.id, "description": task.description, "done": task.done} for task in self.tasks]
            json.dump(tasks_data, file, indent=4)

    #Load data from JSON file
    def load_from_file(self, filename="tasks.json"):
        try:
            with open(filename, "r") as file:
                tasks_data = json.load(file)
                self.tasks = []
                for task_data in tasks_data:
                    task = Task(tasks_data["description"], task_data["done"])
                    task.id = task_data["id"]
                    self.tasks.append(task)
                Task._id_counter = self.tasks[-1].id + 1 if self.tasks else 1
        except FileNotFoundError:
            print(f"File {filename} doesn't exist")

