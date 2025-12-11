from functools import wraps
from typing import Any, Callable, TypeVar, Union

from entities.errors import ValidationError

T = TypeVar("T")


class Goose:
    pass


class BaseCollection:
    _collection: list[Any]


class Chip:
    pass


def validate_honk_volume(func: Callable[..., None]) -> Callable[..., None]:
    """
    Декоратор для валидации громкости крика гуся
    :param func: Функция для декорирования
    :return: Обёрнутая функция с валидацией
    """

    @wraps(func)
    def wrapper(self: "Goose", value: int) -> None:
        """
        Проверить громкость гуся на корректность
        :param self: Экземпляр гуся
        :param value: Значение громкости
        :raises ValidationError: Если громкость не в диапазоне 1-100
        """
        if value <= 0 or value > 100:
            raise ValidationError("Громкость должна быть от 1 до 100")
        return func(self, value)

    return wrapper


def validate_unique_name(func: Callable[..., None]) -> Callable[..., None]:
    """
    Декоратор для валидации уникальности имени в коллекции
    :param func: Функция для декорирования
    :return: Обёрнутая функция с валидацией
    """

    @wraps(func)
    def wrapper(self: Any, value: Any) -> None:
        """
        Проверить уникальность имени объекта в коллекции
        :param self: Экземпляр коллекции
        :param value: Объект для добавления
        :raises ValidationError: Если объект с таким именем уже существует
        """
        for item in self._collection:
            if item.name == value.name:
                raise ValidationError("Объект с таким именем уже был создан")
        return func(self, value)

    return wrapper


def validate_chip(func: Callable[..., Any]) -> Callable[..., Any]:
    """
    Декоратор для валидации типа объекта фишки
    :param func: Функция для декорирования
    :return: Обёрнутая функция с валидацией
    """

    @wraps(func)
    def wrapper(self: Any, value: Union["Chip", int, float]) -> Any:
        """
        Проверить тип объекта на соответствие фишке или числу
        :param self: Экземпляр фишки
        :param value: Значение для проверки
        :raises ValidationError: Если объект не является фишкой или числом
        """
        if not isinstance(value, (type(self), int, float)):
            raise ValidationError("Объект должен быть фишкой или числом")
        return func(self, value)

    return wrapper
