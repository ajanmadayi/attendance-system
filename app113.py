from playwright.sync_api import sync_playwright

print("🚀 Testing browser...", flush=True)

try:
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-dev-shm-usage"]
        )

        page = browser.new_page()

        page.goto("https://example.com")
        print("✅ Browser working!", flush=True)

        browser.close()

except Exception as e:
    print("❌ ERROR:", e, flush=True)