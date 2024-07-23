import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def days_until(booking_date_str):
    date_format = "%d/%m/%Y"
    booking_date = datetime.strptime(booking_date_str, date_format)
    today = datetime.today()
    return (booking_date - today).days


holiday_dates = [
    "28/04/2024", "01/05/2024", "05/05/2024", "08/05/2024", "11/05/2024", "12/05/2024",
    "19/05/2024", "23/05/2024", "26/05/2024", "15/08/2024", "05/09/2024", "02/10/2024",
    "14/11/2024", "25/12/2024", "01/01/2025", "14/01/2025", "26/01/2025"
]

def is_holiday(date_str):
    return date_str in holiday_dates

driver = webdriver.Chrome()
driver.get("https://www.abhibus.com")
time.sleep(5)


from_station_input = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='From Station']")))
from_station_input.send_keys("Hyderabad")
time.sleep(2)
from_station_input.send_keys(Keys.ENTER)

to_station_input = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='To Station']")))
to_station_input.send_keys("Guntur")
time.sleep(2)
to_station_input.send_keys(Keys.ENTER)

date_input = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Onward Journey Date']")))
date_input.click()

desired_date = "15"
date="15/05/2024"
driver.find_element(By.XPATH, f"//span[text()='{desired_date}']").click()
time.sleep(2)

search_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'btn-search')]")))
search_button.click()
time.sleep(5)


# Wait for the service cards container to load
service_cards_container = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "service-cards-container")))

# Extract data only from within the service cards container
bus_names = service_cards_container.find_elements(By.XPATH, ".//h5[@class='title']")
descriptions = service_cards_container.find_elements(By.XPATH, ".//p[@class='sub-title']")
boarding_times = service_cards_container.find_elements(By.XPATH, ".//span[@class='departure-time text-sm']")
arrival_times = service_cards_container.find_elements(By.XPATH, ".//span[@class='arrival-time text-sm']")
journey_times = service_cards_container.find_elements(By.XPATH, ".//div[@class='chip  tertiary outlined sm travel-time col auto']")
prices = service_cards_container.find_elements(By.XPATH, ".//strong[@class='h5 fare']")
seats_available = service_cards_container.find_elements(By.XPATH, ".//div[@class='text-grey']")
ratings = service_cards_container.find_elements(By.XPATH, ".//div[@class='highRating col auto']")

date = "15/05/2024"
journey_date = datetime.strptime(date, "%d/%m/%Y")
is_weekday = journey_date.weekday() < 5
is_holiday_flag = is_holiday(date)

for i in range(len(bus_names)):
    print("Bus Name: ", bus_names[i].text)
    print("Description: ", descriptions[i].text)
    description_text = descriptions[i].text.lower()
    is_NONAC = "non-ac" in description_text
    is_AC = not is_NONAC
    print("Is AC: ", is_AC)
    print("Is NON-AC:", is_NONAC)
    is_sleeper = "sleeper" in description_text
    is_seater = "seater" in description_text
    print("Is Sleeper: ", is_sleeper)
    print("Is Seater: ", is_seater)
    print("Boarding Time: ", boarding_times[i].text)
    print("Arrival Time: ", arrival_times[i].text)
    print("Journey Time: ", journey_times[i].text)
    print("Price: $", prices[i].text)
    print("Available seats:", seats_available[i].text)
    if i < len(ratings):
        print("Rating:", ratings[i].text)
    else:
        print("Rating: Not Available")
    print("Is Weekday: ", is_weekday)
    print("Is Weekend: ", not is_weekday)
    print("Is Holiday:", is_holiday_flag)
    date_difference = days_until(date)
    print("Days until booking:", date_difference)
    print("---------------------")

time.sleep(1000)

driver.quit()
