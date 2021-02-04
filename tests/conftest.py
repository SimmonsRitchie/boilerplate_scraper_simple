from pathlib import Path

import pytest
from dotenv import load_dotenv
from typing import Dict

from definitions import DIR_TESTS_FIXTURES
from src.helper.pandas_opts import pandas_opts


def pytest_configure(config):
    """
    Allows plugins and conftest files to perform initial configuration.
    This hook is called for every plugin and initial conftest
    file after command line options have been parsed.
    """
    # Makes it easier to see pandas DFs when printing to console
    pandas_opts()
    load_dotenv()


@pytest.fixture
def dir_too_many_files(tmpdir) -> None:
    """
    Example fixture.

    """
    # test_dir = DIR_TESTS_FIXTURES / "too_many_files"
    tmpdir = Path(tmpdir)
    print("tmpdir", tmpdir)
    for x in range(1, 11):
        with open(tmpdir / f"test-file-{x}.txt", "w") as fin:
            fin.write(str(x))
    return tmpdir
