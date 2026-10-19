"""Enigma plugboard (Steckerbrett) connections."""


class Plugboard:
    """An involutive letter swap table built from pairs such as ``AB CD``."""

    def __init__(self, pairs: str | list[str] | tuple[str, ...] = ()) -> None:
        if isinstance(pairs, str):
            pairs = pairs.split()
        mapping = {chr(code): chr(code) for code in range(ord("A"), ord("Z") + 1)}
        used: set[str] = set()
        for pair in pairs:
            pair = pair.upper()
            if len(pair) != 2 or not pair.isalpha() or not pair.isascii():
                raise ValueError(f"Invalid plugboard pair {pair!r}; expected two letters")
            left, right = pair
            if left == right:
                raise ValueError(f"Plugboard pair {pair!r} must use two different letters")
            if left in used or right in used:
                raise ValueError("A letter may appear in at most one plugboard pair")
            used.update((left, right))
            mapping[left], mapping[right] = right, left
        self._mapping = mapping

    def swap(self, letter: str) -> str:
        return self._mapping[letter]
