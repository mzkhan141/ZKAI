"""Cookie and Session Management."""

from typing import Dict, Any


class CookieManager:
    """Manages browser cookies across HTTP sessions."""

    def __init__(self):
        self.cookies: Dict[str, str] = {}

    def set_cookie(self, name: str, value: str) -> None:
        self.cookies[name] = value

    def get_cookies(self) -> Dict[str, str]:
        return self.cookies


class SessionManager:
    """Manages authenticated browser sessions."""

    def __init__(self):
        self.cookie_manager = CookieManager()
