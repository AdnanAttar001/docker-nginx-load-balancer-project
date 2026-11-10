from flask import Flask, jsonify
import socket
import os
from datetime import datetime

app = Flask(__name__)

SERVER_NAME = socket.gethostname()
APP_VERSION = os.getenv("APP_VERSION", "1.0")

@app.route("/")
def home():

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Docker Nginx Project</title>

        <style>
            body {{
                font-family: Arial;
                background: #101827;
                color: white;
                text-align: center;
                padding-top: 100px;
            }}

            .container {{
                background: #1e293b;
                padding: 40px;
                margin: auto;
                width: 60%;
                border-radius: 15px;
            }}

            h1 {{
                color: #38bdf8;
            }}
        </style>

    </head>

    <body>

        <div class="container">

            <h1>Docker Two-Tier Application</h1>

            <h2>Welcome to Nginx Load Balancing</h2>

            <p>Application Server: {SERVER_NAME}</p>

            <p>Application Version: {APP_VERSION}</p>

            <p>Time: {datetime.now()}</p>

            <p>Backend Status: Running</p>

        </div>

    </body>
    </html>
    """

@app.route("/health")
def health():

    return jsonify({
        "status": "healthy",
        "server": SERVER_NAME
    }), 200


@app.route("/api/info")
def info():

    return jsonify({
        "application": "Docker Two-Tier Application",
        "server": SERVER_NAME,
        "version": APP_VERSION,
        "timestamp": datetime.now().isoformat()
    })


if __name__ == "__main__":

    app.run(host="0.0.0.0", port=5000)
