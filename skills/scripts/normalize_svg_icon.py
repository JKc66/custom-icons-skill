#!/usr/bin/env python3
"""Normalize SVG artwork to an exact square viewBox with optical padding."""

from __future__ import annotations

import argparse
import math
from pathlib import Path
import sys
import xml.etree.ElementTree as ET


ROOT_ONLY_ELEMENTS = {"defs", "style", "title", "desc", "metadata"}


def _die(message: str, code: int = 1) -> None:
    print(f"Error: {message}", file=sys.stderr)
    raise SystemExit(code)


def _local_name(tag: object) -> str:
    return tag.rsplit("}", 1)[-1] if isinstance(tag, str) else ""


def _namespace(tag: str) -> str | None:
    if tag.startswith("{") and "}" in tag:
        return tag[1:].split("}", 1)[0]
    return None


def _parse_viewbox(raw: str | None) -> tuple[float, float, float, float]:
    if not raw:
        _die("Input SVG is missing a viewBox.")
    values = raw.replace(",", " ").split()
    if len(values) != 4:
        _die("Input SVG viewBox must contain four numbers.")
    try:
        parsed = tuple(float(value) for value in values)
    except ValueError:
        _die("Input SVG viewBox contains a non-numeric value.")
    if not all(math.isfinite(value) for value in parsed):
        _die("Input SVG viewBox values must be finite.")
    if parsed[2] <= 0 or parsed[3] <= 0:
        _die("Input SVG viewBox width and height must be positive.")
    return parsed  # type: ignore[return-value]


def _fmt(value: float) -> str:
    rounded = round(value, 6)
    return f"{rounded:g}"


def _validate_args(args: argparse.Namespace) -> None:
    source = Path(args.input)
    if not source.is_file():
        _die(f"Input SVG not found: {source}")
    output = Path(args.out)
    if output.suffix.lower() != ".svg":
        _die("--out must end in .svg.")
    if output.exists() and not args.force:
        _die(f"Output already exists: {output} (use --force to overwrite)")
    if not math.isfinite(args.canvas_size) or args.canvas_size <= 0:
        _die("--canvas-size must be a positive finite number.")
    if not math.isfinite(args.padding) or args.padding < 0:
        _die("--padding must be a non-negative finite number.")
    if args.padding * 2 >= args.canvas_size:
        _die("--padding must leave a positive inner canvas.")


def _normalize(args: argparse.Namespace) -> None:
    source = Path(args.input)
    output = Path(args.out)
    try:
        tree = ET.parse(source)
    except (ET.ParseError, OSError) as error:
        _die(f"Could not parse input SVG: {error}")
    root = tree.getroot()
    if _local_name(root.tag) != "svg":
        _die("Input XML root is not <svg>.")

    min_x, min_y, width, height = _parse_viewbox(root.get("viewBox"))
    inner = args.canvas_size - (args.padding * 2)
    scale = min(inner / width, inner / height)
    translated_width = width * scale
    translated_height = height * scale
    translate_x = ((args.canvas_size - translated_width) / 2) - (min_x * scale)
    translate_y = ((args.canvas_size - translated_height) / 2) - (min_y * scale)

    namespace = _namespace(root.tag)
    if namespace:
        ET.register_namespace("", namespace)
    group_tag = f"{{{namespace}}}g" if namespace else "g"
    group = ET.Element(
        group_tag,
        {
            "transform": (
                f"translate({_fmt(translate_x)} {_fmt(translate_y)}) "
                f"scale({_fmt(scale)})"
            )
        },
    )

    movable = [
        child for child in list(root) if _local_name(child.tag) not in ROOT_ONLY_ELEMENTS
    ]
    if not movable:
        _die("Input SVG contains no movable artwork elements.")
    for child in movable:
        root.remove(child)
        group.append(child)
    root.append(group)

    size = _fmt(args.canvas_size)
    root.set("viewBox", f"0 0 {size} {size}")
    root.set("width", size)
    root.set("height", size)
    root.set("preserveAspectRatio", "xMidYMid meet")

    output.parent.mkdir(parents=True, exist_ok=True)
    tree.write(output, encoding="utf-8", xml_declaration=True)
    print(f"Wrote {output}")
    print(
        f"Canvas: {size}x{size}; padding: {_fmt(args.padding)}; "
        f"scale: {_fmt(scale)}"
    )


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Normalize SVG artwork to an exact square coordinate system."
    )
    parser.add_argument("--input", required=True, help="Input SVG path.")
    parser.add_argument("--out", required=True, help="Output SVG path.")
    parser.add_argument(
        "--canvas-size",
        required=True,
        type=float,
        help="Square output viewBox, width, and height.",
    )
    parser.add_argument(
        "--padding",
        type=float,
        default=2.0,
        help="Optical padding in output viewBox units (default: 2).",
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
