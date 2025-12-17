import pytest
from src.reports.performance_report import PerformanceReport
from src.reports.base_report import BaseReport


class TestPerformanceReport:
    """Тесты для класса PerformanceReport."""

    @pytest.fixture
    def report(self):
        """Фикстура с экземпляром отчёта."""
        return PerformanceReport()

    @pytest.fixture
    def sample_data(self, sample_csv_data):
        """Фикстура с тестовыми данными."""
        return sample_csv_data

    def test_report_inheritance(self, report):
        """Тест, что PerformanceReport наследует BaseReport."""
        assert isinstance(report, BaseReport)

    def test_get_name(self, report):
        """Тест получения имени отчёта."""
        assert report.get_name() == 'performance'

    def test_generate_report(self, report, sample_data):
        """Тест генерации отчёта."""
        results = report.generate(sample_data)

        assert isinstance(results, list)
        assert len(results) == 5

        # Проверяем структуру результата
        for result in results:
            assert 'position' in result
            assert 'avg_performance' in result
            assert len(result) == 2  # Только два поля по ТЗ

        # Проверяем сортировку по убыванию эффективности
        performances = [r['avg_performance'] for r in results]
        assert performances == sorted(performances, reverse=True)

        # Первый в списке должен быть DevOps Engineer с 4.9
        assert results[0]['position'] == 'DevOps Engineer'
        assert results[0]['avg_performance'] == 4.9

        # Последний должен быть QA Engineer с 4.5
        assert results[-1]['position'] == 'QA Engineer'
        assert results[-1]['avg_performance'] == 4.5

    def test_generate_report_empty_data(self, report):
        """Тест генерации отчёта с пустыми данными."""
        results = report.generate([])
        assert results == []

    def test_generate_report_duplicate_positions(self, report):
        """Тест генерации отчёта с дублирующимися должностями."""
        data = [
            {'position': 'Developer', 'performance': '4.5'},
            {'position': 'Developer', 'performance': '4.7'},
            {'position': 'QA', 'performance': '4.8'},
            {'position': 'QA', 'performance': '4.9'}
        ]

        results = report.generate(data)

        assert len(results) == 2

        # Проверяем сортировку
        assert results[0]['position'] == 'QA'  # (4.8 + 4.9) / 2 = 4.85
        assert results[0]['avg_performance'] == 4.85

        assert results[1]['position'] == 'Developer'  # (4.5 + 4.7) / 2 = 4.6
        assert results[1]['avg_performance'] == 4.6