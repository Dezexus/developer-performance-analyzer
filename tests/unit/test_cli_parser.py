import pytest
from src.cli.parser import CLIParser


class TestCLIParser:
    """Тесты для класса CLIParser."""

    @pytest.mark.parametrize("test_args, expected_files, expected_report", [
        # Разные комбинации файлов
        (['--files', 'file1.csv', '--report', 'performance'], ['file1.csv'], 'performance'),
        (['--files', 'file1.csv', 'file2.csv', '--report', 'performance'],
         ['file1.csv', 'file2.csv'], 'performance'),
        (['--files', 'file1.csv', 'file2.csv', 'file3.csv', 'file4.csv', '--report', 'performance'],
         ['file1.csv', 'file2.csv', 'file3.csv', 'file4.csv'], 'performance'),
    ])
    def test_parse_args_success_various_cases(self, test_args, expected_files, expected_report):
        """Параметризованный тест успешного парсинга аргументов."""
        args = CLIParser.parse_args(test_args)
        assert args.files == expected_files
        assert args.report == expected_report

    @pytest.mark.parametrize("test_args", [
        ['--report', 'performance'],  # нет --files
        ['--files', 'file1.csv'],  # нет --report
        [],  # нет аргументов
    ])
    def test_parse_args_missing_required(self, test_args):
        """Параметризованный тест отсутствия обязательных аргументов."""
        with pytest.raises(SystemExit):
            CLIParser.parse_args(test_args)