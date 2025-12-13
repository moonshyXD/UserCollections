from typing import Any

import pytest

from src.adapters.logger import Logger
from src.controllers.casino import Casino
from src.entities.errors import EntitiesError
from src.entities.goose import HonkGoose
from src.entities.player import Player
from src.usecases.honk import Honk


class TestHonk:
    def test_honk_no_geese_raises(self) -> None:
        """
        Проверяет ошибку при крике без гусей
        """
        casino = Casino()
        logger = Logger()
        player = Player("PeterZhabin", 100)
        casino.register_player(player)
        with pytest.raises(EntitiesError):
            Honk.execute(casino, logger)

    def test_honk_no_players_raises(self) -> None:
        """
        Проверяет ошибку при крике без игроков
        """
        casino = Casino()
        logger = Logger()
        goose = HonkGoose("PeterZhabin", 30)
        casino.register_goose(goose)
        with pytest.raises(EntitiesError):
            Honk.execute(casino, logger)

    def test_honk_low_volume(self, capsys: Any) -> None:
        """
        Проверяет крик гуся с низкой громкостью
        """
        casino = Casino()
        logger = Logger()
        player = Player("PeterZhabin", 100)
        goose = HonkGoose("SamirAhmed", 10)
        casino.register_player(player)
        casino.register_goose(goose)
        casino._set_seed(1)
        Honk.execute(casino, logger)
        assert len(casino._chips_history) == 1

    def test_honk_high_volume(self, capsys: Any) -> None:
        """
        Проверяет крик гуся с высокой громкостью
        """
        casino = Casino()
        logger = Logger()
        player = Player("PeterZhabin", 100)
        g1 = HonkGoose("SamirAhmed1", 80)
        g2 = HonkGoose("SamirAhmed2", 20)
        casino.register_player(player)
        casino.register_goose(g1)
        casino.register_goose(g2)
        casino._set_seed(5)
        initial_count = len(casino._goose_collection)
        Honk.execute(casino, logger)
        assert len(casino._goose_collection) <= initial_count
