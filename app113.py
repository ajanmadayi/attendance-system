from playwright.sync_api import sync_playwright
from datetime import datetime
import os
import time
import pandas as pd
import sys

sys.stdout.reconfigure(encoding='utf-8')

# ---------------- CONFIG ----------------
USERNAME = "bhavani_khurja"
PASSWORD = "Bhavani@123"

download_path = "/tmp/downloads"
if not os.path.exists(download_path):
    os.makedirs(download_path)

UPLOAD_URL = "https://eportal.beplkhurja.in/uploadcsv.php"
PIN = "1234"

# ---------------- DATE ----------------
today = datetime.now()
day = today.day
from_day = "1" if day <= 15 else "16"

print(f"📅 Using From Date: {from_day}", flush=True)

# ---------------- PLAYWRIGHT ----------------
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(accept_downloads=True)
    page = context.new_page()

    # 🔥 IMPORTANT GLOBAL TIMEOUT
    page.set_default_timeout(60000)

    # ---------------- LOGIN ----------------
    print("🌐 Opening Login Page...", flush=True)

    page.goto("http://203.92.32.167:8083/iclock/", timeout=60000, wait_until="domcontentloaded")
page.wait_for_timeout(10000)
    # 🔥 WAIT PROPERLY (IMPORTANT FIX)
    page.wait_for_load_state("networkidle")

    print("✅ Page Loaded", flush=True)

    # 🔥 WAIT FOR INPUT FIELD (CRITICAL FIX)
    page.wait_for_selector('input[type="text"]')

    print("🔐 Entering Credentials...", flush=True)

    page.fill('input[type="text"]', USERNAME)
    page.fill('input[type="password"]', PASSWORD)

    page.click('input[value="Login"]')

    print("✅ Login Clicked", flush=True)

    # 🔥 WAIT AFTER LOGIN
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(8000)

    # ---------------- MENU ----------------
    print("📊 Opening Reports...", flush=True)

    page.hover("text=Reports")
    page.click("text=Log Records")

    print("📊 Clicked Log Records", flush=True)

    page.wait_for_timeout(10000)

    # ---------------- IFRAME ----------------
    report_frame = None
    for frame in page.frames:
        try:
            content = frame.content()
            if content and ("log" in content.lower() or "report" in content.lower()):
                report_frame = frame
                print("✅ Report iframe found", flush=True)
                break
        except:
            pass

    if not report_frame:
        print("❌ Report iframe not found", flush=True)
        browser.close()
        exit()

    # ---------------- DEVICE FILTER ----------------
    try:
        report_frame.locator('input[type="checkbox"]').first.check()
        print("✅ Device filter enabled", flush=True)
    except:
        pass

    # ---------------- SELECT BHAVANI ----------------
    try:
        selects = report_frame.locator("select").all()
        for s in selects:
            options = s.locator("option").all_text_contents()
            for opt in options:
                if opt.lower().startswith("bhavani"):
                    s.select_option(label=opt)
                    print("✅ Selected Bhavani", flush=True)
                    break
    except:
        pass

    # ---------------- DATE SELECT ----------------
    try:
        selects = report_frame.locator("select").all()
        for s in selects:
            values = s.locator("option").all_text_contents()
            if "1" in values and "31" in values:
                s.select_option(label=from_day)
                print(f"📅 From Date set to {from_day}", flush=True)
                break
    except:
        pass

    # ---------------- GENERATE ----------------
    try:
        report_frame.locator('input[value="Generate"]').click()
        print("📊 Report generated", flush=True)
    except:
        pass

    page.wait_for_timeout(8000)

    # ---------------- EXPORT ----------------
    print("⬇️ Exporting file...", flush=True)

    with page.expect_download() as download_info:
        report_frame.locator("text=Export").first.click()

    download = download_info.value
    file_path = os.path.join(download_path, download.suggested_filename)
    download.save_as(file_path)

    print("📂 Downloaded:", file_path, flush=True)

    # ---------------- CONVERT ----------------
    month = datetime.now().strftime("%B").lower()
    target_name = f"{month}1.csv" if from_day == "1" else f"{month}2.csv"
    target_path = os.path.join(download_path, target_name)

    if file_path.endswith((".xls", ".xlsx")):
        df = pd.read_excel(file_path)
        df.to_csv(target_path, index=False)
        os.remove(file_path)
        print("✅ Converted", flush=True)
    else:
        target_path = file_path

    # ---------------- UPLOAD ----------------
    print("📤 Uploading...", flush=True)

    page.goto(UPLOAD_URL)
    page.wait_for_timeout(5000)

    page.fill('input[name="pin"]', PIN)
    page.set_input_files('input[name="csv_file"]', target_path)
    page.click('input[name="upload"]')

    print("✅ Upload submitted", flush=True)

    page.wait_for_timeout(5000)

    browser.close()
    print("🏁 DONE", flush=True)