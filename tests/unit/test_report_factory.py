import pytest
from src.reports import ReportFactory
from src.reports.performance_report import PerformanceReport


class TestReportFactory:
    """Тесты для фабрики отчётов."""

    def test_create_report_success(self):
        """Тест успешного создания отчёта."""
        report = ReportFactory.create_report('performance')

        assert isinstance(report, PerformanceReport)
        assert report.get_name() == 'performance'

    def test_create_report_case_insensitive(self):
        """Тест создания отчёта без учёта регистра."""
        report1 = ReportFactory.create_report('PERFORMANCE')
        report2 = ReportFactory.create_report('Performance')
        report3 = ReportFactory.create_report('performance')

        assert isinstance(report1, PerformanceReport)
        assert isinstance(report2, PerformanceReport)
        assert isinstance(report3, PerformanceReport)

    def test_create_report_nonexistent(self):
        """Тест создания несуществующего отчёта."""
        with pytest.raises(ValueError, match='не найден'):
            ReportFactory.create_report('nonexistent')

    def test_get_available_reports(self):
        """Тест получения списка доступных отчётов."""
        reports = ReportFactory.get_available_reports()

        assert isinstance(reports, list)
        assert 'performance' in reports

    def test_register_new_report(self):
        """Тест регистрации нового отчёта."""

        # Создаём тестовый класс отчёта
        class TestReport:
            def get_name(self):
                return 'test'

        # Регистрируем новый отчёт
        ReportFactory.register_report('test', TestReport)

        # Проверяем, что он появился в списке доступных
        reports = ReportFactory.get_available_reports()
        assert 'test' in reports

        # Создаём экземпляр нового отчёта
        report = ReportFactory.create_report('test')
        assert isinstance(report, TestReport)
        assert report.get_name() == 'test'