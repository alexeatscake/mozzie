from __future__ import annotations

import os

import numpy as np
import pandas as pd
import yaml

from mozzie.generate import parameter_order


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


def load_test_train(config_path: str, train_fraction: float = 0.8) -> tuple[dict, dict]:
    """
    Load the configuration file and split the data into training and testing sets.

    Args:
        config_path (str): Path to the configuration file.
        train_fraction (float): Fraction of data to use for training.

    Returns:
        train_set (dict): Training set configuration.
        test_set (dict): Testing set configuration.
    """
    with open(config_path) as file:
        config = yaml.safe_load(file)

    set_values, to_sample, num_samples, start_index, analysis_range = read_config(
        config
    )

    num_train_samples = int(num_samples * train_fraction)
    num_test_samples = num_samples - num_train_samples

    train_set = {
        "set_values": set_values,
        "to_sample": to_sample,
        "num_samples": num_train_samples,
        "start_index": start_index,
        "analysis_range": analysis_range,
    }

    test_set = {
        "set_values": set_values,
        "to_sample": to_sample,
        "num_samples": num_test_samples,
        "start_index": start_index + num_train_samples,
        "analysis_range": analysis_range,
    }

    return train_set, test_set


def read_values_from_params(
    params_path: str, to_sample: dict | list
) -> dict[str, float]:
    """
    Reads parameter values from a file and maps them to specified sample names.

    Args:
        params_path (str): The path to the file containing parameter values.
        to_sample (dict, list): A dictionary where keys are sample names or a list of
            sample names to extract values for.

    Returns:
        dict[str, float]: A dictionary mapping sample names to their corresponding
            parameter values.

    Raises:
        ValueError: If a sample name in `to_sample` is not found in `parameter_order`.
    """

    with open(params_path) as file:
        lines = file.readlines()

    sample_values = {}

    for sample_name in to_sample:
        if sample_name not in parameter_order:
            msg = f"Sample name '{sample_name}' not found in parameter order."
            raise ValueError(msg)

        s_idx = parameter_order.index(sample_name)
        sample_values[sample_name] = float(lines[s_idx].strip())

    return sample_values


def load_samples_values(
    data_path: str, config_dict: dict
) -> dict[int, dict[str, float]]:
    """
    This loads the sample values from the parameters files.
    It reads the parameters from the files and returns a dictionary
    where the keys are the sample indices and the values are dictionaries
    containing the parameter values for each sample.

    Args:
        data_path (str): The path to the directory containing the parameters files.
        config_dict (dict): The configuration dictionary which needs to contain:
            - "start_index": The starting index for the samples.
            - "num_samples": The number of samples to load.
            - "to_sample": A dictionary of parameters to sample.

    Returns:
        dict[int, dict[str, float]]: A dictionary where keys are sample indices and
            values are dictionaries of parameter values for each sample.
    """
    start_index = config_dict["start_index"]
    end_index = start_index + config_dict["num_samples"]

    to_sample = config_dict["to_sample"].keys()

    params_dir = os.path.join(data_path, "params")
    if not os.path.exists(params_dir):
        msg = f"Parameters directory {params_dir} does not exist."
        raise FileNotFoundError(msg)

    all_sample_values = {}

    for val in range(start_index, end_index):
        params_path = os.path.join(params_dir, f"params_{val}.txt")
        if not os.path.exists(params_path):
            msg = f"Parameters file {params_path} does not exist."
            raise FileNotFoundError(msg)

        all_sample_values[val] = read_values_from_params(params_path, to_sample)

    return all_sample_values


def load_local_values(
    data_path: str, config_dict: dict
) -> dict[int, dict[int, np.ndarray]]:
    """
    This loads the stepwise local data from the output files.

    Args:
        data_path (str): The path to the directory containing the output files.
        config_dict (dict): The configuration dictionary which needs to contain:
            - "start_index": The starting index for the samples.
            - "num_samples": The number of samples to load.
            - "analysis_range": A dictionary with keys "start", "end", and "step".

    Returns:
        dict[int, dict[int, np.ndarray]]: A dictionary where keys are sample indices
            and values are dictionaries mapping time points to local data arrays.
    """
    output_files_dir = os.path.join(data_path, "output_files")
    if not os.path.exists(output_files_dir):
        msg = f"Output files directory {output_files_dir} does not exist."
        raise FileNotFoundError(msg)

    start_index = config_dict["start_index"]
    end_index = start_index + config_dict["num_samples"]

    local_time_points = np.arange(
        config_dict["analysis_range"]["start"],
        config_dict["analysis_range"]["end"],
        config_dict["analysis_range"]["step"],
    )

    local_data: dict[int, dict[int, np.ndarray]] = {}

    for val in range(start_index, end_index):
        local_df = pd.read_csv(
            os.path.join(data_path, "output_files", f"LocalData{val}run1.txt"),
            sep="\t",
            header=1,
        )
        local_data[val] = {}

        for time_point in local_time_points:
            if time_point not in local_df["Day"].values:
                msg = f"Time point {time_point} not found in LocalData{val}run1.txt."
                raise ValueError(msg)

            local_data[val][time_point] = local_df[local_df["Day"] == time_point][
                ["WW", "WD", "DD", "WR", "RR", "DR"]
            ].values

    return local_data


