import pytest
from src.core.validator import Validator


class TestValidator:
    """Тесты для класса Validator."""

    # Параметризация для тестов валидации имени отчёта
    @pytest.mark.parametrize("report_name, expected_valid, expected_message_contains", [
        # Успешные случаи
        ('performance', True, None),
        ('PERFORMANCE', True, None),
        ('Performance', True, None),
        # Неуспешные случаи
        ('', False, 'не поддерживается'),
        ('invalid_report', False, 'не поддерживается'),
        ('nonexistent', False, 'не поддерживается'),
    ])
    def test_validate_report_name(self, report_name, expected_valid, expected_message_contains):
        """Параметризованный тест валидации имени отчёта."""
        if expected_valid:
            valid_name = Validator.validate_report_name(report_name)
            assert valid_name == 'performance'
        else:
            with pytest.raises(ValueError) as exc_info:
                Validator.validate_report_name(report_name)
            if expected_message_contains:
                assert expected_message_contains in str(exc_info.value)

    # Параметризация для тестов валидации файлов
    @pytest.mark.parametrize("file_paths, should_exist_count, should_raise", [
        # Существующие файлы
        (['test1.txt', 'test2.txt'], 2, False),
        # Смесь существующих и несуществующих
        (['test1.txt', 'nonexistent.txt'], 1, False),
        # Все несуществующие
        (['fake1.txt', 'fake2.txt'], 0, True),
        # Пустой список
        ([], 0, True),
    ])
    def test_validate_files(self, tmp_path, file_paths, should_exist_count, should_raise):
        """Параметризованный тест валидации файлов."""
        # Создаём реальные файлы для теста
        real_files = []
        for i, path in enumerate(file_paths):
            if path.startswith('test'):
                real_file = tmp_path / path
                real_file.write_text(f"test content {i}")
                real_files.append(str(real_file))
            else:
                real_files.append(path)

        if should_raise:
            with pytest.raises(ValueError, match='Не найдено ни одного существующего файла'):
                Validator.validate_files(real_files)
        else:
            valid_files = Validator.validate_files(real_files)
            assert len(valid_files) == should_exist_count