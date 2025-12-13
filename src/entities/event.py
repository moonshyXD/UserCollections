from abc import ABC, abstractmethod

from src.entities.protocols import Casino, Logger


class BaseEvent(ABC):
    @staticmethod
    @abstractmethod
    def execute(casino: Casino, logger: Logger) -> None: ...
