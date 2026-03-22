import argparse
import sys
from typing import Any


def print_help() -> None:
    print("Usage: ./manager.sh cluster -d [dataset file] -o [output file] -k [max clusters]")
    print("")
    print("  -d (required)  Vectorized dataset .csv file")
    print("  -o (optional)  Output .csv file (default: 'clustered' prepended to dataset name)")
    print("  -k (optional)  Maximum number of clusters to try (default: 10)")


def print_parsed_args(
    dataset_file: Any,
    output_file: Any,
    max_clusters: Any,
) -> None:
    print(f"dataset_file={dataset_file}")
    print(f"output_file={output_file}")
    print(f"max_clusters={max_clusters}")


def main() -> None:
    if len(sys.argv) > 1 and sys.argv[1] == "--help":
        print_help()
        return

    parser = argparse.ArgumentParser()
    parser.add_argument("-d", dest="dataset")
    parser.add_argument("-o", dest="output", default=None)
    parser.add_argument("-k", dest="max_clusters", default=None)
    args = parser.parse_args()

    dataset_file = args.dataset
    output_file = args.output
    max_clusters = args.max_clusters
    print_parsed_args(dataset_file, output_file, max_clusters)


if __name__ == "__main__":
    main()
