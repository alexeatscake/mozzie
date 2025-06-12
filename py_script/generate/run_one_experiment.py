import argparse
import os

from mozzie.generate import run_custom


def main(params_path: str):
    main_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))

    script_path = os.path.join(main_dir, "GeneralMetapop/build/gdsimsapp")
    working_dir = os.path.join(main_dir, "data/generated/example")
    params_path = os.path.join(main_dir, params_path)
    if not os.path.exists(script_path):
        msg = f"GDSiMS params not found at {params_path}"
        raise FileNotFoundError(msg)

    output = run_custom(
        script_path=script_path,
        working_dir=working_dir,
        params_path=params_path,
    )

    print("Output from GDSiMS script:")
    print(output)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run GDSiMS with default parameters.")
    parser.add_argument(
        "params_path",
        type=str,
        help="Relative path to the GDSiMS script.",
    )
    main(parser.parse_args().params_path)
