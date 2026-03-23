import argparse
import os
import sys
from typing import Optional

import pandas as pd


def print_help() -> None:
    print("Usage: ./manager.sh format -s [source file] -o [output file]")
    print("")
    print("  -s (required)  Source .csv file")
    print("  -o (optional)  Output .csv file (default: 'formatted' prepended to source name)")


def print_parsed_args(source_file: Optional[str], output_file: Optional[str]) -> None:
    print(f"source_file={source_file}")
    print(f"output_file={output_file}")


def default_output_path(source_file: str) -> str:
    directory = os.path.dirname(source_file)
    filename = os.path.basename(source_file)
    return os.path.join(directory, f"formatted{filename}")


def read_weird_csv(source_file: str) -> pd.DataFrame:
    read_options = {
        "sep": ",",
        "engine": "python",
        "dtype": str,
        "na_filter": False,
        "keep_default_na": False,
        "quotechar": '"',
        "doublequote": True,
        "on_bad_lines": "skip",
    }

    try:
        return pd.read_csv(source_file, encoding="utf-8", **read_options)
    except UnicodeDecodeError:
        return pd.read_csv(source_file, encoding="latin-1", **read_options)


def add_job_id_column(df: pd.DataFrame) -> pd.DataFrame:
    formatted_df = df.copy()
    job_ids = range(1, len(formatted_df) + 1)

    if "job_id" in formatted_df.columns:
        formatted_df["job_id"] = job_ids
    else:
        formatted_df.insert(0, "job_id", job_ids)

    return formatted_df


def main() -> None:
    if len(sys.argv) > 1 and sys.argv[1] == "--help":
        print_help()
        return

    parser = argparse.ArgumentParser()
    parser.add_argument("-s", dest="source", required=True)
    parser.add_argument("-o", dest="output", default=None)
    args = parser.parse_args()

    source_file = args.source
    output_file = args.output or default_output_path(source_file)
    print_parsed_args(source_file, output_file)

    df = read_weird_csv(source_file)
    formatted_df = add_job_id_column(df)
    formatted_df.to_csv(output_file, index=False)
    print(f"Wrote {len(formatted_df)} rows to {output_file}")

if __name__ == "__main__":
    main()
