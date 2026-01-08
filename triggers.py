from game_objects import HeavyItem, Item, Pokemon, Move
import time

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
    print("Mom gave you a \033[32mPotion\033[0m!")

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
            break
        else:
            print("Invalid choice. Please type Bulbasaur, Squirtle, or Charmander.")

#----------------------------------------------------------------------------------------------------------------------
#                               TRIGGERS - VIRIDIAN_FOREST_AREA
#----------------------------------------------------------------------------------------------------------------------

# Spawn Pokemon after using Apply Force Command on a tree.
def tree_hit_trigger(player):
    caterpie = Pokemon(
        "Caterpie",
        "Bug",
        45,
        moves=[Move("Tackle", "Normal"), Move("String shot", "Bug")]
    )
    player.current_room.add_object(caterpie)
    print("A wild \033[32mCaterpie\033[0m fell from the tree!")

    # Update room description
    player.current_room.description = "\033[32mCaterpie\033[0m shakes dust and leaves from its tiny body, looking surprisingly fierce and expressive for such a small bug."


# -----------------------------------------------------------------
# Example commands: "hit tree", "kick rock"
def apply_force_handler(player, command):
    parts = command.split()
    if len(parts) < 2:
        print("Apply force to what?")
        return

    verb = parts[0]  # The action: hit, kick, etc.
    target_name = " ".join(parts[1:]).strip().lower()  # everything after the verb

    # Look for objects in the current room
    for obj in player.current_room.objects:
        if obj.name.lower() == target_name:
            # If the object has trigger_action, use it
            if hasattr(obj, "trigger_action") and callable(obj.trigger_action):
                obj.trigger_action(verb, player)
                return
            # Default message if object has no trigger
            print(f"You {verb} the {obj.name}, but nothing happens.")
            return

    print(f"You don't see a {target_name} here.")

#----------------------------------------------------------------------------------------------------------------------
#                               TRIGGERS - VIRIDIAN_FOREST_POND
#----------------------------------------------------------------------------------------------------------------------

# -----------------------------------------------------------------
# Allows you to drop items
def drop_handler(player, command):
    parts = command.split()
    if len(parts) < 2:
        print("Drop what?")
        return

    target_name = " ".join(parts[1:]).strip().lower()
    item = next((i for i in player.inventory if i.name.lower() == target_name), None)

    if not item:
        print("You don't have that.")
        return

    player.inventory.remove(item)
    player.current_room.add_object(item)
    print(f"You dropped the {item.name}.")

    # Check if it’s the pond bait
    poliwag = next((p for p in player.current_room.objects if isinstance(p, Pokemon) and p.name.lower() == "poliwag"), None)
    if poliwag and item.name.lower() == "bait":
        poliwag.pond_puzzle.bait_dropped = True
        print("wait...")

        for i in range(3, 0, -1):
            print(i)
            time.sleep(1)

        print("Poliwag took the bait!")



# -----------------------------------------------------------------
def pull_handler(player, command):
    parts = command.split()
    if len(parts) < 2:
        print("Pull what?")
        return

    target_name = " ".join(parts[1:]).strip().lower()

    # --------------------------
    # 1. Try to find the object in the room
    # --------------------------
    target_obj = next(
        (obj for obj in player.current_room.objects if obj.name.lower() == target_name),
        None
    )

    if not target_obj:
        print("Nothing happens.")
        return

    # --------------------------
    # 2. Call the object's "pull" trigger if it exists
    # --------------------------
    if hasattr(target_obj, "triggers") and "pull" in target_obj.triggers:
        target_obj.triggers["pull"](player)
        return

    # --------------------------
    # 3. Pokémon-specific interactions
    # --------------------------
    if isinstance(target_obj, Pokemon):
        if target_obj.name.lower() == "sandshrew":
            print("Sandshrew wriggles furiously but it's stuck. You can't pull it out!")
            return
        # Add more Pokémon here if needed

    # --------------------------
    # 4. Poliwag pond puzzle fallback
    # --------------------------
    bait = next((i for i in player.current_room.objects if i.name.lower() == "bait"), None)
    if not bait:
        print("Nothing happens.")
        return

    poliwag = next((p for p in player.current_room.objects
                    if isinstance(p, Pokemon) and p.name.lower() == "poliwag"), None)
    if not poliwag:
        print("Nothing happens.")
        return

    if getattr(poliwag, "pond_puzzle", None) and getattr(poliwag.pond_puzzle, "catchable", False):
        print("Nothing happens.")
        return

    poliwag.pond_puzzle.catchable = True
    print("Poliwag fell on its face! Now you can capture it.")


#----------------------------------------------------------------------------------------------------------------------
#                               TRIGGERS - VIRIDIAN_FOREST_FARM
#----------------------------------------------------------------------------------------------------------------------

