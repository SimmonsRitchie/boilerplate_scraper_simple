import logging
import os
import shutil
from pathlib import Path
from typing import List


def delete_dir_contents(folder):
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print("Failed to delete %s. Reason: %s" % (file_path, e))


def env_bool(env_name: str) -> bool:
    """
    Checks whether an env variable is 'true'. Returns false otherwise.

    Args:
        env_name (str): Name of env variable. eg. ENABLE_SLACK

    Returns:
        bool
    """
    env_value = os.getenv(env_name)
    if env_value and isinstance(env_value, str) and env_value.lower() == "true":
        return True
    return False


def get_files_in_dir(dir_path: Path) -> List:
    files_and_dirs = dir_path.glob("**/*")
    return [x for x in files_and_dirs if x.is_file()]


def remove_oldest_files(dir_path: Path, file_limit: int) -> None:
    """
    Removes the oldest files in a directory if they exceed a given limit.

    Args:
        dir_path (Path): Path to directory
        file_limit (int): If there are more than this many files, the oldest will be deleted.

    Returns:
        None
    """
    files = get_files_in_dir(dir_path)
    if len(files) > file_limit:
        logging.info(
            f"{dir_path.stem} dir exceeds limit of {file_limit} files. Deleting files based on oldest ctime..."
        )
        sorted_files = sorted(files, key=os.path.getctime)
        delete_list = sorted_files[file_limit:]
        for file in delete_list:
            file.unlink()
        logging.info(f"Files deleted: {delete_list}")
