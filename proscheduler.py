import os
import re
import json
import html
import platform
import argparse
import subprocess
from playsound import playsound
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC

prometric_logo = r"""

 ____                           _        _      
|  _ \ _ __ ___  _ __ ___   ___| |_ _ __(_) ___ 
| |_) | '__/ _ \| '_ ` _ \ / _ \ __| '__| |/ __|
|  __/| | | (_) | | | | | |  __/ |_| |  | | (__ 
|_|__ |_|  \___/|_| |_| |_|\___|\__|_|  |_|\___|
/ ___|  ___| |__   ___  __| |_   _| | ___ _ __  
\___ \ / __| '_ \ / _ \/ _` | | | | |/ _ \ '__| 
 ___) | (__| | | |  __/ (_| | |_| | |  __/ |    
|____/ \___|_| |_|\___|\__,_|\__,_|_|\___|_|    


"""


country = "PAK"
city_centers = {
    "Lahore, Pakistan": ["//a[@title='Availability - 8783:LAHORE, PAKISTAN#8783']"],
    "Islamabad, Pakistan": ["//a[@title='Availability - 8782:ISLAMABAD, PAKISTAN #8782']"],                      
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
print("You'll be prompted to provide some initial information, such as the exam name,")
print("month and year, and date range to search for available slots. Also how often")
print("you want to run script automatically.")
print("Once dates found it will play alert.mp3")
print("Let's get started!")
print("------------------------------------------------")


def notify(title, message):
    title = html.escape(title)
    message = html.escape(message)
    if operating_system == "Darwin":
        subprocess.run([
            "osascript", "-e",
            f'display notification "{message}" with title "{title}"'
        ])
    elif operating_system == "Linux":
        subprocess.run(['notify-send', title, message])
    elif operating_system == "Windows":
        powershell_cmd = (
            "[Windows.UI.Notifications.ToastNotificationManager, Windows.UI.Notifications, ContentType = WindowsRuntime] > $null; "
            "$t=[Windows.UI.Notifications.ToastNotificationManager]::GetTemplateContent([Windows.UI.Notifications.ToastTemplateType]::ToastText02); "
            "$textNodes = $t.GetElementsByTagName('text'); "
            f"$textNodes.Item(0).AppendChild($t.CreateTextNode('{title}')) > $null; "
            f"$textNodes.Item(1).AppendChild($t.CreateTextNode('{message}')) > $null; "
            "$toast=[Windows.UI.Notifications.ToastNotification]::new($t); "
            '[Windows.UI.Notifications.ToastNotificationManager]::CreateToastNotifier("Prometric Scheduler").Show($toast);'
        )

        subprocess.run(["powershell", "-NoProfile", "-Command", powershell_cmd], shell=True)


# usage examples of sanitised_input():
# age = sanitised_input("Enter your age: ", int, 1, 101)
# answer = sanitised_input("Enter your answer: ", str.lower, range_=('a', 'b', 'c', 'd'))
def sanitised_input(prompt, type_=None, min_=None, max_=None, range_=None, subsetof_=None):
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
        elif (subsetof_ is not None) and (not(set(ui.split(' '))) <= set(subsetof_)):
            print(f"Input must be a subset of {subsetof_}")
        else:
            return ui


parser = argparse.ArgumentParser()
# creating optional argument -e
parser.add_argument('-e', action='store_true', help='Edit user_input.txt file')
# create -c argument
parser.add_argument('-c', action='store_true', help='Stores custom entry for center in custom_centers.txt')
args = parser.parse_args()

# If -e flag is provided, delete the file
if args.e:
    if os.path.exists("user_input.txt"):
        os.remove("user_input.txt")

# If -c flag is provided, create a json file for storing custom centers
if args.c:
    custom_center = input("copy paste the element of center from browser: ")
    location_pattern = r'title="Availability - \d+:(.+?)[#"]'
    xpath_pattern = r'<a\s+[^>]*title="([^"]+)"[^>]*>'
    location_match = re.search(location_pattern, custom_center)
    xpath_match = re.search(xpath_pattern, custom_center)
    if location_match and xpath_match:
        location = re.sub(r'\d+\s?', '', ' '.join(word.capitalize() for word in location_match.group(1).split()))
        xpath = f'//a[@title="{xpath_match.group(1)}"]'

        # update centers in file with new data and store them in json file
        city_centers = {}
        new_centers = {location: [xpath]}
        if os.path.exists("custom_centers.txt"):
            with open("custom_centers.txt", "r") as file:
                city_centers = json.load(file)
        city_centers.update(new_centers)
        with open("custom_centers.txt", "w") as file:
            json.dump(city_centers, file)
            print("SUCCESS: custom_centers.txt file created.")
            exit()
    else:
        print("FAULTY REGEX:Can't extract Xpath or Location from Element.")
        exit()


# check if custom_centers.txt exist and load centers from that file
if os.path.exists("custom_centers.txt"):
    with open("custom_centers.txt", "r") as file:
        city_centers = json.load(file)

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
    selected_city_indices = sanitised_input("Enter the numbers corresponding to the cities you want to check (separated by space): ", str, subsetof_=(tuple(str(n) for n in range(1, len(city_centers)+1))))

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





# If not all centers are selected, filter selected_test_centers based on user input
if len(selected_city_indices) < len(city_centers):
    selected_cities = [list(city_centers.keys())[index - 1] for index in selected_city_indices]
    selected_test_centers = {city: centers for city, centers in city_centers.items() if city in selected_cities}
else:
    selected_test_centers = city_centers







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
            display = os.environ.get("DISPLAY")
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


# Set up Chrome options
options = Options()
options.add_argument("--headless")  # Headless mode
options.add_argument("--disable-gpu")  # Optional but recommended
options.add_argument("--window-size=1920,1080")  # Optional for consistent rendering
options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems
# loading webdriver for chrome
print("Loading webdriver for chrome...")
print("\033[33mThis will take a while, if this is first time.\033[0m")
print("\033[33mPlease wait...\033[0m")
driver = webdriver.Chrome(options=options)

# Now you can proceed with checking availability for the selected test centers
print("checking...")

for city, test_centers in selected_test_centers.items():

    for center in test_centers:
        # Open the desired URL
        driver.get("https://securereg3.prometric.com/Welcome.aspx")
        print("prometric website loaded...")

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

        # Appointment selection
        appointment_selection = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "masterPage_cphPageBody_ddlExam"))
        )

        if (exam_name == "STEP1"):
            appointment_selection_value = "STEP1 STEP1"
        elif (exam_name == "STEP2"):
            appointment_selection_value = "STEP2 STEP2"
        elif (exam_name == "STEP3"):
            appointment_selection_value = "STEP3 STEP3"
            
        Select(appointment_selection).select_by_value(appointment_selection_value)
        driver.find_element(By.ID, "masterPage_cphPageBody_btnNext").click()


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
        print("searching...")

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


            # Extract dates from active links and filter based on date range
            available_dates_inrange = [int(link.text) for link in active_links if start_date <= int(link.text) <= end_date]


            # Print available_dates_inrange
            if any(available_dates_inrange):
                print(f"for {city} in {month_year} from {start_date} to {end_date}: ")
                print(f'\033[92mdates found: {available_dates_inrange} \033[0m')
                notify(f"Prometric - {city}", f"dates found: {available_dates_inrange} in {month_year}")
                playsound(audio_file, block=True)


        # If no active links are found, print a message            
        except TimeoutException:
            print(f'\033[91mNo seats found for {city} in {month_year} from {start_date} to {end_date}.\033[0m')
            # notify(f"Prometric - {city}", f"No seats found in {month_year} from {start_date} to {end_date}")
            continue


driver.close()
print("\033[32mTask complete! Closing chromedriver!\033[0m")
# Read LICENSE