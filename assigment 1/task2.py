from __future__ import annotations

import sys
from pathlib import Path


FOLDER_PATH = Path(__file__).resolve().parent / "text_files"


def create_sample_files(folder: Path) -> None:
    """Create five sample text files in the target folder."""
    folder.mkdir(parents=True, exist_ok=True)

    sample_data: dict[str, str] = {
        "name_1.txt": (
            "Математика — это язык науки. "
            "Теория вероятности помогает анализировать случайности."
        ),
        "name_2.txt": (
            "В программировании важно писать чистый и понятный код. "
            "Логика и алгоритмы лежат в основе решения задач."
        ),
        "name_3.txt": (
            "История мира наполнена великими открытиями и реформами. "
            "Литература учит нас понимать людей и культуру."
        ),
        "name_4.txt": (
            "Теория вероятности рассматривает случайные события, "
            "распределения и законы больших чисел."
        ),
        "name_5.txt": (
            "Физика объясняет движение тел и законы природы. "
            "Математика помогает строить модели явлений."
        ),
    }

    for filename, content in sample_data.items():
        (folder / filename).write_text(content, encoding="utf-8")


def find_matching_files(query: str, folder: Path) -> list[str]:
    """Return .txt filenames containing the requested substring."""
    normalized_query = query.strip().lower()
    if not normalized_query:
        raise ValueError("Поисковый запрос не может быть пустым.")

    matches: list[str] = []
    for file_path in sorted(folder.glob("*.txt")):
        text = file_path.read_text(encoding="utf-8")
        if normalized_query in text.lower():
            matches.append(file_path.name)

    return matches


def main() -> None:
    """Generate sample files and print those matching the search query."""
    create_sample_files(FOLDER_PATH)

    if len(sys.argv) > 1:
        raw_query = " ".join(sys.argv[1:])
    else:
        raw_query = input("Введите поисковый запрос: ")

    try:
        matches = find_matching_files(raw_query, FOLDER_PATH)
    except ValueError as exc:
        print(f"Ошибка: {exc}")
        return

    if not matches:
        print("В данных файлах отсутствует поисковый запрос.")
        return

    print("Файлы, содержащие запрос:")
    for filename in matches:
        print(filename)


if __name__ == "__main__":
    main()
