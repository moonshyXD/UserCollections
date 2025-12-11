from abc import ABC, abstractmethod

from entities.validators import validate_honk_volume


class Goose(ABC):
    """Абстрактный класс гуся"""

    def __init__(self, name: str, honk_volume: int) -> None:
        """
        Инициализировать гуся
        :param name: Имя гуся
        :param honk_volume: Громкость крика гуся (1-100)
        """
        self._name = name
        self._honk_volume = 0
        self.honk_volume = honk_volume

    @property
    def name(self) -> str:
        """
        Получить имя гуся
        :return: Имя гуся
        """
        return self._name

    @property
    def honk_volume(self) -> int:
        """
        Получить громкость крика гуся
        :return: Громкость крика (1-100)
        """
        return self._honk_volume

    @honk_volume.setter
    @validate_honk_volume
    def honk_volume(self, value: int) -> None:
        """
        Установить громкость крика гуся
        :param value: Новая громкость крика (1-100)
        :raises ValidationError: Если громкость вне диапазона 1-100
        """
        self._honk_volume = value

    @abstractmethod
    def execute(self) -> str:
        """
        Выполнить действие гуся
        :return: Строка с описанием действия
        """
        pass

    def __repr__(self) -> str:
        """
        Получить строковое представление гуся
        :return: Строка с именем и громкостью гуся
        """
        return f"Гусь: {self._name} Громкость: {self._honk_volume}"


class WarGoose(Goose):
    """Класс боевого гуся"""

    def execute(self) -> str:
        """
        Выполнить атаку гуся
        :return: Строка с описанием атаки
        """
        return f"{self.name} атакует! Атака: {self.honk_volume}"


class HonkGoose(Goose):
    """Класс кричащего гуся"""

    def execute(self) -> str:
        """
        Выполнить крик гуся
        :return: Строка с описанием крика
        """
        return f"{self.name} кричит! Громкость: {self.honk_volume}"
