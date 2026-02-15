import json

def get_save_data():
    with open("save_data.json") as f:
        saved_data = json.load(f)

    return saved_data