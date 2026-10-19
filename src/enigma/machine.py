"""A historically wired three-rotor Enigma I machine."""

from __future__ import annotations

from .plugboard import Plugboard
from .reflector import Reflector
from .rotor import ALPHABET, Rotor


class EnigmaMachine:
    """A three-rotor Enigma I machine.

    Rotor and setting strings are ordered left to right, e.g. ``I II III`` and
    ``A A A``. Encryption and decryption are the same operation.
    """

    def __init__(
        self,
        rotors: str | tuple[str, str, str] = ("I", "II", "III"),
        positions: str = "AAA",
        ring_settings: str = "AAA",
        reflector: str = "B",
        plugboard: str | tuple[str, ...] = (),
    ) -> None:
        if isinstance(rotors, str):
            rotors = tuple(rotors.upper().replace(",", " ").split())
        if len(rotors) != 3:
            raise ValueError("Exactly three rotors must be specified from left to right")
        if len(set(rotors)) != 3:
            raise ValueError("Each rotor must be different")
        positions = positions.replace(" ", "").upper()
        ring_settings = ring_settings.replace(" ", "").upper()
        if len(positions) != 3 or len(ring_settings) != 3:
            raise ValueError("Positions and ring settings must each contain three letters")
        self.rotors = [
            Rotor(name, position, ring)
            for name, position, ring in zip(rotors, positions, ring_settings, strict=True)
        ]
        self.reflector = Reflector(reflector)
        self.plugboard = Plugboard(plugboard)

    @property
    def positions(self) -> str:
        return "".join(rotor.window for rotor in self.rotors)

    def _step_rotors(self) -> None:
        left, middle, right = self.rotors
        middle_at_notch = middle.at_notch
        right_at_notch = right.at_notch
        # The middle rotor steps both at its own notch and when the right rotor
        # reaches its notch; this is the characteristic double-step behaviour.
        if middle_at_notch:
            left.step()
        if middle_at_notch or right_at_notch:
            middle.step()
        right.step()

    def process(self, message: str) -> str:
        """Transform text, preserving punctuation and spaces without stepping on them."""
        output: list[str] = []
        for character in message:
            if character.upper() not in ALPHABET or not character.isascii():
                output.append(character)
                continue
            self._step_rotors()
            value = ord(self.plugboard.swap(character.upper())) - ord("A")
            for rotor in reversed(self.rotors):
                value = rotor.encode_forward(value)
            value = self.reflector.reflect(value)
            for rotor in self.rotors:
                value = rotor.encode_reverse(value)
            output.append(self.plugboard.swap(ALPHABET[value]))
        return "".join(output)

    encrypt = process
    decrypt = process
