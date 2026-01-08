
import sys
from player import Player
from triggers import apply_force_handler, brock_battle, drop_handler, handle_use, pull_handler, water_handler
from world import build_world
from game_objects import NPC, Pokemon, Move
from game_objects import Item


#----------------------------------------------------------------------------------------------------------------------
#                               GENERAL HANDLES
#----------------------------------------------------------------------------------------------------------------------
# Returns current rooms full description.
def handle_look(player, command):
    print()
    print()
    print(player.current_room.full_description())


# -----------------------------------------------------------------
# Example command: "examine potion" or "examine bulbasaur"
# Prints the description of the target item, object, or Pokémon.
def handle_examine(player, command):
    
    parts = command.split(" ", 1)
    
    if len(parts) < 2:
        print("Examine what?")
        return

    target_name = parts[1].strip().lower()

    # 1. Search objects in the current room
    for obj in player.current_room.objects:
        if obj.name.lower() == target_name:
            print(obj) if isinstance(obj, Pokemon) else print(f"{obj.name.title()} > {obj.inspect()}")
            return

    # 2. Search objects in the player's inventory
    for obj in player.inventory:
        if obj.name.lower() == target_name:
            print(obj) if isinstance(obj, Pokemon) else print(f"{obj.name.title()} > {obj.inspect()}")
            return

    # 3. Search player's party (Pokémon)
    for pokemon in player.party:
        if pokemon.name.lower() == target_name:
            print(pokemon)  # uses Pokemon.__str__()
            return

    # 4. Target not found
    print("You don't see that here.")



# -----------------------------------------------------------------
# Example commands: "go north", "head down", "move west"
def handle_move(player, command):
    parts = command.split()

    if len(parts) < 2:
        print("Go where?")
        return

#   The word after go/walk/move
    direction = parts[1]                

#   Calls for player.move method, passing direction as a parameter.
    result = player.move(direction)
    print()
    print()
    print(result)


# -----------------------------------------------------------------
#   Prints help
def handle_help(player,command):
    print("Check player inventory with -inventory. ")
    print("Check player party with -party. ")
    print("Examine Pokemon and items with -check Bulbasaur/Potion. ")
    print("Also check out commands like: look around, go, take, talk, use, pull, drop, water crops/plants, catch/pokeball. Have fun!")



# -----------------------------------------------------------------
#   Quits game
def handle_quit(player, command):
    print("Quitting!")
    sys.exit()



# -----------------------------------------------------------------
#   Example commands: "take potion", "pick up rope"
def handle_take(player, command):
    parts = command.split(" ", 1)
    if len(parts) < 2:
        print("Take what?")
        return

    target_name = parts[1].strip().lower()

    for obj in player.current_room.objects:
        if obj.name.lower() == target_name:

            # Run "take" trigger if it exists
            if hasattr(obj, "triggers") and "take" in obj.triggers:
                trigger_handled = obj.triggers["take"](player)
                # Do NOT return here; the trigger may unlock the item
                # Only return if the trigger completely handled the action
                if getattr(obj, "takeable", False) is False and trigger_handled:
                    return

            # Now check if the object is takeable
            if getattr(obj, "takeable", True):
                player.inventory.append(obj)
                player.current_room.objects.remove(obj)
                print(f"You picked up the \033[32m{obj.name}\033[0m.")

                # Update room description for rope
                if obj.name.lower() == "rope" and player.current_room.name == "Viridian Forest Picnic Area":
                    player.current_room.description = (
                        "The picnic area is calm now, with the crafting table still present. "
                        "The sturdy rope you saw earlier has been taken, leaving the spot empty and serene."
                    )

                # Dynamic room update for potion
                if obj.name.lower() == "potion" and player.current_room.name == "My Room":
                    player.current_room.description = (
                        "Your cozy bedroom is bathed in morning sunlight filtering through the curtains. "
                        "The desk is now empty, with only a neatly folded map of Pallet Town remaining. "
                        "Posters of various Pokémon line the walls, and a faint smell of old books and wooden furniture fills the air."
                    )
                return

            else:
                print("You can't take that yet.")
                return

    print("You don't see that here.")



