import json
from datetime import datetime

def save_score(choice, score, total_questions, percentage):
    entry = {
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "practiced": choice,
        "score": score,
        "total": total_questions,
        "percentage": percentage
    }
    
    try:
        with open("progress.json", "r") as f:
            history = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        history = []
    
    history.append(entry)
    
    with open("progress.json", "w") as f:
        json.dump(history, f, indent=4)
        
def show_history():
    try:
        with open("progress.json", "r") as f:
            history = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        print("No past scores. Let's get it started!")
        return

    if not history:
        return
    else:
        recent = history[-5:]
        print("--- Recent Sessions ---")
        for entry in recent:
            print(f"{entry['date']} | {entry['practiced']} | {entry['score']}/{entry['total']} | ({entry['percentage']}%)\n")