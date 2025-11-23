# This file tells the IDE what is inside the Rust binary
from typing import List

class LineToken:
    line_num: int
    indent: int
    name: str
    is_dir: bool
    decorators: List[str]

def tokenize_sketch(content: str) -> List[LineToken]:
    """
    Fast Rust parser that converts text content into a list of tokens.
    """
    ...