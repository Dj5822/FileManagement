import shutil
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
def rename(
    start: Annotated[int, typer.Option(help="The name of the starting file.")] = 0,
    digit_count: Annotated[int, typer.Option(help="The number of digits the output files should have.")] = 4,
    path: Annotated[str, typer.Option(help="Used to configure the working directory.")] = get_default_path(),
) -> None:
    """
    Used to rename all the files within the folder such that all file names have the same number of digits.

    Example:

    If there exists the following files within a folder: 1.png 22.png 390.png

    Then after renaming, all the files we be changed to: 001.png 022.png 390.png
    """

    selected: str = select_directory(path)
    main_folder = os.path.join(path, selected)

    if not change_directory(main_folder):
        err_console.print("Failed to find the specified path")
        return
    else:
        print(f"Renaming file in {main_folder}")

    if len(os.listdir()) == 0:
        print("The specified directory is empty.")
        return

    extend_files(os.listdir(), main_folder)

    files = sorted(os.listdir())
    file_extension = files[0].rsplit(".")[-1]

    digit_count = len(str(start + len(files))) if digit_count is None else digit_count

    file_nums = [str(file_num) for file_num in range(start, start + len(files))]
    processed_names = {
        file: "0" * max(digit_count - len(file_nums[i]), 0) + file_nums[i]
        for i, file in enumerate(files)
    }
    new_names = {
        file: f"{name}.{file_extension}" for file, name in processed_names.items()
    }

    for file, name in new_names.items():
        shutil.move(f"{main_folder}\\{file}", f"{main_folder}\\{name}")

    print("Files within the folder have been renamed successfully.")
