from sketchforge.core import parse, print_tree

sketch = """
project:
    -> .env @secret
    backend:
        -> main.py @fastapi
        utils:
            -> helper.py
"""

print("--- Parsing Sketch ---")
tree = parse(sketch)
print_tree(tree)