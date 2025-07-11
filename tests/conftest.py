import pytest


@pytest.fixture()
def working_dir(tmp_path_factory) -> pytest.TempPathFactory:
    """
    Fixture to create a temporary output directory for tests.

    Returns:
        pytest.TempPathFactory: A temporary path factory for creating directories.
    """
    return tmp_path_factory.mktemp("output")
