import numpy as np
from scipy.stats import qmc


def generate_parameter_samples(
    to_sample: dict,
    num_samples: int,
    seed: int | None = None,
) -> np.ndarray:
    """
    Generate Latin Hypercube samples for the given parameters.

    Args:
        to_sample (dict): Dictionary of parameters to sample with their options
        num_samples (int): Number of samples to generate

    Returns:
        samples (ndarray): Array of samples with shape (num_samples, num_parameters)
    """
    # Pull out the parameters to sample
    cube_ranges = []
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

    # Generate the Latin Hypercube samples
    lhc_sampler = qmc.LatinHypercube(d=len(cube_ranges), seed=seed)
    return qmc.scale(
        lhc_sampler.random(num_samples),
        [r[0] for r in cube_ranges],
        [r[1] for r in cube_ranges],
    )
