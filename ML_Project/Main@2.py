import csv
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


def days_until(booking_date_str):
    date_format = "%d/%m/%Y"
    booking_date = datetime.strptime(booking_date_str, date_format)
    today = datetime.today()
    return (booking_date - today).days


holiday_dates = [
    "23/05/2024", "26/05/2024", "02/06/2024", "09/06/2024", "16/06/2024", "17/06/2024", "23/06/2024", "30/06/2024",
    "07/07/2024", "14/07/2024", "17/07/2024", "21/07/2024", "28/07/2024", "04/08/2024", "11/08/2024", "15/08/2024",
    "18/08/2024", "19/08/2024", "25/08/2024", "26/08/2024", "08/09/2024", "02/10/2024", "14/11/2024", "25/12/2024",
    "01/01/2025", "14/01/2025", "26/01/2025"
]


def is_holiday(date_str):
    return date_str in holiday_dates

# WEBDRIVER

driver = webdriver.Chrome()
driver.get("https://www.abhibus.com")
time.sleep(5)

# FROM STATION
from_station_input = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='From Station']")))
from_station_input.send_keys("Hyderabad")
time.sleep(2)
from_station_input.send_keys(Keys.ENTER)

# TO STATION
to_station_input = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='To Station']")))
to_station_input.send_keys("Guntur")
time.sleep(2)
to_station_input.send_keys(Keys.ENTER)

# DATE INPUT
date_input = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Onward Journey Date']")))
date_input.click()

desired_date = "29"
date = "29/07/2024"
driver.find_element(By.XPATH, f"//span[text()='{desired_date}']").click()
time.sleep(2)

# CLICK SEARCH BUTTON
search_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'btn-search')]")))
search_button.click()
time.sleep(5)

# ALL BUS
try:
    service_cards_container = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.ID, "service-cards-container")))
except TimeoutException:
    print("Timed out waiting for service cards container to load")
    driver.quit()
    exit()

# ONE BUS
service_cards = service_cards_container.find_elements(By.XPATH, "//div[@class='row card-body service-info lighter ']")
# WEEKDAY OR WEEKEND
journey_date = datetime.strptime(date, "%d/%m/%Y")
is_weekday = journey_date.weekday() < 5
# HOLIDAY
is_holiday_flag = is_holiday(date)

# Prepare CSV file....1
with open("bus.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Bus Name", "Description", "Is AC", "Is NON-AC", "Is Sleeper", "Is Seater",
                     "Boarding Time", "Arrival Time", "Journey Time", "Price", "Available Seats",
                     "Rating", "Is Weekday", "Is Weekend", "Is Holiday", "Days until Booking"])

    for card in service_cards:
        bus_name = card.find_element(By.XPATH, ".//h5[@class='title']").text
        description = card.find_element(By.XPATH, ".//p[@class='sub-title']").text.lower()
        is_NONAC = "non-ac" in description
        is_AC = not is_NONAC
        is_sleeper = "sleeper" in description
        is_seater = "seater" in description
        boarding_time = card.find_element(By.XPATH, ".//span[@class='departure-time text-sm']").text
        arrival_time = card.find_element(By.XPATH, ".//span[@class='arrival-time text-sm']").text
        journey_time = card.find_element(By.XPATH, ".//div[@class='chip  tertiary outlined sm travel-time col auto']").text
        price = card.find_element(By.XPATH, ".//strong[@class='h5 fare']").text
        seats_available = card.find_element(By.XPATH, ".//div[@class='text-grey']").text

        try:
            rating = card.find_element(By.XPATH, ".//div[@class='highRating col auto']").text
        except:
            rating = "Not Available"

        writer.writerow([bus_name, description, is_AC, is_NONAC, is_sleeper, is_seater,
                         boarding_time, arrival_time, journey_time, price, seats_available,
                         rating, is_weekday, not is_weekday, is_holiday_flag, days_until(date)])
# Prepare CSV file....2
driver.get("https://www.abhibus.com/bus_search/Hyderabad/3/Guntur/15/30-07-2024/O")
time.sleep(5)

# Wait for the service cards container with a longer timeout
try:
    service_cards_container = WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.ID, "service-cards-container")))
except TimeoutException:
    print("Timed out waiting for service cards container to load")
    driver.quit()
    exit()

# Extract data only from within the service cards container
service_cards = service_cards_container.find_elements(By.XPATH, "//div[@class='row card-body service-info lighter ']")

date = "30/07/2024"
journey_date = datetime.strptime(date, "%d/%m/%Y")
is_weekday = journey_date.weekday() < 5
is_holiday_flag = is_holiday(date)

