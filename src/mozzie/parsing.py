from pathlib import Path

import numpy as np
import pandas as pd


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


def read_total_data(file_path: str | Path) -> pd.DataFrame:
    """
    Reads total mosquito population data from a text file into a DataFrame.

    Args:
        file_path (str | Path): Path to the text file containing the total data.

    Returns:
        pd.DataFrame: DataFrame containing the total mosquito population data.
            The columns are expected to be ["WW", "WD", "DD", "WR", "RR", "DR"]
            The index represents the time points (days).
    """
    file_path = Path(file_path)
    if not file_path.exists():
        msg = f"File {file_path} does not exist."
        raise FileNotFoundError(msg)

    try:
        df = pd.read_csv(file_path, sep="\t", header=1)
    except Exception as e:
        msg = f"Error reading file {file_path}: {e}"
        raise ValueError(msg) from e

    expected_columns = ["Day", "WW", "WD", "DD", "WR", "RR", "DR"]
    if not all(col in df.columns for col in expected_columns):
        missing_cols = [col for col in expected_columns if col not in df.columns]
        msg = f"Missing expected columns: {missing_cols}"
        raise ValueError(msg)

    df.set_index("Day", inplace=True)
    return df[expected_columns[1:]]  # Return only mozzie type columns


def read_local_data(file_path: str | Path) -> tuple[np.ndarray, np.ndarray]:
    """
    Reads local mosquito population data from a text file and organizes it into
    a 3D numpy array.

    Args:
        file_path (str | Path): Path to the text file containing the local data.

    Returns:
        data_3d (np.ndarray): 3D array with shape [time, location, mozzie_type]
            where mozzie_type corresponds to ["WW", "WD", "DD", "WR", "RR", "DR"]
        timestamps (np.ndarray): 1D array of unique time points
    """
    file_path = Path(file_path)
    if not file_path.exists():
        msg = f"File {file_path} does not exist."
        raise FileNotFoundError(msg)

    # Read the data, skipping the first header line
    try:
        df = pd.read_csv(file_path, sep="\t", header=1)
    except Exception as e:
        msg = f"Error reading file {file_path}: {e}"
        raise ValueError(msg) from e

    # Validate expected columns
    expected_columns = ["Day", "Site", "WW", "WD", "DD", "WR", "RR", "DR"]
    if not all(col in df.columns for col in expected_columns):
        missing_cols = [col for col in expected_columns if col not in df.columns]
        msg = f"Missing expected columns: {missing_cols}"
        raise ValueError(msg)

    # Get unique timestamps and sites
    timestamps = np.sort(df["Day"].unique())
    sites = np.sort(df["Site"].unique())

    # Initialize 3D array: [time, location, mozzie_type]
    data_3d = np.zeros((len(timestamps), len(sites), 6))

    # Fill the 3D array
    mozzie_columns = ["WW", "WD", "DD", "WR", "RR", "DR"]
    for time_idx, timestamp in enumerate(timestamps):
        for site_idx, site in enumerate(sites):
            # Get data for this time and site
            mask = (df["Day"] == timestamp) & (df["Site"] == site)
            site_data = df[mask]

            if len(site_data) == 0:
                msg = f"No data found for Day {timestamp}, Site {site}"
                raise ValueError(msg)
            if len(site_data) > 1:
                msg = f"Multiple entries found for Day {timestamp}, Site {site}"
                raise ValueError(msg)

            # Extract mozzie type data
            data_3d[time_idx, site_idx, :] = site_data[mozzie_columns].values[0]

    return data_3d, timestamps


def aggregate_mosquito_data(
    data: np.ndarray,
    aggregation_type: str,
) -> np.ndarray:
    """
    Aggregates mosquito population data across mosquito types.

    This function can handle both 2D data [site, mozzie_type] and 3D data
    [time, site, mozzie_type], reducing the mozzie_type dimension according
    to the specified aggregation method.

    Args:
        data (np.ndarray): Input data array. Can be either:
            - 2D array with shape [site, mozzie_type]
            - 3D array with shape [time, site, mozzie_type]
            The mozzie_type dimension should correspond to
            ["WW", "WD", "DD", "WR", "RR", "DR"]
        aggregation_type (str): Type of aggregation to perform. Options:
            - "total_drive": Sum of drive genes (WD + DD*2 + DR)
            - "total_wild": Sum of wild alleles (WW*2 + WD + WR)
            - "total_resistant": Sum of resistance alleles (WR + RR*2 + DR)
            - "total_population": Sum of all mosquito types
            - "drive_frequency": Frequency of drive alleles in population
                If total population is zero, frequency is set to 1.
            - "wild_frequency": Frequency of wild alleles in population
                If total population is zero, frequency is set to 0.
            - "resistant_frequency": Frequency of resistant alleles in population
                If total population is zero, frequency is set to 1.

    Returns:
        np.ndarray: Aggregated data array with reduced dimensions:
            - If input is 2D [site, mozzie_type] -> returns 1D [site]
            - If input is 3D [time, site, mozzie_type] -> returns 2D [time, site]
    """
    if data.ndim not in [2, 3]:
        msg = "Data must be 2D [site, mozzie_type] or 3D [time, site, mozzie_type]"
        raise ValueError(msg)

    if data.shape[-1] != 6:
        msg = f"Last dimension must be 6 (mozzie types), got {data.shape[-1]}"
        raise ValueError(msg)

    # Extract mosquito type counts
    # Indices correspond to ["WW", "WD", "DD", "WR", "RR", "DR"]
    ww = data[..., 0]  # Wild-Wild
    wd = data[..., 1]  # Wild-Drive
    dd = data[..., 2]  # Drive-Drive
    wr = data[..., 3]  # Wild-Resistance
    rr = data[..., 4]  # Resistance-Resistance
    dr = data[..., 5]  # Drive-Resistance

    if aggregation_type == "total_drive":
        return wd + (dd * 2) + dr

    if aggregation_type == "total_wild":
        return (ww * 2) + wd + wr

    if aggregation_type == "total_resistant":
        return wr + (rr * 2) + dr

    if aggregation_type == "total_population":
        return ww + wd + dd + wr + rr + dr

    if aggregation_type == "drive_frequency":
        total_alleles = 2 * (ww + wd + dd + wr + rr + dr)
        drive_alleles = wd + (dd * 2) + dr

        return np.divide(
            drive_alleles,
            total_alleles,
            out=np.ones_like(drive_alleles, dtype=float),  # default value = 1
            where=total_alleles > 0,
        )

    if aggregation_type == "wild_frequency":
        # Calculate frequency of wild alleles
        total_alleles = 2 * (ww + wd + dd + wr + rr + dr)
        wild_alleles = (ww * 2) + wd + wr

        return np.divide(
            wild_alleles,
            total_alleles,
            out=np.zeros_like(wild_alleles, dtype=float),  # default value = 0
            where=total_alleles > 0,
        )

    if aggregation_type == "resistant_frequency":
        # Calculate frequency of resistance alleles
        total_alleles = 2 * (ww + wd + dd + wr + rr + dr)
        resistance_alleles = wr + (rr * 2) + dr

        return np.divide(
            resistance_alleles,
            total_alleles,
            out=np.ones_like(resistance_alleles, dtype=float),  # default value = 1
            where=total_alleles > 0,
        )

    available_types = [
        "total_drive",
        "total_wild",
        "total_resistant",
        "total_population",
        "drive_frequency",
        "wild_frequency",
        "resistant_frequency",
    ]
    msg = f"Unknown aggregation_type '{aggregation_type}'. Available: {available_types}"
    raise ValueError(msg)
