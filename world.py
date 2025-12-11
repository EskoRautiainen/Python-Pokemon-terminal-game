from room import Room
from game_objects import Item, NPC
from triggers import give_potion

#   build_world creates all rooms, places objects, connects the map, and returns the starting room. 
#   It is called from main() in test_game.py.

def build_world():
    bedroom = Room("My Room", "Your cozy bedroom. A small red spray bottle labeled 'Potion' sits on your desk.")
    home = Room("Home", "Mom is cooking in the kitchen.")
    pallet = Room("Pallet Town", "A quiet town with a sea breeze.")
    lab = Room("Oak's Lab", "Professor Oak's famous research laboratory.")
    viridian_Forest_Area = Room("Viridian Forest Open Field", "Dim forest with thick trees all around. Old oak stands tall and on a quick glance, you could see something move on the branches")
    viridian_Forest_Pond = Room("Viridian Forest Pond", "Beautiful pond glisters nearby")
    viridian_Forest_Stone_Formation = Room("Viridian Forest Stone Formation", "lirum")
    viridian_Forest_Picnic = Room("Viridian Forest Picnic Area", "lirum")
    viridian_Forest_Farm = Room("Viridian Forest Small Farm", "lirum")
    viridian_Forest_Thicket_Cave = Room("Viridian Forest Thicket Cave", "lirum")
    viridian_Forest_Barren_Field = Room("Viridian Forest Barren Field", "lirum")
    Path_To_Pewter_City = Room("Path to Pewter City", "lirum")
    Pewter_City = Room("Pewter City", "lirum")
    Pewter_City_Gym = Room("Pewter City Gym", "lirum")

#   Create objects that can be placed inside rooms.
#   In the NPC class, dialogues is a list of tuples: (dialogue_text, optional_trigger_function)
#   If the trigger is not None, it is executed when that dialogue line is reached.

    potion = Item("potion", "A basic healing spray used for Pokémon.")
    mom = NPC("Mom", "Mom is making mashed potatoes.",
    dialogues=[
        ("Ash! Today is time to start your Pokémon adventure... Sniff...", None),
        ("It's okay. All children must leave home one day.", None),
        ("Remember to always be kind to Pokémon and trainers you meet!", give_potion)
    ]
)

#   Place objects in rooms

    bedroom.add_object(potion)
    home.add_object(mom)


#   Connect rooms using one-way directional links.

    bedroom.connect("down", home)
    home.connect("up", bedroom)

    home.connect("east", pallet)
    pallet.connect("west", home)

    pallet.connect("east", lab)
    lab.connect("west", pallet)

    pallet.connect("north", viridian_Forest_Area)
    viridian_Forest_Area.connect("south", pallet)

    viridian_Forest_Area.connect("east", viridian_Forest_Pond)
    viridian_Forest_Pond.connect("west", viridian_Forest_Area)

    viridian_Forest_Pond.connect("east", viridian_Forest_Stone_Formation)
    viridian_Forest_Pond.connect("north", viridian_Forest_Farm)

    viridian_Forest_Stone_Formation.connect("west", viridian_Forest_Pond)

    viridian_Forest_Stone_Formation.connect("north", viridian_Forest_Picnic)
    viridian_Forest_Picnic.connect("south", viridian_Forest_Stone_Formation)

    viridian_Forest_Picnic.connect("west", viridian_Forest_Farm)
    viridian_Forest_Farm.connect("east", viridian_Forest_Picnic)
    viridian_Forest_Farm.connect("south", viridian_Forest_Pond)

    viridian_Forest_Farm.connect("north", viridian_Forest_Thicket_Cave)
    viridian_Forest_Thicket_Cave.connect("south", viridian_Forest_Farm)

    viridian_Forest_Area.connect("west", viridian_Forest_Barren_Field)
    viridian_Forest_Barren_Field.connect("east", viridian_Forest_Area)

    viridian_Forest_Barren_Field.connect("north", Path_To_Pewter_City)
    Path_To_Pewter_City.connect("south", viridian_Forest_Barren_Field)

    Path_To_Pewter_City.connect("north", Pewter_City)
    Pewter_City.connect("south", Path_To_Pewter_City)

    Pewter_City.connect("west", Pewter_City_Gym)
    Pewter_City_Gym.connect("east", Pewter_City)

#   Return the starting room. (Game entry point)

#   def build_world is called with:
#       def main():
#       starting_room = build_world()

    return bedroom 
