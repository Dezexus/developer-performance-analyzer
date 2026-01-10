import csv
import os
import tempfile

import pytest

from src.data.reader import CSVReader


class TestCSVReader:
    """Тесты чтения CSV данных."""

    def test_read_file_success(self, sample_csv_file):
        """Успешное чтение корректного CSV файла."""
        data = CSVReader.read_file(sample_csv_file)

        assert len(data) == 5
        assert isinstance(data[0], dict)
        assert data[0]["name"] == "Alex Ivanov"
        assert data[0]["position"] == "Backend Developer"

    def test_read_file_not_found(self):
        """Ошибка при попытке чтения отсутствующего файла."""
        with pytest.raises(FileNotFoundError):
            CSVReader.read_file("non_existent_file.csv")

    def test_read_multiple_files_success(self, multiple_csv_files):
        """Объединение данных из нескольких файлов."""
        data = CSVReader.read_multiple_files(multiple_csv_files)

        assert len(data) == 5
        assert data[0]["name"] == "Alex Ivanov"
        assert data[2]["name"] == "John Smith"

    def test_read_empty_file(self, empty_csv_file):
        """Чтение файла, содержащего только заголовки."""
        data = CSVReader.read_file(empty_csv_file)
        assert len(data) == 0

    def test_read_file_with_invalid_data(self, csv_with_invalid_data):
        """Чтение файла с некорректным содержимым строк."""
        data = CSVReader.read_file(csv_with_invalid_data)
        assert len(data) == 1
        assert data[0]["performance"] == "not_a_number"

    def test_data_types(self, sample_csv_file):
        """Проверка, что все считанные поля являются строками."""
        data = CSVReader.read_file(sample_csv_file)
        for record in data:
            assert all(isinstance(v, str) for v in record.values())

    def test_unicode_support(self):
        """Проверка корректной обработки кодировки UTF-8."""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".csv", encoding="utf-8", delete=False
        ) as f:
            writer = csv.writer(f)
            writer.writerow(["name", "position", "performance"])
            writer.writerow(["Иван Петров", "Разработчик", "4.5"])
            file_path = f.name

        try:
            data = CSVReader.read_file(file_path)
            assert data[0]["name"] == "Иван Петров"
        finally:
            os.unlink(file_path)
