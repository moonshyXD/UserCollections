from entities.chip import Chip


class Player:
    def __init__(self, name: str, balance: float):
        self._name = name
        self._balance = Chip(balance)

    @property
    def balance(self):
        return self._balance

    @property
    def name(self):
        return self._name

    def __repr__(self):
        return f"Игрок(имя={self.name.value}, баланс={self.balance.value})"
