import pytest

from src.reports import ReportFactory
from src.reports.performance_report import PerformanceReport


class TestReportFactory:
    """Тесты фабрики отчётов."""

    def test_create_report_success(self):
        """Успешное создание экземпляра отчёта."""
        report = ReportFactory.create_report("performance")
        assert isinstance(report, PerformanceReport)
        assert report.get_name() == "performance"

    def test_create_report_case_insensitive(self):
        """Создание отчёта вне зависимости от регистра имени."""
        reports = [
            ReportFactory.create_report("PERFORMANCE"),
            ReportFactory.create_report("Performance"),
            ReportFactory.create_report("performance"),
        ]
        for report in reports:
            assert isinstance(report, PerformanceReport)

    def test_create_report_nonexistent(self):
        """Обработка запроса на создание неизвестного отчёта."""
        with pytest.raises(ValueError, match="не найден"):
            ReportFactory.create_report("nonexistent")

    def test_get_available_reports(self):
        """Проверка получения списка зарегистрированных отчётов."""
        reports = ReportFactory.get_available_reports()
        assert isinstance(reports, list)
        assert "performance" in reports

    def test_register_new_report(self):
        """Динамическая регистрация нового типа отчёта."""

        class TestReport:
            def get_name(self):
                return "test"

        ReportFactory.register_report("test", TestReport)

        assert "test" in ReportFactory.get_available_reports()

        report = ReportFactory.create_report("test")
        assert isinstance(report, TestReport)
        assert report.get_name() == "test"
