"""A configurable Enigma I rotor."""

from __future__ import annotations

from .wiring import ROTORS

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


class Rotor:
    """A rotor with a wiring, turnover notch, ring setting, and window position."""

    def __init__(
        self, name: str, position: str = "A", ring_setting: str = "A"
    ) -> None:
        name = name.upper()
        if name not in ROTORS:
            raise ValueError(f"Unknown rotor {name!r}; choose from {', '.join(ROTORS)}")
        self.name = name
        self.wiring, self.notch = ROTORS[name]
        self.position = self._letter_index(position, "position")
        self.ring_setting = self._letter_index(ring_setting, "ring setting")
        self._inverse_wiring = [self.wiring.index(letter) for letter in ALPHABET]

    @staticmethod
    def _letter_index(letter: str, label: str) -> int:
        if len(letter) != 1 or letter.upper() not in ALPHABET:
            raise ValueError(f"{label.capitalize()} must be one letter A-Z")
        return ALPHABET.index(letter.upper())

    @property
    def at_notch(self) -> bool:
        return self.position == ALPHABET.index(self.notch)

    def step(self) -> None:
        self.position = (self.position + 1) % 26

    def encode_forward(self, value: int) -> int:
        shifted = (value + self.position - self.ring_setting) % 26
        wired = ALPHABET.index(self.wiring[shifted])
        return (wired - self.position + self.ring_setting) % 26

    def encode_reverse(self, value: int) -> int:
        shifted = (value + self.position - self.ring_setting) % 26
        wired = self._inverse_wiring[shifted]
        return (wired - self.position + self.ring_setting) % 26

    @property
    def window(self) -> str:
        return ALPHABET[self.position]
