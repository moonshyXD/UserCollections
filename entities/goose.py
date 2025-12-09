from abc import ABC, abstractmethod

from entities.validators import validate_honk_volume


class Goose(ABC):
    def __init__(self, name: str, honk_volume: int) -> None:
        self._name = name
        self._honk_volume = 0
        self.honk_volume = honk_volume

    @property
    def name(self) -> str:
        return self._name

    @property
    def honk_volume(self) -> int:
        return self._honk_volume

    @honk_volume.setter
    @validate_honk_volume
    def honk_volume(self, value: int) -> None:
        self._honk_volume = value

    @abstractmethod
    def execute(self) -> str:
        pass

    def __repr__(self) -> str:
        return f"Гусь: {self._name} Громкость: {self._honk_volume}"


class WarGoose(Goose):
    def execute(self) -> str:
        return f"{self.name} атакует! Атака: {self.honk_volume}"


class HonkGoose(Goose):
    def execute(self) -> str:
        return f"{self.name} кричит! Громкость: {self.honk_volume}"
