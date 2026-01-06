import os
import json
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
DATA_FILE = 'user_progress.json'

def load_progress():
    if not os.path.exists(DATA_FILE):
        return {"lastIdx": 0, "stats": {}}
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except Exception:
        return {"lastIdx": 0, "stats": {}}

def save_progress_to_file(data):
    # merge with existing to avoid overwriting if partial update? 
    # For simplicity, we assume frontend sends complete state or we merge here.
    # Actually, let's just save what we get if it's the full object, or merge.
    # To be safe and simple: let's read, merge, write.
    current = load_progress()
    
    # Update fields provided
    if 'lastIdx' in data:
        current['lastIdx'] = data['lastIdx']
    if 'stats' in data:
        # We might want to merge stats deeply, but for now let's assume the frontend 
        # is sending the specific update for a question or the whole thing. 
        # But wait, the frontend has the state in memory. 
        # Let's design the API to receive the delta or the full object.
        # Sending full object is easiest for now for a local app.
        current['stats'] = data.get('stats', current['stats'])

    with open(DATA_FILE, 'w') as f:
        json.dump(current, f, indent=2)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/progress', methods=['GET'])
def get_progress():
    return jsonify(load_progress())

@app.route('/api/progress', methods=['POST'])
def update_progress():
    data = request.json
    save_progress_to_file(data)
    return jsonify({"status": "success"})

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5101, debug=True)
