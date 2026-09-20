import random

from .keyboards import FI_DESKTOP, KeyboardLayout

def _validate_rate(rate: float) -> None:
    if not 0.0 <= rate <= 1.0:
        raise ValueError("Rate must be between 0.0 and 1.0")

def _keyboard_error(
        text: str,
        *,
        rate: float,
        layout: KeyboardLayout,
        rng: random.Random,
) -> str:
    result: list[str] = []

    for char in text:
        if char not in layout:
            result.append(char)
            continue

        neighbors = layout.neighbors(char)

        if not neighbors:
            result.append(char)
            continue

        if rng.random() >= rate:
            result.append(char)
            continue

        result.append(rng.choice(neighbors))

    return "".join(result)

def keyboard_error(
        text: str,
        *,
        rate: float = 0.05,
        seed: int | None = None,
        layout: KeyboardLayout = FI_DESKTOP,
) -> str:
    """Introduce neighbouring-key substitutions into text."""
    _validate_rate(rate)

    rng = random.Random(seed)

    return _keyboard_error(
        text,
        rate=rate,
        layout=layout,
        rng=rng,
    )

def _transpose_chars(
    text: str,
    *,
    rate: float,
    rng: random.Random,
) -> str:
    chars = list(text)
    index = 0

    while index < len(chars) - 1:
        if rng.random() < rate:
            chars[index], chars[index + 1] = (
                chars[index + 1],
                chars[index],
            )
            index += 2
        else:
            index += 1

    return "".join(chars)

def transpose_chars(
    text: str,
    *,
    rate: float = 0.05,
    seed: int | None = None,
) -> str:
    """Randomly transpose adjacent characters."""
    _validate_rate(rate)

    rng = random.Random(seed)

    return _transpose_chars(
        text,
        rate=rate,
        rng=rng,
    )

def _drop_chars(
    text: str,
    *,
    rate: float,
    rng: random.Random,
) -> str:
    result: list[str] = []

    for char in text:
        if rng.random() < rate:
            continue

        result.append(char)

    return "".join(result)

def drop_chars(
    text: str,
    *,
    rate: float = 0.02,
    seed: int | None = None,
) -> str:
    """Randomly remove characters from text."""
    _validate_rate(rate)

    rng = random.Random(seed)

    return _drop_chars(
        text=text,
        rate=rate,
        rng=rng,
    )
