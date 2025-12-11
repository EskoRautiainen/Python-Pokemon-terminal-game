#   New class Room represents a location in game.
#   Room object has:
#   - name          (name of the room)
#   - description   (player can view room description with command: look around)
#   - exits         (exits to other rooms)
#   - objects       (objects inside the room, such as "Potion", "Mom", "Professor Oak")

class Room:
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.exits = {}   # example: {"north": Viridian Forest}
        self.objects = []


#   def connect is called from world.py with: bedroom.connect("direction", room)
#   this creates an exit into another room.

    def connect(self, direction, room):
        # Connect this room to another room in a given direction
        self.exits[direction] = room

#   Items are created using Item or NPC constructor: potion = Item("potion", "A basic healing spray used for Pokémon.")
#   def add_object is called from world.py with: bedroom.add_object(potion)
#   This adds an item into the chosen room.

    def add_object(self, obj):
        self.objects.append(obj)

# def full_description is called from test_game.py, when using handle_look: print(player.current_room.full_description())
# full_description returns room description and possible exits.

    def full_description(self):
        # Return description + available exits
        exits = ", ".join(self.exits.keys()) if self.exits else "None"
        return f"{self.description}\nExits: {exits}"

