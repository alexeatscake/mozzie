import argparse
import os
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

from tqdm import tqdm

from mozzie.generate import run_custom


def run_for_parallel(x):
    return run_custom(*x)


def main(set_path: str, number_of_workers: int):
    main_dir = Path(__file__).resolve().parent.parent.parent
    script_path = main_dir / "GeneralMetapop/build/gdsimsapp"
    working_dir = main_dir / set_path
    params_dir = working_dir / "params"

    if not script_path.exists():
        msg = f"GDSiMS script not found at {script_path}"
        raise FileNotFoundError(msg)

    if not params_dir.is_dir():
        msg = f"Params folder not found at {params_dir}"
        raise FileNotFoundError(msg)

    txt_files = sorted(params_dir.glob("*.txt"))
    if not txt_files:
        print(f"No .txt files found in {params_dir}")
        return

    input_values = [
        (str(script_path), str(working_dir), str(params_path))
        for params_path in txt_files
    ]

    print(f"Found {len(input_values)} .txt files to process in {params_dir}")
    print(f"Using {number_of_workers} workers for processing.")
    with ProcessPoolExecutor(max_workers=number_of_workers) as executor:
        list(
            tqdm(
                executor.map(run_for_parallel, input_values),
                total=len(input_values),
            )
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Run GDSiMS for all .tex params in a folder."
    )
    parser.add_argument(
        "set_path",
        type=str,
        help="Relative path to the experiment set.",
    )
    number_of_workers = os.environ.get("WORKERS_FOR_MOZZIE", "4")
    main(parser.parse_args().set_path, int(number_of_workers))
