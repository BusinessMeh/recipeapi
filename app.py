from flask import Flask, jsonify, request
import threading
import time
import os
import subprocess
from datetime import datetime

app = Flask(__name__)

# Store active processes
active_processes = {}

def open_url_continuously(url, interval, process_id):
    while True:
        try:
            # Log the attempt
            print(f"{datetime.now()} - Opening {url}")
            
            # Platform-independent way to open URL
            if os.name == 'nt':  # Windows
                os.startfile(url)
            elif os.name == 'posix':  # macOS/Linux
                subprocess.run(['open', url] if sys.platform == 'darwin' 
                              else ['xdg-open', url])
            
            time.sleep(interval)
            
            # Check if we should stop
            if not active_processes.get(process_id, False):
                break
                
        except Exception as e:
            print(f"Error opening URL: {e}")
            time.sleep(5)  # Wait before retrying

@app.route('/start', methods=['POST'])
def start_opening():
    data = request.json
    url = data.get('url', 'https://mackrosophta.netlify.app')
    interval = data.get('interval', 5)  # seconds
    
    process_id = str(time.time())  # Unique ID for this process
    
    active_processes[process_id] = True
    thread = threading.Thread(target=open_url_continuously, 
                             args=(url, interval, process_id))
    thread.daemon = True
    thread.start()
    
    return jsonify({
        "status": "started",
        "process_id": process_id,
        "url": url,
        "interval": interval
    })

@app.route('/stop', methods=['POST'])
def stop_opening():
    data = request.json
    process_id = data.get('process_id')
    
    if process_id in active_processes:
        active_processes[process_id] = False
        return jsonify({"status": "stopped", "process_id": process_id})
    return jsonify({"status": "not_found"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)