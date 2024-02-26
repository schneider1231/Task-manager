# Notes: 
# 1. Use the following username and password to access the admin rights 
# username: admin
# password: password
# 2. Ensure you open the whole folder for this task in VS Code otherwise the 
# program will look in your root directory for the text files.

#=====importing libraries===========
import os
from datetime import datetime, date

DATETIME_STRING_FORMAT = "%Y-%m-%d"

# Create tasks.txt if it doesn't exist
if not os.path.exists("tasks.txt"):
    with open("tasks.txt", "w") as default_file:
        pass

with open("tasks.txt", 'r') as task_file:
    task_data = task_file.read().split("\n")
    task_data = [t for t in task_data if t != ""]


task_list = []
for index, t_str in enumerate(task_data, start=1):
    curr_t = {}

    # Split by semicolon and manually add each component
    task_components = t_str.split(";")
    curr_t['task_number'] = index  # Add task number
    curr_t['username'] = task_components[0]
    curr_t['title'] = task_components[1]
    curr_t['description'] = task_components[2]
    curr_t['due_date'] = datetime.strptime(task_components[3], DATETIME_STRING_FORMAT)
    curr_t['assigned_date'] = datetime.strptime(task_components[4], DATETIME_STRING_FORMAT)
    curr_t['completed'] = True if task_components[5] == "Yes" else False

    task_list.append(curr_t)


#====Login Section====
'''This code reads usernames and password from the user.txt file to 
    allow a user to login.
'''
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

logged_in = False
while not logged_in:

    print("LOGIN")
    curr_user = input("Username: ")
    curr_pass = input("Password: ")
    if curr_user not in username_password.keys():
        print("User does not exist")
        continue
    elif username_password[curr_user] != curr_pass:
        print("Wrong password")
        continue
    else:
        print("Login Successful!")
        logged_in = True


def reg_user():
    '''Add a new user to the user.txt file'''
    while True:
         # - Request input of a new username
         new_username = input("New Username: ")
         if new_username in username_password.keys():
            print("Error Username already exists")
         else:
            break                 

    # - Request input of a new password
    new_password = input("New Password: ")

    # - Request input of password confirmation.
    confirm_password = input("Confirm Password: ")

    # - Check if the new password and confirmed password are the same.
    if new_password == confirm_password:
        # - If they are the same, add them to the user.txt file,
        print("New user added")
        username_password[new_username] = new_password
        
        with open("user.txt", "w") as out_file:
            user_data = []
            for k in username_password:
                user_data.append(f"{k};{username_password[k]}")
            out_file.write("\n".join(user_data))

    # - Otherwise you present a relevant message.
    else:
        print("Passwords do no match")


def add_task():
        '''Allow a user to add a new task to task.txt file
            Prompt a user for the following: 
             - A username of the person whom the task is assigned to,
             - A title of a task,
             - A description of the task and 
             - the due date of the task.'''
        task_username = input("Name of person assigned to task: ")
        if task_username not in username_password.keys():
            print("User does not exist. Please enter a valid username")
        task_title = input("Title of Task: ")
        task_description = input("Description of Task: ")
        while True:
            try:
                task_due_date = input("Due date of task (YYYY-MM-DD): ")
                due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
                break

            except ValueError:
                print("Invalid datetime format. Please use the format specified")


        # Then get the current date.
        curr_date = date.today()
        ''' Add the data to the file task.txt and
            Include 'No' to indicate if the task is complete.'''
        new_task = {
            "username": task_username,
            "title": task_title,
            "description": task_description,
            "due_date": due_date_time,
            "assigned_date": curr_date,
            "completed": False
        }

        task_list.append(new_task)
        print("Task successfully added.")
        write_task_file()



def view_all():
        '''Reads the task from task.txt file and prints to the console in the 
           format of Output 2 presented in the task pdf (i.e. includes spacing
           and labelling) 
        '''

        for t in task_list:
            disp_str = f"Task Number: \t {t['task_number']}\n"
            disp_str += f"Task: \t\t {t['title']}\n"
            disp_str += f"Assigned to: \t {t['username']}\n"
            disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Task Completion: \t {'YES' if t['completed'] else 'NO'}\n"
            disp_str += f"Task Description: \n {t['description']}\n"
            print(disp_str)
            

