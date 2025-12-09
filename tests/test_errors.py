import pytest

from entities.errors import CasinoError, EntitiesError, ValidationError


class TestErrors:
    def test_casino_error(self):
        with pytest.raises(CasinoError):
            raise CasinoError("Test error")

    def test_entities_error_is_casino_error(self):
        assert issubclass(EntitiesError, CasinoError)

    def test_validation_error_is_casino_error(self):
        assert issubclass(ValidationError, CasinoError)
