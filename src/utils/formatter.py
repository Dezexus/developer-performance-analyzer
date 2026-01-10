from typing import Any, Dict, List, Optional

from tabulate import tabulate


class ReportFormatter:
    """Форматирование отчётов в табличный вид."""

    @staticmethod
    def format_table(report_data: List[Dict[str, Any]], headers: Optional[List[str]] = None) -> str:
        """Преобразует список словарей в форматированную таблицу."""
        if not report_data:
            return "Нет данных для отображения"

        table_data = [list(row.values()) for row in report_data]

        if headers is None:
            headers = list(report_data[0].keys())

        return tabulate(table_data, headers=headers, tablefmt="grid")
