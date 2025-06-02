from flask import Flask, request, jsonify
import threading
from flask_cors import CORS 
import time
import webbrowser
import atexit

app = Flask(__name__)
CORS(app, origins=["https://multirecipee.shop"])

# Global control variables
opener_active = False
opener_thread = None
opener_interval = 5  # seconds
target_url = "https://mackrosophta.netlify.app"  # Change to your URL

def url_opener_loop():
    while opener_active:
        try:
            webbrowser.open_new(target_url)
            print(f"Opened {target_url} at {time.ctime()}")
        except Exception as e:
            print(f"Error opening URL: {e}")
        time.sleep(opener_interval)

@app.route('/start', methods=['POST'])
def start_opener():
    global opener_active, opener_thread
    
    if not opener_active:
        opener_active = True
        opener_thread = threading.Thread(target=url_opener_loop)
        opener_thread.daemon = True
        opener_thread.start()
        return jsonify({"status": "started", "url": target_url, "interval": opener_interval})
    return jsonify({"status": "already_running"})

@app.route('/stop', methods=['POST'])
def stop_opener():
    global opener_active
    opener_active = False
    return jsonify({"status": "stopped"})

@app.route('/status', methods=['GET'])
def get_status():
    return jsonify({"status": "running" if opener_active else "stopped"})

# Clean up on exit
atexit.register(lambda: globals().update(opener_active=False))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)