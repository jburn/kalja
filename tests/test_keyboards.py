import pytest

from kalja.keyboards import FI_DESKTOP, US_DESKTOP, Key, KeyboardLayout


def test_fi_desktop_contains_finnish_letters() -> None:
    for character in "åäöÅÄÖ":
        assert character in FI_DESKTOP


def test_fi_desktop_contains_ascii_letters() -> None:
    for character in "abcdefghijklmnopqrstuvwxyz":
        assert character in FI_DESKTOP


def test_fi_desktop_f_neighbors() -> None:
    assert FI_DESKTOP.neighbors("f") == (
        "r",
        "t",
        "d",
        "g",
        "c",
        "v",
    )


def test_fi_desktop_preserves_shift_state() -> None:
    assert FI_DESKTOP.neighbors("F") == (
        "R",
        "T",
        "D",
        "G",
        "C",
        "V",
    )


def test_fi_desktop_finnish_letter_neighbors() -> None:
    assert "ö" in FI_DESKTOP.neighbors("ä")
    assert "å" in FI_DESKTOP.neighbors("ä")


def test_fi_desktop_distant_keys_are_not_neighbors() -> None:
    assert "q" not in FI_DESKTOP.neighbors("ä")


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
    assert "x" not in layout


def test_fi_desktop_contains_expected_characters() -> None:
    expected = (
        "abcdefghijklmnopqrstuvwxyz"
        "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        "åäöÅÄÖ"
        "0123456789"
        '§½!"#¤%&/()=+?'
        "<>,.;:-_"
    )

    for character in expected:
        assert character in FI_DESKTOP


def test_key_returns_physical_key() -> None:
    key = Key("ä", "Ä", 0.0, 0.0)
    layout = KeyboardLayout("test", (key,))

    assert layout.key("ä") is key
    assert layout.key("Ä") is key


def test_key_raises_for_unknown_character() -> None:
    layout = KeyboardLayout(
        "test",
        (Key("a", "A", 0.0, 0.0),),
    )

    with pytest.raises(KeyError):
        layout.key("x")


def test_empty_name_is_rejected() -> None:
    with pytest.raises(ValueError):
        KeyboardLayout(
            "",
            (Key("a", "A", 0.0, 0.0),),
        )


def test_empty_layout_is_rejected() -> None:
    with pytest.raises(ValueError):
        KeyboardLayout("test", ())


@pytest.mark.parametrize("radius", [0.0, -0.1, -1.0])
def test_invalid_neighbor_radius_is_rejected(radius: float) -> None:
    with pytest.raises(ValueError):
        KeyboardLayout(
            "test",
            (Key("a", "A", 0.0, 0.0),),
            neighbor_radius=radius,
        )


def test_multi_character_primary_is_rejected() -> None:
    with pytest.raises(ValueError):
        KeyboardLayout(
            "test",
            (Key("ab", "A", 0.0, 0.0),),
        )


def test_multi_character_shifted_is_rejected() -> None:
    with pytest.raises(ValueError):
        KeyboardLayout(
            "test",
            (Key("a", "AB", 0.0, 0.0),),
        )


def test_duplicate_primary_character_is_rejected() -> None:
    with pytest.raises(ValueError):
        KeyboardLayout(
            "test",
            (
                Key("a", "A", 0.0, 0.0),
                Key("a", "B", 1.0, 0.0),
            ),
        )


def test_duplicate_shifted_character_is_rejected() -> None:
    with pytest.raises(ValueError):
        KeyboardLayout(
            "test",
            (
                Key("a", "A", 0.0, 0.0),
                Key("b", "A", 1.0, 0.0),
            ),
        )


def test_duplicate_character_across_primary_and_shifted_is_rejected() -> None:
    with pytest.raises(ValueError):
        KeyboardLayout(
            "test",
            (
                Key("a", "A", 0.0, 0.0),
                Key("A", "B", 1.0, 0.0),
            ),
        )