def view_mine():
        '''Reads the task from task.txt file and prints to the console in the 
           format of Output 2 presented in the task pdf (i.e. includes spacing
           and labelling).Allows options to edit a task or return to main menu.  
        '''
        for t in task_list:
            if t['username'] == curr_user:
                disp_str = f"Task Number: \t {t['task_number']}\n"
                disp_str += f"Task: \t\t {t['title']}\n"
                disp_str += f"Assigned to: \t {t['username']}\n"
                disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
                disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
                disp_str += f"Task Completion: \t {'YES' if t['completed'] else 'NO'}\n"
                disp_str += f"Task Description: \n {t['description']}\n"
                print(disp_str)
    # Gets input for sub menu
        while True:
            print()
            sub_menu = input('''Select one of the following Options below:
1 - Select a task to edit
-1 - Return to main menu                         
: ''').lower()     
            if sub_menu == "-1":
                main()
                break
            elif sub_menu == "1":
                task_num = int(input("Enter the Task Number"))
                for t in task_list:
                    if t['task_number'] == task_num and t['completed'] == True:
                        print("Task is completed cannot be edited")
                        main()
                    else:          
                        edit_task(task_num) 
                        break
            else:
                print("Error Incorrect entry")           


def displat_stat():
    # Generate report if it does not exist
    if not os.path.exists("task_overview.txt") or not os.path.exists("user_overview.txt"):
        generate_report()

    # Read and display task overview report
    with open("task_overview.txt", "r") as task_report:
        print("Task Overview:")
        print(task_report.read())

    # Read and display user overview report
    with open("user_overview.txt", "r") as user_report:
        print("\nUser Overview:")
        print(user_report.read())


def edit_task(task_num):
    """
    Prints the task chosen by the user and allows them to update its 
    completed status and/or update which user the task is assigned to and
    the due
    """
    for t in task_list:
            if t['task_number'] == task_num:
                disp_str = f"Task Number: \t {t['task_number']}\n"
                disp_str += f"Task: \t\t {t['title']}\n"
                disp_str += f"Assigned to: \t {t['username']}\n"
                disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
                disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
                disp_str += f"Task Completion: \t {'YES' if t['completed'] else 'NO'}\n"
                disp_str += f"Task Description: \n {t['description']}\n"
                print(disp_str)
    while True:
         print()
         choice = input("""Select one of the options:
1 - Mark task as complete
2 - Edit task  
3 - Main menu                                                    
""")
         if choice == '1':
            for t in task_list:
                if t['task_number'] == task_num:
                    t['completed'] = True
                    print("Task marked as complete.")
                    write_task_file()
                    break
         elif choice == '2':
            new_user_name = input("Enter new username: ")
            new_due_date = input("Enter new due date (YYYY-MM-DD): ")
        
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
                    write_task_file()
                    break
         elif choice == '3':
             main()       
         else:
             print("Error incorrect Selection")
                    

def generate_report():
    """
    Generates two reports in a text file format which are a summary of tasks
    and a summary of user tasks
    """
    tasks_completed = 0
    tasks_incompleted = 0
    tasks_overdue = 0
    tasks_overdue_incom = 0
    
    # Checks task completion
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

    # Calculates task completion percentages
    incomplete_per = (tasks_incompleted / total_tasks) * 100 
    overdue_per = (tasks_overdue / total_tasks) * 100 

    time = datetime.today().strftime(DATETIME_STRING_FORMAT + " %H:%M")
    # Writes the task_overview.txt
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
        completed_percentage = (completed_tasks / total_tasks_assigned) * 100 if total_tasks_assigned > 0 else 0
        overdue_percentage = (overdue_tasks / total_tasks_assigned) * 100 if total_tasks_assigned > 0 else 0
        incomplete_percentage = (incomplete_tasks / total_tasks_assigned) * 100 if total_tasks_assigned > 0 else 0

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

    # Write the report to user_overview.txt
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
    

def write_task_file():
    '''Write the updated task list to tasks.txt'''
    with open("tasks.txt", "w") as task_file:
        task_list_to_write = []
        for t in task_list:
            str_attrs = [
                t['username'],
                t['title'],
                t['description'],
                t['due_date'].strftime(DATETIME_STRING_FORMAT),
                t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                "Yes" if t['completed'] else "No"
            ]
            task_list_to_write.append(";".join(str_attrs))
        task_file.write("\n".join(task_list_to_write))


def main():
    while True:
    # presenting the menu to the user and 
    # making sure that the user input is converted to lower case.
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
            reg_user()
        elif menu == "a":
             add_task()
        elif menu == "va":
             view_all()
        elif menu == "vm":
             view_mine()
        elif menu == "gr":
             generate_report()     
        elif menu == "ds":
             displat_stat()
        elif menu == "e":
             print("end")
             exit()
        else:
             print("You have made a wrong choice, Please Try again")     


main()