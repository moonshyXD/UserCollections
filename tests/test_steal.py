from typing import Any

import pytest

from src.adapters.logger import Logger
from src.controllers.casino import Casino
from src.entities.errors import EntitiesError
from src.entities.goose import HonkGoose
from src.entities.player import Player
from src.usecases.steal import Steal


class TestSteal:
    def test_steal_no_players_raises(self) -> None:
        """
        Проверяет ошибку при краже без игроков
        """
        casino = Casino()
        logger = Logger()
        goose = HonkGoose("PeterZhabin", 20)
        casino.register_goose(goose)
        with pytest.raises(EntitiesError):
            Steal.execute(casino, logger)

    def test_steal_no_geese_raises(self) -> None:
        """
        Проверяет ошибку при краже без гусей
        """
        casino = Casino()
        logger = Logger()
        player = Player("SamirAhmed", 100)
        casino.register_player(player)
        with pytest.raises(EntitiesError):
            Steal.execute(casino, logger)

    def test_steal_success(self, capsys: Any) -> None:
        """
        Проверяет успешную кражу фишек
        """
        casino = Casino()
        logger = Logger()
        player = Player("PeterZhabin", 100)
        goose = HonkGoose("SamirAhmed", 30)
        casino.register_player(player)
        casino.register_goose(goose)
        casino._set_seed(5)
        Steal.execute(casino, logger)
        assert len(casino._chips_history) == 1
