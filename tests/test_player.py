from entities.chip import Chip
from entities.player import Player


class TestPlayer:
    def test_init(self) -> None:
        """
        Проверить создание игрока с именем и балансомs
        """
        player = Player("Peter Zhabin", 100)
        assert player.name == "Peter Zhabin"
        assert isinstance(player.balance, Chip)
        assert player.balance.value == 100

    def test_name_property(self) -> None:
        """
        Проверить получение имени игрока
        """
        player = Player("Peter Zhabin", 50)
        assert player.name == "Peter Zhabin"

    def test_balance_property(self) -> None:
        """
        Проверить получение баланса игрока
        """
        player = Player("Peter Zhabin", 200)
        assert player.balance.value == 200

    def test_repr(self) -> None:
        """
        Проверить строковое представление игрока
        """
        player = Player("Peter Zhabin", 75)
        assert repr(player) == "Игрок: Peter Zhabin Баланс: 75"
