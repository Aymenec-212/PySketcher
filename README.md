<div align="center">

# ⚡ SketchForge

[![PyPI](https://img.shields.io/pypi/v/sketchforge)](https://pypi.org/project/sketchforge/)
[![Build Status](https://github.com/Aymenec-212/PySketcher/actions/workflows/release.yml/badge.svg)](https://github.com/Aymenec-212/Pysketcher/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Infrastructure-as-Code for your Application Logic.**

<p align="center">
  SketchForge is a bidirectional scaffolding tool powered by <b>Rust</b> and <b>Python</b>.<br>
  It turns a simple indented text file into a fully functional project structure, and keeps them in sync.
</p>

> **⛔ No AI. No API Keys. Just Logic.**

</div>

---

## 🚀 Why?

Most scaffolders (like `cookiecutter`) are "Fire and Forget." Once you generate the project, the template is dead.

**SketchForge is a living daemon.** It watches your sketch file and updates your code in real-time. It can even reverse-engineer your existing code back into a sketch.

## 📦 Installation

```bash
pip install sketchforge
```

# 🎮 Features
## 1. The Sketch Format (DSL)
Write your project structure like you would draw it on a napkin.
```YAML
my_app:
    -> config.py @pydantic(Settings, db_url:str, debug:bool)
    -> main.py @fastapi
    -> neural_net.py @pytorch(Transformer, attn:linear, ff:linear)
```

## 2. Interactive Mode (TUI)
Don't like writing text files blindly? Launch the Terminal UI.

```Bash
sketchforge interactive plan.txt
```

## 3. Bidirectional Sync
Forward: Edit plan.txt → Files are created instantly.

Reverse: Run sketchforge capture . → Generates a sketch from existing code.

# 🛠️ Tech Stack
* Core: Rust (using pyo3) for blazingly fast parsing.

* Logic: Python 3.12+ for AST analysis and generation.

* Templating: Jinja2 (Sandboxed).

# 🔮 Roadmap & Contributing
This is v0.1.0. We are building the ultimate offline prototyping tool, and we need your help!

Current Goals:

* Plugin System: Allow users to define custom @templates (e.g., @django, @react).

* Deep Capture: Improve AST inspection to capture complex class logic back into the sketch.

* LSP Support: VS Code extension for syntax highlighting in .sketch files.

Want to help?
Fork the repo.

Install dev dependencies: pip install -e .

If touching Rust code, ensure you have cargo installed.

Submit a PR!







