# This version is what I have manipulated
# Originals are all untouched.
# Notes: 
# 1. Use the following username and password to access the admin rights 
# username: admin
# password: password
# 2. Ensure you open the whole folder for this task in VS Code otherwise the 
# program will look in your root directory for the text files.

#=====importing libraries===========
import os
# Import re to help with gr option
import re
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
for t_str in task_data:
    curr_t = {}

    # Split by semicolon and manually add each component
    task_components = t_str.split(";")
    curr_t['username'] = task_components[0]
    curr_t['title'] = task_components[1]
    curr_t['description'] = task_components[2]
    curr_t['due_date'] = datetime.strptime(task_components[3], DATETIME_STRING_FORMAT)
    curr_t['assigned_date'] = datetime.strptime(task_components[4], DATETIME_STRING_FORMAT)
    curr_t['completed'] = True if task_components[5] == "Yes" else False

    task_list.append(curr_t)

# Function created to make code more efficient - as this function will be used for gr and ds menu options.
def report() :
    # TASK OVERVIEW
    # gather info to generate report
    with open("tasks.txt", "r") as task_file:
        lines = task_file.read()
        completed = len(re.findall("Yes", lines))
        incomplete = len(re.findall("No", lines))
        total = completed + incomplete
        per_incomplete = incomplete / total * 100
    # To work out overdue tasks
    # First get the info of due dates only from the dictionaries in the task_list
    due_dates = []
    for i in task_list :
        due_dates.append(i["due_date"])
    # Compare due dates with today's date
    overdue = 0
    for d in due_dates :
        if datetime.today() > d :
            overdue +=1    
    # Get percentage of overdue tasks
    per_overdue = overdue / total * 100

    # use with/as to open a new txt file
    with open("task_overview.txt", "w") as t_view :
        l1 = f"The total number of tasks that have been generated and tracked: {total}\n"
        l2 = f"The total number of completed tasks: {completed}\n"
        l3 = f"The total number of incomplete tasks: {incomplete}\n"
        l4 = f"The total number of overdue tasks: {overdue}\n"
        l5 = f"Percentage of incomplete tasks: {per_incomplete:.2f}%\n"
        l6 = f"Percentage of overdue tasks: {per_overdue:.2f}%\n"
        t_view.writelines([l1, l2, l3, l4, l5, l6])

    # USER OVERVIEW
    user_a = []
    for i in task_list:
        if i["username"] not in user_a : 
            user_a.append(i["username"])

    # use with/as to open a new txt file
    with open("user_overview.txt", "w") as u_view :
        l1 = f"The total number of users registered: {len(user_data)}\n"
        l2 = f"The total number of tasks that have been generated and tracked: {total}\n"
        u_view.writelines([l1, l2])

    with open("tasks.txt", "r") as task_file:
        lines = task_file.read()
        for i in user_a:
            t = len(re.findall(i, lines))
            completed = len(re.findall("Yes", lines))
            incomplete = len(re.findall("No", lines))
            due_dates = []
            for j in task_list :
                due_dates.append(j["due_date"])
            # Compare due dates with today's date
            overdue = 0
            for d in due_dates :
                if datetime.today() > d :
                    overdue +=1    
            with open("user_overview.txt", "a") as u_view :
                u_view.writelines(f"\nReport for the {i}:\n")
                u_view.writelines(f"The total number of tasks assigned to the {i} is {t} \n")  
                u_view.writelines(f"Percentage of total tasks assigned to the {i} is {t/total*100:.2f}%\n")
                u_view.writelines(f"Percentage of tasks assigned to the {i} that have been completed: {completed/t*100:.2f}%\n")
                u_view.writelines(f"Percentage of tasks assigned to the {i} that have not been completed: {incomplete/t*100:.2f}%\n")
                u_view.writelines(f"Percentage of tasks assigned to the {i} that are yet to be completed and overdue: {overdue/t*100:.2f}%\n")
            return

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


