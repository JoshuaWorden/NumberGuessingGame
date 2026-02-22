import random
from score import Score
from score import DifficultyLevel
import save_data

class Game:
    def __init__(self):
        self.difficulty = None
        self.scores = Score()
        self.difficulty_data = None
        self.answer = None

        save_data.load_save_data(self.scores)

    def game_loop(self):
        while (True):
            match self.main_menu():
                case 1:
                    self.select_difficulty()
                    self.player_guessing()
                case 2:
                    self.high_scores()
                case 3:
                    return
                
    def print_select_difficulty_screen(self):
        # Prompt the user to select a difficulty
        print("What difficulty would you like to play on?\n"
        f"1. Easy ({self.scores.easy.lower_limit} - {self.scores.easy.upper_limit})\n" 
        f"2. Medium ({self.scores.medium.lower_limit} - {self.scores.medium.upper_limit})\n" 
        f"3. Hard ({self.scores.hard.lower_limit} - {self.scores.hard.upper_limit})")

    def select_difficulty(self):
        self.scores.current_score = 0 
        
        while (True):
            # If user input is valid, apply that difficulty
            try:
                self.print_select_difficulty_screen()
                self.difficulty = DifficultyLevel(int(input()))
                self.difficulty_data = self.scores.get_difficulties_obj(self.difficulty)
                break
            # If user input is invalid, notify user and reprint options
            except ValueError:
                print("Invalid choice")
                

        # Determine the number to be guessed by the user
        self.answer = random.randint(self.difficulty_data.lower_limit, 
                                     self.difficulty_data.upper_limit)

        # Prompt the user to select_difficulty guessing the number
        print(f"Okay, I have picked a number between "
              f"{self.difficulty_data.lower_limit} and {self.difficulty_data.upper_limit} ({self.answer})")
        print("What number do you think it is?")

    def player_guessing(self):
        while (True):
            # Get the guessed number from the user
            try:
                guess = int(input())
                if guess < self.difficulty_data.lower_limit or guess > self.difficulty_data.upper_limit:
                    raise ValueError
            except ValueError:
                print(f"You must guess a number between {self.difficulty_data.lower_limit} and {self.difficulty_data.upper_limit}")
                continue
            
            self.scores.current_score += 1

            if guess == self.answer:
                self.win_screen()
                return
            
            # Inform the user of whether the number they need to guess is higher or lower than what they guessed
            elif guess < self.answer:
                print("Higher!")

            elif guess > self.answer:
                print("Lower!")

    def win_screen(self):
        print("Correct!")
        print(f"It took you {self.scores.current_score} attempts to guess it")
        
        # Update the score for the difficulty, and if the player achieved a high score, inform the user
        if self.scores.update_score_data(self.difficulty):
            print(f"Congratulations! "
                  f"{self.difficulty_data.best_score} is now your new best score on {self.difficulty.name}!")
        else:
            print(f"Your current best is {self.difficulty_data.best_score}")

        save_data.update_save_data(self.scores, self.difficulty)

        print("Press any key to return to the main menu")
        input()

    def print_main_menu_screen(self):
        print("GUESS THE NUMBER\n"
              "1. Play\n" 
              "2. High Scores\n"
              "3. Quit")

    def main_menu(self):
        while (True):
            # Get user choice and make sure it's valid
            try:
                self.print_main_menu_screen()
                choice = int(input())
                if choice < 1 or choice > 3:
                    raise ValueError
                return choice
            except ValueError:
                print("Invalid choice")

    def print_high_score_screen(self):
        # Width of the columns used for text alignment
        score_width = 11
        difficulty_width = 8

        # NOTE_TO_SELF: This is hard as shit to read compared to doing it all manually
        #               Although techincally this is much easier to edit and scale differently later on if needed
        print(f"{'HIGH SCORES'.center(4 + score_width*4)}\n\n"
        f"{' '.rjust(score_width)}|{'BEST'.center(score_width)}|{'AVERAGE'.center(score_width)}|{'GAMES'.center(score_width)}|\n"
        f"{'-'.center(score_width, '-')}|{'-'.center(score_width, '-')}|{'-'.center(score_width, '-')}|{'-'.center(score_width, '-')}|")
        for difficulty in DifficultyLevel: 
             print(f"{difficulty.name.rjust(difficulty_width)}   |{self.scores.easy.print_score(self.scores.difficulties[difficulty].best_score).center(score_width)}|"
             f"{self.scores.easy.print_score(self.scores.difficulties[difficulty].average_score).center(score_width)}|"
             f"{self.scores.easy.print_score(self.scores.difficulties[difficulty].games_played).center(score_width)}|")
        

        print("\n0. Back\n"
        "1. Reset ALL High Scores\n"
        f"2. Reset EASY High Scores\n"
        f"3. Reset MEDIUM High Scores\n"
        f"4. Reset HARD High Scores")

    def high_scores(self):

        while (True):
            try:
                self.print_high_score_screen()
                choice = int(input())
                if choice < 0 or choice > 4:
                    raise ValueError
            except ValueError:
                print("Invalid choice")
            
            match choice:
                case 0:
                    return
                case 1:
                    save_data.overwrite_save_data(save_data.DEFAULT_SAVE_DATA)
                case 2:
                    save_data.reset_single_difficulty(DifficultyLevel.EASY.name.lower())
                case 3:
                    save_data.reset_single_difficulty(DifficultyLevel.MEDIUM.name.lower())
                case 4:
                    save_data.reset_single_difficulty(DifficultyLevel.HARD.name.lower())

            # This will execute only if one of the reset options is selected
            save_data.load_save_data(self.scores)