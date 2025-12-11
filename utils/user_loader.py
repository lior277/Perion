import json
import os

def load_users():
    path = os.path.join("data", "users.json")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
