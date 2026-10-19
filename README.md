# Enigma

A Python simulation of the three-rotor German Enigma I cipher. It includes
historical wiring for rotors I–V, reflectors B and C, configurable ring and
window settings, the plugboard, and the Enigma double-step turnover behavior.

## Install

Requires Python 3.14 or newer. From a checkout, install with:

```sh
uv sync
```

## Desktop GUI

Launch the graphical field console with:

```sh
enigma-gui
```

Or run it from the project checkout with `uv run enigma gui`. The interface
provides rotor selection and window/ring settings, reflector and plugboard
configuration, message processing, live final rotor windows, a lampboard, and
a compact guide to the signal path and stepping mechanism. It uses Python's
Tkinter toolkit and adds no runtime dependencies. On Linux, install your
distribution's Tk package if Tkinter is not available in your Python build.

## Command line

Encrypt and decrypt are the same transformation: use the same machine settings
and starting window positions to reverse a message.

```sh
enigma encrypt "HELLO WORLD" --rotors I,II,III --positions AAA --rings AAA --reflector B --plugboard "AB CD"
enigma decrypt "ILBDA AMTAZ" --positions AAA
```

Available rotors are I, II, III, IV, and V. Choose three distinct rotors in
left-to-right order. Positions and ring settings each take three letters in
that same order. Plugboard pairs must use distinct letters, with no letter
appearing in more than one pair. Non-letter characters are preserved and do
not advance the rotors; letters are processed as uppercase.

## Python API

```python
from enigma import EnigmaMachine

machine = EnigmaMachine(
    rotors="I II III",
    positions="AAA",
    ring_settings="AAA",
    reflector="B",
    plugboard="AB CD",
)
ciphertext = machine.encrypt("HELLO WORLD")
```
