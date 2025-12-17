import sys
from .cli.parser import CLIParser
from .core.validator import Validator
from .data.reader import CSVReader
from .reports import ReportFactory
from .utils.formatter import ReportFormatter


def main():
    """Основная функция приложения."""
    try:
        # Парсим аргументы командной строки
        args = CLIParser.parse_args()

        # Валидируем файлы
        valid_files = Validator.validate_files(args.files)

        # Читаем данные из файлов
        data = CSVReader.read_multiple_files(valid_files)

        if not data:
            print("Ошибка: в файлах нет данных")
            sys.exit(1)

        # Валидируем имя отчёта
        report_name = Validator.validate_report_name(args.report)

        # Создаём отчёт
        report = ReportFactory.create_report(report_name)
        report_data = report.generate(data)

        if not report_data:
            print("Отчёт не содержит данных")
            sys.exit(0)

        # Форматируем и выводим результат
        formatted_report = ReportFormatter.format_table(report_data)
        print(f"\nОтчёт: {report.get_name()}")
        print(formatted_report)

    except ValueError as e:
        print(f"Ошибка: {e}")
        sys.exit(1)
    except SystemExit as e:
        raise e
    except Exception as e:
        print(f"Непредвиденная ошибка: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()