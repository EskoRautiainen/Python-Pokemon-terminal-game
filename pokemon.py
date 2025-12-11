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
    def __init__(self, name, type_, health=100, moves=None):
        self.name = name
        self.type = type_
        self.health = health
        self.moves = moves or []

    def __str__(self):
        moves_list = ", ".join(str(move) for move in self.moves) if self.moves else "No moves"
        return f"{self.name} ({self.type}) - HP: {self.health} | Moves: {moves_list}"