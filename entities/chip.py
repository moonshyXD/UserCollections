from entities.errors import ValidationError


class Chip:
    def __init__(self, value: int):
        self._value = max(0, value)

    @property
    def value(self):
        return self._value

    def __add__(self, other: ("Chip", int, float)):
        if isinstance(other, Chip):
            return Chip(self.value + other.value)
        elif isinstance(other, (int, float)):
            return Chip(self.value + other)

        return ValidationError(f"Объект {other} должен быть фишкой или числом")
