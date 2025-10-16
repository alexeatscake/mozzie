from pathlib import Path
from unittest.mock import patch

import pandas as pd
import pytest

import mozzie

REPO_ROOT = Path(__file__).resolve().parent.parent
METAPOP_LOC = REPO_ROOT / "GeneralMetapop" / "build" / "gdsimsapp"


def test_run_default(working_dir: Path):
    """
    Test running the GDSiMS script with default parameters.

    Args:
        out_path (Path): Path to the output directory.
    """
    working_default_dir = working_dir / "default"
    working_default_dir.mkdir()
    output = mozzie.generate.run_default(METAPOP_LOC, working_default_dir)
    msg = "Program did not give expected output."
    assert "Program run time" in output, msg
    out_file_dir = working_default_dir / "output_files"
    msg = "Output directory not created as expected."
    assert out_file_dir.is_dir(), msg
    msg = "Expected output files not found in the output directory."
    assert (out_file_dir / "Totals1run1.txt").is_file(), msg
    assert (out_file_dir / "Totals1run2.txt").is_file(), msg
    assert (out_file_dir / "CoordinateList1run1.txt").is_file(), msg
    assert (out_file_dir / "CoordinateList1run2.txt").is_file(), msg
    assert (out_file_dir / "LocalData1run1.txt").is_file(), msg
    assert (out_file_dir / "LocalData1run2.txt").is_file(), msg
    # Additional checks for specific output files

    total1_df = pd.read_csv(out_file_dir / "Totals1run1.txt", sep="\t", header=1)
    msg = "Totals1run1.txt does not contain expected data."
    assert not total1_df.empty, msg
    assert "WW" in total1_df.columns, msg
    assert total1_df.shape[0] == 1001, msg


def test_run_custom(working_dir: Path):
    """
    Test running the GDSiMS script with custom parameters.

    Args:
        out_path (Path): Path to the output directory.
    """
    working_custom_dir = working_dir / "custom"
    working_custom_dir.mkdir()
    params_path = REPO_ROOT / "tests" / "test_data" / "test_params.txt"
    output = mozzie.generate.run_custom(METAPOP_LOC, working_custom_dir, params_path)
    msg = "Program did not give expected output."
    assert "Program run time" in output, msg
    out_file_dir = working_custom_dir / "output_files"
    msg = "Output directory not created as expected."
    assert out_file_dir.is_dir(), msg
    msg = "Expected output files not found in the output directory."
    assert (out_file_dir / "Totals1001run1.txt").is_file(), msg
    assert (out_file_dir / "CoordinateList1001run1.txt").is_file(), msg
    assert (out_file_dir / "LocalData1001run1.txt").is_file(), msg

    total1_df = pd.read_csv(out_file_dir / "Totals1001run1.txt", sep="\t", header=1)
    msg = "Totals1001run1.txt does not contain expected data."
    assert not total1_df.empty, msg
    assert "WW" in total1_df.columns, msg
    assert total1_df.shape[0] == 101, msg


def test_run_with_coords(working_dir: Path):
    """
    Test running the GDSiMS script with coordinates.

    Args:
        out_path (Path): Path to the output directory.
    """
    working_coords_dir = working_dir / "coords"
    working_coords_dir.mkdir()
    params_path = REPO_ROOT / "tests" / "test_data" / "test_coord_params.txt"
    coords_path = REPO_ROOT / "tests" / "test_data" / "test_coords.csv"
    output = mozzie.generate.run_custom_with_coords(
        METAPOP_LOC, working_coords_dir, params_path, coords_path
    )
    msg = "Program did not give expected output."
    assert "Program run time" in output, msg
    out_file_dir = working_coords_dir / "output_files"
    msg = "Output directory not created as expected."
    assert out_file_dir.is_dir(), msg
    msg = "Expected output files not found in the output directory."
    assert (out_file_dir / "Totals1002run1.txt").is_file(), msg
    assert (out_file_dir / "CoordinateList1002run1.txt").is_file(), msg
    assert (out_file_dir / "LocalData1002run1.txt").is_file(), msg

    total1_df = pd.read_csv(out_file_dir / "Totals1002run1.txt", sep="\t", header=1)
    msg = "Totals1002run1.txt does not contain expected data."
    assert not total1_df.empty, msg
    assert "WW" in total1_df.columns, msg
    assert total1_df.shape[0] == 51, msg


def test_run_default_stdin_error(working_dir: Path):
    """
    Test run_default to simulate stdin error.
    """
    working_default_dir = working_dir / "default"
    working_default_dir.mkdir()

    with patch("subprocess.Popen") as mock_popen:
        mock_process = mock_popen.return_value
        mock_process.stdin = None  # Simulate stdin being None
        mock_process.communicate.return_value = (b"", b"")

        with pytest.raises(RuntimeError, match="Failed to open stdin for the process."):
            mozzie.generate.run_default(METAPOP_LOC, working_default_dir)


def test_run_custom_stdin_error(working_dir: Path):
    """
    Test run_custom to simulate stdin error.
    """
    working_custom_dir = working_dir / "custom"
    working_custom_dir.mkdir()
    params_path = REPO_ROOT / "tests" / "test_data" / "test_params.txt"

    with patch("subprocess.Popen") as mock_popen:
        mock_process = mock_popen.return_value
        mock_process.stdin = None  # Simulate stdin being None
        mock_process.communicate.return_value = (b"", b"")

        with pytest.raises(RuntimeError, match="Failed to open stdin for the process."):
            mozzie.generate.run_custom(METAPOP_LOC, working_custom_dir, params_path)
