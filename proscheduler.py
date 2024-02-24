import os
import platform
import argparse
import subprocess
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC

prometric_logo = """
  _____                          _        _      
 |  __ \                        | |      (_)     
 | |__) | __ ___  _ __ ___   ___| |_ _ __ _  ___ 
 |  ___/ '__/ _ \| '_ ` _ \ / _ \ __| '__| |/ __|
 | |   | | | (_) | | | | | |  __/ |_| |  | | (__ 
 |_|   |_|  \___/|_| |_| |_|\___|\__|_|  |_|\___|
                                                 
                                                 
"""


country = "PAK"
city_centers = {
    "Lahore, Pakistan": ["//a[@title='Availability - 8783:LAHORE, PAKISTAN#8783']",
                          "//a[@title='Availability - 8782:ISLAMABAD, PAKISTAN #8782']"],
                          
    "Karachi, Pakistan": ["//a[@title='Availability - 8781:KARACHI, PAKISTAN #8781']"]
              }

audio_file = "alert.mp3"
schedule_task = ""
schedule = ""
operating_system = platform.system()


print(prometric_logo)
print("Welcome to the Test Center Availability Checker!")
print("------------------------------------------------")
print("This script helps you check for available test center slots for your exam.")
print("You'll be prompted to provide some initial information, such as the exam name, month and year,")
print("and date range to search for available slots.")
print("Once dates found it will play alert.mp3")
print("Let's get started!")
print("------------------------------------------------")


# usage examples of sanitised_input():
# age = sanitised_input("Enter your age: ", int, 1, 101)
# answer = sanitised_input("Enter your answer: ", str.lower, range_=('a', 'b', 'c', 'd'))
def sanitised_input(prompt, type_=None, min_=None, max_=None, range_=None):
    if min_ is not None and max_ is not None and max_ < min_:
        raise ValueError("min_ must be less than or equal to max_.")
    while True:
        ui = input(prompt)
        if type_ is not None:
            try:
                ui = type_(ui)
            except ValueError:
                print("Input type must be {0}.".format(type_.__name__))
                continue
        if max_ is not None and ui > max_:
            print("Input must be less than or equal to {0}.".format(max_))
        elif min_ is not None and ui < min_:
            print("Input must be greater than or equal to {0}.".format(min_))
        elif range_ is not None and ui not in range_:
            if isinstance(range_, range):
                template = "Input must be between {0.start} and {0.stop}."
                print(template.format(range_))
            else:
                template = "Input must be {0}."
                if len(range_) == 1:
                    print(template.format(*range_))
                else:
                    expected = " or ".join((
                        ", ".join(str(x) for x in range_[:-1]),
                        str(range_[-1])
                    ))
                    print(template.format(expected))
        else:
            return ui

# creating optional argument -e
parser = argparse.ArgumentParser()
parser.add_argument('-e', action='store_true', help='Edit user_input.txt file')
args = parser.parse_args()
# If -e flag is provided, delete the file
if args.e:
    if os.path.exists("user_input.txt"):
        os.remove("user_input.txt")


# Check if it's the first time running the script
try:
    with open("user_input.txt", "r") as file:
        # If file exists, read values from it
        exam_name, month_year, selected_city_indices, start_date, end_date= file.read().split(',')
        print("Values loaded from previous session file user_input.txt.")
