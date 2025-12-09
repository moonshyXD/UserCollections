from typing import TypeVar

from entities.chip import Chip
from entities.collection import BaseCollection
from entities.goose import Goose
from entities.player import Player
from entities.validators import validate_unique_name

T = TypeVar("T")


class PlayerCollection(BaseCollection[Player]):
    @validate_unique_name
    def append(self, value: Player) -> None:
        print(f"Добавлен {value}")
        self._collection.append(value)

    def remove(self, value: Player) -> None:
        print(f"Удалён {value}")
        self._collection.remove(value)

    def __repr__(self):
        return print(self._collection)


class GooseCollection(BaseCollection[Goose]):
    @validate_unique_name
    def append(self, value: Goose) -> None:
        print(f"Добавлен {value}")
        self._collection.append(value)

    def remove(self, value: Goose) -> None:
        print(f"Удалён {value}")
        self._collection.remove(value)

    def __repr__(self):
        return print(self._collection)


class ChipTransaction:
    def __init__(self, chip: Chip, event: str):
        self.chip = chip
        self.event = event

    def __repr__(self) -> str:
        return f"Фишка: {self.chip}, Событие: '{self.event}'"


class ChipCollection(BaseCollection[ChipTransaction]):
    def append(self, chip: Chip, event: str) -> None:
        transaction = ChipTransaction(chip, event)
        print(f"Добавлена {chip} ({event})")
        self._collection.append(transaction)

    def remove(self, value: ChipTransaction) -> None:
        print(f"Удалена {value}")
        self._collection.remove(value)

    def get_history(self) -> list[tuple[Chip, str]]:
        return [(t.chip, t.event) for t in self._collection]

    def __repr__(self):
        return print(self._collection)
