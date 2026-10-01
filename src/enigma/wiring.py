"""Historical wiring data for the Enigma I machine.

Each rotor wiring string is a permutation of A-Z: the letter at index i
is what the letter at keyboard position i maps to when current enters
that rotor at its home position. The notch is the letter that, when it
reaches the top window, causes the *next* rotor to the left to step.

Source: public, widely-published Enigma I specifications.
"""

ROTOR_I = "EKMFLGDQVZNTOWYHXUSPAIBRCJ"
ROTOR_II = "AJDKSIRUXBLHWTMCQGZNPYFVOE"
ROTOR_III = "BDFHJLCPRTXVZNYEIWGAKMUSQO"
ROTOR_IV = "ESOVPZJAYQUIRHXLNFTGKDCMWB"
ROTOR_V = "VZBRGITYUPSDNHLXAWMJQOFECK"

NOTCH_I = "Q"
NOTCH_II = "E"
NOTCH_III = "V"
NOTCH_IV = "J"
NOTCH_V = "Z"

REFLECTOR_B = "YRUHQSLDPXNGOKMIEBFZCWVJAT"
REFLECTOR_C = "FVPJIAOYEDRZXWGCTKUQSBNMHL"

# name -> (wiring, notch), so rotor.py can look rotors up by the names
# everyone actually uses ("I", "II", "III", ...).
ROTORS = {
    "I": (ROTOR_I, NOTCH_I),
    "II": (ROTOR_II, NOTCH_II),
    "III": (ROTOR_III, NOTCH_III),
    "IV": (ROTOR_IV, NOTCH_IV),
    "V": (ROTOR_V, NOTCH_V),
}

REFLECTORS = {
    "B": REFLECTOR_B,
    "C": REFLECTOR_C,
}# This stores historical rotor wiring and reflector wiring as constants.

ROTOR_I   = "EKMFLGDQVZNTOWYHXUSPAIBRCJ"
ROTOR_II  = "AJDKSIRUXBLHWTMCQGZNPYFVOE"
ROTOR_III = "BDFHJLCPRTXVZNYEIWGAKMUSQO"
NOTCH_I, NOTCH_II, NOTCH_III = "Q", "E", "V"
REFLECTOR_B = "YRUHQSLDPXNGOKMIEBFZCWVJAT"