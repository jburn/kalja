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
                    raise ValueError(f"Duplicate keyboard character: {character!r}")

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


FI_DESKTOP = KeyboardLayout(
    "fi-desktop",
    (
        # Number row
        Key("§", "½", -1.00, -1.0),
        Key("1", "!", 0.00, -1.0),
        Key("2", '"', 1.00, -1.0),
        Key("3", "#", 2.00, -1.0),
        Key("4", "¤", 3.00, -1.0),
        Key("5", "%", 4.00, -1.0),
        Key("6", "&", 5.00, -1.0),
        Key("7", "/", 6.00, -1.0),
        Key("8", "(", 7.00, -1.0),
        Key("9", ")", 8.00, -1.0),
        Key("0", "=", 9.00, -1.0),
        Key("+", "?", 10.00, -1.0),
        Key("´", "`", 11.00, -1.0),
        # QWERTY row
        Key("q", "Q", 0.25, 0.0),
        Key("w", "W", 1.25, 0.0),
        Key("e", "E", 2.25, 0.0),
        Key("r", "R", 3.25, 0.0),
        Key("t", "T", 4.25, 0.0),
        Key("y", "Y", 5.25, 0.0),
        Key("u", "U", 6.25, 0.0),
        Key("i", "I", 7.25, 0.0),
        Key("o", "O", 8.25, 0.0),
        Key("p", "P", 9.25, 0.0),
        Key("å", "Å", 10.25, 0.0),
        Key("¨", "^", 11.25, 0.0),
        # Home row
        Key("a", "A", 0.50, 1.0),
        Key("s", "S", 1.50, 1.0),
        Key("d", "D", 2.50, 1.0),
        Key("f", "F", 3.50, 1.0),
        Key("g", "G", 4.50, 1.0),
        Key("h", "H", 5.50, 1.0),
        Key("j", "J", 6.50, 1.0),
        Key("k", "K", 7.50, 1.0),
        Key("l", "L", 8.50, 1.0),
        Key("ö", "Ö", 9.50, 1.0),
        Key("ä", "Ä", 10.50, 1.0),
        Key("'", "*", 11.50, 1.0),
        # Bottom row
        Key("<", ">", 0.25, 2.0),
        Key("z", "Z", 1.25, 2.0),
        Key("x", "X", 2.25, 2.0),
        Key("c", "C", 3.25, 2.0),
        Key("v", "V", 4.25, 2.0),
        Key("b", "B", 5.25, 2.0),
        Key("n", "N", 6.25, 2.0),
        Key("m", "M", 7.25, 2.0),
        Key(",", ";", 8.25, 2.0),
        Key(".", ":", 9.25, 2.0),
        Key("-", "_", 10.25, 2.0),
    ),
    neighbor_radius=1.3,
)

US_DESKTOP = KeyboardLayout(
    "us-desktop",
    (
        # Number row
        Key("`", "~", -1.00, -1.0),
        Key("1", "!", 0.00, -1.0),
        Key("2", "@", 1.00, -1.0),
        Key("3", "#", 2.00, -1.0),
        Key("4", "$", 3.00, -1.0),
        Key("5", "%", 4.00, -1.0),
        Key("6", "^", 5.00, -1.0),
        Key("7", "&", 6.00, -1.0),
        Key("8", "*", 7.00, -1.0),
        Key("9", "(", 8.00, -1.0),
        Key("0", ")", 9.00, -1.0),
        Key("-", "_", 10.00, -1.0),
        Key("=", "+", 11.00, -1.0),
        # QWERTY row
        Key("q", "Q", 0.25, 0.0),
        Key("w", "W", 1.25, 0.0),
        Key("e", "E", 2.25, 0.0),
        Key("r", "R", 3.25, 0.0),
        Key("t", "T", 4.25, 0.0),
        Key("y", "Y", 5.25, 0.0),
        Key("u", "U", 6.25, 0.0),
        Key("i", "I", 7.25, 0.0),
        Key("o", "O", 8.25, 0.0),
        Key("p", "P", 9.25, 0.0),
        Key("[", "{", 10.25, 0.0),
        Key("]", "}", 11.25, 0.0),
        Key("\\", "|", 12.25, 0.0),
        # Home row
        Key("a", "A", 0.50, 1.0),
        Key("s", "S", 1.50, 1.0),
        Key("d", "D", 2.50, 1.0),
        Key("f", "F", 3.50, 1.0),
        Key("g", "G", 4.50, 1.0),
        Key("h", "H", 5.50, 1.0),
        Key("j", "J", 6.50, 1.0),
        Key("k", "K", 7.50, 1.0),
        Key("l", "L", 8.50, 1.0),
        Key(";", ":", 9.50, 1.0),
        Key("'", '"', 10.50, 1.0),
        # Bottom row
        Key("z", "Z", 1.25, 2.0),
        Key("x", "X", 2.25, 2.0),
        Key("c", "C", 3.25, 2.0),
        Key("v", "V", 4.25, 2.0),
        Key("b", "B", 5.25, 2.0),
        Key("n", "N", 6.25, 2.0),
        Key("m", "M", 7.25, 2.0),
        Key(",", "<", 8.25, 2.0),
        Key(".", ">", 9.25, 2.0),
        Key("/", "?", 10.25, 2.0),
    ),
    neighbor_radius=1.3,
)

_LAYOUTS: dict[str, KeyboardLayout] = {
    "fi-desktop": FI_DESKTOP,
    "us-desktop": US_DESKTOP,
}
