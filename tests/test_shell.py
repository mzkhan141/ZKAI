"""Tests for ZKShell and ZKAICLI engines."""

import pytest
from zkai.shell.shell import ZKShell
from zkai.shell.cli import ZKAICLI, ArgparseCLIEngine, ClickCLIEngine


def test_zk_shell_commands():
    shell = ZKShell()
    res_chat = shell.execute_line("chat hello world")
    assert "[ZKAI Chat Response]" in res_chat

    res_search = shell.execute_line("search quantum physics")
    assert "[ZKAI Search Results]" in res_search

    res_unknown = shell.execute_line("invalid_cmd_123")
    assert "Command not found" in res_unknown


def test_shell_alias_and_pipeline():
    shell = ZKShell()
    shell.set_alias("c", "chat")
    res_alias = shell.execute_line("c alias prompt")
    assert "[ZKAI Chat Response]" in res_alias

    res_pipe = shell.execute_line("search query | chat")
    assert "[ZKAI Chat Response]" in res_pipe


def test_dual_cli_engine():
    cli_argparse = ZKAICLI(preferred_engine="argparse")
    out1 = cli_argparse.main(["chat", "hello"])
    assert "[ZKAI Chat Response]" in out1

    cli_click = ZKAICLI(preferred_engine="click")
    out2 = cli_click.main(["chat", "hello"])
    assert "[ZKAI Chat Response]" in out2
