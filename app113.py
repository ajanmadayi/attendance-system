from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from datetime import datetime
import os
import time
import pandas as pd
import sys

# Encoding fix
sys.stdout.reconfigure(encoding='utf-8')

# ---------------- CONFIG ----------------
USERNAME = "bhavani_khurja"
PASSWORD = "Bhavani@123"

download_path = "/tmp/downloads"

if not os.path.exists(download_path):
    os.makedirs(download_path)

UPLOAD_URL = "https://eportal.beplkhurja.in/uploadcsv.php"
PIN = "1234"

# ---------------- DOWNLOAD WAIT ----------------
def wait_for_download_complete(folder, timeout=180):
    print("⏳ Waiting for download...")
    start = time.time()

    while True:
        files = os.listdir(folder)

        if any(f.endswith(".crdownload") for f in files):
            time.sleep(2)
            continue

        valid = [f for f in files if f.endswith((".xls", ".xlsx", ".csv"))]

        if valid:
            latest = max(
                [os.path.join(folder, f) for f in valid],
                key=os.path.getctime
            )
            return latest

        if time.time() - start > timeout:
            print("❌ Download timeout")
            return None

        time.sleep(2)

# ---------------- DATE ----------------
today = datetime.now()
day = today.day
from_day = "1" if day <= 15 else "16"

print(f"📅 Using From Date: {from_day}")

# ---------------- CHROME SETUP (FINAL FIX) ----------------
options = Options()
options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920,1080")

prefs = {
    "download.default_directory": download_path,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
}
options.add_experimental_option("prefs", prefs)

# ✅ FINAL SAFE CHROME PATH (AUTO DETECT)
chrome_binary = "/usr/bin/chromium"
chromedriver_path = "/usr/bin/chromedriver"

if not os.path.exists(chrome_binary):
    chrome_binary = "/usr/bin/google-chrome"

options.binary_location = chrome_binary

driver = webdriver.Chrome(
    service=Service(chromedriver_path),
    options=options
)

# Enable download in headless
driver.execute_cdp_cmd(
    "Page.setDownloadBehavior",
    {"behavior": "allow", "downloadPath": download_path}
)

driver.set_window_size(1920, 1080)
wait = WebDriverWait(driver, 60)

# ---------------- LOGIN ----------------
driver.get("http://203.92.32.167:8083/iclock/")

wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='text']"))).send_keys(USERNAME)
wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='password']"))).send_keys(PASSWORD)
wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@value='Login']"))).click()

print("✅ Login done")
time.sleep(5)

# ---------------- MENU ----------------
actions = ActionChains(driver)

for item in driver.find_elements(By.XPATH, "//td"):
    if item.text.strip().lower() == "reports":
        actions.move_to_element(item).perform()
        break

time.sleep(2)

for item in driver.find_elements(By.XPATH, "//td"):
    if "log records" in item.text.lower():
        driver.execute_script("arguments[0].click();", item)
        print("📊 Clicked Log Records")
        break

time.sleep(8)

# ---------------- IFRAME ----------------
def switch_to_report_iframe():
    driver.switch_to.default_content()

    for frame in driver.find_elements(By.TAG_NAME, "iframe"):
        driver.switch_to.frame(frame)
        time.sleep(2)

        if "log" in driver.page_source.lower():
            print("✅ Report iframe found")
            return True

        driver.switch_to.default_content()

    return False

if not switch_to_report_iframe():
    print("❌ Initial iframe not found")
    driver.quit()
    exit()

# ---------------- DEVICE FILTER ----------------
for cb in driver.find_elements(By.XPATH, "//input[@type='checkbox']"):
    try:
        if "device" in cb.find_element(By.XPATH, "..").text.lower():
            driver.execute_script("arguments[0].click();", cb)
            print("✅ Device filter enabled")
            break
    except:
        pass

time.sleep(2)

# ---------------- SELECT ----------------
for s in driver.find_elements(By.TAG_NAME, "select"):
    try:
        select = Select(s)
        select.deselect_all()

        for opt in select.options:
            if opt.text.lower().startswith("bhavani"):
                select.select_by_visible_text(opt.text)

        print("✅ Selected Bhavani")
        break
    except:
        pass

time.sleep(2)

# ---------------- DATE SELECT ----------------
for s in driver.find_elements(By.TAG_NAME, "select"):
    values = [o.text.strip() for o in s.find_elements(By.TAG_NAME, "option")]

    if "1" in values and "31" in values:
        for opt in s.find_elements(By.TAG_NAME, "option"):
            if opt.text.strip() == from_day:
                opt.click()

        print(f"📅 From Date set to {from_day}")
        break

time.sleep(2)

# ---------------- GENERATE ----------------
for b in driver.find_elements(By.XPATH, "//input | //button"):
    if "generate" in (b.get_attribute("value") or "").lower():
        driver.execute_script("arguments[0].click();", b)
        print("📊 Report generated")
        break

time.sleep(5)

print("🔄 Refreshing iframe...")

if not switch_to_report_iframe():
    print("❌ Report iframe not found")
    driver.quit()
    exit()

# ---------------- EXPORT ----------------
print("⬇️ Finding Export button...")

for el in driver.find_elements(By.XPATH, "//*[@onclick]"):
    if "export" in (el.get_attribute("onclick") or "").lower():
        driver.execute_script("arguments[0].click();", el)
        print("✅ Export clicked")
        break

time.sleep(5)

# ---------------- CLEAN ----------------
for f in os.listdir(download_path):
    if f.endswith((".xls", ".xlsx", ".csv")):
        try:
            os.remove(os.path.join(download_path, f))
        except:
            pass

print("🧹 Old files cleared")

# ---------------- DOWNLOAD ----------------
latest_file = wait_for_download_complete(download_path)

if not latest_file:
    print("❌ Download failed")
    driver.quit()
    exit()

print("📂 Downloaded:", latest_file)

# ---------------- CONVERT ----------------
month = datetime.now().strftime("%B").lower()
target_name = f"{month}1.csv" if from_day == "1" else f"{month}2.csv"
target_path = os.path.join(download_path, target_name)

if latest_file.endswith((".xls", ".xlsx")):
    df = pd.read_excel(latest_file)
    df.to_csv(target_path, index=False)
    os.remove(latest_file)
    print("✅ Converted")
else:
    target_path = latest_file

# ---------------- UPLOAD ----------------
print("📤 Uploading...")

driver.get(UPLOAD_URL)
time.sleep(3)

try:
    driver.find_element(By.NAME, "pin").send_keys(PIN)
    driver.find_element(By.NAME, "csv_file").send_keys(target_path)
    driver.find_element(By.NAME, "upload").click()

    print("✅ Upload submitted")
    time.sleep(5)

except Exception as e:
    print("❌ Upload error:", str(e))

# ---------------- CLOSE ----------------
driver.quit()
print("🏁 DONE")