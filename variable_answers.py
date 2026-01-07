import json
import os
import difflib

# Data for variable answers

NATIONAL_DATA = {
    'president': ['Donald Trump', 'Trump', 'Donald J. Trump'],
    'vice_president': ['JD Vance', 'Vance', 'J.D. Vance'],
    'speaker_house': ['Mike Johnson', 'Johnson'], 
    'party_president': ['Republican', 'Republican Party'],
    'chief_justice': ['John Roberts', 'Roberts', 'John G. Roberts Jr.'],
    'sc_justices_count': ['9', 'nine', 'nine (9)', '9 (nine)'],
}

def load_state_data():
    if os.path.exists('state_data.json'):
        with open('state_data.json', 'r') as f:
            return json.load(f)
    return {}

STATE_DATA = load_state_data()

def check_answer(variable_type, user_input):
    """
    Checks if the user_input matches the expected answers for the given variable_type.
    Returns True if match, False otherwise.
    """
    if not user_input:
        return False
        
    user_input_clean = user_input.strip().lower()
    
    valid_answers = []
    if variable_type in NATIONAL_DATA:
        valid_answers = NATIONAL_DATA[variable_type]
    elif variable_type in STATE_DATA:
        valid_answers = STATE_DATA[variable_type]
    
    if not valid_answers:
        # If we have a variable type but no data (e.g. representative), 
        # what should we do? 
        # If we return False, it marks it wrong.
        # If we aren't enforcing it yet, maybe we shouldn't have assigned the variable_type to the question yet.
        return False

    for ans in valid_answers:
        ans_clean = ans.lower()
        
        # Exact match or substring
        if ans_clean in user_input_clean:
            return True
            
        # Fuzzy match
        matcher = difflib.SequenceMatcher(None, user_input_clean, ans_clean)
        if matcher.ratio() > 0.85:
            return True
            
    return False
