from flask import Flask
import threading
import time
import requests

app = Flask(__name__)
stop_flag = False

def url_opener():
    global stop_flag
    while not stop_flag:
        try:
            print("Pinging URL...")
            requests.get("https://mackrosophta.netlify.app", timeout=5)
        except Exception as e:
            print(f"Error pinging URL: {e}")
        time.sleep(5)

@app.route("/")
def index():
    return "URL pinger is running. Visit /stop to stop."

@app.route("/stop")
def stop():
    global stop_flag
    stop_flag = True
    return "Stopping URL pinger."

# Start the thread when the app starts
@app.before_first_request
def activate_job():
    thread = threading.Thread(target=url_opener)
    thread.daemon = True
    thread.start()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
