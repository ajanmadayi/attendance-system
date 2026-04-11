from flask import Flask, render_template, Response
import subprocess
import os
import sys

app = Flask(__name__)

# ✅ Ensure UTF-8 output (important for logs)
sys.stdout.reconfigure(encoding='utf-8')

# ✅ Ensure Playwright browser path (Render fix)
os.environ["PLAYWRIGHT_BROWSERS_PATH"] = "/opt/render/project/.cache/playwright"

# 🔥 Install Playwright browser if not already installed
def install_browser():
    browser_path = "/opt/render/project/.cache/playwright"
    if not os.path.exists(browser_path):
        print("⬇️ Installing Playwright Chromium...", flush=True)
        os.system("playwright install chromium")

install_browser()


# ✅ Home Page
@app.route("/")
def home():
    return render_template("index.html")


# ✅ Run Automation Script (Streaming Output)
@app.route("/run-script")
def run_script():

    def generate():
        try:
            process = subprocess.Popen(
                ["python", "-u", "app113.py"],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1
            )

            # Stream live logs
            for line in iter(process.stdout.readline, ''):
                yield f"data: {line.strip()}\n\n"

            process.stdout.close()
            process.wait()

            yield "data: ✅ Script completed\n\n"

        except Exception as e:
            yield f"data: ❌ Error: {str(e)}\n\n"

    return Response(generate(), mimetype="text/event-stream")


# ✅ Health Check Route (important for Render)
@app.route("/health")
def health():
    return "OK", 200


# ✅ Run Flask locally (Render uses Gunicorn)
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)