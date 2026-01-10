import pytest

from src.core.validator import Validator


class TestValidator:
    """Тесты валидации входных данных."""

    @pytest.mark.parametrize(
        "report_name, is_valid",
        [
            ("performance", True),
            ("PERFORMANCE", True),
            ("Performance", True),
            ("", False),
            ("invalid_report", False),
            ("nonexistent", False),
        ],
    )
    def test_validate_report_name(self, report_name, is_valid):
        """Проверка валидации имен доступных отчётов."""
        if is_valid:
            assert Validator.validate_report_name(report_name) == "performance"
        else:
            with pytest.raises(ValueError, match="не поддерживается"):
                Validator.validate_report_name(report_name)

    @pytest.mark.parametrize(
        "file_paths, expected_count, should_raise",
        [
            (["test1.txt", "test2.txt"], 2, False),
            (["test1.txt", "missing.txt"], 1, False),
            (["fake1.txt", "fake2.txt"], 0, True),
            ([], 0, True),
        ],
    )
    def test_validate_files(self, tmp_path, file_paths, expected_count, should_raise):
        """Проверка валидации существования файлов."""
        prepared_paths = []
        for i, path in enumerate(file_paths):
            if path.startswith("test"):
                test_file = tmp_path / path
                test_file.write_text(f"content {i}")
                prepared_paths.append(str(test_file))
            else:
                prepared_paths.append(path)

        if should_raise:
            with pytest.raises(ValueError, match="Не найдено ни одного"):
                Validator.validate_files(prepared_paths)
        else:
            valid_files = Validator.validate_files(prepared_paths)
            assert len(valid_files) == expected_count
