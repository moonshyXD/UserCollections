from entities.chip import Chip
from usecases.dict_collection import CasinoBalance


class TestCasinoBalance:
    def test_init_empty(self) -> None:
        """
        Проверить создание пустого баланса
        """
        balance = CasinoBalance()
        assert len(balance) == 0

    def test_setitem_with_int(self) -> None:
        """
        Проверить установку баланса целым числом
        """
        balance = CasinoBalance()
        balance["PeterZhabin"] = 100
        assert isinstance(balance["PeterZhabin"], Chip)
        assert balance["PeterZhabin"].value == 100

    def test_setitem_with_chip(self) -> None:
        """
        Проверить установку баланса фишкой
        """
        balance = CasinoBalance()
        chip = Chip(50)
        balance["PeterZhabin"] = chip
        assert balance["PeterZhabin"].value == 50

    def test_getitem(self) -> None:
        """
        Проверить получение баланса по ключу
        """
        balance = CasinoBalance()
        balance["PeterZhabin"] = 25
        assert balance["PeterZhabin"].value == 25

    def test_iter(self) -> None:
        """
        Проверить итерацию по балансам
        """
        balance = CasinoBalance()
        balance["PeterZhabin"] = 10
        balance["SamirAhmed"] = 20
        items = dict(balance)
        assert "PeterZhabin" in items
        assert "SamirAhmed" in items

    def test_len(self) -> None:
        """
        Проверить получение количества записей в балансе
        """
        balance = CasinoBalance()
        balance["PeterZhabin"] = 10
        balance["SamirAhmed"] = 20
        assert len(balance) == 2

    def test_repr(self) -> None:
        """
        Проверить строковое представление баланса
        """
        balance = CasinoBalance()
        balance["PeterZhabin"] = 15
        rep = repr(balance)
        assert "PeterZhabin" in rep
