# Transparent raster workflow

Use this branch for 3D, multicolor, shaded, textured, or highly detailed icons whose appearance depends on continuous tone. Deliver PNG or lossless WebP with an alpha channel.

## Choose a key color

Select a saturated flat background color that is absent from the subject and its edge colors. Green `#00ff00` is a useful default; use magenta `#ff00ff` for green subjects, or another distant hue when both appear in the palette. Record the selected key color with the source.

## Create or edit the source

Use a supplied image as the edit target when one exists. Otherwise, generate a high-resolution raster using this prompt contract:

```text
Asset: one transparent-ready raster icon
Subject: [exact subject and distinguishing features]
Style: [style anchor, material, lighting, perspective]
Composition: one centered isolated subject, square canvas, even optical padding, clear silhouette at [smallest target size]
Palette: [contracted subject colors]; exclude the background key color from the subject
Backdrop: perfectly uniform solid [key color] extending to every edge
Preserve from references: [identity, silhouette, proportions, composition, or other invariants]
Exclude: floor plane, backdrop shadows, reflections on the backdrop, gradients or texture in the backdrop, scenery, unintended text, signatures, unrequested marks, and watermarks
```

Generate one icon per image. For a set, repeat the pilot's camera, lighting, material, palette, optical size, and padding language and use the pilot as a style reference when supported.

Accept the source only when the background is uniform at all four corners, the subject does not use the key color, and no intended shadow or reflection merges into the backdrop.

## Remove the key

Resolve `<skill-dir>` from the active `SKILL.md` and `<workspace>` from the main workflow.

```bash
python3 "<skill-dir>/scripts/remove_chroma_key.py" \
  --input "<source-image>" \
  --out "<workspace>/<asset-name>.png" \
  --auto-key border \
  --soft-matte \
  --spill-cleanup \
  --edge-feather 0.5 \
  --force

python3 "<skill-dir>/scripts/validate_icon.py" \
  "<workspace>/<asset-name>.png" \
  --require-transparent-corners
```

Use a `.webp` output path when lossless WebP is contracted; the utility preserves alpha and writes WebP losslessly.

If the source already has clean transparency, preserve it and skip chroma-key removal. For an exact requested size or a set whose source dimensions differ, normalize each transparent result to one shared canvas:

```bash
python3 "<skill-dir>/scripts/normalize_raster_icon.py" \
  --input "<transparent-source>" \
  --out "<workspace>/<asset-name>.png" \
  --canvas-size "<shared-pixel-size>" \
  --padding 12 \
  --force
```

## Tune only when evidence requires it

- Add `--edge-contract 1` when a key-colored fringe remains.
- Reduce `--edge-feather` toward `0.25` when edges look soft; raise it cautiously when a hard cutout is visible.
- Set `--key-color "#rrggbb" --auto-key none` when border sampling selects the wrong color.
- Add `--trim --padding 12` only when the source has excessive transparent margins. If one set member is trimmed, normalize every member to one shared square canvas before delivery.
- Adjust `--transparent-threshold` and `--opaque-threshold` only after inspecting partial-alpha edges.
- Regenerate the source when lighting, texture, or shadows vary across the backdrop. Matte tuning cannot reliably repair a non-uniform background.

Keep the smallest change that fixes the observed defect and record the successful parameters in the workspace.

## Validate visually

Preview the output over light, dark, and high-contrast backgrounds at the smallest intended size. Confirm transparent corners, a nonempty opaque subject, clean hairline/detail edges, no key-color fringe, no clipped antialiasing, and consistent optical padding across the set.

For a set, retain the same square source dimensions rather than trimming each subject to a different canvas, then run:

```bash
python3 "<skill-dir>/scripts/validate_icon.py" \
  "<asset-1>.png" "<asset-2>.png" "<asset-n>.png" \
  --require-transparent-corners \
  --require-matching-canvas
```
