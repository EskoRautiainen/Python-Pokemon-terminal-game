# game_objects.py defines the types of objects that can exist in the world
# GameObjects is the base class, while Item and NPC are subclasses of it.
# takeable and talkable are boolean values that define object rules.
# You can't talk to a rock or put Professor Oak in your inventory.


#----------------------------------------------------------------------------------------------------------------------
#                               GAME_OBJECT CLASS
#----------------------------------------------------------------------------------------------------------------------
class GameObject:
    def __init__(self, name, description, takeable=False, talkable=False):
        self.name = name.lower()
        self.description = description
        self.takeable = takeable
        self.talkable = talkable

# Used to examine items. Prints out items self.description.
    def inspect(self):
        return self.description


# Defines default behaviour for talking to a GameObject.
    def talk(self, player=None):
        return "They don't respond."

#----------------------------------------------------------------------------------------------------------------------
#                               GAME_OBJECT SUBCLASSES
#----------------------------------------------------------------------------------------------------------------------

# Item is a subclass of GameObject. It inherits all attributes and methods from GameObject.
# Item subclass overrides parent class takeable boolean setting.
# All Items are takeable, while all HeavyItems are not takeable, but you can apply triggers to them.

class Item(GameObject):
    def __init__(self, name, description):
        super().__init__(name, description, takeable=True)

class HeavyItem(GameObject):
    def __init__(self, name, description, triggers=None):
        super().__init__(name, description, takeable=False)
        self.triggers = triggers or {}

    def trigger_action(self, action, player=None):
        if action in self.triggers and callable(self.triggers[action]):
            self.triggers[action](player)
        else:
            print(f"You {action} the {self.name}, but nothing happens.")






class NPC(GameObject):
    def __init__(self, name, description, dialogues=None, repeatable=True):
        super().__init__(name, description, talkable=True)
        self.dialogues = dialogues or [("Hello.", None)]
        self.dialog_index = 0
        self.repeatable = repeatable

    def talk(self, player=None):
        if not self.dialogues:
            return "They have nothing more to say."

        if self.dialog_index >= len(self.dialogues):
            if self.repeatable:
                self.dialog_index = 0
            else:
                self.dialog_index = len(self.dialogues) - 1

        line, trigger = self.dialogues[self.dialog_index]
        if callable(trigger):
            trigger(player)
            # remove trigger so it triggers only once
            self.dialogues[self.dialog_index] = (line, None)

        self.dialog_index += 1
        return line
