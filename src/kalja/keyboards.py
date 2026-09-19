from collections.abc import Mapping
from dataclasses import dataclass
from types import MappingProxyType


@dataclass(frozen=True)
class Key:
    """Physical key in a keyboard"""
 
    primary: str
    shifted: str
    x: float
    y: float

class KeyboardLayout:
    """Physical keyboard layout used for neighboring-key mutations."""

    def __init__(self, name: str, keys: tuple[Key, ...]) -> None:
        if not name:
            raise ValueError("Keyboard layout name cannot be empty")

        if not keys:
            raise ValueError("Keyboard layout has to contain at least one key")

        by_character: dict[str, Key] = {}

        for key in keys:
            if len(key.primary) != 1 or len(key.shifted) != 1:
                raise ValueError("Keyboard keys need to single characters")

            for character in (key.primary, key.shifted):
                if character in by_character:
                    raise ValueError(
                        f"Duplicate keyboard character: {character!r}"
                    )

                by_character[character] = key

        self._name = name
        self._keys = keys
        self._by_character: Mapping[str, Key] = MappingProxyType(by_character)

    @property
    def name(self) -> str:
        return self._name

    def keys(self) -> tuple[Key, ...]:
        return self._keys

    def __contains__(self, character: object) -> bool:
        return character in self._by_character

    def key(self, character: str) -> Key:
        return self._by_character[character]
