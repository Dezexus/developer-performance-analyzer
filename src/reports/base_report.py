from abc import ABC, abstractmethod
from typing import List

from src.core.types import DeveloperRecord, ReportResult


class BaseReport(ABC):
    """Базовый класс для генерации отчётов."""

    @abstractmethod
    def generate(self, data: List[DeveloperRecord]) -> List[ReportResult]:
        """Генерация данных отчёта."""
        pass

    @abstractmethod
    def get_name(self) -> str:
        """Получение идентификатора отчёта."""
        pass
