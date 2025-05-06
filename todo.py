from todo_list import ToDoList
from task import Priority, Task
from datetime import datetime, date

#Handle adding task
def handle_add_task(to_do_list: ToDoList):

    #Enter task description
    description = input("\nEnter task's description: ")
    if not description:
        print("Description cannot be empty.")
        return

    #Enter task priority
    print("\nChoose priority:")
    print("1. Low")
    print("2. Medium")
    print("3. High")

    try:
        choice = int(input("Your choice: "))
    except ValueError:
        print("Input is not a number.")
        return
    if choice == 1:
        priority = Priority.LOW
    elif choice == 2:
        priority = Priority.MEDIUM
    elif choice == 3:
        priority = Priority.HIGH
    else:
        print("Invalid priority choice. Task not added.")
        return

    #Enter task deadline
    deadline: date | None = None
    deadline_input = input("\nAdd deadline? (yes/no): ").lower()

    if deadline_input == "yes":
        deadline_str = input("Enter deadline (YYYY-MM-DD): ")
        try:
            deadline = datetime.strptime(deadline_str, '%Y-%m-%d').date()
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")
            print("Task will be added without deadline.")

    #Create new task and add to list
    to_do_list.add_task(description, priority, deadline)
    print("\nNew task created!")

#Handle removing task
def handle_remove_task(to_do_list: ToDoList):
    try:
        task = int(input("\nEnter ID of the task which will be deleted: "))
    except ValueError:
        print("Input is not a number.")
        return
    
    for t in to_do_list.tasks:
        if t.id == task:
            task_object = t
            break

    if task_object:
        confirm = input(f"Are you sure you want to remove task '{task_object.description}'? (yes/no): ").lower()
        if confirm == "yes":
            to_do_list.remove_task(task)
            print("Task removed!")
        elif confirm == "no":
            print("Removal cancelled.")
        else:
            print("Unexpected answer, no action taken.")
            return
    else: 
        print("Task not found.")

#Handle getting task done
def handle_get_done(to_do_list: ToDoList):
    try:
        task = int(input("\nWhich task have you done? Enter ID: "))
    except ValueError:
        print("Input is not a number.")
        return
    
    if to_do_list.task_exists(task):
        result = to_do_list.get_done(task)
        if result == "marked_done":
            print("Task done, good job!")
        elif result == "already_done":
            print("This task was already done!")
    else: 
        print("Task not found.")

#Handle change task description
def handle_change_task(to_do_list: ToDoList):
    try:
        task = int(input("\nEnter ID of the task you want to change: "))
    except ValueError:
        print("Input is not a number.")
        return
    
    if to_do_list.task_exists(task):
        description = input("New description: ")
        if not description:
            print("Description cannot be empty.")
            return
        to_do_list.change_task(task, description)
        print("Task changed!")
    else: print("Task not found.")

#Handle change task priority
def handle_change_priority(to_do_list: ToDoList):
    try:
        task = int(input("\nEnter ID of the task whose priority you want to change: "))
    except ValueError:
        print("Input is not a number.")
        return
    
    if to_do_list.task_exists(task):
        print("\nChoose priority:")
        print("1. Low")
        print("2. Medium")
        print("3. High")

        try:
            choice = int(input("Your choice: "))
        except ValueError:
            print("Input is not a number.")
            return
        
        if choice == 1:
            priority = Priority.LOW
        elif choice == 2:
            priority = Priority.MEDIUM
        elif choice == 3:
            priority = Priority.HIGH
        else:
            print("Invalid priority choice. Task not changed.")
            return
        
        to_do_list.change_priority(task, priority)
        print("Task's priority changed.")
    else:
        print("Task not found.")

#Handle change task deadline
def handle_change_deadline(to_do_list: ToDoList):
    try:
        task = int(input("\nEnter ID of the task whose deadline you want to change: "))
    except ValueError:
        print("Input is not a number.")
        return
    
    if to_do_list.task_exists(task):
        deadline_str = input("\nEnter deadline (YYYY-MM-DD) or leave empty to remove: ")
        #Remove deadline
        if not deadline_str:
            deadline = None
            to_do_list.change_deadline(task, deadline)
            print("Deadline removed.")
        #Change/Add deadline
        else:
            try:
                deadline = datetime.strptime(deadline_str, '%Y-%m-%d').date()
                to_do_list.change_deadline(task, deadline)
                print("Deadline changed.")
            except ValueError:
                print("Invalid date format. Please use YYYY-MM-DD.")
                print("Deadline will not be changed.")
                return
    else:
        print("Task not found.")

