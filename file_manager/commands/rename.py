from pathlib import Path
import shutil
import os
import typer  # type: ignore
from rich import print  # type: ignore
from rich.console import Console  # type: ignore
from typing_extensions import Annotated

from ..core.utils import (
    change_directory,
    execute_modification,
    extend_files,
    get_file_extension,
    select_directory,
    get_default_path,
    show_result,
)

app = typer.Typer()
err_console = Console(stderr=True)


@app.command()
def rename(
    start: Annotated[int, typer.Option(help="The name of the starting file.")] = 0,
    digit_count: Annotated[int, typer.Option(help="The number of digits the output files should have.")] = 4,
    path: Annotated[Path, typer.Option(help="Used to configure the working directory.")] = get_default_path(),
) -> None:
    """
    Used to rename all the files within the folder such that all file names have the same number of digits.

    Example:

    If there exists the following files within a folder: 1.png 22.png 390.png

    Then after renaming, all the files we be changed to: 001.png 022.png 390.png
    """

    selected: str = select_directory(path)
    target_folder = Path(path) / selected
    files = os.listdir(target_folder)

    if len(files) == 0:
        print("The specified directory is empty.")
        return

    extension_result = extend_files(files, target_folder)
    execute_modification(extension_result)

    files = sorted(os.listdir(target_folder))
    file_extension = get_file_extension(files[0])

    digit_count = len(str(start + len(files))) if digit_count is None else digit_count

    file_nums = [str(file_num) for file_num in range(start, start + len(files))]
    processed_names = {
        file: "0" * max(digit_count - len(file_nums[i]), 0) + file_nums[i]
        for i, file in enumerate(files)
    }
    result = {
        target_folder / file: target_folder / f"{name}{file_extension}" for file, name in processed_names.items()
    }

    show_result(result)

    if typer.confirm(f"Are you sure you want to extend the file names?"):
        execute_modification(result)
        print("Files within the folder have been renamed successfully.")
    else:
        print("Operation cancelled.")


