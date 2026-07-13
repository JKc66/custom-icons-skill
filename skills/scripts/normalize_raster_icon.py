#!/usr/bin/env python3
"""Center a transparent raster icon on an exact square canvas."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys


def _die(message: str, code: int = 1) -> None:
    print(f"Error: {message}", file=sys.stderr)
    raise SystemExit(code)


def _load_pillow():
    try:
        from PIL import Image, UnidentifiedImageError
    except ImportError:
        _die("Pillow is required. Install the Python package 'pillow' in the active environment.")
    return Image, UnidentifiedImageError


def _validate_args(args: argparse.Namespace) -> None:
    source = Path(args.input)
    if not source.is_file():
        _die(f"Input image not found: {source}")
    output = Path(args.out)
    if output.suffix.lower() not in {".png", ".webp"}:
        _die("--out must end in .png or .webp.")
    if output.exists() and not args.force:
        _die(f"Output already exists: {output} (use --force to overwrite)")
    if args.canvas_size <= 0:
        _die("--canvas-size must be greater than zero.")
    if args.padding < 0:
        _die("--padding must be zero or greater.")
    if args.padding * 2 >= args.canvas_size:
        _die("--padding must leave a positive inner canvas.")


def _normalize(args: argparse.Namespace) -> None:
    Image, UnidentifiedImageError = _load_pillow()
    source = Path(args.input)
    output = Path(args.out)
    try:
        with Image.open(source) as opened:
            image = opened.convert("RGBA")
    except (UnidentifiedImageError, OSError) as error:
        _die(f"Could not read input image {source}: {error}")

    alpha = image.getchannel("A")
    alpha_min, alpha_max = alpha.getextrema()
    if alpha_max == 0:
        _die("Input is fully transparent; no icon subject remains.")
    if alpha_min == 255:
        _die("Input has no transparent pixels to define an isolated icon subject.")
    bbox = alpha.getbbox()
    if bbox is None:
        _die("Input has no visible alpha bounds.")
    subject = image.crop(bbox)

    inner_size = args.canvas_size - (args.padding * 2)
    scale = min(inner_size / subject.width, inner_size / subject.height)
    width = max(1, int(round(subject.width * scale)))
    height = max(1, int(round(subject.height * scale)))
    subject = subject.resize((width, height), Image.Resampling.LANCZOS)

    canvas = Image.new("RGBA", (args.canvas_size, args.canvas_size), (0, 0, 0, 0))
    left = (args.canvas_size - width) // 2
    top = (args.canvas_size - height) // 2
    canvas.alpha_composite(subject, (left, top))

    output.parent.mkdir(parents=True, exist_ok=True)
    if output.suffix.lower() == ".webp":
        canvas.save(output, format="WEBP", lossless=True, quality=100, method=6)
    else:
        canvas.save(output, format="PNG", optimize=True)
    print(f"Wrote {output}")
    print(f"Canvas: {args.canvas_size}x{args.canvas_size}; visible size: {width}x{height}")


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Center a transparent PNG/WebP icon on an exact square canvas."
    )
    parser.add_argument("--input", required=True, help="Transparent input image.")
    parser.add_argument("--out", required=True, help="Output .png or .webp path.")
    parser.add_argument(
        "--canvas-size",
        required=True,
        type=int,
        help="Square output width and height in pixels.",
    )
    parser.add_argument(
        "--padding",
        type=int,
        default=12,
        help="Minimum transparent padding in output pixels (default: 12).",
    )
    parser.add_argument("--force", action="store_true", help="Overwrite an existing output file.")
    return parser


def main() -> None:
    parser = _build_parser()
    args = parser.parse_args()
    _validate_args(args)
    _normalize(args)


if __name__ == "__main__":
    main()
