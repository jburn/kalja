import pytest

from kalja.keyboards import US_DESKTOP
from kalja.mutator import Mutator, mutate, variants


def test_mutators_with_same_seed_produce_same_sequence() -> None:
    first = Mutator(seed=42)
    second = Mutator(seed=42)

    assert first.mutate("Missä te olette?") == second.mutate("Missä te olette?")

    assert first.mutate("Olen Oulussa.") == second.mutate("Olen Oulussa.")


def test_mutator_rng_state_advances() -> None:
    mutator = Mutator(
        keyboard_error_rate=0.8,
        seed=42,
    )

    first = mutator.mutate("abcdefghijklmnop")
    second = mutator.mutate("abcdefghijklmnop")

    assert first != second


def test_all_zero_rates_return_original_text() -> None:
    mutator = Mutator(
        keyboard_error_rate=0.0,
        transposition_rate=0.0,
        omission_rate=0.0,
        repetition_rate=0.0,
        spacing_rate=0.0,
        casing_rate=0.0,
        punctuation_rate=0.0,
        seed=42,
    )

    text = "Missä te olette? 🙂"

    assert mutator.mutate(text) == text


def test_mutator_can_enable_only_repetition() -> None:
    mutator = Mutator(
        keyboard_error_rate=0.0,
        transposition_rate=0.0,
        omission_rate=0.0,
        repetition_rate=1.0,
        spacing_rate=0.0,
        casing_rate=0.0,
        punctuation_rate=0.0,
        seed=42,
    )

    assert mutator.mutate("abc") == "aabbcc"


def test_mutator_can_enable_only_omission() -> None:
    mutator = Mutator(
        keyboard_error_rate=0.0,
        transposition_rate=0.0,
        omission_rate=1.0,
        repetition_rate=0.0,
        spacing_rate=0.0,
        casing_rate=0.0,
        punctuation_rate=0.0,
        seed=42,
    )

    assert mutator.mutate("abc") == ""


@pytest.mark.parametrize(
    "argument",
    [
        "keyboard_error_rate",
        "transposition_rate",
        "omission_rate",
        "repetition_rate",
        "spacing_rate",
        "casing_rate",
        "punctuation_rate",
    ],
)
def test_mutator_rejects_rate_above_one(argument: str) -> None:
    with pytest.raises(ValueError):
        Mutator(**{argument: 1.1})


def test_mutate_intensity_zero_returns_original_text() -> None:
    text = "Missä te olette? 123 🙂"

    assert mutate(text, intensity=0.0, seed=42) == text


def test_mutate_is_deterministic_with_seed() -> None:
    text = "Missä te olette tänään?"

    first = mutate(text, intensity=0.8, seed=42)
    second = mutate(text, intensity=0.8, seed=42)

    assert first == second


def test_mutate_handles_empty_string() -> None:
    assert mutate("", intensity=1.0, seed=42) == ""


@pytest.mark.parametrize(
    "intensity",
    [-1.0, -0.01, 1.01, 2.0],
)
def test_mutate_rejects_invalid_intensity(
    intensity: float,
) -> None:
    with pytest.raises(ValueError):
        mutate("test", intensity=intensity)


def test_mutate_intensity_one_is_deterministic() -> None:
    text = "Tämä on riittävän pitkä testilause mutaatioita varten."

    first = mutate(text, intensity=1.0, seed=123)
    second = mutate(text, intensity=1.0, seed=123)

    assert first == second


def test_variants_returns_requested_count() -> None:
    result = variants(
        "Missä te olette?",
        count=5,
        intensity=0.8,
        seed=42,
    )

    assert len(result) == 5


def test_variants_is_deterministic_with_seed() -> None:
    text = "Tämä on riittävän pitkä testilause."

    first = variants(
        text,
        count=10,
        intensity=0.8,
        seed=42,
    )
    second = variants(
        text,
        count=10,
        intensity=0.8,
        seed=42,
    )

    assert first == second


def test_variants_zero_count_returns_empty_list() -> None:
    assert (
        variants(
            "test",
            count=0,
            intensity=0.5,
            seed=42,
        )
        == []
    )


def test_variants_intensity_zero_returns_original_text() -> None:
    text = "Missä te olette?"

    result = variants(
        text,
        count=5,
        intensity=0.0,
        seed=42,
    )

    assert result == [text] * 5


def test_variants_handles_empty_string() -> None:
    result = variants(
        "",
        count=3,
        intensity=1.0,
        seed=42,
    )

    assert result == ["", "", ""]


def test_variants_rejects_negative_count() -> None:
    with pytest.raises(ValueError):
        variants("test", count=-1)


@pytest.mark.parametrize(
    "intensity",
    [-1.0, -0.01, 1.01, 2.0],
)
def test_variants_rejects_invalid_intensity(
    intensity: float,
) -> None:
    with pytest.raises(ValueError):
        variants(
            "test",
            intensity=intensity,
        )


def test_mutate_accepts_us_desktop_layout() -> None:
    result = mutate(
        "hello world",
        intensity=1.0,
        layout=US_DESKTOP,
        seed=42,
    )

    assert isinstance(result, str)


def test_variants_accepts_us_desktop_layout() -> None:
    result = variants(
        "hello world",
        count=5,
        intensity=1.0,
        layout=US_DESKTOP,
        seed=42,
    )

    assert len(result) == 5
