import random

from src.entities.chip import Chip
from src.entities.event import BaseEvent
from src.entities.protocols import CasinoProtocol, LoggerProtocol, Player


class BonusRain(BaseEvent):
    @staticmethod
    def execute(casino: CasinoProtocol, logger: LoggerProtocol) -> None:
        """
        Выполняет событие дождя бонусов для игроков
        :param casino: Объект казино
        :param logger: Объект логгера
        """
        action = "[BONUS-RAIN]"
        logger.event_start(action)

        casino._check_players_collection(action)

        lucky_count = random.randint(1, len(casino._player_collection))
        lucky_players: list[Player] = random.sample(
            list(casino._player_collection), lucky_count
        )

        print(f"Дождь бонусов! {lucky_count} игрок(ов) получат фишки!")

        for player in lucky_players:
            bonus_amount = random.randint(10, 100)
            bonus_chip = Chip(bonus_amount)

            old_balance = casino._players_balance[player.name].value
            new_balance = old_balance + bonus_amount

            casino._players_balance[player.name] = new_balance
            logger.balance_change(player.name, old_balance, new_balance)

            casino._chips_history.append(
                bonus_chip, f"Бонус дождь для {player.name}"
            )
            logger.chip_added(bonus_amount, f"Бонус дождь для {player.name}")

            print(f"{player.name} получил {bonus_amount} фишек!")
