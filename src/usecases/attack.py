import random

from src.entities.chip import Chip
from src.entities.event import BaseEvent
from src.entities.goose import WarGoose
from src.entities.protocols import CasinoProtocol, LoggerProtocol, Player


class Attack(BaseEvent):
    @staticmethod
    def execute(casino: CasinoProtocol, logger: LoggerProtocol) -> None:
        """
        Выполняет событие атаки военного гуся на игрока
        :param casino: Объект казино
        :param logger: Объект логгера
        """
        action = "[ATTACK]"
        logger.event_start(action)

        war_geese = [
            g for g in casino._goose_collection if isinstance(g, WarGoose)
        ]

        casino._check_players_collection(action)
        casino._check_goose_collection(war_geese, action)

        goose = random.choice(war_geese)
        player: Player = random.choice(casino._player_collection)

        damage = random.randint(1, 100)
        cur_chip = casino._players_balance[player.name]
        old_balance = cur_chip.value
        new_value = max(0, old_balance - damage)
        damage_chip = Chip(damage)

        casino._players_balance[player.name] = new_value
        logger.balance_change(player.name, old_balance, new_value)

        casino._chips_history.append(
            damage_chip, f"{goose.name} атаковал {player.name}"
        )
        logger.chip_added(damage, f"{goose.name} атаковал {player.name}")

        print(f"{goose.name} атакует {player.name}! Урон: {damage}")
