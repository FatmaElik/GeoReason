"""
Step 1 — Prepare samples for Pilot 01.

What this script does:
 1. Reads image_label_pairs.csv from the satdemo folder.
 2. Derives a patch-level damage class from each mask
    (max non-zero value: if classes 3 and 4 both appear, the patch is 4).
 3. Computes the bounding box of all damage pixels and draws a RED BOX
    around it on the optical image. The pixels under the box stay visible
    — this is a visual prompt, not an overlay that hides evidence.
 4. Saves the boxed images to prompt_images/ and a samples.csv manifest.

Why a box and not a filled mask?
In an earlier exploratory notebook I painted the mask in red on top of
the image. That hides the very pixels the model must judge, so the task
degenerates into "count red blobs". A box outline keeps the evidence
visible while telling the model where to look.

Usage:
    python prepare_samples.py --base satdemo --out pilot_data
"""

import argparse
import os

import numpy as np
import pandas as pd
from PIL import Image, ImageDraw

BOX_MARGIN = 8      # pixels of context around the damage bounding box
BOX_WIDTH = 3       # line width of the red box
MIN_DAMAGE_PIXELS = 15  # skip patches where damage is too tiny to judge


def patch_class_and_bbox(label_path: str):
    """Return (patch_class, bbox) from a mask file. bbox = (x0, y0, x1, y1)."""
    mask = np.array(Image.open(label_path))
    if mask.ndim == 3:
        mask = mask[:, :, 0]

    values = np.unique(mask)
    damage_values = values[values != 0]
    if len(damage_values) == 0:
        return 0, None

    patch_class = int(damage_values.max())

    ys, xs = np.where(mask > 0)
    if len(xs) < MIN_DAMAGE_PIXELS:
        return patch_class, None  # too small to be a fair visual question

    height, width = mask.shape
    x0 = max(int(xs.min()) - BOX_MARGIN, 0)
    y0 = max(int(ys.min()) - BOX_MARGIN, 0)
    x1 = min(int(xs.max()) + BOX_MARGIN, width - 1)
    y1 = min(int(ys.max()) + BOX_MARGIN, height - 1)
    return patch_class, (x0, y0, x1, y1)


def draw_box(image_path: str, bbox, out_path: str):
    image = Image.open(image_path).convert("RGB")
    draw = ImageDraw.Draw(image)
    draw.rectangle(bbox, outline=(255, 0, 0), width=BOX_WIDTH)
    image.save(out_path)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", default="satdemo", help="dataset folder")
    parser.add_argument("--out", default="pilot_data", help="output folder")
    args = parser.parse_args()

    prompt_dir = os.path.join(args.out, "prompt_images")
    os.makedirs(prompt_dir, exist_ok=True)

    pairs = pd.read_csv(
        os.path.join(args.base, "image_label_pairs.csv"), dtype=str
    )
    pairs = pairs[pairs["pair_status"] == "matched"].reset_index(drop=True)

    rows = []
    skipped = 0

    for _, row in pairs.iterrows():
        label_path = os.path.join(args.base, row["label_path"])
        image_path = os.path.join(args.base, row["image_path"])

        patch_class, bbox = patch_class_and_bbox(label_path)

        if patch_class == 0 or bbox is None:
            skipped += 1
            continue

        out_name = f"{row['sample_id']}.png"
        draw_box(image_path, bbox, os.path.join(prompt_dir, out_name))

        rows.append({
            "sample_id": row["sample_id"],
            "prompt_image": os.path.join("prompt_images", out_name),
            "true_class": patch_class,
            "bbox": "-".join(map(str, bbox)),
        })

    samples = pd.DataFrame(rows)
    samples_path = os.path.join(args.out, "samples.csv")
    samples.to_csv(samples_path, index=False)

    print("Prepared samples:", len(samples))
    print("Skipped (empty or too small):", skipped)
    print("Class distribution:")
    print(samples["true_class"].value_counts().sort_index())
    print("Saved:", samples_path)


if __name__ == "__main__":
    main()
