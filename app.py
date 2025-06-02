from flask import Flask, request, jsonify
import threading
import webbrowser
import time

app = Flask(__name__)

# Global variable to control the loop
running = False
loop_thread = None

def open_url_in_loop(url="https://mackrosophta.netlify.app", interval=5):
    global running
    while running:
        webbrowser.open_new_tab(url)
        time.sleep(interval)

@app.route('/start', methods=['POST'])
def start():
    global running, loop_thread
    
    if not running:
        running = True
        loop_thread = threading.Thread(target=open_url_in_loop)
        loop_thread.start()
        return jsonify({"status": "started", "message": "URL loop started"})
    else:
        return jsonify({"status": "already_running", "message": "URL loop is already running"})

@app.route('/stop')
def stop():
    global running, loop_thread
    
    if running:
        running = False
        if loop_thread:
            loop_thread.join()
        return jsonify({"status": "stopped", "message": "URL loop stopped"})
    else:
        return jsonify({"status": "not_running", "message": "URL loop is not running"})

@app.route('/status')
def status():
    global running
    return jsonify({"status": "running" if running else "stopped"})

if __name__ == '__main__':
    app.run(debug=True)