from __future__ import annotations

import argparse
import os

import pandas as pd

from mozzie.data_prep import (
    contruct_total_x_and_y,
    load_samples_values,
    load_test_train,
    load_total_values,
)


def main(config_path: str):
    train_config, test_config = load_test_train(config_path)

    sample_values_train = load_samples_values(
        os.path.dirname(config_path), train_config
    )
    total_data_train = load_total_values(os.path.dirname(config_path), train_config)
    X_train, y_train = contruct_total_x_and_y(total_data_train, sample_values_train)

    print("X train shape:", X_train.shape)
    print("y train shape:", y_train.shape)

    sample_values_test = load_samples_values(os.path.dirname(config_path), test_config)
    total_data_test = load_total_values(os.path.dirname(config_path), test_config)
    X_test, y_test = contruct_total_x_and_y(total_data_test, sample_values_test)
    print("X test shape:", X_test.shape)
    print("y test shape:", y_test.shape)

    processed_data_dir = os.path.join(os.path.dirname(config_path), "processed_total")
    os.makedirs(processed_data_dir, exist_ok=True)
    pd.DataFrame(X_train).to_csv(
        os.path.join(processed_data_dir, "X_train.csv"), index=False
    )
    pd.DataFrame(y_train).to_csv(
        os.path.join(processed_data_dir, "y_train.csv"), index=False
    )
    pd.DataFrame(X_test).to_csv(
        os.path.join(processed_data_dir, "X_test.csv"), index=False
    )
    pd.DataFrame(y_test).to_csv(
        os.path.join(processed_data_dir, "y_test.csv"), index=False
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Load data form GDSiMS experiments.")
    parser.add_argument(
        "config_path",
        type=str,
        help="Relative path to the GDSiMS config file.",
    )
    args = parser.parse_args()
    main_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
    config_path = os.path.join(main_dir, args.config_path)

    main(args.config_path)
