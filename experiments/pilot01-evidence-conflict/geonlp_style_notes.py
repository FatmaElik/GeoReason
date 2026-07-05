"""
Optional — Where the news-style template comes from.

The Turkish Disaster GeoNLP dataset is NOT used as ground truth here
(its labels are machine-generated and not yet human-verified). Its role
in this pilot is smaller and honest: it shows how real disaster news
actually phrases building damage, and that phrasing inspired the
NEWS_REPORT template in prompts.py.

This script samples earthquake-related articles so that the connection
is documented and reproducible.

Usage:
    pip install datasets
    python geonlp_style_notes.py
"""

import pandas as pd
from datasets import load_dataset


def main():
    dataset = load_dataset("FatmaElik/turkish-disaster-news-geonlp")

    parts = []
    for split in dataset.keys():
        part = dataset[split].to_pandas()
        part["split"] = split
        parts.append(part)
    news = pd.concat(parts, ignore_index=True)

    quake = news[
        news["hazard_type"].astype(str).str.lower().str.contains("earthquake", na=False)
    ]

    print("Total articles:", len(news))
    print("Earthquake-related:", len(quake))
    print("\nSample phrasings (first 200 chars each):\n")

    for _, row in quake.head(5).iterrows():
        text = str(row.get("text", row.get("content", "")))[:200]
        print("-", text.replace("\n", " "), "\n")


if __name__ == "__main__":
    main()
