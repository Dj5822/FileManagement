import shutil
import os
from pathlib import Path
import inquirer # type: ignore
import typer # type: ignore
from rich import print # type: ignore
from rich.console import Console # type: ignore
from typing_extensions import Annotated
import yaml

app = typer.Typer()
err_console = Console(stderr=True)
CONFIG_FILE_PATH = './config.yaml'
with open(CONFIG_FILE_PATH, "r", encoding="utf-8") as file:
    config_data = yaml.load(file, Loader=yaml.FullLoader)
    default_path = config_data["default-path"]

@app.command()
def merge(
    path: Annotated[
        str, typer.Option(help="The directory to apply the command.")
    ] = default_path,
) -> None:
    """
    Used to merge to folders together while maintaining order.
    """
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
        shutil.move(
            f"{merge_folder}\\{file}", f"{path}\\{new_name}"
        )

    print("Files have been merged successfully.")


@app.command()
def rename(
    start: Annotated[int, typer.Option(help="The name of the starting file.")] = 0,
    digit_count: Annotated[
        int, typer.Option(help="The number of digits the output files should have.")
    ] = 4,
    path: Annotated[
        str, typer.Option(help="The directory to apply the command.")
    ] = default_path,
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

    file_nums = [str(file_num) for file_num in range(start,start+len(files))]
    processed_names = { file : "0" * max(digit_count - len(file_nums[i]), 0) + file_nums[i] for i, file in enumerate(files) }
    new_names = { file: f"{name}.{file_extension}" for file, name in processed_names.items() }

    for file, name in new_names.items():
        shutil.move(
            f"{main_folder}\\{file}", f"{main_folder}\\{name}"
        )

    print("Files within the folder have been renamed successfully.")


@app.command()
def extend(
    path: Annotated[
        str, typer.Option(help="The directory to apply the command.")
    ] = default_path,
) -> None:
    """
    Given a directory of files, it will rename all the files within that directory
    such that all the file names are the same length.
    Typically, this will be done by adding '0' to the front of each file name
    until the length matches the largest file length.
    """
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


def select_directory(path: str = default_path) -> str:
    """
    By default, the program path is set to C:\\Users\\Dj582\\Downloads\\
    """
    directories = [d.name for d in Path(path).iterdir() if d.is_dir()]

    questions = [
        inquirer.List(
            "directory",
            message="Select a directory",
            choices=directories,
        )
    ]

    selected_directory = inquirer.prompt(questions)
    return selected_directory["directory"]


def change_directory(new_path: str) -> bool:
    """
    Set the working directory.
    Returns true when directory changed successfully.
    Otherwise, returns false.
    """
    try:
        os.chdir(new_path)
        print("Currently in: " + os.getcwd())
        return True
    except OSError:
        return False


def get_file_extension(file_name: str) -> str:
    """
    Given a file name, returns the file extension.
    """
    return file_name.rsplit(".")[-1]


def extend_files(files, main_folder):
    file_extension: str = get_file_extension(files[0])

    current_names = { file : file.rsplit(".")[0] for file in files }
    digit_count = max(len(file) for file in current_names.values())
    extended_names = { file : "0" * max(digit_count - len(name), 0) + name for file, name in current_names.items() }
    new_names = { file: f"{name}.{file_extension}" for file, name in extended_names.items() }

    for file, name in new_names.items():
        shutil.move(f"{main_folder}\\{file}", f"{main_folder}\\{name}")

def main():
    app()

if __name__ == "__main__":
    main()
