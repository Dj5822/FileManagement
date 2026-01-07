import os
from pathlib import Path
import typer  # type: ignore
from rich import print  # type: ignore
from rich.console import Console  # type: ignore
from typing_extensions import Annotated

from ..core.utils import (
    change_directory,
    extend_files,
    select_directory,
    get_default_path,
)

app = typer.Typer()
err_console = Console(stderr=True)


@app.command()
def extend(
    path: Annotated[Path, typer.Option(help="Used to configure the working directory.")] = get_default_path(),
) -> None:
    """
    Given a directory of files, it will rename all the files within that directory
    such that all the file names have the same length.
    Typically, this will be done by adding '0' to the front of each file name
    until the length matches the largest file length.
    """

    selected: str = select_directory(path)
    target_folder = Path(path) / selected

    if not change_directory(target_folder):
        err_console.print("Failed to find the specified path")
        return
    else:
        print(f"Extending {target_folder}")

    if len(os.listdir()) == 0:
        print("The specified directory is empty.")
        return

    files = os.listdir()

    extend_files(files, target_folder)
