from typing import Any

import pytest

from src.adapters.logger import Logger
from src.controllers.casino import Casino
from src.entities.errors import EntitiesError
from src.entities.player import Player
from src.usecases.bonus_rain import BonusRain


class TestBonusRain:
    def test_bonus_rain_no_players_raises(self) -> None:
        """
        Проверяет ошибку при бонусном дожде без игроков
        """
        casino = Casino()
        logger = Logger()
        with pytest.raises(EntitiesError):
            BonusRain.execute(casino, logger)

    def test_bonus_rain_success(self, capsys: Any) -> None:
        """
        Проверяет успешный бонусный дождь
        """
        casino = Casino()
        logger = Logger()
        p1 = Player("PeterZhabin", 100)
        p2 = Player("PeterZhabin2", 200)
        casino.register_player(p1)
        casino.register_player(p2)
        casino._set_seed(40)
        BonusRain.execute(casino, logger)
        assert len(casino._chips_history) >= 1
