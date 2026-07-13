# Native vector workflow

Use this branch for an existing SVG, deterministic geometric/UI artwork, or an SVG illustration whose fills, gradients, masks, and effects can express the requested appearance faithfully.

## Preserve the contract

Inspect the target project's existing icon conventions before editing or creating artwork. Match its `viewBox`, rendered width and height, fill/stroke model, stroke width, caps, joins, corner radius, optical padding, naming, and color behavior. Preserve an existing SVG's IDs and geometry unless the request requires changing them.

For a new icon without project conventions, use a square `24×24` coordinate system for simple UI artwork or `1024×1024` for detailed illustration. Use the exact contracted color; use `currentColor` only when the user or target system expects inherited color.

## Build self-contained SVG

- Express geometry with SVG paths and primitives; keep repeated geometry intentional and readable.
- Keep gradients, masks, clip paths, and filters local to the file with unique IDs and local `#id` references.
- Include a `viewBox` and explicit matching width and height. Keep artwork inside the viewBox with the contracted optical padding.
- Preserve transparency where the appearance requires it.
- Keep the delivered SVG self-contained: embed no raster image, script, remote resource, external stylesheet, font dependency, or reference to another file.

For a set, reuse one shared artboard, geometry grammar, stroke/detail weight, palette behavior, and optical bounds.

## Validate and preview

```bash
python3 "<skill-dir>/scripts/validate_icon.py" \
  "<workspace>/<asset-name>.svg"
```

Render the SVG at the smallest intended size and at a larger inspection size. Confirm the subject, geometry, effects, color, transparency, clipping, and padding against the asset contract. For a set, validate every SVG together with `--require-matching-canvas` and compare the rendered row as one family.
