from typing import Tuple

from entities.chip import Chip
from entities.collection import BaseCollection
from entities.goose import Goose
from entities.player import Player
from entities.validators import validate_unique_name


class ChipTransaction:
    """Класс транзакции фишки"""

    def __init__(self, chip: Chip, event: str) -> None:
        """
        Инициализировать транзакцию фишки
        :param chip: Фишка транзакции
        :param event: Описание события транзакции
        """
        self.chip = chip
        self.event = event

    def __repr__(self) -> str:
        """
        Получить строковое представление транзакции
        :return: Строка с фишкой и событием
        """
        return f"({self.chip}, '{self.event}')"


class PlayerCollection(BaseCollection[Player]):
    """Коллекция игроков"""

    @validate_unique_name
    def append(self, value: Player) -> None:
        """
        Добавить игрока в коллекцию
        :param value: Игрок для добавления
        :raises ValidationError: Если игрок с таким именем уже существует
        """
        self._collection.append(value)

    def remove(self, value: Player) -> None:
        """
        Удалить игрока из коллекции
        :param value: Игрок для удаления
        """
        self._collection.remove(value)

    def __repr__(self) -> str:
        """
        Получить строковое представление коллекции игроков
        :return: Строка со списком игроков
        """
        return str(self._collection)


class GooseCollection(BaseCollection[Goose]):
    """Коллекция гусей"""

    @validate_unique_name
    def append(self, value: Goose) -> None:
        """
        Добавить гуся в коллекцию
        :param value: Гусь для добавления
        :raises ValidationError: Если гусь с таким именем уже существует
        """
        self._collection.append(value)

    def remove(self, value: Goose) -> None:
        """
        Удалить гуся из коллекции
        :param value: Гусь для удаления
        """
        self._collection.remove(value)

    def __repr__(self) -> str:
        """
        Получить строковое представление коллекции гусей
        :return: Строка со списком гусей
        """
        return str(self._collection)


class ChipCollection(BaseCollection[ChipTransaction]):
    """Коллекция транзакций фишек"""

    def append(self, chip: Chip, event: str) -> None:  # type: ignore[override]
        """
        Добавить транзакцию фишки в историю
        :param chip: Фишка транзакции
        :param event: Описание события транзакции
        """
        transaction = ChipTransaction(chip, event)
        self._collection.append(transaction)

    def remove(self, value: ChipTransaction) -> None:
        """
        Удалить транзакцию из коллекции
        :param value: Транзакция для удаления
        """
        self._collection.remove(value)

    def get_history(self) -> list[Tuple[Chip, str]]:
        """
        Получить историю транзакций фишек
        :return: Список кортежей (фишка, событие)
        """
        return [(t.chip, t.event) for t in self._collection]

    def __repr__(self) -> str:
        """
        Получить строковое представление коллекции транзакций
        :return: Строка со списком транзакций
        """
        return str(self._collection)
