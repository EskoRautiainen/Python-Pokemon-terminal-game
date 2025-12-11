from game_objects import Item
from pokemon import Pokemon, Move

#   Triggers are functions that modify the game state.
#   give_potion is executed automatically when an NPC dialogue line includes this trigger.
#   The NPC.talk(player) method calls the trigger when the corresponding dialogue entry is reached.


def give_potion(player):
    potion = Item("potion", "A basic healing spray used for Pokémon.")
    player.inventory.append(potion)
    print("Mom gave you a Potion!")




bulbasaur = Pokemon(
    "Bulbasaur", "Grass",
    moves=[Move("Tackle", "Normal"), Move("Vine Whip", "Leaf")]
)
squirtle = Pokemon(
    "Squirtle", "Water",
    moves=[Move("Tackle", "Normal"), Move("Water Gun", "Water")]
)
charmander = Pokemon(
    "Charmander", "Fire",
    moves=[Move("Scratch", "Normal"), Move("Ember", "Fire")]
)



def choose_starter(player):
    # Define starter Pokémon
    starters = {
        "bulbasaur": Pokemon("Bulbasaur", "Grass", moves=[Move("Tackle", "Normal"), Move("Razor Leaf", "Leaf")]),
        "squirtle": Pokemon("Squirtle", "Water", moves=[Move("Tackle", "Normal"), Move("Water Gun", "Water")]),
        "charmander": Pokemon("Charmander", "Fire", moves=[Move("Scratch", "Normal"), Move("Ember", "Fire")])
    }

    # Show choices with colored names
    print("Choose your starter Pokémon:")
    print(" - Leaf-type \033[32mBulbasaur\033[0m")
    print(" - Water-type \033[34mSquirtle\033[0m")
    print(" - Fire-type \033[31mCharmander\033[0m")

    while True:
        choice = input("> ").strip().lower()
        if choice in starters:
            selected = starters[choice]
            # Add Pokémon to player's party or inventory
            if not hasattr(player, "party"):
                player.party = []
            player.party.append(selected)

            print(f"\nYou chose {selected.name}!")
            print(f"{selected} \nMoves: {', '.join(str(m) for m in selected.moves)}")
            break
        else:
            print("Invalid choice. Please type Bulbasaur, Squirtle, or Charmander.")