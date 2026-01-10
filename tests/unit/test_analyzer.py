import pytest

from src.core.analyzer import DataAnalyzer


class TestDataAnalyzer:
    """Тесты бизнес-логики анализатора данных."""

    def test_group_by_position(self, sample_csv_data):
        """Проверка корректности группировки данных по должностям."""
        grouped = DataAnalyzer.group_by_position(sample_csv_data)

        assert isinstance(grouped, dict)
        assert len(grouped) == 5
        assert "Backend Developer" in grouped
        assert len(grouped["Backend Developer"]) == 1
        assert grouped["Backend Developer"][0]["name"] == "Alex Ivanov"

    def test_group_by_position_empty_data(self):
        """Группировка пустого списка данных."""
        assert DataAnalyzer.group_by_position([]) == {}

    def test_group_by_position_missing_field(self):
        """Пропуск записей с отсутствующим полем position."""
        data = [
            {"name": "Test", "performance": "4.5"},
            {"name": "Test2", "position": "Developer", "performance": "4.6"},
        ]
        grouped = DataAnalyzer.group_by_position(data)
        assert list(grouped.keys()) == ["Developer"]

    def test_calculate_average_performance(self, sample_csv_data):
        """Проверка расчёта среднего значения по должностям."""
        results = DataAnalyzer.calculate_average_performance(sample_csv_data)

        assert len(results) == 5
        for result in results:
            assert "position" in result
            assert isinstance(result["avg_performance"], float)

        devops = next(r for r in results if r["position"] == "DevOps Engineer")
        assert devops["avg_performance"] == 4.9

    @pytest.mark.parametrize(
        "test_data, expected",
        [
            (
                [
                    {"position": "Dev", "performance": "4.5"},
                    {"position": "Dev", "performance": "4.7"},
                    {"position": "QA", "performance": "4.8"},
                ],
                [
                    {"position": "Dev", "avg_performance": 4.6},
                    {"position": "QA", "avg_performance": 4.8},
                ],
            ),
            (
                [
                    {"position": "Dev", "performance": "4.5"},
                    {"position": "Dev", "performance": "invalid"},
                ],
                [{"position": "Dev", "avg_performance": 4.5}],
            ),
            (
                [
                    {"position": "Dev", "performance": "4.555"},
                    {"position": "Dev", "performance": "4.666"},
                ],
                [{"position": "Dev", "avg_performance": 4.61}],
            ),
        ],
    )
    def test_calculate_performance_scenarios(self, test_data, expected):
        """Параметризованная проверка различных сценариев расчёта."""
        results = DataAnalyzer.calculate_average_performance(test_data)

        results.sort(key=lambda x: x["position"])
        expected.sort(key=lambda x: x["position"])

        for res, exp in zip(results, expected):
            assert res["position"] == exp["position"]
            assert res["avg_performance"] == pytest.approx(exp["avg_performance"], 0.01)

    def test_performance_rounding(self):
        """Проверка округления результата до двух знаков."""
        data = [
            {"position": "Dev", "performance": "4.555"},
            {"position": "Dev", "performance": "4.666"},
        ]
        results = DataAnalyzer.calculate_average_performance(data)
        assert results[0]["avg_performance"] == 4.61
