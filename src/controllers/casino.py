import random
import time
from typing import Iterator

from src.entities.chip import Chip
from src.entities.errors import EntitiesError
from src.entities.goose import Goose
from src.entities.player import Player
from src.entities.protocols import (
    CasinoProtocol,
    GooseCollectionProtocol,
    Logger,
)
from src.usecases.attack import Attack
from src.usecases.bet import Bet
from src.usecases.bonus_rain import BonusRain
from src.usecases.dict_collection import CasinoBalance
from src.usecases.flock_steal import FlockSteal
from src.usecases.freebet import Freebet
from src.usecases.fruit_party import FruitParty
from src.usecases.honk import Honk
from src.usecases.list_collections import (
    ChipCollection,
    GooseCollection,
    PlayerCollection,
)
from src.usecases.sabotage import Sabotage
from src.usecases.steal import Steal


class Casino(CasinoProtocol):
    def __init__(self) -> None:
        """Инициализировать казино с пустыми коллекциями"""
        Logger.setup_logging()
        self._goose_collection = GooseCollection()
        self._players_balance = CasinoBalance()
        self._geese_balance = CasinoBalance()
        self._player_collection = PlayerCollection()
        self._chips_history = ChipCollection()

    def _set_seed(self, seed: int | None = None) -> None:
        """
        Установить seed для генератора случайных чисел
        :param seed: Значение seed или None для случайного поведения
        """
        if seed is not None:
            random.seed(seed)
            Logger.start_execution(f"Установлен seed: {seed}")

    def _check_players_collection(self, action: str) -> None:
        """
        Проверить наличие игроков в коллекции
        :param action: Название действия для сообщения об ошибке
        :raises EntitiesError: Если коллекция игроков пуста
        """
        if len(self._player_collection) == 0:
            raise EntitiesError(f"Нет игроков для события {action}")

    def _check_goose_collection(
        self,
        collection: GooseCollectionProtocol,
        action: str,
    ) -> None:
        """
        Проверить наличие гусей в коллекции
        :param collection: Коллекция гусей для проверки
        :param action: Название действия для сообщения об ошибке
        :raises EntitiesError: Если коллекция гусей пуста
        """
        if len(collection) == 0:
            raise EntitiesError(f"Нет гусей для события {action}")

    def register_goose(self, value: Goose) -> None:
        """
        Зарегистрировать гуся в казино
        :param value: Гусь для регистрации
        """
        self._goose_collection.append(value)
        self._geese_balance[value.name] = Chip(0)
        Logger.success_execution(f"Зарегистрирован гусь: {value.name}")

    def register_player(self, value: Player) -> None:
        """
        Зарегистрировать игрока в казино
        :param value: Игрок для регистрации
        """
        self._player_collection.append(value)
        self._players_balance[value.name] = value.balance
        Logger.success_execution(
            f"Зарегистрирован игрок {value.name} баланс: {value.balance.value}"
        )

    def __iter__(self) -> Iterator[Player]:
        """
        Получить итератор по игрокам казино
        :return: Итератор по коллекции игроков
        """
        return iter(self._player_collection)

    def run_simulation(self, steps: int = 20, seed: int | None = None) -> None:
        self._set_seed(seed)
        Logger.start_execution(f"Симуляция на {steps} шагов")

        actions = [
            lambda cas: Attack.execute(cas, Logger),
            lambda cas: Bet.execute(cas, Logger),
            lambda cas: Honk.execute(cas, Logger),
            lambda cas: Steal.execute(cas, Logger),
            lambda cas: Sabotage.execute(cas, Logger),
            lambda cas: Freebet.execute(cas, Logger),
            lambda cas: FruitParty.execute(cas, Logger),
            lambda cas: FlockSteal.execute(cas, Logger),
            lambda cas: BonusRain.execute(cas, Logger),
        ]

        for step in range(1, steps + 1):
            action = random.choice(actions)
            try:
                print(f"\nСобытие {step}/{steps}")
                action(self)
            except EntitiesError as e:
                Logger.failure_execution(e)
                print(f"Ошибка: {e}")

        random.seed(time.time())
        Logger.success_execution("Симуляция завершена")
