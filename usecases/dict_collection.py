from entities.chip import Chip


class CasinoBalance:
    def __init__(self):
        self._balance = {}

    def __getitem__(self, player_name: str) -> float:
        return self._balance.get(player_name, 0.0)

    def __setitem__(self, player_name: str, balance: Chip | int | float):
        if isinstance(balance, Chip):
            new_chip = balance
        else:
            new_chip = Chip(int(balance))

        self._balance[player_name] = new_chip

    def __iter__(self):
        return iter(self._balance.items())

    def __len__(self):
        return len(self._balance)
