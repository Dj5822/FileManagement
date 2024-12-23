import shutil
import os
from pathlib import Path
import inquirer
import typer
from rich import print
from rich.console import Console
from typing_extensions import Annotated

app = typer.Typer()
err_console = Console(stderr=True)
default_path = "C:\\Users\\Dj582\\Downloads\\"

@app.command()
def merge(
        path: Annotated[str, typer.Option(help="The directory to apply the command.")] = default_path
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
        print("Merging {} to {}".format(merge_folder, survivor_folder))

    if len(os.listdir()) == 0:
        print("The specified directory is empty.")
        return

    file_extension = os.listdir()[0].rsplit(".")[1]

    # code below is used to extend the file name.
    max_len = 0
    max_num = 0

    for file in os.listdir():
        if len(file.rsplit(".")[0]) > max_len:
            max_len = len(file.rsplit(".")[0])
        if int(file.rsplit(".")[0]) > max_num:
            max_num = int(file.rsplit(".")[0])

    os.chdir(merge_folder)

    for file in os.listdir():
        file_number = int(file.rsplit(".")[0]) + max_num
        new_name = "{}.{}".format(str(file_number), file_extension)
        shutil.move("{}\\{}".format(merge_folder, file), "{}\\{}".format(path, new_name))

    print("Files have been merged successfully.")

@app.command()
def rename(
        start: Annotated[int, typer.Option(help="The name of the starting file.")] = 0,
        digit_count: Annotated[int, typer.Option(help="The number of digits the output files should have.")] = 4,
        path: Annotated[str, typer.Option(help="The directory to apply the command.")] = default_path
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
        print("Renaming file in {}".format(main_folder))

    if len(os.listdir()) == 0:
        print("The specified directory is empty.")
        return

    file_extension = os.listdir()[0].rsplit(".")[-1]
    if digit_count is None:
        digit_count = len(str(start + len(os.listdir())))
    current_num = start

    for file in os.listdir():
        current_name = str(current_num)
        if len(current_name) < digit_count:
            current_name = "0" * (digit_count - len(current_name)) + current_name
        new_name = "{}.{}".format(current_name, file_extension)
        shutil.move("{}\\{}".format(main_folder, file), "{}\\{}".format(main_folder, new_name))
        current_num += 1

    print("Files within the folder have been renamed successfully.")

@app.command()
def extend(
           digit_count: Annotated[int, typer.Option(help="The number of digits the output files should have.")] = 4,
           path: Annotated[str, typer.Option(help="The directory to apply the command.")] = default_path
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
        print("Extending {}".format(main_folder))

    if len(os.listdir()) == 0:
        print("The specified directory is empty.")
        return

    file_extension: str = get_file_extension(os.listdir()[0])

    for file in os.listdir():
        current_name = file.rsplit(".")[0]
        if len(current_name) < digit_count:
            current_name = "0" * (digit_count - len(current_name)) + current_name
        new_name = "{}.{}".format(current_name, file_extension)
        shutil.move("{}\\{}".format(main_folder, file), "{}\\{}".format(main_folder, new_name))

def select_directory(path: str = default_path) -> str:
    """
    By default, the program path is set to C:\\Users\\Dj582\\Downloads\\
    """
    directories = [d.name for d in Path(path).iterdir() if d.is_dir()]

    questions = [
        inquirer.List(
            'directory',
            message="Select a directory",
            choices=directories,
        )
    ]

    selected_directory = inquirer.prompt(questions)
    return selected_directory['directory']

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

app()