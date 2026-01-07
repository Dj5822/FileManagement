import os
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
    path: Annotated[
        str, typer.Option(help="The directory to apply the command.")
    ] = None,
) -> None:
    """
    Given a directory of files, it will rename all the files within that directory
    such that all the file names are the same length.
    Typically, this will be done by adding '0' to the front of each file name
    until the length matches the largest file length.
    """

    path = get_default_path() if path is None else path

    selected: str = select_directory(path)
    main_folder = os.path.join(path, selected)

    if not change_directory(main_folder):
        err_console.print("Failed to find the specified path")
        return
    else:
        print(f"Extending {main_folder}")

    if len(os.listdir()) == 0:
        print("The specified directory is empty.")
        return

    files = os.listdir()

    extend_files(files, main_folder)
