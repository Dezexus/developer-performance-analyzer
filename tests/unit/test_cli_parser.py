import pytest

from src.cli.parser import CLIParser


class TestCLIParser:
    """Тесты парсера аргументов командной строки."""

    @pytest.mark.parametrize(
        "test_args, expected_files, expected_report",
        [
            (["--files", "f1.csv", "--report", "performance"], ["f1.csv"], "performance"),
            (
                ["--files", "f1.csv", "f2.csv", "--report", "performance"],
                ["f1.csv", "f2.csv"],
                "performance",
            ),
            (
                ["--files", "f1.csv", "f2.csv", "f3.csv", "--report", "performance"],
                ["f1.csv", "f2.csv", "f3.csv"],
                "performance",
            ),
        ],
    )
    def test_parse_args_success(self, test_args, expected_files, expected_report):
        """Проверка успешного парсинга различных комбинаций аргументов."""
        args = CLIParser.parse_args(test_args)
        assert args.files == expected_files
        assert args.report == expected_report

    @pytest.mark.parametrize(
        "test_args",
        [
            ["--report", "performance"],
            ["--files", "file1.csv"],
            [],
        ],
    )
    def test_parse_args_missing_required(self, test_args):
        """Проверка реакции на отсутствие обязательных аргументов."""
        with pytest.raises(SystemExit):
            CLIParser.parse_args(test_args)
