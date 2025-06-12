import argparse
import glob
import os
from concurrent.futures import ProcessPoolExecutor

from tqdm import tqdm

from mozzie.generate import run_custom


def run_for_parallel(x):
    return run_custom(*x)


def main(set_path: str, number_of_workers: int):
    main_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
    script_path = os.path.join(main_dir, "GeneralMetapop/build/gdsimsapp")
    working_dir = os.path.join(main_dir, set_path)
    params_dir = os.path.join(main_dir, set_path, "params")

    if not os.path.exists(script_path):
        msg = f"GDSiMS script not found at {script_path}"
        raise FileNotFoundError(msg)

    if not os.path.isdir(params_dir):
        msg = f"Params folder not found at {params_dir}"
        raise FileNotFoundError(msg)

    tex_files = glob.glob(os.path.join(params_dir, "*.txt"))
    if not tex_files:
        print(f"No .tex files found in {params_dir}")
        return

    input_values = [
        (script_path, working_dir, params_path) for params_path in sorted(tex_files)
    ]

    print(f"Found {len(input_values)} .tex files to process in {params_dir}")
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
    print(os.environ)
    main(parser.parse_args().set_path, int(number_of_workers))
