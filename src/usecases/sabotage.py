import random

from src.entities.event import BaseEvent
from src.entities.protocols import CasinoProtocol, LoggerProtocol


class Sabotage(BaseEvent):
    @staticmethod
    def execute(casino: CasinoProtocol, logger: LoggerProtocol) -> None:
        """
        Выполняет событие саботажа с перемешиванием балансов
        :param casino: Объект казино
        :param logger: Объект логгера
        """
        action = "[SABOTAGE]"
        logger.event_start(action)

        casino._check_players_collection(action)
        casino._check_goose_collection(casino._goose_collection, action)

        players = casino._player_collection
        player_balances = [casino._players_balance[p.name] for p in players]
        random.shuffle(player_balances)

        for i in range(len(players)):
            old_balance = casino._players_balance[players[i].name].value
            new_balance = player_balances[i].value
            casino._players_balance[players[i].name] = player_balances[i]
            logger.balance_change(players[i].name, old_balance, new_balance)

        geese = casino._goose_collection
        goose_balances = [casino._geese_balance[g.name] for g in geese]
        random.shuffle(goose_balances)

        for i in range(len(geese)):
            old_balance = casino._geese_balance[geese[i].name].value
            new_balance = goose_balances[i].value
            casino._geese_balance[geese[i].name] = goose_balances[i]
            logger.balance_change(geese[i].name, old_balance, new_balance)

        print("Балансы игроков и гусей перемешаны!")
