import argparse
import sys
from typing import Optional


def print_help() -> None:
    print("Usage: ./manager.sh vectorize -d [dataset file] -w [word set file] -o [output file]")
    print("")
    print("  -d (required)  Dataset .csv file")
    print("  -w (required)  Word set .txt file")
    print("  -o (optional)  Output .csv file (default: 'vectorized' prepended to dataset name)")


def print_parsed_args(
    dataset_file: Optional[str],
    wordset_file: Optional[str],
    output_file: Optional[str],
) -> None:
    print(f"dataset_file={dataset_file}")
    print(f"wordset_file={wordset_file}")
    print(f"output_file={output_file}")


def main() -> None:
    if len(sys.argv) > 1 and sys.argv[1] == "--help":
        print_help()
        return

    parser = argparse.ArgumentParser()
    parser.add_argument("-d", dest="dataset")
    parser.add_argument("-w", dest="wordset")
    parser.add_argument("-o", dest="output", default=None)
    args = parser.parse_args()

    dataset_file = args.dataset
    wordset_file = args.wordset
    output_file = args.output
    print_parsed_args(dataset_file, wordset_file, output_file)


if __name__ == "__main__":
    main()
