import random
import json
from score import Score
from score import DifficultyLevel
import save_data

class Game:
    def __init__(self):
        self.difficulty = None
        self.scores = Score()
        self.difficulty_data = None
        self.answer = None
        self.easy = self.scores.difficulties[DifficultyLevel.EASY]
        self.medium = self.scores.difficulties[DifficultyLevel.MEDIUM]
        self.hard = self.scores.difficulties[DifficultyLevel.HARD]

    def select_difficulty(self):
        self.scores.current_score = 0 

        # Prompt the user to select a difficulty
        print("What difficulty would you like to play on?\n" \
        f"1. Easy ({self.easy.lower_limit} - {self.easy.upper_limit})\n" 
        f"2. Medium ({self.medium.lower_limit} - {self.medium.upper_limit})\n" 
        f"3. Hard ({self.hard.lower_limit} - {self.hard.upper_limit})")
        
        # If user input is valid, apply that difficulty
        try:
            self.difficulty = DifficultyLevel(int(input()))
            self.difficulty_data = self.scores.get_difficulty(self.difficulty)
        # If user input is invalid, notify user and reprint options
        except ValueError:
            print("Invalid choice")
            self.select_difficulty()
        
        # Determine the number to be guessed by the user
        self.answer = random.randint(self.difficulty_data.lower_limit, 
                                     self.difficulty_data.upper_limit)

        # Prompt the user to select_difficulty guessing the number
        print(f"Okay, I have picked a number between "
              f"{self.difficulty_data.lower_limit} and {self.difficulty_data.upper_limit} ({self.answer})")
        print("What number do you think it is?")

        self.player_guessing() 

    def player_guessing(self):
        # Get the guessed number from the user
        try:
            guess = int(input())
        except ValueError:
            print("You must guess a number")
            self.player_guessing()

        self.scores.current_score += 1

        if guess == self.answer:
            self.print_win_screen()
        
        # Check to see if the users number is within the bounds of the current difficulty of the game
        elif guess < self.difficulty_data.lower_limit:
            print(f"The number can't be lower than {self.difficulty_data.lower_limit},"
                  f" guess a number between {self.difficulty_data.lower_limit}"
                  f" and {self.difficulty_data.upper_limit}")

        elif guess > self.difficulty_data.upper_limit:
            print(f"The number can't be greater than {self.difficulty_data.upper_limit},"
                  f" guess a number between {self.difficulty_data.lower_limit}"
                  f" and {self.difficulty_data.upper_limit}")
        
        # Inform the user of whether the number they need to guess is higher or lower than what they guessed
        elif guess < self.answer:

            print("Higher!")

        elif guess > self.answer:
            print("Lower!")
        
        self.player_guessing()

    def print_win_screen(self):
        print("Correct!")
        print(f"It took you {self.scores.current_score} attempts to guess it")
        
        # Update the score for the difficulty, and if the player achieved a high score, inform the user
        if self.scores.update_score_data(self.difficulty):
            print(f"Congratulations! "
                  f"{self.difficulty_data.best_score} is now your new best score on {self.difficulty}!")
        else:
            print(f"Your current best is {self.difficulty_data.best_score}")

        print(f"Your current average for {self.difficulty} is"
              f" {self.difficulty_data.get_average()} guesses")

        self.print_play_again_screen()

    def print_play_again_screen(self):
        print("Would you like to play again? Y / N")

        choice = input()

        if choice == "Y" or choice == "y":
            self.select_difficulty()
        elif choice == "N" or choice == "n":
            self.print_main_menu_screen()
        else:
            print("Invalid response\n")
        self.print_play_again_screen()

    def print_main_menu_screen(self):

        print("GUESS THE NUMBER\n"
              "1. Play\n" 
              "2. High Scores\n"
              "3. Quit")

        # Get user choice and make sure it's valid
        try:
            choice = int(input())
            if choice < 1 and choice > 3:
                raise ValueError
        except ValueError:
            print("Invalid choice")
            self.print_main_menu_screen()

        match choice:
            case 1:
                self.select_difficulty()
            case 2:
                self.print_high_score_screen()
                self.print_main_menu_screen()
            case 3:
                quit()

    def print_high_score_screen(self):
        # Width of the columns used for text alignment
        key_width = 13 # Technically 17, minus the four spaces before column line
        value_width = 12

        # NOTE_TO_SELF: This is hard as shit to read compared to doing it all manually
        #               Although techincally this is much easier to edit and scale differently later on if needed
        print(
        f"{'HIGH SCORES'.center(key_width+4 + value_width*3 + 4)}\n\n"
        f"{'DIFFICULTY'.rjust(key_width)}    |{'EASY'.center(value_width)}|{'MEDIUM'.center(value_width)}|{'HARD'.center(value_width)}|\n"
        f"{'-'.center(key_width+4, '-')}|{'-'.center(value_width, '-')}|{'-'.center(value_width, '-')}|{'-'.center(value_width, '-')}|\n"
        f"{'BEST SCORE'.rjust(key_width)}    |{str(self.easy.best_score).center(value_width)}|"
                          f"{str(self.medium.best_score).center(value_width)}|"
                          f"{str(self.hard.best_score).center(value_width)}|\n" 
        f"{'AVERAGE SCORE'.rjust(key_width)}    |{str(self.easy.get_average()).center(value_width)}|"
                          f"{str(self.medium.get_average()).center(value_width)}|"
                          f"{str(self.hard.get_average()).center(value_width)}|\n"
        f"{'GAMES PLAYED'.rjust(key_width)}    |{str(self.easy.games_played).center(value_width)}|"
                          f"{str(self.medium.games_played).center(value_width)}|"
                          f"{str(self.hard.games_played).center(value_width)}|\n\n"
        "Press any key to go back to the main menu")

        input()
                
    def load_save_data(self):
        saved_data = save_data.get_save_data()

        for key, value in saved_data["difficulties"].items():
            # Simplify difficulty assigning by upper-casing key to match enum
            difficulty = DifficultyLevel[key.upper()]

            self.scores.difficulties[difficulty].best_score = value["best_score"]
            self.scores.difficulties[difficulty].total_score = value["total_score"]
            self.scores.difficulties[difficulty].games_played = value["games_played"]