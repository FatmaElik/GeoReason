"""
Visual prompting helpers.

Design decision (see research-log/2026-07-05-pilot01-design.md):
we mark the target region with a box OUTLINE, never a filled overlay.
A filled overlay hides the very pixels the model must judge; an
outline tells the model where to look while keeping the evidence
visible.
"""

from PIL import Image, ImageDraw


def draw_box(
    image_path: str,
    bbox,
    out_path: str | None = None,
    color=(255, 0, 0),
    width: int = 3,
) -> Image.Image:
    """Draw a rectangle outline on an image.

    Parameters
    ----------
    image_path : path to the source image.
    bbox : (x0, y0, x1, y1) rectangle in pixel coordinates.
    out_path : if given, the result is also saved there.
    color, width : outline appearance.

    Returns the PIL image with the box drawn.
    """
    image = Image.open(image_path).convert("RGB")
    draw = ImageDraw.Draw(image)
    draw.rectangle(bbox, outline=color, width=width)
    if out_path is not None:
        image.save(out_path)
    return image
