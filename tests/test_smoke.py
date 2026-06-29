import worldbuild_core
import worldbuild_mcp


def test_packages_import():
    assert worldbuild_core.__doc__
    assert worldbuild_mcp.__doc__
