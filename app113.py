from playwright.sync_api import sync_playwright
import sys
import os

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
            "--disable-setuid-sandbox",
            "--single-process"
        ]
    )

    context = browser.new_context(
        ignore_https_errors=True
    )

    page = context.new_page()

    page.set_default_timeout(120000)

    print("🌐 Opening Login Page...", flush=True)

    try:
        page.goto(
            "http://203.92.32.167:8083/iclock/",
            wait_until="domcontentloaded",
            timeout=120000
        )
    except Exception as e:
        print(f"❌ Page load error: {e}", flush=True)

    # 🔥 Force wait for page content instead of load
    page.wait_for_timeout(5000)

    # 🔥 Debug screenshot
    page.screenshot(path="/tmp/debug.png")
    print("📸 Screenshot saved", flush=True)

    try:
        page.wait_for_selector('input[type="text"]', timeout=60000)
        page.wait_for_selector('input[type="password"]', timeout=60000)

        print("🔐 Entering credentials...", flush=True)

        page.fill('input[type="text"]', USERNAME)
        page.fill('input[type="password"]', PASSWORD)

        page.click('input[value="Login"]')

        page.wait_for_timeout(8000)

        print(f"🌍 Current URL: {page.url}", flush=True)

    except Exception as e:
        print(f"❌ Login error: {e}", flush=True)

    browser.close()
    print("🏁 DONE", flush=True)