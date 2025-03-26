import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By


# ==== Configuration ====
CHROMEDRIVER_PATH = "/path/to/chromedriver"  # Update this
COOKIES_FILE = "linkedin_cookies.json"
PROFILE_URL = "https://www.linkedin.com/in/YOUR_USERNAME_HERE/"

# ==== Setup Selenium ====
options = webdriver.ChromeOptions()
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
# options.add_argument("--headless")  # Uncomment for headless mode

driver = webdriver.Chrome(service=Service(CHROMEDRIVER_PATH), options=options)
driver.get("https://www.linkedin.com/")

# ==== Load Cookies ====
with open(COOKIES_FILE, "r") as f:
    cookies = json.load(f)

for cookie in cookies:
    if 'sameSite' in cookie:
        del cookie['sameSite']  # Avoid issues with ChromeDriver
    driver.add_cookie(cookie)

# ==== Load Your Profile ====
driver.get(PROFILE_URL)
time.sleep(5)

# ==== Scrape Data ====
try:
    name = driver.find_element(By.CSS_SELECTOR, "h1").text
    headline = driver.find_element(By.CSS_SELECTOR, "div.text-body-medium").text
    location = driver.find_element(By.CSS_SELECTOR, "span.text-body-small.inline").text

    print("Name:", name)
    print("Headline:", headline)
    print("Location:", location)
except Exception as e:
    print("Error while scraping:", e)

driver.quit()
