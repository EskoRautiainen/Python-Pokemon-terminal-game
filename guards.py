def barren_field_north_guard(player):
    has_juice = any(item.name == "lemonade" for item in player.inventory)

    # Find ranger
    ranger = next(
        (obj for obj in player.current_room.objects if obj.name == "ranger"),
        None
    )

    if not has_juice:
        if ranger:
            print("Ranger: Sorry, kid. I can’t let you pass without something to drink.")
        return False

    # Player has lemonade
    if ranger:
        print("Ranger: Ahhh… Lemonade!")
        print("Ranger: Go on ahead. I’ll hold the fort.")

        ranger.dialogues = [
            ("Thanks again for the drink.", None),
            ("The road ahead won’t be easy.", None),
        ]

    player.current_room.description = (
        "The ranger steps aside, clearing the northern path."
    )

    return True
