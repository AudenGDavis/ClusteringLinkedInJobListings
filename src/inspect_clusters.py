import argparse
import sys

import pandas as pd


def print_help() -> None:
    print("Usage: ./manager.sh inspect -c [cluster file] -d [dataset file] -k [k value]")
    print("")
    print("  -c (required)  Clustered .csv file (output of cluster command)")
    print("  -d (required)  Original dataset .csv file")
    print("  -k (required)  K value to inspect (number of clusters)")


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


def inspect_clusters(cluster_file: str, dataset_file: str, k: int) -> None:
    cluster_df = pd.read_csv(cluster_file)
    dataset_df = read_weird_csv(dataset_file)

    cluster_col = f"cluster_k{k}"
    if cluster_col not in cluster_df.columns:
        print(f"Error: Column '{cluster_col}' not found in '{cluster_file}'.")
        print(f"Available k values: {[c for c in cluster_df.columns if c.startswith('cluster_k')]}")
        sys.exit(1)

    id_col = cluster_df.columns[0]

    cluster_df[id_col] = cluster_df[id_col].astype(str)
    dataset_df[id_col] = dataset_df[id_col].astype(str)

    merged = cluster_df[[id_col, cluster_col]].merge(
        dataset_df[[id_col, "description"]], on=id_col, how="inner"
    )

    for cluster_id in sorted(merged[cluster_col].astype(int).unique()):
        group = merged[merged[cluster_col].astype(int) == cluster_id]
        sample = group.head(10)

        print(f"\n{'='*80}")
        print(f" CLUSTER {cluster_id}  ({len(group)} total jobs)")
        print(f"{'='*80}")

        for i, (_, row) in enumerate(sample.iterrows(), 1):
            desc = str(row["description"])
            if len(desc) > 300:
                desc = desc[:300] + "..."
            print(f"\n  [{i}] Job {row[id_col]}")
            print(f"      {desc}")

    print()


def main() -> None:
    if len(sys.argv) > 1 and sys.argv[1] == "--help":
        print_help()
        return

    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("-c", dest="cluster_file", required=True)
    parser.add_argument("-d", dest="dataset", required=True)
    parser.add_argument("-k", dest="k", type=int, required=True)
    args = parser.parse_args()

    inspect_clusters(args.cluster_file, args.dataset, args.k)


if __name__ == "__main__":
    main()
