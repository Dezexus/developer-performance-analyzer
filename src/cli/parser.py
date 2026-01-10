import argparse
from typing import List, Optional

from src.reports import ReportFactory


class CLIParser:
    """Класс для парсинга аргументов командной строки."""

    @staticmethod
    def parse_args(args: Optional[List[str]] = None) -> argparse.Namespace:
        parser = argparse.ArgumentParser(description="Анализ эффективности работы разработчиков")

        parser.add_argument(
            "--files",
            nargs="+",
            required=True,
            help="Пути к CSV-файлам с данными разработчиков",
        )

        available_reports = ReportFactory.get_available_reports()

        parser.add_argument(
            "--report",
            required=True,
            choices=available_reports,
            help=f"Название отчёта для генерации (доступно: {', '.join(available_reports)})",
        )

        return parser.parse_args(args)
