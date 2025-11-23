import time
import sys
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from .core import parse
from .engine.generator import ProjectGenerator


class SketchHandler(FileSystemEventHandler):
    """Handles file system events."""

    def __init__(self, sketch_file: str, output_dir: str):
        self.sketch_file = str(Path(sketch_file).resolve())
        self.output_dir = output_dir
        self.generator = ProjectGenerator(output_dir)

    def on_modified(self, event):
        # Only react if the specific sketch file changed
        if str(Path(event.src_path).resolve()) == self.sketch_file:
            print(f"\n⚡ Detected change in {self.sketch_file}")
            self.rebuild_project()

    def rebuild_project(self):
        try:
            print("🔄 Rebuilding project...")

            # 1. Read File
            with open(self.sketch_file, "r", encoding="utf-8") as f:
                content = f.read()

            # 2. Parse (Rust)
            tree = parse(content)

            # 3. Generate (Python)
            self.generator.generate(tree)

            print("✅ Project synced successfully!")

        except Exception as e:
            print(f"❌ Error during rebuild: {e}")


def start_watcher(sketch_path: str, output_dir: str):
    path_obj = Path(sketch_path)
    if not path_obj.exists():
        print(f"❌ Error: Sketch file '{sketch_path}' not found.")
        return

    # Watch the directory containing the sketch file
    dir_to_watch = path_obj.parent

    event_handler = SketchHandler(sketch_path, output_dir)
    observer = Observer()
    observer.schedule(event_handler, path=str(dir_to_watch), recursive=False)

    observer.start()
    print(f"👀 Watching '{sketch_path}' for changes...")
    print(f"📂 Output target: '{output_dir}'")
    print("Use Ctrl+C to stop.")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()