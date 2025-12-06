import logging


class Logger:
    @staticmethod
    def setup_logging() -> None:
        """
        Настраивает логирование
        """
        logging.basicConfig(
            filename="shell.log",
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
