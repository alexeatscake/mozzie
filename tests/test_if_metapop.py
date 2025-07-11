from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
METAPOP_DIR = REPO_ROOT / "GeneralMetapop"
BUILD_LOC = METAPOP_DIR / "build" / "gdsimsapp"


def test_submodule_checked_out():
    """Fail fast if the sub-module was not cloned with --recursive."""
    msg = "No GeneralMetapop did you forget --recursive?"
    assert METAPOP_DIR.is_dir(), msg


def test_metapop_build():
    """Test if the metapop has been built."""
    msg = f"Metapop not built, expected directory {BUILD_LOC} does not exist."
    assert BUILD_LOC.is_file(), msg
