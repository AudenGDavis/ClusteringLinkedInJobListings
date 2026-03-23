import argparse
import os
import re
import sys
from collections import Counter
from typing import Dict, Optional, Union

import pandas as pd
import spacy


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


def default_output_path(dataset_file: str) -> str:
    directory = os.path.dirname(dataset_file)
    filename = os.path.basename(dataset_file)
    return os.path.join(directory, f"vectorized{filename}")


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


def read_wordset(wordset_file: str) -> list[str]:
    words: list[str] = []
    seen: set[str] = set()

    with open(wordset_file, "r", encoding="utf-8") as handle:
        for raw_line in handle:
            word = raw_line.strip().lower()
            if not word:
                continue
            if word in seen:
                continue
            seen.add(word)
            words.append(word)

    return words


def load_spacy_pipeline() -> spacy.language.Language:
    try:
        return spacy.load("en_core_web_sm", disable=["ner", "parser", "textcat"])
    except OSError:
        return spacy.blank("en")


def normalize_token(token: spacy.tokens.Token) -> str:
    lemma = token.lemma_.lower().strip()
    if not lemma:
        lemma = token.text.lower().strip()
    return str(lemma)


def tokenize_and_lemmatize(nlp: spacy.language.Language, text: str) -> list[str]:
    doc = nlp(text)
    lemmas: list[str] = []

    for token in doc:
        if token.is_space or token.is_punct:
            continue
        normalized = normalize_token(token)
        if re.search(r"[a-z0-9]", normalized):
            lemmas.append(normalized)

    return lemmas


def find_column_name(df: pd.DataFrame, target: str) -> str:
    normalized_map = {column.strip().lower(): column for column in df.columns}
    if target not in normalized_map:
        raise ValueError(f"Input CSV must contain a '{target}' column")
    return str(normalized_map[target])


def build_vectorized_dataframe(
    df: pd.DataFrame, words: list[str], nlp: spacy.language.Language
) -> pd.DataFrame:
    job_id_column = find_column_name(df, "job id")
    description_column = find_column_name(df, "description")

    # Lemmatize each word-set entry once so vector values are based on lemma frequency.
    word_lemmas: list[str] = []
    for word in words:
        lemmas = tokenize_and_lemmatize(nlp, word)
        word_lemmas.append(lemmas[0] if lemmas else word)

    rows: list[Dict[str, Union[float, str]]] = []

    for _, row in df.iterrows():
        description = str(row[description_column])
        lemmas = tokenize_and_lemmatize(nlp, description)
        total_terms = len(lemmas)
        lemma_counts = Counter(lemmas)

        vector_row: Dict[str, Union[float, str]] = {"job id": str(row[job_id_column])}
        for word, word_lemma in zip(words, word_lemmas):
            if total_terms == 0:
                vector_row[word] = 0.0
            else:
                vector_row[word] = lemma_counts[word_lemma] / total_terms

        rows.append(vector_row)

    return pd.DataFrame(rows)


def main() -> None:
    if len(sys.argv) > 1 and sys.argv[1] == "--help":
        print_help()
        return

    parser = argparse.ArgumentParser()
    parser.add_argument("-d", dest="dataset", required=True)
    parser.add_argument("-w", dest="wordset", required=True)
    parser.add_argument("-o", dest="output", default=None)
    args = parser.parse_args()

    dataset_file = args.dataset
    wordset_file = args.wordset
    output_file = args.output or default_output_path(dataset_file)
    print_parsed_args(dataset_file, wordset_file, output_file)

    df = read_weird_csv(dataset_file)
    words = read_wordset(wordset_file)
    nlp = load_spacy_pipeline()
    vectorized_df = build_vectorized_dataframe(df, words, nlp)
    vectorized_df.to_csv(output_file, index=False)

    print(f"Wrote {len(vectorized_df)} rows and {len(words)} word columns to {output_file}")


if __name__ == "__main__":
    main()
