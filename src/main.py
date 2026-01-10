import sys

from .cli.parser import CLIParser
from .core.validator import Validator
from .data.reader import CSVReader
from .reports import ReportFactory
from .utils.formatter import ReportFormatter


def main() -> None:
    """Точка входа в приложение."""
    try:
        args = CLIParser.parse_args()
        valid_files = Validator.validate_files(args.files)
        data = CSVReader.read_multiple_files(valid_files)

        if not data:
            print("Ошибка: в файлах нет данных")
            sys.exit(1)

        report_name = Validator.validate_report_name(args.report)
        report = ReportFactory.create_report(report_name)
        report_data = report.generate(data)

        if not report_data:
            print("Отчёт не содержит данных")
            sys.exit(0)

        formatted_report = ReportFormatter.format_table(report_data)

        print(f"\nОтчёт: {report.get_name()}")
        print(formatted_report)

    except ValueError as e:
        print(f"Ошибка: {e}")
        sys.exit(1)
    except SystemExit:
        raise
    except Exception as e:
        print(f"Непредвиденная ошибка: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
