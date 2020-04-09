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
        if not name:
            name = color
        number = len(Player.players) + 2
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
