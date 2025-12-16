from typing import List, Dict
from tabulate import tabulate


class ReportFormatter:
    """Класс для форматирования отчётов в таблицу."""

    @staticmethod
    def format_table(report_data: List[Dict], headers=None) -> str:
        """
        Форматирует данные отчёта в таблицу.

        Args:
            report_data: Данные отчёта (список словарей)
            headers: Заголовки столбцов (ключи словаря, если не указаны)

        Returns:
            Отформатированная таблица в виде строки
        """
        if not report_data:
            return "Нет данных для отображения"

        # Преобразуем список словарей в список списков
        table_data = []
        for row in report_data:
            table_data.append(list(row.values()))

        # Используем ключи первого словаря как заголовки, если не указаны другие
        if headers is None:
            headers = list(report_data[0].keys())

        return tabulate(table_data, headers=headers, tablefmt="grid")
