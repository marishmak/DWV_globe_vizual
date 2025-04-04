from flask import Flask, jsonify, request
from threading import Lock
import time
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=["http://localhost:8000"])

# In-memory storage for received data
data_store = []
lock = Lock()

@app.route('/')
def home():
    return "Flask server is running."

@app.route('/favicon.ico')
def favicon():
    return "", 204

@app.route('/receive_data', methods=['POST'])
def receive_data():
    global data_store
    try:
        # Parse incoming JSON data
        data = request.json
        
        # Add timestamp of reception
        data["received_at"] = time.time()
        
        # Store the data
        with lock:
            data_store.append(data)
        
        return jsonify({"status": "success", "message": "Data received"}), 200
    
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

@app.route('/get_data', methods=['GET'])
def get_data():
    # Safely retrieve a copy of the data store
    with lock:
        data_copy = list(data_store)
        
    return jsonify(data_copy), 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5050)