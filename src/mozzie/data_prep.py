from __future__ import annotations


def read_config(config_dict: dict):
    """
    Reads and validates the configuration dictionary for sampling parameters.

    Args:
        config_dict (dict): The configuration dictionary.

    Returns:
        set_values (dict): The 'set_values' section of the configuration dictionary.
        to_sample (dict): The 'to_sample' section of the configuration dictionary.
        num_samples (int): The number of samples to generate.
        start_index (int): The starting index for sampling.
        analysis_range (dict): The range for analysis,
            including 'min', 'max', and 'step'.
    """
    # Set values
    set_values = config_dict.get("set_values")
    if set_values is None:
        msg = "No set values found in the config file."
        raise ValueError(msg)
    if not isinstance(set_values, dict):
        msg = "The 'set_values' field must be a dictionary."
        raise ValueError(msg)

    # To Sample
    to_sample = config_dict.get("to_sample")
    if to_sample is None:
        msg = "No parameters to sample found in the config file."
        raise ValueError(msg)

    if not isinstance(to_sample, dict):
        msg = "The 'to_sample' field must be a dictionary of parameters."
        raise ValueError(msg)
    for param_options in to_sample.values():
        if not isinstance(param_options, dict):
            msg = "Each parameter option must be a dictionary."
            raise ValueError(msg)
        if "type" not in param_options:
            msg = "Each parameter option must specify a 'type'."
            raise ValueError(msg)
        if "min" not in param_options or "max" not in param_options:
            msg = "Each parameter option must specify 'min' and 'max' values."
            raise ValueError(msg)

    # Number of Samples
    num_samples = config_dict.get("num_samples", 100)
    if not isinstance(num_samples, int) or num_samples <= 0:
        msg = "num_samples must be a positive integer."
        raise ValueError(msg)

    # Start Index
    start_index = config_dict.get("start_index", num_samples)
    if not isinstance(start_index, int) or start_index < 0:
        msg = "start_index must be a non-negative integer."
        raise ValueError(msg)

    # Analysis Range
    analysis_range = config_dict.get("analysis_range")
    if not isinstance(analysis_range, dict):
        msg = "analysis_range must be a dictionary."
        raise ValueError(msg)
    if not isinstance(analysis_range.get("start"), int):
        msg = "analysis_range must have an integer 'start' value and be an integer."
        raise ValueError(msg)
    if not isinstance(analysis_range.get("end"), int):
        msg = "analysis_range must have an integer 'end' value and be an integer."
        raise ValueError(msg)
    if not isinstance(analysis_range.get("step"), int):
        msg = "analysis_range must have an integer 'step' value and be an integer."
        raise ValueError(msg)

    return set_values, to_sample, num_samples, start_index, analysis_range
