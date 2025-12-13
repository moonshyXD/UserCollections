from typing import Any

import pytest

from src.adapters.logger import Logger
from src.controllers.casino import Casino
from src.entities.errors import EntitiesError
from src.entities.player import Player
from src.usecases.freebet import Freebet


class TestFreeBet:
    def test_freebet_no_players_raises(self) -> None:
        """
        Проверяет ошибку при бесплатной ставке без игроков
        """
        casino = Casino()
        logger = Logger()
        with pytest.raises(EntitiesError):
            Freebet.execute(casino, logger)

    def test_freebet_success(self, capsys: Any) -> None:
        """
        Проверяет успешную бесплатную ставку
        """
        casino = Casino()
        logger = Logger()
        player = Player("PeterZhabin", 100)
        casino.register_player(player)
        casino._set_seed(20)
        Freebet.execute(casino, logger)
        assert casino._players_balance["PeterZhabin"].value == 150
        assert len(casino._chips_history) == 1
