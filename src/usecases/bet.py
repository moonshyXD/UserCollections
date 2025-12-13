import random

from src.entities.chip import Chip
from src.entities.event import BaseEvent
from src.entities.protocols import CasinoProtocol, LoggerProtocol, Player


class Bet(BaseEvent):
    @staticmethod
    def execute(casino: CasinoProtocol, logger: LoggerProtocol) -> None:
        """
        Выполняет событие ставки игрока в казино
        :param casino: Объект казино
        :param logger: Объект логгера
        """
        action = "[BET]"
        logger.event_start(action)

        casino._check_players_collection(action)

        player: Player = random.choice(casino._player_collection)

        casino_x = [0, 0.5, 1, 2, 3, 10]
        casino_procent = [30, 40, 10, 10, 9, 1]

        x = random.choices(casino_x, weights=casino_procent)[0]

        current_chip = casino._players_balance[player.name]
        old_value = current_chip.value
        new_value = int(old_value * x)
        bet_chip = Chip(old_value)

        casino._players_balance[player.name] = new_value
        logger.balance_change(player.name, old_value, new_value)

        casino._chips_history.append(bet_chip, f"Ставка {player.name} х{x}")
        logger.chip_added(old_value, f"Ставка {player.name} х{x}")

        match x:
            case 0:
                print(f"{player.name} проиграл всё в казино! Множитель: х{x}")
            case 0.5:
                print(
                    f"{player.name} получил обидный проигрыш! Множитель: х{x}"
                )
            case 1:
                print(f"Ставка {player.name} не засчиталась! Множитель: х{x}")
            case 2:
                print(f"{player.name} победил! Множитель: х{x}")
            case 3:
                print(f"{player.name} получил крупную победу! Множитель: х{x}")
            case 10:
                print(f"{player.name} выиграл джекпот!!! Множитель: х{x}")
