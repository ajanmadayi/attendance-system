from flask import Flask, render_template, Response
import subprocess

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/run-script")
def run_script():
    def generate():
        process = subprocess.Popen(
            ["python", "-u", "app113.py"],  # 🔥 KEY FIX
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8",
            errors="ignore"
        )

        for line in process.stdout:
            yield f"data:{line}\n\n"

    return Response(generate(), mimetype="text/event-stream")

if __name__ == "__main__":
    app.run(debug=True)