def water_crops_trigger(player):
    # Check if player has watering can
    watering_can = next((i for i in player.inventory if i.name.lower() == "watering can"), None)
    if not watering_can:
        print("You need a watering can to water the crops.")
        return

    # Water crops
    print("You water the crops. Slowly, the wilted plants regain their color and vitality.")
    
    # Update room description
    player.current_room.description = (
        "The small farm now looks lively. The once-wilted crops have been revived, "
        "glimmering under the sun. The elderly couple smiles gratefully at you."
    )

    # Reward player with lemonade
    lemonade = Item("lemonade", "A refreshing drink made from fresh lemons grown on the farm.")
    player.inventory.append(lemonade)
    print("The elderly couple thanks you and gives you some \033[32mLemonade\033[0m!")


def handle_use(player, command):
    parts = command.split()
    if len(parts) < 2:
        print("Use what?")
        return

    target_name = " ".join(parts[1:]).strip().lower()

    # Look for object in room first, then inventory
    target = next((o for o in player.current_room.objects if o.name.lower() == target_name), None)
    if not target:
        target = next((o for o in player.inventory if o.name.lower() == target_name), None)
    if not target:
        print(f"You don't see a {target_name} here or in your inventory.")
        return

    # Call trigger_action with proper action
    if hasattr(target, "trigger_action") and callable(target.trigger_action):
        # Use "water" for crops, "use" for other objects
        action = "water" if target.name.lower() == "crops" else "use"
        target.trigger_action(action, player)
        return

    print(f"You try to use the {target.name}, but nothing happens.")


def water_handler(player, action=None):
    # Find crops in the room
    crops = next((obj for obj in player.current_room.objects if obj.name.lower() == "crops"), None)
    if not crops:
        print("There are no crops here to water.")
        return

    # Check if already watered
    if getattr(crops, "watered", False):
        print("The crops are already watered. The elderly couple smiles at you.")
        return

    # Check if player has watering can
    watering_can = next((i for i in player.inventory if i.name.lower() == "watering can"), None)
    if not watering_can:
        print("You need a watering can to water the crops.")
        return

    # Water crops
    print("You water the crops. Slowly, the wilted plants regain their color and vitality.")
    
    # Update room description
    player.current_room.description = (
        "The small farm now looks lively. The once-wilted crops have been revived, "
        "glimmering under the sun. The elderly couple smiles gratefully at you."
    )

    # Reward player with lemonade
    lemonade = Item("lemonade", "A refreshing drink made from fresh lemons grown on the farm.")
    player.inventory.append(lemonade)
    print("The elderly couple thanks you and gives you some \033[32mLemonade\033[0m!")

    # Set crops as watered
    crops.watered = True





#----------------------------------------------------------------------------------------------------------------------
#                               TRIGGERS - VIRIDIAN_FOREST_STONE_FORMATION
#----------------------------------------------------------------------------------------------------------------------

def pull_sandshrew_trigger(player):
    """
    Trigger for pulling the stuck Sandshrew.
    Removes the HeavyItem and spawns the Pokémon for capture.
    """
    # Find the sandshrew in the room
    sandshrew = next((obj for obj in player.current_room.objects
                      if obj.name.lower() == "sandshrew"), None)
    if not sandshrew:
        print("You can't pull that here.")
        return

    print("You pull the Sandshrew out with effort. It slides free from the ground!")
    
    # Remove the HeavyItem
    player.current_room.objects.remove(sandshrew)

    # Add the Pokémon
    sandshrew = Pokemon(
        "Sandshrew",
        "Ground",
        40,
        moves=[Move("Scratch", "Normal"), Move("Sand Attack", "Ground")]
    )
    player.current_room.add_object(sandshrew)
    
    # Update room description
    player.current_room.description = (
        "You enter a strange area where jagged stones rise from the forest floor like ancient monuments. "
        "The air is cooler here, and the sunlight filters through the cracks in the stones, casting strange shadows. "
        "The ground is now clear, and \033[32mSandshrew\033[0m! happily scurries around the forest floor, free from being stuck."
    )


#----------------------------------------------------------------------------------------------------------------------
#                               TRIGGERS - VIRIDIAN_FOREST_PICNIC_AREA
#----------------------------------------------------------------------------------------------------------------------

def crafting_table_trigger(player):
    print("You approach the crafting table.")
    
    if len(player.inventory) < 2:
        print("You need at least two items to try crafting.")
        return
    
    print("Which items will be combined? (Type in format: item1 + item2)")
    choice = input("> ").strip().lower()
    
    if "+" not in choice:
        print("Invalid format. Use 'item1 + item2'.")
        return
    
    item1_name, item2_name = [x.strip() for x in choice.split("+")]
    
    # Search inventory for items
    item1 = next((i for i in player.inventory if i.name.lower() == item1_name), None)
    item2 = next((i for i in player.inventory if i.name.lower() == item2_name), None)
    
    if not item1 or not item2:
        print("You don't have those items.")
        return
    
    # Define successful combination
    if {item1.name, item2.name} == {"rope", "berry"}:
        # Remove the original items
        player.inventory.remove(item1)
        player.inventory.remove(item2)
        # Add new item
        bait = Item("bait", "A makeshift bait made from rope and berries. Can be used to catch wild Pokémon.")
        player.inventory.append(bait)
        print("Success! You created BAIT.")
    else:
        print("Those items cannot be combined.")




