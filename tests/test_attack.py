from typing import Any

import pytest

from src.adapters.logger import Logger
from src.controllers.casino import Casino
from src.entities.errors import EntitiesError
from src.entities.goose import HonkGoose, WarGoose
from src.entities.player import Player
from src.usecases.attack import Attack


class TestAttack:
    def test_attack_no_players_raises(self) -> None:
        """
        Проверяет ошибку при атаке без игроков
        """
        casino = Casino()
        logger = Logger()
        goose = WarGoose("PeterZhabin", 30)
        casino.register_goose(goose)
        with pytest.raises(EntitiesError):
            Attack.execute(casino, logger)

    def test_attack_no_war_geese_raises(self) -> None:
        """
        Проверяет ошибку при атаке без боевых гусей
        """
        casino = Casino()
        logger = Logger()
        player = Player("PeterZhabin", 100)
        goose = HonkGoose("SamirAhmed", 20)
        casino.register_player(player)
        casino.register_goose(goose)
        with pytest.raises(EntitiesError):
            Attack.execute(casino, logger)

    def test_attack_success(self, capsys: Any) -> None:
        """
        Проверяет успешную атаку
        """
        casino = Casino()
        logger = Logger()
        player = Player("PeterZhabin", 100)
        goose = WarGoose("SamirAhmed", 50)
        casino.register_player(player)
        casino.register_goose(goose)
        casino._set_seed(42)
        Attack.execute(casino, logger)
        assert len(casino._chips_history) == 1
        assert casino._players_balance["PeterZhabin"].value <= 100
