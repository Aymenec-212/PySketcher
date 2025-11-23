import shutil
import os
from datetime import datetime
from pathlib import Path

def create_backup(target_file: str):
    """
    If target_file exists, copy it to .sketchforge/backups/ with a timestamp.
    """
    path = Path(target_file)
    if not path.exists():
        return

    # 1. Create hidden backup directory
    # We place it relative to the sketch file location
    backup_dir = path.parent / ".sketchforge" / "backups"
    backup_dir.mkdir(parents=True, exist_ok=True)

    # 2. Generate Timestamped Name
    # e.g., sketch_20231027_143055.txt.bak
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f"{path.stem}_{timestamp}{path.suffix}.bak"
    backup_path = backup_dir / backup_name

    # 3. Copy the file
    shutil.copy2(path, backup_path)
    print(f"🛡️ Backup created: {backup_path}")