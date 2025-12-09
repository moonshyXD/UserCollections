import pytest

from entities.chip import Chip
from entities.errors import ValidationError


class TestChip:
    def test_init_positive_value(self):
        chip = Chip(100)
        assert chip.value == 100
        assert chip.denomination == 1

    def test_init_negative_value_becomes_zero(self):
        chip = Chip(-50)
        assert chip.value == 0

    def test_init_with_denomination(self):
        chip = Chip(10, denomination=5)
        assert chip.value == 10
        assert chip.denomination == 5
        assert chip.total == 50

    def test_add_chip_to_chip(self):
        chip1 = Chip(100)
        chip2 = Chip(50)
        result = chip1 + chip2
        assert result.value == 150
        assert result.denomination == 1

    def test_add_int_to_chip(self):
        chip = Chip(100)
        result = chip + 50
        assert result.value == 150

    def test_add_float_to_chip(self):
        chip = Chip(100)
        result = chip + 50.7
        assert result.value == 150

    def test_add_invalid_type_raises_error(self):
        chip = Chip(100)
        with pytest.raises(ValidationError):
            chip + "invalid"

    def test_sub_chip_from_chip(self):
        chip1 = Chip(100)
        chip2 = Chip(30)
        result = chip1 - chip2
        assert result.value == 70

    def test_sub_more_than_available_returns_zero(self):
        chip = Chip(50)
        result = chip - 100
        assert result.value == 0

    def test_sub_int_from_chip(self):
        chip = Chip(100)
        result = chip - 40
        assert result.value == 60

    def test_sub_float_from_chip(self):
        chip = Chip(100)
        result = chip - 30.8
        assert result.value == 70

    def test_sub_invalid_type_raises_error(self):
        chip = Chip(100)
        with pytest.raises(ValidationError):
            chip - "invalid"

    def test_repr_without_denomination(self):
        chip = Chip(100)
        assert repr(chip) == "Фишка(100)"

    def test_repr_with_denomination(self):
        chip = Chip(10, denomination=5)
        assert repr(chip) == "Фишка (10x5=50)"
