from playwright.sync_api import sync_playwright
import time
import os

print("📅 Using From Date: 1", flush=True)

try:
    print("🚀 Launching browser...", flush=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=[
                "--no-sandbox",
                "--disable-dev-shm-usage",
                "--disable-gpu",
                "--single-process"
            ]
        )

        context = browser.new_context()
        page = context.new_page()

        # 🔥 OPEN LOGIN PAGE
        print("🌐 Opening Login Page...", flush=True)
        page.goto("http://203.92.32.167:8083/iclock/", timeout=60000)

        # 🔐 LOGIN
        print("🔐 Entering credentials...", flush=True)
        page.fill('input[name="username"]', "admin")
        page.fill('input[name="password"]', "admin")  # change if needed
        page.click('button[type="submit"]')

        page.wait_for_timeout(5000)

        print("✅ Login done", flush=True)

        # 📊 CLICK LOG RECORDS
        page.click("text=Log Records")
        print("📊 Clicked Log Records", flush=True)

        page.wait_for_timeout(5000)

        # 🔍 SWITCH TO IFRAME (IMPORTANT)
        iframe = page.frame_locator("iframe")

        print("✅ Report iframe found", flush=True)

        # 🔧 DEVICE FILTER
        iframe.locator('input[placeholder="Search"]').fill("Bhavani")
        iframe.locator("text=Bhavani").click()

        print("✅ Device filter enabled", flush=True)

        # 📅 SET DATE
        iframe.locator('input[name="from_date"]').fill("1")

        print("📅 From Date set to 1", flush=True)

        # 📊 GENERATE REPORT
        iframe.locator("text=Search").click()

        print("📊 Report generated", flush=True)

        page.wait_for_timeout(5000)

        # 🔄 REFRESH IFRAME
        iframe = page.frame_locator("iframe")
        print("🔄 Refreshing iframe...", flush=True)

        # ⬇️ EXPORT
        print("⬇️ Finding Export button...", flush=True)
        iframe.locator("text=Export").click()

        page.wait_for_timeout(2000)

        iframe.locator("text=Excel").click()

        print("⬇️ Selecting Excel...", flush=True)

        print("⏳ Waiting for download...", flush=True)
        time.sleep(5)

        print("📂 Download completed", flush=True)

        browser.close()

except Exception as e:
    print(f"❌ ERROR: {e}", flush=True)

print("🏁 DONE", flush=True)