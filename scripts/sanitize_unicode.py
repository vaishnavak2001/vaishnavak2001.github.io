import json
import re

def sanitize_string(s):
    if isinstance(s, str):
        # Remove non-ascii characters
        return s.encode('ascii', 'ignore').decode('ascii')
    return s

def sanitize_data(data):
    if isinstance(data, dict):
        return {k: sanitize_data(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [sanitize_data(v) for v in data]
    elif isinstance(data, str):
        return sanitize_string(data)
    else:
        return data

files = ['_data/projects.json', '_data/research_data.json']

for f_path in files:
    try:
        with open(f_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        clean_data = sanitize_data(data)
        
        with open(f_path, 'w', encoding='utf-8') as f:
            json.dump(clean_data, f, indent=2)
            
        print(f"Sanitized {f_path}")
    except Exception as e:
        print(f"Error processing {f_path}: {e}")
