import csv
from pathlib import Path
from typing import List, cast

from src.core.types import DeveloperRecord


class CSVReader:
    """Чтение данных из CSV файлов."""

    @staticmethod
    def read_file(file_path: str) -> List[DeveloperRecord]:
        """Считывает данные из одного CSV файла."""
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"Файл не найден: {file_path}")

        with open(path, encoding="utf-8", newline="") as file:
            reader = csv.DictReader(file)
            return [cast(DeveloperRecord, row) for row in reader]

    @staticmethod
    def read_multiple_files(file_paths: List[str]) -> List[DeveloperRecord]:
        """Считывает данные из нескольких файлов в один общий список."""
        all_data: List[DeveloperRecord] = []
        for file_path in file_paths:
            all_data.extend(CSVReader.read_file(file_path))
        return all_data
