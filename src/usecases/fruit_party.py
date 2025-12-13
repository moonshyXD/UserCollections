import random

from src.entities.event import BaseEvent
from src.entities.protocols import CasinoProtocol, LoggerProtocol, Player


class FruitParty(BaseEvent):
    @staticmethod
    def execute(casino: CasinoProtocol, logger: LoggerProtocol) -> None:
        """
        Выполняет событие проигрыша всех фишек в слоте Fruit Party
        :param casino: Объект казино
        :param logger: Объект логгера
        """
        action = "[FRUIT-PARTY]"
        logger.event_start(action)

        casino._check_players_collection(action)

        player: Player = random.choice(list(casino._player_collection))
        lost_chips = casino._players_balance[player.name]
        old_balance = lost_chips.value

        casino._players_balance[player.name] = 0
        logger.balance_change(player.name, old_balance, 0)

        casino._chips_history.append(
            lost_chips, f"{player.name} проиграл всё в Fruit Party"
        )
        logger.chip_added(
            old_balance, f"{player.name} проиграл всё в Fruit Party"
        )

        print(f"{player.name} проиграл всё в слоте Fruit Party!")