def test_neighboring_keys_uses_physical_distance() -> None:
    a = Key("a", "A", 0.0, 0.0)
    b = Key("b", "B", 1.0, 0.0)
    c = Key("c", "C", 3.0, 0.0)

    layout = KeyboardLayout(
        "test",
        (a, b, c),
        neighbor_radius=1.1,
    )

    assert layout.neighboring_keys("a") == (b,)
    assert layout.neighboring_keys("b") == (a,)
    assert layout.neighboring_keys("c") == ()


def test_neighboring_keys_includes_diagonal_keys_within_radius() -> None:
    center = Key("a", "A", 0.0, 0.0)
    diagonal = Key("b", "B", 0.5, 1.0)

    layout = KeyboardLayout(
        "test",
        (center, diagonal),
        neighbor_radius=1.2,
    )

    assert layout.neighboring_keys("a") == (diagonal,)


def test_neighboring_keys_excludes_key_itself() -> None:
    key = Key("a", "A", 0.0, 0.0)
    layout = KeyboardLayout("test", (key,))

    assert layout.neighboring_keys("a") == ()


def test_primary_and_shifted_have_same_physical_neighbors() -> None:
    a = Key("a", "A", 0.0, 0.0)
    b = Key("b", "B", 1.0, 0.0)

    layout = KeyboardLayout("test", (a, b))

    assert layout.neighboring_keys("a") == (b,)
    assert layout.neighboring_keys("A") == (b,)


def test_neighbors_preserves_primary_state() -> None:
    layout = KeyboardLayout(
        "test",
        (
            Key("a", "A", 0.0, 0.0),
            Key("b", "B", 1.0, 0.0),
        ),
    )

    assert layout.neighbors("a") == ("b",)


def test_neighbors_preserves_shifted_state() -> None:
    layout = KeyboardLayout(
        "test",
        (
            Key("a", "A", 0.0, 0.0),
            Key("b", "B", 1.0, 0.0),
        ),
    )

    assert layout.neighbors("A") == ("B",)


def test_layout_properties() -> None:
    keys = (
        Key("a", "A", 0.0, 0.0),
        Key("b", "B", 1.0, 0.0),
    )
    layout = KeyboardLayout(
        "test",
        keys,
        neighbor_radius=1.25,
    )

    assert layout.name == "test"
    assert layout.keys == keys
    assert layout.neighbor_radius == 1.25


def test_us_desktop_contains_ascii_letters() -> None:
    for char in "abcdefghijklmnopqrstuvwxyz":
        assert char in US_DESKTOP

    for char in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        assert char in US_DESKTOP


def test_us_desktop_contains_digits() -> None:
    for char in "0123456789":
        assert char in US_DESKTOP


def test_us_desktop_contains_us_punctuation() -> None:
    for char in "`~!@#$%^&*()-_=+[]{}\\|;:'\",<.>/?":
        assert char in US_DESKTOP


def test_us_desktop_does_not_contain_finnish_letters() -> None:
    for char in "äöåÄÖÅ":
        assert char not in US_DESKTOP


def test_us_desktop_has_expected_neighbors() -> None:
    neighbors = US_DESKTOP.neighbors("f")

    assert "r" in neighbors
    assert "t" in neighbors
    assert "d" in neighbors
    assert "g" in neighbors
    assert "c" in neighbors
    assert "v" in neighbors


def test_us_desktop_preserves_shift_state() -> None:
    neighbors = US_DESKTOP.neighbors("F")

    assert "R" in neighbors
    assert "T" in neighbors
    assert "D" in neighbors
    assert "G" in neighbors
    assert "C" in neighbors
    assert "V" in neighbors


def test_us_desktop_name() -> None:
    assert US_DESKTOP.name == "us-desktop"


def test_finnish_and_us_desktop_have_different_number_row() -> None:
    assert FI_DESKTOP.key("2").shifted == '"'
    assert US_DESKTOP.key("2").shifted == "@"

    assert FI_DESKTOP.key("6").shifted == "&"
    assert US_DESKTOP.key("6").shifted == "^"

    assert FI_DESKTOP.key("7").shifted == "/"
    assert US_DESKTOP.key("7").shifted == "&"
