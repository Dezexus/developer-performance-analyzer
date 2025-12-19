from collections import defaultdict
from typing import List, Dict, Any
from statistics import mean


class DataAnalyzer:
    """Класс для анализа данных разработчиков."""

    @staticmethod
    def group_by_position(data: List[Dict]) -> Dict[str, List[Dict]]:
        """
        Группирует данные по должностям.

        Args:
            data: Список словарей с данными разработчиков

        Returns:
            Словарь с ключами-должностями и значениями-списками записей
        """
        grouped = defaultdict(list)
        for record in data:
            position = record.get('position', '').strip()
            if position:
                grouped[position].append(record)
        return dict(grouped)

    @staticmethod
    def calculate_average_performance(data: List[Dict]) -> List[Dict[str, Any]]:
        """
        Рассчитывает среднюю эффективность по должностям.

        Args:
            data: Список словарей с данными разработчиков

        Returns:
            Список словарей с должностями и средней эффективностью
        """
        grouped_data = DataAnalyzer.group_by_position(data)
        results = []

        for position, records in grouped_data.items():
            performances = []
            for record in records:
                performance_value = record.get('performance', '').strip()
                if performance_value:  # Проверяем, что значение не пустое
                    try:
                        perf = float(performance_value)
                        performances.append(perf)
                    except (ValueError, TypeError):
                        # Пропускаем некорректные значения
                        continue

            if performances:  # Проверяем, что есть хотя бы одно валидное значение
                avg_perf = mean(performances)
                results.append({
                    'position': position,
                    'avg_performance': round(avg_perf, 2)
                })

        return results