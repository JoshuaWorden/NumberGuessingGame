from enum import Enum

class DifficultyLevel(Enum):
    EASY = 1
    MEDIUM = 2
    HARD = 3

class Difficulty:
    def __init__(self, lower_limit, upper_limit):
        self.best_score = 1
        self.total_score = 0
        self.games_played = 0
        self.upper_limit = upper_limit
        self.lower_limit = lower_limit
    
    def get_average(self):
        if self.games_played == 0:
            return 0
        else:
            return self.total_score / self.games_played
        
    def update_total_score(self, current_score):
        self.total_score += current_score
    
    def update_best_score(self, current_score):
        self.best_score = current_score

class Score:
    def __init__(self):
        self.current_score = 1

        # Manage difficulties data by storing them in a dictionary, using enum as the key and the difficulty object as the value
        self.difficulties = {
            DifficultyLevel.EASY: Difficulty(1, 100),
            DifficultyLevel.MEDIUM: Difficulty(1, 1000),
            DifficultyLevel.HARD: Difficulty(1, 10000)
        }

    # This is purely to shorten the code to access current difficulty in game.py
    def get_difficulty(self, current_difficulty):
        return self.difficulties[current_difficulty]
    
    def updaate_score_data(self, current_difficulty):
        self.difficulties[current_difficulty].games_played += 1
        self.difficulties[current_difficulty].update_total_score(self.current_score)

        # If player achieved a high score, update high score and return true
        if self.current_score < self.difficulties[current_difficulty].best_score:
            self.difficulties[current_difficulty].update_best_score(self.current_score)
            return True

        # Signifies the player did not achieve a high score
        return False