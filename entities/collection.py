from abc import ABC, abstractmethod
from collections.abc import Sequence
from typing import Any, Generic, Iterator, TypeVar, Union, overload

T = TypeVar("T")


class BaseCollection(ABC, Sequence[T], Generic[T]):
    def __init__(self) -> None:
        """Инициализировать пустую коллекцию"""
        self._collection: list[T] = []

    @property
    def collection(self) -> list[T]:
        """
        Получить внутреннюю коллекцию
        :return: Список элементов коллекции
        """
        return self._collection

    @overload
    def __getitem__(self, index: int) -> T: ...

    @overload
    def __getitem__(self, index: slice) -> Sequence[T]: ...

    def __getitem__(self, index: Union[int, slice]) -> Union[T, Sequence[T]]:
        """
        Получить элемент коллекции по индексу
        :param index: Индекс элемента
        :return: Элемент коллекции
        """
        return self._collection[index]

    def __iter__(self) -> Iterator[T]:
        """
        Получить итератор коллекции
        :return: Итератор по элементам коллекции
        """
        return iter(self._collection)

    def __len__(self) -> int:
        """
        Получить длину коллекции
        :return: Количество элементов в коллекции
        """
        return len(self._collection)

    @abstractmethod
    def append(self, value: Any, *args: Any) -> None:
        """
        Добавить элемент в коллекцию
        :param value: Элемент для добавления
        :param args: Дополнительные аргументы
        """
        pass

    @abstractmethod
    def remove(self, value: T) -> None:
        """
        Удалить элемент из коллекции
        :param value: Элемент для удаления
        """
        pass

    @abstractmethod
    def __repr__(self) -> str:
        """
        Получить строковое представление коллекции
        :return: Строка с содержимым коллекции
        """
        pass
