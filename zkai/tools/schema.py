"""SchemaGenerator for producing JSON schema tool definitions."""

import inspect
from typing import Any, Dict
from zkai.tools.base import Tool


class SchemaGenerator:
    """Generates JSON schema tool calling function specifications."""

    @staticmethod
    def generate_schema(tool: Tool) -> Dict[str, Any]:
        sig = inspect.signature(tool.execute)
        properties = {}
        for param in sig.parameters.values():
            if param.name not in ("self", "args", "kwargs"):
                properties[param.name] = {"type": "string", "description": f"Parameter {param.name}"}
        return {
            "name": tool.metadata.name,
            "description": tool.metadata.description,
            "parameters": {
                "type": "object",
                "properties": properties,
            },
        }
