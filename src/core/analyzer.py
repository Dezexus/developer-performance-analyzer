from collections import defaultdict
from statistics import mean
from typing import Dict, List

from src.core.types import DeveloperRecord, ReportResult


class DataAnalyzer:
    """Аналитика данных разработчиков."""

    @staticmethod
    def group_by_position(data: List[DeveloperRecord]) -> Dict[str, List[DeveloperRecord]]:
        """Группировка записей по должностям."""
        grouped = defaultdict(list)
        for record in data:
            position = record.get("position", "").strip()
            if position:
                grouped[position].append(record)
        return dict(grouped)

    @staticmethod
    def calculate_average_performance(data: List[DeveloperRecord]) -> List[ReportResult]:
        """Расчет средней эффективности по каждой должности."""
        grouped_data = DataAnalyzer.group_by_position(data)
        results: List[ReportResult] = []

        for position, records in grouped_data.items():
            performances = []
            for record in records:
                value = record.get("performance", "").strip()
                if not value:
                    continue

                try:
                    performances.append(float(value))
                except (ValueError, TypeError):
                    continue

            if performances:
                avg_val = round(mean(performances), 2)
                results.append({"position": position, "avg_performance": avg_val})

        return results
