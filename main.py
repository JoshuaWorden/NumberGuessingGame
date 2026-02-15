from game import Game
import json 

def main():
    game = Game()
    game.print_main_menu_screen()
    return

    with open("states.json") as f:
        data = json.load(f)
    
    # Print data on file
    for state in data["states"]:
        print(state["name"], state["abbreviation"])

    for state in data["states"]:
        del state["abbreviation"]
        state["name"]["abbreviation"] = "N/A"

    with open("new_states.json", "w") as f:
        json.dump(data, f, indent = 2)
    

if __name__ == "__main__":
    main()
 