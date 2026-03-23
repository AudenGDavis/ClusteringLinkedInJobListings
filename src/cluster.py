import argparse
import os
import sys

import matplotlib.pyplot as plt
import pandas as pd
from sklearn.cluster import KMeans


def print_help() -> None:
    print("Usage: ./manager.sh cluster -d [dataset file] -o [output file] -k [max clusters]")
    print("")
    print("  -d (required)  Vectorized dataset .csv file")
    print("  -o (optional)  Output .csv file (default: 'clustered' prepended to dataset name)")
    print("  -k (optional)  Maximum number of clusters to try (default: 10)")


def default_output_path(dataset_file: str) -> str:
    directory = os.path.dirname(dataset_file)
    filename = os.path.basename(dataset_file)
    return os.path.join(directory, f"clustered{filename}")


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


def run_clustering(dataset_file: str, output_file: str, max_k: int) -> None:
    if not os.path.isfile(dataset_file):
        print(f"Error: Dataset file '{dataset_file}' not found.")
        sys.exit(1)

    if not dataset_file.endswith(".csv"):
        print("Error: Dataset file must be a .csv file.")
        sys.exit(1)

    if not output_file.endswith(".csv"):
        print("Error: Output file must be a .csv file.")
        sys.exit(1)

    df = read_weird_csv(dataset_file)

    # The first column is the job_id; the rest are feature columns.
    id_col = df.columns[0]
    feature_cols = df.columns[1:]
    X = df[feature_cols].astype(float).values

    n_samples = len(df)
    if max_k >= n_samples:
        print(
            f"Warning: max_k ({max_k}) >= number of samples ({n_samples}). "
            f"Capping max_k at {n_samples - 1}."
        )
        max_k = n_samples - 1

    inertias: list[float] = []
    k_values = list(range(1, max_k + 1))

    result_df = df[[id_col]].copy()

    for k in k_values:
        model = KMeans(n_clusters=k, random_state=42, n_init="auto")
        model.fit(X)
        inertia = float(model.inertia_)
        inertias.append(inertia)
        print(f"k={k:>3}  avg_squared_euclidean_distance={inertia / n_samples:.6f}")
        result_df[f"cluster_k{k}"] = model.labels_

    result_df.to_csv(output_file, index=False)
    print(f"\nCluster assignments saved to '{output_file}'")

    # Save elbow plot
    plot_path = os.path.splitext(output_file)[0] + ".png"
    avg_inertias = [v / n_samples for v in inertias]

    plt.figure(figsize=(14, 8))
    plt.plot(k_values, avg_inertias, marker="o")
    plt.xlabel("Number of clusters (k)")
    plt.ylabel("Avg squared Euclidean distance")
    plt.title("K-means Elbow Plot")
    plt.xticks(range(0, max_k + 1, 5))
    plt.tight_layout()
    plt.savefig(plot_path)
    plt.close()
    print(f"Elbow plot saved to '{plot_path}'")


def main() -> None:
    if len(sys.argv) > 1 and sys.argv[1] == "--help":
        print_help()
        return

    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("-d", dest="dataset", required=True)
    parser.add_argument("-o", dest="output", default=None)
    parser.add_argument("-k", dest="max_clusters", type=int, default=10)
    args = parser.parse_args()

    dataset_file = args.dataset
    output_file = args.output or default_output_path(dataset_file)
    max_k = args.max_clusters

    run_clustering(dataset_file, output_file, max_k)


if __name__ == "__main__":
    main()
