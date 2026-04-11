from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import os
import time
import sys
import glob

sys.stdout.reconfigure(encoding='utf-8')

print("🚀 Launching browser...", flush=True)

# 🔥 Find Chromium path dynamically
base_path = "/opt/render/.cache/ms-playwright"
chromium_dirs = glob.glob(f"{base_path}/chromium-*")

if not chromium_dirs:
    print("❌ Chromium not found. Install failed.", flush=True)
    exit()

chromium_path = os.path.join(chromium_dirs[0], "chrome-linux", "chrome")

print(f"✅ Using Chromium: {chromium_path}", flush=True)

# ---------------- Selenium Setup ----------------
options = Options()
options.binary_location = chromium_path
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=options)

# ---------------- LOGIN ----------------
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