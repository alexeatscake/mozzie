from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from mozzie.data_prep import (
    contruct_local_x_and_y,
    load_local_values,
    load_samples_values,
    load_test_train,
)


def main(rel_config_path: str):
    main_dir = Path(__file__).resolve().parent.parent.parent

    config_path = main_dir / rel_config_path
    train_config, test_config = load_test_train(config_path)

    sample_values_train = load_samples_values(config_path.parent, train_config)
    local_data_train = load_local_values(config_path.parent, train_config)
    X_train, y_train = contruct_local_x_and_y(local_data_train, sample_values_train)

    print("X train shape:", X_train.shape)
    print("y train shape:", y_train.shape)

    sample_values_test = load_samples_values(config_path.parent, test_config)
    local_data_test = load_local_values(config_path.parent, test_config)
    X_test, y_test = contruct_local_x_and_y(local_data_test, sample_values_test)
    print("X test shape:", X_test.shape)
    print("y test shape:", y_test.shape)

    processed_data_dir = config_path.parent / "processed_local"
    processed_data_dir.mkdir(exist_ok=True)
    pd.DataFrame(X_train).to_csv(processed_data_dir / "X_train.csv", index=False)
    pd.DataFrame(y_train).to_csv(processed_data_dir / "y_train.csv", index=False)
    pd.DataFrame(X_test).to_csv(processed_data_dir / "X_test.csv", index=False)
    pd.DataFrame(y_test).to_csv(processed_data_dir / "y_test.csv", index=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Load data form GDSiMS experiments.")
    parser.add_argument(
        "config_path",
        type=str,
        help="Relative path to the GDSiMS config file.",
    )
    args = parser.parse_args()
    main(args.config_path)
