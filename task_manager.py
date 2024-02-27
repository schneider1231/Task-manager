import os
from datetime import datetime, date

DATETIME_STRING_FORMAT = "%Y-%m-%d"

def load_task_data():
    """Load task data from tasks.txt file."""

    # Create tasks.txt if it doesn't exist
    if not os.path.exists("tasks.txt"):
        with open("tasks.txt", "w"):
            pass

    with open("tasks.txt", 'r') as task_file:
        task_data = task_file.read().split("\n")
        task_data = [t for t in task_data if t != ""]

    task_list = []
    for index, t_str in enumerate(task_data, start=1):
        curr_t = {}

        # Split by semicolon and manually add each component
        task_components = t_str.split(";")
        curr_t['task_number'] = index
        curr_t['username'] = task_components[0]
        curr_t['title'] = task_components[1]
        curr_t['description'] = task_components[2]
        curr_t['due_date'] = datetime.strptime(task_components[3], DATETIME_STRING_FORMAT)
        curr_t['assigned_date'] = datetime.strptime(task_components[4], DATETIME_STRING_FORMAT)
        curr_t['completed'] = True if task_components[5] == "Yes" else False

        task_list.append(curr_t)

    return task_list


def load_user_data():
    """Load user data from user.txt file."""

    # If no user.txt file, write one with a default account
    if not os.path.exists("user.txt"):
        with open("user.txt", "w") as default_file:
            default_file.write("admin;password")
    
    # Read in user_data
    with open("user.txt", 'r') as user_file:
        user_data = user_file.read().split("\n")
    
    # Convert to a dictionary
    username_password = {}
    for user in user_data:
        username, password = user.split(';')
        username_password[username] = password

    return username_password


def login():
    """Login user."""

    # Load user data from the file
    username_password = load_user_data()

    logged_in = False
    while not logged_in:
        print("LOGIN")
        # Prompt the user for their username and password
        curr_user = input("Username: ")
        curr_pass = input("Password: ")

        # Check if the entered username exists
        if curr_user not in username_password.keys():
            print("User does not exist")
            continue
        # Check if the entered password matches the password associated with the username
        elif username_password[curr_user] != curr_pass:
            print("Wrong password")
            continue
        else:
            # If both username and password are correct, log the user in
            print("Login Successful!")
            logged_in = True

    return curr_user


def register_user():
    """Register a new user."""
    # Load existing user data
    username_password = load_user_data()

    # Ask for a new username until a unique one is provided
    while True:
        new_username = input("New Username: ")
        if new_username in username_password.keys():
            print("Error: Username already exists")
        else:
            break

    # Prompt the user to enter a new password and confirm it
    new_password = input("New Password: ")
    confirm_password = input("Confirm Password: ")

    # Check if the passwords match
    if new_password == confirm_password:
        print("New user added")

        # Add the new user to the dictionary
        username_password[new_username] = new_password

        # Write the updated user data to the file
        with open("user.txt", "w") as out_file:
            user_data = []
            for k in username_password:
                user_data.append(f"{k};{username_password[k]}")
            out_file.write("\n".join(user_data))
    else:
        print("Error: Passwords do not match")


def add_task(task_list):
    '''Allow a user to add a new task to task.txt file
            Prompt a user for the following: 
             - A username of the person whom the task is assigned to,
             - A title of a task,
             - A description of the task and 
             - the due date of the task.'''
    # Ask for the username of the person assigned to the task
    task_username = input("Name of person assigned to task: ")
    
    # Check if the entered username exists
    if task_username not in load_user_data().keys():
        print("User does not exist. Please enter a valid username")
        return

    # Ask for the title and description of the task
    task_title = input("Title of Task: ")
    task_description = input("Description of Task: ")

    # Prompt the user to enter the due date of the task until a valid date is provided
    while True:
        try:
            task_due_date = input("Due date of task (YYYY-MM-DD): ")
            due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
            break
        except ValueError:
            print("Invalid datetime format. Please use the format specified")

    # Get the current date
    curr_date = date.today()

    # Create a new task dictionary with the provided information
    new_task = {
        "username": task_username,
        "title": task_title,
        "description": task_description,
        "due_date": due_date_time,
        "assigned_date": curr_date,
        "completed": False
    }

    # Add the new task to the task list
    task_list.append(new_task)
    
    # Print a confirmation message
    print("Task successfully added.")
    
    # Write the updated task list to the file
    write_task_file(task_list)


def write_task_file(task_list):
    """
    Write task data to the 'tasks.txt' file.
    """
    # Open the 'tasks.txt' file in write mode
    with open("tasks.txt", "w") as task_file:
        # Create an empty list to store string representations of tasks
        task_list_to_write = []
        
        # Iterate over each task in the task_list
        for t in task_list:
            # Convert task attributes to strings and join them with ';' separator
            str_attrs = [
                t['username'],
                t['title'],
                t['description'],
                t['due_date'].strftime(DATETIME_STRING_FORMAT),
                t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                "Yes" if t['completed'] else "No"
            ]
            # Append the joined string to the task_list_to_write
            task_list_to_write.append(";".join(str_attrs))
        
        # Write the task_list_to_write to the 'tasks.txt' file
        task_file.write("\n".join(task_list_to_write))



