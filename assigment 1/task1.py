from __future__ import annotations

import csv
import json
import shutil
import zipfile
from datetime import datetime
from pathlib import Path
from typing import TypedDict


BASE_DIR = Path(__file__).resolve().parent
PROJECT_DIR = BASE_DIR / "project"
DATA_DIR = PROJECT_DIR / "data"
RESULTS_DIR = PROJECT_DIR / "results"
SOURCE_CSV = BASE_DIR / "students.csv"
STUDENTS_CSV = DATA_DIR / "students.csv"
REPORT_JSON = RESULTS_DIR / "report.json"
ARCHIVE_PATH = BASE_DIR / "results.zip"


class StudentRecord(TypedDict):
    """Structure of one item in the aggregated report."""

    full_name: str
    group: str
    average: float


def create_project_structure() -> None:
    """Create the project directories and copy the source CSV."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    if not SOURCE_CSV.exists():
        raise FileNotFoundError(f"Input file not found: {SOURCE_CSV}")

    shutil.copy2(SOURCE_CSV, STUDENTS_CSV)


def calculate_averages() -> list[StudentRecord]:
    """Read the student CSV and calculate each student's average grade."""
    with STUDENTS_CSV.open("r", encoding="utf-8", newline="") as csv_file:
        reader = csv.DictReader(csv_file)

        if not reader.fieldnames or "full_name" not in reader.fieldnames:
            raise ValueError("CSV must contain a 'full_name' column.")

        grade_columns = [
            column
            for column in reader.fieldnames
            if column not in {"full_name", "group"}
        ]
        if not grade_columns:
            raise ValueError("CSV must contain at least one grade column.")

        report: list[StudentRecord] = []
        for row in reader:
            grades = [float(row[column]) for column in grade_columns]
            report.append(
                {
                    "full_name": row["full_name"],
                    "group": row["group"],
                    "average": round(sum(grades) / len(grades), 2),
                }
            )

    return report


def save_report(report: list[StudentRecord]) -> bool:
    """Save report.json after confirming overwrite if needed."""
    if REPORT_JSON.exists():
        try:
            answer = (
                input(
                    f"Warning: {REPORT_JSON} already exists. "
                    "Overwrite it? [y/N]: "
                )
                .strip()
                .lower()
            )
        except EOFError:
            answer = "n"

        if answer not in {"y", "yes"}:
            print("Saving cancelled.")
            return False

    with REPORT_JSON.open("w", encoding="utf-8") as json_file:
        json.dump(report, json_file, ensure_ascii=False, indent=2)

    print(f"Report saved: {REPORT_JSON}")
    return True


def create_archive() -> None:
    """Create results.zip containing the results directory."""
    with zipfile.ZipFile(
        ARCHIVE_PATH,
        "w",
        compression=zipfile.ZIP_DEFLATED,
    ) as archive:
        for path in RESULTS_DIR.rglob("*"):
            if path.is_file():
                archive.write(
                    path,
                    Path(RESULTS_DIR.name) / path.relative_to(RESULTS_DIR),
                )

    print(f"Archive created: {ARCHIVE_PATH}")


def print_report_metadata() -> None:
    """Print report.json size and its last modification time."""
    if not REPORT_JSON.exists():
        print("report.json does not exist.")
        return

    modified_at = datetime.fromtimestamp(REPORT_JSON.stat().st_mtime)
    print(f"report.json size: {REPORT_JSON.stat().st_size} bytes")
    print(f"Last modified: {modified_at:%Y-%m-%d %H:%M:%S}")


def main() -> None:
    """Main workflow for project creation, data processing, and export."""
    create_project_structure()
    report = calculate_averages()

    if save_report(report):
        create_archive()

    print_report_metadata()


if __name__ == "__main__":
    main()
