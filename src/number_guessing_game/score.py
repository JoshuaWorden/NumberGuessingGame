from enum import Enum

class DifficultyLevel(Enum):
    EASY = 1
    MEDIUM = 2
    HARD = 3

class Difficulty:
    def __init__(self, lower_limit: int, upper_limit: int) -> None:
        self.best_score = 0
        self.total_score = 0
        self.games_played = 0
        self.upper_limit = upper_limit
        self.lower_limit = lower_limit
    
    @property
    def average_score(self) -> float:
        if self.games_played == 0:
            return 0
        else:
            return round(self.total_score / self.games_played, 2)
    
    def print_score(self, score: int) -> str:
        if score == 0:
            return "-"
        return str(score)
        
    def update_total_score(self, current_score: int) -> None:
        self.total_score += current_score
    
    def update_best_score(self, current_score: int) -> None:
        self.best_score = current_score

class Score:
    def __init__(self) -> None:
        self.current_score = 0

        # Manage difficulties data by storing them in a dictionary, using enum as the key and the difficulty object as the value
        self.difficulties = {
            DifficultyLevel.EASY: Difficulty(1, 100),
            DifficultyLevel.MEDIUM: Difficulty(1, 1000),
            DifficultyLevel.HARD: Difficulty(1, 10000)
        }

    # The @property decorator makes the function get treated as a variable when calling
    # For example instead of obj.get_easy(), you can just obj.easy. Much more concise and still very readable
    @property
    def easy(self) -> Difficulty: 
        return self.difficulties[DifficultyLevel.EASY]

    @property
    def medium(self) -> Difficulty: 
        return self.difficulties[DifficultyLevel.MEDIUM]

    @property
    def hard(self) -> Difficulty: 
        return self.difficulties[DifficultyLevel.HARD]

    # Get self.difficulties object of the current difficulty
    def get_difficulties_obj(self, current_difficulty: DifficultyLevel) -> Difficulty:
        return self.difficulties[current_difficulty]
    
    def update_score_data(self, current_difficulty: DifficultyLevel) -> bool:
        self.difficulties[current_difficulty].games_played += 1
        self.difficulties[current_difficulty].update_total_score(self.current_score)

        # If player achieved a high score, update high score and return true
        if self.difficulties[current_difficulty].best_score == 0 or self.current_score < self.difficulties[current_difficulty].best_score:
            self.difficulties[current_difficulty].update_best_score(self.current_score)
            return True

        # Signifies the player did not achieve a high score
        return False