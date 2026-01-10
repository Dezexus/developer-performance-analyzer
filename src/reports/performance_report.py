from typing import List

from src.core.analyzer import DataAnalyzer
from src.core.types import DeveloperRecord, ReportResult

from .base_report import BaseReport


class PerformanceReport(BaseReport):
    """Отчёт по средней эффективности по должностям."""

    def __init__(self) -> None:
        self.name = "performance"

    def generate(self, data: List[DeveloperRecord]) -> List[ReportResult]:
        """Расчёт средней эффективности с сортировкой по убыванию."""
        results = DataAnalyzer.calculate_average_performance(data)
        results.sort(key=lambda x: x["avg_performance"], reverse=True)
        return results

    def get_name(self) -> str:
        return self.name
