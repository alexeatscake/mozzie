import os
import subprocess
import time


def main():
    main_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

    script_path = os.path.join(main_dir, "GeneralMetapop/build/gdsimsapp")
    print(f"Running script: {script_path}")

    process = subprocess.Popen(
        [script_path],
        cwd=os.path.join(main_dir, "data"),
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    time.sleep(0.5)
    process.stdin.write(b"1\n")
    process.stdin.flush()
    print("1")
    time.sleep(0.5)
    process.stdin.write(b"y\n")
    process.stdin.flush()
    print("y")

    stdout, _ = process.communicate()
    print("Process finished.")
    print(stdout.decode())


if __name__ == "__main__":
    main()
