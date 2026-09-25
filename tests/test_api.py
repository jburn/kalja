import random
import kalja


def test_public_api() -> None:
    assert kalja.__all__ == [
        "Mutator",
        "drop_chars",
        "keyboard_error",
        "mutate",
        "mutate_casing",
        "mutate_punctuation",
        "mutate_spacing",
        "repeat_chars",
        "transpose_chars",
        "variants",
    ]


def test_mutate_does_not_change_global_random_state() -> None:
    random.seed(12345)
    before = random.getstate()

    kalja.mutate(
        "Missä te olette?",
        intensity=1.0,
        seed=42,
    )

    after = random.getstate()

    assert after == before


def test_variants_does_not_change_global_random_state() -> None:
    random.seed(12345)
    before = random.getstate()

    kalja.variants(
        "Missä te olette?",
        count=10,
        intensity=1.0,
        seed=42,
    )

    after = random.getstate()

    assert after == before


def test_public_mutate_is_reproducible() -> None:
    text = "Tämä on suomalainen testilause."

    assert kalja.mutate(
        text,
        intensity=0.8,
        seed=42,
    ) == kalja.mutate(
        text,
        intensity=0.8,
        seed=42,
    )


def test_public_variants_is_reproducible() -> None:
    text = "Tämä on suomalainen testilause."

    assert kalja.variants(
        text,
        count=20,
        intensity=0.8,
        seed=42,
    ) == kalja.variants(
        text,
        count=20,
        intensity=0.8,
        seed=42,
    )
