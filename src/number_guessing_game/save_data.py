from __future__ import annotations
from typing import TYPE_CHECKING, Any
import json
import os
import copy

# Avoid circular dependencies while maintaining autocomplete/type hint features
if TYPE_CHECKING:
    from number_guessing_game.score import DifficultyLevel, Score

# Not ideal but fine for this project, if large store somewhere else
DEFAULT_SAVE_DATA = {
  "difficulties": {
    "easy": {
      "best_score": 0,
      "total_score": 0,
      "games_played": 0
    },
    "medium": {
      "best_score": 0,
      "total_score": 0,
      "games_played": 0
    },
    "hard": {
      "best_score": 0,
      "total_score": 0,
      "games_played": 0
    }
  }
}

USER_SAVE_PATH = "data\save_data.json"

def get_save_data() -> dict:
    # Make sure the file exists
    if not os.path.exists(USER_SAVE_PATH):
        # If no file exists, create one using DEFAULT_SAVE_DATA
        overwrite_save_data(DEFAULT_SAVE_DATA)
        print("WARNING: save_data.json not found. File recreated with all data being reset.")
        return copy.deepcopy(DEFAULT_SAVE_DATA)

    # Make sure the file is not corrupted in any way
    try:
        # If not corrupted, open it and store its contents
        with open(USER_SAVE_PATH, "r") as f:
            save_data = json.load(f)
        # Verify the integrity of the save file
        # Passing reference not copy as deepcopy is only called in validate_file_keys() when a key is actually missing
        need_to_overwrite = [delete_unwanted_keys(save_data, DEFAULT_SAVE_DATA), 
                             validate_file_keys(save_data, DEFAULT_SAVE_DATA)]
        if any(need_to_overwrite):
            print("WARNING: Key(s) missing or added in save_data.json, some scores may have been reset.")
            overwrite_save_data(save_data)
        return save_data
    except (json.JSONDecodeError, OSError):
        # If corrupted, overwrite file with DEFAULT_SAVE_DATA
        overwrite_save_data(DEFAULT_SAVE_DATA)
        print("WARNING: save_data.json was corrupted. File recreated with all data being reset.")
        return copy.deepcopy(DEFAULT_SAVE_DATA)   
    
def difficulty_path(save_data: dict, difficulty: DifficultyLevel) -> dict[str, Any]:
    return save_data["difficulties"][str(difficulty.name).lower()]

def update_save_data(score_obj: Score, difficulty: DifficultyLevel) -> None:
    # Create shortcut for current difficulty in json file
    new_save_data = get_save_data()
    difficulty_data = difficulty_path(new_save_data, difficulty)

    for key in difficulty_data:
        difficulty_data[key] = getattr(score_obj.difficulties[difficulty], key)

    overwrite_save_data(new_save_data)

def load_save_data(score_obj: Score) -> None:
    save_data = get_save_data()  

    for difficulty in score_obj.difficulties.keys():
        difficulty_data = difficulty_path(save_data, difficulty)
        for key in difficulty_data:
            setattr(score_obj.difficulties[difficulty], key, difficulty_data[key])

def reset_single_difficulty(difficulty: DifficultyLevel) -> None:
    new_save_data = get_save_data()
    difficulty_data = difficulty_path(new_save_data, difficulty)
    difficulty_data.clear()
    difficulty_data.update(copy.deepcopy(DEFAULT_SAVE_DATA["difficulties"][str(difficulty.name).lower()]))

    overwrite_save_data(new_save_data)

def overwrite_save_data(new_save_data: dict = DEFAULT_SAVE_DATA) -> None:
    # Write the string to a temp_save_data file which will be created as it does not exist yet
    with open("data\\temp_save_data.json", "w") as f:
        json.dump(new_save_data, f, indent = 2)

    # Replace the main save_data with temp_save_data
    # os.replace() works by renaming temp_save_data to save_data, overwriting any existing file of the same name
    # os.rename() can't be used as operation will raise a FileExistsError if file of new name already exists
    # os.replace() is the opposite and will raise an OSError if file of new name doesn't exist
    os.replace("data\\temp_save_data.json", USER_SAVE_PATH)

    # For future reference the above programming technique is called atomic file writing
    # It's to prevent file corruption in events such as a power failure
    # Basic concept is main file is only updated AFTER all data has been updated/file has been written.
    # For example write new data to a temporary file so main data remains untouched.
    # Then once new data has been written, rename file to overwrite main file (this is the atomic operation)

# Ensures all the required keys are present in the save file, uses node-left-right traversal
def validate_file_keys(save_data: dict, default_data: dict, parent_key: str = None) -> bool:
    key_restored = False
    # Use/get the DEFAULT_SAVE_DATA to check if keys exist in main save file
    for key, value in default_data.items():
        if key not in save_data:
            # Check to see if the key belongs to a difficulty dictionary
            # If it does then reset all scores for that difficulty
            # This is to prevent inaccurate data (eg. total_score missing and reset to 0 but still 100 games played)
            if parent_key in DEFAULT_SAVE_DATA["difficulties"].keys():
                for sub_key in default_data:
                    save_data[sub_key] = copy.deepcopy(default_data[sub_key])
            else:  
                save_data[key] = copy.deepcopy(value)
            key_restored = True

        # If the key does exist, check if the value of the dict is another dict object
        # If it's not, then the value is not a key and we cannot nest any further
        elif isinstance(value, dict):
            # Make sure the key in save_data is a dict and not a string or list value
            if not isinstance(save_data[key], dict):
                #If it is, make it a key to a dict by giving it default values
                save_data[key] = value
                key_restored = True

            # If it is another dict, keep nesting to see if all the keys exist
            # Also set key_restored to True if a nested dict needed a key restored
            if validate_file_keys(save_data[key], value, key):
                key_restored = True

    return key_restored

# Delete any unwanted keys. Recurses through dict starting from leaf nodes, node-left-right traversal
def delete_unwanted_keys(save_data: dict, default_data: dict, parent_key: list = []) -> bool:
    key_deleted = False

    # Important: Converting save_data.items() to a list allows us to alter the dicts size/structure during iteration
    for key, value in list(save_data.items()):
        # Check if the key(s) is at the root of the dict
        # Must be done separately as root keys can't have a parent_key
        if parent_key == [] and key not in default_data:
            del save_data[key]
            key_deleted = True
        # Check nested keys against default structure
        # Also check that the data type of the value is correct
        elif key not in default_data or type(value) != type(default_data[key]):
            del save_data[key]
            key_deleted = True
        # Nest deeper if the value is a dict
        elif isinstance(value, dict):
            parent_key.append(key)
            delete_unwanted_keys(save_data[key], default_data[key], parent_key)

    return key_deleted