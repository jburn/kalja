import random

from .keyboards import FI_DESKTOP, KeyboardLayout
from .mutations import (
    _drop_chars,
    _keyboard_error,
    _mutate_casing,
    _mutate_punctuation,
    _mutate_spacing,
    _repeat_chars,
    _transpose_chars,
    _validate_rate,
)


class Mutator:
    """Configurable stateful text mutator."""

    def __init__(
        self,
        *,
        keyboard_error_rate: float = 0.05,
        transposition_rate: float = 0.02,
        omission_rate: float = 0.01,
        repetition_rate: float = 0.01,
        spacing_rate: float = 0.01,
        casing_rate: float = 0.01,
        punctuation_rate: float = 0.01,
        layout: KeyboardLayout = FI_DESKTOP,
        seed: int | None = None,
    ) -> None:
        _validate_rate(keyboard_error_rate)
        _validate_rate(transposition_rate)
        _validate_rate(omission_rate)
        _validate_rate(repetition_rate)
        _validate_rate(spacing_rate)
        _validate_rate(casing_rate)
        _validate_rate(punctuation_rate)

        self.keyboard_error_rate = keyboard_error_rate
        self.transposition_rate = transposition_rate
        self.omission_rate = omission_rate
        self.repetition_rate = repetition_rate
        self.spacing_rate = spacing_rate
        self.casing_rate = casing_rate
        self.punctuation_rate = punctuation_rate

        self.layout = layout
        self._rng = random.Random(seed)

    def mutate(self, text: str) -> str:
        """Apply configured mutations to text."""
        result = _keyboard_error(
            text,
            rate=self.keyboard_error_rate,
            layout=self.layout,
            rng=self._rng,
        )

        result = _transpose_chars(
            result,
            rate=self.transposition_rate,
            rng=self._rng,
        )

        result = _drop_chars(
            result,
            rate=self.omission_rate,
            rng=self._rng,
        )

        result = _repeat_chars(
            result,
            rate=self.repetition_rate,
            rng=self._rng,
        )

        result = _mutate_spacing(
            result,
            rate=self.spacing_rate,
            rng=self._rng,
        )

        result = _mutate_casing(
            result,
            rate=self.casing_rate,
            rng=self._rng,
        )

        result = _mutate_punctuation(
            result,
            rate=self.punctuation_rate,
            rng=self._rng,
        )

        return result
