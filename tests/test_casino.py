from typing import Any

from src.controllers.casino import Casino
from src.entities.goose import HonkGoose, WarGoose
from src.entities.player import Player


class TestCasino:
    def test_init(self) -> None:
        """
        Проверяет создание пустого казино
        """
        casino = Casino()
        assert len(casino._player_collection) == 0
        assert len(casino._goose_collection) == 0

    def test_register_player(self) -> None:
        """
        Проверяет регистрацию игрока в казино
        """
        casino = Casino()
        player = Player("PeterZhabin", 100)
        casino.register_player(player)
        assert len(casino._player_collection) == 1
        assert casino._players_balance["PeterZhabin"].value == 100

    def test_register_goose(self) -> None:
        """
        Проверяет регистрацию гуся в казино
        """
        casino = Casino()
        goose = HonkGoose("PeterZhabin", 50)
        casino.register_goose(goose)
        assert len(casino._goose_collection) == 1
        assert casino._geese_balance["PeterZhabin"].value == 0

    def test_iter_players(self) -> None:
        """
        Проверяет итерацию по игрокам казино
        """
        casino = Casino()
        p1 = Player("PeterZhabin", 50)
        p2 = Player("SamirAhmed", 100)
        casino.register_player(p1)
        casino.register_player(p2)
        players = list(casino)
        assert players == [p1, p2]

    def test_set_seed(self) -> None:
        """
        Проверяет установку seed для генератора случайных чисел
        """
        casino = Casino()
        casino._set_seed(42)

    def test_run_simulation_with_seed(self, capsys: Any) -> None:
        """
        Проверяет запуск симуляции с заданным seed
        """
        casino = Casino()
        p = Player("PeterZhabin", 100)
        g = WarGoose("SamirAhmed", 30)
        casino.register_player(p)
        casino.register_goose(g)
        casino.run_simulation(steps=3, seed=50)

    def test_run_simulation_without_seed(self, capsys: Any) -> None:
        """
        Проверяет запуск симуляции без seed
        """
        casino = Casino()
        p = Player("PeterZhabin", 100)
        g = HonkGoose("SamirAhmed", 30)
        casino.register_player(p)
        casino.register_goose(g)
        casino.run_simulation(steps=2)

    def test_run_simulation_handles_errors(self, capsys: Any) -> None:
        """
        Проверяет обработку ошибок в симуляции
        """
        casino = Casino()
        casino.run_simulation(steps=2, seed=60)
