import json
import os

def get_save_data():
    with open("save_data.json", "r") as f:
        saved_data = json.load(f)

    return saved_data

def update_save_data(score_obj, current_difficulty):
    # Make copy of current save data to write to 
    new_save_data = get_save_data()

    # Update values in the new_save_data string
    new_save_data["difficulties"][f"{current_difficulty.name}".lower()]["best_score"] = score_obj.difficulties[current_difficulty].best_score
    new_save_data["difficulties"][f"{current_difficulty.name}".lower()]["total_score"] = score_obj.difficulties[current_difficulty].total_score
    new_save_data["difficulties"][f"{current_difficulty.name}".lower()]["games_played"] = score_obj.difficulties[current_difficulty].games_played
    
    overwrite_main_save(score_obj, new_save_data)

def load_save_data(score_obj, difficulty_levels):
    saved_data = get_save_data()

    for difficulty in difficulty_levels:
        score_obj.difficulties[difficulty].best_score = saved_data["difficulties"][f"{difficulty.name}".lower()]["best_score"]   
        score_obj.difficulties[difficulty].total_score = saved_data["difficulties"][f"{difficulty.name}".lower()]["total_score"]   
        score_obj.difficulties[difficulty].games_played = saved_data["difficulties"][f"{difficulty.name}".lower()]["games_played"]

def reset_save_data(score_obj):
    with open("save_data_reset.json", "r")as f:
        new_save_data = json.load(f)

    overwrite_main_save(score_obj, new_save_data)

def reset_single_difficulty_scores(score_obj, current_difficulty):
    new_save_data = get_save_data()
    with open("save_data_reset.json", "r") as f:
        reset_data = json.load(f)

    # Assign reset values from save_data_reset.json to new_save_data
    new_save_data["difficulties"][current_difficulty]["best_score"] = reset_data["difficulties"][current_difficulty]["best_score"]
    new_save_data["difficulties"][current_difficulty]["total_score"] = reset_data["difficulties"][current_difficulty]["total_score"]
    new_save_data["difficulties"][current_difficulty]["games_played"] = reset_data["difficulties"][current_difficulty]["games_played"]

    overwrite_main_save(score_obj, new_save_data)

def overwrite_main_save(score_obj, new_save_data):
    # Write the string to a temp_save_data file which will be created as it does not exist yet
    with open("temp_save_data.json", "w") as f:
        json.dump(new_save_data, f, indent = 2)

    # Replace the main save_data with temp_save_data
    # Note: It works by renaming temp_save_data to save_data, removing existing file of the same name
    os.replace("temp_save_data.json", "save_data.json")

    load_save_data(score_obj, score_obj.difficulties.keys())