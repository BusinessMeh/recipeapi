from flask import Flask
import threading
import time
import webbrowser
import os

app = Flask(__name__)
stop_flag = False

def url_opener():
    global stop_flag
    while True:
        if os.path.exists("stop.txt"):
            with open("stop.txt", "r") as f:
                content = f.read().strip().lower()
                if content == "stop":
                    print("Stop signal received. Exiting thread.")
                    break

        webbrowser.open("https://mackrosophta.netlify.app")
        time.sleep(5)

@app.route("/")
def index():
    return "URL opener is running in background. To stop, write 'stop' in stop.txt."

if __name__ == "__main__":
    threading.Thread(target=url_opener).start()
    app.run(debug=True)
