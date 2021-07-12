import shutil
import os


def merge(working_directory, target_directory):
    os.chdir(working_directory)

    print(os.getcwd())

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
        shutil.move("{}\\{}".format(target_directory, file), "{}\\{}".format(working_directory, new_name))

    print("Files have been merged successfully.")


def rename(working_directory):
    os.chdir(working_directory)

    print(os.getcwd())

    file_extension = os.listdir()[0].rsplit(".")[1]
    max_len = 0

    for file in os.listdir():
        if len(file.rsplit(".")[0]) > max_len:
            max_len = len(file.rsplit(".")[0])

    for file in os.listdir():
        file_number = file.rsplit(".")[0]
        if len(file.rsplit(".")[0]) != max_len:
            while len(file_number) < max_len:
                file_number = "0"+file_number
            new_name = "{}.{}".format(file_number, file_extension)
            shutil.move("{}\\{}".format(working_directory, file), "{}\\{}".format(working_directory, new_name))

    print("Files within the folder have been renamed successfully.")


"""
Program path is set to C:\\Users\\Dj582\\Downloads\\
"""

print("Assume that the folder located in downloads.")
main_dir = "C:\\Users\\Dj582\\Downloads\\"

while True:
    files = os.listdir(main_dir)
    print("Available files:")
    for i in range(len(files)):
        print("{}) {}".format(i+1, files[i]))

    print("List of operations:")
    print("merge (will merge two folders and name files numerically from starting from 0)")
    print("rename (will rename the files within a folder to have the same length of digits.")
    print("exit (will exit the program)")
    selection = input("Select an operation: ")

    if selection == "merge":
        try:
            folder_num = int(input("Select folder number: "))
            main_folder = os.path.join(main_dir, files[folder_num-1])
            merge_folder_num = int(input("Select the the folder that you want to merge with the main folder: "))
            merge_folder = os.path.join(main_dir, files[merge_folder_num-1])
            print(main_folder)
            merge(main_folder, merge_folder)
        except TypeError:
            print("Please enter a number.")
    elif selection == "rename":
        try:
            folder_num = int(input("Select folder number: "))
            main_folder = os.path.join(main_dir, files[folder_num-1])
            rename(main_folder)
        except TypeError:
            print("Please enter a number.")
    elif selection == "exit":
        break