while True:
    # presenting the menu to the user and 
    # making sure that the user input is converted to lower case.
    print()
    menu = input('''Select one of the following Options below:
r - Registering a user
a - Adding a task
va - View all tasks
vm - view my task
gr - generate reports
ds - display statistics
e - Exit
: ''').lower()

    if menu == 'r':
        '''Add a new user to the user.txt file'''
        # - Request input of a new username
        
        # Reg_user modified to ensure no two users have the same username.
        new_username = input("New Username: ")
        for u in username_password.keys():
            while new_username == u:
                print("This username already exists, please try something different")
                new_username = input("New Username: ")
                continue

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

    elif menu == 'a':
        '''Allow a user to add a new task to task.txt file
            Prompt a user for the following: 
             - A username of the person whom the task is assigned to,
             - A title of a task,
             - A description of the task and 
             - the due date of the task.'''
        task_username = input("Name of person assigned to task: ")
        if task_username not in username_password.keys():
            print("User does not exist. Please enter a valid username")
            continue
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
        print("Task successfully added.")


    elif menu == 'va':
        '''Reads the task from task.txt file and prints to the console in the 
           format of Output 2 presented in the task pdf (i.e. includes spacing
           and labelling) 
        '''

        for t in task_list:
            disp_str = f"Task: \t\t {t['title']}\n"
            disp_str += f"Assigned to: \t {t['username']}\n"
            disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Task Description: \n {t['description']}\n"
            print(disp_str)
            


    elif menu == 'vm':
        '''Reads the task from task.txt file and prints to the console in the 
           format of Output 2 presented in the task pdf (i.e. includes spacing
           and labelling)
        '''
        # Each task will now be associated with a number
        for number, t in enumerate(task_list):
            if t['username'] == curr_user:
                disp_str = f"Task: \t\t {t['title']}\n"
                # Task has a number
                disp_str += f"Task no: \t {number}\n"
                disp_str += f"Assigned to: \t {t['username']}\n"
                disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
                disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
                disp_str += f"Task Description: \n {t['description']}\n"
                print(disp_str)
        
        # user can select a task with the associate task no. or -1 to return to main menu     
        choice1 = int(input("Enter a task number to make changes or enter -1 to return to the main menu: "))

        # if task chosen, then user can either:
            # mark task as complete (No should become Yes) OR
            # edit the task (username or due date can be edited)
        if choice1 != -1 :
            choice2 = input("To mark the chosen task as complete, select c. To edit the task, select e: ")
            x = task_list[choice1]
            # Marking task as complete
            if choice2 == "c" :
                x["completed"] = True
                print(f"Your task has been updated: \n {x}")
            # Editing the user of the task only if it is incomplete
            elif choice2 == "e" and x["completed"] == False :
                choice3 = input("To edit the task user select u or to change the due date, select d: ")
                if choice3 == "u" :
                    edited_user = input("Who are you assigning the task to: ")
                    x["username"] = edited_user
                    print(f"Your task has been updated: \n {x}")
            # Editing the due date of the task only if it is incomplete
                elif choice3 == "d" :
                    edited_date = input("Due date of task (YYYY-MM-DD): ")
                    edit_due_date = datetime.strptime(edited_date, DATETIME_STRING_FORMAT)
                    x["due_date"] = edited_date
                    print(f"Your task has been updated: \n {x}")
        # return to the main menu           
        elif choice1 == -1 :
            continue

    # Including the extra option on generate report
    elif menu == 'gr' :
        report()
        
    elif menu == 'ds' and curr_user == 'admin': 
        # Use the function define above, in the scenario gr has not already been called
        '''If the user is an admin they can display statistics about number of users
            and tasks.'''
        num_users = len(username_password.keys())
        num_tasks = len(task_list)

        print("-----------------------------------")
        print(f"Number of users: \t\t {num_users}")
        print(f"Number of tasks: \t\t {num_tasks}")
        print("-----------------------------------")    

        # If gr was not selected from the menu previously, report function will be called.
        if task_file.closed == True :
            report()

        # This will display the data stored in the task overview txt file
        print("Task Overview:\n")
        contents1 = ""
        with open("task_overview.txt", "r") as t_view : 
            for l in t_view :
                contents1 = contents1 + l
        print(contents1)
        print("-----------------------------------")
        # This will display the data stored in the user overview txt file
        print("\nUser Overview:\n")
        contents2 = ""
        with open("user_overview.txt", "r") as u_view : 
            for l in u_view :
                contents2 = contents2 + l
        print(contents2)
      
    elif menu == 'e':
        print('Goodbye!!!')
        exit()

    else:
        print("You have made a wrong choice, Please Try again")