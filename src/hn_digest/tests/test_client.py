import pytest

from hn_digest import client


def test_client_module_imports():
    assert client.__name__ == "hn_digest.client"


@pytest.mark.skip(reason="Add client behavior tests when the module is implemented.")
def test_client_behavior():
    pass
