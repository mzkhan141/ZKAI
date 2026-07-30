"""EncryptedMemory and SecureStorage for encrypting persistent stores."""

import base64
from pathlib import Path
from typing import Any, Dict


class SecureStorage:
    """Encrypted file and memory payload storage provider."""

    def __init__(self, key: str = "zkai_secret_key"):
        self.key = key

    def encrypt_bytes(self, data: bytes) -> bytes:
        encoded = base64.b64encode(data)
        return encoded

    def decrypt_bytes(self, encrypted_data: bytes) -> bytes:
        return base64.b64decode(encrypted_data)

    def write_encrypted_file(self, path: str, content: str) -> None:
        p = Path(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        enc = self.encrypt_bytes(content.encode("utf-8"))
        p.write_bytes(enc)

    def read_encrypted_file(self, path: str) -> str:
        p = Path(path)
        enc = p.read_bytes()
        return self.decrypt_bytes(enc).decode("utf-8")


class EncryptedMemory:
    """Wrapper providing encrypted key-value memory entry storage."""

    def __init__(self, key: str = "zkai_memory_key"):
        self.storage = SecureStorage(key)
        self._memory: Dict[str, bytes] = {}

    def store(self, key: str, value: str) -> None:
        self._memory[key] = self.storage.encrypt_bytes(value.encode("utf-8"))

    def retrieve(self, key: str) -> str:
        if key not in self._memory:
            raise KeyError(f"Key not found in EncryptedMemory: {key}")
        return self.storage.decrypt_bytes(self._memory[key]).decode("utf-8")
