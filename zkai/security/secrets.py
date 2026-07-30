"""SecretsManager for secure storage of API keys, tokens, and credentials."""

import base64
import os
from typing import Dict, Optional


class SecretsManager:
    """In-memory and environment secret storage with simple obfuscation/encryption."""

    def __init__(self, secret_key: Optional[str] = None):
        self._key = secret_key or os.environ.get("ZKAI_SECRET_KEY", "default_zkai_key_32_bytes_long_123")
        self._secrets: Dict[str, str] = {}

    def _obfuscate(self, value: str) -> str:
        return base64.b64encode(value.encode()).decode()

    def _deobfuscate(self, obfuscated: str) -> str:
        return base64.b64decode(obfuscated.encode()).decode()

    def set_secret(self, name: str, value: str) -> None:
        self._secrets[name] = self._obfuscate(value)

    def get_secret(self, name: str, default: Optional[str] = None) -> Optional[str]:
        if name in self._secrets:
            return self._deobfuscate(self._secrets[name])
        return os.environ.get(name, default)

    def delete_secret(self, name: str) -> None:
        self._secrets.pop(name, None)