# Append data to the CSV file
with open("bus.csv", "a", newline="") as csvfile:
    writer = csv.writer(csvfile)

    for card in service_cards:
        bus_name = card.find_element(By.XPATH, ".//h5[@class='title']").text
        description = card.find_element(By.XPATH, ".//p[@class='sub-title']").text.lower()
        is_NONAC = "non-ac" in description
        is_AC = not is_NONAC
        is_sleeper = "sleeper" in description
        is_seater = "seater" in description
        boarding_time = card.find_element(By.XPATH, ".//span[@class='departure-time text-sm']").text
        arrival_time = card.find_element(By.XPATH, ".//span[@class='arrival-time text-sm']").text
        journey_time = card.find_element(By.XPATH, ".//div[@class='chip  tertiary outlined sm travel-time col auto']").text
        price = card.find_element(By.XPATH, ".//strong[@class='h5 fare']").text
        seats_available = card.find_element(By.XPATH, ".//div[@class='text-grey']").text

        try:
            rating = card.find_element(By.XPATH, ".//div[@class='highRating col auto']").text
        except:
            rating = "Not Available"

        writer.writerow([bus_name, description, is_AC, is_NONAC, is_sleeper, is_seater,
                         boarding_time, arrival_time, journey_time, price, seats_available,
                         rating, is_weekday, not is_weekday, is_holiday_flag, days_until(date)])

# Prepare CSV file....3
driver.get("https://www.abhibus.com/bus_search/Hyderabad/3/Guntur/15/31-07-2024/O")
time.sleep(5)
try:
    service_cards_container = WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.ID, "service-cards-container")))
except TimeoutException:
    print("Timed out waiting for service cards container to load")
    driver.quit()
    exit()
service_cards = service_cards_container.find_elements(By.XPATH, "//div[@class='row card-body service-info lighter ']")

date = "31/07/2024"
journey_date = datetime.strptime(date, "%d/%m/%Y")
is_weekday = journey_date.weekday() < 5
is_holiday_flag = is_holiday(date)

# Append data to the CSV file
with open("bus.csv", "a", newline="") as csvfile:
    writer = csv.writer(csvfile)

    for card in service_cards:
        bus_name = card.find_element(By.XPATH, ".//h5[@class='title']").text
        description = card.find_element(By.XPATH, ".//p[@class='sub-title']").text.lower()
        is_NONAC = "non-ac" in description
        is_AC = not is_NONAC
        is_sleeper = "sleeper" in description
        is_seater = "seater" in description
        boarding_time = card.find_element(By.XPATH, ".//span[@class='departure-time text-sm']").text
        arrival_time = card.find_element(By.XPATH, ".//span[@class='arrival-time text-sm']").text
        journey_time = card.find_element(By.XPATH, ".//div[@class='chip  tertiary outlined sm travel-time col auto']").text
        price = card.find_element(By.XPATH, ".//strong[@class='h5 fare']").text
        seats_available = card.find_element(By.XPATH, ".//div[@class='text-grey']").text

        try:
            rating = card.find_element(By.XPATH, ".//div[@class='highRating col auto']").text
        except:
            rating = "Not Available"

        writer.writerow([bus_name, description, is_AC, is_NONAC, is_sleeper, is_seater,
                         boarding_time, arrival_time, journey_time, price, seats_available,
                         rating, is_weekday, not is_weekday, is_holiday_flag, days_until(date)])
# Prepare CSV file....4
driver.get("https://www.abhibus.com/bus_search/Hyderabad/3/Guntur/15/01-08-2024/O")
time.sleep(5)

try:
    service_cards_container = WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.ID, "service-cards-container")))
except TimeoutException:
    print("Timed out waiting for service cards container to load")
    driver.quit()
    exit()
service_cards = service_cards_container.find_elements(By.XPATH, "//div[@class='row card-body service-info lighter ']")

date = "01/08/2024"
journey_date = datetime.strptime(date, "%d/%m/%Y")
is_weekday = journey_date.weekday() < 5
is_holiday_flag = is_holiday(date)

