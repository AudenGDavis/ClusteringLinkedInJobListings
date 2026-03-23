import argparse
import os
import re
import sys
from typing import Optional

import spacy
import wordninja


def print_help() -> None:
    print("Usage: ./manager.sh trimwordset -s [source file] -o [output file] -l -w")
    print("")
    print("  -s (required)  Source .txt word set file")
    print("  -o (optional)  Output .txt file (default: 'trimmed' prepended to source name)")
    print("  -l (optional)  Trim using lemmatization")
    print("  -w (optional)  Trim using stopword removal")


def build_output_path(source_file: str) -> str:
    base, ext = os.path.splitext(os.path.basename(source_file))
    dir_ = os.path.dirname(source_file)
    return os.path.join(dir_, f"trimmed{base}{ext}")


def load_nlp() -> spacy.language.Language:
    try:
        return spacy.load("en_core_web_sm", disable=["parser", "ner", "textcat"])
    except OSError:
        print("Error: spaCy model 'en_core_web_sm' is not installed.")
        print("Install it with: python3 -m spacy download en_core_web_sm")
        sys.exit(1)


def clean_word(word: str) -> Optional[str]:
    word = word.strip().lower()
    if not word:
        return None
    if any(ch.isdigit() for ch in word):
        return None

    # Keep letters, apostrophes, and hyphens only
    word = re.sub(r"[^a-z'-]", "", word).strip("'-")

    # Remove single-letter entries
    if len(word) <= 1:
        return None
    return word


def split_compound_word(word: str) -> set[str]:
    # Short tokens are usually not compounds and are safer to keep as-is.
    if len(word) < 8:
        return {word}

    pieces = [piece.lower() for piece in wordninja.split(word)]
    if len(pieces) <= 1:
        return {word}

    cleaned_pieces: list[str] = []
    for piece in pieces:
        cleaned_piece = clean_word(piece)
        if cleaned_piece:
            cleaned_pieces.append(cleaned_piece)

    # If splitting does not produce meaningful parts, keep the original token.
    if len(cleaned_pieces) <= 1:
        return {word}

    return set(cleaned_pieces)


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

    with open(source_file, "r", encoding="utf-8") as f:
        words = [line.strip() for line in f if line.strip()]

    trimmed: set[str] = set()

    if use_lemmatization or use_stopword_removal:
        nlp = load_nlp()

        # Process each original entry separately so lemmatization is reliable.
        for doc in nlp.pipe(words, batch_size=1000):
            for token in doc:
                if token.is_space or token.is_punct:
                    continue
                if use_stopword_removal and token.is_stop:
                    continue

                raw = token.lemma_ if use_lemmatization else token.text
                normalized = clean_word(raw)
                if normalized:
                    for candidate in split_compound_word(normalized):
                        if use_stopword_removal and candidate in nlp.Defaults.stop_words:
                            continue
                        trimmed.add(candidate)
    else:
        for word in words:
            normalized = clean_word(word)
            if normalized:
                for candidate in split_compound_word(normalized):
                    trimmed.add(candidate)

    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(sorted(trimmed)))
        f.write("\n")

    print(f"Trimmed word set with {len(trimmed)} words saved to '{output_file}'")


def main() -> None:
    if len(sys.argv) > 1 and sys.argv[1] == "--help":
        print_help()
        return

    parser = argparse.ArgumentParser()
    parser.add_argument("-s", dest="source", required=True)
    parser.add_argument("-o", dest="output", default=None)
    parser.add_argument("-l", dest="lemmatize", action="store_true")
    parser.add_argument("-w", dest="remove_stopwords", action="store_true")
    args = parser.parse_args()

    source_file = args.source
    output_file = args.output or build_output_path(source_file)

    trim_wordset(
        source_file,
        output_file,
        use_lemmatization=args.lemmatize,
        use_stopword_removal=args.remove_stopwords,
    )


if __name__ == "__main__":
    main()