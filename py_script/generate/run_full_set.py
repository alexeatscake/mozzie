import argparse
from pathlib import Path

import yaml
from tqdm import tqdm

from mozzie.generate import run_custom


def main(config_path: str):
    main_dir = Path(__file__).resolve().parent.parent.parent
    script_path = main_dir / "GeneralMetapop/build/gdsimsapp"
    config_path = main_dir / config_path
    working_dir = main_dir / config_path.parent
    params_dir = working_dir / "params"

    if not config_path.is_file():
        msg = f"Config file not found at {config_path}"
        raise FileNotFoundError(msg)

    if not script_path.exists():
        msg = f"GDSiMS script not found at {script_path}"
        raise FileNotFoundError(msg)

    if not params_dir.is_dir():
        msg = f"Params folder not found at {params_dir}"
        raise FileNotFoundError(msg)

    with open(config_path) as file:
        config = yaml.safe_load(file)

    txt_files = sorted(params_dir.glob("*.txt"))
    if not txt_files:
        print(f"No .txt files found in {params_dir}")
        return

    coords_set = config.get("coords_set")
    if coords_set is not None:
        coords_path = main_dir / coords_set.get("coords_path", "")
        if coords_path.is_file():
            # If coords_path is a file, we use it every time
            input_values = [
                (str(script_path), str(working_dir), str(params_path), str(coords_path))
                for params_path in txt_files
            ]
        elif coords_path.is_dir():
            # If coords_path is a directory, we look for corresponding coords files
            coords_files = []
            for params_path in txt_files:
                coords_name = params_path.stem.replace("params_", "coords_")
                coord_loc = coords_path / f"{coords_name}.csv"
                if not coord_loc.exists():
                    msg = f"Coordinates file {coord_loc} does not exist."
                    raise FileNotFoundError(msg)
                coords_files.append(coord_loc)

            input_values = [
                (str(script_path), str(working_dir), str(params_path), str(coords_file))
                for params_path, coords_file in zip(
                    txt_files, coords_files, strict=True
                )
            ]
        else:
            msg = (
                "coords_path in config included must be a file or directory."
                f"Coordinates file or directory not found at {coords_path}"
            )
            raise FileNotFoundError(msg)
    else:
        # If no coords_set, we assume no coordinates are to be used
        input_values = [
            (str(script_path), str(working_dir), str(params_path), None)
            for params_path in txt_files
        ]

    print(f"Found {len(input_values)} .txt files to process in {params_dir}")
    print("Only using one worker for processing.")

    for settings in (pbar := tqdm(input_values)):
        pbar.set_postfix_str(Path(settings[2]).name)
        run_custom(*settings)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Run GDSiMS for all .txt params in a folder."
    )
    parser.add_argument(
        "config_path",
        type=str,
        help="Path to the experiment config set from the main directory.",
    )
    main(parser.parse_args().config_path)
