from typing import Any

import pytest

from src.adapters.logger import Logger
from src.controllers.casino import Casino
from src.entities.errors import EntitiesError
from src.entities.goose import HonkGoose, WarGoose
from src.entities.player import Player
from src.usecases.flock_steal import FlockSteal


class TestFlockSteal:
    def test_flock_steal_no_players_raises(self) -> None:
        """
        Проверяет ошибку при краже стаей без игроков
        """
        casino = Casino()
        logger = Logger()
        goose = WarGoose("PeterZhabin", 30)
        casino.register_goose(goose)
        with pytest.raises(EntitiesError):
            FlockSteal.execute(casino, logger)

    def test_flock_steal_no_war_geese_raises(self) -> None:
        """
        Проверяет ошибку при краже стаей без боевых гусей
        """
        casino = Casino()
        logger = Logger()
        player = Player("PeterZhabin", 100)
        goose = HonkGoose("SamirAhmed", 30)
        casino.register_player(player)
        casino.register_goose(goose)
        with pytest.raises(EntitiesError):
            FlockSteal.execute(casino, logger)

    def test_flock_steal_success(self, capsys: Any) -> None:
        """
        Проверяет успешную кражу стаей
        """
        casino = Casino()
        logger = Logger()
        player = Player("PeterZhabin", 100)
        g1 = WarGoose("SamirAhmed1", 30)
        g2 = WarGoose("SamirAhmed2", 40)
        casino.register_player(player)
        casino.register_goose(g1)
        casino.register_goose(g2)
        casino._set_seed(30)
        FlockSteal.execute(casino, logger)
        assert casino._players_balance["PeterZhabin"].value <= 100

    def test_flock_steal_player_has_zero_balance(self, capsys: Any) -> None:
        """
        Проверяет кражу стаей когда у игрока нет фишек
        """
        casino = Casino()
        logger = Logger()
        player = Player("PeterZhabin", 0)
        goose = WarGoose("SamirAhmed", 30)
        casino.register_player(player)
        casino.register_goose(goose)
        casino._set_seed(35)
        FlockSteal.execute(casino, logger)
        assert casino._players_balance["PeterZhabin"].value == 0
