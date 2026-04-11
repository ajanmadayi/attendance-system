from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import sys

sys.stdout.reconfigure(encoding='utf-8')

print("🚀 Launching browser...", flush=True)

options = Options()
options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# 🔥 THIS LINE IS KEY (Render compatible)
options.binary_location = "/usr/bin/chromium-browser"

driver = webdriver.Chrome(options=options)

print("🌐 Opening Login Page...", flush=True)

driver.get("http://203.92.32.167:8083/iclock/")
time.sleep(5)

print("🔐 Entering credentials...", flush=True)

driver.find_element(By.NAME, "username").send_keys("bhavani_khurja")
driver.find_element(By.NAME, "userpwd").send_keys("Bhavani@123")
driver.find_element(By.XPATH, "//input[@value='Login']").click()

time.sleep(5)

print("🏁 DONE", flush=True)

driver.quit()