def view_all(task_list):
    '''Reads the task from task.txt file and prints to the console in the 
       format of Output 2 presented in the task pdf (i.e. includes spacing
       and labelling) 
    '''
    if not task_list:
        print("No tasks available.")
        return

    print("All Tasks:\n")
    for t in task_list:
        print(f"Task Number: \t {t['task_number']}")
        print(f"Task: \t\t {t['title']}")
        print(f"Assigned to: \t {t['username']}")
        print(f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}")
        print(f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}")
        print(f"Task Completion: {'YES' if t['completed'] else 'NO'}")
        print(f"Task Description:\n{t['description']}\n")


def view_mine(task_list, curr_user):
    '''Displays tasks assigned to the current user and provides options
       to edit a task or return to the main menu.
       Reads the task data from the 'task.txt' file and prints it to 
       the console in the format of Output 2 presented in the task PDF, 
       including spacing and labeling. Allows the user to select a task 
       for editing or return to the main menu.
    '''
    # Iterate through the task list
    for t in task_list:
        # Check if the task is assigned to the current user
        if t['username'] == curr_user:
            # Construct a formatted string to display task details
            disp_str = f"Task Number: \t {t['task_number']}\n"
            disp_str += f"Task: \t\t {t['title']}\n"
            disp_str += f"Assigned to: \t {t['username']}\n"
            disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Task Completion: \t {'YES' if t['completed'] else 'NO'}\n"
            disp_str += f"Task Description: \n {t['description']}\n"
            # Print the task details
            print(disp_str)

    # Display menu for selecting options
    while True:
        print()
        # Prompt user for input
        sub_menu = input('''Select one of the following Options below:
1 - Select a task to edit
-1 - Return to main menu
: ''').lower()

        # Handle user input
        if sub_menu == "-1":
            break
        elif sub_menu == "1":
            # Prompt user to enter task number
            task_num = int(input("Enter the Task Number"))
            # Find the task in the task list
            for t in task_list:
                # Check if the task number matches and if it's completed
                if t['task_number'] == task_num and t['completed']:
                    print("Task is completed and cannot be edited")
                    break
                else:
                    # Edit the task
                    edit_task(task_list, task_num)
                    break
        else:
            print("Error: Incorrect entry")



def edit_task(task_list, task_num):
    '''Edits a task in the task list based on the task number provided.
       Reads the task data from the 'task.txt' file and prints the details 
       of the task with the given task number.
       Allows the user to mark the task as complete, edit the task details 
       (username and due date), or return to the main menu.
    '''
    # Iterate through the task list
    for t in task_list:
        # Check if the task number matches
        if t['task_number'] == task_num:
            # Construct a formatted string to display task details
            disp_str = f"Task Number: \t {t['task_number']}\n"
            disp_str += f"Task: \t\t {t['title']}\n"
            disp_str += f"Assigned to: \t {t['username']}\n"
            disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Task Completion: \t {'YES' if t['completed'] else 'NO'}\n"
            disp_str += f"Task Description: \n {t['description']}\n"
            # Print the task details
            print(disp_str)

    # Display menu for selecting options
    while True:
        print()
        # Prompt user for input
        choice = input("""Select one of the options:
1 - Mark task as complete
2 - Edit task
3 - Back
: """)
        # Handle user choice
        if choice == '1':
            # Mark the task as complete
            for t in task_list:
                if t['task_number'] == task_num:
                    t['completed'] = True
                    print("Task marked as complete.")
                    write_task_file(task_list)
                    break
        elif choice == '2':
            # Prompt user for new username and due date
            new_user_name = input("Enter new username: ")
            new_due_date = input("Enter new due date (YYYY-MM-DD): ")

            # Edit the task details
            for t in task_list:
                if t['task_number'] == task_num:
                    if new_user_name:
                        t['username'] = new_user_name
                    if new_due_date:
                        try:
                            t['due_date'] = datetime.strptime(new_due_date, DATETIME_STRING_FORMAT)
                        except ValueError:
                            print("Invalid date format.")
                    print("Task successfully edited.")
                    write_task_file(task_list)
                    break
        elif choice == '3':
            break
        else:
            print("Error: Incorrect selection")


