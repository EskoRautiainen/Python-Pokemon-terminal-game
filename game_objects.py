#   game_objects.py defines the types of objects that can exist in the world
#   GameObjects is the base class, while Item and NPC are subclasses of it.
#   takeable and talkable are boolean values that define object rules.
#   You can't talk to a rock or put Professor Oak in your inventory.

class GameObject:
    def __init__(self, name, description, takeable=False, talkable=False):
        self.name = name.lower()
        self.description = description
        self.takeable = takeable
        self.talkable = talkable

#   Used to examine items. Prints out items self.description.

    def inspect(self):
        return self.description


#   Defines default behaviour for talking to a GameObject.

    def talk(self, player=None):
        return "They don't respond."

#   Item is a subclass of GameObject. It inherits all attributes and methods from GameObject.
#   Item subclass overrides parent class takeable boolean setting.

class Item(GameObject):
    def __init__(self, name, description):
        super().__init__(name, description, takeable=True)



class NPC(GameObject):
    def __init__(self, name, description, dialogues=None, repeatable=True):
        super().__init__(name, description, talkable=True)
        # dialogues: list of tuples (line:str, trigger:callable or None)
        self.dialogues = dialogues or [("Hello.", None)]
        self.dialog_index = 0
        self.repeatable = repeatable

    def talk(self, player=None):
        if not self.dialogues:
            return "They have nothing more to say."

        # Get the current dialogue
        line, trigger = self.dialogues[self.dialog_index]

        # Run trigger if it exists
        if callable(trigger):
            trigger(player)
            # Remove trigger so it only happens once
            self.dialogues[self.dialog_index] = (line, None)

        # Advance dialogue index
        self.dialog_index += 1

        if self.repeatable:
            # Loop around if repeatable
            self.dialog_index %= len(self.dialogues)
        else:
            # Stop at last dialogue
            if self.dialog_index >= len(self.dialogues):
                self.dialog_index = len(self.dialogues) - 1

        return line

    
# PROBLEM: NPC NEEDS ADDITIONAL COMMENTS.
