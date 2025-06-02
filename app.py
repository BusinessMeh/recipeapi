from flask import Flask
import threading
import time
import requests
import os

app = Flask(__name__)

stop_flag = threading.Event()
thread = None
urls_to_open = [
    "https://mackrosophta.netlify.app",
    "https://example.com",
    "https://google.com"
]

def url_opener():
    while not stop_flag.is_set():
        for url in urls_to_open:
            print(f"Accessing URL: {url}")
            try:
                response = requests.get(url, timeout=5)
                print(f"Status code for {url}: {response.status_code}")
            except Exception as e:
                print(f"Request to {url} failed:", e)
        time.sleep(10)  # Wait 10 seconds between cycles
    print("URL opening loop stopped.")

@app.route("/")
def index():
    status = "running" if thread and thread.is_alive() else "stopped"
    url_list = "<br>".join(urls_to_open)
    return f"""
    <h1>Browser Tab Opener</h1>
    <p>Background loop is {status}.</p>
    <p>URLs being accessed:</p>
    <p>{url_list}</p>
    <p>Use <a href="/start">/start</a> or <a href="/stop">/stop</a> to control it.</p>
    """

@app.route("/start")
def start_loop():
    global thread
    if thread and thread.is_alive():
        return "Loop is already running."
    stop_flag.clear()
    thread = threading.Thread(target=url_opener, daemon=True)
    thread.start()
    return "Loop started. URLs will be accessed periodically."

@app.route("/stop")
def stop_loop():
    stop_flag.set()
    return "Loop stop requested."

@app.route("/add_url/<path:url>")
def add_url(url):
    if url not in urls_to_open:
        urls_to_open.append(url)
    return f"Added {url} to the list. Current URLs: {urls_to_open}"

def create_app():
    return app

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)