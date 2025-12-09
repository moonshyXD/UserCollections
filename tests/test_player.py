from entities.chip import Chip
from entities.player import Player


class TestPlayer:
    def test_init(self):
        player = Player("Player", 100)
        assert player.name == "Player"
        assert isinstance(player.balance, Chip)
        assert player.balance.value == 100

    def test_repr(self):
        player = Player("Player", 50)
        assert repr(player) == "(имя=Player, баланс=50)"
