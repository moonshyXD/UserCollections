from typing import Union

from src.entities.validators import validate_chip


class Chip:
    def __init__(self, value: int, denomination: int = 1) -> None:
        """
        Инициализировать фишку
        :param value: Количество фишек
        :param denomination: Номинал одной фишки (по умолчанию 1)
        """
        self._value = max(0, value)
        self._denomination = denomination

    @property
    def value(self) -> int:
        """
        Получить количество фишек
        :return: Количество фишек
        """
        return self._value

    @property
    def denomination(self) -> int:
        """
        Получить номинал фишки
        :return: Номинал одной фишки
        """
        return self._denomination

    @property
    def total(self) -> int:
        """
        Получить общую стоимость всех фишек
        :return: Произведение количества фишек на номинал
        """
        return self._value * self._denomination

    @validate_chip
    def __add__(self, other: Union["Chip", int, float]) -> "Chip":
        """
        Сложить фишки с другим объектом
        :param other: Другая фишка или число для сложения
        :return: Новая фишка с суммарным значением
        :raises ValidationError: Если тип other некорректен
        """
        if isinstance(other, Chip):
            return Chip(self.total + other.total, denomination=1)
        return Chip(self.total + int(other), denomination=1)

    @validate_chip
    def __sub__(self, other: Union["Chip", int, float]) -> "Chip":
        """
        Вычесть из фишек другой объект
        :param other: Другая фишка или число для вычитания
        :return: Новая фишка с разностью значений (минимум 0)
        :raises ValidationError: Если тип other некорректен
        """
        if isinstance(other, Chip):
            new_value = max(0, self.total - other.total)
            return Chip(new_value, denomination=1)
        new_value = max(0, self.total - int(other))
        return Chip(new_value, denomination=1)

    def __repr__(self) -> str:
        """
        Получить строковое представление фишки
        :return: Строка с описанием фишки
        """
        if self.denomination == 1:
            return f"Фишка({self.value})"
        return f"({self.value}x{self.denomination}={self.total})"
