class Player:
    def __init__(self, name: str, balance: float):
        self.name = name
        self._balance = max(0.0, balance)

    @property
    def balance(self):
        return self._balance
