"""API Authentication & APIKey Verification."""

from typing import Optional


class APIAuth:
    """Authenticates API Keys for ZKAI REST endpoints."""

    def __init__(self, valid_api_keys: Optional[list[str]] = None):
        self.valid_keys = set(valid_api_keys or [])

    def verify_key(self, api_key: str) -> bool:
        if not self.valid_keys:
            return True
        return api_key in self.valid_keys
