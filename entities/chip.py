from typing import Union

from entities.errors import ValidationError


class Chip:
    def __init__(self, value: int, denomination: int = 1) -> None:
        self._value = max(0, value)
        self._denomination = denomination

    @property
    def value(self) -> int:
        return self._value

    @property
    def denomination(self) -> int:
        return self._denomination

    @property
    def total(self) -> int:
        return self._value * self._denomination

    def __add__(self, other: Union["Chip", int, float]) -> "Chip":
        if isinstance(other, Chip):
            return Chip(self.total + other.total, denomination=1)
        elif isinstance(other, (int, float)):
            return Chip(self.total + int(other), denomination=1)

        raise ValidationError("Объект должен быть фишкой или числом")

    def __sub__(self, other: Union["Chip", int, float]) -> "Chip":
        if isinstance(other, Chip):
            new_value = max(0, self.total - other.total)
            return Chip(new_value, denomination=1)
        elif isinstance(other, (int, float)):
            new_value = max(0, self.total - int(other))
            return Chip(new_value, denomination=1)

        raise ValidationError("Объект должен быть фишкой или числом")

    def __repr__(self) -> str:
        if self.denomination == 1:
            return f"Фишка({self.value})"

        return f"Фишка ({self.value}x{self.denomination}={self.total})"
