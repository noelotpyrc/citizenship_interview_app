import os
import json
import difflib
import variable_answers
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
DATA_FILE = 'user_progress.json'
QUESTIONS_FILE = 'questions.json'

# Load Questions
questions = []
if os.path.exists(QUESTIONS_FILE):
    with open(QUESTIONS_FILE, 'r') as f:
        questions = json.load(f)

def load_progress():
    if not os.path.exists(DATA_FILE):
        return {"lastIdx": 0, "stats": {}}
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except Exception:
        return {"lastIdx": 0, "stats": {}}

def save_progress_to_file(data):
    current = load_progress()
    if 'lastIdx' in data:
        current['lastIdx'] = data['lastIdx']
    if 'stats' in data:
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

@app.route('/api/check_answer', methods=['POST'])
def check_answer():
    data = request.json
    idx = data.get('index')
    user_val = data.get('answer', '').strip().lower()
    
    if idx is None or idx < 0 or idx >= len(questions):
        return jsonify({"correct": False, "error": "Invalid question index"})

    q_data = questions[idx]
    
    # Check for variable answer type first
    variable_type = q_data.get('variable_type')
    if variable_type:
        is_correct = variable_answers.check_answer(variable_type, user_val)
        return jsonify({"correct": is_correct})
        
    keywords = q_data.get('k', [])
    
    is_correct = False
    
    # Check each keyword
    for k in keywords:
        matcher = difflib.SequenceMatcher(None, user_val, k)
        # 1. High ratio match (for typos)
        if matcher.ratio() > 0.85:
            is_correct = True
            break
            
        # 2. Substring match (if keyword is inside user answer, even with slight typo?)
        # difflib doesn't do fuzzy inclusion easily.
        # But if the user typed "I believe he saved the uniton", we want "saved the union" to match.
        # Let's trust user inputs are usually direct.
        # If not, let's look for substring.
        if k in user_val:
            is_correct = True
            break
            
        # 3. Longest common substring check
        # If the longest block is significant part of keyword (e.g. 90% of key)?
        match = matcher.find_longest_match(0, len(user_val), 0, len(k))
        if match.size >= len(k) * 0.9: # 90% of characters match contiguously
            is_correct = True
            break
            
    return jsonify({"correct": is_correct})

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5101, debug=True)
