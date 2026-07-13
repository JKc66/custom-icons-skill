---
name: custom-icons
description: Create or refine custom icon assets as native or traced SVGs and transparent PNG/WebP files. Use when the user asks for a bespoke icon or cohesive icon set, wants an image traced into a clean vector, or needs a detailed or 3D icon with transparency.
---

# Custom Icons

Build each icon through an inspectable source-to-asset pipeline. Treat the user's stated subject, style, palette, format, dimensions, and destination as the asset contract.

## Workflow

### 1. Establish the asset contract

Inspect the request, supplied references, and target project before asking questions. Infer routine details with these defaults:

- Match a supplied reference or existing icon set before introducing a new style.
- Choose SVG for monochrome silhouettes, line art, and simple UI artwork.
- Choose transparent PNG or lossless WebP for 3D, multicolor, shaded, or textured artwork.
- Use a square `24×24` coordinate system for unspecified UI SVGs and `1024×1024` for unspecified detailed illustrative SVGs.
- Use black for an unspecified vector color and preserve the generated/source dimensions for an unspecified raster size.
- Save final assets in the request workspace when no destination is given.

Ask one concise question only when the subject is missing, requirements conflict, or the format choice would materially change the requested appearance. A target framework is optional unless implementation or framework-specific packaging is requested.

For each asset, determine the subject, branch, style anchor, palette, format, and final location. This step is complete when every field is stated or safely inferred and no material conflict remains.

### 2. Choose one branch per asset

- **Traced vector:** Use when a raster source must become SVG or when a new icon needs an organic, hand-drawn, or generated silhouette. Read [references/vector-workflow.md](references/vector-workflow.md) before generating or processing the asset.
- **Transparent raster:** Use for detailed, 3D, multicolor, shaded, or textured artwork. Read [references/raster-workflow.md](references/raster-workflow.md) before generating or processing the asset.
- **Native vector:** Use for an existing vector source, deterministic geometric/UI artwork, or a detailed SVG that can be expressed faithfully with vector fills, gradients, and effects. Read [references/native-vector-workflow.md](references/native-vector-workflow.md) before creating or editing the asset.

Classify mixed icon sets asset by asset; a set may legitimately contain both SVG and raster outputs. Keep the user's requested format when feasible. If the requested format would discard essential visual detail, explain the tradeoff and resolve it before generation.

This step is complete when every asset has exactly one pipeline and the pipeline can produce its contracted format.

### 3. Prepare sources and workspace

Resolve `<skill-dir>` to the directory containing this `SKILL.md`; invoke bundled scripts with `<skill-dir>/scripts/...`, not a path assumed to exist in the user's project.

Create `tmp/custom-icons/<request-slug>/` in the target project. Use filesystem-safe, lowercase names with hyphens for request and asset slugs. Keep prompts, generated sources, processed previews, trace drafts, and validation artifacts there. Preserve these intermediates until the user asks for cleanup, and avoid overwriting an existing final asset unless the request authorizes replacement.

When references are supplied, assign each one a role such as `edit target`, `style reference`, or `palette reference`. Preserve the edit target's identity, silhouette, proportions, and composition except where the request explicitly changes them.

For a set of three or more icons, create one representative pilot first. Confirm its silhouette, style, palette, padding, and small-size legibility before producing the rest, then reuse that visual contract for every asset.

This step is complete when the workspace exists, inputs have explicit roles, and any multi-icon set has a validated pilot.

### 4. Generate and process

Use the selected branch reference as the single source of truth for its prompt and commands. Generate one isolated asset per source image. When an image-generation or editing tool is unavailable, continue from a user-supplied source; if no source exists, report that generation is the blocking step.

Keep all branch attempts in the workspace. Tune the source or processing parameters when the first result misses the contract; do not conceal a failed attempt by switching formats.

This step is complete when every contracted final file exists in the workspace and was produced by its selected pipeline.

### 5. Validate every asset

Run the bundled validator on each output:

```bash
python3 "<skill-dir>/scripts/validate_icon.py" "<final-asset>"
```

For an icon set, also validate all outputs from each branch together:

```bash
python3 "<skill-dir>/scripts/validate_icon.py" \
  "<asset-1>" "<asset-2>" "<asset-n>" \
  --require-matching-canvas
```

Then inspect each icon visually at its intended display size and compare it with the request and any references. Check:

- recognizable subject and clean silhouette;
- consistent canvas, optical size, padding, palette, perspective, and stroke/detail weight across a set;
- crisp vector geometry without stray paths or lost details;
- clean raster transparency without key-color spill, clipped edges, or unintended shadows;
- legibility at the smallest intended size.

Unless the user requests variable artboards, require identical pixel dimensions for raster members and an identical `viewBox`, width, and height coordinate system for SVG members.

Iterate on any failed asset and rerun both checks. This step is complete only when the validator passes and every asset passes the visual checklist; a set is incomplete if any member fails.

### 6. Deliver and report

Copy only validated final assets to the contracted destination.

Report the branch used, final paths, workspace path, validation result, and any deliberate deviation from the request. Include integration code only when requested or when the target environment requires non-obvious usage.

Delivery is complete when every promised asset is present at its reported path and every validation result is accounted for.
