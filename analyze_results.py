"""
Step 3 — Analyze the results.

Reports:
  1. Accuracy per condition
  2. Flip rate: among samples the model got RIGHT in the image-only
     condition, how often did adding text change its answer?
     (This is the core measurement: does text override visual evidence?)
  3. Abstention usage in condition E
  4. One bar chart: accuracy per condition (figure for README / email)

Usage:
    python analyze_results.py --data pilot_data
"""

import argparse
import os

import matplotlib.pyplot as plt
import pandas as pd

from prompts import CLASS_NAMES

CONDITION_LABELS = {
    "A_image_only": "Image only",
    "B_text_consistent": "+ Consistent report",
    "C_text_conflict": "+ Conflicting report",
    "D_news_conflict": "+ Conflicting news",
    "E_conflict_abstain": "Conflict + abstain allowed",
}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", default="pilot_data")
    args = parser.parse_args()

    df = pd.read_csv(
        os.path.join(args.data, "results.csv"), dtype={"sample_id": str}
    )
    df = df.drop_duplicates(subset=["sample_id", "condition"], keep="last")

    df["true_name"] = df["true_class"].map(CLASS_NAMES)
    df["correct"] = df["answer"] == df["true_name"]

    # ---- 1. accuracy per condition ----
    accuracy = (
        df.groupby("condition")["correct"].mean().mul(100).round(1)
    )
    print("=== Accuracy per condition (%) ===")
    print(accuracy.to_string())

    # ---- 2. flip rate ----
    base = df[df["condition"] == "A_image_only"][
        ["sample_id", "answer", "correct"]
    ].rename(columns={"answer": "base_answer", "correct": "base_correct"})

    merged = df.merge(base, on="sample_id")
    print("\n=== Flip rate: model was correct image-only, then text was added ===")
    for condition in ["B_text_consistent", "C_text_conflict",
                      "D_news_conflict", "E_conflict_abstain"]:
        sub = merged[
            (merged["condition"] == condition) & (merged["base_correct"])
        ]
        if len(sub) == 0:
            continue
        flipped = (sub["answer"] != sub["base_answer"]).mean() * 100
        print(f"{CONDITION_LABELS[condition]:32s} flip rate: {flipped:5.1f}%  (n={len(sub)})")

    # ---- 3. abstention usage ----
    abstain = df[df["condition"] == "E_conflict_abstain"]
    if len(abstain):
        used = (abstain["answer"] == "uncertain").mean() * 100
        print(f"\n=== Abstention ===\n'uncertain' used in {used:.1f}% of conflict cases (n={len(abstain)})")

    # ---- per-class breakdown ----
    print("\n=== Accuracy per condition and true class (%) ===")
    table = (
        df.pivot_table(
            index="condition", columns="true_name",
            values="correct", aggfunc="mean"
        ).mul(100).round(1)
    )
    print(table.to_string())

    # ---- 4. figure ----
    fig, ax = plt.subplots(figsize=(8, 4.5))
    labels = [CONDITION_LABELS[c] for c in accuracy.index]
    ax.bar(labels, accuracy.values, color="#4C72B0")
    ax.set_ylabel("Accuracy (%)")
    ax.set_ylim(0, 100)
    ax.set_title("Does conflicting text override visual evidence?")
    plt.xticks(rotation=20, ha="right")
    plt.tight_layout()

    fig_path = os.path.join(args.data, "accuracy_per_condition.png")
    plt.savefig(fig_path, dpi=150)
    print("\nFigure saved:", fig_path)


if __name__ == "__main__":
    main()
