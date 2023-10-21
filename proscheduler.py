from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

# Assuming you've set up your WebDriver (like ChromeDriver)
driver = webdriver.Chrome()

# Open the desired URL
driver.get("https://securereg3.prometric.com/Welcome.aspx")

# select step 1 in drop down menu
programs_menu = driver.find_element(By.ID, "masterPage_cphPageBody_ddlPrograms")
Select(programs_menu).select_by_value("STEP1")

#select country
country_menu = driver.find_element(By.ID, "masterPage_cphPageBody_ddlCountry")
Select(country_menu).select_by_value("PAK")

#click next button
driver.find_element(By.ID, "masterPage_cphPageBody_btnNext").click()


# wait for page to load
# Click the initial link
initial_link = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.ID, "masterPage_cphPageBody_lnkSeatAvail2"))
)
initial_link.click()

# wait for page to load
# Find the search input element and enter "Lahore, Pakistan"
search_input = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.ID, "txtSearch"))
)
search_input.send_keys("Lahore, Pakistan")

# Find the search button and click it
search_button = driver.find_element(By.ID, "btnSearch")
search_button.click()

# Find the link element and click it
availability_link = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//a[@title='Availability - 8783:LAHORE, PAKISTAN#8783']"))
)
availability_link.click()

# Find the dropdown element
dropdown_month = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.ID, "masterPage_cphPageBody_monthYearlist"))
)


# Read user input from a text file
with open('month_year.txt', 'r') as file:
    user_input = file.read().strip()

# Select the option with the value user_input i.e "12 2023"
Select(dropdown_month).select_by_value(user_input)

# Find the submit button and click it
submit_button = driver.find_element(By.ID, "masterPage_cphPageBody_btnGoCal")
submit_button.click()


#check for active links... Availability
# Wait for all elements with class="calActiveLink" to be clickable
active_links = WebDriverWait(driver, 10).until(
    EC.presence_of_all_elements_located((By.CLASS_NAME, "calActiveLink"))
)

if active_links:
    # Print the values
    for link in active_links:
        print(link.text)
else:
    # No active links found
    print("Not available!!")