# Append data to the CSV file
with open("bus.csv", "a", newline="") as csvfile:
    writer = csv.writer(csvfile)

    for card in service_cards:
        bus_name = card.find_element(By.XPATH, ".//h5[@class='title']").text
        description = card.find_element(By.XPATH, ".//p[@class='sub-title']").text.lower()
        is_NONAC = "non-ac" in description
        is_AC = not is_NONAC
        is_sleeper = "sleeper" in description
        is_seater = "seater" in description
        boarding_time = card.find_element(By.XPATH, ".//span[@class='departure-time text-sm']").text
        arrival_time = card.find_element(By.XPATH, ".//span[@class='arrival-time text-sm']").text
        journey_time = card.find_element(By.XPATH, ".//div[@class='chip  tertiary outlined sm travel-time col auto']").text
        price = card.find_element(By.XPATH, ".//strong[@class='h5 fare']").text
        seats_available = card.find_element(By.XPATH, ".//div[@class='text-grey']").text

        try:
            rating = card.find_element(By.XPATH, ".//div[@class='highRating col auto']").text
        except:
            rating = "Not Available"

        writer.writerow([bus_name, description, is_AC, is_NONAC, is_sleeper, is_seater,
                         boarding_time, arrival_time, journey_time, price, seats_available,
                         rating, is_weekday, not is_weekday, is_holiday_flag, days_until(date)])
# Prepare CSV file....5
driver.get("https://www.abhibus.com/bus_search/Hyderabad/3/Guntur/15/02-08-2024/O")
time.sleep(5)

try:
    service_cards_container = WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.ID, "service-cards-container")))
except TimeoutException:
    print("Timed out waiting for service cards container to load")
    driver.quit()
    exit()
service_cards = service_cards_container.find_elements(By.XPATH, "//div[@class='row card-body service-info lighter ']")

date = "02/08/2024"
journey_date = datetime.strptime(date, "%d/%m/%Y")
is_weekday = journey_date.weekday() < 5
is_holiday_flag = is_holiday(date)

# Append data to the CSV file
with open("bus.csv", "a", newline="") as csvfile:
    writer = csv.writer(csvfile)

    for card in service_cards:
        bus_name = card.find_element(By.XPATH, ".//h5[@class='title']").text
        description = card.find_element(By.XPATH, ".//p[@class='sub-title']").text.lower()
        is_NONAC = "non-ac" in description
        is_AC = not is_NONAC
        is_sleeper = "sleeper" in description
        is_seater = "seater" in description
        boarding_time = card.find_element(By.XPATH, ".//span[@class='departure-time text-sm']").text
        arrival_time = card.find_element(By.XPATH, ".//span[@class='arrival-time text-sm']").text
        journey_time = card.find_element(By.XPATH, ".//div[@class='chip  tertiary outlined sm travel-time col auto']").text
        price = card.find_element(By.XPATH, ".//strong[@class='h5 fare']").text
        seats_available = card.find_element(By.XPATH, ".//div[@class='text-grey']").text

        try:
            rating = card.find_element(By.XPATH, ".//div[@class='highRating col auto']").text
        except:
            rating = "Not Available"

        writer.writerow([bus_name, description, is_AC, is_NONAC, is_sleeper, is_seater,
                         boarding_time, arrival_time, journey_time, price, seats_available,
                         rating, is_weekday, not is_weekday, is_holiday_flag, days_until(date)])
# Prepare CSV file....6

driver.get("https://www.abhibus.com/bus_search/Hyderabad/3/Guntur/15/03-08-2024/O")
time.sleep(5)
try:
    service_cards_container = WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.ID, "service-cards-container")))
except TimeoutException:
    print("Timed out waiting for service cards container to load")
    driver.quit()
    exit()
service_cards = service_cards_container.find_elements(By.XPATH, "//div[@class='row card-body service-info lighter ']")
date = "03/08/2024"
journey_date = datetime.strptime(date, "%d/%m/%Y")
is_weekday = journey_date.weekday() < 5
is_holiday_flag = is_holiday(date)

# Append data to the CSV file
with open("bus.csv", "a", newline="") as csvfile:
    writer = csv.writer(csvfile)

    for card in service_cards:
        bus_name = card.find_element(By.XPATH, ".//h5[@class='title']").text
        description = card.find_element(By.XPATH, ".//p[@class='sub-title']").text.lower()
        is_NONAC = "non-ac" in description
        is_AC = not is_NONAC
        is_sleeper = "sleeper" in description
        is_seater = "seater" in description
        boarding_time = card.find_element(By.XPATH, ".//span[@class='departure-time text-sm']").text
        arrival_time = card.find_element(By.XPATH, ".//span[@class='arrival-time text-sm']").text
        journey_time = card.find_element(By.XPATH, ".//div[@class='chip  tertiary outlined sm travel-time col auto']").text
        price = card.find_element(By.XPATH, ".//strong[@class='h5 fare']").text
        seats_available = card.find_element(By.XPATH, ".//div[@class='text-grey']").text

        try:
            rating = card.find_element(By.XPATH, ".//div[@class='highRating col auto']").text
        except:
            rating = "Not Available"

        writer.writerow([bus_name, description, is_AC, is_NONAC, is_sleeper, is_seater,
                         boarding_time, arrival_time, journey_time, price, seats_available,
                         rating, is_weekday, not is_weekday, is_holiday_flag, days_until(date)])
