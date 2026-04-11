from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return """
    <h2 style='text-align:center;margin-top:100px;'>Open Attendance System</h2>
    <div style='text-align:center;'>
        <a href="http://203.92.32.167:8083/iclock/" target="_blank"
           style="padding:15px 25px;background:green;color:white;
                  text-decoration:none;font-size:18px;border-radius:5px;">
            Open System
        </a>
    </div>
    """

# 🔥 THIS LINE IS IMPORTANT FOR GUNICORN
application = app