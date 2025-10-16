import argparse
from pathlib import Path

from mozzie.generate import run_custom


def main(params_path: str | Path, coords_path: str | Path | None = None):
    main_dir = Path(__file__).resolve().parent.parent.parent

    script_path = main_dir / "GeneralMetapop/build/gdsimsapp"
    working_dir = main_dir / "data/generated/example"
    params_path = main_dir / params_path
    if coords_path is not None:
        coords_path = main_dir / coords_path

    if not script_path.exists():
        msg = f"GDSiMS params not found at {params_path}"
        raise FileNotFoundError(msg)

    output = run_custom(
        script_path=script_path,
        working_dir=working_dir,
        params_path=params_path,
        coords_path=coords_path,
    )

    print("Output from GDSiMS script:")
    print(output)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run GDSiMS with default parameters.")
    parser.add_argument(
        "params_path",
        type=str,
        help="Relative path to the GDSiMS script.",
    )
    parser.add_argument(
        "--coords_path",
        type=str,
        help="Relative path to the coordinates file (if needed).",
        default=None,
    )
    main(parser.parse_args().params_path, parser.parse_args().coords_path)
