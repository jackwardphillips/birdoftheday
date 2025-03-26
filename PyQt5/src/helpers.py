import os

def check_directory(path: str) -> None:
    if not os.path.exists(path):
        os.mkdir(path)
    return