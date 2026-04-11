from playwright.sync_api import sync_playwright
import sys
import os

sys.stdout.reconfigure(encoding='utf-8')

USERNAME = "bhavani_khurja"
PASSWORD = "Bhavani@123"

# Ensure temp folder exists (Render safe)
os.makedirs("/tmp", exist_ok=True)

with sync_playwright() as p:
    print("🚀 Launching browser...", flush=True)

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

    page.set_default_timeout(120000)

    print("🌐 Opening Login Page...", flush=True)

    page.goto(
        "http://203.92.32.167:8083/iclock/",
        wait_until="load",
        timeout=120000
    )

    # Take screenshot for debugging
    screenshot_path = "/tmp/login_page.png"
    page.screenshot(path=screenshot_path)
    print(f"📸 Screenshot saved at: {screenshot_path}", flush=True)

    # Wait for login fields
    page.wait_for_selector('input[type="text"]', timeout=60000)
    page.wait_for_selector('input[type="password"]', timeout=60000)

    print("🔐 Entering credentials...", flush=True)

    page.fill('input[type="text"]', USERNAME)
    page.fill('input[type="password"]', PASSWORD)

    page.click('input[value="Login"]')

    print("⏳ Waiting after login...", flush=True)
    page.wait_for_timeout(8000)

    # Check login success
    current_url = page.url
    print(f"🌍 Current URL: {current_url}", flush=True)

    if "login" not in current_url.lower():
        print("✅ LOGIN SUCCESS", flush=True)
    else:
        print("❌ LOGIN FAILED", flush=True)

    browser.close()
    print("🏁 DONE", flush=True)