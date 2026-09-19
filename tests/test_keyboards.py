import pytest

from kalja.keyboards import Key, KeyboardLayout


def test_layout_contains_primary_and_shifted_characters() -> None:
    layout = KeyboardLayout(
        "test",
        (
            Key("a", "A", 0.0, 0.0),
            Key("b", "B", 1.0, 0.0),
        ),
    )

    assert "a" in layout
    assert "A" in layout
    assert "b" in layout
    assert "B" in layout


def test_key_returns_physical_key() -> None:
    key = Key("ä", "Ä", 0.0, 0.0)
    layout = KeyboardLayout("test", (key,))

    assert layout.key("ä") is key
    assert layout.key("Ä") is key


def test_empty_name_is_rejected() -> None:
    with pytest.raises(ValueError):
        KeyboardLayout(
            "",
            (Key("a", "A", 0.0, 0.0),),
        )


def test_empty_layout_is_rejected() -> None:
    with pytest.raises(ValueError):
        KeyboardLayout("test", ())


def test_duplicate_character_is_rejected() -> None:
    with pytest.raises(ValueError):
        KeyboardLayout(
            "test",
            (
                Key("a", "A", 0.0, 0.0),
                Key("a", "B", 1.0, 0.0),
            ),
        )
