import json
import os
from datetime import datetime

PROGRESS_FILE = "study_progress.json"

def load_progress(username):
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, "r") as f:
            all_progress = json.load(f)
            return all_progress.get(username, {})
    return {}

def save_progress(username, progress):
    all_progress = {}
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, "r") as f:
            all_progress = json.load(f)
    all_progress[username] = progress
    with open(PROGRESS_FILE, "w") as f:
        json.dump(all_progress, f, indent=2)

def add_topic(username, topic, status="Studying"):
    progress = load_progress(username)
    if topic not in progress:
        progress[topic] = {
            "status": status,
            "date_added": datetime.now().strftime("%d %b %Y"),
            "date_updated": datetime.now().strftime("%d %b %Y"),
            "notes": ""
        }
        save_progress(username, progress)
        return True, "✅ Topic added!"
    return False, "⚠️ Topic already exists!"

def update_topic_status(username, topic, status):
    progress = load_progress(username)
    if topic in progress:
        progress[topic]["status"] = status
        progress[topic]["date_updated"] = datetime.now().strftime("%d %b %Y")
        save_progress(username, progress)
        return True
    return False

def delete_topic(username, topic):
    progress = load_progress(username)
    if topic in progress:
        del progress[topic]
        save_progress(username, progress)
        return True
    return False

def get_stats(progress):
    total = len(progress)
    if total == 0:
        return 0, 0, 0, 0
    studying = sum(1 for t in progress.values() if t["status"] == "Studying")
    completed = sum(1 for t in progress.values() if t["status"] == "Completed")
    mastered = sum(1 for t in progress.values() if t["status"] == "Mastered")
    return total, studying, completed, mastered