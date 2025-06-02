from flask import Flask, request, jsonify
from flask_cors import CORS 
import webbrowser
import threading
import time

app = Flask(__name__)
CORS(app, origins=["https://multirecipee.shop"])

# Global variable to control the loop
running = False
loop_thread = None

def open_url_in_loop(url="https://example.com", interval=5):
    global running
    while running:
        try:
            # Open URL in default browser
            webbrowser.open_new(url)
            time.sleep(interval)
        except Exception as e:
            print(f"Error: {e}")
            break

@app.route('/start', methods=['POST'])
def start_process():
    global running, loop_thread
    
    if not running:
        running = True
        loop_thread = threading.Thread(target=open_url_in_loop)
        loop_thread.start()
        return jsonify({"status": "started", "message": "Process started"})
    else:
        return jsonify({"status": "already_running", "message": "Process is already running"})

@app.route('/stop', methods=['GET'])
def stop_process():
    global running, loop_thread
    
    if running:
        running = False
        if loop_thread:
            loop_thread.join()
        return jsonify({"status": "stopped", "message": "Process stopped"})
    else:
        return jsonify({"status": "not_running", "message": "No process is currently running"})

@app.route('/status', methods=['GET'])
def status():
    global running
    return jsonify({"status": "running" if running else "stopped"})

if __name__ == '__main__':
    app.run(debug=True)