except FileNotFoundError:
    # If file doesn't exist, prompt user for input
    exam_name = sanitised_input("Enter exam name (STEP1/STEP2): ", str.upper, range_=('STEP1', 'STEP2'))
    month_year = sanitised_input("Enter month and year (3 2024): ", str)

    # Display available cities to the user and prompt for selection
    print("Available cities:")
    for index, city in enumerate(city_centers.keys(), start=1):
        print(f"{index}. {city}")

    # input for cities
    selected_city_indices = sanitised_input("Enter the numbers corresponding to the cities you want to check (separated by space): ", str, range_=('1', '2', '1 2')) or '1 2'

    start_date = sanitised_input("Enter start date (1): ", int, 1, 31)
    end_date = sanitised_input("Enter end date (31): ", int, 1, 31)

    if (operating_system == "Linux" or operating_system == "Darwin"):
        print("")
        print("\033[33mWarning! This will delete all other cronjobs\033[0m")
        schedule_task = sanitised_input("Schedule script to run automatically(yes/no): ", str.lower, range_=('yes', 'no'))    
        if schedule_task == "yes":
            print("")
            print("------------------------------------------------------------")
            print("Input crontab entry. e.g (*/30 * * * *) will run script every 30 minutes")
            print("\033[94mfor more info visit https://crontab.guru website\033[0m")
            print("------------------------------------------------------------")
            schedule = input("how frequently you want to run script?: ")

    if (operating_system == "Windows"):
        schedule_task = sanitised_input("Schedule script to run automatically(yes/no): ", str.lower, range_=('yes', 'no'))
        if schedule_task == "yes":
            print("")
            print("------------------------------------------------------")
            print("for example, To run script after every 30 minutes input 30")
            schedule = sanitised_input("Input number of minutes (30): ", int, 5)


    # Write input values to file for later use
    with open("user_input.txt", "w") as file:
        file.write(f"{exam_name},{month_year},{selected_city_indices},{start_date},{end_date}")
        print("Values stored for later use in user_input.txt.")

# formating variables
selected_city_indices = [int(index) for index in selected_city_indices.split(' ')]
exam_name = exam_name.upper()
start_date = int(start_date)
end_date = int(end_date)

# Validate user input for city selection
for index in selected_city_indices:
    if index < 1 or index > len(city_centers):
        print("Invalid selection. Please enter numbers within the range.")
        exit()


# Gather selected test centers based on user input
selected_test_centers = {city: centers for city, centers in city_centers.items()}

# If not all centers are selected, filter selected_test_centers based on user input
if len(selected_city_indices) < len(city_centers):
    selected_cities = [list(city_centers.keys())[index - 1] for index in selected_city_indices]
    selected_test_centers = {city: centers for city, centers in selected_test_centers.items() if city in selected_cities}


# Now you can proceed with checking availability for the selected test centers
print("checking...")


