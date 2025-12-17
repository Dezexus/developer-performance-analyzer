import pytest
import tempfile
from pathlib import Path
from src.core.validator import Validator


class TestValidator:
    """Тесты для класса Validator."""

    def test_validate_files_success(self):
        """Тест успешной валидации существующих файлов."""
        # Создаём временные файлы
        temp_files = []
        for i in range(2):
            temp_file = tempfile.NamedTemporaryFile(suffix='.txt', delete=False)
            temp_files.append(temp_file.name)
            temp_file.close()

        try:
            valid_files = Validator.validate_files(temp_files)
            assert len(valid_files) == 2
            assert all(Path(f).exists() for f in valid_files)
        finally:
            # Очистка
            for file_path in temp_files:
                Path(file_path).unlink(missing_ok=True)

    def test_validate_files_with_nonexistent(self, capsys):
        """Тест валидации с несуществующими файлами."""
        # Создаём один реальный файл
        with tempfile.NamedTemporaryFile(suffix='.txt', delete=False) as f:
            real_file = f.name

        try:
            files = [real_file, 'non_existent_file.txt', 'another_fake.txt']

            valid_files = Validator.validate_files(files)

            # Должны получить только один файл
            assert len(valid_files) == 1
            assert valid_files[0] == real_file

            # Проверяем вывод предупреждений
            captured = capsys.readouterr()
            assert 'не найден' in captured.out
        finally:
            Path(real_file).unlink(missing_ok=True)

    def test_validate_files_all_nonexistent(self):
        """Тест валидации, когда все файлы не существуют."""
        files = ['fake1.txt', 'fake2.txt']

        with pytest.raises(ValueError, match='Не найдено ни одного существующего файла'):
            Validator.validate_files(files)

    def test_validate_files_empty_list(self):
        """Тест валидации пустого списка файлов."""
        with pytest.raises(ValueError, match='Не найдено ни одного существующего файла'):
            Validator.validate_files([])

    def test_validate_files_directory_instead_of_file(self, tmp_path):
        """Тест валидации, когда передан путь к директории вместо файла."""
        # Создаём директорию
        dir_path = tmp_path / "subdir"
        dir_path.mkdir()

        # Создаём реальный файл
        file_path = tmp_path / "real_file.txt"
        file_path.write_text("test")

        files = [str(dir_path), str(file_path)]

        valid_files = Validator.validate_files(files)

        # Должны получить только файл, директория должна быть пропущена
        assert len(valid_files) == 1
        assert valid_files[0] == str(file_path)

    def test_validate_report_name_success(self):
        """Тест успешной валидации имени отчёта."""
        # Только 'performance' доступен по умолчанию
        valid_name = Validator.validate_report_name('performance')
        assert valid_name == 'performance'

        # Проверяем case-insensitive
        valid_name = Validator.validate_report_name('PERFORMANCE')
        assert valid_name == 'performance'

    def test_validate_report_name_invalid(self):
        """Тест валидации несуществующего имени отчёта."""
        with pytest.raises(ValueError, match='не поддерживается'):
            Validator.validate_report_name('nonexistent_report')

    def test_validate_report_name_empty(self):
        """Тест валидации пустого имени отчёта."""
        with pytest.raises(ValueError, match='не поддерживается'):
            Validator.validate_report_name('')