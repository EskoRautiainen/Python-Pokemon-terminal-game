#----------------------------------------------------------------------------------------------------------------------
#                               GAMEOBJECT
#----------------------------------------------------------------------------------------------------------------------

class GameObject:
    def __init__(self, name, description, takeable=False, talkable=False):
        self.name = name.lower()
        self.description = description
        self.takeable = takeable
        self.talkable = talkable

    def inspect(self):
        return self.description

    def talk(self, player=None):
        return "They don't respond."


#----------------------------------------------------------------------------------------------------------------------
#                               GAMEOBJECT - SUBCLASSES
#----------------------------------------------------------------------------------------------------------------------

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


#----------------------------------------------------------------------------------------------------------------------
#                               MOVE CLASS
#----------------------------------------------------------------------------------------------------------------------
class Move:
    def __init__(self, name, type_):
        self.name = name
        self.type = type_

    def __str__(self):
        return f"{self.name} ({self.type})"


#----------------------------------------------------------------------------------------------------------------------
#                               POKEMON CLASS
#----------------------------------------------------------------------------------------------------------------------
class Pokemon:
    def __init__(self, name, type_, health=50, moves=None):
        self.name = name
        self.type = type_
        self.health = health
        self.moves = moves or []

        # Optional puzzle/state hook (used for special cases like Poliwag pond)
        self.pond_puzzle = None  

    def __str__(self):
        moves_list = ", ".join(str(move) for move in self.moves) if self.moves else "No moves"
        return f"{self.name} ({self.type}) - HP: {self.health} | Moves: {moves_list}"


#----------------------------------------------------------------------------------------------------------------------
#                               POLIWAG POND PUZZLE
#----------------------------------------------------------------------------------------------------------------------
class PoliwagPondPuzzle:
    def __init__(self):
        self.bait_dropped = False
        self.counter = 0
        self.rope_pulled = False
        self.catchable = False



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
            self.dialogues[self.dialog_index] = (line, None)

        self.dialog_index += 1
        return line
