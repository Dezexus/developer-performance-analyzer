from pathlib import Path
from typing import List


class Validator:
    """Класс для валидации входных данных."""

    @staticmethod
    def validate_files(file_paths: List[str]) -> List[str]:
        """
        Проверяет существование файлов.

        Args:
            file_paths: Список путей к файлам

        Returns:
            Список существующих файлов

        Raises:
            ValueError: Если не найдено ни одного файла
        """
        existing_files = []
        for file_path in file_paths:
            if Path(file_path).exists():
                existing_files.append(file_path)
            else:
                print(f"Предупреждение: файл '{file_path}' не найден, пропускаем")

        if not existing_files:
            raise ValueError("Не найдено ни одного существующего файла")

        return existing_files

    @staticmethod
    def validate_report_name(report_name: str, available_reports: List[str]) -> str:
        """
        Проверяет корректность имени отчёта.

        Args:
            report_name: Имя отчёта для проверки
            available_reports: Список доступных отчётов

        Returns:
            Валидное имя отчёта

        Raises:
            ValueError: Если отчёт не поддерживается
        """
        if report_name.lower() not in available_reports:
            raise ValueError(
                f"Отчёт '{report_name}' не поддерживается. "
                f"Доступные отчёты: {', '.join(available_reports)}"
            )
        return report_name.lower()
