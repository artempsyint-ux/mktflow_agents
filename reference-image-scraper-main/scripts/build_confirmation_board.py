#!/usr/bin/env python3
"""Build a PNG confirmation board from a reference-image manifest."""

from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont, ImageOps
except ImportError as exc:
    raise SystemExit(
        "Missing dependency: Pillow. Install pillow in the active environment or create the PNG board manually."
    ) from exc


W, H = 1920, 1080
BG = (0x17, 0x17, 0x19)
TEXT = (0xFF, 0xFF, 0xFF)

TITLE_POS = (60, 48)
TITLE_SIZE = 32

ROW_CATEGORY_POSITIONS = ((60, 205), (60, 638))
CATEGORY_SIZE = 26

IMG_W, IMG_H = 344, 245
IMG_X = (60, 424, 788, 1152, 1516)
ROW_Y = (261, 694)
MAX_ITEMS = 10


def font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = [
        ("/System/Library/Fonts/PingFang.ttc", 1),
        ("/System/Library/Fonts/PingFang.ttc", 0),
        ("/Library/Fonts/PingFang.ttc", 1),
        ("/System/Library/Fonts/STHeiti Medium.ttc", 0),
        ("/System/Library/Fonts/Supplemental/Arial.ttf", 0),
        ("/System/Library/Fonts/Helvetica.ttc", 0),
    ]
    for path, index in candidates:
        try:
            return ImageFont.truetype(path, size, index=index)
        except OSError:
            continue
    return ImageFont.load_default()


TITLE_FONT = font(TITLE_SIZE)
CATEGORY_FONT = font(CATEGORY_SIZE)


def fit_image(path: Path, size: tuple[int, int]) -> Image.Image:
    try:
        img = Image.open(path).convert("RGB")
    except OSError:
        img = Image.new("RGB", size, (40, 40, 42))
    return ImageOps.fit(img, size, method=Image.Resampling.LANCZOS, centering=(0.5, 0.5))


def row_category_label(items: list[dict]) -> str:
    if not items:
        return ""
    labels = [item.get("category") or item.get("keyword") or "Reference" for item in items]
    return Counter(labels).most_common(1)[0][0]


def board_title(data: dict) -> str:
    title = (data.get("title") or "").strip()
    if title:
        return title
    keywords = [kw.strip() for kw in data.get("keywords", []) if kw and str(kw).strip()]
    if keywords:
        return " / ".join(keywords)
    return "Reference image board"


def split_rows(items: list[dict]) -> tuple[list[dict], list[dict]]:
    selected = items[:MAX_ITEMS]
    return selected[:5], selected[5:10]


def draw_image_row(canvas: Image.Image, folder: Path, items: list[dict], y: int) -> None:
    for col, item in enumerate(items[:5]):
        x = IMG_X[col]
        img = fit_image(folder / item.get("filename", ""), (IMG_W, IMG_H))
        canvas.paste(img, (x, y))


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: build_confirmation_board.py <manifest.json>", file=sys.stderr)
        return 2

    manifest_path = Path(sys.argv[1]).expanduser().resolve()
    folder = manifest_path.parent
    data = json.loads(manifest_path.read_text(encoding="utf-8"))
    items = data.get("items", [])

    canvas = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(canvas)

    draw.text(TITLE_POS, board_title(data), fill=TEXT, font=TITLE_FONT)

    row1_items, row2_items = split_rows(items)
    rows = (row1_items, row2_items)

    if not items:
        message = "No image items found in manifest."
        draw.text((60, 261), message, fill=TEXT, font=CATEGORY_FONT)
    else:
        for row_items, (cat_x, cat_y), img_y in zip(rows, ROW_CATEGORY_POSITIONS, ROW_Y):
            if not row_items:
                continue
            draw.text((cat_x, cat_y), row_category_label(row_items), fill=TEXT, font=CATEGORY_FONT)
            draw_image_row(canvas, folder, row_items, img_y)

    output = folder / "confirmation-board.png"
    canvas.save(output)
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
