#!/usr/bin/env python3
import os
import glob
import math
import argparse

def load_probs(path):
    """Load lines 'Ri 0.xxx' -> dict[Ri] = float."""
    probs = {}
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) != 2:
                continue
            resp, p = parts
            try:
                probs[resp] = float(p)
            except ValueError:
                continue
    return probs

def load_clusters(path):
    """Load lines 'Ri 1' -> dict[Ri] = int."""
    clusters = {}
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) != 2:
                continue
            resp, c = parts
            try:
                clusters[resp] = int(c)
            except ValueError:
                continue
    return clusters

def semantic_entropy(probs, clusters):
    """
    Compute semantic entropy over the given clusters.
    probs: dict[resp]->p, clusters: dict[resp]->cluster_id
    """
    # Sum probs per cluster
    p_per_c = {}
    for resp, p in probs.items():
        c = clusters.get(resp)
        if c is None:
            # response with no cluster assignment -> skip its mass entirely
            continue
        p_per_c[c] = p_per_c.get(c, 0.0) + p

    # Compute entropy (natural log)
    H = 0.0
    for p in p_per_c.values():
        if p > 0:
            H -= p * math.log(p)
    return H

def main():
    parser = argparse.ArgumentParser(
        description="Compute semantic entropy for paired probability+cluster files."
    )
    parser.add_argument("prob_dir", help="Directory with probability files (*.txt)")
    parser.add_argument("cluster_dir", help="Directory with cluster files (*.txt)")
    parser.add_argument("output_path", help="Output file for '<id> <semantic_entropy>'")
    args = parser.parse_args()

    out_lines = []
    for prob_path in glob.glob(os.path.join(args.prob_dir, "*.txt")):
        file_id = os.path.splitext(os.path.basename(prob_path))[0]
        cluster_path = os.path.join(args.cluster_dir, f"{file_id}.txt")
        # Skip if no cluster file exists
        if not os.path.isfile(cluster_path):
            continue

        probs    = load_probs(prob_path)
        clusters = load_clusters(cluster_path)

        H = semantic_entropy(probs, clusters)
        out_lines.append(f"{file_id} {H:.6f}")

    with open(args.output_path, 'w', encoding='utf-8') as outf:
        outf.write("\n".join(out_lines))

    print(f"Computed semantic entropy for {len(out_lines)} files. Results in {args.output_path}")

if __name__ == "__main__":
    main()
