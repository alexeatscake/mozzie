"""
Generate: This module contains functions to run the GDSiMS to generate example
data for training and testing the surrogate models.
"""

from __future__ import annotations

import subprocess
import time
from pathlib import Path

__all__ = [
    "parameter_order",
    "run_custom",
    "run_default",
]

parameter_order = [
    "num_runs",
    "max_t",
    "num_pat",
    "mu_j",
    "mu_a",
    "beta",
    "theta",
    "comp_power",
    "min_dev",
    "gamma",
    "xi",
    "e",
    "driver_start",
    "num_driver_M",
    "num_driver_sites",
    "disp_rate",
    "max_disp",
    "psi",
    "mu_aes",
    "t_hide1",
    "t_hide2",
    "t_wake1",
    "t_wake2",
    "alpha0_mean",
    "alpha0_variance",
    "alpha1",
    "amp",
    "resp",
    "rec_start",
    "rec_end",
    "rec_interval_global",
    "rec_interval_local",
    "rec_sites_freq",
    "set_label",
]


def run_default(script_path: str | Path, working_dir: str | Path) -> str:
    """
    Run the GDSiMS script with default parameters.

    Args:
        script_path (str): Path to the GDSiMS script.
        working_dir (str): Directory where the script should be run.

    Returns:
        str: Output from the GDSiMS script.
    """
    print(f"Running script: {script_path}")

    process = subprocess.Popen(
        [str(script_path)],
        cwd=str(working_dir),
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    if process.stdin is None:
        msg = "Failed to open stdin for the process."
        raise RuntimeError(msg)

    time.sleep(0.5)
    process.stdin.write(b"1\n")
    process.stdin.flush()
    print("Selecting default parameters")

    time.sleep(0.5)
    process.stdin.write(b"y\n")
    process.stdin.flush()
    print("Starting Process")

    stdout, _ = process.communicate()
    return stdout.decode()


def run_custom(
    script_path: str | Path, working_dir: str | Path, params_path: str | Path
) -> str:
    """
    Run the GDSiMS script with custom parameters.

    Args:
        script_path (str): Path to the GDSiMS script.
        working_dir (str): Directory where the script should be run.
        params_path (str): Path to the file containing custom parameters.

    Returns:
        str: Output from the GDSiMS script.
    """
    if not Path(working_dir).is_dir():
        msg = f"Working directory {working_dir} does not exist."
        raise FileNotFoundError(msg)
    if not Path(params_path).is_file():
        msg = f"Parameters file {params_path} does not exist."
        raise FileNotFoundError(msg)

    process = subprocess.Popen(
        [str(script_path)],
        cwd=str(working_dir),
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    if process.stdin is None:
        msg = "Failed to open stdin for the process."
        raise RuntimeError(msg)

    time.sleep(0.1)
    process.stdin.write(b"100\n")
    process.stdin.flush()

    time.sleep(0.1)
    process.stdin.write(f"{params_path}\n".encode())
    process.stdin.flush()

    time.sleep(0.1)
    process.stdin.write(b"y\n")
    process.stdin.flush()

    stdout, _ = process.communicate()
    return stdout.decode()


def run_with_coords(
    script_path: str | Path,
    working_dir: str | Path,
    params_path: str | Path,
    coords_path: str | Path,
) -> str:
    """
    Run the GDSiMS script with custom parameters.

    Args:
        script_path (str): Path to the GDSiMS script.
        working_dir (str): Directory where the script should be run.
        params_path (str): Path to the file containing custom parameters.
        coords_path (str): Path to the file containing coordinates.

    Returns:
        str: Output from the GDSiMS script.
    """

    if not Path(working_dir).is_dir():
        msg = f"Working directory {working_dir} does not exist."
        raise FileNotFoundError(msg)
    if not Path(params_path).is_file():
        msg = f"Parameters file {params_path} does not exist."
        raise FileNotFoundError(msg)
    if not Path(coords_path).is_file():
        msg = f"Coordinates file {coords_path} does not exist."
        raise FileNotFoundError(msg)

    process = subprocess.Popen(
        [str(script_path)],
        cwd=str(working_dir),
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    if process.stdin is None:
        msg = "Failed to open stdin for the process."
        raise RuntimeError(msg)

    time.sleep(0.01)
    process.stdin.write(b"100\n")
    process.stdin.flush()

    time.sleep(0.01)
    process.stdin.write(f"{params_path}\n".encode())
    process.stdin.flush()

    time.sleep(0.1)
    process.stdin.write(b"y\n")  # Confirm to use custom parameters
    process.stdin.flush()

    time.sleep(0.01)
    process.stdin.write(b"y\n")  # Want advanced options
    process.stdin.flush()

    time.sleep(0.01)
    process.stdin.write(b"4\n")  # Select coordinates file
    process.stdin.flush()

    time.sleep(0.01)
    process.stdin.write(f"{coords_path}\n".encode())
    process.stdin.flush()

    time.sleep(0.01)
    process.stdin.write(b"0\n")  # No additional options
    process.stdin.flush()

    stdout, _ = process.communicate()
    return stdout.decode()
