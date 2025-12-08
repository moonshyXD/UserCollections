from entities.chip import Chip


class Player:
    def __init__(self, name: str, balance: int) -> None:
        self._name = name
        self._balance = Chip(balance)

    @property
    def balance(self) -> Chip:
        return self._balance

    @property
    def name(self) -> str:
        return self._name

    def __repr__(self) -> str:
        return f"(имя={self.name}, баланс={self.balance.value})"
