import pytest
from src.core.analyzer import DataAnalyzer


class TestDataAnalyzer:
    """Тесты для класса DataAnalyzer."""

    @pytest.fixture
    def sample_data(self, sample_csv_data):
        """Фикстура с тестовыми данными."""
        return sample_csv_data

    def test_group_by_position(self, sample_data):
        """Тест группировки данных по должностям."""
        grouped = DataAnalyzer.group_by_position(sample_data)

        assert isinstance(grouped, dict)
        assert len(grouped) == 5  # 5 уникальных должностей

        # Проверяем, что данные сгруппированы правильно
        assert 'Backend Developer' in grouped
        assert len(grouped['Backend Developer']) == 1
        assert grouped['Backend Developer'][0]['name'] == 'Alex Ivanov'

    def test_group_by_position_empty_data(self):
        """Тест группировки пустых данных."""
        grouped = DataAnalyzer.group_by_position([])
        assert grouped == {}

    def test_group_by_position_missing_field(self):
        """Тест группировки данных с отсутствующим полем position."""
        data = [
            {'name': 'Test', 'performance': '4.5'},
            {'name': 'Test2', 'position': 'Developer', 'performance': '4.6'}
        ]

        grouped = DataAnalyzer.group_by_position(data)

        # Запись без position должна быть пропущена
        assert 'Developer' in grouped
        assert len(grouped) == 1

    def test_calculate_average_performance(self, sample_data):
        """Тест расчёта средней эффективности."""
        results = DataAnalyzer.calculate_average_performance(sample_data)

        assert isinstance(results, list)
        assert len(results) == 5  # 5 должностей

        # Проверяем структуру результата
        for result in results:
            assert 'position' in result
            assert 'avg_performance' in result
            assert 'employee_count' in result
            assert isinstance(result['avg_performance'], float)
            assert isinstance(result['employee_count'], int)

        # Находим DevOps Engineer (должен иметь самую высокую эффективность)
        devops_result = next(r for r in results if r['position'] == 'DevOps Engineer')
        assert devops_result['avg_performance'] == 4.9
        assert devops_result['employee_count'] == 1

    def test_calculate_average_performance_empty_data(self):
        """Тест расчёта средней эффективности для пустых данных."""
        results = DataAnalyzer.calculate_average_performance([])
        assert results == []

    def test_calculate_average_performance_invalid_values(self):
        """Тест расчёта с некорректными значениями performance."""
        data = [
            {'position': 'Developer', 'performance': '4.5'},
            {'position': 'Developer', 'performance': 'invalid'},
            {'position': 'Developer', 'performance': ''},
            {'position': 'Developer'},  # Нет поля performance
            {'position': 'QA', 'performance': '4.8'}
        ]

        results = DataAnalyzer.calculate_average_performance(data)

        # Только Developer и QA с валидными значениями
        # Developer: только одно валидное значение 4.5
        # QA: одно валидное значение 4.8
        assert len(results) == 2

        # Сортируем результаты для стабильности теста
        results.sort(key=lambda x: x['position'])

        # Проверяем Developer (только одно валидное значение)
        assert results[0]['position'] == 'Developer'
        assert results[0]['avg_performance'] == 4.5
        assert results[0]['employee_count'] == 1

        # Проверяем QA
        assert results[1]['position'] == 'QA'
        assert results[1]['avg_performance'] == 4.8
        assert results[1]['employee_count'] == 1

    def test_calculate_average_performance_multiple_same_position(self):
        """Тест расчёта средней эффективности для нескольких сотрудников на одной должности."""
        data = [
            {'position': 'Developer', 'performance': '4.5'},
            {'position': 'Developer', 'performance': '4.7'},
            {'position': 'Developer', 'performance': '4.9'},
            {'position': 'QA', 'performance': '4.8'}
        ]

        results = DataAnalyzer.calculate_average_performance(data)

        dev_result = next(r for r in results if r['position'] == 'Developer')
        assert dev_result['avg_performance'] == pytest.approx((4.5 + 4.7 + 4.9) / 3, 0.01)
        assert dev_result['employee_count'] == 3

    def test_calculate_average_performance_rounding(self):
        """Тест округления средней эффективности."""
        data = [
            {'position': 'Developer', 'performance': '4.555'},
            {'position': 'Developer', 'performance': '4.666'}
        ]

        results = DataAnalyzer.calculate_average_performance(data)
        assert len(results) == 1
        dev_result = results[0]

        # Ожидаем округление до 2 знаков
        # (4.555 + 4.666) / 2 = 4.6105 -> округляем до 4.61
        assert dev_result['avg_performance'] == 4.61
        assert dev_result['employee_count'] == 2