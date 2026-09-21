from __future__ import annotations

import re
from pathlib import Path
from typing import NamedTuple


FILE_PATH = Path(__file__).resolve().parent / "file.txt"


class FileStatistics(NamedTuple):
    """Statistics calculated for a text file."""

    latin_letters: int
    words: int
    lines: int


def get_file_statistics(file_path: Path) -> FileStatistics:
    """Return the number of Latin letters, words, and lines in a file."""
    if not file_path.exists():
        raise FileNotFoundError(f"Файл не найден: {file_path}")

    text = file_path.read_text(encoding="utf-8")
    latin_letters = sum(
        1 for character in text if character.isascii() and character.isalpha()
    )
    words = len(re.findall(r"[^\W\d_]+", text, flags=re.UNICODE))
    lines = len(text.splitlines())

    return FileStatistics(
        latin_letters=latin_letters,
        words=words,
        lines=lines,
    )


def main() -> None:
    """Read file.txt and print its text statistics."""
    try:
        statistics = get_file_statistics(FILE_PATH)
    except (OSError, UnicodeError) as error:
        print(f"Ошибка: {error}")
        return

    print(f"Количество букв латинского алфавита: {statistics.latin_letters}")
    print(f"Число слов: {statistics.words}")
    print(f"Число строк: {statistics.lines}")


if __name__ == "__main__":
    main()
