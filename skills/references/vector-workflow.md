# Traced vector workflow

Use this branch for monochrome silhouettes, line art, simple decorative artwork, or a raster image that must become SVG. Prefer a direct vector edit for an existing SVG and for deterministic geometry explicitly requested by the user.

## Create the source

Use a supplied image as the source when one exists. Otherwise, generate a high-resolution raster using this prompt contract:

```text
Asset: one scalable icon source
Subject: [exact subject and distinguishing features]
Style: [style anchor], monochrome vector-like [silhouette or line art]
Geometry: [stroke/detail weight, corner character, symmetry or asymmetry]
Composition: one centered isolated subject, square canvas, even optical padding, clear at [smallest target size]
Color: solid black artwork on a pure white background
Preserve from references: [identity, silhouette, proportions, composition, or other invariants]
Exclude: gradients, gray shading, texture, scenery, borders, unintended text, signatures, unrequested marks, and watermarks
```

Generate one icon per image. For a set, repeat the pilot's exact geometry, composition, and padding language and use the pilot as a style reference when the tool supports references.

Accept the source only when black/white separation is unambiguous, all intended negative spaces remain open, and the subject is recognizable at the target size.

## Process the source

Resolve `<skill-dir>` from the active `SKILL.md` and `<workspace>` from the main workflow. Keep trace drafts separate from the final SVG.

```bash
python3 "<skill-dir>/scripts/crop_and_trace.py" \
  "<source-image>" "<workspace>" "<asset-name>" \
  --threshold 180 --padding 12

potrace "<workspace>/<asset-name>.pbm" \
  --svg --flat --tight --turdsize 2 \
  --color "#000000" \
  --output "<workspace>/<asset-name>.trace.svg"

python3 "<skill-dir>/scripts/normalize_svg_icon.py" \
  --input "<workspace>/<asset-name>.trace.svg" \
  --out "<workspace>/<asset-name>.normalized.svg" \
  --canvas-size "<contracted-square-size>" \
  --padding "<contracted-padding>" \
  --force

bunx svgo "<workspace>/<asset-name>.normalized.svg" \
  --output "<workspace>/<asset-name>.svg" \
  --multipass

python3 "<skill-dir>/scripts/validate_icon.py" \
  "<workspace>/<asset-name>.svg"
```

Replace `#000000` with the contracted color at the Potrace step. This produces filled path geometry even when the source resembles a stroked line drawing.

Use the same square size and padding for every member of a set. Use size `24` with padding `2` for unspecified UI icons; scale both values proportionally for a different coordinate system.

If `bunx` cannot create temporary files in the environment, set `TMPDIR` to a writable temporary directory for that command. If SVGO is unavailable but the unoptimized trace validates, retain the trace as an explicitly reported unoptimized fallback rather than blocking delivery.

## Tune only when evidence requires it

- Raise `--threshold` when pale antialiasing or fine marks disappear; lower it when gray noise thickens the shape. Keep the value within `0..255`.
- Raise Potrace `--turdsize` to remove isolated specks; lower it when intentional tiny details disappear.
- Regenerate the source when tracing cannot recover a clean silhouette or open negative space. Tracing is not a substitute for a suitable source.

Keep the smallest change that fixes the observed defect and record the successful parameters in the workspace.

## Validate visually

Render or preview the final SVG rather than judging XML alone. Compare it with the processed PNG at the smallest intended size. Confirm that the `viewBox` is present, the artwork is not clipped, intended holes remain open, curve simplification has not changed the subject, and the final color matches the contract.

For a set, run:

```bash
python3 "<skill-dir>/scripts/validate_icon.py" \
  "<asset-1>.svg" "<asset-2>.svg" "<asset-n>.svg" \
  --require-matching-canvas
```