def contruct_local_x_and_y(
    local_data: dict[int, dict[int, np.ndarray]],
    sample_values: dict[int, dict[str, float]],
) -> tuple[np.ndarray, np.ndarray]:
    """
    Constructs the feature matrix X and target vector y from local data and
    sample values.
    This function iterates over the local data, concatenates the local data
    arrays with the corresponding sample values, and prepares the target vector
    for the next time point.

    Args:
        local_data (dict[int, dict[int, np.ndarray]]): Local data where keys are
            sample indices and values are dictionaries mapping time points to local
            data arrays.
        sample_values (dict[int, dict[str, float]]): Sample values where keys are
            sample indices and values are dictionaries of parameter values for
            each sample.

    Returns:
        tuple[np.ndarray, np.ndarray]: A tuple containing the feature matrix X and
            the target vector y. X is a 2D array where each row corresponds to a
            sample's local data concatenated with its sample values, and y is a 2D
            array where each row corresponds to the local data at the next time point.
    """
    X = []
    y = []

    for sample_idx, local_values in local_data.items():
        time_points = sorted(local_values.keys())

        these_sample_values = np.array(list(sample_values[sample_idx].values()))

        for tidx in range(len(time_points) - 1):
            time_point = time_points[tidx]
            next_time_point = time_points[tidx + 1]
            X.append(np.append(local_values[time_point].flatten(), these_sample_values))
            y.append(local_values[next_time_point].flatten())

    return np.array(X), np.array(y)


def load_total_values(data_path: str, config_dict: dict) -> dict[int, np.ndarray]:
    """
    This loads the total values from the output files.

    Args:
        data_path (str): The path to the directory containing the output files.
        config_dict (dict): The configuration dictionary which needs to contain:
            - "start_index": The starting index for the samples.
            - "num_samples": The number of samples to load.

    Returns:
        dict[int, np.ndarray]: A dictionary where keys are sample indices and values
            are numpy arrays containing the total values for each sample.
    """
    output_files_dir = os.path.join(data_path, "output_files")
    if not os.path.exists(output_files_dir):
        msg = f"Output files directory {output_files_dir} does not exist."
        raise FileNotFoundError(msg)

    start_index = config_dict["start_index"]
    end_index = start_index + config_dict["num_samples"]

    total_data: dict[int, np.ndarray] = {}

    for val in range(start_index, end_index):
        local_df = pd.read_csv(
            os.path.join(data_path, "output_files", f"Totals{val}run1.txt"),
            sep="\t",
            header=1,
        )
        total_data[val] = local_df[["WW", "WD", "DD", "WR", "RR", "DR"]].values

    return total_data


def contruct_total_x_and_y(
    total_data: dict[int, np.ndarray],
    sample_values: dict[int, dict[str, float]],
) -> tuple[np.ndarray, np.ndarray]:
    """
    Constructs the feature matrix X and target vector y from total data and
    sample values.

    Args:
        total_data (dict[int, np.ndarray]): Total data where keys are sample indices
            and values are numpy arrays containing the total values for each sample.
        sample_values (dict[int, dict[str, float]]): Sample values where keys are
            sample indices and values are dictionaries of parameter values for each
            sample.

    Returns:
        tuple[np.ndarray, np.ndarray]: A tuple containing the feature matrix X and
            the target vector y. X is a 2D array where each row corresponds to a
            sample's total values concatenated with its sample values, and y is a 2D
            array where each row corresponds to the total values for the sample.
    """
    X = []
    y = []

    for sample_idx, total_values in total_data.items():
        X.append(np.array(list(sample_values[sample_idx].values())))
        y.append(total_values.flatten())

    return np.array(X), np.array(y)


def cast_back_data(flattened_data: np.ndarray) -> pd.DataFrame:
    """
    Casts back the flattened data to a DataFrame with the original column names.

    Args:
        flattened_data (np.ndarray): The flattened data to be cast back.

    Returns:
        pd.DataFrame: A DataFrame with the original column names.
    """
    columns = ["WW", "WD", "DD", "WR", "RR", "DR"]
    return pd.DataFrame(flattened_data.reshape(-1, len(columns)), columns=columns)
