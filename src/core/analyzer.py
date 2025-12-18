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

    @staticmethod
    def filter_by_skill(data: List[Dict], skill: str) -> List[Dict]:
        """
        Фильтрует разработчиков по наличию навыка.

        Args:
            data: Список словарей с данными разработчиков
            skill: Навык для поиска

        Returns:
            Отфильтрованный список разработчиков
        """
        filtered = []
        skill_lower = skill.lower().strip()

        for record in data:
            skills_str = record.get('skills', '')
            if skill_lower in skills_str.lower():
                filtered.append(record)

        return filtered

    @staticmethod
    def get_statistics(data: List[Dict]) -> Dict[str, Any]:
        """
        Возвращает общую статистику по данным.

        Args:
            data: Список словарей с данными разработчиков

        Returns:
            Словарь со статистикой
        """
        if not data:
            return {}

        total_employees = len(data)

        # Собираем все валидные значения performance
        performances = []
        for record in data:
            performance_value = record.get('performance', '').strip()
            if performance_value:
                try:
                    perf = float(performance_value)
                    performances.append(perf)
                except (ValueError, TypeError):
                    continue

        stats = {
            'total_employees': total_employees,
            'total_performance_records': len(performances),
        }

        if performances:
            stats.update({
                'avg_performance': round(mean(performances), 2),
                'min_performance': min(performances),
                'max_performance': max(performances)
            })

        return stats