import json
from typing import Any, Optional, Tuple

try:
    from jsonschema import validate as _validate
    from jsonschema import ValidationError
except Exception:
    _validate = None
    ValidationError = Exception


class Validator:
    """Wrapper around jsonschema to allow optional validation.

    If no schema is provided, `validate` returns (True, None) and acts as a no-op.
    """

    def __init__(self, schema: Optional[dict] = None) -> None:
        self.schema = schema

    def load_schema_from_file(self, path: str) -> None:
        with open(path, "r", encoding="utf-8") as f:
            import json as _json

            self.schema = _json.load(f)

    def validate(self, data: Any) -> Tuple[bool, Optional[str]]:
        if not self.schema:
            return True, None
        if _validate is None:
            return False, "jsonschema not installed"
        try:
            _validate(instance=data, schema=self.schema)
            return True, None
        except ValidationError as e:
            return False, str(e)
