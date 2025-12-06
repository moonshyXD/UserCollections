from abc import ABC, abstractmethod


class Goose(ABC):
    def __init__(self, name: str, honk_volume: int | float):
        self._name = name
        self._honk_volume = honk_volume

    @property
    def name(self):
        return self._name

    @property
    def honk_volume(self):
        return self._honk_volume

    @abstractmethod
    def execute(self):
        pass


class WarGoose(Goose):
    def execute(self):
        return f"{self.name} атакует! Громкость: {self.honk_volume}"


class HonkGoose(Goose):
    def execute(self):
        return f"{self.name} кричит! Громкость: {self.honk_volume}"
