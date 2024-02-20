import os
import platform
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
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

print(prometric_logo)
print("Welcome to the Test Center Availability Checker!")
print("------------------------------------------------")
print("This script helps you check for available test center slots for your exam.")
print("You'll be prompted to provide some initial information, such as the exam name, month and year,")
print("and date range to search for available slots.")
print("Once dates found it will play alert.mp3")
print("Let's get started!")
print("------------------------------------------------")


# Check if it's the first time running the script
try:
    with open("user_input.txt", "r") as file:
        # If file exists, read values from it
        exam_name, month_year, selected_city_indices, start_date, end_date= file.read().split(',')
        print("Values loaded from previous session file user_input.txt.")
except FileNotFoundError:
    # If file doesn't exist, prompt user for input
    exam_name = input("Enter exam name (STEP1/STEP2): ")
    month_year = input("Enter month and year (3 2024): ")

    # Display available cities to the user and prompt for selection
    print("Available cities:")
    for index, city in enumerate(city_centers.keys(), start=1):
        print(f"{index}. {city}")

    # input for cities
    selected_city_indices = input("Enter the numbers corresponding to the cities you want to check (separated by space): ") or '1 2'

    start_date = input("Enter start date (1): ")
    end_date = input("Enter end date (32): ")

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


audio_file = "alert.mp3"
operating_system = platform.system()
# invisible browser
options = Options()
options.add_argument("--headless=new")
driver = webdriver.Chrome(options=options)


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


for city, test_centers in selected_test_centers.items():

    for center in test_centers:

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

            print(f"center '{center}' for month and year '{month_year}' in range '{start_date}'-'{end_date}':")

            # Extract dates from active links and filter based on date range
            available_dates_inrange = [int(link.text) for link in active_links if start_date <= int(link.text) < end_date]


            # Print available_dates_inrange
            print('\033[92m' + 'dates found: ' + '\033[0m', available_dates_inrange)

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
            print(f'\033[91mNo seats found for \'{center}\' in \'{month_year}\' from \'{start_date}\' to \'{end_date}\'.\033[0m')
            continue


driver.close()

print_progress_bar(total_iterations, total_iterations)

# Read LICENSE