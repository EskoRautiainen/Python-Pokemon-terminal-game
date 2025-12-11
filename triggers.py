from game_objects import Item
from pokemon import Pokemon, Move

# Triggers are functions that modify the game state.
# give_potion is executed automatically when an NPC dialogue line includes this trigger.
# The NPC.talk(player) method calls the trigger when the corresponding dialogue entry is reached.

#----------------------------------------------------------------------------------------------------------------------
#                               TRIGGERS - HOME
#----------------------------------------------------------------------------------------------------------------------

# Mom gives a potion after you talk to her 3 times.
def give_potion(player):
    potion = Item("potion", "A basic healing spray used for Pokémon.")
    player.inventory.append(potion)
    print("Mom gave you a Potion!")

#----------------------------------------------------------------------------------------------------------------------
#                               TRIGGERS - LAB
#----------------------------------------------------------------------------------------------------------------------

# Starter is picked after talking to Professor Oak 4 times.
def choose_starter(player):
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

#----------------------------------------------------------------------------------------------------------------------
#                               TRIGGERS - VIRIDIAN_FOREST_AREA
#----------------------------------------------------------------------------------------------------------------------

# Spawn Pokemon after using Apply Force Command on a tree.
def tree_hit_trigger(player):
    bulbasaur = Pokemon(
        "Bulbasaur",
        "Leaf",
        45,
        moves=[Move("Tackle", "Normal"), Move("Vine Whip", "Leaf")]
    )
    player.current_room.add_object(bulbasaur)
    print("A wild Bulbasaur fell from the tree!")

    # Update room description
    player.current_room.description = "Dim forest with thick trees all around. Bulbasaur is angry!"

    