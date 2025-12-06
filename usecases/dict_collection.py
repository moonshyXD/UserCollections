class CasinoBalance:
    def __init__(self):
        self._balance = {}

    def __getitem__(self, player_name: str) -> float:
        return self._balance.get(player_name, 0.0)

    def __setitem__(self, player_name: str, balance: float):
        old_balance = self._balance.get(player_name, 0.0)
        self._balance[player_name] = balance
        print(f"[BALANCE] {player_name}: {old_balance} → {balance}")

    def __iter__(self):
        return iter(self._balance.items())

    def __len__(self):
        return len(self._balance)
