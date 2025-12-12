from typing import Any

import pytest

from src.entities.chip import Chip
from src.entities.errors import ValidationError


class TestChip:
    def test_init_positive_value(self) -> None:
        """
        Проверяет создание фишки с положительным значением
        """
        chip = Chip(10)
        assert chip.value == 10
        assert chip.denomination == 1

    def test_init_negative_value_becomes_zero(self) -> None:
        """
        Проверяет, что отрицательное значение приводится к нулю
        """
        chip = Chip(-5)
        assert chip.value == 0

    def test_init_with_denomination(self) -> None:
        """
        Проверяет создание фишки с номиналом
        """
        chip = Chip(5, 10)
        assert chip.value == 5
        assert chip.denomination == 10

    def test_total_property(self) -> None:
        """
        Проверяет расчёт общей стоимости фишек
        """
        chip = Chip(5, 10)
        assert chip.total == 50

    def test_add_two_chips(self) -> None:
        """
        Проверяет сложение двух фишек
        """
        c1 = Chip(10, 2)
        c2 = Chip(5, 3)
        result = c1 + c2
        assert result.value == 35
        assert result.denomination == 1

    def test_add_chip_and_int(self) -> None:
        """
        Проверяет сложение фишки с целым числом
        """
        chip = Chip(10)
        result = chip + 5
        assert result.value == 15

    def test_add_chip_and_float(self) -> None:
        """
        Проверяет сложение фишки с вещественным числом
        """
        chip = Chip(10)
        result = chip + 5.7
        assert result.value == 15

    def test_add_invalid_type_raises(self) -> None:
        """
        Проверяет ошибку при сложении с некорректным типом
        """
        chip: Any = Chip(10)
        with pytest.raises(ValidationError):
            _ = chip + "abc"

    def test_sub_two_chips(self) -> None:
        """
        Проверяет вычитание двух фишек
        """
        c1 = Chip(20)
        c2 = Chip(5)
        result = c1 - c2
        assert result.value == 15

    def test_sub_result_cannot_be_negative(self) -> None:
        """
        Проверяет, что результат вычитания не может быть отрицательным
        """
        c1 = Chip(5)
        c2 = Chip(10)
        result = c1 - c2
        assert result.value == 0

    def test_sub_chip_and_int(self) -> None:
        """
        Проверяет вычитание целого числа из фишки
        """
        chip = Chip(20)
        result = chip - 5
        assert result.value == 15

    def test_sub_invalid_type_raises(self) -> None:
        """
        Проверяет ошибку при вычитании некорректного типа
        """
        chip: Any = Chip(10)
        with pytest.raises(ValidationError):
            _ = chip - "abc"

    def test_repr_denomination_one(self) -> None:
        """
        Проверяет строковое представление фишки с номиналом 1
        """
        chip = Chip(10)
        assert repr(chip) == "Фишка(10)"

    def test_repr_with_denomination(self) -> None:
        """
        Проверяет строковое представление фишки с номиналом больше 1
        """
        chip = Chip(5, 2)
        assert repr(chip) == "(5x2=10)"
