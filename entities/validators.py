from functools import wraps
from typing import Callable, TypeVar

from entities.errors import ValidationError

T = TypeVar("T")


class Goose:
    pass


class BaseCollection:
    pass


class Chip:
    pass


def validate_honk_volume(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(self: "Goose", value: int) -> None:
        if value <= 0 or value > 100:
            raise ValidationError("Громкость должна быть от 1 до 100")
        return func(self, value)

    return wrapper


def validate_unique_name(func: Callable):
    @wraps(func)
    def wrapper(self: "BaseCollection", value: T):
        for item in self._collection:
            if item.name == value.name:
                raise ValidationError("Объект с таким именем уже был создан")

        return func(self, value)

    return wrapper


def validate_chip(func: Callable):
    @wraps(func)
    def wrapper(self, value: list["Chip", int, float]):
        if not isinstance(value, (Chip, int, float)):
            raise ValidationError("Объект должен быть фишкой или числом")
        return func(self, value)

    return wrapper
