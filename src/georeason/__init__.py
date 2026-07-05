"""
georeason — small reusable utilities shared across GeoReason experiments.

Rule of the repository: each experiment stays self-contained and
runnable on its own. Code moves here only after it has been used by
at least two experiments or is clearly experiment-independent.
"""

__version__ = "0.1.0"

from .masks import patch_class_and_bbox
from .visual_prompt import draw_box

__all__ = ["patch_class_and_bbox", "draw_box"]
