from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from datetime import datetime
import time
import os
import pandas as pd
import sys

sys.stdout.reconfigure(encoding='utf-8')

# ---------------- CONFIG ----------------
USERNAME = "bhavani_khurja"
PASSWORD = "Bhavani@123"

download_path = "/tmp/downloads"
os.makedirs(download_path, exist_ok=True)

UPLOAD_URL = "https://eportal.beplkhurja.in/uploadcsv.php"
PIN = "1234"

# ---------------- DATE ----------------
today = datetime.now()
day = today.day
from_day = "1" if day <= 15 else "16"

print(f"📅 Using From Date: {from_day}", flush=True)

# ---------------- SELENIUM SETUP ----------------
print("🚀 Launching browser...", flush=True)

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# download settings
prefs = {
    "download.default_directory": download_path,
    "download.prompt_for_download": False,
    "directory_upgrade": True
}
chrome_options.add_experimental_option("prefs", prefs)

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=chrome_options
)

driver.set_page_load_timeout(120)

# ---------------- LOGIN ----------------
print("🌐 Opening Login Page...", flush=True)

driver.get("http://203.92.32.167:8083/iclock/")
time.sleep(5)

print("🔐 Entering credentials...", flush=True)

driver.find_element(By.NAME, "username").send_keys(USERNAME)
driver.find_element(By.NAME, "userpwd").send_keys(PASSWORD)
driver.find_element(By.XPATH, "//input[@value='Login']").click()

time.sleep(8)
print("✅ Login done", flush=True)

# ---------------- NAVIGATION ----------------
print("📊 Opening Reports...", flush=True)

driver.find_element(By.LINK_TEXT, "Reports").click()
time.sleep(2)
driver.find_element(By.LINK_TEXT, "Log Records").click()

time.sleep(8)

# ---------------- EXPORT (basic version) ----------------
print("⬇️ Trying export...", flush=True)

try:
    driver.find_element(By.XPATH, "//button[contains(text(),'Export')]").click()
    time.sleep(5)
    print("📂 Export triggered", flush=True)
except:
    print("⚠️ Export button not found (check UI)", flush=True)

# ---------------- UPLOAD ----------------
print("📤 Uploading...", flush=True)

driver.get(UPLOAD_URL)
time.sleep(5)

driver.find_element(By.NAME, "pin").send_keys(PIN)

# find latest file
files = os.listdir(download_path)
if files:
    latest_file = os.path.join(download_path, files[-1])
    driver.find_element(By.NAME, "csv_file").send_keys(latest_file)
    driver.find_element(By.NAME, "upload").click()
    print("✅ Upload submitted", flush=True)
else:
    print("❌ No file found to upload", flush=True)

time.sleep(5)

driver.quit()
print("🏁 DONE", flush=True)