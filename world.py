from room import Room
from game_objects import Item, NPC, HeavyItem, Pokemon, Move
from triggers import brock_battle, give_potion, choose_starter, tree_hit_trigger, crafting_table_trigger, rope_trigger, water_crops_trigger, pull_sandshrew_trigger
from guards import barren_field_north_guard


def build_world():
#----------------------------------------------------------------------------------------------------------------------
#                               DEFINE MAP OBJECTS
#----------------------------------------------------------------------------------------------------------------------

#   Create objects that can be placed inside rooms.
#   In the NPC class, dialogues is a list of tuples: (dialogue_text, optional_trigger_function)
#   If the trigger is not None, it is executed when that dialogue line is reached.


#----------------------------------------------------------------------------------------------------------------------
#                               ITEMS
#----------------------------------------------------------------------------------------------------------------------
    potion = Item("potion", "A basic healing spray used for Pokémon.")
    berry = Item("berry", "A small, juicy berry. Might be useful for crafting")
    watering_can = Item("watering can", "A small metal watering can, perfect for reviving plants.")


    rope = HeavyItem("rope", "A sturdy piece of rope.",
    triggers={"take": rope_trigger}
    )
    

    forest_tree = HeavyItem("tree", "A tall oak tree with thick branches.",
        triggers={
            "hit": tree_hit_trigger,
            "kick": tree_hit_trigger
        }
    )


    crafting_table = HeavyItem(
        "crafting table",
        "A sturdy wooden table with various tools scattered on it.",
        triggers={"use": crafting_table_trigger}
    )


    crops = HeavyItem(
    "crops",
    "Wilted crops that desperately need watering.",
    triggers={"water crops": water_crops_trigger, "water plants": water_crops_trigger}
)
    crops.watered = False  # initially not watered


    sandshrew = HeavyItem(
        "sandshrew",
        "A rusty metal screw embedded in the ground. Something seems trapped beneath it.",
        triggers={"pull": pull_sandshrew_trigger}
)