# -----------------------------------------------------------------
#   handle_inventory prints all items in the inventory and includes error handling for empty inventory.
def handle_inventory(player, command):
    if not player.inventory:
        print("You are not carrying anything.")
        return

    print("You are carrying:")
    for item in player.inventory:
        print(f" - {item.name}")



# -----------------------------------------------------------------
#  shows your current pokemon party
def handle_party(player, command):
    print("Your current party:")
    for item in player.party:
        print(f" - {item.name}")




# -----------------------------------------------------------------
#   How the method works:
#   Player writes: " Talk to Mom ". 
#   => "talk to mom" (converts to lowercase, removes any trailing spaces).
#   => "to mom" (removes first four letters, removes any trailing spaces).
#   => "mom" (if word starts with "to", remove first three letters.)

def handle_talk(player, command):
    text = command.lower().strip()
    text = text[len("talk"):].strip()
    if text.startswith("to "):
        text = text[3:].strip()

    if not text:
        print("Talk to who?")
        return


#   Look for NPC in the current room.
#   If statement "isinstance(x,y)" checks the objects subclass.

#   1. First check if the object is an Item
    for obj in player.current_room.objects:
        if isinstance(obj, Item) and obj.name == text:
            print(f"You try to talk to the {obj.name}, but it doesn't respond.")
            return

#   2. Then check if the object is an NPC
    for obj in player.current_room.objects:
        if isinstance(obj, NPC) and obj.name == text:
            # Pass the player object for triggers
            print(obj.talk(player))
            return

#   3. Object not found in the room
    print("They are not here.")



# -----------------------------------------------------------------
# Catch Pokemon to add them into your party
def handle_throw_pokeball(player, command):
    parts = command.split()
    if len(parts) < 2:
        print("Throw pokeball at what?")
        return

    target_name = " ".join(parts[1:]).strip().lower()
    target = next(
        (p for p in player.current_room.objects if isinstance(p, Pokemon) and p.name.lower() == target_name),
        None
    )

    if not target:
        print(f"There is no {target_name} here.")
        return

    # Pond puzzle: Poliwag cannot be caught until bait is used
    if target.name.lower() == "poliwag" and getattr(target, "pond_puzzle", None):
        if not target.pond_puzzle.catchable:
            print("\033[32mPoliwag\033[0mquickly dashed underwater and dodged your PokeBall. \033[32mPoliwag\033[0m is too close to the pond to be caught.")
            return

    # Catch normally
    if len(player.party) < 6:
        player.party.append(target)
        player.current_room.objects.remove(target)
        print(f"You caught {target.name}!")

        # Update room description based on which Pokémon was caught
        if target.name.lower() == "caterpie":
            player.current_room.description = (
                "The ground is carpeted with moss and scattered leaves. "
                "The trees ahead are quiet now; the small shape that once darted among them is gone. "
                "A faint breeze rustles the leaves where \033[32mCaterpie\033[0m once scurried."
            )
        elif target.name.lower() == "poliwag":
            player.current_room.description = (
                "The pond's surface ripples gently, now free of the playful \033[32mPoliwag\033[0m. "
                "A few droplets linger on nearby leaves, marking where it splashed and dived."
            )
        elif target.name.lower() == "growlithe":
            player.current_room.description = (
            "The clearing is quiet again, the wild \033[32mGrowlithe\033[0m now happily in your party. "
            "The sturdy wooden crafting table stands nearby, tools neatly arranged on its surface. "
            "The rope lies safely on the ground, ready for you to pick up. Sunlight filters through the trees, and the forest feels calm and peaceful once more."
            )
        elif target.name.lower() == "sandshrew":
            player.current_room.description = (
            "The wide clearing looks a bit emptier now, with the dry grass swaying gently in the wind. "
            "The ranger is still here, looking exhausted from his long watch, but \033[32mPikachu\033[0m is no longer playing in the field. "
            "The northern path is clear, inviting you to continue your journey."
            )
        elif target.name.lower() == "pikachu":
            player.current_room.description = (
            "The wide clearing looks a bit emptier now, with the dry grass swaying gently in the wind. "
            "The ranger is still here, looking exhausted from his long watch, but \033[32mPikachu\033[0m is no longer playing in the field. "
            "The northern path is clear, inviting you to continue your journey."
            )
        elif target.name.lower() == "vaporeon":
            player.current_room.description = (
            "You ascend a steep, narrow passage to the cave's upper level. The walls are rougher here, with jagged stalactites hanging dangerously overhead. "
            "A faint, cold draft snakes through the tunnels, carrying the earthy scent of damp stone and moss. "
            "Small pools of water glimmer in the dim light, reflecting shadows of unseen Pokémon moving in the darkness. "
            "Loose gravel underfoot makes every step precarious, and the sound of distant footsteps echoes eerily through the cavern"
            )
        
        else:
            print(f"Your party is full! {target.name} remains wild.")


