from functools import wraps
from typing import Any, Callable, Union

from src.entities.errors import ValidationError
from src.entities.protocols import Chip, Goose, HasCollection, Player


def validate_honk_volume(func: Callable[..., None]) -> Callable[..., None]:
    """
    Декоратор для валидации громкости крика гуся
    :param func: Функция для декорирования
    :return: Функция с валидацией
    """

    @wraps(func)
    def wrapper(self: Goose, value: int) -> None:
        if value <= 0 or value > 100:
            raise ValidationError("Громкость должна быть от 1 до 100")

        return func(self, value)

    return wrapper


def validate_unique_name(func: Callable[..., None]) -> Callable[..., None]:
    """
    Декоратор для валидации уникальности имени в коллекции
    :param func: Функция для декорирования
    :return: Функция с валидацией
    """

    @wraps(func)
    def wrapper(self: HasCollection, value: Player | Goose) -> None:
        for item in self._collection:
            if item.name == value.name:
                raise ValidationError("Объект с таким именем уже был создан")

        return func(self, value)

    return wrapper


def validate_chip(func: Callable[..., Any]) -> Callable[..., Any]:
    """
    Декоратор для валидации типа объекта фишки
    :param func: Функция для декорирования
    :return: Функция с валидацией
    """

    @wraps(func)
    def wrapper(self: Chip, value: Union[Chip, int, float]) -> Any:
        if not isinstance(value, (type(self), int, float)):
            raise ValidationError("Объект должен быть фишкой или числом")

        return func(self, value)

    return wrapper
