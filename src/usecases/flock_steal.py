import random

from src.entities.chip import Chip
from src.entities.event import BaseEvent
from src.entities.goose import WarGoose
from src.entities.protocols import CasinoProtocol, LoggerProtocol


class FlockSteal(BaseEvent):
    @staticmethod
    def execute(casino: CasinoProtocol, logger: LoggerProtocol) -> None:
        """
        Выполняет событие кражи фишек стаей военных гусей
        :param casino: Объект казино
        :param logger: Объект логгера
        """
        action = "[FLOCK_STEAL]"
        logger.event_start(action)

        war_geese = [
            g for g in casino._goose_collection if isinstance(g, WarGoose)
        ]

        casino._check_players_collection(action)
        casino._check_goose_collection(war_geese, action)

        geese_count = random.randint(1, len(war_geese))
        player = random.choice(list(casino._player_collection))
        player_chip = casino._players_balance[player.name]

        if player_chip.value == 0:
            logger.event_start(f"{action} - У игрока {player.name} нет фишек")
            print(f"У {player.name} нет фишек для кражи")
            return

        amount = random.randint(1, player_chip.value)
        stolen_chip = Chip(amount)

        old_balance = player_chip.value
        casino._players_balance[player.name] = old_balance - amount
        logger.balance_change(player.name, old_balance, old_balance - amount)

        casino._chips_history.append(
            stolen_chip, f"Стая гусей украла у {player.name}"
        )
        logger.chip_added(amount, f"Стая гусей украла у {player.name}")

        per_goose = amount // geese_count
        goose_share = Chip(per_goose)

        for _ in range(geese_count):
            goose = random.choice(war_geese)
            old_goose = casino._geese_balance[goose.name].value
            new_goose = old_goose + per_goose

            casino._geese_balance[goose.name] = new_goose
            logger.balance_change(goose.name, old_goose, new_goose)

            casino._chips_history.append(
                goose_share, f"Flock steal: {goose.name}"
            )
            logger.chip_added(per_goose, f"Flock steal: {goose.name}")

        print(
            f"Стая из {geese_count} гусей украла "
            f"{amount} фишек у {player.name}!"
        )
