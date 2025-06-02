from flask import Flask
import threading
import time

app = Flask(__name__)

stop_flag = threading.Event()

def url_opener():
    while not stop_flag.is_set():
        print("Pretending to open URL: https://mackrosophta.netlify.app")
        time.sleep(5)
    print("Background thread stopped.")

@app.route("/")
def index():
    return "URL opener is running. Visit /stop to stop it."

@app.route("/stop")
def stop():
    stop_flag.set()
    return "URL opener has been stopped."

if __name__ == "__main__":
    threading.Thread(target=url_opener, daemon=True).start()
    app.run()
