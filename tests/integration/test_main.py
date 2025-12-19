import pytest
import sys
import tempfile
import csv
import os
from unittest.mock import patch
from src.main import main


class TestMainIntegration:
    """Интеграционные тесты для основного приложения."""

    def test_main_success(self, capsys):
        """Тест успешного выполнения основного скрипта."""
        # Создаём временный файл
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            writer = csv.writer(f)
            writer.writerow(['name', 'position', 'performance'])
            writer.writerow(['Alex', 'Developer', '4.8'])
            writer.writerow(['Maria', 'QA', '4.7'])
            file_path = f.name

        test_args = ['script.py', '--files', file_path, '--report', 'performance']

        with patch.object(sys, 'argv', test_args):
            main()

        captured = capsys.readouterr()
        output = captured.out

        assert 'Отчёт: performance' in output
        assert 'Developer' in output or 'QA' in output

        os.unlink(file_path)

    def test_main_multiple_files(self, capsys):
        """Тест выполнения с несколькими файлами."""
        files = []
        for i in range(2):
            with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
                writer = csv.writer(f)
                writer.writerow(['name', 'position', 'performance'])
                writer.writerow([f'Dev{i}', 'Developer', '4.5'])
                files.append(f.name)

        test_args = ['script.py', '--files'] + files + ['--report', 'performance']

        with patch.object(sys, 'argv', test_args):
            main()

        captured = capsys.readouterr()
        output = captured.out

        assert 'Отчёт: performance' in output

        for file_path in files:
            os.unlink(file_path)

    def test_main_file_not_found(self, capsys):
        """Тест выполнения с несуществующим файлом."""
        test_args = ['script.py', '--files', 'nonexistent.csv', '--report', 'performance']

        with patch.object(sys, 'argv', test_args):
            with pytest.raises(SystemExit):
                main()

        captured = capsys.readouterr()
        output = captured.out
        assert 'Ошибка' in output

    def test_main_invalid_report(self, capsys):
        """Тест выполнения с неверным именем отчёта."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            writer = csv.writer(f)
            writer.writerow(['name', 'position', 'performance'])
            writer.writerow(['Test', 'Dev', '4.5'])
            file_path = f.name

        test_args = ['script.py', '--files', file_path, '--report', 'invalid_report']

        with patch.object(sys, 'argv', test_args):
            with pytest.raises(SystemExit):
                main()

        os.unlink(file_path)

    def test_main_empty_files(self, capsys):
        """Тест выполнения с пустыми файлами."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            writer = csv.writer(f)
            writer.writerow(['name', 'position', 'performance'])
            file_path = f.name

        test_args = ['script.py', '--files', file_path, '--report', 'performance']

        with patch.object(sys, 'argv', test_args):
            with pytest.raises(SystemExit):
                main()

        os.unlink(file_path)