#Show filtered tasks
def display_tasks(task_list: list[Task], title: str):
    print(f"\n--- {title} ---")
    if not task_list:
        print("No tasks found matching the criteria.")
    else:
        for task in task_list:
            print(task)

#Handle show tasks
def handle_display_tasks(to_do_list: ToDoList):
    print("\n--- Task View ---")
    print("1. None.")
    print("2. Name.")
    print("3. Status.")
    print("4. Priority.")
    print("5. Deadline.")
    print("0. Cancel.")

    try:
        choice = int(input("\nPlease enter your choice: "))
    except ValueError:
        print("Input is not a number.")
        return

    match choice:
        #No filter
        case 1:
            sort_by = "none"
            value = None
            title = "All tasks"  
        #Sort by name
        case 2:
            print("\n--- Sort ---")
            print("1. Ascending.")
            print("2. Descending.")
            sort_by = "name"

            try:
                choice = int(input("\nPlease enter your choice: "))
            except ValueError:
                print("Input is not a number.")
                return
            
            if choice == 1:
                value = False
                title = "Tasks Ascending"
            elif choice == 2:
                value = True
                title = "Tasks Descending"
            else:
                print("Invalid choice.")
                return
        #Filter by status
        case 3:
            print("\n--- Filter ---")
            print("1. Pending.")
            print("2. Done.")
            sort_by = "status"

            try:
                choice = int(input("\nPlease enter your choice: "))
            except ValueError:
                print("Input is not a number.")
                return
            
            if choice == 1:
                value = False
                title = "Pending Tasks"
            elif choice == 2:
                value = True
                title = "Tasks Done"
            else:
                print("Invalid choice.")
                return
        #Filter by priority
        case 4:
            print("\n--- Filter ---")
            print("Choose priority:")
            print("1. Low.")
            print("2. Medium.")
            print("3. High.")
            sort_by = "priority"

            try:
                choice = int(input("\nPlease enter your choice: "))
            except ValueError:
                print("Input is not a number.")
                return
            
            if choice == 1:
                value = Priority.LOW
                title = "Low Priority Tasks"
            elif choice == 2:
                value = Priority.MEDIUM
                title = "Medium Priority Tasks"
            elif choice == 3:
                value = Priority.HIGH
                title = "High Priority Tasks"
            else:
                print("Invalid choice.")
                return
        #View by deadline
        case 5:
            print("\n--- View ---")
            print("1. Today.")
            print("2. Overdue.")
            print("3. No deadline.")
            print("4. Ascending.")
            print("5. Descending.")
            sort_by = "deadline"

            try:
                choice = int(input("\nPlease enter your choice: "))
            except ValueError:
                print("Input is not a number.")
                return
            
            if choice == 1:
                value = "today"
                title = "Today's Tasks"
            elif choice == 2:
                value = "overdue"
                title = "Overdue Tasks"
            elif choice == 3:
                value = "none"
                title = "No Deadline Tasks"
            elif choice == 4:
                value = "asc"
                title = "Tasks Ascending"
            elif choice == 5:
                value = "desc"
                title = "Tasks Descending"
            else:
                print("Invalid choice.")
                return
        #Cancel show
        case 0:
            print("Showing cancelled.")
            return
        #Default case
        case _:
            print("Invalid input.")
            return
    
    #Filter tasks
    view_options = to_do_list.get_tasks_view(sort_by, value)
    #Show tasks
    display_tasks(view_options, title)

if __name__ == "__main__":
    to_do_list = ToDoList()
    choice = -1

    while choice != 0:
        #Main menu
        print("\nWelcome to your To-Do list, what are you up to?")
        print("1. Show tasks.")
        print("2. Add a new task.")
        print("3. Remove a task.")
        print("4. Mark task as done.")
        print("5. Edit task's description.")
        print("6. Change task's priority.")
        print("7. Change task's deadline.")
        print("0. Leave.")

        #Menu input
        try:
            print("")
            choice = int(input("Enter your choice: "))
        except ValueError:
            print("Invalid input. Please enter a number.")
            choice = -1
            continue

        #Handle menu input
        match choice:
            case 1:
                handle_display_tasks(to_do_list)
            case 2:
                handle_add_task(to_do_list)
            case 3:
                handle_remove_task(to_do_list)
            case 4:
                handle_get_done(to_do_list)
            case 5:
                handle_change_task(to_do_list)
            case 6:
                handle_change_priority(to_do_list)
            case 7:
                handle_change_deadline(to_do_list)
            #End program message    
            case 0:
                print("")
                print("Goodbye! See you next time!")
                pass
            #Default case
            case _:
                print("Invalid input.")
