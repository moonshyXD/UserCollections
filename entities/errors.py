class CasinoError(Exception):
    """Базовое исключение для ошибок казино"""

    pass


class EntitiesError(CasinoError):
    """Исключение для ошибок сущностей казино"""

    pass


class ValidationError(CasinoError):
    """Исключение для ошибок валидации"""

    pass
