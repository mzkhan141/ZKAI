"""Headless Browser Automation, HTML/PDF Parsing, DOM Inspection, and JS Execution for ZKAI."""

from zkai.browser.browser import Browser, Tab, Page
from zkai.browser.search import BrowserSearch
from zkai.browser.downloader import Downloader
from zkai.browser.parsers import HTMLParser, PDFParser
from zkai.browser.dom import DOMInspector
from zkai.browser.cookies import CookieManager, SessionManager
from zkai.browser.js import JSExecutor

__all__ = [
    "Browser",
    "Tab",
    "Page",
    "BrowserSearch",
    "Downloader",
    "HTMLParser",
    "PDFParser",
    "DOMInspector",
    "CookieManager",
    "SessionManager",
    "JSExecutor",
]
