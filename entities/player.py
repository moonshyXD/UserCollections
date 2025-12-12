from entities.chip import Chip


class Player:
    def __init__(self, name: str, balance: int) -> None:
        """
        Инициализировать игрока
        :param name: Имя игрока
        :param balance: Начальный баланс игрока в фишках
        """
        self._name = name
        self._balance = Chip(balance)

    @property
    def balance(self) -> Chip:
        """
        Получить баланс игрока
        :return: Объект фишки с балансом игрока
        """
        return self._balance

    @property
    def name(self) -> str:
        """
        Получить имя игрока
        :return: Имя игрока
        """
        return self._name

    def __repr__(self) -> str:
        """
        Получить строковое представление игрока
        :return: Строка с именем игрока и балансом
        """
        return f"Игрок: {self.name} Баланс: {self.balance.value}"
