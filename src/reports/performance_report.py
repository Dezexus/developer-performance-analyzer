from typing import List, Dict
from .base_report import BaseReport
from src.core.analyzer import DataAnalyzer


class PerformanceReport(BaseReport):
    """Отчёт по средней эффективности по должностям."""

    def __init__(self):
        self.name = "performance"

    def generate(self, data: List[Dict]) -> List[Dict]:
        """
        Рассчитывает среднюю эффективность по каждой должности.

        Args:
            data: Список словарей с данными разработчиков

        Returns:
            Список словарей с должностями и средней эффективностью,
            отсортированный по убыванию эффективности
        """
        results = DataAnalyzer.calculate_average_performance(data)
        results.sort(key=lambda x: x['avg_performance'], reverse=True)

        return results

    def get_name(self) -> str:
        """Возвращает имя отчёта."""
        return self.name
