"""This file does the work of parsing and CLI input that we are going to take from the user. It will use typer."""

import typer

app = typer.Typer(
    name = "Enigmac",
    help = "A python replica of German Enigma machine.",
    no_args_is_help = True,
)


@app.command
def encrypt() -> None:
    """Encrypt a message using this command."""

    print("Encryption is not yet implemented.")