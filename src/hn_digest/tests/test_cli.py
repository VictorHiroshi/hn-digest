import pytest

from hn_digest import cli


def test_cli_module_imports():
    assert cli.__name__ == "hn_digest.cli"


@pytest.mark.skip(reason="Add CLI behavior tests when the module is implemented.")
def test_cli_behavior():
    pass
