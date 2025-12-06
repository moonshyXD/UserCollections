from entities.chip import Chip


class CasinoBalance:
    def __init__(self):
        self._balance = {}

    def __getitem__(self, player_name: str) -> float:
        return self._balance.get(player_name, 0.0)

    def __setitem__(self, player_name: str, balance: Chip | int | float):
        old_chip = self._balance.get(player_name, Chip(0))
        if isinstance(balance, Chip):
            new_chip = balance
        else:
            new_chip = Chip(int(balance))

        self._balance[player_name] = new_chip
        print(f"[BALANCE] {player_name}: {old_chip.value} → {new_chip.value}")

    def __iter__(self):
        return iter(self._balance.items())

    def __len__(self):
        return len(self._balance)
