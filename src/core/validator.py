from pathlib import Path
from typing import List

from src.reports import ReportFactory


class Validator:
    """Валидация входных данных."""

    @staticmethod
    def validate_files(file_paths: List[str]) -> List[str]:
        """Проверяет существование файлов и возвращает список путей к ним."""
        existing_files = []
        for file_path in file_paths:
            path = Path(file_path)
            if path.exists() and path.is_file():
                existing_files.append(str(path))
            else:
                print(f"Предупреждение: файл '{file_path}' не найден, пропускаем")

        if not existing_files:
            raise ValueError("Не найдено ни одного существующего файла")

        return existing_files

    @staticmethod
    def validate_report_name(report_name: str) -> str:
        """Проверяет корректность имени отчёта."""
        available_reports = ReportFactory.get_available_reports()
        name_lower = report_name.lower()

        if name_lower not in available_reports:
            raise ValueError(
                f"Отчёт '{report_name}' не поддерживается. "
                f"Доступные отчёты: {', '.join(available_reports)}"
            )
        return name_lower
