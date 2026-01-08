#   New class Player represents the player character.
#   Player character object has:
#   - current_room (the room player is currently in)
#   - inventory (a list of items the player carries)
#   - party (holds up to 6 pokemon objects)

#   NOTE: current_room is initially set to starting_room, which is defined in world.py (currently returns bedroom).
#   NOTE: inventory and party are initialized as empty lists.

class Player:                                       
    def __init__(self, starting_room):         
        self.current_room = starting_room
        self.inventory = []
        self.party = []

#   'self' is a reference to the current instance of the Player class.
#   'direction' is a string like "north", "down", or "east".
#   self.current_room.exits is a dictionary mapping directions to connected Room objects.

#   How the move function works?
#   => def move is called from test_game with: result = player.move(direction)
#   => If the player types "go north", it checks if "north" exists in the self_current_room.exits dictionary.
#   => If the exit exists, updates self.current_room to the connected room.
#   => Returns a message stating where the player has moved, or that the movement is not possible.


    def move(self, direction):
        exit_data = self.current_room.exits.get(direction)

        if not exit_data:
            return "You can't go that way."

        guard = exit_data.get("guard")
        if guard and not guard(self):
            return "You can't go that way."

        self.current_room = exit_data["room"]
        return f"You move {direction} to {self.current_room.name}."