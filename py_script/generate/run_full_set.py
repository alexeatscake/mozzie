import argparse
from pathlib import Path

from tqdm import tqdm

from mozzie.generate import run_custom


def main(set_path: str):
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

    tex_files = sorted(params_dir.glob("*.txt"))
    if not tex_files:
        print(f"No .tex files found in {params_dir}")
        return

    for params_path in (pbar := tqdm(tex_files)):
        pbar.set_postfix_str(params_path.name)
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
