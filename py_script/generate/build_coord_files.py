import argparse
from pathlib import Path

import numpy as np
import pandas as pd
import yaml
from tqdm import tqdm

from mozzie.coords import make_grid_coords
from mozzie.data_prep import read_config


def load_coords_set(config: dict) -> dict:
    """Extract and validate coords_set section; create output directory."""
    coords_set = config.get("coords_set")
    if coords_set is None:
        msg = "coords_set section missing in config."
        raise ValueError(msg)
    if coords_set.get("coords_type") not in ["grid"]:
        msg = "coords_type must be 'grid' for this script."
        raise NotImplementedError(msg)
    required_top = ["coords_path", "coords_type", "release_sites"]
    for key in required_top:
        if key not in coords_set:
            msg = f"coords_set missing required key: {key}"
            raise ValueError(msg)

    return coords_set


def main(rel_config_path: str):
    main_dir = Path(__file__).resolve().parent.parent.parent

    # Make Parameters folder
    config_path = Path(rel_config_path)
    params_folder = config_path.parent / "params"
    params_folder.mkdir(exist_ok=True)

    # Load Config and Check Validity
    with (main_dir / config_path).open() as file:
        config = yaml.safe_load(file)

    # Continue to read parameter sampling config (left as-is for future use)
    _, _, num_samples, start_index, _ = read_config(config)

    # Load coords_set (first goal)
    coords_set = load_coords_set(config)

    # Check coords_path directory
    coords_path = main_dir / coords_set["coords_path"]
    if not coords_path.exists():
        if not coords_path.parent.exists():
            msg = f"Coordinates path {coords_path.parent} does not exist."
            raise FileNotFoundError(msg)
        coords_path.mkdir(exist_ok=True)
    elif coords_path.is_file():
        msg = f"Coordinates path {coords_path} already exists as a file."
        raise FileExistsError(msg)

    if coords_set.get("coords_type") == "grid":
        coord_list = make_grid_coords(coords_set)
    else:
        msg = "Only 'grid' coords_type is supported in this script."
        raise NotImplementedError(msg)

    num_release_sites = int(coords_set["release_sites"])
    if num_release_sites <= 0:
        msg = "Number of release sites must be a positive integer."
        raise ValueError(msg)
    if num_release_sites > len(coord_list):
        msg = (
            f"Number of release sites ({num_release_sites}) exceeds "
            f"available coordinates ({len(coord_list)})."
        )
        raise ValueError(msg)

    col_names = [[f"x_{i+1}", f"y_{i+1}"] for i in range(num_release_sites)]

    release_sites_df = pd.DataFrame(
        columns=np.concatenate([["sample_idx"], *col_names]),
    )

    coords_default = pd.DataFrame(
        {
            "x": [coord[0] for coord in coord_list],
            "y": [coord[1] for coord in coord_list],
            "if": ["n" for _ in coord_list],
        }
    )

    for s_i in tqdm(range(start_index, start_index + num_samples)):
        # Pick num_release_sites coordinates without replacement
        selected_indices = np.random.choice(
            len(coord_list) - 1, num_release_sites, replace=False
        )  # -1 is to avoid the off-by-one error in GDSiMS
        selected_coords = [coord_list[i] for i in selected_indices]

        # Place selected coordinates into the dataframe
        row = [s_i] + [coord for pair in selected_coords for coord in pair]
        release_sites_df.loc[len(release_sites_df)] = row

        # Update 'if' column in these_coords for selected coordinates
        these_coords = coords_default.copy()
        these_coords.loc[selected_indices, "if"] = "y"

        # Save the coordinates for this sample
        sample_coords_path = coords_path / f"coords_{s_i}.csv"
        these_coords.to_csv(sample_coords_path, sep="\t", index=False)

    # Save the dataframe to a CSV file
    release_sites_df["sample_idx"] = release_sites_df["sample_idx"].astype(int)
    release_sites_df.to_csv(coords_path.parent / "release_sites.csv", index=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Build the coords files for GDSiMS from a config file."
    )
    parser.add_argument(
        "config_path",
        type=str,
        help="Relative path to the sampling config setting.",
    )
    main(parser.parse_args().config_path)
