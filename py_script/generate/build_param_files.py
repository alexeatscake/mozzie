import argparse
import os

import yaml
from autoemulate.experimental_design import LatinHypercube
from tqdm import tqdm

from mozzie.data_prep import read_config
from mozzie.generate import parameter_order


def main(config_path: str):
    main_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))

    # Make Parameters folder
    params_folder = os.path.join(os.path.dirname(config_path), "params")
    os.makedirs(params_folder, exist_ok=True)

    # Load Config and Check Validity
    with open(os.path.join(main_dir, config_path)) as file:
        config = yaml.safe_load(file)

    set_values, to_sample, num_samples, start_index, _ = read_config(config)

    # Pull out the parameters to sample
    cube_ranges = []
    cube_names = []
    for param_name, param_options in to_sample.items():
        if param_options["type"] != "float":
            msg = f"Unsupported type {param_options['type']} for {param_name}."
            raise ValueError(msg)
        if not param_options["min"] < param_options["max"]:
            msg = (
                f"Invalid range for {param_name}: "
                f"{param_options['min']} >= {param_options['max']}."
            )
            raise ValueError(msg)

        cube_ranges.append((param_options["min"], param_options["max"]))
        cube_names.append(param_name)

    # Generate the Latin Hypercube samples
    samples = LatinHypercube(cube_ranges).sample(num_samples)

    # Write the parameter files
    for i, sample in tqdm(
        enumerate(samples, start=start_index),
        total=num_samples,
    ):
        this_set = set_values.copy()
        for j, param_name in enumerate(cube_names):
            this_set[param_name] = sample[j]

        this_set["set_label"] = i
        params_path = os.path.join(params_folder, f"params_{i}.txt")
        with open(params_path, "w") as params_file:
            for param_name in parameter_order:
                if param_name in this_set:
                    params_file.write(f"{this_set[param_name]}\n")
                else:
                    msg = f"Parameter {param_name} not found in the set."
                    raise ValueError(msg)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Build parameter files for GDSiMS from a config file."
    )
    parser.add_argument(
        "config_path",
        type=str,
        help="Relative path to the sampling config setting.",
    )
    main(parser.parse_args().config_path)
