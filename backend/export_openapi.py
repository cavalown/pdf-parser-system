import json
from pathlib import Path

from app.main import app

output_path = Path(__file__).parent.parent / "openspec" / "openapi.json"
output_path.write_text(json.dumps(app.openapi(), indent=2, ensure_ascii=False))
print(f"OpenAPI spec exported to {output_path}")
