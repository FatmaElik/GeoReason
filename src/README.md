# src/georeason

Small reusable utilities shared across GeoReason experiments.

## Scope rule

Experiments in `experiments/` are **self-contained** — each one runs on
its own so that a reader can reproduce a single pilot without
installing anything repo-wide. Code is promoted into this package only
when it is used by more than one experiment or is clearly
experiment-independent.

Current modules:

| Module | What it provides |
|---|---|
| `masks.py` | `load_mask`, `patch_class_and_bbox` — patch-level class and damage bounding box from a pixel mask |
| `visual_prompt.py` | `draw_box` — box-outline visual prompt (never a filled overlay) |

Pilot 01 was written before this package existed and keeps its own
copies of these functions by design (self-containment). Future pilots
import from here.

## Usage

From the repository root:

```python
import sys
sys.path.append("src")

from georeason import patch_class_and_bbox, draw_box

patch_class, bbox = patch_class_and_bbox("satdemo/labels/000000000005.tif")
draw_box("satdemo/images/000000000005.tif", bbox, "boxed.png")
```

No installation step is required; the package is plain Python with
`numpy` and `Pillow` as its only dependencies.