# Prepare CSV file....7
driver.get("https://www.abhibus.com/bus_search/Hyderabad/3/Guntur/15/04-08-2024/O")
time.sleep(5)

try:
    service_cards_container = WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.ID, "service-cards-container")))
except TimeoutException:
    print("Timed out waiting for service cards container to load")
    driver.quit()
    exit()
service_cards = service_cards_container.find_elements(By.XPATH, "//div[@class='row card-body service-info lighter ']")

date = "04/08/2024"
journey_date = datetime.strptime(date, "%d/%m/%Y")
is_weekday = journey_date.weekday() < 5
is_holiday_flag = is_holiday(date)

# Append data to the CSV file
with open("bus.csv", "a", newline="") as csvfile:
    writer = csv.writer(csvfile)

    for card in service_cards:
        bus_name = card.find_element(By.XPATH, ".//h5[@class='title']").text
        description = card.find_element(By.XPATH, ".//p[@class='sub-title']").text.lower()
        is_NONAC = "non-ac" in description
        is_AC = not is_NONAC
        is_sleeper = "sleeper" in description
        is_seater = "seater" in description
        boarding_time = card.find_element(By.XPATH, ".//span[@class='departure-time text-sm']").text
        arrival_time = card.find_element(By.XPATH, ".//span[@class='arrival-time text-sm']").text
        journey_time = card.find_element(By.XPATH, ".//div[@class='chip  tertiary outlined sm travel-time col auto']").text
        price = card.find_element(By.XPATH, ".//strong[@class='h5 fare']").text
        seats_available = card.find_element(By.XPATH, ".//div[@class='text-grey']").text

        try:
            rating = card.find_element(By.XPATH, ".//div[@class='highRating col auto']").text
        except:
            rating = "Not Available"

        writer.writerow([bus_name, description, is_AC, is_NONAC, is_sleeper, is_seater,
                         boarding_time, arrival_time, journey_time, price, seats_available,
                         rating, is_weekday, not is_weekday, is_holiday_flag, days_until(date)])
# Prepare CSV file....8
driver.get("https://www.abhibus.com/bus_search/Hyderabad/3/Guntur/15/05-08-2024/O")
time.sleep(5)

try:
    service_cards_container = WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.ID, "service-cards-container")))
except TimeoutException:
    print("Timed out waiting for service cards container to load")
    driver.quit()
    exit()
service_cards = service_cards_container.find_elements(By.XPATH, "//div[@class='row card-body service-info lighter ']")

date = "05/08/2024"
journey_date = datetime.strptime(date, "%d/%m/%Y")
is_weekday = journey_date.weekday() < 5
is_holiday_flag = is_holiday(date)

# Append data to the CSV file
with open("bus.csv", "a", newline="") as csvfile:
    writer = csv.writer(csvfile)

    for card in service_cards:
        bus_name = card.find_element(By.XPATH, ".//h5[@class='title']").text
        description = card.find_element(By.XPATH, ".//p[@class='sub-title']").text.lower()
        is_NONAC = "non-ac" in description
        is_AC = not is_NONAC
        is_sleeper = "sleeper" in description
        is_seater = "seater" in description
        boarding_time = card.find_element(By.XPATH, ".//span[@class='departure-time text-sm']").text
        arrival_time = card.find_element(By.XPATH, ".//span[@class='arrival-time text-sm']").text
        journey_time = card.find_element(By.XPATH, ".//div[@class='chip  tertiary outlined sm travel-time col auto']").text
        price = card.find_element(By.XPATH, ".//strong[@class='h5 fare']").text
        seats_available = card.find_element(By.XPATH, ".//div[@class='text-grey']").text

        try:
            rating = card.find_element(By.XPATH, ".//div[@class='highRating col auto']").text
        except:
            rating = "Not Available"

        writer.writerow([bus_name, description, is_AC, is_NONAC, is_sleeper, is_seater,
                         boarding_time, arrival_time, journey_time, price, seats_available,
                         rating, is_weekday, not is_weekday, is_holiday_flag, days_until(date)])

time.sleep(10)
driver.quit()
