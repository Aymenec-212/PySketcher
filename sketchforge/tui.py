from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import Header, Footer, TextArea, Tree, Static
from textual.binding import Binding
from sketchforge.core import parse


class SketchForgeApp(App):
    CSS = """
    Screen {
        layout: horizontal;
    }
    #editor-container {
        width: 50%;
        border: solid green;
    }
    #preview-container {
        width: 50%;
        border: solid blue;
    }
    TextArea {
        height: 100%;
    }
    """

    BINDINGS = [
        Binding("ctrl+q", "quit", "Quit"),
        Binding("ctrl+s", "save_file", "Save Sketch"),
    ]

    def __init__(self, sketch_path="sketch.txt"):
        super().__init__()
        self.sketch_path = sketch_path

    def compose(self) -> ComposeResult:
        yield Header()

        # Left Side: The Editor
        with Container(id="editor-container"):
            yield Static("📝 Sketch Editor", classes="header")
            yield TextArea.code_editor(id="editor")

        # Right Side: The Tree Preview
        with Container(id="preview-container"):
            yield Static("🌲 Live Structure Preview", classes="header")
            yield Tree("Project Root", id="tree")

        yield Footer()

    def on_mount(self):
        """Called when app starts."""
        editor = self.query_one("#editor", TextArea)

        # Load file if exists
        try:
            with open(self.sketch_path, "r") as f:
                content = f.read()
                editor.text = content
                self.update_tree(content)
        except FileNotFoundError:
            editor.text = "project:\n    -> main.py"

    def on_text_area_changed(self, event: TextArea.Changed):
        """Called whenever the user types."""
        self.update_tree(event.text_area.text)

    def update_tree(self, content):
        """Parses the sketch and updates the visual tree."""
        tree_widget = self.query_one("#tree", Tree)
        tree_widget.clear()

        try:
            # 1. Parse using our Rust-powered parser
            nodes = parse(content)

            # 2. Populate the Textual Tree
            self._build_visual_tree(nodes, tree_widget.root)

            # Expand default
            tree_widget.root.expand()

        except Exception:
            # Ignore parsing errors while typing
            pass

    def _build_visual_tree(self, nodes, parent_node):
        for node in nodes:
            icon = "📁" if node.is_dir else "📄"
            label = f"{icon} {node.name}"

            if node.decorators:
                label += f" [dim cyan]{node.decorators}[/]"

            # Add to UI tree
            new_ui_node = parent_node.add(label, expand=True)

            # Recurse
            self._build_visual_tree(node.children, new_ui_node)

    def action_save_file(self):
        """Save the content to disk."""
        editor = self.query_one("#editor", TextArea)
        with open(self.sketch_path, "w") as f:
            f.write(editor.text)
        self.notify(f"Saved {self.sketch_path}!")