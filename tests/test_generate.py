from pathlib import Path

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
