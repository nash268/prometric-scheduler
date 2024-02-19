import os
import platform
import pywhatkit
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC


country = "PAK"
city_centers = {
    "Lahore, Pakistan": ["//a[@title='Availability - 8783:LAHORE, PAKISTAN#8783']",
                          "//a[@title='Availability - 8782:ISLAMABAD, PAKISTAN #8782']"],
                          
    "Karachi, Pakistan": ["//a[@title='Availability - 8781:KARACHI, PAKISTAN #8781']"]
              }


print("Welcome to the Test Center Availability Checker!")
print("------------------------------------------------")
print("This script helps you check for available test center slots for your exam.")
print("You'll be prompted to provide some initial information, such as the exam name, month and year,")
print("and date range to search for available slots.")
print("If desired, you can also choose to receive a WhatsApp message notification with the results.")
print("Please ensure that WhatsApp is logged in to your default browser for this feature to work.")
print("Let's get started!")
print("------------------------------------------------")


# Check if it's the first time running the script
try:
    with open("user_input.txt", "r") as file:
        # If file exists, read values from it
        exam_name, month_year, selected_city_indices, start_date, end_date, send_msg_to_yourself, phone= file.read().split(',')
        selected_city_indices = [int(index) for index in selected_city_indices.split(' ')]
        print("Values loaded from previous session.")
except FileNotFoundError:
    # If file doesn't exist, prompt user for input
    exam_name = input("Enter exam name: STEP1/STEP2").capatilize()
    month_year = input("Enter month and year (e.g. 3 2024): ")

    # Display available cities to the user and prompt for selection
    print("Available cities:")
    for index, city in enumerate(city_centers.keys(), start=1):
        print(f"{index}. {city}")

    # input for cities
    selected_city_indices = input("Enter the numbers corresponding to the cities you want to check (separated by space): ")

    start_date = int(input("Enter start date: "))
    end_date = int(input("Enter end date: "))
    send_msg_to_yourself = input("send whatsapp message to yourself(whatsapp must be logged in default browser). yes/no: ")
    if send_msg_to_yourself == "yes":
        phone = input("whatsapp number: ")
    else:
        phone = ""

    # Write input values to file for later use
    with open("user_input.txt", "w") as file:
        file.write(f"{exam_name},{month_year},{selected_city_indices},{start_date},{end_date},{send_msg_to_yourself},{phone}")
        selected_city_indices = [int(index) for index in selected_city_indices.split(' ')]
        print("Values stored for later use.")


# Validate user input for city selection
for index in selected_city_indices:
    if index < 1 or index > len(city_centers):
        print("Invalid selection. Please enter numbers within the range.")
        exit()

# Gather selected test centers based on user input
selected_test_centers = {city: centers for city, centers in city_centers.items()}

# If not all centers are selected, filter selected_test_centers based on user input
if len(selected_city_indices) < len(city_centers):
    selected_cities = [city[index - 1] for index in selected_city_indices]
    selected_test_centers = {city: centers for city, centers in selected_test_centers.items() if city in selected_cities}


# Now you can proceed with checking availability for the selected test centers
print("checking...")


audio_file = "alert.mp3"
operating_system = platform.system()
driver = webdriver.Chrome()

msg_contents = ''
available_dates_inrange_msg = []

def send_msg(msg_body, phone):
    try:
        # wait 60 seconds before sending to let things load
        pywhatkit.sendwhatmsg_instantly(phone, msg_body, 60, close_tab=True)
        print("message sent successfully!")
    except:
        print("unexpected error when sending whatsapp message")


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

            print(f"center '{center}' for month and year '{month_year}' in range '{start_date}'-'{end_date}':")
            # create whatsapp msg contents
            msg_contents += f"center '{center}' for month and year '{month_year}' in range '{start_date}'-'{end_date}': "

            # Extract dates from active links and filter based on date range
            available_dates_inrange = [int(link.text) for link in active_links if start_date <= int(link.text) < end_date]


            # Print available_dates_inrange
            print('dates found: ', available_dates_inrange)
            # create whatsapp msg content
            available_dates_inrange_msg.extend(available_dates_inrange)
            msg_contents += f"dates found: {available_dates_inrange}"

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
            print(f"No seats found for '{center}' in '{month_year}' from '{start_date}' to '{end_date}'.")
            continue


driver.close()

if any(available_dates_inrange_msg) and (send_msg_to_yourself == "yes"):
    send_msg(msg_contents, phone)

# Read LICENSE