import shutil
import os
import typer  # type: ignore
from rich import print  # type: ignore
from rich.console import Console  # type: ignore
from typing_extensions import Annotated

from ..core.utils import change_directory, select_directory, get_default_path

app = typer.Typer()
err_console = Console(stderr=True)


@app.command()
def merge(
    path: Annotated[
        str, typer.Option(help="The directory to apply the command.")
    ] = None,
) -> None:
    """
    Used to merge to folders together while maintaining order.
    """

    path = get_default_path() if path is None else path

    print("Select the survivor directory.")
    survivor: str = select_directory(path)
    survivor_folder = os.path.join(path, survivor)

    if not change_directory(survivor_folder):
        err_console.print("Failed to find the specified path")

    print("Select the victim directory.")
    victim: str = select_directory(path)
    merge_folder = os.path.join(path, victim)

    if not change_directory(merge_folder):
        err_console.print("Failed to find the specified path")
    else:
        print(f"Merging {merge_folder} to {survivor_folder}")

    if len(os.listdir()) == 0:
        print("The specified directory is empty.")
        return

    file_extension = os.listdir()[0].rsplit(".")[1]

    max_num = max(int(file.rsplit(".")[0]) for file in os.listdir())

    os.chdir(merge_folder)

    for file in os.listdir():
        file_number = int(file.rsplit(".")[0]) + max_num
        new_name = f"{str(file_number)}.{file_extension}"
        shutil.move(f"{merge_folder}\\{file}", f"{path}\\{new_name}")

    print("Files have been merged successfully.")
