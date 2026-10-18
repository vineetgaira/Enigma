"""This file does the work of parsing and CLI input that we are going to take from the user. It will use typer."""

import typer

app = typer.Typer(
    name = "Enigma",
    help = "A python replica of German Enigma machine.",
    no_args_is_help = True,
)

@app.command()
def encrypt():
    """Encrypt a message using this command."""

    typer.echo("Encryption is not yet implemented.")

@app.command()
def decrypt():
    """Decrypt a message using this command."""

    typer.echo("cryption is not yet implemented.")