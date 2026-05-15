"""Lesson 13: repo scanner for coding agents.

Before a coding agent can answer questions about a project, it needs boring
but reliable inspection tools:

1. List project files.
2. Search for text inside those files.
3. Return small, useful observations instead of dumping the whole repo.

This lesson has no fake model. It builds the local repo-inspection layer that a
future real-model coding agent will call.
"""

from dataclasses import dataclass
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
IGNORED_DIR_NAMES = {
    ".git",
    ".mypy_cache",
    ".pytest_cache",
    "__pycache__",
    "node_modules",
    "venv",
    ".venv",
}
TEXT_FILE_SUFFIXES = {".md", ".py", ".txt", ".json", ".toml", ".yaml", ".yml"}
MAX_LISTED_FILES = 40
MAX_SEARCH_MATCHES = 12


@dataclass(frozen=True)
class SearchMatch:
    path: str
    line_number: int
    line_text: str


def project_relative_path(path: Path) -> str:
    return path.relative_to(PROJECT_ROOT).as_posix()


def should_skip_path(path: Path) -> bool:
    return any(part in IGNORED_DIR_NAMES for part in path.parts)


def is_text_file(path: Path) -> bool:
    return path.suffix in TEXT_FILE_SUFFIXES


def iter_project_files() -> list[Path]:
    files: list[Path] = []

    for path in PROJECT_ROOT.rglob("*"):
        if should_skip_path(path):
            continue

        if path.is_file():
            files.append(path)

    return sorted(files, key=project_relative_path)


def list_project_files() -> str:
    files = iter_project_files()
    visible_files = files[:MAX_LISTED_FILES]

    lines = [project_relative_path(path) for path in visible_files]

    if len(files) > MAX_LISTED_FILES:
        lines.append(f"... {len(files) - MAX_LISTED_FILES} more files")

    return "\n".join(lines)


def search_file(path: Path, query: str) -> list[SearchMatch]:
    matches: list[SearchMatch] = []

    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except UnicodeDecodeError:
        return matches

    for line_number, line_text in enumerate(lines, start=1):
        if query.lower() in line_text.lower():
            matches.append(
                SearchMatch(
                    path=project_relative_path(path),
                    line_number=line_number,
                    line_text=line_text.strip(),
                )
            )

    return matches


def search_project(query: str) -> str:
    if not query.strip():
        return "Search query cannot be empty."

    matches: list[SearchMatch] = []

    for path in iter_project_files():
        if not is_text_file(path):
            continue

        matches.extend(search_file(path, query))

        if len(matches) >= MAX_SEARCH_MATCHES:
            break

    if not matches:
        return f"No matches for {query!r}."

    return "\n".join(
        f"{match.path}:{match.line_number}: {match.line_text}"
        for match in matches[:MAX_SEARCH_MATCHES]
    )


def print_section(title: str, content: str) -> None:
    print("=" * 60)
    print(title)
    print("-" * 60)
    print(content)


def main() -> None:
    print_section("PROJECT FILES", list_project_files())
    print_section("SEARCH: ToolCall", search_project("ToolCall"))
    print_section("SEARCH: real model", search_project("real model"))

    # TODO: Add ".csv" to TEXT_FILE_SUFFIXES and search for text in a CSV file.
    # TODO: Add one more ignored directory name and explain why agents should skip it.
    # TODO: Change MAX_SEARCH_MATCHES to 3 and observe how the output changes.
    # TODO: Add a function named summarize_file_types that counts files by suffix.


if __name__ == "__main__":
    main()
