import pytest

from helper.misc import remove_oldest_files, get_files_in_dir


def test_remove_oldest_files(dir_too_many_files):
    limit = 5
    remove_oldest_files(dir_too_many_files, limit)
    files = get_files_in_dir(dir_too_many_files)
    assert len(files) <= limit
    assert not len(files) <= limit - 1
