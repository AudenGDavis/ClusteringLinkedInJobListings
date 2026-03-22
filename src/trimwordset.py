import argparse
import sys
from typing import Optional


def print_help() -> None:
    print("Usage: ./manager.sh trimwordset -s [source file] -o [output file] -l -w")
    print("")
    print("  -s (required)  Source .txt word set file")
    print("  -o (optional)  Output .txt file (default: 'trimmed' prepended to source name)")
    print("  -l (optional)  Trim using lemmatization")
    print("  -w (optional)  Trim using stopword removal")


def print_parsed_args(
    source_file: Optional[str],
    output_file: Optional[str],
    use_lemmatization: Optional[bool],
    use_stopword_removal: Optional[bool],
) -> None:
    print(f"source_file={source_file}")
    print(f"output_file={output_file}")
    print(f"use_lemmatization={use_lemmatization}")
    print(f"use_stopword_removal={use_stopword_removal}")


def main() -> None:
    if len(sys.argv) > 1 and sys.argv[1] == "--help":
        print_help()
        return

    parser = argparse.ArgumentParser()
    parser.add_argument("-s", dest="source")
    parser.add_argument("-o", dest="output", default=None)
    parser.add_argument("-l", dest="lemmatize", action="store_const", const=True, default=None)
    parser.add_argument("-w", dest="remove_stopwords", action="store_const", const=True, default=None)
    args = parser.parse_args()

    source_file = args.source
    output_file = args.output
    use_lemmatization = args.lemmatize
    use_stopword_removal = args.remove_stopwords
    print_parsed_args(source_file, output_file, use_lemmatization, use_stopword_removal)


if __name__ == "__main__":
    main()
