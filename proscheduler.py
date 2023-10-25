import os
import platform
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException


'''Hello! people, you can edit code bellow to fit your needs. Remember! only edit text inside
qoutes in front of equal sign. Also keep capital letters as they're, python is case sensitive.
Don't add any unnecessary spaces.
To select step2, change exam_name = "STEP2".
To select month and year, for example December 2023, change month_year = "12 2023",
similarly for April 2024, change month_year = "4 2024". Don't add any extra Zeros.
Also, you can store any mp3 file in the same folder to alert you. just remember to rename it to alert.mp3.

This script checks for open slots in Islamabad, Karachi, and Lahore prometric-test centers.
It was written in 2023, and might not work because of any major website updates in future.

Wish you good luck for your usmle journey!!!
'''

exam_name = "STEP1"
month_year = "3 2024"


region = "PAK"
addresses = {
    "Lahore, Pakistan": ["//a[@title='Availability - 8783:LAHORE, PAKISTAN#8783']",
                          "//a[@title='Availability - 8782:ISLAMABAD, PAKISTAN #8782']"],
                          
    "Karachi, Pakistan": ["//a[@title='Availability - 8781:KARACHI, PAKISTAN #8781']"]
              }

audiofile = "alert.mp3"
driver = webdriver.Chrome()

for address, test_centers in addresses.items():

    for center in test_centers:

        # Open the desired URL
        driver.get("https://securereg3.prometric.com/Welcome.aspx")

        # select exam_name in drop down menu
        programs_menu = driver.find_element(By.ID, "masterPage_cphPageBody_ddlPrograms")
        Select(programs_menu).select_by_value(exam_name)

        #select country
        country_menu = driver.find_element(By.ID, "masterPage_cphPageBody_ddlCountry")
        Select(country_menu).select_by_value(region)

        #click next button
        driver.find_element(By.ID, "masterPage_cphPageBody_btnNext").click()


        # wait for page to load
        # Click the initial link
        initial_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "masterPage_cphPageBody_lnkSeatAvail2"))
        )
        initial_link.click()

        # wait for page to load
        # Find the search input element and enter address "Lahore, Pakistan"
        search_input = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "txtSearch"))
        )
        # change address
        search_input.send_keys(address)

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

            print(f"following dates are availalbe in center '{center}' for month and year '{month_year}'.")

            # Print each active link's text
            for link in active_links:
                print(link.text)

            #open a media file to alert user
            if active_links:
                if platform.system() == "Windows":
                    os.startfile(audiofile)
                elif platform.system() == "Darwin":
                    os.system(f"open {audiofile}")
                elif platform.system() == "Linux":
                    os.system(f"xdg-open {audiofile}")
                else:
                    print("unsupported operating system/ media player to play audio!")
        except TimeoutException:
            print(f"following dates are availalbe in center '{center}' for month and year '{month_year}'.")
            print("Seats not available!! Timeout while waiting for active links.")


# Read LICENSE