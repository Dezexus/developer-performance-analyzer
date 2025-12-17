import pytest
from pathlib import Path
from src.data.reader import CSVReader


class TestCSVReader:
    """Тесты для класса CSVReader."""

    def test_read_file_success(self, sample_csv_file):
        """Тест успешного чтения CSV файла."""
        data = CSVReader.read_file(sample_csv_file)

        assert len(data) == 5
        assert isinstance(data, list)
        assert isinstance(data[0], dict)
        assert data[0]['name'] == 'Alex Ivanov'
        assert data[0]['position'] == 'Backend Developer'

    def test_read_file_not_found(self):
        """Тест чтения несуществующего файла."""
        with pytest.raises(FileNotFoundError):
            CSVReader.read_file('non_existent_file.csv')

    def test_read_multiple_files_success(self, multiple_csv_files):
        """Тест чтения нескольких CSV файлов."""
        data = CSVReader.read_multiple_files(multiple_csv_files)

        assert len(data) == 5
        assert data[0]['name'] == 'Alex Ivanov'
        assert data[2]['name'] == 'John Smith'

    def test_read_multiple_files_with_invalid(self, sample_csv_file):
        """Тест чтения нескольких файлов, когда один не существует."""
        files = [sample_csv_file, 'non_existent_file.csv']

        with pytest.raises(FileNotFoundError):
            CSVReader.read_multiple_files(files)

    def test_read_empty_file(self, empty_csv_file):
        """Тест чтения пустого CSV файла (только заголовки)."""
        data = CSVReader.read_file(empty_csv_file)

        assert len(data) == 0
        assert isinstance(data, list)

    def test_read_file_with_invalid_data(self, csv_with_invalid_data):
        """Тест чтения файла с некорректными данными."""
        data = CSVReader.read_file(csv_with_invalid_data)

        assert len(data) == 1
        assert data[0]['name'] == 'Test User'
        assert data[0]['performance'] == 'not_a_number'

    def test_data_types(self, sample_csv_file):
        """Тест проверки типов данных в результатах."""
        data = CSVReader.read_file(sample_csv_file)

        for record in data:
            assert isinstance(record['name'], str)
            assert isinstance(record['position'], str)
            assert isinstance(record['performance'], str)
            assert isinstance(record['skills'], str)

    def test_unicode_support(self):
        """Тест поддержки Unicode в CSV файлах."""
        import tempfile
        import csv
        import os

        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', encoding='utf-8', delete=False) as f:
            writer = csv.writer(f)
            writer.writerow(['name', 'position', 'performance'])
            writer.writerow(['Иван Петров', 'Разработчик', '4.5'])
            file_path = f.name

        try:
            data = CSVReader.read_file(file_path)
            assert len(data) == 1
            assert data[0]['name'] == 'Иван Петров'
        finally:
            os.unlink(file_path)