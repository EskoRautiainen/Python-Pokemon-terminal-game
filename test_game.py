import sys
from player import Player
from world import build_world
from game_objects import NPC
from game_objects import Item

#   Returns current rooms full description.

def handle_look(player, command):
    print()
    print()
    print(player.current_room.full_description())

#   Returns targets full description. Searches the room and player inventory for the chosen item.

def handle_examine(player, command):        # Example command: "examine potion"
    parts = command.split(" ", 1)           # Split into ['examine', 'potion']
    
    if len(parts) < 2:
        print("Examine what?")
        return
    
    target_name = parts[1].strip().lower()

#   1. Search in current room
    for obj in player.current_room.objects:                     # For loop over room objects.
        if obj.name == target_name:
            print(f"{obj.name.title()} > {obj.inspect()}")      # Returns Potion > A basic healing spray used for Pokémon.
            return

#   2. Search in player's inventory
    for obj in player.inventory:
        if obj.name == target_name:
            print(f"{obj.name.title()} > {obj.inspect()}")
            return

#   3. Object not found
    print("You don't see that here.")



#   Example commands: "go north", "head down", "move west"
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


#   Quits game
def handle_quit(player, command):
    print("Quitting!")
    sys.exit()


#   Example commands: "take potion", "pick up rope"
def handle_take(player, command):
    parts = command.split(" ", 1)
    if len(parts) < 2:
        print("Take what?")
        return

    target_name = parts[1].strip().lower()

#   Search for the object in the room
    for obj in player.current_room.objects:
        if obj.name == target_name:

            #   Found it
            if obj.takeable:
                player.inventory.append(obj)
                player.current_room.objects.remove(obj)
                print(f"You picked up the {obj.name}.")
                return
            else:
                print("You can't take that.")
                return

#   No matching object found
    print("You don't see that here.")


#   handle_inventory prints all items in the inventory and includes error handling for empty inventory.
def handle_inventory(player, command):
    if not player.inventory:
        print("You are not carrying anything.")
        return

    print("You are carrying:")
    for item in player.inventory:
        print(f" - {item.name}")


#  COMMENT LATER
def handle_party(player, command):
    print("Your current party:")
    for item in player.party:
        print(f" - {item.name}")
    



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



COMMAND_HANDLERS = {
    # LOOK / EXAMINE COMMANDS
    "look": handle_look,
    "examine": handle_look,
    "inspect": handle_look,
    "check": handle_look,
    "view": handle_look,
    "observe": handle_look,
    "scan": handle_look,

    # CHECK ROOM
    "look around": handle_look,

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

    # QUIT
    "quit": handle_quit,

    # APPLY FORCE COMMANDS
    #"hit": apply_force_handler,
    #"strike": apply_force_handler,
    #"punch": apply_force_handler,
    #"swing": apply_force_handler,
    #"kick": apply_force_handler,
    #"tackle": apply_force_handler,
    #"smack": apply_force_handler,

    # PULL COMMANDS
    #"pull": pull_handler,
    #"yank": pull_handler,
    #"lift": pull_handler,
    #"tug": pull_handler,
    #"haul": pull_handler,
    #"draw": pull_handler,
    #"jerk": pull_handler,
    #"heave": pull_handler,
}


#   Build your world.
def main():
    starting_room = build_world()

#   Build player character, set starting location and print this information to start the game.
    player = Player(starting_room)
    print()
    print()
    print("Location:", player.current_room.name)



#   while True: is an infinite loop that keeps the game running, until we explicitly break or exit.
#   Loop converts input into lowercase and removes trailing spaces.
#   Take user input and compare it to all items in COMMAND_HANDLERS to find a match.
#   If user input does not find a match in COMMAND_HANDLERS, print "Unknown command"

    while True:
        command = input("> ").lower().strip()

        for cmd, func in COMMAND_HANDLERS.items():
            if command.startswith(cmd):
                func(player, command)
                break
        else:
            print("Unknown command.")

if __name__ == "__main__":
    main()


# Problems:
# "go to" does not work.
# "examine potion" returns room description, not item description.
# "pokemon use skill" is not implimented.
# Pokemon objects missing
# Battle mechanics missing
# "Look aroundZ command does not work due to "look" triggering a method first. 
# ... many more