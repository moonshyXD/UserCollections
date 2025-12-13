import random

from src.entities.chip import Chip
from src.entities.event import BaseEvent
from src.entities.goose import HonkGoose
from src.entities.protocols import CasinoProtocol, LoggerProtocol


class Honk(BaseEvent):
    @staticmethod
    def execute(casino: CasinoProtocol, logger: LoggerProtocol) -> None:
        """
        Выполняет событие крика гуся
        :param casino: Объект казино
        :param logger: Объект логгера
        """
        action = "[HONK]"
        logger.event_start(action)

        honk_geese = [
            g for g in casino._goose_collection if isinstance(g, HonkGoose)
        ]

        casino._check_goose_collection(honk_geese, action)
        casino._check_players_collection(action)

        goose = random.choice(honk_geese)
        honk_volume = goose.honk_volume
        stun_chip = Chip(10)

        if honk_volume <= 50:
            player = random.choice(list(casino._player_collection))
            old_balance = casino._players_balance[player.name].value
            new_balance = old_balance - 10

            casino._players_balance[player.name] = new_balance
            logger.balance_change(player.name, old_balance, new_balance)

            casino._chips_history.append(
                stun_chip, f"{goose.name} оглушил {player.name}"
            )
            logger.chip_added(10, f"{goose.name} оглушил {player.name}")

            print(f"Гусь кричит! {player.name} оглушился и потерял 10 фишек")
        else:
            random_goose = random.choice(list(casino._goose_collection))
            old_balance = casino._geese_balance[random_goose.name].value
            new_balance = old_balance - 10

            casino._geese_balance[random_goose.name] = new_balance
            logger.balance_change(random_goose.name, old_balance, new_balance)

            casino._chips_history.append(
                stun_chip, f"{goose.name} оглушил {random_goose.name}"
            )
            logger.chip_added(10, f"{goose.name} оглушил {random_goose.name}")

            print(f"Гусь кричит слишком громко! {random_goose.name} оглушён")
            print(f"Гусь {goose.name} сломал голос и выходит из игры")

            casino._goose_collection.remove(goose)
            logger.entity_removed(
                "Гусь", goose.name, f"Громкость: {goose.honk_volume}"
            )
