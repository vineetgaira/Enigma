"""End-to-end checks for Enigma message processing."""

from enigma import EnigmaMachine


def test_default_known_vector() -> None:
    assert EnigmaMachine().process("AAAAA") == "BDZGO"


def test_decrypt_restores_plaintext_with_same_starting_key() -> None:
    settings = {
        "rotors": "IV II V",
        "positions": "QAZ",
        "ring_settings": "MCK",
        "reflector": "C",
        "plugboard": "AB CD EF GH IJ KL MN",
    }
    plaintext = "Attack at dawn! 0123"
    ciphertext = EnigmaMachine(**settings).process(plaintext)

    assert ciphertext != plaintext
    assert EnigmaMachine(**settings).process(ciphertext) == plaintext.upper()


def test_non_letters_are_preserved_without_advancing_rotors() -> None:
    machine = EnigmaMachine()
    assert machine.process(" !? 123 ") == " !? 123 "
    assert machine.positions == "AAA"
