from playwright.sync_api import sync_playwright
import time

print("📅 Using From Date: 1", flush=True)

try:
    print("🚀 Launching browser...", flush=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=[
                "--no-sandbox",
                "--disable-dev-shm-usage"
            ]
        )

        page = browser.new_page()

        print("🌐 Opening Login Page...", flush=True)
        page.goto("http://203.92.32.167:8083/iclock/", timeout=60000)

        print("🔐 Entering credentials...", flush=True)
        page.fill('input[name="username"]', "admin")
        page.fill('input[name="password"]', "admin")
        page.click('button[type="submit"]')

        page.wait_for_timeout(5000)
        print("✅ Login done", flush=True)

        browser.close()

except Exception as e:
    print(f"❌ ERROR: {e}", flush=True)

print("🏁 DONE", flush=True)