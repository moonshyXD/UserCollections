from typing import Any

import pytest

from src.adapters.logger import Logger
from src.controllers.casino import Casino
from src.entities.errors import EntitiesError
from src.entities.goose import HonkGoose
from src.entities.player import Player
from src.usecases.sabotage import Sabotage


class TestSabotage:
    def test_sabotage_no_players_raises(self) -> None:
        """
        Проверяет ошибку при саботаже без игроков
        """
        casino = Casino()
        logger = Logger()
        goose = HonkGoose("SamirAhmed", 20)
        casino.register_goose(goose)
        with pytest.raises(EntitiesError):
            Sabotage.execute(casino, logger)

    def test_sabotage_no_geese_raises(self) -> None:
        """
        Проверяет ошибку при саботаже без гусей
        """
        casino = Casino()
        logger = Logger()
        player = Player("PeterZhabin", 100)
        casino.register_player(player)
        with pytest.raises(EntitiesError):
            Sabotage.execute(casino, logger)

    def test_sabotage_success(self, capsys: Any) -> None:
        """
        Проверяет успешный саботаж
        """
        casino = Casino()
        logger = Logger()
        p1 = Player("PeterZhabin1", 100)
        p2 = Player("PeterZhabin2", 200)
        goose = HonkGoose("SamirAhmed", 30)
        casino.register_player(p1)
        casino.register_player(p2)
        casino.register_goose(goose)
        casino._set_seed(15)
        Sabotage.execute(casino, logger)
        assert len(casino._player_collection) == 2
