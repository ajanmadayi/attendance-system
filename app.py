from flask import Flask, render_template, Response
import subprocess
import os

app = Flask(__name__)

# 🔥 FORCE BROWSER INSTALL
if not os.path.exists("/opt/render/.cache/ms-playwright"):
    print("⬇️ Installing Playwright browser...", flush=True)
    os.system("python -m playwright install chromium")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/run-script")
def run_script():
    def generate():
        process = subprocess.Popen(
            ["python", "-u", "app113.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )

        for line in process.stdout:
            yield f"data:{line}\n\n"

    return Response(generate(), mimetype="text/event-stream")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)