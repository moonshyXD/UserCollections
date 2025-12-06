from abc import ABC, abstractmethod
from typing import Generic, TypeVar

T = TypeVar("T")


class BaseCollection(ABC, Generic[T]):
    def __init__(self):
        self._collection: list[T] = []

    @property
    def collection(self):
        return self._collection

    def __getitem__(self, index):
        return self._collection[index]

    def __iter__(self):
        return iter(self._collection)

    def __len__(self):
        return len(self._collection)

    @abstractmethod
    def append(self, value: T):
        pass

    @abstractmethod
    def remove(self, value: T):
        pass
