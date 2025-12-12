from abc import ABC, abstractmethod

from entities.validators import validate_honk_volume


class Goose(ABC):
    def __init__(self, name: str, honk_volume: int) -> None:
        """
        Инициализация гуся
        :param _name: Имя гуся
        :param honk_volume: Громкость крика гуся
        """
        self._name = name
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
        :return: Громкость крика гуся
        """
        return self._honk_volume

    @honk_volume.setter
    @validate_honk_volume
    def honk_volume(self, value: int) -> None:
        """
        Установка громкости крика гуся
        :param value: Громкость крика гуся
        :raises ValidationError: Если громкость вне 1-100
        """
        self._honk_volume = value

    @abstractmethod
    def execute(self) -> str:
        """
        Действие гуся
        :return: Описание действия гуся
        """
        pass

    def __repr__(self) -> str:
        """
        Строковое представление гуся
        :return: Имя и громкость гуся
        """
        return f"Гусь: {self._name} Громкость: {self._honk_volume}"


class WarGoose(Goose):
    def execute(self) -> str:
        """
        Атака гуся
        :return: Описание атаки
        """
        return f"{self._name} атакует! Атака: {self._honk_volume}"


class HonkGoose(Goose):
    def execute(self) -> str:
        """
        Крик гуся
        :return: Описание крика
        """
        return f"{self._name} кричит! Громкость: {self._honk_volume}"
