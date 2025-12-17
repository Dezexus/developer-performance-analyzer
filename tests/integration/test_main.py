import pytest
import sys
import tempfile
import csv
from unittest.mock import patch
from src.main import main


class TestMainIntegration:
    """Интеграционные тесты для основного приложения."""

    @pytest.fixture
    def sample_csv_content(self):
        """Фикстура с содержимым CSV."""
        return """name,position,completed_tasks,performance,skills,team,experience_years
Alex Ivanov,Backend Developer,45,4.8,"Python, Django, PostgreSQL, Docker",API Team,5
Maria Petrova,Frontend Developer,38,4.7,"React, TypeScript, Redux, CSS",Web Team,4
John Smith,Data Scientist,29,4.6,"Python, ML, SQL, Pandas",AI Team,3"""

    def test_main_success(self, sample_csv_content, capsys):
        """Тест успешного выполнения основного скрипта."""
        # Создаём временный файл
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            f.write(sample_csv_content)
            file_path = f.name

        # Мокаем sys.argv
        test_args = ['script.py', '--files', file_path, '--report', 'performance']

        with patch.object(sys, 'argv', test_args):
            # Запускаем main
            main()

        # Проверяем вывод
        captured = capsys.readouterr()
        output = captured.out

        assert 'Отчёт: performance' in output
        assert 'Backend Developer' in output
        assert 'Frontend Developer' in output
        assert 'Data Scientist' in output
        assert '4.8' in output
        assert '4.7' in output
        assert '4.6' in output

    def test_main_multiple_files(self, capsys):
        """Тест выполнения с несколькими файлами."""
        # Создаём два временных файла
        files = []
        for i in range(2):
            with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
                writer = csv.DictWriter(f, fieldnames=['name', 'position', 'performance'])
                writer.writeheader()
                writer.writerow({'name': f'Dev{i}', 'position': 'Developer', 'performance': '4.5'})
                files.append(f.name)

        # Мокаем sys.argv
        test_args = ['script.py', '--files'] + files + ['--report', 'performance']

        with patch.object(sys, 'argv', test_args):
            main()

        # Проверяем вывод
        captured = capsys.readouterr()
        output = captured.out

        assert 'Отчёт: performance' in output
        assert 'Developer' in output
        assert '4.5' in output

        # Очищаем временные файлы
        for file_path in files:
            import os
            os.unlink(file_path)

    def test_main_file_not_found(self, capsys):
        """Тест выполнения с несуществующим файлом."""
        test_args = ['script.py', '--files', 'nonexistent.csv', '--report', 'performance']

        with patch.object(sys, 'argv', test_args):
            # Ожидаем SystemExit с кодом 1
            with pytest.raises(SystemExit) as exc_info:
                main()

        # Проверяем код выхода
        assert exc_info.value.code == 1

        # Проверяем вывод
        captured = capsys.readouterr()
        output = captured.out

        assert 'Ошибка' in output

    def test_main_invalid_report(self, capsys):
        """Тест выполнения с неверным именем отчёта."""
        # Создаём временный файл
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            writer = csv.DictWriter(f, fieldnames=['name', 'position', 'performance'])
            writer.writeheader()
            writer.writerow({'name': 'Test', 'position': 'Dev', 'performance': '4.5'})
            file_path = f.name

        test_args = ['script.py', '--files', file_path, '--report', 'invalid_report']

        with patch.object(sys, 'argv', test_args):
            # Ожидаем SystemExit с кодом 1
            with pytest.raises(SystemExit) as exc_info:
                main()

        # Проверяем код выхода
        assert exc_info.value.code == 1

        # Проверяем вывод
        captured = capsys.readouterr()
        output = captured.out

        assert 'Ошибка' in output

        # Очищаем временный файл
        import os
        os.unlink(file_path)

    def test_main_empty_files(self, capsys):
        """Тест выполнения с пустыми файлами."""
        # Создаём пустой файл
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            writer = csv.DictWriter(f, fieldnames=['name', 'position', 'performance'])
            writer.writeheader()
            file_path = f.name

        test_args = ['script.py', '--files', file_path, '--report', 'performance']

        with patch.object(sys, 'argv', test_args):
            # Ожидаем SystemExit с кодом 1
            with pytest.raises(SystemExit) as exc_info:
                main()

        # Проверяем код выхода
        assert exc_info.value.code == 1

        # Проверяем вывод
        captured = capsys.readouterr()
        output = captured.out

        assert 'Ошибка' in output

        # Очищаем временный файл
        import os
        os.unlink(file_path)

    def test_main_unexpected_error(self, capsys):
        """Тест обработки непредвиденной ошибки."""
        # Мокаем CLIParser.parse_args чтобы вызвать исключение
        with patch('src.main.CLIParser.parse_args', side_effect=Exception('Test error')):
            with patch.object(sys, 'argv', ['script.py']):
                # Ожидаем SystemExit с кодом 1
                with pytest.raises(SystemExit) as exc_info:
                    main()

        # Проверяем код выхода
        assert exc_info.value.code == 1

        # Проверяем вывод
        captured = capsys.readouterr()
        output = captured.out

        assert 'Непредвиденная ошибка' in output
        assert 'Test error' in output