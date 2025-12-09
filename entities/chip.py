from entities.validators import validate_chip


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

    @validate_chip
    def __add__(self, other: list["Chip", int, float]) -> "Chip":
        if isinstance(other, Chip):
            return Chip(self.total + other.total, denomination=1)
        elif isinstance(other, (int, float)):
            return Chip(self.total + int(other), denomination=1)

    def __sub__(self, other: list["Chip", int, float]) -> "Chip":
        if isinstance(other, Chip):
            new_value = max(0, self.total - other.total)
            return Chip(new_value, denomination=1)
        elif isinstance(other, (int, float)):
            new_value = max(0, self.total - int(other))
            return Chip(new_value, denomination=1)

    def __repr__(self) -> str:
        if self.denomination == 1:
            return f"Фишка({self.value})"

        return f"({self.value}x{self.denomination}={self.total})"
