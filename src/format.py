import argparse
import sys
from typing import Optional


def print_help() -> None:
    print("Usage: ./manager.sh format -s [source file] -o [output file]")
    print("")
    print("  -s (required)  Source .csv file")
    print("  -o (optional)  Output .csv file (default: 'formatted' prepended to source name)")


def print_parsed_args(source_file: Optional[str], output_file: Optional[str]) -> None:
    print(f"source_file={source_file}")
    print(f"output_file={output_file}")


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
    print_parsed_args(source_file, output_file)


if __name__ == "__main__":
    main()
