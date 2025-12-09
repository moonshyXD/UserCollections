from typing import Iterator

from entities.chip import Chip


class CasinoBalance:
    def __init__(self) -> None:
        self._balance: dict[str, Chip] = {}

    def __getitem__(self, player_name: str) -> Chip:
        return self._balance.get(player_name, Chip(0))

    def __setitem__(self, player_name: str, balance: Chip | int) -> None:
        if isinstance(balance, int):
            balance = Chip(balance)

        old_chip = self._balance.get(player_name, Chip(0))
        self._balance[player_name] = balance
        print(f"[BALANCE] {player_name}: {old_chip.value} → {balance.value}")

    def __iter__(self) -> Iterator[tuple[str, Chip]]:
        return iter(self._balance.items())

    def __len__(self) -> int:
        return len(self._balance)

    def __repr__(self) -> None:
        for key, value in self._balance:
            print(f"Объект: {key}, баланс: {value}")
