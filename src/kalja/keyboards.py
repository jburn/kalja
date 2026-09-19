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

    def __init__(
        self,
        name: str,
        keys: tuple[Key, ...],
        *,
        neighbor_radius: float = 1.1,
    ) -> None:
        if not name:
            raise ValueError("Keyboard layout name cannot be empty")

        if not keys:
            raise ValueError("Keyboard layout has to contain at least one key")

        if neighbor_radius <= 0:
            raise ValueError("Neighbor radius must be greater than zero")

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
        self._neighbor_radius = neighbor_radius
        self._by_character: Mapping[str, Key] = MappingProxyType(by_character)

    @property
    def name(self) -> str:
        return self._name

    @property
    def keys(self) -> tuple[Key, ...]:
        return self._keys

    def __contains__(self, character: object) -> bool:
        return character in self._by_character

    def key(self, character: str) -> Key:
        return self._by_character[character]

    @property
    def neighbor_radius(self) -> float:
        return self._neighbor_radius

    def neighboring_keys(self, character: str) -> tuple[Key, ...]:
        """Return physical keys neighboring the key for character."""
        key = self.key(character)
        radius_squared = self._neighbor_radius**2

        neighbors: list[Key] = []

        for candidate in self._keys:
            if candidate is key:
                continue

            dx = candidate.x - key.x
            dy = candidate.y - key.y
            distance_squared = dx * dx + dy * dy

            if distance_squared <= radius_squared:
                neighbors.append(candidate)

        return tuple(neighbors)

    def neighbors(self, character: str) -> tuple[str, ...]:
        """Return neighboring characters while preserving shift state."""
        key = self.key(character)
        shifted = character == key.shifted

        return tuple(
            neighbor.shifted if shifted else neighbor.primary
            for neighbor in self.neighboring_keys(character)
        )
