from abc import ABC, abstractmethod
from typing import Generic, Iterator, TypeVar

T = TypeVar("T")


class BaseCollection(ABC, Generic[T]):
    def __init__(self) -> None:
        self._collection: list[T] = []

    @property
    def collection(self):
        return self._collection

    def __getitem__(self, index: int) -> T:
        return self._collection[index]

    def __iter__(self) -> Iterator[T]:
        return iter(self._collection)

    def __len__(self) -> int:
        return len(self._collection)

    @abstractmethod
    def append(self, value: T) -> None:
        pass

    @abstractmethod
    def remove(self, value: T) -> None:
        pass

    @abstractmethod
    def __repr__(self):
        pass