def generate_report(task_list, username_password):
    """
    Generate two reports based on the provided task list and user data.

    1. Task Overview: Provides an overview of the tasks, including the total number of tasks,
       completed tasks, incompleted tasks, tasks incomplete and overdue, percentage of tasks
       incomplete, and percentage of tasks overdue.
    2. User Overview: Provides an overview of user statistics, including total tasks assigned,
       completed tasks, overdue tasks, and percentages for each user.
    """

    # Create variables to track task stats
    tasks_completed = 0
    tasks_incompleted = 0
    tasks_overdue = 0
    tasks_overdue_incom = 0

    # Calculate task statistics
    for t in task_list:
        if t['completed']:
            tasks_completed += 1
        elif datetime.today() > t['due_date']:
            tasks_incompleted += 1
            tasks_overdue += 1
            tasks_overdue_incom += 1
        else:
            tasks_incompleted += 1

    total_tasks = len(task_list)

    try:
        incomplete_per = (tasks_incompleted / total_tasks) * 100
        overdue_per = (tasks_overdue / total_tasks) * 100
    except ZeroDivisionError:
        incomplete_per = 0
        overdue_per = 0

    # Get current time for the report timestamp
    time = datetime.today().strftime("%Y-%m-%d %H:%M")

    # Write the task overview report to 'task_overview.txt'
    with open("task_overview.txt", "w") as report_file:
        report_file.write("Task Overview\n" + (time))
        report_file.write("-" * 20 + "\n")
        report_file.write(f"\nTotal number of tasks:\t{total_tasks}")
        report_file.write(f"\nTotal number of completed tasks:\t{tasks_completed}")
        report_file.write(f"\nTotal number of incompleted tasks:\t{tasks_incompleted}")
        report_file.write(f"\nTotal number of tasks incomplete and overdue:\t{tasks_overdue_incom}")
        report_file.write(f"\nPercentage of tasks incomplete:\t{incomplete_per}%")
        report_file.write(f"\nPercentage of tasks overdue:\t{overdue_per}%")

    # Calculate statistics for each user
    user_stats = []
    for username, password in username_password.items():
        user_tasks = [task for task in task_list if task['username'] == username]
        total_tasks_assigned = len(user_tasks)
        completed_tasks = sum(1 for task in user_tasks if task['completed'])
        overdue_tasks = sum(1 for task in user_tasks if not task['completed'] and task['due_date'] < datetime.today())
        incomplete_tasks = total_tasks_assigned - completed_tasks

        # Calculate percentages
        try:
            completed_percentage = (completed_tasks / total_tasks_assigned) * 100 if total_tasks_assigned > 0 else 0
            overdue_percentage = (overdue_tasks / total_tasks_assigned) * 100 if total_tasks_assigned > 0 else 0
            incomplete_percentage = (incomplete_tasks / total_tasks_assigned) * 100 if total_tasks_assigned > 0 else 0
        except ZeroDivisionError:
            completed_percentage = 0
            overdue_percentage = 0
            incomplete_percentage = 0

        user_stats.append({
            'username': username,
            'total_tasks_assigned': total_tasks_assigned,
            'completed_tasks': completed_tasks,
            'overdue_tasks': overdue_tasks,
            'incomplete_tasks': incomplete_tasks,
            'completed_percentage': completed_percentage,
            'overdue_percentage': overdue_percentage,
            'incomplete_percentage': incomplete_percentage
        })

    # Write the user overview report to 'user_overview.txt'
    with open("user_overview.txt", "w") as report_file:
        report_file.write("User Overview\n")
        report_file.write("-" * 20 + "\n")
        report_file.write(f"Total number of users:\t{len(username_password)}\n")
        report_file.write(f"Total number of tasks:\t{len(task_list)}\n\n")
        report_file.write("User Summary:\n")
        for user_stat in user_stats:
            report_file.write(f"Username:\t{user_stat['username']}\n")
            report_file.write(f"Total tasks assigned:\t{user_stat['total_tasks_assigned']}\n")
            report_file.write(f"Percentage of tasks completed:\t{user_stat['completed_percentage']}%\n")
            report_file.write(f"Percentage of tasks overdue:\t{user_stat['overdue_percentage']}%\n")
            report_file.write(f"Percentage of tasks incomplete:\t{user_stat['incomplete_percentage']}%\n")
            report_file.write("\n")
 

def display_stat(task_list):
    """Display statistics."""
    username_password = load_user_data()
    generate_report(task_list, username_password)

    with open("task_overview.txt", "r") as task_report:
        print("Task Overview:")
        print(task_report.read())


def main():
    # Load task data
    task_list = load_task_data()
    
    # Load user data
    username_password = load_user_data()
    
    # Log in user
    curr_user = login()

    while True:
        print()
        menu = input('''Select one of the following Options below:
r - Registering a user
a - Adding a task
va - View all tasks
vm - View my task
gr - generate reports
ds - Display statistics
e - Exit
: ''').lower()

        if menu == "r":
            register_user()
        elif menu == "a":
            add_task(task_list)
        elif menu == "va":
            view_all(task_list)
        elif menu == "vm":
            view_mine(task_list, curr_user)
        elif menu == "gr":
            generate_report(task_list, username_password) 
        elif menu == "ds":
            display_stat(task_list)
        elif menu == "e":
            print("End")
            break
        else:
            print("You have made a wrong choice, Please Try again")

main()

