import logging

from src.entities.protocols import LoggerProtocol


class Logger(LoggerProtocol):
    @staticmethod
    def setup_logging() -> None:
        """
        Настраивает логирование
        """
        logging.basicConfig(
            filename="casino.log",
            level=logging.INFO,
            format="[%(asctime)s] %(levelname)s: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

    @staticmethod
    def start_execution(command: str) -> None:
        """
        Логирует начало выполнения команды
        :param command: Команда для логирования
        """
        logging.info(f"STARTED: {command}")

    @staticmethod
    def success_execution(command: str) -> None:
        """
        Логирует успешное выполнение команды
        :param command: Команда для логирования
        """
        logging.info(f"SUCCESS: {command}")

    @staticmethod
    def failure_execution(message: Exception) -> None:
        """
        Логирует ошибку выполнения команды
        :param message: Сообщение об ошибке
        """
        logging.error(f"{type(message).__name__}: {message}")

    @staticmethod
    def event_start(event_name: str) -> None:
        """
        Логирует начало события казино
        :param event_name: Название события
        """
        logging.info(f"EVENT-START: {event_name}")

    @staticmethod
    def balance_change(player: str, old: int, new: int) -> None:
        """
        Логирует изменение баланса
        :param player: Имя игрока
        :param old: Старый баланс
        :param new: Новый баланс
        """
        logging.info(f"BALANCE: {player}: {old} → {new}")

    @staticmethod
    def chip_added(chip_value: int, reason: str) -> None:
        """
        Логирует добавление фишки в историю
        :param chip_value: Значение фишки
        :param reason: Причина добавления
        """
        logging.info(f"CHIP: Фишка({chip_value}) - {reason}")

    @staticmethod
    def entity_removed(entity_type: str, name: str, details: str = "") -> None:
        """
        Логирует удаление сущности
        :param entity_type: Тип объекта
        :param name: Имя
        :param details: Дополнительные детали
        """
        logging.info(f"REMOVED: {entity_type} {name} {details}")
