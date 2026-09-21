from __future__ import annotations

import re
from pathlib import Path
from typing import Callable


BASE_DIR = Path(__file__).resolve().parent
WORDS_FILE = BASE_DIR / "words.txt"
FORBIDDEN_WORDS_FILE = BASE_DIR / "forbidden_words.txt"


def read_forbidden_words(file_path: Path) -> list[str]:
    """Read forbidden words separated by whitespace."""
    content = file_path.read_text(encoding="utf-8")
    return [word for word in content.split() if word]
 

def replace_forbidden_words(text: str, forbidden_words: list[str]) -> str:
    """Replace forbidden substrings with stars, ignoring letter case."""
    unique_words = sorted(set(forbidden_words), key=len, reverse=True)
    if not unique_words:
        return text

    pattern = re.compile(
        "|".join(re.escape(word) for word in unique_words),
        flags=re.IGNORECASE,
    )

    replacement: Callable[[re.Match[str]], str] = (
        lambda match: "*" * len(match.group(0))
    )
    return pattern.sub(replacement, text)


def main() -> None:
    """Read the input files and print the edited text."""
    try:
        text = WORDS_FILE.read_text(encoding="utf-8")
        forbidden_words = read_forbidden_words(FORBIDDEN_WORDS_FILE)
        edited_text = replace_forbidden_words(text, forbidden_words)
    except (OSError, UnicodeError) as error:
        print(f"Ошибка: {error}")
        return

    print(edited_text)


if __name__ == "__main__":
    main()
