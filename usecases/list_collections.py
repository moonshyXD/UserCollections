from typing import TypeVar

from entities.chip import Chip
from entities.collection import BaseCollection
from entities.goose import Goose
from entities.player import Player

T = TypeVar("T")


class PlayerCollection(BaseCollection[Player]):
    def append(self, value: Player) -> None:
        print(f"Добавлен {value}")
        self._collection.append(value)

    def remove(self, value: Player) -> None:
        print(f"Удалён {value}")
        self._collection.remove(value)


class GooseCollection(BaseCollection[Goose]):
    def append(self, value: Goose) -> None:
        print(f"Добавлен {value}")
        self._collection.append(value)

    def remove(self, value: Goose) -> None:
        print(f"Удалён {value}")
        self._collection.remove(value)


class ChipCollection(BaseCollection[Chip]):
    def append(self, value: Chip) -> None:
        print(f"Добавлена {value}")
        self._collection.append(value)

    def remove(self, value: Chip) -> None:
        print(f"Удалена {value}")
        self._collection.remove(value)
