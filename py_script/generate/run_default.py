import os

from mozzie.generate import run_default


def main():
    main_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))

    script_path = os.path.join(main_dir, "GeneralMetapop/build/gdsimsapp")
    working_dir = os.path.join(main_dir, "data/generated/example")

    output = run_default(script_path, working_dir)

    print("Output from GDSiMS script:")
    print(output)


if __name__ == "__main__":
    main()
