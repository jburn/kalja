import random

import pytest

from kalja.keyboards import FI_DESKTOP
from kalja.mutations import drop_chars, keyboard_error, repeat_chars, transpose_chars


def test_keyboard_error_rate_zero_returns_original_text() -> None:
    text = "Missä te olette? 123"

    assert keyboard_error(text, rate=0.0, seed=42) == text


def test_keyboard_error_is_deterministic_with_seed() -> None:
    first = keyboard_error(
        "Missä te olette?",
        rate=0.5,
        seed=42,
    )
    second = keyboard_error(
        "Missä te olette?",
        rate=0.5,
        seed=42,
    )

    assert first == second


def test_keyboard_error_rate_one_mutates_eligible_characters() -> None:
    result = keyboard_error("test", rate=1.0, seed=42)

    assert result != "test"
    assert len(result) == len("test")


def test_keyboard_error_uses_actual_neighbors() -> None:
    result = keyboard_error("f", rate=1.0, seed=42)

    assert result in FI_DESKTOP.neighbors("f")


def test_keyboard_error_preserves_unknown_characters() -> None:
    text = "🙂漢"

    assert keyboard_error(text, rate=1.0, seed=42) == text


def test_keyboard_error_preserves_spaces() -> None:
    text = "a b"

    result = keyboard_error(text, rate=1.0, seed=42)

    assert result[1] == " "


def test_keyboard_error_handles_finnish_characters() -> None:
    for character in "äöåÄÖÅ":
        result = keyboard_error(character, rate=1.0, seed=42)

        assert result in FI_DESKTOP.neighbors(character)


def test_keyboard_error_handles_digits() -> None:
    for character in "0123456789":
        result = keyboard_error(character, rate=1.0, seed=42)

        assert result in FI_DESKTOP.neighbors(character)


def test_keyboard_error_handles_empty_string() -> None:
    assert keyboard_error("", rate=1.0, seed=42) == ""


@pytest.mark.parametrize("rate", [-1.0, -0.01, 1.01, 2.0])
def test_keyboard_error_rejects_invalid_rate(rate: float) -> None:
    with pytest.raises(ValueError):
        keyboard_error("test", rate=rate)


def test_keyboard_error_does_not_change_global_random_state() -> None:
    random.seed(12345)
    state_before = random.getstate()

    keyboard_error("Missä te olette?", rate=0.5, seed=42)

    state_after = random.getstate()

    assert state_after == state_before

def test_keyboard_error_only_uses_neighboring_keys() -> None:
    text = "suomi123"

    result = keyboard_error(text, rate=1.0, seed=42)

    assert len(result) == len(text)

    for original, mutated in zip(text, result, strict=True):
        assert mutated in FI_DESKTOP.neighbors(original)



def test_transpose_chars_rate_zero_returns_original_text() -> None:
    text = "Missä te olette?"

    assert transpose_chars(text, rate=0.0, seed=42) == text


def test_transpose_chars_is_deterministic_with_seed() -> None:
    first = transpose_chars(
        "abcdefghijklmnop",
        rate=0.5,
        seed=42,
    )
    second = transpose_chars(
        "abcdefghijklmnop",
        rate=0.5,
        seed=42,
    )

    assert first == second


def test_transpose_chars_rate_one_swaps_adjacent_pairs() -> None:
    assert transpose_chars("abcdef", rate=1.0) == "badcfe"


def test_transpose_chars_rate_one_preserves_final_odd_character() -> None:
    assert transpose_chars("abcde", rate=1.0) == "badce"


def test_transpose_chars_handles_single_character() -> None:
    assert transpose_chars("a", rate=1.0) == "a"


def test_transpose_chars_handles_empty_string() -> None:
    assert transpose_chars("", rate=1.0) == ""


@pytest.mark.parametrize("rate", [-1.0, -0.01, 1.01, 2.0])
def test_transpose_chars_rejects_invalid_rate(rate: float) -> None:
    with pytest.raises(ValueError):
        transpose_chars("test", rate=rate)


def test_drop_chars_rate_zero_returns_original_text() -> None:
    text = "Missä te olette?"

    assert drop_chars(text, rate=0.0, seed=42) == text


def test_drop_chars_rate_one_returns_empty_string() -> None:
    assert drop_chars("Missä te olette?", rate=1.0) == ""


def test_drop_chars_is_deterministic_with_seed() -> None:
    text = "abcdefghijklmnop"

    first = drop_chars(text, rate=0.5, seed=42)
    second = drop_chars(text, rate=0.5, seed=42)

    assert first == second


def test_drop_chars_handles_empty_string() -> None:
    assert drop_chars("", rate=0.5, seed=42) == ""


def test_drop_chars_handles_unicode() -> None:
    result = drop_chars("ääö🙂漢", rate=0.5, seed=42)

    assert isinstance(result, str)


@pytest.mark.parametrize("rate", [-1.0, -0.01, 1.01, 2.0])
def test_drop_chars_rejects_invalid_rate(rate: float) -> None:
    with pytest.raises(ValueError):
        drop_chars("test", rate=rate)

def test_drop_chars_only_removes_characters() -> None:
    text = "abcdef"

    result = drop_chars(text, rate=0.5, seed=42)

    iterator = iter(text)

    assert all(char in iterator for char in result)

def test_repeat_chars_rate_zero_returns_original_text() -> None:
    text = "Missä te olette?"

    assert repeat_chars(text, rate=0.0, seed=42) == text


def test_repeat_chars_rate_one_duplicates_every_character() -> None:
    assert repeat_chars("kalja", rate=1.0) == "kkaalljjaa"


def test_repeat_chars_is_deterministic_with_seed() -> None:
    text = "abcdefghijklmnop"

    first = repeat_chars(text, rate=0.5, seed=42)
    second = repeat_chars(text, rate=0.5, seed=42)

    assert first == second


def test_repeat_chars_handles_empty_string() -> None:
    assert repeat_chars("", rate=0.5, seed=42) == ""


def test_repeat_chars_handles_single_character() -> None:
    assert repeat_chars("a", rate=1.0) == "aa"


def test_repeat_chars_handles_finnish_characters() -> None:
    assert repeat_chars("äöå", rate=1.0) == "ääööåå"


def test_repeat_chars_handles_unicode() -> None:
    assert repeat_chars("🙂漢", rate=1.0) == "🙂🙂漢漢"


def test_repeat_chars_can_duplicate_whitespace() -> None:
    assert repeat_chars("a b", rate=1.0) == "aa  bb"


def test_repeat_chars_can_duplicate_punctuation() -> None:
    assert repeat_chars("a!", rate=1.0) == "aa!!"


@pytest.mark.parametrize("rate", [-1.0, -0.01, 1.01, 2.0])
def test_repeat_chars_rejects_invalid_rate(rate: float) -> None:
    with pytest.raises(ValueError):
        repeat_chars("test", rate=rate)

def test_repeat_chars_only_duplicates_original_characters() -> None:
    text = "abcdef"

    result = repeat_chars(text, rate=0.5, seed=42)

    index = 0

    for char in text:
        assert result[index] == char
        index += 1

        if index < len(result) and result[index] == char:
            index += 1

    assert index == len(result)