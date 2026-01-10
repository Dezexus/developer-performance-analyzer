from typing import TypedDict


class DeveloperRecord(TypedDict):
    """Данные разработчика из CSV."""

    name: str
    position: str
    completed_tasks: str
    performance: str
    skills: str
    team: str
    experience_years: str


class ReportResult(TypedDict):
    """Строка итогового отчета."""

    position: str
    avg_performance: float
