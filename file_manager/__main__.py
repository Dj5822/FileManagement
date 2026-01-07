import typer  # type: ignore

from .commands import app as commands

app = typer.Typer()

app.add_typer(commands)

if __name__ == "__main__":
    app()
