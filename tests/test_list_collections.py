import pytest

from src.entities.chip import Chip
from src.entities.errors import ValidationError
from src.entities.goose import HonkGoose, WarGoose
from src.entities.player import Player
from src.usecases.list_collections import (
    ChipCollection,
    GooseCollection,
    PlayerCollection,
)


class TestBaseCollection:
    def test_player_collection_init_empty(self) -> None:
        """
        Проверяет создание пустой коллекции игроков
        """
        coll = PlayerCollection()
        assert len(coll) == 0

    def test_player_collection_append_and_len(self) -> None:
        """
        Проверяет добавление игроков и получение длины
        """
        coll = PlayerCollection()
        coll.append(Player("Peter", 100))
        coll.append(Player("Zhabin", 200))
        assert len(coll) == 2

    def test_player_collection_getitem(self) -> None:
        """
        Проверяет получение игрока по индексу
        """
        coll = PlayerCollection()
        p1 = Player("Peter", 100)
        coll.append(p1)
        assert coll[0] == p1

    def test_player_collection_iter(self) -> None:
        """
        Проверяет итерацию по коллекции игроков
        """
        coll = PlayerCollection()
        p1 = Player("Peter", 100)
        p2 = Player("Zhabin", 200)
        coll.append(p1)
        coll.append(p2)
        assert list(coll) == [p1, p2]

    def test_player_collection_remove(self) -> None:
        """
        Проверяет удаление игрока из коллекции
        """
        coll = PlayerCollection()
        p1 = Player("Peter", 100)
        p2 = Player("Zhabin", 200)
        coll.append(p1)
        coll.append(p2)
        coll.remove(p1)
        assert list(coll) == [p2]

    def test_player_collection_property(self) -> None:
        """
        Проверяет доступ к внутренней коллекции игроков
        """
        coll = PlayerCollection()
        p = Player("Peter Zhabin", 100)
        coll.append(p)
        assert coll.collection == [p]

    def test_player_collection_repr(self) -> None:
        """
        Проверяет строковое представление коллекции игроков
        """
        coll = PlayerCollection()
        p = Player("Peter Zhabin", 50)
        coll.append(p)
        assert "Peter Zhabin" in repr(coll)

    def test_player_collection_duplicate_name_raises(self) -> None:
        """
        Проверяет ошибку при добавлении игрока с существующим именем
        """
        coll = PlayerCollection()
        coll.append(Player("Peter Zhabin", 100))
        with pytest.raises(ValidationError):
            coll.append(Player("Peter Zhabin", 200))

    def test_goose_collection_init_empty(self) -> None:
        """
        Проверяет создание пустой коллекции гусей
        """
        coll = GooseCollection()
        assert len(coll) == 0

    def test_goose_collection_append_and_len(self) -> None:
        """
        Проверяет добавление гусей и получение длины
        """
        coll = GooseCollection()
        coll.append(HonkGoose("Peter", 30))
        coll.append(WarGoose("Zhabin", 40))
        assert len(coll) == 2

    def test_goose_collection_getitem(self) -> None:
        """
        Проверяет получение гуся по индексу
        """
        coll = GooseCollection()
        g = HonkGoose("Peter Zhabin", 50)
        coll.append(g)
        assert coll[0] == g

    def test_goose_collection_iter(self) -> None:
        """
        Проверяет итерацию по коллекции гусей
        """
        coll = GooseCollection()
        g1 = HonkGoose("Peter Zhabin", 30)
        g2 = WarGoose("Samir Ahmed", 40)
        coll.append(g1)
        coll.append(g2)
        assert list(coll) == [g1, g2]

    def test_goose_collection_remove(self) -> None:
        """
        Проверяет удаление гуся из коллекции
        """
        coll = GooseCollection()
        g1 = HonkGoose("Peter Zhabin", 30)
        g2 = WarGoose("Samir Ahmed", 40)
        coll.append(g1)
        coll.append(g2)
        coll.remove(g1)
        assert list(coll) == [g2]

    def test_goose_collection_property(self) -> None:
        """
        Проверяет доступ к внутренней коллекции гусей
        """
        coll = GooseCollection()
        g = HonkGoose("Peter Zhabin", 20)
        coll.append(g)
        assert coll.collection == [g]

    def test_goose_collection_repr(self) -> None:
        """
        Проверяет строковое представление коллекции гусей
        """
        coll = GooseCollection()
        g = HonkGoose("Peter Zhabin", 25)
        coll.append(g)
        assert "Peter Zhabin" in repr(coll)

    def test_goose_collection_duplicate_name_raises(self) -> None:
        """
        Проверяет ошибку при добавлении гуся с существующим именем
        """
        coll = GooseCollection()
        coll.append(HonkGoose("Peter", 30))
        with pytest.raises(ValidationError):
            coll.append(WarGoose("Peter", 40))

    def test_chip_collection_init_empty(self) -> None:
        """
        Проверяет создание пустой коллекции транзакций фишек
        """
        coll = ChipCollection()
        assert len(coll) == 0

    def test_chip_collection_append_and_len(self) -> None:
        """
        Проверяет добавление транзакций фишек и получение длины
        """
        coll = ChipCollection()
        coll.append(Chip(10), "event1")
        coll.append(Chip(20), "event2")
        assert len(coll) == 2

    def test_chip_collection_getitem(self) -> None:
        """
        Проверяет получение транзакции по индексу
        """
        coll = ChipCollection()
        chip = Chip(15)
        coll.append(chip, "event")
        tx = coll[0]
        assert tx.chip == chip
        assert tx.event == "event"

    def test_chip_collection_iter(self) -> None:
        """
        Проверяет итерацию по коллекции транзакций
        """
        coll = ChipCollection()
        c1 = Chip(10)
        c2 = Chip(20)
        coll.append(c1, "event1")
        coll.append(c2, "event2")
        transactions = list(coll)
        assert len(transactions) == 2

    def test_chip_collection_remove(self) -> None:
        """
        Проверяет удаление транзакции из коллекции
        """
        coll = ChipCollection()
        coll.append(Chip(5), "event")
        tx = coll[0]
        coll.remove(tx)
        assert len(coll) == 0

    def test_chip_collection_get_history(self) -> None:
        """
        Проверяет получение истории транзакций фишек
        """
        coll = ChipCollection()
        c1 = Chip(10)
        c2 = Chip(20)
        coll.append(c1, "event1")
        coll.append(c2, "event2")
        history = coll.get_history()
        assert len(history) == 2
        assert history[0] == (c1, "event1")
        assert history[1] == (c2, "event2")

    def test_chip_collection_property(self) -> None:
        """
        Проверяет доступ к внутренней коллекции транзакций
        """
        coll = ChipCollection()
        coll.append(Chip(7), "event")
        assert len(coll.collection) == 1

    def test_chip_collection_repr(self) -> None:
        """
        Проверяет строковое представление коллекции транзакций
        """
        coll = ChipCollection()
        coll.append(Chip(8), "event")
        assert "8" in repr(coll)
