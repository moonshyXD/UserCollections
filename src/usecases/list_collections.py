from src.entities.chip import Chip
from src.entities.collection import BaseCollection
from src.entities.goose import Goose
from src.entities.player import Player
from src.entities.validators import validate_unique_name


class ChipTransaction:
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
    @validate_unique_name
    def append(self, value: Player) -> None:
        """
        Добавить игрока в коллекцию
        :param value: Игрок
        :raises ValidationError: Если игрок с таким именем существует
        """
        self._collection.append(value)

    def remove(self, value: Player) -> None:
        """
        Удалить игрока из коллекции
        :param value: Игрок
        """
        self._collection.remove(value)

    def __repr__(self) -> str:
        """
        Получить строковое представление коллекции игроков
        :return: Строка со списком игроков
        """
        return str(self._collection)


class GooseCollection(BaseCollection[Goose]):
    @validate_unique_name
    def append(self, value: Goose) -> None:
        """
        Добавить гуся в коллекцию
        :param value: Гусь
        :raises ValidationError: Если гусь с таким именем существует
        """
        self._collection.append(value)

    def remove(self, value: Goose) -> None:
        """
        Удалить гуся из коллекции
        :param value: Гусь
        """
        self._collection.remove(value)

    def __repr__(self) -> str:
        """
        Получить строковое представление коллекции гусей
        :return: Строка со списком гусей
        """
        return str(self._collection)


class ChipCollection(BaseCollection[ChipTransaction]):
    def append(self, chip: Chip, event: str) -> None:
        """
        Добавить транзакцию фишки в историю
        :param chip: Фишка транзакции
        :param event: Событие транзакции
        """
        transaction = ChipTransaction(chip, event)
        self._collection.append(transaction)

    def remove(self, value: ChipTransaction) -> None:
        """
        Удалить транзакцию из коллекции
        :param value: Транзакция для удаления
        """
        self._collection.remove(value)

    def get_history(self) -> list[tuple[Chip, str]]:
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
