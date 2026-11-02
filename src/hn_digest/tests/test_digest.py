import pytest

from hn_digest import digest


def test_digest_module_imports():
    assert digest.__name__ == "hn_digest.digest"


@pytest.mark.skip(reason="Add digest behavior tests when the module is implemented.")
def test_digest_behavior():
    pass
