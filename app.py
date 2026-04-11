from flask import Flask, render_template, Response
import subprocess
import os
import sys

app = Flask(__name__)

# UTF-8 logs
sys.stdout.reconfigure(encoding='utf-8')


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/run-script")
def run_script():

    def generate():
        try:
            print("🚀 Starting script...", flush=True)

            process = subprocess.Popen(
                ["python", "-u", "app113.py"],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1
            )

            for line in iter(process.stdout.readline, ''):
                yield f"data: {line.strip()}\n\n"

            process.stdout.close()
            process.wait()

            yield "data: 🏁 DONE\n\n"

        except Exception as e:
            yield f"data: ❌ Error: {str(e)}\n\n"

    return Response(generate(), mimetype="text/event-stream")


@app.route("/health")
def health():
    return "OK", 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)