#----------------------------------------------------------------------------------------------------------------------
#                               PERSONS
#----------------------------------------------------------------------------------------------------------------------

    professor = NPC(
        "Professor Oak",
        "Professor Oak is respected troughout entire Kanto region",
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


    ranger = NPC(
        "Ranger",
        "A ranger blocking the northern path. He looks exhausted.",
        dialogues=[
            ("Ugh… I’ve been standing here all day. I’d give anything for some lemonade.", None),
            ("Seriously… my canteen is bone dry.", None),
        ],
        repeatable=True
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


    daisy = NPC(
        "Daisy",
        "Garys little sister is drawing on the table",
        dialogues=[
        ("Hi Ash! Are you excited to start your Pokémon adventure?", None),
        ("Gary always talks about his Pokémon battles… I hope you do well!", None),
        ("Don't forget to be kind to Pokémon—they're your friends, not just battle partners.", None),
        ("If you see Gary, say hi for me!", None),
        ("I drew a picture of Pikachu for you! Keep it safe.", None)
        ],
        repeatable=True
    )


    nurse = NPC(
        "Nurse",
        "Nurse is working hard by the counter",
        dialogues=[
        ("Hello! Welcome to the Pokémon Center!", None),
        ("Do you need your Pokémon healed?", None),
        ("Your Pokémon are looking strong and healthy!", None),
        ("Remember to take good care of your Pokémon between battles.", None),
        ("Come back anytime if your Pokémon need some rest.", None)
        ],
        repeatable=True
    )


    brock = NPC(
        "Brock",
        "Tough trainer that specializes in Rock-type Pokémon.",
        dialogues=[
        ("Welcome to the Pewter City Gym!", None),
        ("I am Brock, the Rock-type Gym Leader.", None),
        ("Are you ready to test your skills in a Pokémon battle?", None),
        ("Let’s see if your team is strong enough!", brock_battle)  # triggers the battle
    ],
    repeatable=True
)



#----------------------------------------------------------------------------------------------------------------------
#                               POKEMON
#----------------------------------------------------------------------------------------------------------------------

    pikachu = Pokemon(
        "Pikachu",
        "Electric",
        40,
        moves=[Move("Thunder Shock", "Electric"), Move("Quick Attack", "Normal")]
    )

    vaporeon = Pokemon(
        "Vaporeon",
        "Water",
        95,
        moves=[Move("Water Pulse", "Water"), Move("Tail Slam", "Normal")]
    )


    poliwag = Pokemon(
        "Poliwag",
        "Water",
        30,
        moves=[Move("Splash", "Water"), Move("Water Gun", "Water")]
    )
    poliwag.pond_puzzle = type("PondPuzzle", (), {})()  # empty object to hold state
    poliwag.pond_puzzle.bait_dropped = False
    poliwag.pond_puzzle.catchable = False


#----------------------------------------------------------------------------------------------------------------------
#                               CREATE ROOMS AND ADD OBJECTS.
#----------------------------------------------------------------------------------------------------------------------

    bedroom = Room("My Room",
    "Your cozy bedroom is bathed in morning sunlight filtering through the curtains. "
    "On your desk lies a small, red spray bottle labeled \033[32mPotion\033[0m, next to a neatly folded map of Pallet Town. "
    "Posters of various Pokémon line the walls, and a faint smell of old books and wooden furniture fills the air. ")
    bedroom.add_object(potion)
    

    home = Room("Home",
    "The warm, inviting kitchen of your home smells faintly of mashed potatoes and freshly baked bread. "
    "\033[32mMom\033[0m is bustling about, preparing meals while humming a tune. "
    "Family photos are hung on the walls, and a soft rug covers part of the wooden floor. "
    "A sense of safety and nostalgia permeates the room, but adventure calls beyond the door.")
    home.add_object(mom)


    pallet = Room("Pallet Town",
    "Pallet Town is a quiet, coastal town where the sea breeze carries the scent of salt and wildflowers. "
    "Small houses with red rooftops are dotted along cobblestone paths, and children can be seen playing in the distance. "
    "The town exudes calm, yet the faint sounds of Pokémon calls hint at the wild adventures just beyond its borders.")


    garys_house = Room("Garys House",
    "The house of your rival, Gary, stands proudly on a tidy lot with a white picket fence. "
    "The garden is well-kept, with colorful flowers swaying gently in the breeze. "
    "Inside, you can glimpse neat furniture, shelves lined with books and gadgets, and faint sounds of laughter echoing from within. "
    "\033[32mDaisy\033[0m appears to be drawing on the kitchen table")
    garys_house.add_object(daisy)


    lab = Room("Oak's Lab",
    "\033[32mProfessor Oak's\033[0m research laboratory is filled with shelves of books, glass beakers bubbling with colorful liquids, "
    "and high-tech devices whirring softly in the background. "
    "Charts of Pokémon anatomy and evolution are pinned to the walls, and a soft hum of energy fills the room. "
    "The air smells faintly of ink, paper, and metallic tools, a testament to decades of Pokémon research.")
    lab.add_object(professor)


    viridian_Forest_Area = Room("Viridian Forest Open Field",
    "The Viridian Forest opens up into a dim, dense field where sunlight struggles to pierce the thick canopy above. "
    "Towering oak and pine trees stand like guardians, their leaves rustling with every breeze. "
    "The ground is carpeted with moss and fallen leaves. Faint movement flickers between the trees, and an uneasy feeling creeps over you—as if you’re being watched. "
    "There is certainly something up in that tree.")
    viridian_Forest_Area.add_object(forest_tree)
    

    viridian_Forest_Pond = Room("Viridian Forest Pond",
    "A serene pond lies nestled in a clearing of Viridian Forest. The water glistens under the filtered sunlight, "
    "reflecting the surrounding trees and the occasional passing cloud. "
    "\033[32mPoliwag\033[0m can be seen splashing near the edge, circling playfully and making ripples across the surface. "
    "Dragonflies hover above, and the scent of fresh water mixed with wet foliage gives the area a calming, almost magical atmosphere. "
    "You can hear the distant calls of forest Pokémon, and the occasional rustle in the reeds hints at creatures just out of sight.")
    viridian_Forest_Pond.add_object(poliwag)
    
    
    viridian_Forest_Stone_Formation = Room("Viridian Forest Stone Formation",
    "Cool air drifts between the towering stones, and the forest feels still again. "
    "Behind the imposing stones, you find an unusual sight. "
    "You notice a \033[32mSandshrew\033[0m with its head stuck on the ground, struggling to get free." )
    viridian_Forest_Stone_Formation.add_object(sandshrew)
    
    
    viridian_Forest_Picnic = Room("Viridian Forest Picnic Area",
    "You arrive at a peaceful clearing in Viridian Forest. " \
    "Soft grass carpets the ground, and a sturdy wooden \033[32mcrafting table\033[0m sits near a tree, scattered with tools and bits of wood. " \
    "A sturdy \033[32mrope\033[0m lies coiled nearby, ready for use. Sunlight filters gently through the canopy above, and the forest feels calm and watchful.")
    viridian_Forest_Picnic.add_object(rope)
    
    
    viridian_Forest_Farm = Room("Viridian Forest Small Farm",
    "You arrive at a small, sun-drenched farm nestled among the forest trees. "
    "An elderly couple tends to the land, looking weary from the dry season. "
    "Their crops have wilted and cracked under the relentless sun, and the soil begs for water. "
    "A few scattered tools lie near a wooden shed. A watering can sits by the fence. "
    "Despite the hardships, the couple greets you warmly, hopeful that some help might revive their farm.")
    viridian_Forest_Farm.add_object(watering_can)
    viridian_Forest_Farm.add_object(crops)
    

    viridian_Forest_Thicket_Cave = Room("Viridian Forest Thicket Cave",
    "You step cautiously into a narrow cave. " \
    "On your left, a small \033[32mberry\033[0m bush offers ripe, juicy fruits. To your right, a dried thicket crumbles underfoot")
    viridian_Forest_Thicket_Cave.add_object(berry)
    
    
    viridian_Forest_Barren_Field = Room("Viridian Forest Barren Field",
    "A wide, sun-bleached clearing stretches before you, dotted with patches of dry grass and cracked earth. "
    "The wind whispers through the sparse trees at the edges, carrying the faint rustle of distant leaves. "
    "A lone Pokémon \033[32mRanger\033[0m stands near the northern path, looking weary and parched. "
    "You notice \033[32mPikachu\033[0m playfully darting among the sparse tufts of grass, ears twitching at every sound.")
    viridian_Forest_Barren_Field.add_object(ranger)
    viridian_Forest_Barren_Field.add_object(pikachu)
    
    
    Path_To_Pewter_City = Room("Path to Pewter City",
    "A rocky trail winds northward, cutting through low hills and scattered boulders. "
    "The air feels cooler here, carrying the scent of stone and pine. "
    "Tall grass rustles along the edges of the path, and the distant silhouette of Pewter City "
    "can be seen beyond the hills. Trainers often pass through here, preparing themselves "
    "for the challenges that lie ahead.")


    Path_To_Victory_Road = Room("Path to Victory Road",
    "A rocky trail winds upward through jagged cliffs, the wind howling between the stone walls. "
    "Loose gravel crunches beneath your feet as you carefully navigate narrow ledges. "
    "Occasional wild Pokémon can be heard rustling in the nearby underbrush, and the path ahead "
    "seems treacherous yet inviting for those seeking adventure."
    "I wish to return here one day, but right now I need to focus on collecting all the badges.")
    
    
    Pewter_City = Room("Pewter City",
    "Pewter City is a quiet, stone-built town nestled between rugged cliffs. "
    "Gray brick buildings line the streets, giving the city a sturdy, grounded feel. "
    "Trainers wander about with determined expressions, preparing for their first real test. "
    "At the heart of the city stands the Pokémon Gym, its massive stone façade impossible to miss.")


    Poke_center = Room("Poke Center",
    "The Pewter City Pokémon Center is bright and welcoming, a stark contrast to the rugged city outside. "
    "The clean, polished floors gleam under the soft overhead lights, and the gentle hum of conversation fills the air. "
    "\033[32mNurses\033[0m in crisp uniforms tend to Pokémon at the counter, while a warm scent of herbs and clean water creates a calming atmosphere. "
    "Trainers sit on benches, chatting quietly or tending to their Pokémon, and a few Poké Balls rest on tables ready for new adventures. "
    "A large digital display shows the latest Pokémon news, and a map of the city hangs near the entrance, inviting trainers to explore beyond the walls.")
    Poke_center.add_object(nurse)
    
    
    Pewter_City_Gym = Room("Pewter City Gym",
    "The Pewter City Gym is cool and dim, illuminated by light reflecting off towering stone pillars. "
    "The battlefield is carved directly into the rock, rough and unyielding underfoot. "
    "A sense of pressure hangs in the air — \033[32mBrock\033[0m is looking at you unimpressed.")
    Pewter_City_Gym.add_object(brock)


    Road_6 = Room("Road 6",
    "A long, winding path stretches between dense forests and open fields. "
    "The sound of rustling leaves and distant Pokémon cries fills the air, "
    "as trainers and wild Pokémon move through the area. "
    "Patches of tall grass sway with the wind, hiding potential wild encounters, "
    "and the road itself is uneven, with stones and roots threatening to trip the unwary.")


    Rock_Cave = Room(
    "Rock Cave",
    "A narrow, shadowy cave burrows into the hillside, its walls jagged and slick with moisture. "
    "The echo of dripping water resonates through the tunnels, and faint glimmers of light bounce off mineral veins embedded in the stone. "
    "The air is cool and slightly musty, carrying the scent of damp earth and minerals. "
    "Hidden crevices and loose rocks make footing uncertain, and the occasional scuttling sound hints at Pokémon lurking just out of sight." )


    Rock_Cave_2F = Room(
    "Rock Cave - 2nd Floor",
    "You ascend a steep, narrow passage to the cave's upper level. "
    "The walls are rougher here, with jagged stalactites hanging dangerously overhead. "
    "A faint, cold draft snakes through the tunnels, carrying the earthy scent of damp stone and moss. "
    "Small pools of water glimmer in the dim light, reflecting shadows of unseen Pokémon moving in the darkness. "
    "Loose gravel underfoot makes every step precarious, and the sound of distant footsteps echoes eerily through the cavern. "
    "\033[32mVaporeon\033[0m raises its head from the pools of water and steps in gracefully. ")
    Rock_Cave_2F.add_object(vaporeon)

#----------------------------------------------------------------------------------------------------------------------
#                               CONNECT ROOMS
#----------------------------------------------------------------------------------------------------------------------

    bedroom.connect("down", home)
    home.connect("up", bedroom)

    home.connect("east", pallet)
    pallet.connect("west", home)

    pallet.connect("east", lab)
    lab.connect("west", pallet)

    pallet.connect("south", garys_house)
    garys_house.connect("north", pallet)

    pallet.connect("north", viridian_Forest_Area)
    viridian_Forest_Area.connect("south", pallet)

    viridian_Forest_Area.connect("east", viridian_Forest_Pond)
    viridian_Forest_Pond.connect("west", viridian_Forest_Area)

    viridian_Forest_Pond.connect("east", viridian_Forest_Stone_Formation)
    viridian_Forest_Pond.connect("north", viridian_Forest_Farm)

    viridian_Forest_Stone_Formation.connect("west", viridian_Forest_Pond)

    viridian_Forest_Stone_Formation.connect("north", viridian_Forest_Picnic)
    viridian_Forest_Picnic.connect("south", viridian_Forest_Stone_Formation)
    viridian_Forest_Picnic.add_object(crafting_table)

    viridian_Forest_Picnic.connect("west", viridian_Forest_Farm)
    viridian_Forest_Farm.connect("east", viridian_Forest_Picnic)
    viridian_Forest_Farm.connect("south", viridian_Forest_Pond)

    viridian_Forest_Farm.connect("north", viridian_Forest_Thicket_Cave)
    viridian_Forest_Thicket_Cave.connect("south", viridian_Forest_Farm)

    viridian_Forest_Area.connect("west", viridian_Forest_Barren_Field)
    viridian_Forest_Barren_Field.connect("east", viridian_Forest_Area)

    viridian_Forest_Barren_Field.connect(
    "north",
    Path_To_Pewter_City,
    guard=barren_field_north_guard
)
    Path_To_Pewter_City.connect("south", viridian_Forest_Barren_Field)

    Path_To_Pewter_City.connect("west", Path_To_Victory_Road)
    Path_To_Victory_Road.connect("east", Path_To_Pewter_City)

    Path_To_Pewter_City.connect("north", Pewter_City)
    Pewter_City.connect("south", Path_To_Pewter_City)

    Pewter_City.connect("north", Poke_center)
    Poke_center.connect("south", Pewter_City)

    Pewter_City.connect("west", Pewter_City_Gym)
    Pewter_City_Gym.connect("east", Pewter_City)

    Pewter_City.connect("east", Road_6)
    Road_6.connect("west", Pewter_City)

    Road_6.connect("north", Rock_Cave)
    Rock_Cave.connect("south", Road_6)

    Rock_Cave.connect("north", Rock_Cave_2F)
    Rock_Cave_2F.connect("south", Rock_Cave)


#----------------------------------------------------------------------------------------------------------------------
#                               STARTING POINT
#----------------------------------------------------------------------------------------------------------------------
#   def build_world is called with:
#       def main():
#       starting_room = build_world()

    return bedroom
    
