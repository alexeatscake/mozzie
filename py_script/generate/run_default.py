from pathlib import Path

from mozzie.generate import run_default


def main():
    main_dir = Path(__file__).resolve().parent.parent.parent

    script_path = main_dir / "GeneralMetapop/build/gdsimsapp"
    working_dir = main_dir / "data/generated/example"

    output = run_default(script_path, working_dir)

    print("Output from GDSiMS script:")
    print(output)


if __name__ == "__main__":
    main()
