import shutil
import os
from pathlib import Path
import inquirer  # type: ignore
from rich import print  # type: ignore
from rich.progress import track
from rich.table import Table
import yaml


def load_config():
    CONFIG_FILE_PATH = Path("./config.yaml")
    with open(CONFIG_FILE_PATH, "r", encoding="utf-8") as file:
        config_data = yaml.load(file, Loader=yaml.FullLoader)
        return config_data


def get_default_path() -> Path:
    config = load_config()
    return Path(config["default-path"])


def select_directory(path: str) -> str:
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


def change_directory(new_path: Path) -> bool:
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
    return Path(file_name).suffix


def extend_files(files: list[str], target_folder: Path, filler_char: str = '0'):
    """
    Given a list of files, return a dict which represents how each file will be transformed
    after extending the file length by appending a filler character to the left of the file.
    """

    file_extension: str = get_file_extension(files[0])

    current_names = {file: Path(file).stem for file in files}
    digit_count = max(len(file) for file in current_names.values())
    extended_names = {
        file: filler_char * max(digit_count - len(name), 0) + name
        for file, name in current_names.items()
    }
    result = {
        target_folder / file: target_folder / f"{name}{file_extension}" for file, name in extended_names.items()
    }

    return result


def show_result(result: dict[Path, Path]) -> None:
    table = Table(title="Result")
    table.add_column("Previous Name")
    table.add_column("New Name")
    for old_name, new_name in result.items():
        table.add_row(old_name.name, new_name.name)
    print(table)


def execute_modification(result: dict[Path, Path]) -> bool:
    try:
        for old_name, new_name in track(result.items(), description="Modifying files..."):
            shutil.move(old_name, new_name)
        return True
    except Exception:
        return False