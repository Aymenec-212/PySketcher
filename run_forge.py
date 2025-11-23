import os
import shutil
from sketchforge.core import parse
from sketchforge.engine.generator import ProjectGenerator

# 1. The Input (Your Sketch)
sketch_content = """
analytics_app:
    -> models.py @sqlalchemy(Visitor, ip_address:str, visit_count:int, is_bot:bool)
"""

# 2. Parse (Rust + Python)
print("🔹 Parsing Sketch...")
tree = parse(sketch_content)

# 3. Generate (Python)
output_dir = "generated_output"

# Cleanup previous run for testing
if os.path.exists(output_dir):
    shutil.rmtree(output_dir)

print(f"🔹 Generating Project in ./{output_dir} ...")
generator = ProjectGenerator(output_dir)
generator.generate(tree)

print("\n✅ Done! Check the 'generated_output' folder.")