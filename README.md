# File Management

This program can rename files in a particular pattern and merge two folders together.

## Application setup

- You must have Python3+ installed
- You must have Poetry installed

Run the following commands:
`poetry install`
`poetry run start`

## Type checking

When modifying this project, you use the following command to check typing issues:

`poetry run mypy ./file_management/file_manager.py`

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
