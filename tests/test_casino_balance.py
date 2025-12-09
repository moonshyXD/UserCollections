from entities.chip import Chip
from usecases.dict_collection import CasinoBalance


class TestCasinoBalance:
    def test_init_empty(self):
        balance = CasinoBalance()
        assert len(balance) == 0

    def test_getitem_nonexistent_returns_zero_chip(self):
        balance = CasinoBalance()
        chip = balance["Goose"]
        assert chip.value == 0

    def test_setitem_with_chip(self, capsys):
        balance = CasinoBalance()
        balance["Goose"] = Chip(100)
        assert balance["Goose"].value == 100
        captured = capsys.readouterr()
        assert "[BALANCE] Goose: 0 → 100" in captured.out

    def test_setitem_with_int(self, capsys):
        balance = CasinoBalance()
        balance["Goose"] = 50
        assert balance["Goose"].value == 50
        captured = capsys.readouterr()
        assert "[BALANCE] Goose: 0 → 50" in captured.out

    def test_iter(self):
        balance = CasinoBalance()
        balance["Goose1"] = Chip(100)
        balance["Goose2"] = Chip(50)
        items = list(balance)
        assert len(items) == 2

    def test_len(self):
        balance = CasinoBalance()
        balance["Goose1"] = Chip(100)
        balance["Goose2"] = Chip(50)
        assert len(balance) == 2
