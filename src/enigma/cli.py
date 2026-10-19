"""Command line interface for the Enigma I simulator."""

import typer

from .machine import EnigmaMachine

app = typer.Typer(
    name="enigma",
    help="Encrypt or decrypt text with a simulated Enigma I machine.",
    no_args_is_help=True,
)


@app.command()
def gui() -> None:
    """Open the desktop Enigma console."""
    try:
        from .gui import main
    except ImportError as exc:
        raise typer.BadParameter(
            "The desktop GUI requires Tkinter. Install your Python distribution's Tk package, "
            "then run `enigma gui` again."
        ) from exc

    main()


def _run(
    message: str,
    rotors: str,
    positions: str,
    rings: str,
    reflector: str,
    plugboard: str,
) -> None:
    try:
        machine = EnigmaMachine(
            rotors=rotors,
            positions=positions,
            ring_settings=rings,
            reflector=reflector,
            plugboard=plugboard,
        )
    except ValueError as exc:
        raise typer.BadParameter(str(exc)) from exc
    typer.echo(machine.process(message))


@app.command()
def encrypt(
    message: str = typer.Argument(..., help="Text to encrypt."),
    rotors: str = typer.Option("I,II,III", "--rotors", help="Three rotors, left to right."),
    positions: str = typer.Option("AAA", "--positions", help="Starting window letters."),
    rings: str = typer.Option("AAA", "--rings", help="Ring settings, left to right."),
    reflector: str = typer.Option("B", "--reflector", help="Reflector B or C."),
    plugboard: str = typer.Option("", "--plugboard", help="Space-separated pairs, e.g. 'AB CD'."),
) -> None:
    """Encrypt a message using the selected machine settings."""
    _run(message, rotors, positions, rings, reflector, plugboard)


@app.command()
def decrypt(
    message: str = typer.Argument(..., help="Text to decrypt."),
    rotors: str = typer.Option("I,II,III", "--rotors", help="Three rotors, left to right."),
    positions: str = typer.Option("AAA", "--positions", help="Starting window letters."),
    rings: str = typer.Option("AAA", "--rings", help="Ring settings, left to right."),
    reflector: str = typer.Option("B", "--reflector", help="Reflector B or C."),
    plugboard: str = typer.Option("", "--plugboard", help="Space-separated pairs, e.g. 'AB CD'."),
) -> None:
    """Decrypt a message with the same settings and starting position."""
    _run(message, rotors, positions, rings, reflector, plugboard)
