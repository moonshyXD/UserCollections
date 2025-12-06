class CasinoError(Exception):
    pass


class EntitiesError(CasinoError):
    pass


class ValidationError(CasinoError):
    pass
