"""
Generate: This module contains functionst to run the GDSiMS to generate example
data for training and testing the surrogate models.
"""

from __future__ import annotations

import subprocess
import time


def run_default(script_path: str, working_dir: str) -> str:
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
        [script_path],
        cwd=working_dir,
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


def run_custom(script_path: str, working_dir: str, params_path: str) -> str:
    """
    Run the GDSiMS script with custom parameters.

    Args:
        script_path (str): Path to the GDSiMS script.
        working_dir (str): Directory where the script should be run.
        params_path (str): Path to the file containing custom parameters.

    Returns:
        str: Output from the GDSiMS script.
    """
    print(f"Running script: {script_path}")

    process = subprocess.Popen(
        [script_path],
        cwd=working_dir,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    if process.stdin is None:
        msg = "Failed to open stdin for the process."
        raise RuntimeError(msg)

    time.sleep(0.5)
    process.stdin.write(b"100\n")
    process.stdin.flush()
    print("Selecting custom parameters")

    time.sleep(0.5)
    process.stdin.write(f"{params_path}\n".encode())
    process.stdin.flush()
    print("providing parameters file")

    time.sleep(0.5)
    process.stdin.write(b"y\n")
    process.stdin.flush()
    print("Starting Process")

    stdout, _ = process.communicate()
    return stdout.decode()
