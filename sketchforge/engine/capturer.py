import os
from pathlib import Path
from sketchforge.engine.inspector import inspect_code

IGNORE_DIRS = {".git", ".venv", "__pycache__", ".idea", "sketchforge.egg-info"}


class ProjectCapturer:
    def __init__(self, root_path: str):
        self.root_path = Path(root_path).resolve()

    def capture(self) -> str:
        lines = [f"{self.root_path.name}:"]
        self._walk(self.root_path, lines, indent_level=1)
        return "\n".join(lines)

    def _walk(self, current_path: Path, lines: list, indent_level: int):
        # Sort items to keep folders first, then files
        items = sorted(os.listdir(current_path))

        # Separate directories and files for cleaner output
        dirs = []
        files = []

        for item in items:
            if item in IGNORE_DIRS:
                continue

            full_path = current_path / item
            if full_path.is_dir():
                dirs.append(item)
            else:
                files.append(item)

        # 1. Process Directories
        for d in dirs:
            indent = "    " * indent_level
            lines.append(f"{indent}{d}:")
            self._walk(current_path / d, lines, indent_level + 1)

        # 2. Process Files
        for f in files:
            indent = "    " * indent_level
            full_path = current_path / f

            # Default arrow syntax
            line = f"{indent}-> {f}"

            # Add Intelligence if it's a Python file
            if f.endswith(".py"):
                try:
                    content = full_path.read_text(encoding="utf-8")
                    tags = inspect_code(content)
                    if tags:
                        line += f" {' '.join(tags)}"
                except Exception:
                    pass  # Skip unreadable files

            lines.append(line)