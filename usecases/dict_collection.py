from typing import Iterator

from entities.chip import Chip


class CasinoBalance:
    def __init__(self) -> None:
        """Инициализировать словарь балансов"""
        self._balance: dict[str, Chip] = {}

    def __setitem__(self, key: str, value: Chip | int) -> None:
        """
        Установить баланс для ключа
        :param key: Имя игрока или гуся
        :param value: Баланс в виде фишки или числа
        :raises ValidationError: Если значение не является фишкой или числом
        """
        if isinstance(value, int):
            value = Chip(value)

        self._balance[key] = value

    def __getitem__(self, key: str) -> Chip:
        """
        Получить баланс для ключа
        :param key: Имя игрока или гуся
        :return: Фишка
        """
        return self._balance[key]

    def __iter__(self) -> Iterator[tuple[str, Chip]]:
        """
        Получить итератор по парам ключ-значение
        :return: Итератор словаря балансов
        """
        return iter(self._balance.items())

    def __len__(self) -> int:
        """
        Получить количество балансов
        :return: Количество игроков или гусей с балансом
        """
        return len(self._balance)

    def __repr__(self) -> str:
        """
        Получить строковое представление балансов
        :return: Строка со словарем балансов
        """
        return str(self._balance)
