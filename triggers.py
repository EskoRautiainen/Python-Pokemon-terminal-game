from game_objects import Item

#   Triggers are functions that modify the game state.
#   give_potion is executed automatically when an NPC dialogue line includes this trigger.
#   The NPC.talk(player) method calls the trigger when the corresponding dialogue entry is reached.


def give_potion(player):
    potion = Item("potion", "A basic healing spray used for Pokémon.")
    player.inventory.append(potion)
    print("Mom gave you a Potion!")