"""A single Enigma rotor.

A rotor does two unrelated jobs, kept as separate methods on purpose:

1. Letter mapping — forward() and backward() turn one letter into
   another, depending on the rotor's wiring, its ring setting, and
   its current rotated position. The signal passes through every
   rotor twice per keypress: once forward (toward the reflector) and
   once backward (on the way out).
2. Stepping — step() rotates the rotor one position, and at_notch()
   reports whether this rotor is currently positioned to carry the
   rotor to its left along with it on the next keypress. The machine
   (not the rotor) decides *when* to call step() — see machine.py.
"""

from __future__ import annotations

from . import wiring

_A = ord("A")


def _letter_to_index(letter: str) -> int:
    return ord(letter.upper()) - _A


def _index_to_letter(index: int) -> str:
    return chr((index % 26) + _A)


class Rotor:
    def __init__(
        self,
        wiring_str: str,
        notch: str,
        position: str | int = "A",
        ring: str | int = "A",
    ) -> None:
        if len(wiring_str) != 26 or sorted(wiring_str) != sorted(
            "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        ):
            raise ValueError("wiring must be a permutation of A-Z")

        self.wiring = wiring_str
        self.notch = notch.upper()
        self.position = (
            _letter_to_index(position) if isinstance(position, str) else position
        )
        self.ring = _letter_to_index(ring) if isinstance(ring, str) else ring

    @classmethod
    def from_name(cls, name: str, position: str | int = "A", ring: str | int = "A") -> Rotor:
        """Build a historical rotor by name, e.g. Rotor.from_name("III")."""
        wiring_str, notch = wiring.ROTORS[name]
        return cls(wiring_str, notch, position=position, ring=ring)

    # --- letter mapping -----------------------------------------------

    def forward(self, index: int) -> int:
        """Signal entering from the right (keyboard/plugboard side)."""
        shift = self.position - self.ring
        return (ord(self.wiring[(index + shift) % 26]) - _A - shift) % 26

    def backward(self, index: int) -> int:
        """Signal entering from the left (reflector side)."""
        shift = self.position - self.ring
        shifted_letter = _index_to_letter(index + shift)
        return (self.wiring.index(shifted_letter) - shift) % 26

    # --- stepping -------------------------------------------------------

    def at_notch(self) -> bool:
        return _index_to_letter(self.position) == self.notch

    def step(self) -> None:
        self.position = (self.position + 1) % 26

    # --- convenience ------------------------------------------------

    @property
    def position_letter(self) -> str:
        return _index_to_letter(self.position)

    def __repr__(self) -> str:
        return f"Rotor(position={self.position_letter!r}, ring={self.ring + 1})"