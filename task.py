from enum import Enum
from datetime import date

class Priority(Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"

#Task class definition
class Task:
    #Class variable for id numeration
    _id_counter = 1

    #Task init
    def __init__(self, description: str, priority: Priority, done: bool = False, deadline: date | None = None):
        self.id = Task._id_counter
        Task._id_counter += 1

        self.description = description
        self.priority = priority
        self.done = done
        self.deadline = deadline
    
    #Get task for print
    def __str__(self):
        status = "Done" if self.done else "Pending"
        deadline_str = f", Deadline: {self.deadline.strftime('%Y-%m-%d')}" if self.deadline else ""
        return f"{self.id}. Task: '{self.description}', Priority: {self.priority.value}, {status}{deadline_str}"
