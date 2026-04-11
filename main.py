from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return """
    <html>
    <head>
        <title>Attendance System</title>
        <script>
            function openAndLogin() {
                var win = window.open("http://203.92.32.167:8083/iclock/", "_blank");

                setTimeout(function() {
                    try {
                        win.document.querySelector("input[type='text']").value = "bhavani_khurja";
                        win.document.querySelector("input[type='password']").value = "Bhavani@123";

                        // OPTIONAL AUTO CLICK LOGIN
                        var btn = win.document.querySelector("input[type='submit'], button");
                        if (btn) btn.click();

                    } catch (e) {
                        alert("Auto login blocked by browser security. Please login manually.");
                    }
                }, 3000);
            }
        </script>

        <style>
            body { text-align:center; font-family: Arial; margin-top:100px; }
            button {
                padding:15px 25px;
                background:green;
                color:white;
                font-size:18px;
                border:none;
                border-radius:5px;
                cursor:pointer;
            }
        </style>
    </head>
    <body>

        <h2>Open Attendance System</h2>

        <button onclick="openAndLogin()">
            Open & Auto Login
        </button>

    </body>
    </html>
    """
