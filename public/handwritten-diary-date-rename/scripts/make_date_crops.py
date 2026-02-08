#!/usr/bin/env python3
"""Create cropped helper images for reading handwritten dates in diary photos."""
from __future__ import annotations

import argparse
from pathlib import Path
from typing import Iterable, Tuple

from PIL import Image, ImageFilter, ImageOps

IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".heic"}


def parse_bands(value: str) -> list[Tuple[float, float]]:
    bands: list[Tuple[float, float]] = []
    for part in value.split(","):
        part = part.strip()
        if not part:
            continue
        a, b = part.split("-")
        bands.append((float(a), float(b)))
    return bands


def enhance(img: Image.Image, do_enhance: bool) -> Image.Image:
    if not do_enhance:
        return img
    img = ImageOps.autocontrast(img)
    img = img.filter(ImageFilter.SHARPEN)
    return img


def iter_images(src: Path) -> Iterable[Path]:
    for p in src.iterdir():
        if p.is_file() and p.suffix.lower() in IMAGE_EXTS:
            yield p


def main() -> int:
    parser = argparse.ArgumentParser(description="Create date crops for diary photos")
    parser.add_argument("--src", default=".", help="Source folder with images")
    parser.add_argument("--out", default="_datecrops", help="Output folder")
    parser.add_argument("--scale", type=int, default=2, help="Resize scale for crops")
    parser.add_argument("--top-frac", type=float, default=0.12, help="Top band height fraction")
    parser.add_argument(
        "--mid-bands",
        default="0.33-0.52,0.52-0.71,0.71-0.9",
        help="Comma-separated band ranges as start-end fractions",
    )
    parser.add_argument("--enhance", action="store_true", help="Auto-contrast + sharpen crops")
    args = parser.parse_args()

    src = Path(args.src)
    out = Path(args.out)
    top_dir = out / "top"
    mid_dir = out / "mid"
    top_dir.mkdir(parents=True, exist_ok=True)
    mid_dir.mkdir(parents=True, exist_ok=True)

    bands = parse_bands(args.mid_bands)

    count = 0
    for p in iter_images(src):
        try:
            im = Image.open(p)
        except Exception:
            continue
        w, h = im.size
        top_h = int(h * args.top_frac)
        top = im.crop((0, 0, w, top_h))
        if args.scale != 1:
            top = top.resize((top.width * args.scale, top.height * args.scale))
        top = enhance(top, args.enhance)
        top.save(top_dir / f"{p.stem}_top.jpg", quality=95)

        for i, (a, b) in enumerate(bands, 1):
            y1, y2 = int(h * a), int(h * b)
            mid = im.crop((0, y1, w, y2))
            if args.scale != 1:
                mid = mid.resize((mid.width * args.scale, mid.height * args.scale))
            mid = enhance(mid, args.enhance)
            mid.save(mid_dir / f"{p.stem}_mid{i}.jpg", quality=95)

        count += 1

    print(f"Saved crops for {count} images to: {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
