import argparse
import sys
import os
import pandas as pd
from typing import Optional


def print_help() -> None:
    print("Usage: ./manager.sh format -s [source file] -o [output file]")
    print("")
    print("  -s (required)  Source .csv file")
    print("  -o (optional)  Output .csv file (default: 'formatted' prepended to source name)")


def build_output_path(source_file: str) -> str:
    base, ext = os.path.splitext(os.path.basename(source_file))
    dir_ = os.path.dirname(source_file)
    return os.path.join(dir_, f"formatted{base}{ext}")


def format_dataset(source_file: str, output_file: Optional[str]) -> None:
    if not os.path.isfile(source_file):
        print(f"Error: Source file '{source_file}' not found.")
        sys.exit(1)

    if not source_file.endswith(".csv"):
        print("Error: Source file must be a .csv file.")
        sys.exit(1)

    out = output_file if output_file else build_output_path(source_file)

    if not out.endswith(".csv"):
        print("Error: Output file must be a .csv file.")
        sys.exit(1)

    df = pd.read_csv(source_file)
    df.insert(0, "Job ID", range(1, len(df) + 1))
    df.to_csv(out, index=False)
    print(f"Formatted dataset saved to '{out}'")


def main() -> None:
    if len(sys.argv) > 1 and sys.argv[1] == "--help":
        print_help()
        return

    parser = argparse.ArgumentParser()
    parser.add_argument("-s", dest="source")
    parser.add_argument("-o", dest="output", default=None)
    args = parser.parse_args()

    source_file = args.source
    output_file = args.output

    if not source_file:
        print("Error: -s (source file) is required.")
        print_help()
        sys.exit(1)

    format_dataset(source_file, output_file)


if __name__ == "__main__":
    main()