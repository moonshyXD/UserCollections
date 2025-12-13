import random

from src.entities.chip import Chip
from src.entities.event import BaseEvent
from src.entities.protocols import CasinoProtocol, LoggerProtocol, Player


class Freebet(BaseEvent):
    @staticmethod
    def execute(casino: CasinoProtocol, logger: LoggerProtocol) -> None:
        """
        Выполняет событие фрибета для случайного игрока
        :param casino: Объект казино
        :param logger: Объект логгера
        """
        action = "[FREEBET]"
        logger.event_start(action)

        casino._check_players_collection(action)

        player: Player = random.choice(list(casino._player_collection))
        old_balance = casino._players_balance[player.name].value
        new_balance = old_balance + 50

        casino._players_balance[player.name] = new_balance
        logger.balance_change(player.name, old_balance, new_balance)

        freebet_chip = Chip(50)
        casino._chips_history.append(freebet_chip, f"Фрибет для {player.name}")
        logger.chip_added(50, f"Фрибет для {player.name}")

        print(f"{player.name} получил фрибет 50 фишек!")
