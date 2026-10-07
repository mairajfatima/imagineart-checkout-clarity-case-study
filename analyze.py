"""
03_analyze_and_chart.py

Reads your final, manually-corrected categorized_reviews.csv
(specifically the 'category_final' column) and produces:
  - summary counts printed to the console
  - chart_complaint_categories.png

HOW TO RUN:
    pip install pandas matplotlib
    python 03_analyze_and_chart.py
"""

import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

INPUT_FILE = "categorized_reviews.csv"


def main():
    df = pd.read_csv(INPUT_FILE)

    # use category_final if filled in, otherwise fall back to category_auto
    df["category"] = df["category_final"].where(
        df["category_final"].notna() & (df["category_final"] != ""),
        df["category_auto"],
    )

    df["rating"] = pd.to_numeric(df["rating"], errors="coerce")

    print("Total reviews:", len(df))

    negative = df[df["rating"] <= 3]
    print("Negative/neutral (<=3 stars):", len(negative))
    print()

    counts = negative["category"].value_counts()
    print("Category breakdown (negative/neutral only):")
    print(counts)

    top_category = counts.index[0]
    top_pct = round(100 * counts.iloc[0] / len(negative), 1)
    print(f"\nTop complaint category: {top_category} "
          f"({counts.iloc[0]} of {len(negative)} = {top_pct}%)")

    # --- chart ---
    plt.rcParams.update({"font.size": 10, "axes.spines.top": False, "axes.spines.right": False})
    fig, ax = plt.subplots(figsize=(7, 4.5))
    colors = ["#5b4bdb" if c == top_category else "#8a94a6" for c in counts.index]
    ax.barh(counts.index[::-1], counts.values[::-1], color=colors[::-1])
    for i, v in enumerate(counts.values[::-1]):
        ax.text(v + 0.1, i, str(v), va="center", fontweight="bold")
    ax.set_xlabel(f"Number of negative/neutral reviews (n={len(negative)})")
    ax.set_title("ImagineArt: real review complaint categories")
    plt.tight_layout()
    plt.savefig("chart_complaint_categories.png", dpi=160)
    print("\nSaved chart_complaint_categories.png")


if __name__ == "__main__":
    main()