def rope_trigger(player):
    rope = next((obj for obj in player.current_room.objects if obj.name == "rope"), None)
    if not rope:
        return False  # Nothing happened

    growlithe_present = any(isinstance(obj, Pokemon) and obj.name.lower() == "growlithe"
                            for obj in player.current_room.objects)
    growlithe_caught = any(p.name.lower() == "growlithe" for p in player.party)

    if growlithe_caught:
        unlock_rope(player)
        return True

    if not growlithe_present:
        growlithe = Pokemon(
            "Growlithe",
            "Fire",
            50,
            moves=[Move("Bite", "Normal"), Move("Flame Wheel", "Fire")]
        )
        player.current_room.add_object(growlithe)
        print("A wild \033[32mGrowlithe\033[0m appeared!")
        print("\033[32mGrowlithe\033[0m has latched onto the rope, tugging back with impressive strength.")
        return True
    else:
        print("\033[32mGrowlithe\033[0m has latched onto the rope, tugging back with impressive strength.")
        return True

# Create Rope as HeavyItem with trigger
rope = HeavyItem(
    "rope",
    "A sturdy piece of rope.",
    triggers={"take": rope_trigger}
)

# Function to convert rope into pickable Item when Growlithe is caught
def unlock_rope(player):
    # Find rope in the room
    rope_obj = next((obj for obj in player.current_room.objects if obj.name == "rope"), None)
    if rope_obj:
        # Replace HeavyItem with normal Item
        player.current_room.objects.remove(rope_obj)
        pickable_rope = Item("rope", "A sturdy piece of rope. Now you can pick it up.")
        player.current_room.add_object(pickable_rope)
        print("With \033[32mGrowlithe\033[0m caught, the rope is now safe to pick up!")


#----------------------------------------------------------------------------------------------------------------------
#                               TRIGGERS - PEWTER-CITY-GYM
#----------------------------------------------------------------------------------------------------------------------

def brock_battle(player, command=None):
    # Check if player has enough Pokémon
    if len(player.party) < 0:
        print("Brock: You need at least 2 Pokémon to challenge me!")
        return False  # block battle

    # Brock's Pokémon: Onix
    onix = Pokemon("Onix", "Rock", 120, moves=[
        Move("Rock Throw", "Rock"),
        Move("Tackle", "Normal")
    ])
    print(f"Brock: Onix, let's battle!")
    print(f"Onix HP: {onix.health}")

    # Battle loop
    while onix.health > 0 and any(p.health > 0 for p in player.party):
        # Select first available Pokémon in the party
        active_pokemon = next((p for p in player.party if p.health > 0), None)
        if not active_pokemon:
            print("All your Pokémon have fainted! Brock wins!")
            return False

        # Player attack
        print(f"\nYour turn! {active_pokemon.name}'s moves:")
        for i, move in enumerate(active_pokemon.moves):
            print(f"{i+1}. {move.name} ({move.type})")
        print(f"{active_pokemon.name} has {active_pokemon.health} HP")
        choice = input("Choose a move number: ")

        try:
            move_index = int(choice) - 1
            move = active_pokemon.moves[move_index]
        except (ValueError, IndexError):
            print("Invalid choice, using default attack.")
            move = active_pokemon.moves[0]

        # Calculate damage
        if move.type.lower() in ["water", "grass", "nature"]:
            damage = 20  # double damage to Rock
            print(f"{active_pokemon.name} used {move.name}! It's super effective! (-20 HP)")
        else:
            damage = 10
            print(f"{active_pokemon.name} used {move.name}! (-10 HP)")

        onix.health -= damage
        if onix.health <= 0:
            print("Onix fainted! You won the battle!")

            # Give the player the Boulder Badge
            boulder_badge = Item("Boulder Badge", "Awarded for defeating Brock, the Pewter City Gym Leader.")
            player.inventory.append(boulder_badge)
            print("You received the Boulder Badge! It has been added to your inventory.")
            
            return True
        else:
            print(f"Onix HP: {onix.health}")

        # Onix counterattack
        onix_move = onix.moves[0]  # simple AI: first move
        print(f"Onix used {onix_move.name}! (-40 HP)")
        active_pokemon.health -= 40
        if active_pokemon.health <= 0:
            print(f"{active_pokemon.name} fainted!")

    print("")
    print("Battle ended.")
    print("Ash whited out.")




