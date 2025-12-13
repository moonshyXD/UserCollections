from typing import Any

import pytest

from src.adapters.logger import Logger
from src.controllers.casino import Casino
from src.entities.errors import EntitiesError
from src.entities.player import Player
from src.usecases.fruit_party import FruitParty


class TestFruitParty:
    def test_fruit_party_no_players_raises(self) -> None:
        """
        Проверяет ошибку при Fruit Party без игроков
        """
        casino = Casino()
        logger = Logger()
        with pytest.raises(EntitiesError):
            FruitParty.execute(casino, logger)

    def test_fruit_party_success(self, capsys: Any) -> None:
        """
        Проверяет успешный Fruit Party
        """
        casino = Casino()
        logger = Logger()
        player = Player("PeterZhabin", 100)
        casino.register_player(player)
        casino._set_seed(25)
        FruitParty.execute(casino, logger)
        assert casino._players_balance["PeterZhabin"].value == 0
        assert len(casino._chips_history) == 1
