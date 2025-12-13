import random

from src.entities.chip import Chip
from src.entities.event import BaseEvent
from src.entities.protocols import (
    CasinoProtocol,
    Goose,
    LoggerProtocol,
    Player,
)


class Steal(BaseEvent):
    @staticmethod
    def execute(casino: CasinoProtocol, logger: LoggerProtocol) -> None:
        """
        Выполняет событие кражи фишек гусем у игрока
        :param casino: Объект казино
        :param logger: Объект логгера
        """
        action = "[STEAL]"
        logger.event_start(action)

        casino._check_players_collection(action)
        casino._check_goose_collection(casino._goose_collection, action)

        goose: Goose = random.choice(casino._goose_collection)
        player: Player = random.choice(casino._player_collection)

        stolen = min(
            random.randint(1, 100), casino._players_balance[player.name].value
        )
        stolen_chip = Chip(stolen)

        old_player = casino._players_balance[player.name].value
        casino._players_balance[player.name] = old_player - stolen
        logger.balance_change(player.name, old_player, old_player - stolen)

        old_goose = casino._geese_balance[goose.name].value
        casino._geese_balance[goose.name] = old_goose + stolen
        logger.balance_change(goose.name, old_goose, old_goose + stolen)

        casino._chips_history.append(
            stolen_chip, f"{goose.name} украл у {player.name}"
        )
        logger.chip_added(stolen, f"{goose.name} украл у {player.name}")

        print(f"{goose.name} крадёт у {player.name}! Украдено: {stolen}")
