"""Finnish-focused text mutation and human-input fuzzing."""

from .keyboards import FI_DESKTOP, US_DESKTOP
from .mutations import (
    drop_chars,
    keyboard_error,
    mutate_casing,
    mutate_punctuation,
    mutate_spacing,
    repeat_chars,
    transpose_chars,
)
from .mutator import Mutator, mutate, variants

__all__ = [
    "FI_DESKTOP",
    "Mutator",
    "US_DESKTOP",
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
