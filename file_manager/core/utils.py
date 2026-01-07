import shutil
import os
from pathlib import Path
import inquirer  # type: ignore
from rich import print  # type: ignore
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
    return file_name.rsplit(".")[-1]


def extend_files(files, main_folder):
    file_extension: str = get_file_extension(files[0])

    current_names = {file: file.rsplit(".")[0] for file in files}
    digit_count = max(len(file) for file in current_names.values())
    extended_names = {
        file: "0" * max(digit_count - len(name), 0) + name
        for file, name in current_names.items()
    }
    new_names = {
        file: f"{name}.{file_extension}" for file, name in extended_names.items()
    }

    for file, name in new_names.items():
        shutil.move(f"{main_folder}\\{file}", f"{main_folder}\\{name}")
