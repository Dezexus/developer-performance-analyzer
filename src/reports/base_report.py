from abc import ABC, abstractmethod
from typing import List, Dict


class BaseReport(ABC):
    """Абстрактный базовый класс для всех отчётов."""

    @abstractmethod
    def generate(self, data: List[Dict]) -> List[Dict]:
        """
        Генерирует отчёт на основе данных.

        Args:
            data: Список словарей с исходными данными

        Returns:
            Список словарей с результатами отчёта
        """
        pass

    @abstractmethod
    def get_name(self) -> str:
        """Возвращает имя отчёта."""
        pass