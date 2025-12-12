import pytest

from src.entities.errors import ValidationError
from src.entities.goose import HonkGoose
from src.entities.player import Player
from src.usecases.list_collections import GooseCollection, PlayerCollection


class TestValidateHonkVolume:
    def test_valid_volume(self) -> None:
        """
        Проверяет установку допустимой громкости
        """
        goose = HonkGoose("Peter Zhabin", 50)
        assert goose.honk_volume == 50

    def test_volume_zero_raises(self) -> None:
        """
        Проверяет ошибку при громкости 0
        """
        with pytest.raises(ValidationError):
            HonkGoose("Peter Zhabin", 0)

    def test_volume_negative_raises(self) -> None:
        """
        Проверяет ошибку при отрицательной громкости
        """
        with pytest.raises(ValidationError):
            HonkGoose("Peter Zhabin", -5)

    def test_volume_over_100_raises(self) -> None:
        """
        Проверяет ошибку при громкости больше 100
        """
        with pytest.raises(ValidationError):
            HonkGoose("Peter Zhabin", 101)


class TestValidateUniqueName:
    def test_append_unique_players(self) -> None:
        """
        Проверяет добавление игроков с уникальными именами
        """
        coll = PlayerCollection()
        coll.append(Player("Peter", 100))
        coll.append(Player("Zhabin", 200))
        assert len(coll) == 2

    def test_append_duplicate_player_raises(self) -> None:
        """
        Проверяет ошибку при добавлении игрока с существующим именем
        """
        coll = PlayerCollection()
        coll.append(Player("Peter", 100))
        with pytest.raises(ValidationError):
            coll.append(Player("Peter", 200))

    def test_append_unique_geese(self) -> None:
        """
        Проверяет добавление гусей с уникальными именами
        """
        coll = GooseCollection()
        coll.append(HonkGoose("Samir", 30))
        coll.append(HonkGoose("Ahmed", 40))
        assert len(coll) == 2

    def test_append_duplicate_goose_raises(self) -> None:
        """
        Проверяет ошибку при добавлении гуся с существующим именем
        """
        coll = GooseCollection()
        coll.append(HonkGoose("Samir", 30))
        with pytest.raises(ValidationError):
            coll.append(HonkGoose("Samir", 40))