# progress bar function
total_iterations = len(selected_test_centers) * sum(len(test_centers) for test_centers in selected_test_centers.values())
current_iterations = 0
def print_progress_bar(iteration, total, bar_length=50):
    percent = "{0:.1f}".format(100 * (iteration / float(total)))
    filled_length = int(bar_length * iteration // total)
    bar = '=' * filled_length + '-' * (bar_length - filled_length)
    print()
    print(f'\rProgress: [{bar}] {percent}% complete', end='', flush=True)
    print()


# class for managing tasks on windows
class WindowsTasks:
    def __init__(self):
        pass

    def task_exists(self, task_name):
        # Command to query existing tasks
        query_command = f'schtasks /query /tn "{task_name}"'
        
        # Execute the command and capture the output
        result = subprocess.run(query_command, shell=True, capture_output=True, text=True)
        
        # Check if the task name is found in the output
        return task_name in result.stdout
    
    def delete_task(self, task_name):
        # Command to delete the task
        command = f'schtasks /delete /tn "{task_name}" /f'
        subprocess.run(command, shell=True)

    def create_task(self, task_name, schedule, script_path, script_name):
        
        # Command to schedule the task
        command = f'schtasks /create /sc minute /mo {schedule} /tn "{task_name}" /tr "cmd /c cd /d {script_path} && py {script_name}"'

        # Execute the command to create the task
        subprocess.run(command, shell=True)

# create task using task scheduler on windows
if operating_system == "Windows" and schedule_task == "yes":
    # Initialize WindowsTasks object
    tasks = WindowsTasks()

    # Define task parameters
    task_name = "prometric-scheduler"
    script_path = os.getcwd()
    script_name = "proscheduler.py"

    # Check if the task already exists
    if not tasks.task_exists(task_name):
        # Task does not exist, create it
        tasks.create_task(task_name, schedule, script_path, script_name)
    else:
        # Task does exist, Delete previvous Task and create New
        tasks.delete_task(task_name)
        tasks.create_task(task_name, schedule, script_path, script_name)


class CronJobs:
    def __init__(self):
        pass

    def delete_job(self):
        # Command to remove the cron job
        delete_command = f'crontab -r'
        subprocess.run(delete_command, shell=True)
        print("SUCCESS: all previous cronjobs deleted.")

    def create_job(self, operating_system, schedule, script_path, script_name):
        if operating_system == "Linux":
            # for Linux, the DISPLAY environment variable is used for GUI applications.
            # Find the display value
            display = subprocess.check_output(["echo", "$DISPLAY"]).decode().strip()
            # command for setting up cronjob
            command = f'(echo "{schedule} export DISPLAY={display}; cd {script_path} && python3 {script_name} >> {script_path}/logfile 2>&1") | crontab -'

        elif operating_system == "Darwin":
            # cron jobs on macOS can work without setting the DISPLAY environment variable
            command = f'(echo "{schedule} cd {script_path} && python3 {script_name} >> {script_path}/logfile 2>&1") | crontab -'
            
        subprocess.run(command, shell=True)
        print("SUCCESS: prometric cronjob created successfully.")

# create cron job
if (operating_system == "Linux" or operating_system == "Darwin") and (schedule_task == "yes"):
    script_path = os.getcwd()
    script_name = "proscheduler.py"
    cron = CronJobs()
    cron.delete_job()
    cron.create_job(operating_system, schedule, script_path, script_name)



# loading webdriver for chrome
driver = webdriver.Chrome()

for city, test_centers in selected_test_centers.items():

    for center in test_centers:
        # extract city_name from center for later use with print statement
        city_name = center.split(":")[1].split(",")[0].strip()

        # Open the desired URL
        driver.get("https://securereg3.prometric.com/Welcome.aspx")

        # select exam_name in drop down menu
        programs_menu = driver.find_element(By.ID, "masterPage_cphPageBody_ddlPrograms")
        Select(programs_menu).select_by_value(exam_name)

        #select country
        country_menu = driver.find_element(By.ID, "masterPage_cphPageBody_ddlCountry")
        Select(country_menu).select_by_value(country)


        #click next button
        driver.find_element(By.ID, "masterPage_cphPageBody_btnNext").click()


        # wait for page to load
        # Click the initial link
        initial_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "masterPage_cphPageBody_lnkSeatAvail2"))
        )
        initial_link.click()


        # wait for page to load
        # Find the search input element and enter city "Lahore, Pakistan"
        search_input = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "txtSearch"))
        )
        # change city
        search_input.send_keys(city)


        # Find the search button and click it
        search_button = driver.find_element(By.ID, "btnSearch")
        search_button.click()

        # selecting center
        availability_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, center))
        )
        availability_link.click()


        # Find the dropdown element
        dropdown_month = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "masterPage_cphPageBody_monthYearlist"))
        )


        # select month and year.
        Select(dropdown_month).select_by_value(month_year)

        # Find the submit button and click it
        submit_button = driver.find_element(By.ID, "masterPage_cphPageBody_btnGoCal")
        submit_button.click()


        try:
            # Check for active links' availability
            active_links = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "calActiveLink"))
            )

            # update print_progress_bar at end of 2nd loop
            current_iterations += 1
            print_progress_bar(current_iterations, total_iterations)

            # Extract dates from active links and filter based on date range
            available_dates_inrange = [int(link.text) for link in active_links if start_date <= int(link.text) <= end_date]


            # Print available_dates_inrange
            if any(available_dates_inrange):
                print(f"for {city_name} in {month_year} from {start_date} to {end_date}: ")
                print(f'\033[92mdates found: {available_dates_inrange} \033[0m')

            # opening file in different operating systems
            os_to_command = {
                "Windows": lambda file: os.startfile(file),
                "Darwin": lambda file: os.system(f"open {file}"),
                "Linux": lambda file: os.system(f"xdg-open {file}")
                }

            # play audio if dates within range found
            if any(available_dates_inrange):
                if operating_system in os_to_command:
                    os_to_command[operating_system](audio_file)
                else:
                    print("unsupported operating system/ media player to play audio!")

        # If no active links are found, print a message            
        except TimeoutException:
            # update print_progress_bar at end of 2nd loop
            current_iterations += 1
            print_progress_bar(current_iterations, total_iterations)
            print(f'\033[91mNo seats found for {city_name} in {month_year} from {start_date} to {end_date}.\033[0m')
            continue


driver.close()

# complete progress bar
print_progress_bar(total_iterations, total_iterations)

# Read LICENSE