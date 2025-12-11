from room import Room
from game_objects import Item, NPC, HeavyItem, GameObject
from triggers import give_potion, choose_starter, tree_hit_trigger


def build_world():
#----------------------------------------------------------------------------------------------------------------------
#                               DEFINE MAP OBJECTS
#----------------------------------------------------------------------------------------------------------------------

    #   Create objects that can be placed inside rooms.
    #   In the NPC class, dialogues is a list of tuples: (dialogue_text, optional_trigger_function)
    #   If the trigger is not None, it is executed when that dialogue line is reached.

    potion = Item("potion", "A basic healing spray used for Pokémon.")

    forest_tree = HeavyItem("tree", "A tall oak tree with thick branches.",
        triggers={
            "hit": tree_hit_trigger,
            "kick": tree_hit_trigger
        }
    )

    mom = NPC(
        "Mom",
        "Mom is making mashed potatoes.",
        dialogues=[
            ("Ash! Today is time to start your Pokémon adventure... Sniff...", None),
            ("It's okay. All children must leave home one day.", None),
            ("Remember to always be kind to Pokémon and trainers you meet!", give_potion)
        ],
        repeatable=True
    )

    professor = NPC(
        "Professor Oak",
        "Professor Oak is tinkering with some gadgets.",
        dialogues=[
            (
                "Hello, there! My name is Oak. People affectionately refer to me as the Pokémon professor.",
                None
            ),
            (
                "For some people, Pokémon are pets. Others use them for battling. As for myself, I study Pokémon as a profession.",
                None
            ),
            (
                "When I was younger, I was a passionate Pokémon trainer. That was a long time ago, and now I only have a few left. "
                "I'll let you choose one so you can start your own Pokémon adventure. "
                "I have the Leaf-type \033[32mBulbasaur\033[0m, the Water-type \033[34mSquirtle\033[0m, or the Fire-type \033[31mCharmander\033[0m?",
                None
            ),
            (
                "That's a fine choice. Please take good care of it.",
                choose_starter
            )
        ],
        repeatable=False
    )

#----------------------------------------------------------------------------------------------------------------------
#                               CREATE ROOMS AND ADD OBJECTS.
#----------------------------------------------------------------------------------------------------------------------

    bedroom = Room("My Room", "Your cozy bedroom. A small red spray bottle labeled 'Potion' sits on your desk.")
    bedroom.add_object(potion)
    
    home = Room("Home", "Mom is cooking in the kitchen.")
    home.add_object(mom)

    pallet = Room("Pallet Town", "A quiet town with a sea breeze.")


    lab = Room("Oak's Lab", "Professor Oak's famous research laboratory.")
    lab.add_object(professor)

    viridian_Forest_Area = Room("Viridian Forest Open Field", "Dim forest with thick trees all around. Old oak stands tall and on a quick glance, you could see something move on the branches")
    viridian_Forest_Area.add_object(forest_tree)
    
    viridian_Forest_Pond = Room("Viridian Forest Pond", "Beautiful pond glisters nearby")
    
    
    viridian_Forest_Stone_Formation = Room("Viridian Forest Stone Formation", "lirum")
    
    
    viridian_Forest_Picnic = Room("Viridian Forest Picnic Area", "lirum")
    
    
    viridian_Forest_Farm = Room("Viridian Forest Small Farm", "lirum")
    
    
    viridian_Forest_Thicket_Cave = Room("Viridian Forest Thicket Cave", "lirum")
    
    
    viridian_Forest_Barren_Field = Room("Viridian Forest Barren Field", "lirum")
    
    
    Path_To_Pewter_City = Room("Path to Pewter City", "lirum")
    
    
    Pewter_City = Room("Pewter City", "lirum")
    
    
    Pewter_City_Gym = Room("Pewter City Gym", "lirum")




#----------------------------------------------------------------------------------------------------------------------
#                               CONNECT ROOMS
#----------------------------------------------------------------------------------------------------------------------

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


#----------------------------------------------------------------------------------------------------------------------
#                               STARTING POINT
#----------------------------------------------------------------------------------------------------------------------
#   def build_world is called with:
#       def main():
#       starting_room = build_world()

    return viridian_Forest_Area 
