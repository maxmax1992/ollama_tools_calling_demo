import json
import os

def add_to_json_file(python_object):
    try:
        if not os.path.exists("issues.json"):
            with open("issues.json", "w") as f:
                json.dump([], f)
        with open("issues.json", "r") as f:
            issues = json.load(f)
        issues.append(python_object)
        with open("issues.json", "w") as f:
            json.dump(issues, f, indent=2)  # Added indent for better readability
    except Exception as e:
        print(f"Error handling JSON file: {e}")
        raise

def clean_json_file():
    """Clean up the issues.json file by removing all entries"""
    with open("issues.json", "w") as f:
        json.dump([], f) 