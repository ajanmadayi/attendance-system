from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return """
    <html>
    <head>
        <title>Attendance System</title>
        <style>
            body { text-align:center; font-family: Arial; margin-top:100px; }
            a {
                padding:15px 25px;
                background:green;
                color:white;
                text-decoration:none;
                font-size:18px;
                border-radius:5px;
            }
        </style>
    </head>
    <body>

        <h2>Open Attendance System</h2>

        <a href="http://203.92.32.167:8083/iclock/" target="_blank">
            Open System
        </a>

    </body>
    </html>
    """

if __name__ == "__main__":
    app.run(debug=True)