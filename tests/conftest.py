import csv
import tempfile
from pathlib import Path

import pytest


@pytest.fixture
def sample_csv_data():
    """Тестовый набор данных разработчиков."""
    return [
        {
            "name": "Alex Ivanov",
            "position": "Backend Developer",
            "completed_tasks": "45",
            "performance": "4.8",
            "skills": "Python, Django, PostgreSQL, Docker",
            "team": "API Team",
            "experience_years": "5",
        },
        {
            "name": "Maria Petrova",
            "position": "Frontend Developer",
            "completed_tasks": "38",
            "performance": "4.7",
            "skills": "React, TypeScript, Redux, CSS",
            "team": "Web Team",
            "experience_years": "4",
        },
        {
            "name": "John Smith",
            "position": "Data Scientist",
            "completed_tasks": "29",
            "performance": "4.6",
            "skills": "Python, ML, SQL, Pandas",
            "team": "AI Team",
            "experience_years": "3",
        },
        {
            "name": "Anna Lee",
            "position": "DevOps Engineer",
            "completed_tasks": "52",
            "performance": "4.9",
            "skills": "AWS, Kubernetes, Terraform, Ansible",
            "team": "Infrastructure Team",
            "experience_years": "6",
        },
        {
            "name": "Mike Brown",
            "position": "QA Engineer",
            "completed_tasks": "41",
            "performance": "4.5",
            "skills": "Selenium, Jest, Cypress, Postman",
            "team": "Testing Team",
            "experience_years": "4",
        },
    ]


@pytest.fixture
def sample_csv_file(sample_csv_data):
    """Временный CSV файл с корректными данными."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
        writer = csv.DictWriter(f, fieldnames=sample_csv_data[0].keys())
        writer.writeheader()
        writer.writerows(sample_csv_data)
        file_path = f.name

    yield file_path
    Path(file_path).unlink(missing_ok=True)


@pytest.fixture
def multiple_csv_files(sample_csv_data):
    """Набор из нескольких временных CSV файлов."""
    files = []
    chunks = [sample_csv_data[:2], sample_csv_data[2:]]

    for i, data in enumerate(chunks):
        with tempfile.NamedTemporaryFile(mode="w", suffix=f"_{i}.csv", delete=False) as f:
            writer = csv.DictWriter(f, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)
            files.append(f.name)

    yield files
    for file_path in files:
        Path(file_path).unlink(missing_ok=True)


@pytest.fixture
def empty_csv_file():
    """Пустой CSV файл (только заголовки)."""
    headers = [
        "name",
        "position",
        "completed_tasks",
        "performance",
        "skills",
        "team",
        "experience_years",
    ]
    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        file_path = f.name

    yield file_path
    Path(file_path).unlink(missing_ok=True)


@pytest.fixture
def csv_with_invalid_data():
    """CSV файл с некорректными типами данных."""
    headers = [
        "name",
        "position",
        "completed_tasks",
        "performance",
        "skills",
        "team",
        "experience_years",
    ]
    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerow(["User", "Dev", "invalid", "not_a_number", "Python", "Team", "five"])
        file_path = f.name

    yield file_path
    Path(file_path).unlink(missing_ok=True)
