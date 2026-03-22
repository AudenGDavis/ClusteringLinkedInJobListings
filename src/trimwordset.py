import argparse
import sys
import os
from typing import Optional

import spacy


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


def build_output_path(source_file: str) -> str:
    base, ext = os.path.splitext(os.path.basename(source_file))
    dir_ = os.path.dirname(source_file)
    return os.path.join(dir_, f"trimmed{base}{ext}")


def trim_wordset(
    source_file: str,
    output_file: str,
    use_lemmatization: bool,
    use_stopword_removal: bool,
) -> None:
    if not os.path.isfile(source_file):
        print(f"Error: Source file '{source_file}' not found.")
        sys.exit(1)

    if not source_file.endswith(".txt"):
        print("Error: Source file must be a .txt file.")
        sys.exit(1)

    if not output_file.endswith(".txt"):
        print("Error: Output file must be a .txt file.")
        sys.exit(1)

    with open(source_file, "r") as f:
        words = [line.strip() for line in f if line.strip()]

    if use_lemmatization or use_stopword_removal:
        nlp = spacy.load("en_core_web_sm")
        doc = nlp(" ".join(words))

        trimmed = set()
        for token in doc:
            if use_stopword_removal and token.is_stop:
                continue
            word = token.lemma_ if use_lemmatization else token.text
            trimmed.add(word.lower())
    else:
        trimmed = set(words)

    with open(output_file, "w") as f:
        f.write("\n".join(sorted(trimmed)))

    print(f"Trimmed word set with {len(trimmed)} words saved to '{output_file}'")


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

    if not source_file:
        print("Error: -s (source file) is required.")
        print_help()
        sys.exit(1)

    out = output_file if output_file else build_output_path(source_file)

    trim_wordset(
        source_file,
        out,
        use_lemmatization=bool(use_lemmatization),
        use_stopword_removal=bool(use_stopword_removal),
    )


if __name__ == "__main__":
    main()
