# File Management
This program can rename files in a particular pattern and merge two folders together.

## How to run the program
First, make sure that the latest version of Python is installed.

Next, navigate to the directory where main.py is located.

Try the following commands:

`py main.py`

`python main.py`

`python3 main.py`

If that doesn't work, then you probably screwed up your Python installation or something.

## Type checking
When modifying this project, you use the following command to check typing issues:

`py -m mypy main.py`

## Rename
Used to rename all the files within the folder such that all file names have the same number of digits.

### Example 
If there exists the following files within a folder: 
1.png 22.png 390.png

Then after renaming, all the files we be changed to: 
001.png 022.png 390.png

## Merge
Used to merge to folders together while maintaining order.

### Example 
If there exists the following two folders:

Directory 1: 1.png, 2.png, 3.png

Directory 2: 1.png, 2.png, 3.png

Merged result: 1.png, 2.png, 3.png, 4.png, 5.png, 6.png
