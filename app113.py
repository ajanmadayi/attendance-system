from playwright.sync_api import sync_playwright
import sys

sys.stdout.reconfigure(encoding='utf-8')

USERNAME = "bhavani_khurja"
PASSWORD = "Bhavani@123"

with sync_playwright() as p:
    print("🚀 Launching browser...", flush=True)

    browser = p.chromium.launch(
        headless=True,
        args=[
            "--no-sandbox",
            "--disable-dev-shm-usage",
            "--disable-gpu",
            "--disable-setuid-sandbox"
        ]
    )

    page = browser.new_page()

    print("🌐 Opening Login Page...", flush=True)
    page.goto("http://203.92.32.167:8083/iclock/", timeout=120000)

    print("🔐 Entering credentials...", flush=True)

    page.fill('input[type="text"]', USERNAME)
    page.fill('input[type="password"]', PASSWORD)

    page.click('input[value="Login"]')

    page.wait_for_timeout(8000)

    print("🏁 DONE", flush=True)

    browser.close()