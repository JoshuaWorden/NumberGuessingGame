import random
import json
from score import Score
from score import DifficultyLevel
import save_data

class Game:
    difficulty = None
    scores = Score()
    difficulty_data = None
    answer = None

    def select_difficulty(self):
        # Prompt the user to select a difficulty
        print("What difficulty would you like to play on?\n" \
        f"1. Easy ({self.scores.difficulties[DifficultyLevel.EASY].lower_limit} - "
        f"{self.scores.difficulties[DifficultyLevel.EASY].upper_limit})\n" 
        f"2. Medium ({self.scores.difficulties[DifficultyLevel.MEDIUM].lower_limit} - "
        f"{self.scores.difficulties[DifficultyLevel.MEDIUM].upper_limit})\n" 
        f"3. Hard ({self.scores.difficulties[DifficultyLevel.HARD].lower_limit} - "
        f"{self.scores.difficulties[DifficultyLevel.HARD].upper_limit})")
        
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
            self.scores.current_score += 1
            print("Higher!")

        elif guess > self.answer:
            self.scores.current_score += 1
            print("Lower!")
        
        self.player_guessing()

    def print_win_screen(self):
        print("Correct!")
        print(f"It took you {self.scores.current_score} attempts to guess it")
        
        # Update the score for the difficulty, and if the player achieved a high score, inform the user
        if self.scores.updaate_score_data(self.difficulty):
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
            self.scores.current_score = 1 
            self.select_difficulty()
        elif choice == "N" or choice == "n":
            quit()
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
                print("HIGH SCORES\n"
                    "TO BE COMPLETED....")
            case 3:
                quit()
                
    def load_save_data(self):
        saved_data = save_data.get_save_data()

        for key, value in saved_data["difficulties"].items():
            # Simplify difficulty assigning by upper-casing key to match enum
            difficulty = DifficultyLevel[key.upper()]

            self.scores.difficulties[difficulty].best_score = value["best_score"]
            self.scores.difficulties[difficulty].total_score = value["total_score"]
            self.scores.difficulties[difficulty].games_played = value["games_played"]