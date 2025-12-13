from typing import Any

import pytest

from src.adapters.logger import Logger
from src.controllers.casino import Casino
from src.entities.errors import EntitiesError
from src.entities.player import Player
from src.usecases.bet import Bet


class TestBet:
    def test_bet_no_players_raises(self) -> None:
        """
        Проверяет ошибку при ставке без игроков
        """
        casino = Casino()
        logger = Logger()
        with pytest.raises(EntitiesError):
            Bet.execute(casino, logger)

    def test_bet_success(self, capsys: Any) -> None:
        """
        Проверяет успешную ставку
        """
        casino = Casino()
        logger = Logger()
        player = Player("PeterZhabin", 100)
        casino.register_player(player)
        casino._set_seed(10)
        Bet.execute(casino, logger)
        assert len(casino._chips_history) == 1
