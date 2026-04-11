from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

print("🚀 Testing Gmail...", flush=True)

try:
    options = Options()
    options.binary_location = "/usr/bin/chromium"

    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)

    print("🌐 Opening Gmail...", flush=True)
    driver.get("http://203.92.32.167:8083/iclock/")

    time.sleep(5)

    print("✅ Gmail opened successfully", flush=True)

    driver.quit()

except Exception as e:
    print(f"❌ ERROR: {e}", flush=True)

print("🏁 DONE", flush=True)