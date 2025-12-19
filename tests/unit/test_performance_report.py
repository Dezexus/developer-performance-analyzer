import pytest
from src.reports.performance_report import PerformanceReport


class TestPerformanceReport:
    """Тесты для класса PerformanceReport."""

    @pytest.mark.parametrize("test_data, expected_results", [
        # Базовый тест
        (
                [
                    {'position': 'Developer', 'performance': '4.5'},
                    {'position': 'QA', 'performance': '4.8'},
                    {'position': 'Developer', 'performance': '4.7'},
                    {'position': 'QA', 'performance': '4.9'}
                ],
                [
                    {'position': 'QA', 'avg_performance': 4.85},
                    {'position': 'Developer', 'avg_performance': 4.6}
                ]
        ),
        # Сортировка по убыванию
        (
                [
                    {'position': 'A', 'performance': '4.5'},
                    {'position': 'B', 'performance': '4.9'},
                    {'position': 'C', 'performance': '4.7'}
                ],
                [
                    {'position': 'B', 'avg_performance': 4.9},
                    {'position': 'C', 'avg_performance': 4.7},
                    {'position': 'A', 'avg_performance': 4.5}
                ]
        ),
        # Пустые данные
        ([], []),
    ])
    def test_generate_report_various_cases(self, test_data, expected_results):
        """Параметризованный тест генерации отчётов."""
        report = PerformanceReport()
        results = report.generate(test_data)

        assert len(results) == len(expected_results)

        for i, (result, expected) in enumerate(zip(results, expected_results)):
            assert result['position'] == expected['position']
            assert result['avg_performance'] == pytest.approx(expected['avg_performance'], 0.01)