import argparse


class CLIParser:
    """Класс для парсинга аргументов командной строки."""

    @staticmethod
    def parse_args(args=None):
        """
        Парсит аргументы командной строки.

        Args:
            args: Список аргументов (по умолчанию берется из sys.argv)

        Returns:
            Namespace с распарсенными аргументами
        """
        parser = argparse.ArgumentParser(
            description='Анализ эффективности работы разработчиков'
        )

        parser.add_argument(
            '--files',
            nargs='+',
            required=True,
            help='Пути к CSV-файлам с данными разработчиков'
        )

        parser.add_argument(
            '--report',
            required=True,
            help='Название отчёта для генерации (performance)'
        )

        return parser.parse_args(args)
