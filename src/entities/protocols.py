from typing import Any, Protocol


class Goose(Protocol):
    """Заглушка для Goose"""

    name: str
    _honk_volume: int


class Player(Protocol):
    """Заглушка для Player"""

    name: str


class Chip(Protocol):
    """Заглушка для Chip"""

    pass


class HasCollection(Protocol):
    """Заглушка для объектов с коллекцией"""

    _collection: list[Any]
