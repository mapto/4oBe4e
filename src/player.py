from typing import Set, Any

colors = set(
    [
        "RED",
        "BLUE",
        "GREEN",
        "YELLOW",
        "CYAN",
        "MAGENTA",
        "LIGHTBLACK_EX",
        "LIGHTBLUE_EX",
        "LIGHTCYAN_EX",
        "LIGHTGREEN_EX",
        "LIGHTMAGENTA_EX",
        "LIGHTRED_EX",
        "LIGHTWHITE_EX",
        "LIGHTYELLOW_EX",
    ]
)


class Player:
    players: Set["Player"] = set()

    @staticmethod
    def create(color: str = None, name: str = None) -> "Player":

        if not color:
            if len(Player.players) == len(colors):
                raise PermissionError(
                    "Console interface cannot assign any more colours"
                )
            color = colors.difference([p.color for p in Player.players]).pop()
        number = len(Player.players)
        if not name:
            name = "Player {:d}".format(number + 1)
        player = Player(number, name, color)
        Player.players.add(player)

        return player

    @staticmethod
    def get(num: int) -> "Player":
        return [p for p in Player.players if p.number == num].pop()

    def __init__(self, number: int, name: str, color: str):
        self.number = number
        self.name = name
        self.color = color

    def __str__(self):
        return str(self.number)

    def __format__(self, format):
        if format == "s":
            return self.name
        if format == "d":
            return self.number
        return str(self)

    def __repr__(self):
        return str(self.number)

    def __eq__(self, other):
        if isinstance(other, Player):
            return self.name == other.name and self.number == other.number
        return False

    def __hash__(self):
        return hash((self.name, self.number))
