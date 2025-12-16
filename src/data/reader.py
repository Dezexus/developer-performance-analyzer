import csv
from pathlib import Path
from typing import List, Dict


class CSVReader:
    """Класс для чтения CSV-файлов с данными разработчиков."""

    @staticmethod
    def read_file(file_path: str) -> List[Dict]:
        """
        Читает CSV-файл и возвращает список словарей.

        Args:
            file_path: Путь к CSV-файлу

        Returns:
            Список словарей с данными из CSV

        Raises:
            FileNotFoundError: Если файл не существует
        """
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"Файл не найден: {file_path}")

        with open(path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            return list(reader)

    @staticmethod
    def read_multiple_files(file_paths: List[str]) -> List[Dict]:
        """
        Читает несколько CSV-файлов и объединяет данные.

        Args:
            file_paths: Список путей к CSV-файлам

        Returns:
            Объединённый список всех записей из всех файлов
        """
        all_data = []
        for file_path in file_paths:
            data = CSVReader.read_file(file_path)
            all_data.extend(data)
        return all_data