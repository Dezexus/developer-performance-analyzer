from typing import Type

from .base_report import BaseReport
from .performance_report import PerformanceReport


class ReportFactory:
    """Фабрика для создания отчётов."""

    _reports = {
        "performance": PerformanceReport,
        # Другие отчёты можно будет добавить здесь в будущем
    }

    @classmethod
    def create_report(cls, report_name: str) -> BaseReport:
        """
        Создаёт экземпляр отчёта по имени.

        Args:
            report_name: Имя отчёта

        Returns:
            Экземпляр класса отчёта

        Raises:
            ValueError: Если отчёт с таким именем не найден
        """
        report_class = cls._reports.get(report_name.lower())
        if not report_class:
            raise ValueError(
                f"Отчёт '{report_name}' не найден. Доступные отчёты: {list(cls._reports.keys())}"
            )
        return report_class()

    @classmethod
    def register_report(cls, report_name: str, report_class: Type[BaseReport]) -> None:
        """
        Регистрирует новый тип отчёта.

        Args:
            report_name: Имя отчёта
            report_class: Класс отчёта (должен наследовать BaseReport)
        """
        cls._reports[report_name.lower()] = report_class

    @classmethod
    def get_available_reports(cls) -> list:
        """Возвращает список доступных отчётов."""
        return list(cls._reports.keys())
