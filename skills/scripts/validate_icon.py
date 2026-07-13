#!/usr/bin/env python3
"""Validate structural requirements for generated SVG and transparent raster icons."""

from __future__ import annotations

import argparse
import math
from pathlib import Path
import sys
import xml.etree.ElementTree as ET


SVG_GRAPHICS = {"path", "circle", "ellipse", "rect", "line", "polyline", "polygon", "use"}
SVG_FORBIDDEN = {"script", "foreignObject", "image"}
RASTER_SUFFIXES = {".png", ".webp"}


def _die(message: str, code: int = 1) -> None:
    print(f"FAIL: {message}", file=sys.stderr)
    raise SystemExit(code)


def _local_name(tag: object) -> str:
    return tag.rsplit("}", 1)[-1] if isinstance(tag, str) else ""


def _parse_viewbox(raw: str) -> tuple[float, float, float, float]:
    values = raw.replace(",", " ").split()
    if len(values) != 4:
        _die("SVG viewBox must contain four numbers.")
    try:
        parsed = tuple(float(value) for value in values)
    except ValueError:
        _die("SVG viewBox contains a non-numeric value.")
    if not all(math.isfinite(value) for value in parsed):
        _die("SVG viewBox values must be finite.")
    if parsed[2] <= 0 or parsed[3] <= 0:
        _die("SVG viewBox width and height must be positive.")
    return parsed  # type: ignore[return-value]


def _validate_svg(path: Path) -> dict[str, object]:
    try:
        tree = ET.parse(path)
    except (ET.ParseError, OSError) as error:
        _die(f"Could not parse SVG: {error}")

    root = tree.getroot()
    if _local_name(root.tag) != "svg":
        _die("The XML root element is not <svg>.")
    viewbox_raw = root.get("viewBox")
    if not viewbox_raw:
        _die("SVG is missing a viewBox.")
    viewbox = _parse_viewbox(viewbox_raw)

    graphics = []
    forbidden = []
    local_ids = {
        element.get("id")
        for element in root.iter()
        if isinstance(element.tag, str) and element.get("id")
    }
    for element in root.iter():
        name = _local_name(element.tag)
        if name in SVG_GRAPHICS:
            graphics.append(element)
        if name in SVG_FORBIDDEN:
            forbidden.append(name)
        for attribute, value in element.attrib.items():
            if _local_name(attribute) != "href":
                continue
            reference = value.strip()
            if not reference.startswith("#"):
                _die("SVG href references must stay inside the delivered file.")
            if len(reference) == 1 or reference[1:] not in local_ids:
                _die(f"SVG href points to a missing local ID: {reference}")

    if forbidden:
        _die(f"SVG contains disallowed element(s): {', '.join(sorted(set(forbidden)))}.")
    if not graphics:
        _die("SVG contains no vector graphics elements.")
    for element in graphics:
        if _local_name(element.tag) == "path" and not element.get("d", "").strip():
            _die("SVG contains an empty path.")

    path_count = sum(_local_name(element.tag) == "path" for element in graphics)
    print(
        "PASS: SVG "
        f"viewBox={viewbox[0]:g} {viewbox[1]:g} {viewbox[2]:g} {viewbox[3]:g}; "
        f"graphics={len(graphics)}; paths={path_count}"
    )
    return {
        "kind": "svg",
        "path": path,
        "canvas": (viewbox, root.get("width"), root.get("height")),
    }


def _load_pillow():
    try:
        from PIL import Image, UnidentifiedImageError
    except ImportError:
        _die("Pillow is required. Install the Python package 'pillow' in the active environment.")
    return Image, UnidentifiedImageError


def _validate_raster(path: Path, require_transparent_corners: bool) -> dict[str, object]:
    Image, UnidentifiedImageError = _load_pillow()
    try:
        with Image.open(path) as source:
            source.load()
            image = source.convert("RGBA")
    except (UnidentifiedImageError, OSError) as error:
        _die(f"Could not read raster image: {error}")

    width, height = image.size
    if width <= 0 or height <= 0:
        _die("Raster dimensions must be positive.")

    alpha = image.getchannel("A")
    alpha_min, alpha_max = alpha.getextrema()
    if alpha_max == 0:
        _die("Raster is fully transparent; no icon subject remains.")
    if alpha_min == 255:
        _die("Raster has no transparent pixels.")

    corners = [
        alpha.getpixel((0, 0)),
        alpha.getpixel((width - 1, 0)),
        alpha.getpixel((0, height - 1)),
        alpha.getpixel((width - 1, height - 1)),
    ]
    if require_transparent_corners and any(value != 0 for value in corners):
        _die(f"Raster corners are not fully transparent: {corners}.")

    bbox = alpha.getbbox()
    if bbox is None:
        _die("Raster has no visible alpha bounds.")
    histogram = alpha.histogram()
    transparent = histogram[0]
    partial = sum(histogram[1:255])
    opaque = histogram[255]
    print(
        "PASS: raster "
        f"size={width}x{height}; alpha_bbox={bbox}; "
        f"transparent={transparent}; partial={partial}; opaque={opaque}"
    )
    return {"kind": "raster", "path": path, "canvas": (width, height)}


def _validate_matching_canvases(results: list[dict[str, object]]) -> None:
    for kind in ("svg", "raster"):
        branch = [result for result in results if result["kind"] == kind]
        if len(branch) < 2:
            continue
        expected = branch[0]["canvas"]
        mismatches = [result for result in branch[1:] if result["canvas"] != expected]
        if mismatches:
            details = ", ".join(
                f"{result['path']}={result['canvas']}" for result in branch
            )
            _die(f"{kind} canvas mismatch; expected one shared canvas: {details}")
        print(f"PASS: matching {kind} canvas across {len(branch)} assets: {expected}")


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Validate a generated SVG, transparent PNG, or transparent WebP icon."
    )
    parser.add_argument("asset", nargs="+", help="Path(s) to icon assets.")
    parser.add_argument(
        "--require-transparent-corners",
        action="store_true",
        help="Require all four raster corner pixels to have alpha 0.",
    )
    parser.add_argument(
        "--require-matching-canvas",
        action="store_true",
        help="Require one shared canvas within each SVG or raster group.",
    )
    return parser


def main() -> None:
    parser = _build_parser()
    args = parser.parse_args()
    results: list[dict[str, object]] = []
    for raw_path in args.asset:
        path = Path(raw_path)
        if not path.is_file():
            _die(f"Asset not found: {path}")

        suffix = path.suffix.lower()
        if suffix == ".svg":
            if args.require_transparent_corners:
                _die("--require-transparent-corners applies only to raster assets.")
            results.append(_validate_svg(path))
        elif suffix in RASTER_SUFFIXES:
            results.append(_validate_raster(path, args.require_transparent_corners))
        else:
            _die("Supported asset extensions are .svg, .png, and .webp.")

    if args.require_matching_canvas:
        _validate_matching_canvases(results)


if __name__ == "__main__":
    main()
