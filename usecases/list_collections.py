from entities.chip import Chip
from entities.goose import Goose
from entities.player import Player
from entities.collection import BaseCollection


class PlayerCollection(BaseCollection):
    def append(self, value: Player):
        print(f"Добавлен игрок {value}")
        self._collection.append(value)

    def remove(self, value: Player):
        print(f"Удалён игрок {value}")
        self._collection.remove(value)


class GooseCollection(BaseCollection):
    def append(self, value: Goose):
        print(f"Добавлен гусь {value}")
        self._collection.append(value)

    def remove(self, value: Goose):
        print(f"Удалён гусь {value}")
        self._collection.remove(value)


class ChipCollection(BaseCollection):
    def append(self, value: Chip):
        print(f"Добавлена фишка {value}")
        self._collection.append(value)

    def remove(self, value: Chip):
        print(f"Удалена фишка {value}")
        self._collection.remove(value)
