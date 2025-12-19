import pytest
from src.core.analyzer import DataAnalyzer


class TestDataAnalyzer:
    """Тесты для класса DataAnalyzer."""

    # Убираем старую фикстуру sample_data - она больше не нужна

    def test_group_by_position(self, sample_csv_data):
        """Тест группировки данных по должностям."""
        grouped = DataAnalyzer.group_by_position(sample_csv_data)

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

    def test_calculate_average_performance(self, sample_csv_data):
        """Тест расчёта средней эффективности."""
        results = DataAnalyzer.calculate_average_performance(sample_csv_data)

        assert isinstance(results, list)
        assert len(results) == 5  # 5 должностей

        # Проверяем структуру результата
        for result in results:
            assert 'position' in result
            assert 'avg_performance' in result
            assert isinstance(result['avg_performance'], float)

        # Находим DevOps Engineer (должен иметь самую высокую эффективность)
        devops_result = next(r for r in results if r['position'] == 'DevOps Engineer')
        assert devops_result['avg_performance'] == 4.9

    def test_calculate_average_performance_empty_data(self):
        """Тест расчёта средней эффективности для пустых данных."""
        results = DataAnalyzer.calculate_average_performance([])
        assert results == []

    @pytest.mark.parametrize("test_data, expected_result", [
        # Тест 1: корректные данные
        (
                [
                    {'position': 'Developer', 'performance': '4.5'},
                    {'position': 'Developer', 'performance': '4.7'},
                    {'position': 'QA', 'performance': '4.8'}
                ],
                [
                    {'position': 'Developer', 'avg_performance': 4.6},
                    {'position': 'QA', 'avg_performance': 4.8}
                ]
        ),
        # Тест 2: дублирующиеся должности
        (
                [
                    {'position': 'Developer', 'performance': '4.5'},
                    {'position': 'Developer', 'performance': '4.7'},
                    {'position': 'QA', 'performance': '4.8'},
                    {'position': 'QA', 'performance': '4.9'}
                ],
                [
                    {'position': 'Developer', 'avg_performance': 4.6},
                    {'position': 'QA', 'avg_performance': 4.85}
                ]
        ),
        # Тест 3: некорректные значения
        (
                [
                    {'position': 'Developer', 'performance': '4.5'},
                    {'position': 'Developer', 'performance': 'invalid'},
                    {'position': 'QA', 'performance': '4.8'}
                ],
                [
                    {'position': 'Developer', 'avg_performance': 4.5},
                    {'position': 'QA', 'avg_performance': 4.8}
                ]
        ),
        # Тест 4: округление
        (
                [
                    {'position': 'Developer', 'performance': '4.555'},
                    {'position': 'Developer', 'performance': '4.666'}
                ],
                [
                    {'position': 'Developer', 'avg_performance': 4.61}
                ]
        ),
    ])
    def test_calculate_average_performance_various_cases(self, test_data, expected_result):
        """Параметризованный тест расчёта средней эффективности."""
        results = DataAnalyzer.calculate_average_performance(test_data)

        # Сортируем для сравнения
        results.sort(key=lambda x: x['position'])
        expected_result.sort(key=lambda x: x['position'])

        assert len(results) == len(expected_result)

        for i, (result, expected) in enumerate(zip(results, expected_result)):
            assert result['position'] == expected['position']
            assert result['avg_performance'] == pytest.approx(expected['avg_performance'], 0.01)

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