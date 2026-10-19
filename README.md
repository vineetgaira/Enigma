# Enigma I Simulator

A Python simulation of the three-rotor German Enigma I cipher. It models the
historical wiring for rotors I–V, reflectors B and C, configurable ring and
window settings, a plugboard, and the characteristic double-step behavior.
Use it from the command line, a desktop GUI, or Python code.

> **For learning and historical exploration only.** Enigma is a broken,
> obsolete cipher and this simulator is not suitable for protecting data.

## Contents

- [Requirements and installation](#requirements-and-installation)
- [Desktop application](#desktop-application)
- [Command-line guide](#command-line-guide)
- [Python API](#python-api)
- [How the simulated machine works](#how-the-simulated-machine-works)
- [Supported model](#supported-model)
- [Further reading](#further-reading)

## Requirements and installation

- Python 3.14 or newer
- [uv](https://docs.astral.sh/uv/) for installing and running from a checkout
- Tkinter for the desktop application (often packaged separately on Linux)

From the project directory, install the project and its dependencies:

```sh
uv sync
```

The project provides two commands: `enigma` for the command-line interface and
`enigma-gui` for the desktop application. You can also invoke either through
`uv run` without installing the scripts globally.

## Desktop application

Start the graphical field console with either command:

```sh
uv run enigma gui
# or, after installation
enigma-gui
```

The GUI lets you select the rotor order, starting windows, ring settings,
reflector, and plugboard pairs. It includes message processing, a lampboard,
live rotor windows, and an in-app overview of the signal path and stepping
mechanism. It uses Python's Tkinter toolkit and adds no GUI framework
dependency. If Tkinter is missing, install your operating system's Tk package
for the Python interpreter used by the project.

## Command-line guide

Encrypt a message:

```sh
uv run enigma encrypt "HELLO WORLD" \
  --rotors I,II,III \
  --positions AAA \
  --rings AAA \
  --reflector B \
  --plugboard "AB CD"
```

With these settings the result is `ILBDA AMTAZ`. Decrypt by starting a fresh
machine at the same initial settings and processing the ciphertext. Encryption
and decryption use the same operation:

```sh
uv run enigma decrypt "ILBDA AMTAZ" \
  --rotors I,II,III \
  --positions AAA \
  --rings AAA \
  --reflector B \
  --plugboard "AB CD"
```

The options are:

| Option | Meaning | Default |
| --- | --- | --- |
| `--rotors` | Three distinct rotors, left to right | `I,II,III` |
| `--positions` | Starting window letters, left to right | `AAA` |
| `--rings` | Ring settings, left to right | `AAA` |
| `--reflector` | Reflector `B` or `C` | `B` |
| `--plugboard` | Space-separated letter pairs, such as `"AB CD"` | No pairs |

Rotor order and the three-letter settings are always written left to right:
slow (left), middle, fast (right). The `--positions` letters are the letters
visible in the rotor windows before the first character is processed. The
machine steps before enciphering each letter, so the first letter is processed
after the right rotor has advanced once.

Spaces and punctuation are preserved and do not advance the rotors. ASCII
letters are processed case-insensitively and returned in uppercase. Rotor
choices are I–V; choose each rotor only once. Plugboard pairs must be distinct,
and no letter may appear in more than one pair.

For the complete list of options and subcommands, run:

```sh
uv run enigma --help
uv run enigma encrypt --help
```

## Python API

The `EnigmaMachine` class is available from the `enigma` package. As with the
CLI, create a new machine with the same settings to reverse a message:

```python
from enigma import EnigmaMachine

settings = {
    "rotors": "I II III",
    "positions": "AAA",
    "ring_settings": "AAA",
    "reflector": "B",
    "plugboard": "AB CD",
}

ciphertext = EnigmaMachine(**settings).encrypt("HELLO WORLD")
plaintext = EnigmaMachine(**settings).decrypt(ciphertext)

print(ciphertext)  # ILBDA AMTAZ
print(plaintext)   # HELLO WORLD
```

`process()` is also available; `encrypt()` and `decrypt()` are aliases for that
same transformation. Each call advances the machine state. A machine instance
continues from its current rotor windows, so use a fresh instance when starting
a new message from the original settings.

## How the simulated machine works

For each letter, the machine steps its rotors, then sends the signal through
the plugboard, right-to-left through the three rotors, through the reflector,
back left-to-right through the rotors, and through the plugboard again. The
reflector routes the signal back through the rotors, which makes the same
operation decrypt ciphertext when the initial settings match.

The right rotor advances for each letter. The middle rotor advances when the
right rotor reaches its turnover notch, and the left rotor advances when the
middle rotor reaches its notch. The middle rotor's movement at its own notch
on successive keypresses produces Enigma's well-known double-step behavior.

The ring setting rotates the alphabet ring relative to the rotor wiring. It is
independent of the visible starting window letter; changing either affects
how the wiring maps at a given point in the stepping sequence.

## Supported model

This is a configurable three-rotor Enigma I model with:

- Rotors I, II, III, IV, and V
- Reflectors B and C
- Three-letter window and ring settings
- A plugboard supporting up to 13 non-overlapping pairs
- Historical rotor turnover and double-step behavior

It does not model every Enigma variant or historical operating procedure. For
example, it does not implement the four-rotor naval M4 machine, message key
procedures, or historical key sheets. The machine is intended as an accessible
simulation rather than a complete archival or cryptographic implementation.

## Further reading

- [Enigma machine — Wikipedia](https://en.wikipedia.org/wiki/Enigma_machine): overview of the machine, history, and cryptanalysis.
- [Enigma rotor details — Wikipedia](https://en.wikipedia.org/wiki/Enigma_rotor_details): rotor wirings, turnover notches, and reflector details.
- [The National Museum of Computing: The Bombe](https://www.tnmoc.org/bombe): background on the codebreaking machine developed to attack Enigma.
- [Bletchley Park](https://bletchleypark.org.uk/): the historic site and museum associated with Allied codebreaking.
