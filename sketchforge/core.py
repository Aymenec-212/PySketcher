from . import _sketchforge_core

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Node:
    name: str
    is_dir: bool
    decorators: List[str]
    children: List['Node'] = field(default_factory=list)


def parse(content: str) -> List[Node]:
    # 1. Get fast tokens from Rust
    tokens = _sketchforge_core.tokenize_sketch(content)

    if not tokens:
        return []

    # 2. Convert flat tokens to Tree (The Logic)
    # This is a standard stack-based tree builder
    root_nodes = []
    stack = []  # Tuple of (indent_level, Node)

    for token in tokens:
        new_node = Node(
            name=token.name,
            is_dir=token.is_dir,
            decorators=token.decorators
        )

        # Find parent based on indentation
        while stack and stack[-1][0] >= token.indent:
            stack.pop()

        if not stack:
            # No parent, this is a root node
            root_nodes.append(new_node)
        else:
            # Add to the last node in the stack (the parent)
            parent_node = stack[-1][1]
            parent_node.children.append(new_node)

        # Push current node to stack
        stack.append((token.indent, new_node))

    return root_nodes


def print_tree(nodes: List[Node], level=0):
    for node in nodes:
        icon = "📁" if node.is_dir else "📄"
        decs = f" {node.decorators}" if node.decorators else ""
        print(f"{'  ' * level}{icon} {node.name}{decs}")
        print_tree(node.children, level + 1)