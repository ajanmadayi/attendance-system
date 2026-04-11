from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

print("📅 Using From Date: 1", flush=True)

try:
    print("🚀 Launching browser...", flush=True)

    options = Options()
    options.binary_location = "/usr/bin/chromium"

    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)

    print("🌐 Opening Login Page...", flush=True)
    driver.get("http://203.92.32.167:8083/iclock/")

    time.sleep(3)

    print("🔐 Entering credentials...", flush=True)
    driver.find_element(By.NAME, "username").send_keys("admin")
    driver.find_element(By.NAME, "password").send_keys("admin")
    driver.find_element(By.XPATH, "//button").click()

    time.sleep(5)
    print("✅ Login done", flush=True)

    driver.quit()

except Exception as e:
    print(f"❌ ERROR: {e}", flush=True)

print("🏁 DONE", flush=True)