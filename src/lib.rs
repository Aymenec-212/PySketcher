use pyo3::prelude::*;
use serde::{Serialize, Deserialize};

// 1. Define the Node Structure
// This represents a single line in your sketch (File or Folder)
#[derive(Debug, Serialize, Deserialize, Clone)]
#[pyclass]
pub struct SketchNode {
    #[pyo3(get, set)]
    pub name: String,
    #[pyo3(get, set)]
    pub is_dir: bool,
    #[pyo3(get, set)]
    pub decorators: Vec<String>,
    #[pyo3(get, set)]
    pub children: Vec<SketchNode>,
}

// 2. The Parsing Logic
// We use a stack-based approach to handle indentation
#[pyfunction]
fn parse_sketch(content: String) -> PyResult<Vec<SketchNode>> {
    let mut roots: Vec<SketchNode> = Vec::new();
    // Stack stores: (indentation_level, node)
    // We use RefCell/Rc usually for trees, but for simplicity in data transfer
    // we will build a flat list and reconstruct, or use a recursive parser.
    // Let's use a simplified approach: Parse to a recursive structure directly.

    // For this first version, let's just return a flat list of "Raw Lines"
    // that Python can structure, or go full Rust. Let's go full Rust.

    // Actually, implementing a full tree parser in one go in Rust might be
    // complex for the first step. Let's start by parsing the lines into
    // structured data (Name, Type, Decorators, Indent) and let Python
    // build the Tree hierarchy (easier to debug).

    Ok(roots)
}

// Let's refine the approach ->
// Rust parses the string into a flat list of "LineTokens" with metadata.
// Python constructs the hierarchy. This is a safer hybrid start.

#[derive(Debug, Clone)]
#[pyclass]
pub struct LineToken {
    #[pyo3(get)]
    pub line_num: usize,
    #[pyo3(get)]
    pub indent: usize,
    #[pyo3(get)]
    pub name: String,
    #[pyo3(get)]
    pub is_dir: bool,
    #[pyo3(get)]
    pub decorators: Vec<String>,
}

#[pyfunction]
fn tokenize_sketch(content: String) -> PyResult<Vec<LineToken>> {
    let mut tokens = Vec::new();

    for (i, line) in content.lines().enumerate() {
        if line.trim().is_empty() { continue; }

        let indent = line.chars().take_while(|c| c.is_whitespace()).count();
        let trimmed = line.trim();

        // Split name and decorators (e.g., "main.py @fastapi @auth")
        let parts: Vec<&str> = trimmed.split('@').collect();
        let raw_name = parts[0].trim();

        // Extract decorators
        let decorators: Vec<String> = parts.iter()
            .skip(1) // skip the name
            .map(|s| s.trim().to_string())
            .collect();

        // Check if file or dir
        // Rule: If it has "->" it is a file, otherwise a folder
        let (final_name, is_dir) = if raw_name.starts_with("->") {
            (raw_name.replace("->", "").trim().to_string(), false)
        } else {
            (raw_name.replace(":", "").trim().to_string(), true) // remove trailing colon if exists
        };

        tokens.push(LineToken {
            line_num: i + 1,
            indent,
            name: final_name,
            is_dir,
            decorators,
        });
    }

    Ok(tokens)
}

#[pymodule]
fn _sketchforge_core(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_class::<LineToken>()?;
    m.add_function(wrap_pyfunction!(tokenize_sketch, m)?)?;
    Ok(())
}