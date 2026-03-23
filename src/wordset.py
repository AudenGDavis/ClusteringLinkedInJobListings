import argparse
import re
import sys
import os
import re
import pandas as pd
from typing import Optional

import pandas as pd


def print_help() -> None:
    print("Usage: ./manager.sh wordset -s [source file] -o [output file]")
    print("")
    print("  -s (required)  Source .csv file")
    print("  -o (required)  Output .txt file")


def print_parsed_args(source_file: Optional[str], output_file: Optional[str]) -> None:
    print(f"source_file={source_file}")
    print(f"output_file={output_file}")


<<<<<<< Updated upstream
def derive_wordset(source_file: str, output_file: str) -> None:
    if not os.path.isfile(source_file):
        print(f"Error: Source file '{source_file}' not found.")
        sys.exit(1)

    if not source_file.endswith(".csv"):
        print("Error: Source file must be a .csv file.")
        sys.exit(1)

    if not output_file.endswith(".txt"):
        print("Error: Output file must be a .txt file.")
        sys.exit(1)

    df = pd.read_csv(source_file)

    if "description" not in df.columns:
        print("Error: Source file must contain a 'description' column.")
        sys.exit(1)

    wordset = set()
    for desc in df["description"].dropna():
        words = re.findall(r"[a-zA-Z]+", desc.lower())
        wordset.update(w for w in words if 3 <= len(w) <= 20)

    with open(output_file, "w") as f:
        f.write("\n".join(sorted(wordset)))

    print(f"Word set with {len(wordset)} words saved to '{output_file}'")
=======
def read_weird_csv(source_file: str) -> pd.DataFrame:
    read_options = {
        "sep": ",",
        "engine": "python",
        "dtype": str,
        "na_filter": False,
        "keep_default_na": False,
        "quotechar": '"',
        "doublequote": True,
    }

    try:
        return pd.read_csv(source_file, encoding="utf-8", **read_options)
    except UnicodeDecodeError:
        return pd.read_csv(source_file, encoding="latin-1", **read_options)


def build_word_set(df: pd.DataFrame) -> list[str]:
    if "description" not in df.columns:
        raise ValueError("Input CSV must contain a 'description' column")

    words: set[str] = set()

    for description in df["description"]:
        for word in re.findall(r"[A-Za-z0-9']+", str(description).lower()):
            words.add(word)

    return sorted(words)
>>>>>>> Stashed changes


def main() -> None:
    if len(sys.argv) > 1 and sys.argv[1] == "--help":
        print_help()
        return

    parser = argparse.ArgumentParser()
    parser.add_argument("-s", dest="source", required=True)
    parser.add_argument("-o", dest="output", required=True)
    args = parser.parse_args()

    source_file = args.source
    output_file = args.output

    if not source_file:
        print("Error: -s (source file) is required.")
        print_help()
        sys.exit(1)

    if not output_file:
        print("Error: -o (output file) is required.")
        print_help()
        sys.exit(1)

    derive_wordset(source_file, output_file)

    df = read_weird_csv(source_file)
    words = build_word_set(df)

    with open(output_file, "w", encoding="utf-8") as output_handle:
        output_handle.write("\n".join(words))
        output_handle.write("\n")

    print(f"Wrote {len(words)} unique words to {output_file}")


if __name__ == "__main__":
    main()
