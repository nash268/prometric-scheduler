import os
import platform
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC


'''Hello! people, you can edit code bellow to fit your needs. Remember! only edit text inside
qoutes in front of equal sign. Also keep capital letters as they're, python is case sensitive.
Don't add any unnecessary spaces.
To select step2, change exam_name = "STEP2".
To select month and year, for example December 2023, change month_year = "12 2023",
similarly for April 2024, change month_year = "4 2024". Don't add any extra Zeros.
Also, you can store any mp3 file in the same folder to alert you. just remember to rename it to alert.mp3.

This script checks for open slots in Islamabad, Karachi, and Lahore prometric-test centers.
It was written in 2023, and may not work because of any major website updates in future.

Wish you good luck for your usmle journey!!!
'''

exam_name = "STEP1"
month_year = "3 2024"
start_date = 1
end_date = 30


country = "PAK"
city_centers = {
    "Lahore, Pakistan": ["//a[@title='Availability - 8783:LAHORE, PAKISTAN#8783']",
                          "//a[@title='Availability - 8782:ISLAMABAD, PAKISTAN #8782']"],
                          
    "Karachi, Pakistan": ["//a[@title='Availability - 8781:KARACHI, PAKISTAN #8781']"]
              }

audio_file = "alert.mp3"
driver = webdriver.Chrome()

for city, test_centers in city_centers.items():

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



        # Select the option with the value user_input i.e "12 2023".
        # select month and year.......................................
        Select(dropdown_month).select_by_value(month_year)
        #.............................................................

        # Find the submit button and click it
        submit_button = driver.find_element(By.ID, "masterPage_cphPageBody_btnGoCal")
        submit_button.click()


        try:
            # Check for active links' availability
            active_links = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "calActiveLink"))
            )

            print(f"following dates are availalbe in center '{center}' for month and year '{month_year}' in range '{start_date}'-'{end_date}'.")

            # Extract dates from active links
            available_dates = [link.text for link in active_links]
            # Assuming available_dates is a list of strings representing numbers
            available_dates_int = [int(date_str) for date_str in available_dates]
            # Check if any date in available_dates_int falls within the range from 1 to 15
            available_dates_inrange = (date in range(start_date, end_date) for date in available_dates_int)


            # Print each active link's text
            print(available_dates_inrange)

            #check if dates are 27 or 28
            if any(available_dates_inrange):
                #play media file to alert user
                print("Playing the audio file...")
                if platform.system() == "Windows":
                    os.startfile(audio_file)
                elif platform.system() == "Darwin":
                    os.system(f"open {audio_file}")
                elif platform.system() == "Linux":
                    os.system(f"xdg-open {audio_file}")
                else:
                    print("unsupported operating system/ media player to play audio!")
            else: 
                print("seats not available for 27 or 28 march")
        except TimeoutException:
            print(f"following dates are availalbe in center '{center}' for month and year '{month_year}' in range '{start_date}'-'{end_date}'.")
            print("Seats not available!! Timeout while waiting for active links.")


# Read LICENSE