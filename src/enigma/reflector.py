"""Enigma I reflector wiring."""

from .wiring import REFLECTORS


class Reflector:
    def __init__(self, name: str = "B") -> None:
        name = name.upper()
        if name not in REFLECTORS:
            raise ValueError(f"Unknown reflector {name!r}; choose from {', '.join(REFLECTORS)}")
        self.name = name
        self.wiring = REFLECTORS[name]

    def reflect(self, value: int) -> int:
        return ord(self.wiring[value]) - ord("A")
