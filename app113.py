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

    # 🔐 LOGIN
    print("🔐 Entering credentials...", flush=True)
    driver.find_element(By.NAME, "username").send_keys("admin")
    driver.find_element(By.NAME, "password").send_keys("admin")
    driver.find_element(By.XPATH, "//button").click()

    time.sleep(5)
    print("✅ Login done", flush=True)

    # 📊 CLICK LOG RECORDS
    driver.find_element(By.LINK_TEXT, "Log Records").click()
    time.sleep(5)

    # 🔁 SWITCH TO IFRAME
    iframe = driver.find_element(By.TAG_NAME, "iframe")
    driver.switch_to.frame(iframe)

    # 🔍 FILTER DEVICE
    search_box = driver.find_element(By.XPATH, "//input[@placeholder='Search']")
    search_box.send_keys("Bhavani")
    time.sleep(2)

    driver.find_element(By.XPATH, "//*[contains(text(),'Bhavani')]").click()

    # 📅 SET DATE
    date_input = driver.find_element(By.NAME, "from_date")
    date_input.clear()
    date_input.send_keys("1")

    # 🔎 SEARCH
    driver.find_element(By.XPATH, "//button[contains(text(),'Search')]").click()
    print("📊 Report generated", flush=True)

    time.sleep(5)

    # ⬇️ EXPORT
    driver.find_element(By.XPATH, "//*[contains(text(),'Export')]").click()
    time.sleep(2)

    driver.find_element(By.XPATH, "//*[contains(text(),'Excel')]").click()

    print("📂 Download triggered", flush=True)

    driver.quit()

except Exception as e:
    print(f"❌ ERROR: {e}", flush=True)

print("🏁 DONE", flush=True)