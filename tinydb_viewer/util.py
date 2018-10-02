import os


def get_file_id(file_path):
    try:
        return os.stat(file_path).st_ino
    except FileNotFoundError:
        return None
