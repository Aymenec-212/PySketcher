import ast
from typing import List, Set

# Reverse mapping for Types
TYPE_MAP = {
    "String": "str", "Integer": "int", "Boolean": "bool", "Float": "float",
    "Linear": "linear", "Conv2d": "conv2d", "Dropout": "dropout", "Flatten": "flatten"
}


class FileInspector(ast.NodeVisitor):
    def __init__(self):
        self.decorators: Set[str] = set()
        self.imports: Set[str] = set()

    def visit_Import(self, node):
        for alias in node.names:
            self.imports.add(alias.name)
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        if node.module:
            self.imports.add(node.module)
        self.generic_visit(node)

    def visit_ClassDef(self, node):
        base_ids = []
        for base in node.bases:
            if isinstance(base, ast.Name):
                base_ids.append(base.id)
            elif isinstance(base, ast.Attribute):  # handle nn.Module
                base_ids.append(base.attr)

        # 1. SQL Alchemy Detection
        if "Base" in base_ids:
            self._handle_sqlalchemy(node)

        # 2. PyTorch Detection (nn.Module)
        elif "Module" in base_ids:
            self._handle_pytorch(node)

        # 3. Pydantic Detection (BaseModel)
        elif "BaseModel" in base_ids:
            self._handle_pydantic(node)

        self.generic_visit(node)

    def _handle_sqlalchemy(self, node):
        fields = []
        for item in node.body:
            if isinstance(item, ast.Assign) and self._is_column(item):
                f_name = item.targets[0].id
                # Heuristic to get type... simplified for brevity
                fields.append(f"{f_name}:str")
        self._add_tag("sqlalchemy", node.name, fields)

    def _handle_pydantic(self, node):
        """Captures Pydantic fields (Annotated assignments)."""
        fields = []
        for item in node.body:
            # Pydantic uses AnnAssign: name: type
            if isinstance(item, ast.AnnAssign) and isinstance(item.target, ast.Name):
                var_name = item.target.id
                var_type = self._get_id(item.annotation)
                fields.append(f"{var_name}:{var_type}")

        self._add_tag("pydantic", node.name, fields)

    def _handle_pytorch(self, node):
        """Captures PyTorch layers defined in __init__."""
        layers = []

        # Find __init__ method
        init_method = next((n for n in node.body if isinstance(n, ast.FunctionDef) and n.name == "__init__"), None)

        if init_method:
            for item in init_method.body:
                # Look for self.layer = nn.Type(...)
                if isinstance(item, ast.Assign):
                    # Check targets (self.x)
                    target = item.targets[0]
                    if isinstance(target, ast.Attribute) and isinstance(target.value,
                                                                        ast.Name) and target.value.id == "self":
                        layer_name = target.attr

                        # Check value (nn.Linear)
                        if isinstance(item.value, ast.Call):
                            layer_type = self._get_id(item.value.func)
                            # Convert 'Linear' -> 'linear'
                            sketch_type = TYPE_MAP.get(layer_type, layer_type.lower())
                            layers.append(f"{layer_name}:{sketch_type}")

        self._add_tag("pytorch", node.name, layers)

    def _is_column(self, node: ast.Assign):
        # ... reusing logic from previous step ...
        if isinstance(node.value, ast.Call):
            return self._get_id(node.value.func) == "Column"
        return False

    def _get_id(self, node):
        """Helper to safely extract identifiers from Name or Attribute."""
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Attribute):
            return node.attr
        return "unknown"

    def _add_tag(self, tag_name, class_name, fields):
        if fields:
            field_str = ", ".join(fields)
            self.decorators.add(f"@{tag_name}({class_name}, {field_str})")
        else:
            self.decorators.add(f"@{tag_name}({class_name})")


def inspect_code(content: str) -> List[str]:
    try:
        tree = ast.parse(content)
        inspector = FileInspector()
        inspector.visit(tree)

        # Simple Framework detection
        if any("fastapi" in i for i in inspector.imports):
            inspector.decorators.add("@fastapi")

        return list(inspector.decorators)
    except SyntaxError:
        return []