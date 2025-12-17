import pytest
import sys
from src.cli.parser import CLIParser


class TestCLIParser:
    """Тесты для класса CLIParser."""

    def test_parse_args_success(self):
        """Тест успешного парсинга аргументов."""
        test_args = [
            '--files', 'file1.csv', 'file2.csv',
            '--report', 'performance'
        ]

        args = CLIParser.parse_args(test_args)

        assert args.files == ['file1.csv', 'file2.csv']
        assert args.report == 'performance'

    def test_parse_args_minimal(self):
        """Тест парсинга минимальных аргументов."""
        test_args = [
            '--files', 'single.csv',
            '--report', 'performance'
        ]

        args = CLIParser.parse_args(test_args)

        assert args.files == ['single.csv']
        assert args.report == 'performance'

    def test_parse_args_multiple_files(self):
        """Тест парсинга множества файлов."""
        test_args = [
            '--files', 'file1.csv', 'file2.csv', 'file3.csv', 'file4.csv',
            '--report', 'performance'
        ]

        args = CLIParser.parse_args(test_args)

        assert len(args.files) == 4
        assert args.files == ['file1.csv', 'file2.csv', 'file3.csv', 'file4.csv']

    def test_parse_args_missing_required(self):
        """Тест парсинга с отсутствующими обязательными аргументами."""
        # Не хватает --files
        test_args = [
            '--report', 'performance'
        ]

        with pytest.raises(SystemExit):
            CLIParser.parse_args(test_args)

        # Не хватает --report
        test_args = [
            '--files', 'file1.csv'
        ]

        with pytest.raises(SystemExit):
            CLIParser.parse_args(test_args)

    def test_parse_args_no_args(self):
        """Тест парсинга без аргументов."""
        test_args = []

        with pytest.raises(SystemExit):
            CLIParser.parse_args(test_args)

    def test_parse_args_help(self, capsys):
        """Тест вывода справки."""
        test_args = ['--help']

        with pytest.raises(SystemExit):
            CLIParser.parse_args(test_args)

        captured = capsys.readouterr()
        assert 'Анализ эффективности работы разработчиков' in captured.out
        assert '--files' in captured.out
        assert '--report' in captured.out

    def test_parse_args_real_sys_argv(self, monkeypatch):
        """Тест парсинга с реальными sys.argv."""
        # sys.argv включает имя скрипта первым аргументом
        monkeypatch.setattr(sys, 'argv', [
            'script.py',
            '--files', 'data.csv',
            '--report', 'performance'
        ])

        args = CLIParser.parse_args()  # Без аргументов, использует sys.argv

        assert args.files == ['data.csv']
        assert args.report == 'performance'