COMMAND_HANDLERS = {
    # EXAMINE COMMANDS
    "examine": handle_examine,
    "inspect": handle_examine,
    "check": handle_examine,
    "view": handle_examine,
    "observe": handle_examine,
    "scan": handle_examine,

    # CHECK ROOM
    "look around": handle_look,
    "look": handle_look,

    # MOVE COMMANDS
    "go": handle_move,
    "walk": handle_move,
    "move": handle_move,
    "head": handle_move,
    "run": handle_move,

    # TAKE / PICK UP COMMANDS
    "take": handle_take,
    "pick": handle_take,
    "grab": handle_take,
    "collect": handle_take,
    "get": handle_take,
    "gather": handle_take,
    "loot": handle_take,
    "pocket": handle_take,

    # SHOW INVENTORY
    "inventory": handle_inventory,
    "show inventory": handle_inventory,
    "backpack": handle_inventory,
    "show backpack": handle_inventory,
    "items": handle_inventory,
    "show items": handle_inventory,

    # SHOW PARTY/POKEMON
    "party": handle_party,
    "show party": handle_party,
    "pokemon": handle_party,
    "show pokemon": handle_party,

    # TALK COMMAND
    "talk": handle_talk,
    "talk to": handle_talk,
    "speak": handle_talk,
    "talk to": handle_talk,

    # QUIT
    "quit": handle_quit,

    # APPLY FORCE COMMANDS
    "hit": apply_force_handler,
    "strike": apply_force_handler,
    "punch": apply_force_handler,
    "swing": apply_force_handler,
    "kick": apply_force_handler,
    "tackle": apply_force_handler,
    "smack": apply_force_handler,

    # USE COMMANDS
    "use": handle_use,
    "craft": handle_use,

    # PULL COMMANDS
    "pull": pull_handler,
    "yank": pull_handler,
    "lift": pull_handler,
    "tug": pull_handler,
    "haul": pull_handler,
    "draw": pull_handler,
    "jerk": pull_handler,
    "heave": pull_handler,

    # DROP COMMANDS
    "drop": drop_handler,
    "leave": drop_handler,


    # WATER COMMANDS
    "water plants": water_handler,
    "water crops": water_handler,

    # THROW POKEBALL / CAPTURE
    "pokeball": handle_throw_pokeball,
    "catch": handle_throw_pokeball,

    # HELP
    "help": handle_help,
}

#   while True: is an infinite loop that keeps the game running, until we explicitly break or exit.
#   Loop converts input into lowercase and removes trailing spaces.
#   Take user input and compare it to all items in COMMAND_HANDLERS to find a match.
#   If user input does not find a match in COMMAND_HANDLERS, print "Unknown command"

#   while True: is an infinite loop that keeps the game running, until we explicitly break or exit.
#   Loop converts input into lowercase and removes trailing spaces.
#   Take user input and compare it to all items in COMMAND_HANDLERS to find a match.
#   If user input does not find a match in COMMAND_HANDLERS, print "Unknown command"

FILLER_WORDS = {"to", "at", "the", "a", "an", "on", "in"}

def clean_command(command):
    # Remove common filler words from a command to make parsing easier.
    words = command.split()
    cleaned_words = [w for w in words if w not in FILLER_WORDS]
    return " ".join(cleaned_words)

def main():
    starting_room = build_world()
    player = Player(starting_room)
    print()
    print("Location:", player.current_room.name)

    # Game loop
    while True:
        raw_command = input("> ").lower().strip()
        command = clean_command(raw_command)  # remove "to", "the", etc.

        for cmd, func in COMMAND_HANDLERS.items():
            if command.startswith(cmd):
                func(player, command)
                break
        else:
            print("Unknown command.")


if __name__ == "__main__":
    main()