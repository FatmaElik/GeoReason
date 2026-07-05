"""
Utilities for working with pixel-level damage masks.

Masks follow the SAR–Optical Earthquake Damage Dataset convention:
0 = background, non-zero values = damage class ids.
"""

import numpy as np
from PIL import Image


def load_mask(label_path: str) -> np.ndarray:
    """Load a mask file as a 2-D array (first channel if multi-channel)."""
    mask = np.array(Image.open(label_path))
    if mask.ndim == 3:
        mask = mask[:, :, 0]
    return mask


def patch_class_and_bbox(
    label_path: str,
    margin: int = 8,
    min_damage_pixels: int = 15,
):
    """Derive a patch-level class and a damage bounding box from a mask.

    Class rule: the maximum non-zero value in the mask. If classes 3
    and 4 both appear in a patch, the patch is class 4 (worst damage
    dominates).

    Returns
    -------
    (patch_class, bbox)
        patch_class : int, 0 if the mask is empty.
        bbox : (x0, y0, x1, y1) with `margin` pixels of context,
               clipped to the image, or None if the mask is empty or
               the damage area is smaller than `min_damage_pixels`
               (too small to be a fair visual question).
    """
    mask = load_mask(label_path)

    values = np.unique(mask)
    damage_values = values[values != 0]
    if len(damage_values) == 0:
        return 0, None

    patch_class = int(damage_values.max())

    ys, xs = np.where(mask > 0)
    if len(xs) < min_damage_pixels:
        return patch_class, None

    height, width = mask.shape
    x0 = max(int(xs.min()) - margin, 0)
    y0 = max(int(ys.min()) - margin, 0)
    x1 = min(int(xs.max()) + margin, width - 1)
    y1 = min(int(ys.max()) + margin, height - 1)
    return patch_class, (x0, y0, x1, y1)
