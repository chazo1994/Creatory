from creatory_core.core.utils import slugify


def test_slugify_basic() -> None:
    assert slugify("Hello Creatory World") == "hello-creatory-world"


def test_slugify_strips_symbols() -> None:
    assert slugify("  ***Creator@@@###  ") == "creator"
