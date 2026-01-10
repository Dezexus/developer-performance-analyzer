import pytest

from src.reports.performance_report import PerformanceReport


class TestPerformanceReport:
    """Тесты генерации отчёта по эффективности."""

    @pytest.mark.parametrize(
        "test_data, expected",
        [
            (
                [
                    {"position": "Developer", "performance": "4.5"},
                    {"position": "QA", "performance": "4.8"},
                    {"position": "Developer", "performance": "4.7"},
                    {"position": "QA", "performance": "4.9"},
                ],
                [
                    {"position": "QA", "avg_performance": 4.85},
                    {"position": "Developer", "avg_performance": 4.6},
                ],
            ),
            (
                [
                    {"position": "A", "performance": "4.5"},
                    {"position": "B", "performance": "4.9"},
                    {"position": "C", "performance": "4.7"},
                ],
                [
                    {"position": "B", "avg_performance": 4.9},
                    {"position": "C", "avg_performance": 4.7},
                    {"position": "A", "avg_performance": 4.5},
                ],
            ),
            ([], []),
        ],
    )
    def test_generate_report(self, test_data, expected):
        """Проверка корректности расчётов и сортировки в отчёте."""
        report = PerformanceReport()
        results = report.generate(test_data)

        assert len(results) == len(expected)

        for res, exp in zip(results, expected):
            assert res["position"] == exp["position"]
            assert res["avg_performance"] == pytest.approx(exp["avg_performance"], 0.01)
