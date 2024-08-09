
class GameBase:
    def __init__(self, level: int = 0, name: str = "", amount_attempted: float = 0):
        self.level: int = level
        self.name: str = name
        self.amount_attempted: float = amount_attempted
