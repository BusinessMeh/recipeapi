from flask import Flask
import threading
import time
import requests

app = Flask(__name__)

stop_flag = threading.Event()
thread = None

def url_opener():
    while not stop_flag.is_set():
        print("Pinging URL: https://mackrosophta.netlify.app")
        try:
            requests.get("https://mackrosophta.netlify.app", timeout=5)
        except Exception as e:
            print("Error:", e)
        time.sleep(5)
    print("Loop stopped.")

@app.route("/")
def index():
    status = "running" if thread and thread.is_alive() else "stopped"
    return f"Background loop is {status}. Use /start or /stop to control it."

@app.route("/start")
def start_loop():
    global thread
    if thread and thread.is_alive():
        return "Loop is already running."
    stop_flag.clear()
    thread = threading.Thread(target=url_opener, daemon=True)
    thread.start()
    return "Loop started."

@app.route("/stop")
def stop_loop():
    stop_flag.set()
    return "Loop stop requested."

if __name__ == "__main__":
    app.run()
