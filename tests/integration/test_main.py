import csv
import os
import sys
import tempfile
from unittest.mock import patch

import pytest

from src.main import main


class TestMainIntegration:
    """Интеграционные тесты приложения."""

    def test_main_success(self, capsys):
        """Успешный запуск с одним корректным файлом."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
            writer = csv.writer(f)
            writer.writerow(["name", "position", "performance"])
            writer.writerow(["Alex", "Developer", "4.8"])
            writer.writerow(["Maria", "QA", "4.7"])
            file_path = f.name

        test_args = ["script.py", "--files", file_path, "--report", "performance"]

        try:
            with patch.object(sys, "argv", test_args):
                main()

            output = capsys.readouterr().out
            assert "Отчёт: performance" in output
            assert "Developer" in output or "QA" in output
        finally:
            os.unlink(file_path)

    def test_main_multiple_files(self, capsys):
        """Запуск с объединением данных из нескольких файлов."""
        files = []
        for i in range(2):
            with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
                writer = csv.writer(f)
                writer.writerow(["name", "position", "performance"])
                writer.writerow([f"Dev{i}", "Developer", "4.5"])
                files.append(f.name)

        test_args = ["script.py", "--files"] + files + ["--report", "performance"]

        try:
            with patch.object(sys, "argv", test_args):
                main()

            output = capsys.readouterr().out
            assert "Отчёт: performance" in output
        finally:
            for file_path in files:
                os.unlink(file_path)

    def test_main_file_not_found(self, capsys):
        """Обработка ошибки при отсутствии указанного файла."""
        test_args = ["script.py", "--files", "nonexistent.csv", "--report", "performance"]

        with patch.object(sys, "argv", test_args), pytest.raises(SystemExit):
            main()

        assert "Ошибка" in capsys.readouterr().out

    def test_main_invalid_report(self, capsys):
        """Обработка ошибки при выборе несуществующего отчёта."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
            writer = csv.writer(f)
            writer.writerow(["name", "position", "performance"])
            writer.writerow(["Test", "Dev", "4.5"])
            file_path = f.name

        test_args = ["script.py", "--files", file_path, "--report", "invalid_report"]

        try:
            with patch.object(sys, "argv", test_args), pytest.raises(SystemExit):
                main()
        finally:
            os.unlink(file_path)

    def test_main_empty_files(self, capsys):
        """Обработка ситуации, когда файлы не содержат данных."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
            writer = csv.writer(f)
            writer.writerow(["name", "position", "performance"])
            file_path = f.name

        test_args = ["script.py", "--files", file_path, "--report", "performance"]

        try:
            with patch.object(sys, "argv", test_args), pytest.raises(SystemExit):
                main()
        finally:
            os.unlink(file_path)
