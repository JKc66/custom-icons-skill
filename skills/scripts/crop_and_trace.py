#!/usr/bin/env python3
"""Prepare an icon source for Potrace or make a simple chroma-key cutout."""

from __future__ import annotations

import argparse
from pathlib import Path
import re
import sys
from typing import Tuple


Color = Tuple[int, int, int]


def _die(message: str, code: int = 1) -> None:
    print(f"Error: {message}", file=sys.stderr)
    raise SystemExit(code)


def _load_pillow():
    try:
        from PIL import Image, ImageOps, UnidentifiedImageError
    except ImportError:
        _die("Pillow is required. Install the Python package 'pillow' in the active environment.")
    return Image, ImageOps, UnidentifiedImageError


def _parse_key_color(raw: str) -> Color:
    match = re.fullmatch(r"#?([0-9a-fA-F]{6})", raw.strip())
    if not match:
        _die("--key-color must be a hex RGB value such as #00ff00.")
    value = match.group(1)
    return tuple(int(value[index : index + 2], 16) for index in (0, 2, 4))  # type: ignore[return-value]


def _validate_args(args: argparse.Namespace) -> None:
    source = Path(args.source)
    if not source.is_file():
        _die(f"Input image not found: {source}")
    if not 0 <= args.threshold <= 255:
        _die("--threshold must be between 0 and 255.")
    if not 0 <= args.tolerance <= 255:
        _die("--tolerance must be between 0 and 255.")
    if args.padding < 0:
        _die("--padding must be zero or greater.")
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]*", args.name):
        _die("name must be a filename-safe basename without path separators.")
    if args.key_color and not args.chroma:
        _die("--key-color is only valid together with --chroma.")


def _remove_key(image, key: Color, tolerance: int):
    pixels = image.load()
    width, height = image.size
    matched = 0
    for y in range(height):
        for x in range(width):
            red, green, blue, alpha = pixels[x, y]
            distance = max(abs(red - key[0]), abs(green - key[1]), abs(blue - key[2]))
            if distance <= tolerance:
                pixels[x, y] = (0, 0, 0, 0)
                matched += 1
            else:
                pixels[x, y] = (red, green, blue, alpha)
    if matched == 0:
        _die(
            f"No pixels matched key #{key[0]:02x}{key[1]:02x}{key[2]:02x} "
            f"at tolerance {tolerance}."
        )
    return image


def _composite_on_white(image):
    Image, _, _ = _load_pillow()
    background = Image.new("RGBA", image.size, (255, 255, 255, 255))
    return Image.alpha_composite(background, image).convert("RGB")


def _crop_to_bbox(image, bbox, padding: int):
    if bbox is None:
        _die("No visible icon subject was found in the source image.")
    left, top, right, bottom = bbox
    return image.crop(
        (
            max(0, left - padding),
            max(0, top - padding),
            min(image.width, right + padding),
            min(image.height, bottom + padding),
        )
    )


def process_icon(
    source_path: Path,
    output_dir: Path,
    name: str,
    *,
    threshold: int,
    chroma_key: Color | None,
    tolerance: int,
    padding: int,
) -> None:
    Image, ImageOps, UnidentifiedImageError = _load_pillow()
    try:
        with Image.open(source_path) as source:
            image = source.convert("RGBA")
    except (UnidentifiedImageError, OSError) as error:
        _die(f"Could not read input image {source_path}: {error}")

    if chroma_key is not None:
        image = _remove_key(image, chroma_key, tolerance)
        bbox = image.getchannel("A").getbbox()
    else:
        flattened = _composite_on_white(image)
        gray = ImageOps.grayscale(flattened)
        bbox = gray.point(lambda pixel: 255 if pixel < 245 else 0).getbbox()

    image = _crop_to_bbox(image, bbox, padding)
    output_dir.mkdir(parents=True, exist_ok=True)
    png_path = output_dir / f"{name}.png"
    image.save(png_path, format="PNG", optimize=True)

    print(f"Wrote {png_path}")
    if chroma_key is not None:
        print(f"Key color: #{chroma_key[0]:02x}{chroma_key[1]:02x}{chroma_key[2]:02x}")
        return

    flattened = _composite_on_white(image)
    gray = ImageOps.grayscale(flattened)
    bitmap = gray.point(lambda pixel: 0 if pixel < threshold else 255, mode="1")
    if bitmap.getextrema() == (255, 255):
        _die(
            "Binarization produced no black foreground pixels. "
            "Raise --threshold or use a higher-contrast source."
        )
    pbm_path = output_dir / f"{name}.pbm"
    bitmap.save(pbm_path)
    print(f"Wrote {pbm_path}")
    print(f"Threshold: {threshold}")


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Crop an icon source and prepare a PBM trace or simple chroma-key PNG."
    )
    parser.add_argument("source", help="Input image path.")
    parser.add_argument("output_dir", help="Directory for generated files.")
    parser.add_argument("name", help="Filename-safe basename for generated files.")
    parser.add_argument(
        "--threshold",
        type=int,
        default=180,
        help="Black/white threshold for vector tracing, 0-255 (default: 180).",
    )
    parser.add_argument(
        "--chroma",
        action="store_true",
        help="Write a simple transparent cutout instead of a PBM trace source.",
    )
    parser.add_argument(
        "--key-color",
        help="Chroma key as hex RGB (default with --chroma: #00ff00).",
    )
    parser.add_argument(
        "--tolerance",
        type=int,
        default=60,
        help="Maximum per-channel chroma distance, 0-255 (default: 60).",
    )
    parser.add_argument(
        "--padding",
        type=int,
        default=12,
        help="Source pixels retained around the detected subject (default: 12).",
    )
    return parser


def main() -> None:
    parser = _build_parser()
    args = parser.parse_args()
    _validate_args(args)
    key = _parse_key_color(args.key_color or "#00ff00") if args.chroma else None
    process_icon(
        Path(args.source),
        Path(args.output_dir),
        args.name,
        threshold=args.threshold,
        chroma_key=key,
        tolerance=args.tolerance,
        padding=args.padding,
    )


if __name__ == "__main__":
    main()
