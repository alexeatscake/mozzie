import argparse
import glob
import os

from tqdm import tqdm

from mozzie.generate import run_custom


def main(set_path: str):
    main_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
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

    for params_path in (pbar := tqdm(sorted(tex_files))):
        pbar.set_postfix_str(os.path.basename(params_path))
        run_custom(
            script_path=script_path,
            working_dir=working_dir,
            params_path=params_path,
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
    main(parser.parse_args().set_path)
