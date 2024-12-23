import shutil
import os


def merge(directory: str, target_directory: str) -> None:
    if not change_directory(directory):
        print("Failed to find the specified directory")

    file_extension = os.listdir()[0].rsplit(".")[1]

    # code below is used to extend the file name.
    max_len = 0
    max_num = 0

    for file in os.listdir():
        if len(file.rsplit(".")[0]) > max_len:
            max_len = len(file.rsplit(".")[0])
        if int(file.rsplit(".")[0]) > max_num:
            max_num = int(file.rsplit(".")[0])

    os.chdir(target_directory)

    for file in os.listdir():
        file_number = int(file.rsplit(".")[0]) + max_num
        new_name = "{}.{}".format(str(file_number), file_extension)
        shutil.move("{}\\{}".format(target_directory, file), "{}\\{}".format(directory, new_name))

    print("Files have been merged successfully.")


def rename(directory: str, start_num: int = 0, digit_count: int = 3) -> None:
    if not change_directory(directory):
        print("Failed to find the specified directory")

    file_extension = os.listdir()[0].rsplit(".")[-1]
    if digit_count is None:
        digit_count = len(str(start_num + len(os.listdir())))
    current_num = start_num

    for file in os.listdir():
        current_name = str(current_num)
        while len(current_name) < digit_count:
            current_name = "0" + current_name
        new_name = "{}.{}".format(current_name, file_extension)
        shutil.move("{}\\{}".format(directory, file), "{}\\{}".format(directory, new_name))
        current_num += 1

    print("Files within the folder have been renamed successfully.")


def extend(directory: str, digit_count: int = 4) -> None:
    """
    Given a directory of files, it will rename all the files within that directory
    such that all the file names are the same length.
    Typically, this will be done by adding '0' to the front of each file name
    until the length matches the largest file length.
    """

    if not change_directory(directory):
        print("Failed to find the specified directory")
    file_extension: str = get_file_extension(os.listdir()[0])

    for file in os.listdir():
        current_name = file.rsplit(".")[0]
        while len(current_name) < digit_count:
            current_name = "0" + current_name
        new_name = "{}.{}".format(current_name, file_extension)
        shutil.move("{}\\{}".format(directory, file), "{}\\{}".format(directory, new_name))


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
    finally:
        return False


def get_file_extension(file_name: str) -> str:
    """
    Given a file name, returns the file extension.
    """
    return file_name.rsplit(".")[-1]


def main() -> None:
    """
    Program path is set to C:\\Users\\Dj582\\Downloads\\
    """

    print("Assume that the folder located in downloads.")
    main_dir = "C:\\Users\\Dj582\\Downloads\\"

    while True:
        files = os.listdir(main_dir)
        print("Available files:")
        for i in range(len(files)):
            print("{}) {}".format(i + 1, files[i]))

        print("List of operations:")
        print("merge (will merge two folders and name files numerically from starting from 0)")
        print("rename (will rename the files within a folder to have the same length of digits.")
        print("extend")
        print("exit (will exit the program)")
        selection = input("Select an operation: ")

        if selection == "merge":
            try:
                folder_num = int(input("Select folder number: "))
                main_folder = os.path.join(main_dir, files[folder_num - 1])
                merge_folder_num = int(input("Select the the folder that you want to merge with the main folder: "))
                merge_folder = os.path.join(main_dir, files[merge_folder_num - 1])
                print(main_folder)
                merge(main_folder, merge_folder)
            except TypeError:
                print("Please enter a number.")
        elif selection == "rename":
            try:
                folder_num = int(input("Select folder number: "))
                start = int(input("Input start number: "))
                main_folder = os.path.join(main_dir, files[folder_num - 1])
                rename(main_folder, start)
            except TypeError:
                print("Please enter a number.")
        elif selection == "extend":
            try:
                folder_num = int(input("Select folder number: "))
                main_folder = os.path.join(main_dir, files[folder_num - 1])
                extend(main_folder)
            except TypeError:
                print("Please enter a number.")
        elif selection == "exit":
            break
